import json
import sys


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

def get_power_set(states):
    return []

def get_final_states(N):
    return []
    
def get_transitions(N):
    return []

def get_DFA_from_NFA(N):
    states = get_power_set(N.states)
    letters = N.letters
    transition_matrix = get_transitions(N.transition_matrix)
    start_states = N.start_states
    final_states = get_final_states(N)
    return NFA(states, letters, transition_matrix, start_states, final_states)

def main():
    N = NFA(["Q0"], ["a"], [[]], ["Q0"], ["Q0"])
    print(get_DFA_from_NFA(N).get_dict())

if __name__ == "__main__":
    main()
