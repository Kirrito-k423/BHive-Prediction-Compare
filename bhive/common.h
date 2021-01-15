#ifndef _COMMON_H_
#define _COMMON_H_

/* Address of page to be used for child stack. */
#define AUX_MEM_ADDR (void *)0x0000700000000000

#define ITERATIONS 1

#define INIT_VALUE 0x2324000
#define INIT_VALUE_STR "0x2324000"

#define SHM_FD 42
/* Size of shared memory. First page will be mapped to child virtual address
 * pages. Second page mapped to child stack page.
 */
#define SHARED_MEM_SIZE 2 * PAGE_SIZE

#define _COUNTER_BASE __COUNTER__ + 1
#define CYC_COUNT_OFFSET (__COUNTER__ - _COUNTER_BASE) * 8

#endif // _COMMON_H_
