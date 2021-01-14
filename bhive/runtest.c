/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "runtest_redefines.h"

#define NULL (void *)0

#define ITERATIONS 1

typedef int pid_t;
typedef long int size_t;
typedef unsigned long int ssize_t;

__attribute__((always_inline)) static inline long
syscall(long number, void *param1, void *param2, void *param3, void *param4,
        void *param5, void *param6) {
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

__attribute__((always_inline)) static inline pid_t getpid(void) {
  return syscall(SYS_getpid, NULL, NULL, NULL, NULL, NULL, NULL);
}

__attribute__((always_inline)) static inline int kill(pid_t pid, int sig) {
  return syscall(SYS_kill, (void *)(long int)pid, (void *)(long int)sig, NULL,
                 NULL, NULL, NULL);
}

__attribute__((always_inline)) static inline int munmap(void *addr,
                                                        size_t len) {
  return syscall(SYS_munmap, addr, (void *)len, NULL, NULL, NULL, NULL);
}

__attribute__((always_inline)) static inline ssize_t
write(int fd, const void *buf, size_t count) {
  return syscall(SYS_write, (void *)(long int)fd, (void *)buf, (void *)count,
                 NULL, NULL, NULL);
}

void runtest() {
  kill(getpid(), SIGSTOP);

  /* TODO: Unmap pages */
  asm __volatile__(".global test_block\n\t"
                   "restart_point:\n\t");
  /* TODO: Stop performance counters */
  int iters = ITERATIONS;
  asm __volatile__(".global test_block\n\t"
                   "test_start:\n\t");
  iters--;
  if (iters == 0) {
    kill(getpid(), SIGSTOP);
  }
  /* TODO: Initialize registers and memory */
  /* TODO: Store last performance counter values */
  /* TODO: Start performance counters */
  asm __volatile__(".global test_block\n\t"
                   "test_block:\n\t");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Jump back to test_start */
}
