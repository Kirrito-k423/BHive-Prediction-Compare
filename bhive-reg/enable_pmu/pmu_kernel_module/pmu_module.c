#include <linux/module.h>    // included for all kernel modules
#include <linux/kernel.h>    // included for KERN_INFO
#include <linux/init.h>      // included for __init and __exit macros

MODULE_LICENSE("GPL");
MODULE_AUTHOR("yuanfuyan");
MODULE_DESCRIPTION("Enable user-mode access to PMU counters");

//#define BIT(n) (1<<n)
typedef unsigned long long uint64;
typedef unsigned int uint32;
typedef uint64 u64;

void enable(void *data){
    /* Disable cycle counter overflow interrupt */
    //asm volatile("msr pmintenset_el1, %0" : : "r" ((uint64)(BIT(1) | BIT(0))));
    asm volatile("msr pmintenset_el1, %0" : : "r" ((uint64)0<<31));

    //Enable user-mode access to counters.
    asm volatile("msr pmuserenr_el0, %0" : : "r"((uint64)BIT(3)|BIT(2)|BIT(0)));
}

void disable(void *data){
    asm volatile("msr pmuserenr_el0, %0" ::"r" ((u64)0));
}

static int __init init(void)
{
	on_each_cpu(enable, NULL, 1);
    printk(KERN_INFO "Enable user-mode access to PMU counters\n");
    return 0;
}

static void __exit fini(void)
{
	on_each_cpu(disable, NULL, 1);
    printk(KERN_INFO "Disable user-mode access to PMU counters\n");
}

module_init(init);
module_exit(fini);
