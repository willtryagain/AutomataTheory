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
    


def get_DFA_from_NFA(N):
    states = [s for s in powerset(N.states)]
    letters = N.letters
    start_states = N.start_states
    
    final_states = []
    for R in states:
        for s in N.final_states:
            if s in R:
                final_states.append(R)
                break

    transition_matrix = []
    for R in states:
        for a in letters:
            next_states = []
            for r in R:
                for t in N.transition_matrix:
                    if t[0] == r and t[1] == a:
                        next_states.append(t[2])
            if len(next_states):
                transition_matrix.append([R, a, sorted(next_states)])
    return NFA(states, letters, transition_matrix, start_states, final_states)

def main():
    N = NFA(["Q1", "Q2", "Q3"], ["a", "b"], [["Q1", "b", "Q2"], ["Q2", "a", "Q2"], ["Q2", "a", "Q3"], ["Q2", "b", "Q3"], ["Q3", "a", "Q1"]], ["Q1"], ["Q1"])
    print(get_DFA_from_NFA(N).get_dict()["transition_matrix"])

if __name__ == "__main__":
    main()
