# Generale makefile for use with Harvard CS50 material
# Terminal commands: make EXE=yourfilename

# the compiler: gcc for C program, define as g++ for C+ use clang for Harvard
CC = clang

# compiler flags:
#  -g    adds debugging information to the executable file
#  -Wall turns on most, but not all, compiler warnings
CFLAGS  = -g -Wall

# link THIS for the cs50 functions (add others as needed):
LFLAGS = -lcs50

# the build target executable:
TARGET = $(EXE)

all: $(TARGET)

$(TARGET): $(TARGET).c ; $(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c $(LFLAGS)
