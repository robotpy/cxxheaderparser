import typing

from .lexer import LexToken, Lexer
from .types import Token

# key: token type, value: (left spacing, right spacing)
_want_spacing = {
    "NUMBER": (2, 2),
    "FLOAT_NUMBER": (2, 2),
    "NAME": (2, 2),
    "CHAR_LITERAL": (2, 2),
    "STRING_LITERAL": (2, 2),
    "ELLIPSIS": (2, 2),
    ">": (0, 2),
    ")": (0, 1),
    "(": (1, 0),
    ",": (0, 3),
    "*": (1, 2),
    "&": (0, 2),
}

_want_spacing.update(dict.fromkeys(Lexer.keywords, (2, 2)))


def tokfmt(toks: typing.List[Token]) -> str:
    """
    Helper function that takes a list of tokens and converts them to a string
    """
    last = 0
    vals = []
    default = (0, 0)
    ws = _want_spacing

    for tok in toks:
        value = tok.value
        # special case
        if value == "operator":
            l, r = 2, 0
        else:
            l, r = ws.get(tok.type, default)
        if l + last >= 3:
            vals.append(" ")

        last = r
        vals.append(value)

    return "".join(vals)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("header")
    args = parser.parse_args()

    lexer = Lexer(args.header)
    with open(lexer.filename) as fp:
        lexer.input(fp.read())  # type: ignore

    toks: typing.List[Token] = []
    while True:
        tok = lexer.token_eof_ok()
        if not tok:
            break
        if tok.type == ";":
            print(toks)
            print(tokfmt(toks))
            toks = []
        else:
            toks.append(Token(tok.value, tok.type))

    print(toks)
    print(tokfmt(toks))
