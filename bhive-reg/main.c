#include "harness.h"
// #include "icecream.hpp"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void main(int argc, char **argv) {
    measure_results_t res;
    int count = atoi(argv[2]);
    int byte_size = strlen(argv[1]) / 3;
    char * code_tmp[strlen(argv[1]) + 1];
    strcpy(code_tmp, argv[1]);
    char add_code_tsv110[byte_size];
    char * ch;
    const char s[2] = "x";
    char * brkb;
    int i = 0;
    for (ch = strtok_r(code_tmp, s, &brkb); ch; ch = strtok_r(NULL, s, &brkb)) {
        uint16_t intVal;
        intVal = strtol(ch, NULL, 16);
        add_code_tsv110[i] = intVal;
        i++;
    }
    // IC(add_code_tsv110)

   /* int byte_size = strlen(argv[1]) / 2; */
   /* char *pos = argv[1]; */
   /* uint64_t raw_event = (uint64_t)strtol(argv[2], NULL, 16); */

   /* char *add_code_tsv110 = (char *)malloc(sizeof(char) * byte_size); */

   /* for (size_t count = 0; count < byte_size; count++) { */
   /*   sscanf(pos, "%2hhx", &add_code_tsv110[count]); */
   /*   pos += 2; */
   /* } */
   /* if(argc >= 4){ */
   /*     count = atoi(argv[3]); */
   /* } */
    uint64_t raw_event = (uint64_t)strtol("0011", NULL, 16);
    measure(add_code_tsv110, byte_size, count, &res, raw_event);
}
