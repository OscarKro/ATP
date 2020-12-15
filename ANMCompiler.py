from ANMCompilerTokens import *
from lexer_parser import Reader,Lexer
from ANMdicts import checkNrParamDict,compilerLambdaDict
from typing import *
import os.path
import sys
import copy

def hold_console():
    i = input()
    exit()

def stop():
    print("couldn't executeth programeth.  Err'rs hath found")
    exit()   
print("filepathé: ", end = ' ')

A = TypeVar('A')
def replace_item_in_list(index : int, replacement : A, l : List[A]):
    """Function to change a thing in a list

    Args:
        index (int): the index at which something needs to be changed
        replacement (A): The replacement
        l (List[A]): the original list

    Returns:
        [type]: A new list with the object at the index parameter swapped for the replacement
    """
    return l[:index] + [replacement] + list[index+1:]

def translate_to_1_dimensional_list(l : List[Union[str,int]]) -> List[str]:
    """Function to create a 1 dimensional list with strings from a 2 dimensional list

    Args:
        l (List[Union[str,int]]): The 2 dimensional list

    Returns:
        str: A 1 dimensional list with strings
    """
    if (len(l) == 1):
        return l[0]
    return l[0] + translate_to_1_dimensional_list(l[1:])

# def bundle_instructions_to_2dimensional_list(l : List[Union[str,int]]) -> List[List[Union[str,int]]]:
#     """Function to translate a 1 dimensional list of aap noot mies instructions to a 2 dimensional list with each total instruction on a seperate index

#     Args:
#         l (List[Union[str,int]]): The original lexed list of a aap noot mies file

#     Returns:
#         List[List[Union[str,int]]]: A 2 dimensional list
#     """
#     oneInstruction = []
#     if (len(l) == 1):
#         oneInstruction.append([l[0]])
#         return oneInstruction
#     nrOfParam = checkNrParamDict.get(l[0])
#     oneInstruction.append(l[0:nrOfParam+1])
#     return oneInstruction + bundle_instructions_to_2dimensional_list(l[nrOfParam+1:])

# def change_shet_to_dov_in_2_dimensional_List(l : List[List[Union[str,int]]]) -> List[List[Union[str,int]]]:
#     """Function that changes every hok to a duif with the correct line number

#     Args:
#         l (List[List[Union[str,int]]]): A list, containing lists with an aap noot mies instruction on every line

#     Returns:
#         List[List[Union[str,int]]]: A list, containg lists where every hok in the original is changed to a duif that flies to the next instruction after a weide
#     """
#     n = [copy.deepcopy(l[0])]
#     if (len(l) <= 1):
#         return n
#     if (n[0] == ["hok"]):
#         i = l.index(["weide"])
#         n[0] = ["duif"]
#         n[0].append(i+2)
#     return n + l[1:]

def get_all_functions(l : List[Union[str,int]]) -> List[Union[str,int]]:
    """Function to get all the pieces of code from a hok to a weide from a list with lexed code from the ANM lexer

    Args:
        l (List[Union[str,int]]): A list with lexed code from the ANM lexer

    Returns:
        List[Union[str,int]]: A list with only the functions between hokken and weides
    """
    if (len(l) == 0):
        return []
    if (l[0] == "hok"):
        i = l.index("weide")
        return l[0:i+1] + get_all_functions(l[i+1:])
    else:
        return get_all_functions(l[1:])

def remove_all_functions(l : List[Union[str,int]]) -> List[Union[str,int]]:
    """Function to remove all the functions from a list with lexed code

    Args:
        l (List[Union[str,int]]): A list with lexed code from the ANM lexer

    Returns:
        List[Union[str,int]]: A list with the lexed ANM code without all code between a hok and weide
    """
    if (len(l) == 0):
        return []
    if (l[0] == "hok"):
        i = l.index("weide")
        return remove_all_functions(l[i+1:])
    return [copy.deepcopy(l[0])] + remove_all_functions(l[1:])   

# def translate_to_asm_list(l: List[Union[str,int]]) -> List[List[str]] :
#     if (len(l) == 0):
#         return []
#     if (len(l) == 1):
#         f = compilerLambdaDict.get(l[0])
#         return [[f(l[0])]]
#     nrOfParam = checkNrParamDict.get(l[0])
#     args = l[0:nrOfParam+1]
#     f = compilerLambdaDict.get(args[0])
#     return [[f(*args)]] + translate_to_asm_list(l[nrOfParam+1:])

# def create_list_with_dov_labels(l : list[Union[str,int]], el : List[List]) -> List[List[str]]:
#     newList = copy.deepcopy(el) #create new because functional...
#     if (len(l) <= 1):
#         return newList
#     if (l[0] == "duif"):
#         jumpTo = l[1]
#         label = "\n_D" + str(jumpTo) + ":"
#         newList[jumpTo-1] = [label]
#         return create_list_with_dov_labels(l[2:],newList)
#     return create_list_with_dov_labels(l[1:],newList)

# def change_shet_to_dov(l: List[Union[str,int]]) -> List[Union[str,int]]:
#     """Function that bundles the bundle isntructions function, change all shet to dovs function and unbundle it all into one function

