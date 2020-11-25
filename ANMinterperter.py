from lexer_parser import *
from ANMdicts import *
import os.path

def stop():
    print("couldn't execute program. Errors found")
    exit()
print("filepath: ", end = ' ')
i = input()
if not os.path.isfile(i):
    print("No file found")
    stop()

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
w = Weide(parsedData,[],1,0) #create the first weide with the pc to the first instruction
while True:
    instruction = lambdaDict.get(w.instructionMemoryList[w.pc][0],None)
    nrOfParam = checkNrParamDict.get(w.instructionMemoryList[w.pc][0],None)
    if nrOfParam == None:
        stop()
    elif nrOfParam > 0:
        w = instruction(w,*w.instructionMemoryList[w.pc][1:nrOfParam+1])
    else:
        w = instruction(w)



