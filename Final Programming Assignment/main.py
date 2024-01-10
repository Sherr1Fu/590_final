import copy
from regex import *
from state import * 
from nfa import *
from dfa import *
from collections import deque

# You should write this function.
# It takes an NFA and returns a DFA.
def move(states, symbol):
    next_states = set()

    for state in states:
        if symbol in state.transition:
            next_states.update(state.transition[symbol])

    return next_states

def union(nfa1,nfa2):
    len1=len(nfa1.states)
    nfa1.addStatesFrom(nfa2)
    nfa1.addTransition(nfa1.states[0],nfa1.states[len1])
    return nfa1    

def nfaToDFA(nfa):
    dfa=DFA()
    dfa.alphabet=nfa.alphabet
    init_state=nfa.epsilonClose2([nfa.states[0]])
    #dfa.states=[nfa.epsilonClose2([nfa.states[0]])]   #init state of DFA
    dfa.states=[State(0)]
    dfa.is_accepting[0]=False
    for i in init_state:
        if nfa.is_accepting[i.id]:
            dfa.is_accepting[0]=True
            break
    #state_queue=deque(dfa.states[0])
    #computedstate=[dfa.states[0]]
    state_queue=deque([init_state])
    computedstate=[init_state]
    while state_queue:
        currS=state_queue.popleft()
        for symbol in nfa.alphabet:
            nextS=nfa.epsilonClose2(list(move(currS,symbol)))
            if nextS:
                if nextS not in computedstate:
                    #dfa.states.append(nextS)
                    dfa.states.append(State(len(computedstate)))
                    dfa.is_accepting[len(dfa.states)-1]=False
                    #map[nextS]=len(computedstate)
                    for state in nextS:
                        if nfa.is_accepting[state.id]:
                            dfa.is_accepting[len(dfa.states)-1]=True
                            break
                    state_queue.append(nextS)
                    computedstate.append(nextS)
                            
                    
                dfa.addTransition(dfa.states[computedstate.index(currS)],dfa.states[computedstate.index(nextS)],symbol)
    return dfa                   
    pass
# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa=NFA()
    nfa.states=copy.deepcopy(dfa.states)
    nfa.is_accepting=copy.deepcopy(dfa.is_accepting)
    nfa.alphabet=copy.deepcopy(dfa.alphabet)
    return nfa
    pass
# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1=re1.transformToNFA()
    nfa2=re2.transformToNFA()
    dfa1f=nfaToDFA(nfa1)
    dfa1f.complement()
    dfa1=nfaToDFA(nfa1)
    dfa2f=nfaToDFA(nfa2)
    dfa2f.complement()
    dfa2=nfaToDFA(nfa2)

    union1=union(dfaToNFA(dfa1f),dfaToNFA(dfa2))
    union2=union(dfaToNFA(dfa2f),dfaToNFA(dfa1))

    dfa1e=nfaToDFA(union1)
    dfa2e=nfaToDFA(union2)

    dfa1e.complement()
    dfa2e.complement()

    # str1=dfa1e.shortestString()
    # str2=dfa2e.shortestString()

    for i in dfa1e.is_accepting:
        if dfa1e.is_accepting[i]==True:
            return False
    
    for i in dfa2e.is_accepting:
        if dfa2e.is_accepting[i]==True:
            return False
    return True

    # print(str1)
    # print(str2)
    # if str1=="NoMatch" and str2=="NoMatch":
    #     return True
    # return False

    pass



if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        #res=nfa.problematic(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA_old(nfa, s, expected):
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(strRe, s, expected):
        # test your dfa conversion
        re = parse_re(strRe)
        nfa = re.transformToNFA()
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass
    testNFA('&','', True)
    #test your NFA:
    testNFA('a', '', False)
    testNFA('a', 'a', True)
    testNFA('a', 'ab', False)
    testNFA('ab', 'ab', True)
    testNFA('a*', '', True)
    testNFA('a*', 'a', True)
    testNFA('a*', 'aaa', True)
    testNFA('a|b', '', False)
    testNFA('a|b', 'a', True)
    testNFA('a|b', 'b', True)
    testNFA('a|b', 'ab', False)
    testNFA('ab|cd', '', False)
    testNFA('ab|cd', 'ab', True)
    testNFA('ab|cd', 'cd', True)
    testNFA('ab|cd*', '', False)
    testNFA('ab|cd*', 'c', True)
    testNFA('ab|cd*', 'cd', True)
    testNFA('ab|cd*', 'cddddddd', True)
    testNFA('ab|cd*', 'ab', True)
    testNFA('ab|cd*', 'abc', False)
    testNFA('((ab)|(cd))*', '', True)
    testNFA('((ab)|(cd))*', 'ab', True)
    testNFA('((ab)|(cd))*', 'cd', True)
    testNFA('((ab)|(cd))*', 'abab', True)
    testNFA('((ab)|(cd))*', 'abcd', True)
    testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ad', False)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    testNFA('(aab)|(ab)|((e(ee)*)|((ee)*((aab)|(ab))))','ee',False)

    testDFA('&', '', True)
    testDFA('(&)', '', True)
    testDFA('&', 'a', False)
    testDFA('a', '', False)
    testDFA('a', 'a', True)
    testDFA('a', 'ab', False)
    testDFA('(a)', 'a', True)
    testDFA('((a))', 'a', True)
    testDFA('ab', 'ab', True)
    testDFA('abc', 'abc', True)
    testDFA('abcd', 'abcd', True)
    testDFA('a(bc)d', 'abcd', True)
    testDFA('a*', '', True)
    testDFA('a*', 'a', True)
    testDFA('a*', 'aaa', True)
    testDFA('a*b*', 'a', True)
    testDFA('a*b*', 'ab', True)
    testDFA('a*b*', 'b', True)
    testDFA('a*b*', 'aba', False)
    testDFA('a|b', '', False)
    testDFA('a|b', 'a', True)
    testDFA('a|b', 'b', True)
    testDFA('a|b', 'ab', False)
    testDFA('ab|cd', '', False)
    testDFA('ab|cd', 'ab', True)
    testDFA('ab|cd', 'cd', True)
    testDFA('ab|cd*', '', False)
    testDFA('ab|cd*', 'c', True)
    testDFA('ab|cd*', 'cd', True)
    testDFA('ab|cd*', 'cddddddd', True)
    testDFA('ab|cd*', 'ab', True)
    testDFA('((ab)|(cd))*', '', True)
    testDFA('((ab)|(cd))*', 'ab', True)
    testDFA('((ab)|(cd))*', 'cd', True)
    testDFA('((ab)|(cd))*', 'abab', True)
    testDFA('((ab)|(cd))*', 'abcd', True)
    testDFA('((ab)|(cd))*', 'cdcdabcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    testDFA('((a|b)*|b)*', 'ababb', True)

    testEquivalence('((a|b)*|b)*','(b)((a|b)*|b)*',False)
    testEquivalence('a*','aa*',False)
    testEquivalence('a|b', 'a|((a|b)|b)', True)
    testEquivalence('(a|b)*', '(a|((a|b)|b))*', True)
    testEquivalence('&', '&&', True)
    testEquivalence('&', '&&a', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '((ab|cd)*|(de*fg|h(ij)*klm*m*n|q))*',True)
    pass
    
