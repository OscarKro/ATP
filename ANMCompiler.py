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
    print("couldn't executeth programeth.  Err'rs hath found")
    exit()   
print("filepath: ", end = ' ')


def translate_to_normal_list(l : List[Union[str,int]]) -> List[str]:
    """Function to create a 1 dimensional list with strings from a 2 dimensional list

    Args:
        l (List[Union[str,int]]): The 2 dimensional list

    Returns:
        str: A 1 dimensional list with strings
    """
    if (len(l) == 1):
        return l[0]
    return l[0] + translate_to_normal_list(l[1:])

def bundle_instructions_to_2dimensional_list(l : List[Union[str,int]]) -> List[List[Union[str,int]]]:
    """Function to translate a 1 dimensional list of aap noot mies instructions to a 2 dimensional list with each total instruction on a seperate index

    Args:
        l (List[Union[str,int]]): The original lexed list of a aap noot mies file

    Returns:
        List[List[Union[str,int]]]: A 2 dimensional list
    """
    oneInstruction = []
    if (len(l) == 1):
        oneInstruction.append([l[0]])
        return oneInstruction
    nrOfParam = checkNrParamDict.get(l[0])
    oneInstruction.append(l[0:nrOfParam+1])
    return oneInstruction + bundle_instructions_to_2dimensional_list(l[nrOfParam+1:])

def change_hok_to_duif(l : List[List[Union[str,int]]]) -> List[List[Union[str,int]]]:
    n = [copy.deepcopy(l[0])]
    if (len(l) <= 1):
        return n
    if (n[0] == ["hok"]):
        i = l.index(["weide"])
        n[0] = ["duif"]
        n[0].append(i+2)
    return n + l[1:]
    

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


def create_list_with_dov_labels(l : list[Union[str,int]], el : List[List]) -> List[List[str]]:
    newList = copy.deepcopy(el) #create new because functional...
    if (len(l) <= 1):
        return newList
    if (l[0] == "duif"):
        jumpTo = l[1]
        label = "\n_D" + str(jumpTo) + ":"
        newList[jumpTo-1] = [label]
        return create_list_with_dov_labels(l[2:],newList)
    return create_list_with_dov_labels(l[1:],newList)

#Get the user input and the file name
#============================================================================
i = input()
if not os.path.isfile(i):
    print("no fileth hath found")
    stop()
nameOfFile = i[:-4]
print("we art anon starting the compilation of the fileth: " + nameOfFile)

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
q = translate_to_normal_list(change_hok_to_duif(bundle_instructions_to_2dimensional_list(lexedData[0])))
b = translate_to_asm_list(q)
c = create_list_with_dov_labels(q,[[]] * len(q))
d = list(zipWith(lambda x,y:x+y,c,b))
e = translate_to_normal_list(d)
memorySize = 1000
asmText = start_code_section()
asmText += start_of_ANM_and_allocate_memory_on_stack(memorySize,nameOfFile)
for item in e:
    #no use to do this functional. Yes recursion is possible here, but i'm not going through the trouble for something so trivial.
    asmText += item
asmFile = open(nameOfFile + ".asm", "w")
asmFile.write(asmText)
asmFile.close()
print("did finish compiling " + i + " succesfull.")
