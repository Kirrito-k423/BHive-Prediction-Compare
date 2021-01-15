#define _GNU_SOURCE
#include <errno.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>   /* for memset */
#include <sys/mman.h> /* for mprotect, PROT_* */
#include <sys/ptrace.h>
#include <sys/resource.h> /* for PRIO_PROCESS */
#include <sys/user.h>     /* for user_regs_struct, PAGE_SIZE, PAGE_SHIFT */
#include <sys/wait.h>
#include <unistd.h>

#include <sched.h> /* for pinning child process */

#include <perfmon/pfmlib_perf_event.h>

#include "harness.h"
#include "runtest.h"
#include "tail_template.h"

/*
 * Address of page to be used for child stack.
 */
#define STACK_ADDR (void *)0x0000700000000000

static int read_child_regs(pid_t child, struct user_regs_struct *regs) {
#ifdef __x86_64__
  return ptrace(PTRACE_GETREGS, child, NULL, regs);
#endif
}

static int set_child_regs(pid_t child, struct user_regs_struct *regs) {
#ifdef __x86_64__
  return ptrace(PTRACE_SETREGS, child, NULL, regs);
#endif
}

/**
 * Move child stack to stack_page_addr.
 *
 * @return 0 when successful. -1 if error while reading child registers.
 *         -2 if error copying stack values. -3 if error setting child
 *         registers. Errno set by syscall that produced the error.
 */
static int move_child_stack(pid_t child, void *stack_page_addr) {
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
  long *ori_bp = (long *)regs.rbp;
  long *ori_sp = (long *)regs.rsp;
  /* Copy stack values */
  errno = 0;
  for (long *p = ori_sp, *new_p = stack_page_addr; p < ori_bp; p++, new_p++) {
    long word = ptrace(PTRACE_PEEKDATA, child, p, NULL);
    ptrace(PTRACE_POKEDATA, child, new_p, word);
  }
  if (errno != 0) {
    return -2;
  }
  /* Move stack */
  unsigned long long stack_size = regs.rbp - regs.rsp;
  regs.rbp = (unsigned long long)stack_page_addr + PAGE_SIZE;
  regs.rsp = regs.rbp - stack_size;
  ret = set_child_regs(child, &regs);
  if (ret == -1) {
    return -3;
  }
  return 0;
#endif
}

static void *get_page_start(void *addr) {
  return (void *)(((unsigned long)addr >> PAGE_SHIFT) << PAGE_SHIFT);
}

static void *get_page_end(void *addr) {
  return get_page_start(addr) + PAGE_SIZE;
}

int measure(char *code_to_test, unsigned long code_size,
            unsigned int unroll_factor, measure_results_t *res) {
  pid_t child = fork();
  if (child == -1) { /* Error */
    perror("[PARENT, ERR] Cannot create child with fork");
    kill(child, SIGKILL);
    return -1;

  } else if (child != 0) { /* Parent program */
    int ret;

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
      printf("[PARENT, ERR] Child not stopped by SIGSTOP.\n");
      kill(child, SIGKILL);
      return -1;
    }

    /*
    Prepare child for testing block.
    TODO:
      - move child stack
      - set child rip to execute test code
    */

    /* Move child stack */
    unsigned long unrolled_block_size = code_size * unroll_factor;
    unsigned long tail_size = tail_end - tail_start;
    void *test_block_end = test_block + unrolled_block_size + tail_size;
    void *stack_page_addr = get_page_end(test_block_end);
    ret = move_child_stack(child, stack_page_addr);
    if (ret == -1) {
      perror("[PARENT, ERR] Error reading child registers while moving stack");
    } else if (ret == -2) {
      perror("[PARENT, ERR] Error copying stack values while moving stack");
    } else if (ret == -3) {
      perror("[PARENT, ERR] Error setting child registers while moving stack");
    }
    if (ret != 0) {
      kill(child, SIGKILL);
      return -1;
    }
    printf("[PARENT] Child stack moved.\n");

    kill(child, SIGKILL);
    return -1;

  } else { /* Child program */
    int ret;

    /* Copy test block and tail */
    void *runtest_page_start = get_page_start(runtest);
    unsigned long unrolled_block_size = code_size * unroll_factor;
    unsigned long tail_size = tail_end - tail_start;
    void *runtest_page_end =
        get_page_end(test_block + unrolled_block_size + tail_size);

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
    memcpy(block_ptr, tail_start, tail_end - tail_start);

    mprotect(runtest_page_start, runtest_page_end - runtest_page_start,
             PROT_EXEC);
    if (ret == -1) {
      perror("[CHILD] Error protecting test code");
    }

    /* Allocate memory for stack after unmapping.
     *
     * The stack is setup at the end of the last page containing runtest. If
     * there is less than CHILD_STACK_SIZE bytes left, a new page is allocated.
     */
    void *stack_top =
        mmap(STACK_ADDR, PAGE_SIZE, PROT_READ | PROT_WRITE,
             MAP_PRIVATE | MAP_FIXED_NOREPLACE | MAP_ANONYMOUS, -1, 0);
    if (stack_top == (void *)-1) {
      perror("[CHILD] Error mapping memory for stack");
    }
    printf("[CHILD] Stack page mapped.\n");

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
    printf("[CHILD] Perf. events opened.\n");

    /* Pin this process */
    cpu_set_t cpu_set;
    CPU_ZERO(&cpu_set);
    CPU_SET(1, &cpu_set);
    sched_setaffinity(0, sizeof(cpu_set_t), &cpu_set);
    setpriority(PRIO_PROCESS, 0, 0);
    printf("[CHILD] Process pinned\n");

    /* Let parent trace this child */
    ret = ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    if (ret == -1) {
      perror("[CHILD, ERR] PTRACE_TRACEME error");
      exit(EXIT_FAILURE);
    }

    runtest();
  }
}
