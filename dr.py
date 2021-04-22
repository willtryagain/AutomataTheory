from pythomata import SimpleDFA
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


def get_transitions(D):
    transition_function = {}
    for t in D.transition_function:
        if t[0] not in transition_function:
            transition_function[t[0]] = {}
        transition_function[t[0]][t[1]] = t[2]
    return transition_function

def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    
    # N = NFA(["Q1", "Q2", "Q3"], ["a", "b"], [["Q1", "b", "Q2"], ["Q1", "$", "Q3"], ["Q2", "a", "Q2"], ["Q2", "a", "Q3"], ["Q2", "b", "Q3"], ["Q3", "a", "Q1"]], ["Q1"], ["Q1"])
    with open(inp) as f:
        D = NFA(*json.load(f).values())
    states = set(D.states)
    alphabet = set(D.letters)
    initial_state = D.start_states[0]
    accepting_states = set(D.final_states)
    transition_function  = get_transitions(D)

    dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)
    min_dfa = dfa.minimize()

    MD = NF
    print(min_dfa.states)
    # with open(out, 'w+') as f:
    #     json.dump(D.get_dict(), f, indent=4)

if __name__ == "__main__":
    main()
