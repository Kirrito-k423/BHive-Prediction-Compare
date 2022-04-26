as -o test.o test.s
ld -s -o test test.o -lc

./test