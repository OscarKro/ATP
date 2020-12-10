from ANMCompilerTokens import *
from lexer_parser import Reader,Lexer
from ANMdicts import checkNrParamDict,compilerLambdaDict
from typing import Union,List
import os.path
import sys
import copy

def hold_console():
    i = input()
    exit()


def stop():
    print("couldn't execute program. Errors found")
    exit()   
print("filepath: ", end = ' ')

def translate(l : List[Union[str,int]]) -> str:
    """Recursive function that takes a list, gets the first ANM instruction from the list and its paramaters, and gives back a string with the according assembly code using
    the compiler lambda dict and all the functions from ANMCompilerTokens.py

    Args:
        l (List[Union[str,int]]): The lexed list of all instructions

    Returns:
        str: A string with compiled ANM code to assembly
    """
    if (len(l) == 0):
        return ""
    if (len(l) == 1):
        f = compilerLambdaDict.get(l[0])
        return f(l[0])
    
    nrOfParam = checkNrParamDict.get(l[0])
    args = l[0:nrOfParam+1]
    f = compilerLambdaDict.get(args[0]) 
    return f(*args) + translate(l[nrOfParam+1:])

def translate_to_asm_list(l: List[Union[str,int]]) -> List[List[str]] :
    if (len(l) == 0):
        return []
    if (len(l) == 1):
        f = compilerLambdaDict.get(l[0])
        return [[f(l[0])]]
    nrOfParam = checkNrParamDict.get(l[0])
    args = l[0:nrOfParam+1]
    f = compilerLambdaDict.get(args[0])
    return [[f(*args)]] + translate_to_asm_list(l[nrOfParam+1:])

def create_list_with_dovs(l : list[Union[str,int]], el : List[List]) -> List[List[str]]:
    newList = copy.deepcopy(el)
    if (len(l) <= 1):
        return newList
    if (l[0] == "duif"):
        jumpTo = l[1]
        label = "_L" + str(jumpTo)
        newList[jumpTo-1] = [label]
        return create_list_with_dovs(l[1:],newList)
    return create_list_with_dovs(l[1:],newList)

#Get the user input and the file name
#============================================================================
i = input()
if not os.path.isfile(i):
    print("No file found")
    stop()
nameOfFile = i[:-4]
print(nameOfFile)

#Read the file with instructions and print and exit if an error occured
#============================================================================
f = Reader(i)
if f[1] != "":
    print(f[1])
    stop()

#Lex whatever has been read
#============================================================================
lexer = Lexer()
lexedData = lexer.lex(f[0])
#print the errors and exit the interperter if errors were found
#============================================================================
if len(lexedData[1]) > 0:
    x = list(map(lambda i : print(i),lexedData[1])) 
    stop()
#Create the base Assembly with all the labels
#============================================================================
memorySize = 1000
a = start_code_section()

a += Wim()
a += Jet()
a += Does()
a += Schaap()
a += Lam()
a += Teun()
a += Aap()
a += Noot()
a += Vuur()

a += start_of_ANM_and_allocate_memory_on_stack(memorySize,"_" + nameOfFile)

a += translate(lexedData[0])
create_list_with_dovs(lexedData[0],[[]]*len(lexedData[0]))
print(translate_to_asm_list(lexedData[0]))
asmFile = open(nameOfFile + ".asm", "w")
asmFile.write(a)
asmFile.close()
print("finished compiling " + i + " succesfull. Thank you for using AapNootMies")
