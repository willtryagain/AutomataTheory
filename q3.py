import json
import sys
import os
from itertools import chain, combinations
# assuming no name conflict Q_.

index = 1
def get_name(): 
    global index
    name = "Q_" + str(index)
    index += 1
    return name

class NFA:
    def __init__(self, states=[], letters=[], transition_matrix=[], start_states=[], final_states=[]):
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


def find(state, D):
    

def get_GNFA(D):
    new_start = get_name()
    new_accept = get_name()
    D.states.append(new_start, new_accept)
    # assuming single start state
    D.transition_matrix.append([new_start, "$", D.start_states[0]])
    D.start_states = [new_start]
    for f in D.final_states:
        new_trans.append([f, "$", new_accept])

    D.transition_matrix.extend(new_trans)
    D.final_states = [new_accept]
    # single union edges
    d = {}
    for t in D.transition_matrix:
        s = t[0]
        f = t[2]
        if (s, f) not in d:
            d[(s, f)] = []
        d[(s, f)].append(t[1])

    new_trans = []
    for k in d.keys():
        new_trans(k[0], ''.join(str(x) for x in d[k]),k[1])

    for state in D.states:
        if state != new_start and state != new_accept:
            qi, qj = find(state, D)