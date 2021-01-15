/**
 * This file contains redefines of architecture specific constants for
 * testblock.c.
 **/
#ifndef _TESTBLOCK_REDEFINES_H_
#define _TESTBLOCK_REDEFINES_H_

#ifdef __x86_64__

#define SIGSTOP 19

#define PAGE_SHIFT 12
#define PAGE_SIZE (1u << PAGE_SHIFT)

#define PERF_EVENT_IOC_ENABLE 9216
#define PERF_EVENT_IOC_DISABLE 9217

#define SYS_getpid 39
#define SYS_ioctl 16
#define SYS_kill 62
#define SYS_munmap 11
#define SYS_read 0
#define SYS_write 1

#endif

#endif // _TESTBLOCK_REDEFINES_H_
