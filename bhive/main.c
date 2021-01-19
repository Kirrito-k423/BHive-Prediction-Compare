#include <stdlib.h>

#include "harness.h"

void main() {
  // add rax, 1
  char code[4] = {'\x48', '\x83', '\xC0', '\x01'};
  measure_results_t res;
  measure(code, 0, 0, &res);
}
