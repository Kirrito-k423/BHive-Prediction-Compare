#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>     /* for O_RDWR, O_CREAT */
#include <linux/elf.h> /* for NT_PRSTATUS */
#include <sched.h>     /* for pinning child process */
#include <signal.h>
#include <stdlib.h>
#include <string.h>   /* for memset */
#include <sys/mman.h> /* for mprotect, PROT_* */
#include <sys/ptrace.h>
#include <sys/resource.h> /* for PRIO_PROCESS */
#include <sys/signal.h>   /* for siginfo_t */
#include <sys/user.h>     /* for user_regs_struct */
#include <sys/wait.h>
#include <unistd.h>

#include <perfmon/pfmlib_perf_event.h>

#include "common.h"
#include "harness.h"
#include "runtest.h"

static int read_child_regs(pid_t child, struct user_regs_struct *regs) {
#ifdef __x86_64__
  return ptrace(PTRACE_GETREGS, child, NULL, regs);
#else
  struct iovec iov;
  iov.iov_base = regs;
  iov.iov_len = sizeof(struct user_regs_struct);
  return ptrace(PTRACE_GETREGSET, child, NT_PRSTATUS, &iov);
#endif
}

static int set_child_regs(pid_t child, struct user_regs_struct *regs) {
#ifdef __x86_64__
  return ptrace(PTRACE_SETREGS, child, NULL, regs);
#else
  struct iovec iov;
  iov.iov_base = regs;
  iov.iov_len = sizeof(struct user_regs_struct);
  return ptrace(PTRACE_SETREGSET, child, NT_PRSTATUS, &iov);
#endif
}

static int set_child_pc(pid_t child, void *pc) {
  struct user_regs_struct regs;
  int ret = read_child_regs(child, &regs);
  if (ret == -1) {
    return -1;
  }
#ifdef __x86_64__
  regs.rip = (unsigned long long)pc;
#elif __aarch64__
  regs.pc = (unsigned long long)pc;
#else
#pragma GCC error "set_child_pc not implemented for this architecture"
#endif
  ret = set_child_regs(child, &regs);
  if (ret == -1) {
    return -1;
  }
  return ret;
}

static void *get_child_pc(pid_t child) {
  struct user_regs_struct regs;
  int ret = read_child_regs(child, &regs);
  if (ret == -1) {
    return (void *)-1;
  }
#ifdef __x86_64__
  return (void *)regs.rip;
#elif __aarch64__
  return (void *)regs.pc;
#else
#pragma GCC error "get_child_pc not implemented for this architecture"
#endif
}

/**
 * Save child stack pointer and base pointer.
 *
 * @return 0 when successful. -1 if error while reading child registers.
 */
static int save_child_stack(pid_t child, void *child_aux_mem) {
#ifdef __x86_64__
  /*
   * x86 stack grows downward so base pointer (rbp) is at higher address than
   * stack pointer (rsp).
   */
  struct user_regs_struct regs;
  int ret = read_child_regs(child, &regs);
  if (ret == -1) {
    return -1;
  }
  *(unsigned long *)(child_aux_mem + STACK_BP_OFFSET) = regs.rbp;
  *(unsigned long *)(child_aux_mem + STACK_SP_OFFSET) = regs.rsp;
  return 0;
#elif __aarch64__
  /*
   * ARM64 stack grows downward so base pointer (r29) is at higher address than
   * stack pointer (sp).
   */
  struct user_regs_struct regs;
  int ret = read_child_regs(child, &regs);
  if (ret == -1) {
    return -1;
  }
  *(unsigned long *)(child_aux_mem + STACK_BP_OFFSET) = regs.regs[29];
  *(unsigned long *)(child_aux_mem + STACK_SP_OFFSET) = regs.sp;
  return 0;
#else
#pragma GCC error                                                              \
    "move_child_stack (in harness.c) is not implemented for this architecture"
#endif
}

static int move_child_to_map_and_restart(pid_t child, void *fault_addr,
                                         void *child_aux) {
  int ret = set_child_pc(child, map_and_restart);
  if (ret == -1) {
    perror("error setting child pc");
  }
  *(void **)(child_aux + MAP_AND_RESTART_ADDR_OFFSET) = fault_addr;
  return ret;
}

#ifdef __x86_64__
#define SIZE_OF_REL_JUMP 5
#elif __aarch64__
#define SIZE_OF_REL_JUMP 4
#endif

