#ifndef _TESTBLOCK_H_
#define _TESTBLOCK_H_

void runtest(int perf_fd, int shm_fd, void *test_page_end);
void restart_point();
void test_start();
void test_block();

#endif // _TESTBLOCK_H_
