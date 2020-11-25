import copy
from typing import *

def cp(x):
    """Function to quickly copy an object

    Args:
        x (anything): THe thing that needs to be copied

    Returns:
        anything: the copied thing
    """
    return copy.deepcopy(x)

class Weide:
    """Class that implements the list of instructions, the program counter, the memory and the memorypointer
    """
    def __init__(self, instructionMemoryList : List[Union[str,int]], memoryList : List[int], pc : int, mc : int):
        """Constructor of weide object

        Args:
            instructionMemoryList (List[Union[str,int]]): A list containing all instructions and their parameters as lists
            memoryList (List[int]): A list that is used as memory for integers
            pc (int): The program counter (points to an index within the instructionMemoryList)
            mc (int): The memory counter (points to an index within the memoryList)
        """
        self.instructionMemoryList = instructionMemoryList
        self.memoryList = memoryList
        self.pc = pc
        self.mc = mc

def Wim(w : Weide) -> Weide:
    """Function to increase the memory counter by one

    Args:
        w (Weide): A weide object

    Returns:
        Weide: A new weide object with the memory counter increased by one
    """
    return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(w.pc)+1,cp(w.mc)+1)


def Jet(w : Weide) -> Weide:
    """Function to decrease the memory counter by one

    Args:
        w (Weide): A weide object

    Returns:
        Weide: A new weide object with the memory counter decreased by one
    """
    return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(w.pc)+1,cp(w.mc)-1)


def Duif(w : Weide, goto : int) -> Weide:
    """Function to set the program counter to a different adress

    Args:
        w (Weide): A weide object
        goto (int): The go to adress within the weide's instruction memory

    Returns:
        Weide: A new weide object with the program counter set to the go to value
    """
    return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(goto)-1,cp(w.mc))


def Schaap(w : Weide) -> Weide:
    """Function to increase the byte the memory counter points to by one

    Args:
        w (Weide): A weide object

    Returns:
        Weide: A new weide object with the integer contained within the memory at the location of the memory counter increased by one
    """
    x = cp(w.memoryList)
    x[w.mc] += 1
    return Weide(cp(w.instructionMemoryList),x,cp(w.pc)+1,cp(w.mc))


def Lam(w : Weide) -> Weide:
    """Function to decrease the byte the memory counter points to by one

    Args:
        w (Weide): A weide object

    Returns:
        Weide: A new weide object with the integer contained within the memory at the location of the memory counter decreased by one
    """
    x = cp(w.memoryList)
    x[w.mc] -= 1
    return Weide(cp(w.instructionMemoryList),x,cp(w.pc)+1,cp(w.mc))


def Aap(w : Weide,x : int, y : int, goto : int) -> Weide:
    """Function to compare two adresses and jump to the third parameter if they are equal or continue with the next instruction if they are unequal (BEQ)

    Args:
        w (Weide): A weide object
        x (int): The first memory adress from which the content needs to be compared
        y (int): The second memory adress from which the content needs to be compared
        goto (int): The instruction adress (line) to jump to if x and y are equal

    Returns:
        Weide: A new weide object with the program counter set to the outcome of comparison
    """
    if (w.memoryList[x] == w.memoryList[y]):
        return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(goto)-1,cp(w.mc))
    else:
        return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(w.pc)+1,cp(w.mc))


def Noot(w : Weide, v : int) -> Weide:
    """Function to set a value in the memory at the adress the memory counter currently points to

    Args:
        w (Weide): A weide object
        v (int): The value that needs to be set

    Returns:
        Weide: A new weide object with the value set in the memory at the location the memory counter is currently pointing to
    """
    w = Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(w.pc)+1,cp(w.mc))
    w.memoryList.insert(w.mc,cp(v))
    return w

def Mies(w : Weide) -> Weide:
    """Function to print the value of the memory the memory counter currently points to

    Args:
        w (Weide): A weide object

    Returns:
        Weide: A new weide object with the program counter increased by one (to execute the next instruction)
    """
    print(w.memoryList[w.mc])
    return Weide(cp(w.instructionMemoryList),cp(w.memoryList),cp(w.pc)+1,cp(w.mc))

def Vuur(w : Weide) -> Weide:
    """Function to finish execution

    Args:
        w (Weide): A weide object

    Returns:
        Weide: Absolutely nothing
    """
    exit()