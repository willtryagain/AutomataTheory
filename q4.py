import json
import sys
import os
from os import popen

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

    def remove_unreachable_states(self):
        reachable_states = {self.start_states[0]}
        new_states = {self.start_states[0]}

        while True:
            temp = set()
            for q in new_states:
                for c in self.letters:
                    pset = set()
                    for t in self.transition_function:
                        if t[0] == q and t[1] == c:
                            pset.add(t[2])
                    temp = temp.union(pset)
            new_states = temp.difference(reachable_states)
            reachable_states = reachable_states.union(new_states)
            if new_states == set():
                break
        self.states = list(reachable_states)
        print(self.states)

def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    
    with open(inp) as f:
        N = NFA(*json.load(f).values())
    N.states.append("aman")
    N.remove_unreachable_states()


if __name__ == "__main__":
    main()
