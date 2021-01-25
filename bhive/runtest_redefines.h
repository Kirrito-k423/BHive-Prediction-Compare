/**
 * This file contains redefines of architecture specific constants for
 * testblock.c.
 **/
#ifndef _TESTBLOCK_REDEFINES_H_
#define _TESTBLOCK_REDEFINES_H_

/*******************************************************************************
 * Redefine constants.
 */

#define MAP_SHARED 0x01

#define PROT_READ 0x1
#define PROT_WRITE 0x2

#define PAGE_SHIFT 12
#define PAGE_SIZE (1u << PAGE_SHIFT)
#define HALF_PAGE_STR "2048"

#define PERF_EVENT_IOC_DISABLE 9217
#define PERF_EVENT_IOC_ENABLE 9216
#define PERF_EVENT_IOC_RESET 9219

#define SIGSTOP 19

#ifdef __x86_64__

#define SYS_getpid 39
#define SYS_ioctl 16
#define SYS_kill 62
#define SYS_mmap 9
#define SYS_munmap 11
#define SYS_read 0
#define SYS_write 1

#elif __aarch64__

#define SYS_getpid 172
#define SYS_ioctl 29
#define SYS_kill 129
#define SYS_mmap 222
#define SYS_munmap 215
#define SYS_read 63
#define SYS_write 64

#else

#pragma GCC error                                                              \
    "SYS_* (in runtest_redefines.h) macros are not redefined for this "        \
    "architecture"

#endif

/*******************************************************************************
 * Redefine types.
 */

#define NULL (void *)0

typedef int pid_t;
typedef long int ssize_t;
typedef unsigned long int size_t;
typedef unsigned long int uint64_t;
typedef long off_t;

/*******************************************************************************
 * Redefine syscall functions.
 */

#define ALWAYS_INLINE __attribute__((always_inline)) static inline

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
#elif __aarch64__
  long ret = 0;
  asm __volatile__("mov x8, %1\n\t"
                   "mov x0, %2\n\t"
                   "mov x1, %3\n\t"
                   "mov x2, %4\n\t"
                   "mov x3, %5\n\t"
                   "mov x4, %6\n\t"
                   "mov x5, %7\n\t"
                   "svc #0\n\t"
                   "mov %0, x0"
                   : "=rm"(ret)
                   : "rmn"(number), "rmn"(param1), "rmn"(param2), "rmn"(param3),
                     "rmn"(param4), "rmn"(param5), "rmn"(param6));
  return ret;
#else
#pragma GCC error                                                              \
    "syscall (in runtest_redefines.h) is not implemented for this architecture"
#endif
}

ALWAYS_INLINE pid_t getpid(void) {
  return syscall(SYS_getpid, NULL, NULL, NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE int kill(pid_t pid, int sig) {
  return syscall(SYS_kill, (void *)(size_t)pid, (void *)(size_t)sig, NULL, NULL,
                 NULL, NULL);
}

ALWAYS_INLINE void *mmap(void *addr, size_t length, int prot, int flags, int fd,
                         off_t offset) {
  return (void *)syscall(SYS_mmap, addr, (void *)length, (void *)(ssize_t)prot,
                         (void *)(ssize_t)flags, (void *)(ssize_t)fd,
                         (void *)offset);
}

ALWAYS_INLINE int munmap(void *addr, size_t len) {
  return syscall(SYS_munmap, addr, (void *)len, NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE ssize_t read(int fd, void *buf, size_t count) {
  return syscall(SYS_read, (void *)(ssize_t)fd, buf, (void *)count, NULL, NULL,
                 NULL);
}

ALWAYS_INLINE ssize_t write(int fd, const void *buf, size_t count) {
  return syscall(SYS_write, (void *)(ssize_t)fd, (void *)buf, (void *)count,
                 NULL, NULL, NULL);
}

/*******************************************************************************
 * Utility functions
 */

ALWAYS_INLINE void *get_page_start(void *addr) {
  return (void *)(((uint64_t)addr >> PAGE_SHIFT) << PAGE_SHIFT);
}

ALWAYS_INLINE void *get_page_end(void *addr) {
  return get_page_start(addr) + PAGE_SIZE;
}

ALWAYS_INLINE int enable_pmu(int fd) {
  return syscall(SYS_ioctl, (void *)(ssize_t)fd,
                 (void *)(size_t)PERF_EVENT_IOC_ENABLE, NULL, NULL, NULL, NULL);
}

ALWAYS_INLINE int disable_pmu(int fd) {
  return syscall(SYS_ioctl, (void *)(ssize_t)fd,
                 (void *)(size_t)PERF_EVENT_IOC_DISABLE, NULL, NULL, NULL,
                 NULL);
}

ALWAYS_INLINE int reset_pmu(int fd) {
  return syscall(SYS_ioctl, (void *)(ssize_t)fd,
                 (void *)(size_t)PERF_EVENT_IOC_RESET, NULL, NULL, NULL, NULL);
}

#endif // _TESTBLOCK_REDEFINES_H_
