import js2py

with open("../noam.js") as f:
    module = f.read()

js = module + """
var automaton = {}
automaton['acceptingStates'] = ["s0"]
automaton['alphabet'] = ["a"]
automaton['initialState'] = "s0"
automaton['states'] = ["s0"]
t = {}
t['fromState'] = "s0"
t['symbol'] = 'a'
t['toStates'] = ['s0']
automaton['transitions'] = [t]

function getRegex(automaton){
    automaton = noam.fsm.minimize(automaton);
    var r = noam.fsm.toRegex(automaton);
    r = noam.re.tree.simplify(r, {"useFsmPatterns": false});
    var s = noam.re.tree.toString(r);
    document.write(s)    
}
getRegex(automaton) 
""".replace("document.write", "return ")


result = js2py.eval_js(js)
print(result)