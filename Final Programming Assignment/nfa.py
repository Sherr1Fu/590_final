from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        if sym in s1.transition:
            s1.transition[sym].append(s2)
        else:
            s1.transition[sym]=[s2]
        return
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        state_map=dict()
        state_number=len(self.states)   #self has n states
        for i in range(len(nfa.states)):
            state_map[i]=i+state_number
            self.states.append(nfa.states[i])
            self.states[state_number+i].id=state_map[i]
            self.is_accepting[state_map[i]]=nfa.is_accepting[i]
        for k in nfa.alphabet:
            if k not in self.alphabet:
                self.alphabet.append(k)
        return state_map
        pass
    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose2(self, ns):
        states = set(ns)
        stack=ns
        while stack:
            currS=stack.pop()
            if '&' in currS.transition:
                for nextS in currS.transition['&']:
                    if nextS not in states:
                        states.add(nextS)
                        stack.append(nextS)
        # for n in ns:
        #     states.append(n)
        #     for sym, nn in self.states[n.id].transition.items():  
        #         if sym == '&':
        #             for s in nn:
        #                 states.append(s)
        #                 if s not in ns:
        #                     ns.append(s)
        return states
    
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return states
    # It takes a string and returns True if the string is in the language of this NFA
    def problematic(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop()
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass

    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop(0)  #We should use queue.pop(0) instead of queue.pop()
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass