#ifndef _COMMON_H_
#define _COMMON_H_

/* Address of page to be used for child stack. */
#define AUX_MEM_ADDR (void *)0x0000700000000000

#define ITERATIONS 50

#define INIT_VALUE 0x2324000

#define MAX_FAULTS 1024

#define PAGE_SHIFT 12
#define PAGE_SIZE (1u << PAGE_SHIFT)

#define SHM_FD 42
/* Size of shared memory. First page will be mapped to child virtual address
 * pages. Second page mapped to child stack page.
 */
#define SHARED_MEM_SIZE 2 * PAGE_SIZE

#define CYC_COUNT_OFFSET 0
#define L1_READ_MISSES_OFFSET 8
#define L1_WRITE_MISSES_OFFSET 16
#define ICACHE_MISSES_OFFSET 24
#define CTX_SWITCHES_OFFSET 32

#define PERF_FD_OFFSET 40
#define TEST_PAGE_END_OFFSET 48
#define ITERATIONS_OFFSET 56
#define STACK_BP_OFFSET 64
#define STACK_SP_OFFSET 72
#define MAP_AND_RESTART_ADDR_OFFSET 80
#define INIT_VALUE_OFFSET 88

#endif // _COMMON_H_
