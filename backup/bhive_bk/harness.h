#ifndef _HARNESS_H_
#define _HARNESS_H_

#include <stdint.h>

typedef struct {
  uint64_t core_cyc;
  uint64_t l1_read_misses;
  uint64_t l1_write_misses;
  uint64_t icache_misses;
  uint64_t context_switches;
} measure_results_t;

int measure(char *code_to_test, unsigned long code_size,
            unsigned int unroll_factor, measure_results_t *res);

#endif // _HARNESS_H_
