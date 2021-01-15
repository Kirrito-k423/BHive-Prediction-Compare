/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "common.h"
#include "runtest_redefines.h"

#define ALWAYS_INLINE __attribute__((always_inline)) static inline

#define NULL (void *)0

#define INITIALIZE_REGISTERS()                                                 \
  asm __volatile__("mov " INIT_VALUE_STR ", %rax\n\t"                          \
                   "mov " INIT_VALUE_STR ", %rbx\n\t")

typedef int pid_t;
typedef long int size_t;
typedef unsigned long int ssize_t;
typedef unsigned long int uint64_t;

ALWAYS_INLINE void *get_page_start(void *addr) {
  return (void *)(((uint64_t)addr >> PAGE_SHIFT) << PAGE_SHIFT);
}

ALWAYS_INLINE void *get_page_end(void *addr) {
  return get_page_start(addr) + PAGE_SIZE;
}

ALWAYS_INLINE long syscall(long number, void *param1, void *param2,
                           void *param3, void *param4, void *param5,
                           void *param6) {
#ifdef __x86_64__
  long ret = 0;
  asm __volatile__("mov %1, %%rax\n\t"
                   "mov %2, %%rdi\n\t"
                   "mov %3, %%rsi\n\t"
                   "mov %4, %%rdx\n\t"
                   "mov %5, %%r10\n\t"
                   "mov %6, %%r8\n\t"
                   "mov %7, %%r9\n\t"
                   "syscall\n\t"
                   "mov %%rax, %0"
                   : "=rm"(ret)
                   : "rmn"(number), "rmn"(param1), "rmn"(param2), "rmn"(param3),
                     "rmn"(param4), "rmn"(param5), "rmn"(param6));
  return ret;
#endif
}

ALWAYS_INLINE pid_t getpid(void) {
  return syscall(SYS_getpid, NULL, NULL, NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE int kill(pid_t pid, int sig) {
  return syscall(SYS_kill, (void *)(size_t)pid, (void *)(size_t)sig, NULL, NULL,
                 NULL, NULL);
}

ALWAYS_INLINE int munmap(void *addr, size_t len) {
  return syscall(SYS_munmap, addr, (void *)len, NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE ssize_t read(int fd, void *buf, size_t count) {
  return syscall(SYS_read, (void *)(size_t)fd, buf, (void *)count, NULL, NULL,
                 NULL);
}

ALWAYS_INLINE ssize_t write(int fd, const void *buf, size_t count) {
  return syscall(SYS_write, (void *)(size_t)fd, (void *)buf, (void *)count,
                 NULL, NULL, NULL);
}

ALWAYS_INLINE int enable_pmu(int fd) {
  return syscall(SYS_ioctl, (void *)(ssize_t)fd, (void *)PERF_EVENT_IOC_ENABLE,
                 NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE int disable_pmu(int fd) {
  return syscall(SYS_ioctl, (void *)(ssize_t)fd, (void *)PERF_EVENT_IOC_DISABLE,
                 NULL, NULL, NULL, NULL);
}

void runtest(int perf_fd, int shm_fd, void *test_page_end) {
  kill(getpid(), SIGSTOP);

  /* Unmap pages */
  munmap((void *)0, (size_t)get_page_start(runtest));
  /* TODO: This line causes sigsegv. Fix */
  // munmap(test_page_end, (size_t)AUX_MEM_ADDR -
  // (size_t)test_page_end);

  asm __volatile__(".global restart_point\n\t"
                   "restart_point:\n\t");

  /* Stop performance counters */
  disable_pmu(perf_fd);

  int iters = ITERATIONS;
  asm __volatile__(".global test_start\n\t"
                   "test_start:\n\t");
  iters--;
  if (iters == 0) {
    kill(getpid(), SIGSTOP);
  }
  /* Store last performance counter values */
  uint64_t values[3];
  uint64_t count;
  read(perf_fd, values, sizeof(values));
  if (values[2])
    count = (uint64_t)((double)values[0] * values[1] / values[2]);
  *(uint64_t *)(AUX_MEM_ADDR + CYC_COUNT_OFFSET) = count;
  /* Start performance counters */
  enable_pmu(perf_fd);
  /* TODO: Initialize registers */
  INITIALIZE_REGISTERS();
  asm __volatile__(".global test_block\n\t"
                   "test_block:\n\t");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Jump back to test_start */
}
