# ATP
This repo contains the interpeter (and later the compiler) for the aapNootMies language

## aapNootMies
aapNootMies is a turing complete esoteric programming language that is very basic an pretty similar to a dressed down version of assembly. You can loop, increase and decrease numbers and check if two adresses are equal. So you can do pretty much any mathmetic calculation.
Some instructions need parameters, others don't. Depending on what instruction is read, the user can alter memory. 
It exists completely of so called "weides". Every weide object contains two lists, and two counters. One list contains lists which contain every individual instruction and respective paramaters. The other list is the memory. Which instruction is executed is determined by where the program counter points to in the instruction list. Which memory location is altered is determined by where the memory counter points to in the memory list. By altering the program counter, one can decide what instruction is carried out. By altering the memory counter, one can alter the specific piece of memory. Everytime a state is changed. The language returns a new weide with a new state. Meaning the original state is never changed.

### instructions
To run, type in the terminal: "ANMinterperter.py" and follow the steps. All ANM files need to have the extension ".aap"
All instructions need to be seperated by new lines and all parameters need to be seperated by spaces. Parameters may only be integers, not other instructions.
It's best to not create white lines in between instructions. These are filtered out by the algorithm. So when you want to jump to line 10 in your file, it could actually be line 8 if there are two white lines somewhere in the file. Or keep track of this yourself.

1. weide: This is an instruction that has no use at this very moment, but needs to placed at the beginning of every file (will be used with the compiler probably)
2. wim: increase the memory counter
3. jet: decreaste the memory counter
4. duif X: jump to other line/instruction. Where X is the go to adress
5. schaap: increase the integer within the memory at the place the memory counter currently points to
6. lam: decrease the integer within the memory at the place the memory counter currently points to
7. aap X Y Z: If X is equal to Y jump to instruction Z, else go to next instruction
8. noot X: Place X at the location the memory counter currently points to
9. mies: print the value from the memory, from where the memory counter currently points to
10. vuur: quit the execution

### error handeling
The interperter has some very, very basic error handeling. Wrong or to few parameters will be caught and so will wrong instructions or the wrong file extension.
Inline comments are not possible as of yet.

### example
This small example below will count from 1 to 10 and display each result

1. weide (always start with a new weide)
2. noot 0 (place 0 at wherever the memory counter currently points to, which is 1 at the start of execution)
3. wim (add 1 to the memory counter)
4. noot 10 (place 10 at location 2 in the memory)
5. jet (decrease the memory counter by one to let it point to 1 again)
6. schaap (add one to the byte where the memory counter points to. So that is now +1)
7. mies (print the value from where the memory counter points to)
8. aap 0 1 10 (jump to instruction line 10 if memory adress 0 is equal to adress 1, if not, continue with the next instruction)
9. duif 6 (jump to instruction line 6)
10. vuur (quit the program, or more shakespeary: burn thy pasture!)

### source code
Everything is written in (mostly) functional python