#     Args:
#         l (List[Union[str,int]]): The lexed list from a aap noot mies file

#     Returns:
#         List[Union[str,int]]: A list with strings, containing anm instructions but with all 'hok' instructions changed to 'duif' with the correct paramater
#     """
#     print(get_all_functions(l))
#     bundled = bundle_instructions_to_2dimensional_list(l)
#     changed = change_shet_to_dov_in_2_dimensional_List(bundled)
#     unbundled = translate_to_1_dimensional_list(changed)
#     return unbundled

def create_base_assembly_instructions(l : List[Union[str,int]],i : int = 0) -> List[str]:
    """Function that creates assembly instructions (main!) from anm instructions, but skips all hokken, as these are functions themselves.
    It is differnt from the create_assembly_function_instructions because it creates all labels for instructions with a _L prefix and not a _HL prefix.
    So a duif and Aap only work on the main body of code and not all functions

    Args:
        l (List[Union[str,int]]): A list with correct anm instructions that have been run through the lexer.
        i (int, optional): A parameter used for counting which instruction label to jump to for some assembly instructions. DO NOT TOUCH!. Defaults to 0.
    Returns:
        List[str]: A list with strings containing assembly for each aap noot mies instruction except the pieces between hok and weides
    """
    if (len(l) == 0):
        return [""] # if the length of the list with instructions is zero, compiling is done
    if (l[0] == "hok"): #skip hokken
        ind = l.index("weide")
        i += (ind) # add the amount of instruction lines to the i
        return create_base_assembly_instructions(l[ind + 1:],copy.deepcopy(i))
    instructionLabel = "\n_L" + str(i) + ":" # the label this instruction gets
    nrOfParameters = checkNrParamDict.get(l[0]) # get the number of parameters from this instruction from the dict
    function = compilerLambdaDict.get(l[0]) # get the function that belongs to this instructions (which creates the string of assembly instead of this aap noot mies instruction)
    args = l[0:nrOfParameters+1] # get the arguments that belong to the function
    if (l[0] == "duif"):
        args[1] = "_L" + str(l[1]-1)
    if (l[0] == "aap"):
        args.append("_L"+str(i + 1))
        args.append("_L"+str(i + 2))
    return [instructionLabel + function(*args)] + create_base_assembly_instructions(l[nrOfParameters+1:],copy.deepcopy(i)+1) # create the assembly instruction and contatenate the next one recursive

def create_assembly_function_instructions(l : List[Union[str,int]], i : int = 0) -> List[str]:
    """A function that creates assembly for all the code between a hok and weide. It is different from the create_base_assembly_instructions because
    it creates labels for instructions with a _HL prefix and not a _L prefix so a duif and aap only work within a function and not on the main labels.

    Args:
        l (List[Union[str,int]]): A list with lexed code that has been run through the ANM lexer and trougth the get_all_functions function
        i (int, optional): Do not touch. Used for passing on label numbers recursively. Defaults to 0.

    Returns:
        List[str]: A list with assembly instructions for each aap noot mies instruction
    """
    instructionLabel = ""
    if (len(l) == 0):
        return [""]
    if (l[0] != "hok"):
        instructionLabel = "\n_HL" + str(i) + ":"
    nrOfParameters = checkNrParamDict.get(l[0])
    function = compilerLambdaDict.get(l[0])
    args = l[0:nrOfParameters+1]
    if (l[0] == "duif"):
        args[1] = "_HL" + str(l[1]-1)
    if (l[0] == "aap"):
        args.append("_HL"+str(i + 1))
        args.append("_HL"+str(i + 2))
    return [instructionLabel + function(*args)] + create_assembly_function_instructions(l[nrOfParameters+1:], copy.deepcopy(i)+1)        
        
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
#print(f[0])

#Lex whatever has been read
#============================================================================
lexer = Lexer()
lexedData = lexer.lex(f[0])
#print the errors and exit the compiler if errors were found
#============================================================================
if len(lexedData[1]) > 0:
    x = list(map(lambda i : print(i),lexedData[1])) 
    stop()
#print(lexedData[0])

#Create the base Assembly with all the labels
#============================================================================

memorySize = 100
asmText = start_code_section(nameOfFile)
listWithCompiledFunctions = create_assembly_function_instructions(get_all_functions(lexedData[0]))
listWithCompiledMain = create_base_assembly_instructions(lexedData[0])
for ins in listWithCompiledFunctions: #this for loop is approved by Jan on 11-12 ~16:50!
    asmText += ins
# s = ""
# a = s.join(listWithCompiledFunctions)
asmText += start_of_ANM_and_allocate_memory_on_stack(memorySize,nameOfFile)
for ins in listWithCompiledMain:
    asmText += ins
# a += s.join(listWithCompiledMain)
# asmText += a
#Write the ASM text in the file
#============================================================================
asmFile = open(nameOfFile + ".asm", "w")
asmFile.write(asmText)
asmFile.close()
print("did finish compiling " + i + " succesfull.")
 