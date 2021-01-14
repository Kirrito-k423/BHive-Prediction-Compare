.global tail_start
.global tail_end
.text
tail_start:
    /* TODO: Stop performance counters. */
    /* Jump back to tail_start in runtest.c */
    jmp tail_start
tail_end:
    nop
