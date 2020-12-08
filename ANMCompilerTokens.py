import copy
from typing import *
from functools import *
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def start_code_section() -> str:
	"""Function that creates assembly for the start of a text section and alignment on four bytes (one 32 bit word)

	Returns:
		str: A string containing assembly code
	"""
	return "\n" + ".section .text\n.align 4\n"

def start_data_section() -> str:
	"""Function that creates assembly the start of a data section and alignment on four bytes (one 32 bit word)

	Returns:
		str: A string containing assembly code
	"""
	return "\n" + ".section .data\n.align 4\n"

def branch_to(label : str) -> str:
	"""Function that creates assembly for a branch link to a label

	Args:
		label (str): The label that needs to be jumped to

	Returns:
		str: A string containing assembly code
	"""
	return "\nbl " + label + "\n"


def zipWith(f: Callable[[A, B], C], l1: List[A], l2: List[B]) -> List[C]:
	"""Function to zip two iterables together and call a function on each element, made by Jan Halsema

	Args:
		f (Callable[[A, B], C]): The function that needs to be called on each element of the two iterables combined
		l1 (List[A]): The first iterable to zip
		l2 (List[B]): The second iterable that needs to be zipped

	Returns:
		List[C]: A list with the result
	"""
	return map(lambda tup: f(*tup), zip(l1, l2))

def create_move(dest : str, value : int) -> str:
	"""Function to create a move in assembly

	Args:
		dest (str): The destination register
		value (int): The value that needs to be put there

	Returns:
		str: A string containing assembly
	"""
	return "\nmov " + dest + ", #" + str(value)

def set_scratch_registers(*args : int) -> str:
	"""Function to create assembly move instructions to set values into registers r0, r1, r2,r3

	Args:
		*args : all the args as integers you want to set in registers r0 / r3

	Returns:
		str: A string with a move assembly function on each line for each respective parameter
	"""
	registers = ["r0","r1","r2","r3"]
	return str(reduce(lambda a,b:a+b,list(zipWith(create_move,registers,args))))


def start_of_ANM_and_allocate_memory_on_stack(length : int, label : str) -> str:
	"""Function that creates the start of AapNootMies in assembly. It pushes r4/r11 and the lr to the stack and increases the stack pointer by length. So a piece of memory on the stack 
	is created. The function also copies the SP to R4 and substractes the length of the memory from it. Meaning a new memory pointer is created that is set to adress 1 of 32 bit word.
	The assembly code resulting from this function has no exit. Instead, "deallocate_memory_on_stack_and_end_ANM" should be called to create the code to exit and a branch to "_exit_ANM"
	should be created.

	Args:
		length (int): The length of the memory on the stack that is created by this function and used by ANM	
		label (str): The label that this function needs to be (for example _ANM or _start)

	Returns:
		str: A string containing assembly code
	"""
	pushRegisters = ":\npush {r4,r5,r6,r7,r8,r9,r10,r11,lr}" # push all original registers for safekeeping
	moveSpToR0 = "\nmov r4, sp" # set the stack pointer into r4, which is now the "memory pointer"
	moveSpToR1 = "\nmov r5, r0" # also keep the original start of the memory in r5 so we can always jump there if needed
	add = "\nsub r4, #1" # point the memory adress away from adress 0, so it it starts at adress 1
	allocate = "\nsub sp, #"+ str(length)# this jumps 4 * length in stack to alocate the memory. Each "word" is 4 bytes.


	return "\n\n" + label + pushRegisters + moveSpToR0 + moveSpToR1 + add + allocate

def deallocate_memory_on_stack_and_end_ANM() -> str:
	"""Function that stops the execution of ANM code and pops the lr back in to the pc to resume where ever other code was

	Returns:
		str: A string containing assembly code
	"""
	label = "\n_exit_ANM:"
	deallocate = "\nmov sp, r5" #place the original stack pointer back into r1
	popRegisters = "\npop {r4,r5,r6,r7,r8,r9,r10,r11,pc}\n" # pop all the registers back
	return "\n" + label + deallocate + popRegisters

def Wim() -> str:
	"""Function to create a label that adds one to the memory pointer

	Returns:
		str: A string containing assembly
	"""
	label = "\nwim:"
	push = "\npush {lr}"
	increaseMemoryCounter = "\nsub r4, #1" #increase the memory counter by one word
	pop = "\npop {pc}"
	return "\n" + label + push + increaseMemoryCounter + pop

def Jet() -> str:
	"""Function to create a label that substracts one from the memory pointer

	Returns:
		str: A string containing assembly
	"""
	label = "\njet:"
	push = "\npush {lr}"
	decreaseMemoryCounter = "\nadd r4, #1" #decrease the memory counter by one word
	pop = "\npop {pc}"
	return "\n" + label + push + decreaseMemoryCounter + pop

def Does() -> str:
	"""Function to create a label to set the memory counter to whatever is set in r0

	Returns:
		str: A string containing assembly
	"""
	label = "\ndoes:"
	push = "\npush {lr}"
	setMemoryCounter = "\nmov r4, r0" #set the value or r0 in r4, which is the memory counter
	pop = "\npop {pc}"
	return "\n" + label + push + setMemoryCounter + pop

def Duif() -> str:
	"""Function to create a label to set the program counter to whatever is in r0

	Returns:
		str: A string containing assembly
	"""
	label = "\nduif:"
	code = "\nmov pc, r0"
	return "\n" + label + code  #create a duif label and set the value of r0 in the program counter

def Schaap() -> str:
	"""Function to create a label to add one to wherever the memory counter is pointing to

	Returns:
		str: A string containing assembly
	"""
	label = "\nschaap:"
	push = "\npush {lr}"
	add = "\nadd [r4] #1" # add one to where the memory counter is pointing to
	pop = "\npop {pc}"
	return "\n" + label + push + add + pop

def Lam() -> str:
	"""Function to create a label to substract one from wherever the memory counter is pointing to

	Returns:
		str: A string containing assembly
	"""
	label = "\nlam:"
	push = "\npush {lr}"
	sub = "\nsub [r4] #1" # substract one from where the memory counter is pointing to
	pop = "\npop {pc}"
	return "\n" + label + push + sub + pop

def Teun() -> str:
	label = "\nteun:"
	push = "\npush {lr}"
	add = "\nadd r0, r5" # set the pointer to the correct memory adress in r0, using r5, which holds the stack pointer from when the memory was still to be created, so adress 0
	mov = "\nmov [r4], [r0]" # move the value from adress r0 into where the memory counter currently points to
	pop = "\npop {pc}"
	return "\n" + label + push + add + mov + pop

def Aap(label : str) -> str:
	label = "\naap:"
	push = "\npush {lr}"
	#compare two registers
	# branch if equal to the label. How to do so?
	# pop the lr in to pc 
	# ask wouter how to do beq?
