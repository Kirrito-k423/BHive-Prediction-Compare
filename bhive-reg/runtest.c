/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "common.h"
#include "runtest_redefines.h"

uint64_t global_8byte_data = -1;
uint64_t *global_p = &global_8byte_data;

#ifdef __x86_64__
#define JUMP_TO_ASM_LABEL(l) asm __volatile__("jmp " #l)
#elif __aarch64__
#define JUMP_TO_ASM_LABEL(l) asm __volatile__("b " #l)
#endif

/**
 * Initialize memory in page INIT_VALUE to INIT_VALUE
 */
ALWAYS_INLINE void initialize_memory() {
  for (long *p = (long *)INIT_VALUE; p < (long *)(INIT_VALUE + PAGE_SIZE);
       p++) {
    *p = INIT_VALUE;
  }
}

/**
 * Initialize registers:
 *  - Enable flush-to-zero
 *  - Clear flags (where applicable)
 *  - Initialize registers to INIT_VALUE
 *  - Point base pointer and stack pointer to middle of initial page at
 *    INIT_VALUE
 */
ALWAYS_INLINE void initialize_registers() {
#ifdef __x86_64__
  /* Enable flush-to-zero and denormals-are-zero */
  asm __volatile__("mov %0, %%rsp\n\t"
                   "stmxcsr (%%rsp)\n\t"
                   "orl $0x8000, (%%rsp)\n\t"
                   "ldmxcsr (%%rsp)\n\t"
                   "stmxcsr (%%rsp)\n\t"
                   "orl $0x40, (%%rsp)\n\t"
                   "ldmxcsr (%%rsp)"
                   : /* No output */
                   : "n"(INIT_VALUE + PAGE_SIZE / 2));
  /* Clear flags */
  asm __volatile__("xor %rax, %rax\n\t"
                   "sahf");
  /* Initialize registers */
  asm __volatile__("mov %[init_value], %%rax\n\t"
                   "mov %[init_value], %%rbx\n\t"
                   "mov %[init_value], %%rcx\n\t"
                   "mov %[init_value], %%rdx\n\t"
                   "mov %[init_value], %%rsi\n\t"
                   "mov %[init_value], %%rdi\n\t"
                   "mov %[init_value], %%r8\n\t"
                   "mov %[init_value], %%r9\n\t"
                   "mov %[init_value], %%r10\n\t"
                   "mov %[init_value], %%r11\n\t"
                   "mov %[init_value], %%r12\n\t"
                   "mov %[init_value], %%r13\n\t"
                   "mov %[init_value], %%r14\n\t"
                   "mov %[init_value], %%r15\n\t"
                   : /* No output */
                   : [init_value] "n"(INIT_VALUE));
  /* Move rbp, rsp to middle of page */
  asm __volatile__("mov %rax, %rbp\n\t"
                   "add $2048, %rax\n\t"
                   "mov %rbp, %rsp");
#elif __aarch64__
  /* Enable flush-to-zero */
  asm __volatile__("mrs x0, FPCR\n\t"
                   "orr x0, x0, #0x01000000\n\t"
                   "msr FPCR, x0");
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
#if 1
  asm __volatile__("mov sp, x0\n\t"
                   "add sp, sp, %0"
                   : /* No output */
                   : "n"(PAGE_SIZE / 2));
#endif
#else
#pragma GCC error "initialize_registers not implemented for this architecture"
#endif
}

/**
 * Modify the stack pointer and base pointer registers to point to the stack.
 */
ALWAYS_INLINE void recover_stack() {
#ifdef __x86_64__
  asm __volatile__(
      "mov %[aux_mem], %%rbp\n\t"
      "mov %%rbp, %%rsp\n\t"
      "add %[stack_bp_offset], %%rbp\n\t"
      "add %[stack_sp_offset], %%rsp\n\t"
      "mov (%%rbp), %%rbp\n\t"
      "mov (%%rsp), %%rsp"
      : /* No output */
      : [aux_mem] "n"(AUX_MEM_ADDR), [stack_bp_offset] "n"(STACK_BP_OFFSET),
        [stack_sp_offset] "n"(STACK_SP_OFFSET));
#elif __aarch64__
  asm __volatile__("mov x0, %0\n\t"
                   "ldr x0, [x0, %1]\n\t"
                   "mov sp, x0"
                   : /* No output */
                   : "n"(AUX_MEM_ADDR), "n"(STACK_SP_OFFSET));
#else
#pragma GCC error "recover_stack not implemented for this architecture"
#endif
}

/**
 * Prevent the process from reading or writing to aux. memory and the stack.
 */
