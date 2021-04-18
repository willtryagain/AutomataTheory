import json
import sys
import os
from itertools import chain, combinations
# ASSuminmg no e transitionss
# assume collectons have single elements
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

def delta(q, a, D):
    next_states = []
    for t in D.transition_matrix:
        if t[0] == [q] and t[1] == a:
            next_states.append(t[2])
    assert len(next_states) <= 1, "not dfa"
    return next_states

def remove_unreachable_states(D):
    reachable_states = set(D.start_states)
    new_states = set(D.start_states)
    # print(D.transition_matrix)
    while True:
        temp = set()
        for q in new_states:
            for c in D.letters:
                next_state = delta(q, c, D)
                print(q, c, next_state)
                if len(next_state) == 1:
                   temp.add(tuple(next_state[0]))
        new_states = temp.difference(reachable_states)
        reachable_states.union(new_states)

        if len(new_states) == 0:
            break

    D.states = reachable_states
    return D 

    def get_min_dfa(D):
    D = remove_unreachable_states(D)
    print(D.states)
    G = []
    for a in D.final_states:
        for s in D.states:
            if s not in D.final_states:
                G.append((a, s))
    while True:
        added = False
        for q in D.states:
            for r in D.states:
                if r == q:
                    continue
                for a in D.letters:
                    u = delta(q, a, D)
                    v = delta(r, a, D)
                    if len(u) == 1 and len(v) == 1:
                        if (u[0], v[0]) in G:
                            added = True
                            G.append((q, r))

        if not added:
            break
    q_collect = {}
    for q in D.states:
        collection = []
        for r in D.states:
            if (q, r) not in G:
                collection.append(r)
        q_collect[tuple(q)] = collection

    M = NFA()
    Q = []
    for q in D.states:
        qc = q_collect[tuple(q)]
        if len(qc):
            Q.append(qc)       
    M.states = list(Q)  
    print(M.states)
    # M.letters = D.letters   
    # for q in D.states:
    #     for a in D.letters:
    #         qc = q_collect[tuple(q)]
    #         if len(qc):
    #             next_state = delta(q, a, D)
    #             if len(next_state) == 1:
    #                 M.transition_matrix.append([qc, a, next_state])
def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    with open(inp) as f:
        D = NFA(*json.load(f).values())
    get_min_dfa(D)

if __name__ == "__main__":
    main()