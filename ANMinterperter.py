from lexer_parser import *
from ANMdicts import *
from ANMtokens import Weide
import os.path
import sys

def stop():
    print("Couldn't executeth programeth.  Err'rs hath found")
    exit()
print("filepath: ", end = ' ')

i = input()
if not os.path.isfile(i):
    print("Nay fileth hath found")
    stop()

#test functie voor de decorator, niet gebruiken.
def add(a,b):
    return a + b

def debug_function(f : callable, *args) -> callable:
    """Function to test a function with or without arguments

    Args:
        f (callable): The function you want to test

    Returns:
        callable: The result of the function or an error
    """
    try:
        return  f(*args)
    except:
        return sys.exc_info()

#"By definition, a decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it."
# source : "https://realpython.com/primer-on-python-decorators/"
@debug_function
def dubble_down(f : callable, *args):
    """Python decorator function that calls another function twice and calls the '+' operator on both

    Args:
        f (callable): The function you want to call

    Returns:
        [type]: the parameter function called twice with a '+' operator called on them
    """
    return f(*args) + f(*args)


# print(debug_function(add, 'a' , 5))
# print(debug_function(add,5,5))
# x = lambda : add(5,5)
# print(dubble_down(x))
# print(dubble_down(add,10,10))
# exit()

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
#parse the data into a list (all instructions grouped in a list)
#============================================================================
parser = Parser()
parsedData = parser.parse(lexedData[0])
#execute
#============================================================================
l = [0] * 1001 # create the size 1000 memory
w = Weide(parsedData,l,0,1) #create the first weide with the pc to the first instruction, and the mc set to adress 1 so the linking register is initialy left alone
while True:
    instruction = interperterlambdaDict.get(w.instructionMemoryList[w.pc][0],None)
    nrOfParam = checkNrParamDict.get(w.instructionMemoryList[w.pc][0],None)
    if nrOfParam == None:
        stop()
    elif nrOfParam > 0:
        w = instruction(w,*w.instructionMemoryList[w.pc][1:nrOfParam+1])
    else:
        w = instruction(w)



