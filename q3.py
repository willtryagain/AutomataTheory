import json
import sys          
import os
import js2py

# single start state
# alphabet and  are str

class NFA:
    def __init__(self, states=[], letters=[], transition_function=[], start_states=[], final_states=[]):
        self.states = states
        self.letters = letters
        self.transition_function = transition_function
        self.start_states = start_states
        self.final_states = final_states


    def get_str(self):
        s = "var automaton = {}\n"
        s += "automaton['initialState'] = '" + str(self.start_states[0]) + "'\n"
        s += "automaton['acceptingStates'] = [" 
        for f in self.final_states:
            s +=  "'%s'," % f           
        s += "]\n"
        s += "automaton['alphabet'] = ["
        for l in self.letters:
            s += "'%s'," % l
        s += "]\n"
        s += "automaton['states'] = ["
        for state in self.states:
            s +="'%s'," % state
        s += "] \n"
        s += "automaton['transitions'] = ["
        for t in self.transition_function:
            s += "{'fromState': '%s', 'symbol': '%s', 'toStates': ['%s']},\n" % (t[0], t[1], t[2])
        s += "]\n"
        return s

    def getRegex(self):
        automata = self.get_str()
        with open("../noam.js") as f:
            module = f.read()
        function_call = """
        function getRegex(automaton){
            automaton = noam.fsm.minimize(automaton);
            var r = noam.fsm.toRegex(automaton);
            r = noam.re.tree.simplify(r, {"useFsmPatterns": false});
            var s = noam.re.tree.toString(r);
            document.write(s)    
        }
        getRegex(automaton) 
        """.replace("document.write", "return ")
        
        js = module + automata + function_call
        print(automata + function_call)
        result = js2py.eval_js(js)
        return result

def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    
    # N = NFA(["Q1", "Q2", "Q3"], ["a", "b"], [["Q1", "b", "Q2"], ["Q1", "$", "Q3"], ["Q2", "a", "Q2"], ["Q2", "a", "Q3"], ["Q2", "b", "Q3"], ["Q3", "a", "Q1"]], ["Q1"], ["Q1"])
    with open(inp) as f:
        N = NFA(*json.load(f).values())
    print(N.getRegex())
    # with open(out, 'w+') as f:
    #     json.dump(D.get_dict(), f, indent=4)

if __name__ == "__main__":
    main()






