/**
 * This file contains code left in the child memory after unmapping. Because
 * everything else is unmapped at this point, no stdlib available.
 **/

#include "runtest_redefines.h"

#define NULL (void *)0

#define ITERATIONS 100

typedef int pid_t;
typedef long int size_t;
typedef unsigned long int ssize_t;

__attribute__((always_inline)) static inline long
syscall(long number, void *param1, void *param2, void *param3, void *param4,
        void *param5, void *param6) {
#ifdef __x86_64__
  asm __volatile__("mov %0, %%rax\n\t"
                   "mov %1, %%rdi\n\t"
                   "mov %2, %%rsi\n\t"
                   "mov %3, %%rdx\n\t"
                   "mov %4, %%r10\n\t"
                   "mov %5, %%r8\n\t"
                   "mov %6, %%r9\n\t"
                   "syscall"
                   : // No output
                   : "rm"(number), "rm"(param1), "rm"(param2), "rm"(param3),
                     "rm"(param4), "rm"(param5), "rm"(param6));
#endif
}

static pid_t getpid(void) {
  syscall(SYS_getpid, NULL, NULL, NULL, NULL, NULL, NULL);
}

static int kill(pid_t pid, int sig) {
  syscall(SYS_kill, (void *)(long int)pid, (void *)(long int)sig, NULL, NULL,
          NULL, NULL);
}

static int munmap(void *addr, size_t len) {
  syscall(SYS_munmap, addr, (void *)len, NULL, NULL, NULL, NULL);
}

static ssize_t write(int fd, const void *buf, size_t count) {
  syscall(SYS_write, (void *)(long int)fd, (void *)buf, (void *)count, NULL,
          NULL, NULL);
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
  /* TODO: Store initial performance counter values */
  /* TODO: Start performance counters */
  asm __volatile__(".global test_block\n\t"
                   "test_block:\n\t");
  /* INSERT HERE: Stop performance counters */
  /* INSERT HERE: Store end performance counter values */
  /* INSERT HERE: Jump back to test_start */
}
