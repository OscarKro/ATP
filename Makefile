#############################################################################
#
# Project Makefile
#
# (c) Wouter van Ooijen (www.voti.nl) 2016
#
# This file is in the public domain.
# 
#############################################################################

# source files in this project (main.cpp is automatically assumed)
SOURCES := fibonacci.asm
# header files in this project
HEADERS :=

# other places to look for files for this project
SEARCH  := 

# settings for Arduino Due projects
TARGET            := arduino_due
CONSOLE_BAUDRATE  := 115200

# the location of the ti software directory
RELATIVE          ?= .
TI-SOFTWARE       := $(RELATIVE)/..

# add hwlib
HWLIB             ?= $(TI-SOFTWARE)/hwlib
BMPTK             ?= $(TI-SOFTWARE)/bmptk
include           $(HWLIB)/makefile.inc