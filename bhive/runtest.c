/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "common.h"
#include "runtest_redefines.h"

ALWAYS_INLINE void initialize_memory() {
  for (long *p = (long *)INIT_VALUE; p < (long *)(INIT_VALUE + PAGE_SIZE);
       p++) {
    *p = INIT_VALUE;
  }
}

ALWAYS_INLINE void initialize_registers() {
#ifdef __x86_64__
  /* Clear flags */
  asm __volatile__("xor %rax, %rax\n\t"
                   "sahf");

  /* Initialize registers */
  asm __volatile__("mov $" INIT_VALUE_STR ", %rax\n\t"
                   "mov $" INIT_VALUE_STR ", %rbx\n\t"
                   "mov $" INIT_VALUE_STR ", %rcx\n\t"
                   "mov $" INIT_VALUE_STR ", %rdx\n\t"
                   "mov $" INIT_VALUE_STR ", %rsi\n\t"
                   "mov $" INIT_VALUE_STR ", %rdi\n\t"
                   "mov $" INIT_VALUE_STR ", %r8\n\t"
                   "mov $" INIT_VALUE_STR ", %r9\n\t"
                   "mov $" INIT_VALUE_STR ", %r10\n\t"
                   "mov $" INIT_VALUE_STR ", %r11\n\t"
                   "mov $" INIT_VALUE_STR ", %r12\n\t"
                   "mov $" INIT_VALUE_STR ", %r13\n\t"
                   "mov $" INIT_VALUE_STR ", %r14\n\t"
                   "mov $" INIT_VALUE_STR ", %r15\n\t");

  /* Move rbp, rsp to middle of page */
  asm __volatile__("mov %rax, %rbp\n\t"
                   "add $2048, %rax\n\t"
                   "mov %rbp, %rsp");
#endif
}

void runtest() {
  asm __volatile__("jmp runtest_start");

  asm __volatile__(".global tail_start\n\ttail_start:");
  {
    /* Move stack back */
    asm __volatile__("mov $" STACK_PAGE_ADDR_STR ", %rbp\n\t"
                     "add $2048, %rbp");

    /* Stop performance counters */
    int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
    disable_pmu(perf_fd);
    /* Store performance counter value if smaller than last one */
    struct values {
      uint64_t value;
      uint64_t time_enabled;
      uint64_t time_running;
      uint64_t id;
    } values;
    read(perf_fd, &values, sizeof(values));
    uint64_t prev_value = *(uint64_t *)(AUX_MEM_ADDR + CYC_COUNT_OFFSET);
    uint64_t new_value = values.value;
    if (prev_value != 0 && prev_value < new_value) {
      new_value = prev_value;
    }
    *(uint64_t *)(AUX_MEM_ADDR + CYC_COUNT_OFFSET) = new_value;
    *(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) -= 1;
  }
  asm __volatile__(".global tail_end\n\ttail_end:");

  asm __volatile__(".global map_and_restart\n\t map_and_restart:");
  {
    asm __volatile__("mov $" STACK_PAGE_ADDR_STR ", %rbp\n\t"
                     "add $" HALF_PAGE_STR ", %rbp");

    void *addr;
    asm __volatile__("mov %%rdi, %0" : "=rm"(addr));
    mmap(get_page_start(addr), PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
         SHM_FD, 0);
    /* Stop performance counters */
    int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
    disable_pmu(perf_fd);

    asm __volatile__("jmp test_start");
  }

  asm __volatile__(".global runtest_start\n\t runtest_start:");
  kill(getpid(), SIGSTOP);

  /* Unmap pages */
  munmap((void *)0, (size_t)get_page_start(runtest));
  void *test_page_end = *(void **)(AUX_MEM_ADDR + TEST_PAGE_END_OFFSET);
  munmap(test_page_end, (size_t)AUX_MEM_ADDR - (size_t)test_page_end);

  /* Map memory for test block */
  mmap((void *)INIT_VALUE, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
       SHM_FD, 0);

  asm __volatile__(".global test_start\n\t test_start:\n\t");

  if (*(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) == 0) {
    kill(getpid(), SIGSTOP);
  }

  initialize_memory();

  /* Start performance counters */
  int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
  reset_pmu(perf_fd);
  enable_pmu(perf_fd);

  /* Initialize registers */
  initialize_registers();
  asm __volatile__(".global test_block\n\t test_block:\n\t");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Jump back to test_start */
}
