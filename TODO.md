# Things the parent should do
  1. [DONE] Create the child.
  2. [DONE] Wait for child to be ready.
  3. [DONE] Move child stack.

# Things the child before running block
  1. [DONE] Copy block + tail to designated spot.
  2. [DONE] Enable performance counters.
  3. [DONE] Pin child process.
  4. Unmap pages but the one holding child code and block and stack.
  5. Initialize registers.
  6. Start performance counters.
  7. Jump to block.

# Things the tail should do
  1. Turn off counters.
  2. Store counter values.
  3. [DONE] Jump back to step 5 in child.

# Testing child functionality
  1. Check that block and tail is copied.
  2. Check if registers are initialized.

# Pseudocode
Parent algorithm.
```
create_child()
wait_for_child_ready()
move_child_stack()
start_child_test()
for i in 0..MAX_FAULTS:
  wait_on_child()
  if child terminates successfully:
    return counters
  if child terminates with error:
    return NULL
  find_out_reason_for_termination()
  restart_child()
return NULL
```

Child algorithm.
```
enable_perf_counters()
pin_process()
alert_parent_ready()
copy_block_and_tail()
```

Child test algorithm.
```
unmap_pages()
for i in 0..ITERATIONS:
  initialize_registers_and_mem()
  start_performance_counters()
  test_block()
  stop_performance_counters()
  accumulate_counters()
```
