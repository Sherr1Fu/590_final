import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        s1.transition[sym]=[s2]
        return
        pass 
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for key in self.is_accepting.keys():
            self.is_accepting[key]=not self.is_accepting[key]
        return
        pass
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        currS = self.states[0]
        for i in string:
            if i not in currS.transition:
                return False
            currS=currS.transition[i][0]
        return self.is_accepting[currS.id]
        pass
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        queue=[(self.states[0],"")]
        currS = self.states[0]
        while queue:
            currS,string=queue.pop(0)
            if(len(string)>=len(self.states)):
                break
            if self.is_accepting[currS.id]:
                return string
            for sym in self.alphabet:
                if sym in currS.transition:
                    nextS=currS.transition[sym]
                    string2=string+sym
                    queue.append((nextS[0],string2))
        return "NoMatch"
        pass
    pass