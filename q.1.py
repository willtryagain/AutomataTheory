import json
import sys

# assume 1 length alphabet

def has_less_or_equal_priority(a, b):
    if a == ''

def infix_to_postfix(infix):
    stack = []
    postfix = ''
    # insert o to denote concat
    for c in infix:
        if isalnum(c):
            postfix += c
        else:
            if c == '(':
                stack.append(c)
            elif c == ')':
                operator = stack.pop()
                while not (operator == '('):
                    postfix += operator
                    operator = stack.pop()
            else:
                while (not len(stack) == 0) and 


def main():
    assert len(sys.argv) ==  3, "invalid args" 
    with open(sys.argv[1]) as f:
        inp =  json.load(f)
    assert "regex" in inp, "regex not in input"
    infix = inp["regex"]


if __name__ == "__main__":
    main()
 