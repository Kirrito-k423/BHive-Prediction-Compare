#define _GNU_SOURCE
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

#define CHILD_MEM_SIZE 512

static int read_child_regs(pid_t child, struct user_regs_struct *regs) {
#ifdef __x86_64__
  return ptrace(PTRACE_GETREGS, child, NULL, regs);
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

    /* Wait for child */
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

    struct user_regs_struct regs;
    if (read_child_regs(child, &regs) == -1) {
      perror("[PARENT, ERR] Reading child regs");
      kill(child, SIGKILL);
      return -1;
    }

    /*
    Prepare child for testing block.
    TODO:
      - move child stack
      - set child rip to execute test code
    */

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
    mprotect(runtest_page_start, runtest_page_end - runtest_page_start,
             PROT_READ | PROT_WRITE);
    char *block_ptr = test_block;
    /* Copy test block */
    for (int i = 0; i < unroll_factor; i++) {
      for (char *word = code_to_test; word < code_to_test + code_size; word++) {
        *block_ptr = *word;
        block_ptr++;
      }
    }
    /* Copy tail */
    for (char *word = tail_start; word < tail_end; word++) {
      *block_ptr = *word;
      block_ptr++;
    }
    mprotect(runtest_page_start, runtest_page_end - runtest_page_start,
             PROT_EXEC);

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