ALWAYS_INLINE void protect_aux_stack() {
  void *stack_start = *(void **)(AUX_MEM_ADDR + STACK_SP_OFFSET);
#ifdef __x86_64__
  /* mprotect(aux_start, PAGE_SIZE, PROT_NONE) */
  asm __volatile__("mov %0, %%rax\n\t"
                   "mov %1, %%rdi\n\t"
                   "mov %2, %%rsi\n\t"
                   "mov %3, %%rdx\n\t"
                   "syscall"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(PAGE_SIZE),
                     "n"(PROT_NONE));
  /* mprotect(stack_start, PAGE_SIZE, PROT_NONE) */
  asm __volatile__("mov %0, %%rax\n\t"
                   "mov %1, %%rdi\n\t"
                   "mov %2, %%rsi\n\t"
                   "mov %3, %%rdx\n\t"
                   "syscall"
                   : /* No output */
                   : "n"(SYS_mprotect), "rmn"(stack_start), "n"(PAGE_SIZE),
                     "n"(PROT_NONE));
#elif __aarch64__
  /* mprotect(aux_start, PAGE_SIZE, PROT_NONE) */
  asm __volatile__("mov x8, %0\n\t"
                   "mov x0, %1\n\t"
                   "mov x1, %2\n\t"
                   "mov x2, %3\n\t"
                   "svc #0"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(PAGE_SIZE),
                     "n"(PROT_NONE));
  /* mprotect(stack_start, PAGE_SIZE, PROT_NONE) */
  asm __volatile__("mov x8, %0\n\t"
                   "ldr x0, %1\n\t"
                   "mov x1, %2\n\t"
                   "mov x2, %3\n\t"
                   "svc #0"
                   : /* No output */
                   : "n"(SYS_mprotect), "m"(stack_start), "n"(PAGE_SIZE),
                     "n"(PROT_NONE));
#else
#pragma GCC error "protect_aux_stack not implemented for this architecture"
#endif
}

/**
 * Allow the process to read and write to aux. memory and the stack.
 */
ALWAYS_INLINE void unprotect_aux_stack() {
#ifdef __x86_64__
  /* mprotect(aux_start, PAGE_SIZE, PROT_WRITE | PROT_READ) */
  asm __volatile__("mov %0, %%rax\n\t"
                   "mov %1, %%rdi\n\t"
                   "mov %2, %%rsi\n\t"
                   "mov %3, %%rdx\n\t"
                   "syscall"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(PAGE_SIZE),
                     "n"(PROT_WRITE | PROT_READ));
  /* mprotect(stack_start, PAGE_SIZE, PROT_WRITE | PROT_READ) */
  asm __volatile__("mov %0, %%rax\n\t"
                   "mov %1, %%rdi\n\t"
                   "add %2, %%rdi\n\t"
                   "mov (%%rdi), %%rdi\n\t"
                   "mov %3, %%rsi\n\t"
                   "mov %4, %%rdx\n\t"
                   "syscall"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(STACK_SP_OFFSET),
                     "n"(PAGE_SIZE), "n"(PROT_WRITE | PROT_READ));
#elif __aarch64__
  /* mprotect(aux_start, PAGE_SIZE, PROT_WRITE | PROT_READ) */
  asm __volatile__("mov x8, %0\n\t"
                   "mov x0, %1\n\t"
                   "mov x1, %2\n\t"
                   "mov x2, %3\n\t"
                   "svc #0"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(PAGE_SIZE),
                     "n"(PROT_WRITE | PROT_READ));
  /* mprotect(stack_start, PAGE_SIZE, PROT_WRITE | PROT_READ) */
  asm __volatile__("mov x8, %0\n\t"
                   "mov x0, %1\n\t"
                   "add x0, x0, %2\n\t"
                   "ldr x0, [x0]\n\t"
                   "mov x1, %3\n\t"
                   "mov x2, %4\n\t"
                   "svc #0"
                   : /* No output */
                   : "n"(SYS_mprotect), "n"(AUX_MEM_ADDR), "n"(STACK_SP_OFFSET),
                     "n"(PAGE_SIZE), "n"(PROT_WRITE | PROT_READ));
#else
#pragma GCC error "unprotect_aux_stack not implemented for this architecture"
#endif
}

