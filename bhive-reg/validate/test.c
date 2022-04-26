#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BIT(n) (1<<n)

int main(int argc, char *argv[]) {

  uint64_t start = 0, end = 0;
  uint64_t tmp = 0;
  uint64_t event = (uint64_t)strtol(argv[1], NULL, 16);

  // Set event
  asm volatile("msr pmevtyper0_el0, %0" : : "r"(event));

  // Enable
  asm volatile("msr pmcntenset_el0, %0" : : "r"(BIT(0)));
  asm volatile("isb");
  asm volatile("mrs %0, pmcr_el0" : "=r"(tmp));
  asm volatile("msr pmcr_el0, %0" : : "r"(tmp | BIT(0)));
  
  long init_value = 0x2324000;
  asm volatile("ldr w0, %0"::"m"(init_value));

  //clear
  asm volatile("msr pmevcntr0_el0, %0" ::"r"((uint64_t)0x0));
  asm volatile(
		  "sub sp, sp, #1600\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "ldp x29, x30, [sp], #0x10\n\t"
		  "add sp, sp, #1120\n\t"
  );
  asm volatile("mrs %0, pmevcntr0_el0" : "=r"(end));

  asm volatile("msr pmcntenset_el0, %0" : : "r"(0 << 31));

  printf("Event num is %lu\n", end);
  return 0;
}
