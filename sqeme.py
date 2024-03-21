import sys
from interpreter import *

if __name__ == "__main__":
    match len(sys.argv):
        case 1:
            # Start repl
            ...
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
