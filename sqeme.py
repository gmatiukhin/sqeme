import sys
from interpreter import *

def repl():
    buffer = []
    bracket_count = 0
    interpreter = Interpeter('()')
    while True:
        new_line = input(f'{bracket_count}> ')
        bracket_count += new_line.count('(')
        bracket_count -= new_line.count(')')
        buffer.append(new_line)
        if bracket_count < 0:
            print("Syntax Error: too many closing brackets")
            buffer.clear()
        
        if bracket_count == 0:
            text = '\n'.join(buffer)
            interpreter.set_new_code(text)
            print(interpreter.run())
            buffer.clear()

if __name__ == "__main__":
    match len(sys.argv):
        case 1:
            # Start repl
            repl()
        case 2:
            # Evaluate file
            with open(sys.argv[1], "r") as src:
                interpreter = Interpeter(src.read())
                print(interpreter.tokens)
                print(interpreter.ast)
                print(interpreter.env)
                print(interpreter.run())
        case _:
            # Error out
            ...
