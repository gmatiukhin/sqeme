from typing import Dict, Self
import operator as op


class Env(Dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var) -> Self:
        print("Looking for: ", var)
        return self if var in self else self.outer.find(var)  # type: ignore


def default_env() -> Env:
    env = Env()
    env.update(
        {
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "list": lambda *x: list(x),
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "%": op.mod,
        }
    )
    return env
