import copy
from typing import *
from functools import *
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def start_code_section(s : str) -> str:
	"""Function that creates assembly for the start of a text section and alignment on four bytes (one 32 bit word)

	Args:
		s (str): the name of this whole function
	Returns:
		str: A string containing assembly code
	"""
	return "\n" + ".section .text\n.align 4\n.global " + s

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
	return "\nmov " + dest + ",#" + str(value)

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
	add = "\nsub r4, #4" # point the memory adress away from adress 0, so it it starts at adress 1
	allocate = "\nsub sp, #"+ str(length*4)# this jumps 4 * length in stack to alocate the memory. Each "word" is 4 bytes.
	movePcToR6 = "\nmov r6, pc" # move the program counter to R6, which now holds the very next instruction, just for safekeeping,should i ever need it
	return "\n\n" + label + pushRegisters + moveSpToR0 + moveSpToR1 + add + allocate +  movePcToR6


def Hok(args : int) -> str:
	"""Function that returns a hok label

	Returns:
		str: A string containing assembly
	"""
	return "\n\n_H" + str(args) + ":" + "\npush {lr}" 

def Weide() -> str:
	"""Function to create a string that moves the content of r5 (the adress 0 of the memory where the user linking register is) to the program counter

	Returns:
		str: A string containing assembly
	"""
	return "\npop {pc}"

def Bok(args : int) -> str:
	"""Function to create a label to jump to a function created by a hok and weide

	Args:
		args (int): The hok number to branch link to

	Returns:
		str: A string containing assembly
	"""
	return "\nbl _H" + str(args)

def Wim() -> str:
	#tested, working
	"""Function to create a label that adds one to the memory pointer

	Returns:
		str: A string containing assembly
	"""
	return "\nsub r4, #4" #increase the memory counter by one word


def Jet() -> str:
	#tested, working
	"""Function to create a label that substracts one from the memory pointer

	Returns:
		str: A string containing assembly
	"""
	return "\nadd r4, #4" #decrease the memory counter by one word


def Does() -> str:
	#tested, working
	"""Function to create a label to set the memory counter to whatever is set in r0

	Returns:
		str: A string containing assembly
	"""
	set1 = "\nmov r1, #4"
	multiply = "\nmul r0, r0, r1"
	correct = "\nsub r0, r5, r0" # substract the value in r0, from the base memory counter so it points to the correct adress. and place this in r0
	setMemoryCounter = "\nmov r4, r0" #set the value or r0 in r4, which is the memory counter, so the memory counter now points to the wanted place
	return set1 + multiply + correct + setMemoryCounter


def Duif(args : str) -> str:
	#tested, working
	"""Function to create assembly to jump somewhere. You can only jump within functions or the main. Not from a hok to the main or the other way around, use a bok for that

	Returns:
		str: A string containing assembly
	"""
	return "\nb " + args # branch to label


def Schaap() -> str:
	#tested, working
	"""Function to create a label to add one to wherever the memory counter (r4) is pointing to

	Returns:
		str: A string containing assembly
	"""
	mov = "\nldr r0, [r4]"
	add = "\nadd r0, #1"
	store = "\nstr r0, [r4]"
	return mov + add + store 

def Lam() -> str:
	#tested, working
	"""Function to create a label to substract one from wherever the memory counter (r4) is pointing to

	Returns:
		str: A string containing assembly
	"""
	mov = "\nldr r0, [r4]"
	sub = "\nsub r0, #1"
	store = "\nstr r0, [r4]"
	return mov + sub + store 

def Teun() -> str:
	#tested, working
	"""Function to create a label to place the value of the adress in r0 in to the memory to where the memory pointer on r4 is currently pointing to (copy)

	Returns:
		str: A string containing assembly
	"""
	mov1 = "\nmov r1, #4" #for multiplying
	createOffset = "\nmul r0, r0, r1" 
	getAddress = "\nsub r0, r5, r0"
	getNumber = "\nldr r1, [r4]"
	store = "\nstr r1, [r0]"
	return mov1 + createOffset + getAddress + getNumber + store


def Aap(b1 : str, b2 : str) -> str:
	"""Function to create a label to cmp r0 with r1 and go to r2 if they are equal. r0, r1 and r2 should all be memory adresses

	Returns:
		str: A string containing assembly code
	"""
	mov1 = "\nmov r3,#4"
	mul1 = "\nmul r0,r3"
	mul2 = "\nmul r1,r3"
	createAddress1 = "\nsub r0, r5, r0"
	createAddress2 = "\nsub r1, r5, r1"
	get1 = "\nldr r0, [r0]"
	get2 = "\nldr r1, [r1]"
	c = "\ncmp r0, r1"
	beq = "\nbeq " + b1 #branch to the third paramater if these two are equal"
	bne = "\nbne " + b2
	return mov1 + mul1 + mul2 + createAddress1 + createAddress2 + get1 + get2 + c + beq + bne


def Noot () -> str:
	#tested, working
	"""Function to create a label to place r0 in the adress thats on r4, the memory pointer

	Returns:
		str: A string containing assembly
	"""
	return "\nstr r0, [r4]" # write the value of r0 into the adress thats on r4, which is the memory counter


def Mies() -> str:
	#tested, working
	"""This function needs to be made using c++, ask Jan?

	Returns:
		str: nothing
	"""
	setnumber = "\nldr r0, [r4]"
	branch = "\nbl print"
	return setnumber + branch


def Vuur() -> str:
	#tested, working
	"""Function that creates a label that stops the execution of ANM code and pops the lr back in to the pc to resume where other code was

	Returns:
		str: A string containing assembly code
	"""
	deallocate = "\nmov sp, r5" #place the original stack pointer back into r1
	popRegisters = "\npop {r4,r5,r6,pc}" # pop all the registers back
	return deallocate + popRegisters

