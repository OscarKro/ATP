import copy
from typing import Tuple,Union,List
from ANMdicts import *
import time
class Reader:
    def __init__(self):
        pass
    def __new__(self,filePath : str)-> Tuple[Union[List[str],str]]:
        """Function that reads in a file

        Args:
            filePath (str): The (absolute) path to a file that needs to be read (with .aap extension)

        Returns:
            Tuple[Union[List[str],str]]: Returns a tuple with either a list containing the file seperated on returns on index 0 and an empty string, or an empty list with an error string on index 1 
        """
        if filePath[-4:len(filePath)] == ".aap":
                with open(filePath, "r") as f:
                    text = f.read()
                    text = text.splitlines()
                x = map (lambda a : a.lower(), text)
                return (list(x),"")
        else:
            return ([],"ERROR: file has no .aap extension, extension of file is: " + filePath[-4:len(filePath)])

class Lexer:
    def __init__(self):
        pass
    
    def __convert_string_to_int_noerror(self, string : str) -> bool:
        """Function that checks if a string can also be a number

        Args:
            string (str): The string that needs to be checked

        Returns:
            bool: True if all elements in the string can be interpeterd as a number
        """
        if string[0] == '-':
            s = string[1:]
        else:
            s = string
        return all(map(lambda i : i.isnumeric(),s))
    

    def disassemble_list(self, l : List[List[str]]) -> List[str]:
        """Recursive function that disassembles a list containing lists into a single long list with all elements seperated

        Args:
            l (List[List[str]]): The list containing lists that need to be assembled into one long list

        Returns:
            List[str]: A long list with all elements
        """
        if len(l) == 0 :
            return []
        head, *tail = l
        return head + self.disassemble_list(tail)


    def __seek_syntax_errors(self, l : List[Union[str,int]]) -> List[str]:
        """Function that recursively checks if the list with all words from the .aap file has good syntax

        Args:
            l (List[Union[str,int]]): A list with all the words from the .aap file, seperated on word and parameters, where the parameters need to be integers

        Returns:
            List[str]: a list with all (or none) errors
        """
        if len(l) == 0:
            return []
        nrOfParam = checkNrParamDict.get(l[0],None)
        if nrOfParam != None:
            if (l[0] == "duif" and l[1] <= 0):
                return ["Syntax error: 'duif' instruction cannot jumpeth to 0 'r negative numb'rs. A dove cannot flyeth into the negative"] + self.__seek_syntax_errors([])
            if (l[0] == "hok"):
                try:
                    x = l.index("weide")
                except ValueError:
                    return ["Syntax error: instruction 'hok' hast nay closing 'weide'. How can i closeth a doth'r without a handleth?"] + self.__seek_syntax_errors([])
            if nrOfParam > 0:
                if 1 + nrOfParam > len(l):
                    return ["Syntax error: lasteth instruction doest not has't the c'rrect amount of instruction"] + self.__seek_syntax_errors([])
                else:
                    head, *tail = l[nrOfParam:]
                    if not all(map(lambda i : isinstance(i,int),l[1:nrOfParam+1])): #if not every parameter is numeric
                        return ["Syntax error: not all paramet'rs of w'rd: '" + str(l[0]) + "' art integ'rs. I only accepteth integ'rs as valid wage"] + self.__seek_syntax_errors(tail)
                    return [] + self.__seek_syntax_errors(tail) 
            else:
                head, *tail = l
                return [] + self.__seek_syntax_errors(tail)
        else:
            head, *tail = l
            return ["Syntax error: instruction '" + str(head) + "' doest not existeth.Thee shouldst asketh f'r something yond exists, to beest 'r not to beest, yond is the questioneth"] + self.__seek_syntax_errors(tail)
       

    
    def lex(self, listOfLines : List[str]) -> Tuple[Union[str,int],List[str]]:
        x = map (lambda a: a.split(),listOfLines) # create a list with all lines seperated for each instruction
        simpleLexedList = self.disassemble_list(list(x)) # create a list with all items seperated, including the parameters
        y = map (lambda a : int(a) if self.__convert_string_to_int_noerror(a) else a, simpleLexedList ) # if possible, turn the parameters into integers
        lexedList = list(y) 
           
        #check for wrong words, number of parameters and if they are numbers
        #============================================================================
        errorList = []
        if (lexedList[len(lexedList)-1] != "vuur"):
            errorList.append("syntax error: lasteth instruction shouldst at each moment beest 'vuur'. burneth thy pastures at which hour thou art done!")
        errorList += self.__seek_syntax_errors(lexedList) # check if the syntax is correct, if not, errorList is filled with errors
        return (lexedList,errorList)

class Parser:
    
    def __init__(self):
        pass

    def __create_single_instruction(self, l : List[Union[str,int]]) -> List[Union[str,int]]:
        """Function that takes a list with a single instruction and its parameters from a list with instructions and parameters

        Args:
            l (List[Union[str,int]]): a list with an instruction word on index 0 and its parameters on the next indeces if they are required for that instruction

        Returns:
            List[Union[str,int]]: a list with a single instruction. For example [aap,5,5,3]
        """
        if len(l) == 0:
            return []
        nrOfParam = checkNrParamDict.get(l[0],None)
        if nrOfParam == None:
            return []
        return l[0:nrOfParam+1]
    
    def __create_list_with_instructions(self, l : List[Union[str,int]]) -> List[List[Union[str,int]]]:
        """Function that creates a list with lists containing all instructions

        Args:
            l (List[Union[str,int]]): the lexed list containing all words on seperate indeces

        Returns:
            List[List[Union[str,int]]]: A list of lists containing all instructions grouped per instruction
        """
        if len(l) == 0:
            return []
        nrOfParam = checkNrParamDict.get(l[0],None)
        if nrOfParam == None:
            return []
        return [self.__create_single_instruction(l[:nrOfParam+1])] + self.__create_list_with_instructions(l[nrOfParam+1:])

    def parse(self, lexedList : List[Union[str,int]] ) -> List[Union[str,int]]:
        """Function to create a parsed list containing the instructions

        Args:
            lexedList (List[Union[str,int]]): the lexed list

        Returns:
            List[Union[str,int]]: a parsed list containg all instructions on a seperate indeces
        """
        parsedCode = self.__create_list_with_instructions(lexedList)
        return copy.deepcopy(parsedCode)


        





