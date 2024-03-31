import typing

Symbol = str

Number = int | float

Atom = Symbol | Number

List = typing.List

Expression = Atom | List


DELIMITERS = ["(", ")"]


def tokenize(src: str) -> typing.List[str]:
    # for symbol in DELIMITERS:
    #     src = src.replace(symbol, f" {symbol} ")
    # return src.split()
    import shlex
    lexer = shlex.shlex(src, punctuation_chars='+-*/')
    tokens = []
    next_token = lexer.get_token()
    while next_token != '':
        tokens.append(next_token)
        next_token = lexer.get_token()
    
    return tokens


def read_tokens(tokens: typing.List[str]) -> Expression:
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        l = []
        while tokens[0] != ")":
            l.append(read_tokens(tokens))
        tokens.pop(0)  # remove the last ')'
        return l
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
