#include <stdlib.h>

#include "harness.h"

void main() {
  // mov rax, [2325000]
  char code[8] = {'\x48', '\x8B', '\x04', '\x25',
                  '\x00', '\x50', '\x32', '\x02'};
  measure_results_t res;
  measure(code, 8, 40, &res);
}
