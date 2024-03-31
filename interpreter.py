from parsing import *
from env import *


class Interpeter:
    def __init__(self, src, env=None) -> None:
        e = env if env is not None else default_env()
        self.env = wrap_with_empty(e)
        self.set_new_code(src)
    
    def set_new_code(self, src) -> None:
        self.src = src
        self.tokens = tokenize(self.src)
        print(self.tokens)
        self.ast = read_tokens(self.tokens[:])

    def run(self) -> Expression:
        return eval(self.ast, self.env)


class Procedure:
    def __init__(self, params, body, env) -> None:
        print(f"Prepared procedure with {params=} {body=} {env=}")
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args) -> Expression:
        print("Calling procedure:")
        print("\tParams:", self.params)
        print("\tBody:", self.body)
        env = wrap_with_empty(self.env)
        for param, arg in zip(self.params, args):
            env[param] = arg
        print("\tResulting env for expression:", env)
        return eval(self.body, env)


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
