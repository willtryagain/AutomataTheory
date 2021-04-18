import json
import sys
import os
from os import popen

class Automata:
    def __init__(self, language=set(['0', '1'])):
        self.states = set()     
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language

    @staticmethod
    def epsilon():
        return ":e:"

    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        # why mot addimg tje fial state
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)
    
    def display(self):
        print(self.states)
        print(self.startstate)
        print(self.finalstates)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print(" ", fromstate, "->", state, "on '"+char+"'", end=",")
            print()

    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}

    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        """
        if 
        """
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                # whu are we addomg index to action?
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startstate
            for state in self.states:
                if state in self.finalstates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile 

class BuildAutomata:

    @staticmethod
    def basicstruct(inp):
        state1 = 1 
        state2 = 2
        basic = Automata()
        basic.setstartstate(state1)
        basic.addfinalstates(state2)
        basic.addtransition(state1, state2, inp)
        return basic

    @staticmethod
    def plusstruct(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    @staticmethod
    def dotstruct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2 - 1
        dot = Automata()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, Automata.epsilon()) 
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    @staticmethod
    def starstruct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, Automata.epsilon())
        star.addtransition(star.startstate, star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], a.startstate, Automata.epsilon())
        star.addtransition_dict(a.transitions)
        return star

        
class NFAfromRegex: 

    def __init__(self, regex):
        self.star = "*"
        self.plus = "+"
        self.dot = "."
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65, 91)]
        self.alphabet.extend([chr(i) for i in range(48, 58)])
        self.alphabet.extend([chr(i) for i in range(97, 123)])
        self.buildNFA()

    def getNFA(self):
        return self.nfa

    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise IndexError
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise IndexError
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b, a))
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b, a))
            
    def addOperatorToStack(self, char):
        while True:
            if len(self.stack) == 0:
                break
            top = self.stack[-1]
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildAutomata.basicstruct(char))
            elif char == self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket, self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char == self.closingBracket:
                if previous in self.operators:
                    raise Exception("%s %s" % (char, previous))
                while True:
                    if len(self.stack) == 0:
                        raise Exception
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            elif char ==  self.star:
                if previous in self.operators or previous == self.openingBracket or previous == self.star:
                    raise Exception
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous == self.openingBracket:
                    raise Exception
                else:
                    self.addOperatorToStack(char)
            else:
                raise Exception("alpha")
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            raise Exception
        self.nfa = self.automata.pop()
        self.nfa.language = language


    def displayNFA(self):
        self.nfa.display()

def drawGraph(automata, file = ""):
    """From https://github.com/max99x/automata-editor/blob/master/util.py"""
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()

def get_state(s):
    return ["Q" + str(s)]

def transform(nfa):
    states = []
    for s in nfa.states:
        states.append(get_state(s))
    letters = []
    for s in nfa.language:
        letters.append(s)
    transition_function = []
    for fromstate, tostates in nfa.transitions.items():
        for state in tostates:
            for char in tostates[state]:
                if char == Automata.epsilon():
                    char = "$"
                transition_function.append([get_state(fromstate), char, get_state(state)])
    start_states = [get_state(nfa.startstate)]
    final_states = []
    for s in nfa.finalstates:
        final_states.append(get_state(s))
    d = {}
    d["states"] = states
    d["letters"] = letters
    d["start_states"] = start_states
    d["final_states"] = final_states
    d["transition_function"] = transition_function
    return d


def main():
    assert len(sys.argv) == 3, "invalid args"
    inp = sys.argv[1]
    out = sys.argv[2]

    if not os.path.exists(inp):
        raise AssertionError("arg1 file not found")
    with open(inp) as f:
        obj = json.load(f)
        regex = obj["regex"]

    nfaObj = NFAfromRegex(regex)
    # nfaObj.displayNFA()
    nfa = nfaObj.getNFA()
    d = transform(nfa)
    with open(out, 'w+') as f:
        json.dump(d, f, indent=4)
    # drawGraph(nfa, "nfa")

if __name__ == "__main__":
    main()