static size_t insert_jump_to_test_start(void *addr) {
#ifdef __x86_64__
  *(char *)addr = 0xe9;
  *(int *)(addr + 1) = (long)test_start - (long)addr - SIZE_OF_REL_JUMP;
  return SIZE_OF_REL_JUMP;
#elif __aarch64__
  unsigned int instr = 0x14 << 24;
  int jump_in_words = ((long)test_start - (long)addr) / 4;
  /* Only bits 0:25 */
  instr |= (jump_in_words & 0x03ffffff);
  *(unsigned int *)(addr) = instr;
#else
#pragma GCC error                                                              \
    "insert_jump_to_test_start not implemented for this architecture"
#endif
}

static int aux_mem_overlap(void *test_page_start, void *test_page_end) {
  void *aux_page_end = AUX_MEM_ADDR + PAGE_SIZE;
  void *aux_page_start = AUX_MEM_ADDR;
  return !(test_page_start >= aux_page_end || test_page_end <= aux_page_start);
}

static void *get_page_start(void *addr) {
  return (void *)(((unsigned long)addr >> PAGE_SHIFT) << PAGE_SHIFT);
}

static void *get_page_end(void *addr) {
  return get_page_start(addr) + PAGE_SIZE;
}

int measure(char *code_to_test, unsigned long code_size,
            unsigned int unroll_factor, measure_results_t *res) {
  /* Create shared memory */
  mode_t mode = 0777; // Everyone has read, write, execute permission
  int shm_fd = shm_open("/bhive_shm", O_RDWR | O_CREAT, mode);
  if (shm_fd == -1) {
    perror("[PARENT, ERR] Error creating shared memory");
    return -1;
  }

  shm_unlink("/bhive_shm");
  ftruncate(shm_fd, SHARED_MEM_SIZE);
  dup2(shm_fd, SHM_FD);
  close(shm_fd);

  pid_t child = fork();
  if (child == -1) { /* Error */
    perror("[PARENT, ERR] Cannot create child with fork");
    kill(child, SIGKILL);
    return -1;

  } else if (child != 0) { /* Parent program */
    int ret;

    /* Map shared memory */
    void *child_mem =
        mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, SHM_FD, 0);
    if (child_mem == (void *)-1) {
      perror("[PARENT, ERR] Error mapping child page portion of shared memory");
      kill(child, SIGKILL);
      return -1;
    }
    void *child_aux = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
                           SHM_FD, PAGE_SIZE);
    if (child_aux == (void *)-1) {
      perror("[PARENT, ERR] Error mapping child aux. memory portion of shared "
             "memory");
      kill(child, SIGKILL);
      return -1;
    }

    /*
     * Wait for child. When child stops execution using kill(getpid(), SIGSTOP),
     * it is already in runtest.c::runtest().
     */
    int child_stat;
    if (wait(&child_stat) == -1) {
      perror("[PARENT, ERR] Wait error");
      kill(child, SIGKILL);
      return -1;
    }

    if (!WIFSTOPPED(child_stat)) {
      printf("hm\n");
      printf("[PARENT, ERR] Child not stopped by SIGSTOP.\n");
      kill(child, SIGKILL);
      return -1;
    }

    ret = save_child_stack(child, child_aux);
    if (ret == -1) {
      perror("[PARENT, ERR] Error reading child registers while saving stack");
      kill(child, SIGKILL);
      return -1;
    }
    void *child_stack_sp = *(void **)(child_aux + STACK_SP_OFFSET);
    printf("[PARENT] Child stack at %p saved.\n", child_stack_sp);

    for (int i = 0; i < MAX_FAULTS; i++) {
      ptrace(PTRACE_CONT, child, 0, 0);
      if (wait(&child_stat) == -1) {
        perror("[PARENT, ERR] Wait error");
        kill(child, SIGKILL);
        return -1;
      }

      siginfo_t sinfo;
      ptrace(PTRACE_GETSIGINFO, child, 0, &sinfo);
      if (sinfo.si_signo == SIGSEGV) {
        printf("[PARENT] Child segfaulted at address %p. Mapping and "
               "restarting...\n",
               sinfo.si_addr);
        ret = move_child_to_map_and_restart(child, sinfo.si_addr, child_aux);
        if (ret == -1) {
          perror("[PARENT, ERR] Error moving child to map_and_restart");
        }
        continue;
      }
      printf("Signo: %d\n", sinfo.si_signo);
      printf("Addr: %p\n", sinfo.si_addr);
      printf("core cyc: %lu\n", *(uint64_t *)(child_aux + CYC_COUNT_OFFSET));
      res->core_cyc = *(uint64_t *)(child_aux + CYC_COUNT_OFFSET);
      kill(child, SIGKILL);
      return 0;
    }
    printf("[PARENT] Max faults reached. Giving up...\n");

    kill(child, SIGKILL);
    return -1;
  } else { /* Child program */
    int ret;

    /* Let parent trace this child */
    ret = ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    if (ret == -1) {
      perror("[CHILD, ERR] PTRACE_TRACEME error");
      exit(EXIT_FAILURE);
    }

    /* Copy test block and tail */
    void *runtest_page_start = get_page_start(runtest);
    unsigned long unrolled_block_size = code_size * unroll_factor;
    unsigned long tail_size = tail_end - tail_start;
    void *runtest_page_end = get_page_end(test_block + unrolled_block_size +
                                          tail_size + SIZE_OF_REL_JUMP);

    ret = mprotect(runtest_page_start, runtest_page_end - runtest_page_start,
                   PROT_READ | PROT_WRITE | PROT_EXEC);
    if (ret == -1) {
      perror("[CHILD] Error unprotecting test code");
    }

    char *block_ptr = (char *)test_block;
    for (int i = 0; i < unroll_factor; i++) {
      memcpy(block_ptr, code_to_test, code_size);
      block_ptr += code_size;
    }
    void *pbreak = sbrk(0);
    memcpy(block_ptr, tail_start, tail_size);
    block_ptr += tail_size;
    block_ptr += insert_jump_to_test_start(block_ptr);

    mprotect(runtest_page_start, runtest_page_end - runtest_page_start,
             PROT_EXEC);
    if (ret == -1) {
      perror("[CHILD] Error protecting test code");
    }
    printf("\n[CHILD] Test block and tail copied.\n");

    if (aux_mem_overlap(runtest_page_start, runtest_page_end)) {
      printf("[CHILD, ERR] Aux. memory and test pages overlap. Move aux. "
             "memory somewhere else\n");
      kill(getpid(), SIGKILL);
    }

    /* Allocate aux. memory for use after unmapping.
     *
     * A new stack for child will be setup at the end of the aux. memory.
     * Counter values will be stored at the beginning of the aux. memory.
     */
    void *aux_addr = mmap(AUX_MEM_ADDR, PAGE_SIZE, PROT_READ | PROT_WRITE,
                          MAP_SHARED, SHM_FD, PAGE_SIZE);
    if (aux_addr == (void *)-1) {
      perror("[CHILD, ERR] Error mapping memory for aux. memory");
    }
    printf("[CHILD] Aux. page mapped at %p.\n", aux_addr);

    /* Get perf encoding */
    pfm_initialize();
    struct perf_event_attr perf_attr;
    memset(&perf_attr, 0, sizeof(struct perf_event_attr));
    perf_attr.size = sizeof(struct perf_event_attr);
    pfm_perf_encode_arg_t pfm_arg;
    pfm_arg.attr = &perf_attr;
    pfm_arg.fstr = NULL;
    pfm_arg.size = sizeof(pfm_perf_encode_arg_t);
    ret = pfm_get_os_event_encoding("cycles:u", PFM_PLM0 | PFM_PLM3,
                                    PFM_OS_PERF_EVENT, &pfm_arg);
    if (ret != PFM_SUCCESS) {
      printf("[CHILD, ERR] Cannot get encoding: %s\n", pfm_strerror(ret));
      exit(EXIT_FAILURE);
    }
    /* Open perf event */
    perf_attr.read_format =
        PERF_FORMAT_TOTAL_TIME_ENABLED | PERF_FORMAT_TOTAL_TIME_RUNNING;
    perf_attr.disabled = 1; // Don't start immediately after opening
    int perf_fd = perf_event_open(&perf_attr, getpid(), -1, -1, 0);
    if (perf_fd < 0) {
      perror("[CHILD, ERR] Cannot create perf events");
      exit(EXIT_FAILURE);
    }
    *(int *)(aux_addr + PERF_FD_OFFSET) = perf_fd;
    printf("[CHILD] Perf. events opened.\n");

    /* Pin this process */
    cpu_set_t cpu_set;
    CPU_ZERO(&cpu_set);
    CPU_SET(1, &cpu_set);
    sched_setaffinity(0, sizeof(cpu_set_t), &cpu_set);
    setpriority(PRIO_PROCESS, 0, 0);
    printf("[CHILD] Process pinned\n");

    /* Save parameters */
    *(uint64_t *)(aux_addr + ITERATIONS_OFFSET) = ITERATIONS;
    *(int *)(aux_addr + PERF_FD_OFFSET) = perf_fd;
    *(void **)(aux_addr + TEST_PAGE_END_OFFSET) = runtest_page_end;
    *(long *)(aux_addr + INIT_VALUE_OFFSET) = INIT_VALUE;

    runtest();
  }
}
