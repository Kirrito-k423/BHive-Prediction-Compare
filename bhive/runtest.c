/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "common.h"
#include "runtest_redefines.h"

#define INITIALIZE_REGISTERS()                                                 \
  asm __volatile__("mov $" INIT_VALUE_STR ", %rax\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %rbx\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %rcx\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %rdx\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %rsi\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %rdi\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r8\n\t"                          \
                   "mov $" INIT_VALUE_STR ", %r9\n\t"                          \
                   "mov $" INIT_VALUE_STR ", %r10\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r11\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r12\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r13\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r14\n\t"                         \
                   "mov $" INIT_VALUE_STR ", %r15\n\t")

/**
 * This function contains code to be copied to the end of the test block.
 * The function tail itself is never called, but two symbols `tail_start`
 * and `tail_end` denotes the start and end of the tail code.
 */
void tail() {
  asm __volatile__(".global tail_start\n\t"
                   "tail_start:");

  /* Stop performance counters */
  int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
  disable_pmu(perf_fd);
  /* Store last performance counter values */
  uint64_t values[3];
  uint64_t count;
  read(perf_fd, values, sizeof(values));
  count = values[0];
  *(uint64_t *)(AUX_MEM_ADDR + CYC_COUNT_OFFSET) = count;

  asm __volatile(".global tail_end\n\t"
                 "tail_end:");
}

void runtest() {
  kill(getpid(), SIGSTOP);

  /* Unmap pages */
  munmap((void *)0, (size_t)get_page_start(runtest));
  void *test_page_end = *(void **)(AUX_MEM_ADDR + TEST_PAGE_END_OFFSET);
  munmap(test_page_end, (size_t)AUX_MEM_ADDR - (size_t)test_page_end);

  asm __volatile__(".global restart_point\n\t"
                   "restart_point:\n\t");

  asm __volatile__(".global test_start\n\t"
                   "test_start:\n\t");

  if (*(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) == 0) {
    kill(getpid(), SIGSTOP);
  }
  *(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) -= 1;

  /* Start performance counters */
  int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
  enable_pmu(perf_fd);

  /* Initialize registers */
  INITIALIZE_REGISTERS();
  asm __volatile__(".global test_block\n\t"
                   "test_block:\n\t");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Jump back to test_start */
}
