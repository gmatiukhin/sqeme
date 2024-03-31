from typing import Any, Dict, Self
import operator as op


class Env(Dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = None
        self.layer(outer)

    def find(self, var) -> Self:
        print("Looking for", repr(var), 'in:', repr(self))
        return self if var in self else self.outer.find(var)  # type: ignore

    def layer(self, other: Self) -> None:
        """
        Add another Env as an outer layer above this one.
        If there are more outer layers to be found, put it above them too.
        """
        if other is None: return
        if self.outer is None or isinstance(self.outer, EmptyEnv):
            old_outer = self.outer
            self.outer = other
            other.layer(old_outer)
        else:
            self.outer.layer(other)
    
    def __repr__(self) -> str:
        return f'Env({list(self)}, outer={repr(self.outer)})'

class EmptyEnv(Env):
    """
    An Env that lies at the bottom of the type system.
    It resolves prime-atoms 'FOO as strings "'FOO",
    and for any other atom it raises an error.
    """

    def __init__(self, params=(), args=(), outer=None):
        self.outer = None

    def find(self, var) -> Self:
        return self  # This env always finds things

    def __getitem__(self, key: str) -> Any:
        if key.startswith("'"):
            return str(key)
        else:
            raise ValueError(f"No such name defined: {repr(key)}")
    
    def layer(self, other: Self) -> None:
        raise TypeError("Cannot layer an env on top of the EmptyEnv.")
    
    def __repr__(self) -> str:
        return "EmptyEnv()"

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

def wrap_with_empty(which: Env) -> Env:
    return Env(outer=which)