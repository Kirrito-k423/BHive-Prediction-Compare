#include <stdlib.h>
#include <stdio.h>
#include "harness.h"

void main(int argc, char** argv) {
  // printf("%d \n",argc);
  char add_code_tsv110[argc];
  for(int i=0; i<argc-1; i++){
    uint16_t intVal;
    sscanf(argv[i+1], "%x", &intVal);
    printf("%d \n",intVal);
    add_code_tsv110[i]=intVal;
  }
  measure_results_t res;
  int count = 10000;
  printf("%d %d\n",argc, count);
  measure(add_code_tsv110, argc-1, count, &res);
}
// void main(int argc, char** argv) {
//   /* char add_code_tsv110[4] = {0x88, 0x8d, 0x40, 0xb8}; */
//   char add_code_tsv110[8] = {0xa0, 0xd4, 0x66, 0x4e, 0xa0, 0xd4, 0x66, 0x4e};
//   for(int i=0; i<8; i++){
//     printf("%d ",add_code_tsv110[i]);
//   }
//   measure_results_t res;
//   int count = 10000;
//   /* if(argc >= 2){ */
//   /*     count = atoi(argv[1]); */
//   /* } */
//   measure(add_code_tsv110, 8, count, &res);
// }
