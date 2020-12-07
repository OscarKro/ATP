from ANMCompilerTokens import *
def hold_console():
    i = input()
    exit()

wordSize = 4
memorySize = 1000
a = ""
a += start_code_section()
a += branch_to("_ANM")
a += branch_to("_startup")
a += start_of_ANM_and_allocate_memory_on_stack(memorySize * wordSize,"_ANM")
a += deallocate_memory_on_stack_and_end_ANM(memorySize * wordSize)
print(a)
hold_console()s


