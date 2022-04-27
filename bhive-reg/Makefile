CC := gcc
Debug = -g

CFLAGS := -fno-omit-frame-pointer

main: main.o harness.o runtest.o
	$(CC) $(Debug) -o  bhive main.o harness.o runtest.o -lrt -lpfm

harness.o: harness.c
	$(CC) $(Debug) $(CFLAGS) -c -o harness.o harness.c

main.o: main.c
	$(CC) $(Debug) $(CFLAGS) -c -o main.o main.c

runtest.o: runtest.c
	$(CC) $(Debug) $(CFLAGS) -c -o runtest.o runtest.c -nostdlib

clean:
	rm -f bhive main.o harness.o runtest.o
