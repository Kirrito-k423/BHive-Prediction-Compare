CC := gcc

CFLAGS := -fno-omit-frame-pointer

main: main.o harness.o runtest.o
	$(CC) -o bhive main.o harness.o runtest.o -lrt -lpfm

harness.o: harness.c
	$(CC) $(CFLAGS) -c -o harness.o harness.c

main.o: main.c
	$(CC) $(CFLAGS) -c -o main.o main.c

runtest.o: runtest.c
	$(CC) $(CFLAGS) -c -o runtest.o runtest.c -nostdlib

clean:
	rm -f bhive main.o harness.o runtest.o
