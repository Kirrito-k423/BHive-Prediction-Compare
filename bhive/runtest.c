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
#elif __aarch64__
  /* Clear flags */
  asm __volatile__("msr nzcv, xzr");

  /* Initialize registers */
  long init_value = INIT_VALUE;
  asm __volatile__("ldr x0, %0\n\t"
                   "ldr x1, %0\n\t"
                   "ldr x2, %0\n\t"
                   "ldr x3, %0\n\t"
                   "ldr x4, %0\n\t"
                   "ldr x5, %0\n\t"
                   "ldr x6, %0\n\t"
                   "ldr x7, %0\n\t"
                   "ldr x8, %0\n\t"
                   "ldr x9, %0\n\t"
                   "ldr x10, %0\n\t"
                   "ldr x11, %0\n\t"
                   "ldr x12, %0\n\t"
                   "ldr x13, %0\n\t"
                   "ldr x14, %0\n\t"
                   "ldr x15, %0\n\t"
                   "ldr x16, %0\n\t"
                   "ldr x17, %0\n\t"
                   "ldr x18, %0\n\t"
                   "ldr x19, %0\n\t"
                   "ldr x20, %0\n\t"
                   "ldr x21, %0\n\t"
                   "ldr x22, %0\n\t"
                   "ldr x23, %0\n\t"
                   "ldr x24, %0\n\t"
                   "ldr x25, %0\n\t"
                   "ldr x26, %0\n\t"
                   "ldr x27, %0\n\t"
                   "ldr x28, %0\n\t"
                   "ldr x29, %0\n\t"
                   "ldr x30, %0\n\t"
                   : /* No output */
                   : "m"(init_value));

  /* Move stack to middle of page */
  asm __volatile__("mov sp, x0\n\t"
                   "add sp, sp, #" HALF_PAGE_STR);
#else
#pragma GCC error "initialize_registers not implemented for this architecture"
#endif
}

ALWAYS_INLINE void recover_stack() {
#ifdef __x86_64__
  asm __volatile__("mov $" STACK_PAGE_ADDR_STR ", %rbp\n\t"
                   "add $2048, %rbp");
#else
#pragma GCC error "recover_stack not implemented for this architecture"
#endif
}

void runtest() {
#ifdef __x86_64__
  asm __volatile__("jmp runtest_start");
#elif __aarch64__
  asm __volatile__("b runtest_start");
#else
#pragma GCC error "runtest not implemented for this architecture"
#endif

  asm __volatile__(".global tail_start\n\ttail_start:");
  {
    recover_stack();

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
    recover_stack();

    void *addr;
#ifdef __x86_64__
    asm __volatile__("mov %%rdi, %0" : "=rm"(addr));
#elif __aarch64__
    asm __volatile__("mov x0, %0" : "=rm"(addr));
#else
#pragma GCC error "map_and_restart not implemented for this architecture"
#endif

    mmap(get_page_start(addr), PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
         SHM_FD, 0);
    /* Stop performance counters */
    int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
    disable_pmu(perf_fd);

#ifdef __x86_64__
    asm __volatile__("jmp test_start");
#elif __aarch64__
    asm __volatile__("b test_start");
#else
#pragma GCC error "map_and_restart not implemented for this architecture"
#endif
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
