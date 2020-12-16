# ATP
This repo contains the interpeter (and later the compiler) for the aapNootMies language

## AapNootMies
![image](./Aap-Noot-Mies-Leesplankje.jpg)
aapNootMies is a turing complete esoteric programming language that is very basic an pretty similar to a dressed down version of assembly. You can loop, increase and decrease numbers, check if two addresses are equal and create very basic functions. So you can do pretty much any mathmetic calculation.
Some instructions need parameters, others don't. Depending on what instruction is read, the user can alter memory. You can find the instructions and their explanation and number of parameters in the table below.
## Interperter
The interperter can be used by calling python with the ANMinterperter.py script. It checks for basic syntax errors before running. It does not check for runtime errors. So you can indeed go out of bounds on your memory or do other weird stuff. Both the interperter and the compiler are written in functional python. 
The memory you can use, is actually a size 100 list. You can only place numbers in the list. Because it is written in Python, Python will at runtime check
how large the number is you've put in the memory and will adjust the list accordingly, so your number can be infinite large. This language was made for a school assignment. I first had to build the interperter and then the compiler. During the building of the compiler I encountered some things that were wrong with my initial idea for the language. Because of this, I had to change how functions were called. Within the interperter, you CANNOT use recursion. This is only possible when you compile it. Create loops instead.
## Compiler
The compiler can be used by calling python with the ANMCompiler.py script. It checks for basic syntax errors before running. It does not check for runtime errors. So you can go out of bounds on your memory or do other weird stuff. This can be harmfull because AapNootMies is compiled to ARM Cortex assembly so be sure you do not do this. The memory of 100 times 32 bit words is completely placed on the stack. Meaning that your AapNootMies file can be compiled with other code and your other code
is completely safe from harm as every piece of memory from the ANM file will be cleared after use. 

Your ANM file needs to be compiled using the ANMCompiler, every file will become their own ARM cortex assembly label and memory. Meaning you can create multiple files, which result in multiple labels or functions you can externaly call. Every label will get the name of the file they came from, without the extension. For example the file: 'banana.aap' will create an assembly label named 'banana'. The external function 'banana()' can now be created and called. However, every ANM file gets is own 100 size piece of stack. You cannot call one ANM file from another ANM file. They need to be executed subsequently. Within every ANM file, you can also create functions using 'hok' instructions. Which is explained further below. For an example on how to use ANM with HWLIB and BMPTK, see the 'aapnootmies.aap', 'main.cpp' and 'Makefile' files.

The 'mies' instruction prints numbers to the screen. In my example, I created a function 'void print (int x)' externally in c++ in the main.cpp. This function cout's an integer using hwlib::cout. This type of function called 'print' always needs to be compiled with aapnootmies as well. As a global label called "print" is called by the assembly with the
integer on R0. I did not want to write this in assembly myself. So, compile this existing function with your code externally as well, or create your own 'print (integer x)' function.

## errors
All errors are trown during the parsing of the code. If the syntax is correct, the algorithms implicitly assumes the logic is in order as well. You can go out of bounds or do wrong stuff. I would love to create better error handling but school required this entire assignment to be written 'functional' meaning I could not alter a global state or throw exceptions/return different things. So if I wanted to include more error handling, especially during runtime, it would be a royal pain in the ass. As error handeling was not mandatory at all, I decided to keep to to syntax checking for now. All errors are 
written in "shakespeare" so it could be a bit hard to read.

## Instructions to run and use
To run, type in the terminal: "ANMinterperter.py/ANMCompiler.py" and follow the steps. All ANM files need to have the extension ".aap"
All instructions need to be seperated by new lines and all parameters need to be seperated by spaces. You can use a tab to create more readable code for yourself. Parameters may only be integers, not other instructions. Keep in mind that with jumping to other instructions, we count from 1. So you jump to line 6 for example.
It's good practice to not create white lines in between instructions. These are filtered out by the algorithm. So when you want to jump to instruction 10 in your file, it could actually be instruction 8 if there are two white lines somewhere in the file that you see, but the algortihm skips. You could also keep track of this yourself ofcoarse. It is also best practice to never use address 0 of the memory, as this is used for functions as a linker register. To ensure this is enforced, the algorithm starts with the memory counter set to 1. The user has to explicitly jump to memory address 0 to alter the linker register. When you do not know what you are doing, do NOT use this memory register.

### Functions
A function is created by writing a "hok x" instruction and a "weide" instruction with 
other instructions in between. Whenever the interperter reads the "hok x" instruction during execution, it skips all code untill it sees a "weide" instruction, it then begins to execute the next piece of code after the "weide" instruction. The compiler simply creates a new assembly label from the hok which it cuts away from the main. Meaning you can create incapsulated pieces of code in between a hok and weide instruction that are never used. Every 'hok' has a number, which is its identifier. You can use a 'bok x' instruction to call the function you wish to call. In the interperter, this bok also sets the linking register to wherever it came from. The compiler uses the assembly linking register. So when the end of the function is called (with a 'weide') it jumps back to where it was. Notice that when the code is compiled you can use recursion, when the code is interperter you cannot use recursion. You cannot use a 'duif' to jump from the main, into a 'hok'. A 'bok' needs to be used to call a function. There will be undefined behaviour if you do. Within a 'hok' or the main body you can use a 'duif' to jump to different lines. Because of the nature of the language, you can use 'duif' instructions between 'hokken'. I see no use for it, but go nuts with it. There may be some undefined behaviour however, so be carefull.

