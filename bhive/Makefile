CC := gcc

main: main.o harness.o runtest.o
	$(CC) -o main main.o harness.o runtest.o -lrt -lpfm

harness.o: harness.c
	$(CC) -c -o harness.o harness.c

main.o: main.c
	$(CC) -c -o main.o main.c

runtest.o: runtest.c
	$(CC) -c -o runtest.o runtest.c -nostdlib

clean:
	rm main main.o harness.o runtest.o
