import json
import sys
import os
from itertools import chain, combinations
# ASSuminmg no e transitionss
class NFA:
    def __init__(self, states=[], letters=[], transition_function=[], start_states=[], final_states=[]):
        self.states = states
        self.letters = letters
        self.transition_function = transition_function
        self.start_states = start_states
        self.final_states = final_states


    def get_dict(self):
        N = {}
        N["states"] = self.states
        N["letters"] = self.letters
        N["transition_function"] = self.transition_function
        N["start_states"] = self.start_states
        N["final_states"] = self.final_states
        return N

def powerset(states):
    if len (states) <= 1:
        yield states
        yield []
    else:
        for item in powerset(states[1:]):
            yield [states[0]] + item
            yield item
    

def get_final_states(N):
    return []
    
def E(s, N):
    # assuming one \eps depth
    next_states = [s]
    for t in N.transition_function:
        if t[0] == s and t[1] == '$':
            next_states.append(t[2])
    return next_states

def get_DFA_from_NFA(N):
    # mutation problems
    D = NFA() 
    P = list(powerset(N.states))
    P.reverse() # to get in lexicographical order
    D.states = [s for s in P]
    D.letters = N.letters
    assert len(N.start_states) == 1, "can't handle NFA with more than 1 start state"
    D.start_states = [N.start_states]
    
    for R in D.states:
        for s in N.final_states:
            if s in R:
                D.final_states.append(R)
                break

    for R in D.states:
        for a in D.letters:
            next_states = set()
            for r in R:
                for t in N.transition_function:
                    if t[0] == r and t[1] == a:
                        next_states.add(t[2])
            if len(next_states):
                next_states = list(next_states)
                D.transition_function.append([R, a, sorted(next_states)])
            else:
                D.transition_function.append([R, a, []])
    return D

def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    
    # N = NFA(["Q1", "Q2", "Q3"], ["a", "b"], [["Q1", "b", "Q2"], ["Q1", "$", "Q3"], ["Q2", "a", "Q2"], ["Q2", "a", "Q3"], ["Q2", "b", "Q3"], ["Q3", "a", "Q1"]], ["Q1"], ["Q1"])
    with open(inp) as f:
        N = NFA(*json.load(f).values())
    D = get_DFA_from_NFA(N)
    with open(out, 'w+') as f:
        json.dump(D.get_dict(), f, indent=4)

if __name__ == "__main__":
    main()