# Instructions
| instruction | required paramaters | explanation | But why?...|
| ----------- | ----------- | ----------- |
| hok | 1 | Create a function with the identifier as the first parameter | A 'hok' is a Dutch word for a pen. Animals are placed inside a pen. Just like a function is placed in between to boundaries.|
| weide | 0 |  Jump back to where the linking register was pointing to | A 'weide' is a Dutch word for pasture. When a pen is opened, animals are released into the pasture. Or, the program counter is once again free from the function and can continue the main.|
| bok | 1 | Call the function with the identifier of the parameter | a 'bok' is a male goat. They jump on stuff. This instruction jumps to the start of a function|
| wim | 0 | Increase the memory pointer ( mp ) by one | Wim is a male Dutch name. The carrier of this name is male. Males are generally bigger, so plus one. |
| jet | 0 | Decrease the mp by one | Jet is a female Dutch name. The carrier of this name is female. Females are generally smaller, so minus one |
| does | 1 | set the mp to the value of parameter 1 | The kids in the Netherlands use the picture above as a start for learning to read and write. Does is a Dutch name and dog associated in the picture above with the name is dutch shepherd dog. Which are very fast and run from one side of the herd to the other at high speeds. So a does jumps you to which place in the memory you decide at high speed.|
| duif | 1 | jump to other line/instruction of parameter 1 | A 'duif' is the Dutch word for dov. Dovs can fly, so with this instruction you can fly ot another instruction|
| schaap | 0 | increase the integer within the memory at the place the mp currently points to |  A 'schaap' is the Dutch word for sheep. A sheep is an adult which are generally larger than kids, so plus one. |
| lam | 0 |  decrease the integer within the memory at the place the mp currently points to | A 'lam' is the Dutch word for lamb. A lamb is the kids version of a sheep, which is generally smaller than an adult. So minus one. |
| teun | 1 | set the value of the memory where te mp currently points to, to the value that is in the memory on the address of parameter 1 (copy from mp to parameter address) | Teun is Dutch name. The guy associated with the name 'Teun' in the picture above, looks a bit curious. Just as this instruction requires me to think and read it twice. Making it curious. Just as Teun. |
| aap | 2 | If content of memory address on parameter 1 is equal to content of memory address on parameter 2, execute the next instruction, otherwise execute the second next instruction| A 'aap' is a Dutch word for monkey. A monkey has two arms and hands and likes to grab two things and look at them. Maybe even compare them? As does this instruction. |
| noot | 1 | set the value of parameter 1 on the address where the mp currently points to | A 'noot' is the dutch word for nut. A nut generally has something inside it, like a walnut. So this instruction has something inside, and places this in the memory. Nuts are also liked by monkeys, and opened by them to look at or eat them.|
| mies | 0 | print the value of where the mp currently points to | Mies is a Dutch female name. I knew a Mies once and boy, she had a voice like a broken violin on steroids. She would break windows if she screamed. So, this Mies instruction 'screams' whatever you want it to. |
| vuur | 0 | stop execution, this instruction always has to be placed at the end of each file. It may also be placed on other lines.
| 'Vuur' is the Dutch word for fire. In some countries, farmers are still allowed to burn their pastures to increase fertillity (not allowed in the Netherlands anymore). They essential burn all plants and living things back to carbon which makes the ground reusable. Just like this instruction, you stop everything, and you can start anew.

## Example 1, increase register
This small example below will count from 1 to 10 and display each result

1. noot 0 (place 0 at wherever the memory pointer currently points to, which is 1 because of the first wim)
2. wim (add 1 to the memory pointer)
3. noot 10 (place 10 at location 2 in the memory)
4. jet (decrease the memory pointer by one to let it point to 1 again)
5. schaap (add one to the byte where the memory pointer points to. So that is now +1)
6. mies (print the value from where the memory pointer points to)
7. aap 1 2 (jump to instruction line 8 if memory address 0 is equal to address 1, if not, go to instruction line 9)
8. duif 10
9. duif 5 (jump to instruction line 5)
10. vuur (quit the program, or more shakespeary: burn thy pasture and see that thy and it are now barren!)

## Example 2, increase register within function
This small example does the same as example one, but as a function

1. hok 69 (create a hok with identifier 69)
2. schaap (add one)
3. mies (cout)
4. weide (end of function)
5. noot 0 (place 0 on address 1)
6. does 2 (jump to address 2)
7. noot 10 (place 10 on address 2)
8. does 1 (jump to address 1)
9. aap 1 2 (if adress 1 and two are equal, go to next instruction, otherwise go to instruction after that)
10. duif 13 (end the ANM file)
11. bok 69 (call the function 69)
12. duif 9 (do the comparison again after returning from the function)
13. vuur

See aapnootmies.aap for a working example.
All these examples are writtin from my memory, so it could be there is some small logic error.

## Source code
Everything is written in (mostly) functional python and the only object there is (in the interperter), is a weide object. The weide object contains the current state, so it holds the instruction memory list, the memory list, the program counter and the memory counter. Everytime a state is changed by an instruction, a new weide object is created containing a copy of the old weide, with new values. Meaning that an old state is never changed. Currently, the old states are not saved and will probably be removed by the Python garbage collector.

