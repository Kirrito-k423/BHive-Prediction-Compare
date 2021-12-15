#include <stdlib.h>
#include <stdio.h>

#include "harness.h"

void main(int argc, char** argv) {
  char add_code_tsv110[argc-1];
  int count = atoi(argv[1]);
  for (int i = 1; i < argc-1; i++) {
    uint16_t intVal;
    sscanf(argv[i+1], "%x", &intVal);
    // printf("%d \n",intVal);
    add_code_tsv110[i-1] = intVal; 
  }
  measure_results_t res;
  // printf("%d %d\n",argc-2, count);
  measure(add_code_tsv110, argc-2, count, &res);
}
