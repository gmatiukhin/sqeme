from typing import Any, Dict, Self
import operator as op
import typing

from parsing import Atom, Expression, Number


class Env(Dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = None
        self.layer(outer)

    def find(self, var: Atom) -> Self:
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

    It raises an error for any lookup.
    """

    def __init__(self, params=(), args=(), outer=None):
        self.outer = None

    def find(self, var: Atom) -> Self:
        return self  # This env always finds things

    def __getitem__(self, key: Atom) -> Expression:
            raise ValueError(f"No such name defined: {repr(key)}")
    
    def layer(self, other: Env) -> None:
        raise TypeError("Cannot layer an env on top of the EmptyEnv.")
    
    def __repr__(self) -> str:
        return "EmptyEnv()"

def default_env() -> Env:
    env = Env()
    def manyplus(this, *others):
        if len(others) == 1:
            return this + others[0]
        else:
            return this + manyplus(others[0], *others[1:])
    env.update(
        {
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "list": lambda *x: list(x),
            "+": op.add,
            "++": manyplus,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "%": op.mod,

            "print": lambda v: (print(v), v)[1]

        }
    )
    return env

def wrap_with_empty(which: Env) -> Env:
    return Env(outer=which)