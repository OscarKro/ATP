# ATP
This repo contains the interpeter (and later the compiler) for the aapNootMies language

## AapNootMies
![image](./Aap-Noot-Mies-Leesplankje.jpg)
aapNootMies is a turing complete esoteric programming language that is very basic an pretty similar to a dressed down version of assembly. You can loop, increase and decrease numbers, check if two addresses are equal and create very basic functions. So you can do pretty much any mathmetic calculation.
Some instructions need parameters, others don't. Depending on what instruction is read, the user can alter memory. You can read all instructions in the table below.
It exists completely of so called "weides". Every weide object contains two lists, and two counters. One list contains lists that contain every individual instruction and respective parameter(s). The other list is the memory. Which instruction is executed is determined by where the program counter points to in the instruction list. After each instruction is executed, the program counter is increased by one. By altering the program counter, you can decide what instruction is carried out.

Which memory location is altered is determined by where the memory counter (or memory pointer, mp) points to in the memory list.  By altering the memory pointer, one can alter the specific piece of memory. Everytime a state is changed, the language returns a new weide with a new state. Meaning the original state is never changed.

### Error handling
The interperter has some very, very basic error handeling. Wrong or to few parameters will be caught and so will wrong instructions or the wrong file extension.
Inline comments are not possible as of yet.

## Instructions to run and use
To run, type in the terminal: "ANMinterperter.py" and follow the steps. All ANM files need to have the extension ".aap"
All instructions need to be seperated by new lines and all parameters need to be seperated by spaces. You can use a tab to create more readable code for yourself. Parameters may only be integers, not other instructions. When the isntructions to jump to other instructions are used. The first instruction is 1 (not 0) and count from there.
It's good practice to not create white lines in between instructions. These are filtered out by the algorithm. So when you want to jump to instruction 10 in your file, it could actually be instruction 8 if there are two white lines somewhere in the file that you see, but the algortihm skips. You could also keep track of this yourself ofcoarse. It is also best practice to never use address 0 of the memory, as this is used for functions as a linker register. To ensure this is enforced, the algorithm starts with both the program counter and the memory counter set to 1. The user has to explicitly jump to memory address 0 to alter the linker register. Address 0 of the instruction register does not exist. So setting the program counter to 0 will start undefined behaviour.

### Functions
A function is created by writing a "hok" instruction and a "weide" instruction with 
other instructions in between. Whenever the algorithm reads the "hok" instruction during execution, it skips all code untill it sees a "weide" instruction, it then begins to execute the next piece of code after the "weide" instruction. "You go back into free space, a weide". Meaning you can create incapsulated pieces of code in between a hok and weide instruction that are never used. When you use a "duif" instruction to jump to the line that contains the first instruction after the "hok" you want to execute, the algorithm didn't see the "hok" instruction so it just starts to execute whatever code it reads. When the program hits the first "weide" instruction, the program counter is set to the value that is on adres 0 of the memory. Meaning you have a link register on address zero of the memory. So by setting the current instruction number, plus one, on address 0 of the memory you can continue your program wherever it was after it called the function. You can create as many "hok" instruction as you want. As long as you never forget to close them with a weide. Every hok can obviously acces all memory, meaning that you can give as much parameters as you want.

| instruction | required paramaters | explanation |
| ----------- | ----------- | ----------- |
| hok | 0 | Jump to the instruction after the next upcoming weide instruction ( skip all code between hok and weide )
| weide | 0 |  Jump to the instruction line that is set on index 0 in the memory ( end of function, jump to wherever ) |
| wim | 0 | Increase the memory pointer ( mp ) by one |
| jet | 0 | Decrease the mp by one |
| does | 1 | set the mp to the value of parameter 1 |
| duif | 1 | jump to other line/instruction of parameter 1 |
| schaap | 0 | increase the integer within the memory at the place the mp currently points to |
| lam | 0 |  decrease the integer within the memory at the place the mp currently points to |
| teun | 1 | set the value of the memory where te mp currently points to, to the value that is in the memory on the address of parameter 1 |
| aap | 3 | If content of memory address on parameter 1 is equal to content of memory address on parameter 2, jump to instruction 3, else go to next instruction |
| noot | 1 | set the value of parameter 1 on the address where the mp currently points to |
| mies | 0 | print the value of where the mp currently points to |
| vuur | 0 | stop execution


### Example 1, increase register
This small example below will count from 1 to 10 and display each result

1. noot 0 (place 0 at wherever the memory pointer currently points to, which is 1 because of the first wim)
2. wim (add 1 to the memory pointer)
3. noot 10 (place 10 at location 2 in the memory)
4. jet (decrease the memory pointer by one to let it point to 1 again)
5. schaap (add one to the byte where the memory pointer points to. So that is now +1)
6. mies (print the value from where the memory pointer points to)
7. aap 1 2 10 (jump to instruction line 10 if memory address 0 is equal to address 1, if not, continue with the next instruction)
8. duif 6 (jump to instruction line 6)
9. vuur (quit the program, or more shakespeary: burn thy pasture and see that thy and it are now barren!)

### Example 2, increase register within function
This small example uses example one, but as a function

1. hok (start of function, skipped initialy)
2.  schaap (add 1 the byte in the memory)
3.  mies (cout the byte)
4.  aap 1 2 6 (if address 1 and 2 are equal, jump to the weide on line 6, else go to instruction on line 6)
5.  duif 2 (jump to line 2)
6. weide (end of function, skipped initialy by the hok instruction, but jump to address on memory index 0 (linking register) when this instruction is executed)
8. noot 0 (place 0 on adres 1)
9. wim
10. noot 10 (place 10 on adres 2)
11. does 0 (set the mp to address 0, the linking register)
12. noot 14 (set the link register to the vuur instruction to terminate)
13. wim (increase to make sure address 0 is left alone)
14. duif 2 (start the exection of hok from line 1 to 6 by jumping to the line after the hok)
15. vuur

See aapnootmies.aap for a working example

## Source code
Everything is written in (mostly) functional python and the only object there is, is a weide object. The weide object contains the current state, so it holds the instruction memory list, the memory list, the program counter and the memory counter. Everytime a state is changed by an instruction, a new weide object is created containing a copy of the old weide, with new values. Meaning that an old state is never changed. Currently, the old states are not saved and will probably be removed by the Python garbage collector.

