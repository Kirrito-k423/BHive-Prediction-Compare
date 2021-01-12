CC := gcc

main: main.o harness.o
	$(CC) -o main main.o harness.c -lpfm

harness.o: harness.c
	$(CC) -c -o harness.o harness.c

main.o: main.c
	$(CC) -c -o main.o main.c
