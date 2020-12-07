import copy
from typing import *

def start_code_section() -> str:
    return "\n" + ".section .text\n.align 4\n"

def start_data_section() -> str:
    return "\n" + ".section .data\n.align 4\n"

def branch_to(label : str) -> str:
    return "\n" + "bl " + label + "\n"

def start_of_ANM_and_allocate_memory_on_stack(length : int, label : str) -> str:
	pushRegisters = ":\npush {r4,r5,r6,r7,r8,r9,r10,r11,lr}" # push all original registers for safekeeping
	keepOriginalStackPointer = "\nmov r4, sp" # get the original stackpointer and safe this on the stack
	pushOriginalStackPointer = "\npush {r4}" # push the original stackpointer to the stack
	allocate = "\nsub sp, sp, #"+ str(length)# this jumps 4 * length in stack to alocate the memory. Each "word" is 4 bytes.

	return "\n" + label + pushRegisters + keepOriginalStackPointer + pushOriginalStackPointer + allocate

def deallocate_memory_on_stack_and_end_ANM(length : int):
	deallocate = "\nadd sp, sp, #" + str(length)
	popOriginalStackPointer = "\npop {r4}"
	setOriginalStackPointer = "\nmov sp, r4"
	popRegisters = "\npop {r4,r5,r6,r7,r8,r9,r10,r11,pc}\n"
	return "\n" + deallocate  + popOriginalStackPointer + setOriginalStackPointer + popRegisters