void runtest() {
  kill(getpid(), SIGSTOP);
  JUMP_TO_ASM_LABEL(runtest_start);

  /**
   * Code to be copied to the end of test block.
   */
  asm __volatile__(".global tail_start\n\ttail_start:");
  {
  uint64_t count = 0;
#if 0
    asm __volatile__("isb\n\t"
                     "mrs x1, pmevcntr0_el0\n\t"
                     "ldr x0, %1\n\t"
                     "mov sp, x0\n\t"
                     "ldr x0, [sp, 0]\n\t"
                    //  "sub %0, x1, x0"
                    "sub %0, x1, #0"
                     : "=r"(count) /* No output */
                     : "m"(global_p));
#endif
    asm __volatile__(
                     "isb\n\t"
                     "mrs x0, pmevcntr0_el0\n\t"
                     "add %0, x0, #0\n\t"
                     : "=r"(count)
                     :);
    
    unprotect_aux_stack();
    *(uint64_t *)(AUX_MEM_ADDR + CYC_COUNT_OFFSET) = count;
    *(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) -= 1;
    recover_stack();

    // Disable pmu event
    asm volatile("msr pmcntenset_el0, %0" : : "r"(0 << 31));

#if 0
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
#endif
  }
  asm __volatile__(".global tail_end\n\ttail_end:");

  /**
   * Map page containing accessed address and restart.
   * Parent process will move child pc to this label when segfault happens.
   */
  asm __volatile__(".global map_and_restart\n\t map_and_restart:");
  {
    unprotect_aux_stack();
    recover_stack();

    void *addr = *(void **)(AUX_MEM_ADDR + MAP_AND_RESTART_ADDR_OFFSET);
    mmap(get_page_start(addr), PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
         SHM_FD, 0);

#if 0
    /* Stop performance counters */
    int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
    disable_pmu(perf_fd);
#endif
    JUMP_TO_ASM_LABEL(test_start);
  }

  /**
   * The actual start of function runtest
   */
  asm __volatile__(".global runtest_start\n\t runtest_start:");

  /* Unmap pages except this one, the stack, and aux. memory.
   * Assumption:
   *  - stack grows downward and is placed at the top of address space.
   *  - no overlap between runtest, stack, and aux. memory (checked in
   *    harness.c)
   */

  void *stack_sp = *(void **)(AUX_MEM_ADDR + STACK_SP_OFFSET);
  void *stack_page_start = get_page_start(stack_sp);
  void *stack_bp = *(void **)(AUX_MEM_ADDR + STACK_BP_OFFSET);
  void *stack_page_end = get_page_end(stack_bp);
  void *test_page_end = *(void **)(AUX_MEM_ADDR + TEST_PAGE_END_OFFSET);
  void *test_page_start = get_page_start(runtest);
  void *aux_page_start = AUX_MEM_ADDR;
  void *aux_page_end = AUX_MEM_ADDR + PAGE_SIZE;
  if (aux_page_end <= test_page_start) {
    munmap((void *)0, (size_t)aux_page_start);
    munmap(aux_page_end, (size_t)(test_page_start - aux_page_end));
    munmap(test_page_end, (size_t)(stack_page_start - test_page_end));
  } else if (aux_page_start >= test_page_end) {
    munmap((void *)0, (size_t)test_page_start);
    munmap(test_page_end, (size_t)(aux_page_start - test_page_end));
    munmap(aux_page_end, (size_t)(stack_page_start - aux_page_end));
  } else {
    /* Aux. memory and test page overlaps. Should never be reached because this
     * is checked in harness.c::measure
     */
    kill(getpid(), SIGKILL);
  }

  /* Map memory for test block */
  mmap((void *)INIT_VALUE, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED,
       SHM_FD, 0);

  asm __volatile__(".global test_start\n\t test_start:\n\t");
  if (*(uint64_t *)(AUX_MEM_ADDR + ITERATIONS_OFFSET) == 0) {
    kill(getpid(), SIGSTOP);
  }

  initialize_memory();

#if 0
  /* Start performance counters */
  int perf_fd = *(int *)(AUX_MEM_ADDR + PERF_FD_OFFSET);
  reset_pmu(perf_fd);
  enable_pmu(perf_fd);
#endif
  protect_aux_stack();

  initialize_registers();

#if 0
  long init_value = 0x2324000;
  uint64_t zero = 0x0;

  asm volatile("ldr x0, %2\n\t"
               "mov sp, x0\n\t"
               "mov x0, #0\n\t"
               "msr pmevcntr0_el0, x0\n\t" // clear
               "isb\n\t"
               "mrs x0, pmevcntr0_el0\n\t" // Read counter
               "str x0, [sp, 0]\n\t"
               "ldr x0, %1 \n\t"
               "mov sp, x0 \n\t"       
               "add sp, sp, %0\n\t"
               : /* No output */
               : "n"(PAGE_SIZE / 2), "m"(init_value), "m"(global_p));
#endif

  asm volatile("mov x0, #0\n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
              "isb \n\t"
               "msr pmevcntr0_el0, x0\n\t" // clear
               "add x0, x1, #0"
               :
               : );
  asm __volatile__(".global test_block\n\t test_block:\n\t");
  asm(".rept 0x1000000 ; nop ; .endr");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Jump back to test_start */
}
