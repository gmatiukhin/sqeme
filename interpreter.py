from parsing import *
from env import *


class Interpeter:
    def __init__(self, src) -> None:
        self.src = src
        self.tokens = tokenize(self.src)
        self.ast = read_tokens(self.tokens[:])
        self.env = default_env()

    def run(self) -> Expression:
        return eval(self.ast, self.env)


class Procedure:
    def __init__(self, params, body, env) -> None:
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args) -> Expression:
        print("Procedure:")
        print("\tParams:", self.params)
        print("\tBody:", self.body)
        print("\tEnv:", self.env)
        return eval(self.body, Env(self.params, args, self.env))


def eval(exp: Expression, env: Env) -> Expression:  # type: ignore
    print("Evaluating:", exp)
    if isinstance(exp, Symbol):
        return env.find(exp)[exp]
    elif isinstance(exp, Number):
        return exp
    elif isinstance(exp, List) and len(exp) == 0:
        return exp
    op, *args = exp
    if op == "define":
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
        print("Updated env:", env)
    elif op == "lambda":
        (params, body) = args
        return Procedure(params, body, env)  # type: ignore
    else:
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)  # type: ignore
