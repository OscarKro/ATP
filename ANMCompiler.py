from ANMCompilerTokens import *

def hold_console():
    i = input()
    exit()

memorySize = 1000
a = start_code_section()

a += Wim()
a += Jet()
a += Does()
a += Duif()
a += Schaap()
a += Lam()
a += Teun()

a += start_of_ANM_and_allocate_memory_on_stack(memorySize,"_ANM")
a += set_scratch_registers(5)
a += branch_to("does")
a += deallocate_memory_on_stack_and_end_ANM()
print(a)
hold_console()


