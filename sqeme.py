import sys
import traceback
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
            bracket_count = 0
        
        if bracket_count == 0:
            text = '\n'.join(buffer)
            try:
                interpreter.set_new_code(text)
                value = interpreter.run()
                interpreter.env['_'] = value
                print('--> ', value)
            except:
                traceback.print_exc()
            buffer.clear()
            bracket_count = 0

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
