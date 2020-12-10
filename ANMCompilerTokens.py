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
	return "\nbl " + label

def create_label(label :str) ->str:
	"""Function to create a label in assembly		

	Args:
		label (str): The name the label needs to have

	Returns:
		str: A string containing assembly
	"""
	return "\n" + label + ":"


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
	"""Function to create assembly move instructions to set values into registers r0, r1, r2,r3.

	Args:
		*args : all the args as integers you want to set in registers r0 / r3. The first paramater will be set in r0, the second in r1 etc.

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
	pushRegisters = ":\npush {r4,r5,r6,lr}" # push all original registers for safekeeping
	moveSpToR0 = "\nmov r4, sp" # set the stack pointer into r4, which is now the "memory pointer"
	moveSpToR1 = "\nmov r5, r4" # also keep the original start of the memory in r5 so we can always jump there or get it if needed
	add = "\nsub r4, #1" # point the memory adress away from adress 0, so it it starts at adress 1
	allocate = "\nsub sp, #"+ str(length)# this jumps 4 * length in stack to alocate the memory. Each "word" is 4 bytes.
	movePcToR6 = "\nmov r6, pc" # move the program counter to R6, which now holds the very next instruction


	return "\n\n" + label + pushRegisters + moveSpToR0 + moveSpToR1 + add + allocate +  movePcToR6


def Hok() -> str:
	"""Function to jump to whatever is set in r0. Used for the skipping of code to the next weide instruction

	Returns:
		str: A string containing assembly
	"""
	return "\nmov pc, r0"

def Weide() -> str:
	"""Function to create a string that moves the content of r5 (the adress 0 of the memory where the user linking register is) to the program counter

	Returns:
		str: A string containing assembly
	"""
	return "\nmov pc, [r5]"


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
	correct = "\nsub r0, r5, r0" # substract the value in r0, from the base memory counter so it points to the correct adress. and place this in r0
	setMemoryCounter = "\nmov r4, r0" #set the value or r0 in r4, which is the memory counter, so the memory counter now points to the wanted place
	pop = "\npop {pc}"
	return "\n" + label + push + correct + setMemoryCounter + pop


def Duif(args : str) -> str:
	"""Function to create assembly to jump somewhere

	Returns:
		str: A string containing assembly
	"""
	return "\nb " + args # branch to label


def Schaap() -> str:
	"""Function to create a label to add one to wherever the memory counter (r4) is pointing to

	Returns:
		str: A string containing assembly
	"""
	label = "\nschaap:"
	push = "\npush {lr}"
	add = "\nadd [r4] #1" # add one to where the memory counter is pointing to
	pop = "\npop {pc}"
	return "\n" + label + push + add + pop


def Lam() -> str:
	"""Function to create a label to substract one from wherever the memory counter (r4) is pointing to

	Returns:
		str: A string containing assembly
	"""
	label = "\nlam:"
	push = "\npush {lr}"
	sub = "\nsub [r4] #1" # substract one from where the memory counter is pointing to
	pop = "\npop {pc}"
	return "\n" + label + push + sub + pop


def Teun() -> str:
	"""Function to create a label to place the value of r0 in to the memory to where the memory pointer on r4 is currently pointing to

	Returns:
		str: A string containing assembly
	"""
	label = "\nteun:"
	push = "\npush {lr}"
	add = "\nadd r0, r5" # set the pointer to the correct memory adress in r0, using r5, which holds the stack pointer from when the memory was still to be created, so adress 0
	mov = "\nmov [r4], [r0]" # move the value from adress r0 into where the memory counter currently points to
	pop = "\npop {pc}"
	return "\n" + label + push + add + mov + pop


def Aap() -> str:
	"""Function to create a label to cmp r0 with r1 and go to r2 if they are equal. r0, r1 and r2 should all be memory adresses

	Returns:
		str: A string containing assembly code
	"""
	label = "\naap:"
	push = "\npush {lr}"
	getAddress0 = "\nmov r0, [r0]" #get the content of the first parameter from the stack memory and place it in r0
	compare = "\ncmp r0, [r1]" #compare the content of r0 with the content on adress r1 from the stack memory
	beq = "\nbeq r2" #branch to the third paramater if these two are equal
	pop = "\npop {pc}"
	return "\n" + label + push + getAddress0 + compare + beq + pop


def Noot () -> str:
	"""Function to create a label to place r0 in the adress thats on r4, the memory pointer

	Returns:
		str: A string containing assembly
	"""
	label = "\nnoot:"
	push = "\npush {lr}"
	setValue = "\nmov [r4], r0" # write the value of r0 into the adress thats on r4, which is the memory counter
	pop = "\npop {pc}"
	return "\n" + label + push + setValue + pop


def Mies() -> str:
	"""This function needs to be made using c++, ask Jan?

	Returns:
		str: nothing
	"""
	return "\nmov pc, lr"


def Vuur() -> str:
	"""Function that creates a label that stops the execution of ANM code and pops the lr back in to the pc to resume where other code was

	Returns:
		str: A string containing assembly code
	"""
	label = "\nvuur:"
	deallocate = "\nmov sp, r5" #place the original stack pointer back into r1
	popRegisters = "\npop {r4,r5,r6,pc}\n" # pop all the registers back
	return "\n" + label + deallocate + popRegisters

