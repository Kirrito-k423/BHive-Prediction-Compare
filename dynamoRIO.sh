#!/bin/bash

CC=gcc
CFLAGS=-fno-omit-frame-pointer

# harness.o: harness.c
${CC} ${CFLAGS} -c -o harness.o harness.c

# main.o: main.c
${CC} ${CFLAGS} -c -o main.o main.c

# runtest.o: runtest.c
${CC} ${CFLAGS} -c -o runtest.o runtest.c -nostdlib

# main: main.o harness.o runtest.o
${CC} -o main main.o harness.o runtest.o -lrt -lpfm
