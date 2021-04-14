import json
import sys
from itertools import chain, combinations
# ASSuminmg no e transitionss

class NFA:
    def __init__(self, states, letters, transition_matrix, start_states, final_states):
        self.states = states
        self.letters = letters
        self.transition_matrix = transition_matrix
        self.start_states = start_states
        self.final_states = final_states


    def get_dict(self):
        N = {}
        N["states"] = self.states
        N["letters"] = self.letters
        N["transition_matrix"] = self.transition_matrix
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
    for t in N.transition_matrix:
        if t[0] == s and t[1] == 'e':
            next_states.append(t[2])
    return next_states

def get_DFA_from_NFA(N):
    states = [s for s in powerset(N.states)]
    letters = N.letters
    start_states = []
    for s in N.start_states:
        start_states.extend(E(s, N))
    
    final_states = []
    for R in states:
        for s in N.final_states:
            if s in R:
                final_states.append(R)
                break

    transition_matrix = []
    for R in states:
        for a in letters:
            next_states = set()
            for r in R:
                for t in N.transition_matrix:
                    if t[0] == r and t[1] == a:
                        for s in E(t[2], N):
                            next_states.add(s)
            if len(next_states):
                next_states = list(next_states)
                transition_matrix.append([R, a, sorted(next_states)])
    return NFA(list(states), letters, transition_matrix, start_states, final_states)

def main():
    N = NFA(["Q1", "Q2", "Q3"], ["a", "b"], [["Q1", "b", "Q2"], ["Q1", "e", "Q3"], ["Q2", "a", "Q2"], ["Q2", "a", "Q3"], ["Q2", "b", "Q3"], ["Q3", "a", "Q1"]], ["Q1"], ["Q1"])
    print(get_DFA_from_NFA(N).get_dict()["transition_matrix"])

if __name__ == "__main__":
    main()
