# Copyright (C) 2017, Chris Smeele
# By using this you surrender your firstborn child to the blood god.
# All other rights reserved.

NAME := lemonator
BIN  := $(NAME)$(shell python3-config --extension-suffix)

CXX  := g++
CC   := gcc

# The directory containing RS-232, hwlib and bmptk.
EXTERNALS ?= ../externals
INCDIRS   := \
	../include \
	$(EXTERNALS)/RS-232 \
	$(EXTERNALS)/hwlib/library

CXXFLAGS := \
	-std=c++14 \
	-fPIC \
	-flto \
	-Wall \
	-Og \
	-g3 \
	-DBMPTK_TARGET=pyd \
	-DBMPTK_TARGET_pyd \
	-DBMPTK_CHIP=Linux_Native \
	-DBMPTK_CHIP_Linux_Native \
	-DBMPTK_XTAL= \
	-DBMPTK_BAUDRATE=38400 \
	-DBMPTK_VERSION=V04_00_work_in_progress_2017_01_23 \
	-DBMPTK_HOSTED \
	-DBMPTK_HAS_FILESYSTEM \
	$(addprefix -I, $(INCDIRS)) \
	`python3 -m pybind11 --includes`

CFLAGS := \
	-std=c11 \
	-fPIC \
	-flto \
	-Wall \
	-Os \
	-g3 \
	$(addprefix -I, $(INCDIRS))

LDFLAGS  := -Os -flto -fPIC -shared

CFILES   := $(EXTERNALS)/RS-232/rs232.c
CXXFILES := $(shell find -type f -name '*.cpp')
OFILES   := $(CFILES:%.c=%.o) $(CXXFILES:%.cpp=%.o)

.PHONY: all
all: $(BIN)

$(BIN): $(OFILES) hwlib.o
	$(CXX) -o $@ $(LDFLAGS) $^

hwlib.o: $(EXTERNALS)/hwlib/library/hwlib.cpp Makefile
	$(CXX) -o $@ $(CXXFLAGS) -c $<

%.o: %.c Makefile
	$(CC) -o $@ $(CFLAGS) -c $<

%.o: %.cpp Makefile
	$(CXX) -o $@ $(CXXFLAGS) -c $<

clean:
	rm -f $(OFILES) $(BIN) hwlib.o
