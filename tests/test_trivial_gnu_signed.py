from cxxheaderparser.simple import NamespaceScope, ParsedData, Variable, parse_string
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_gnu_signed_spelling_1() -> None:
    content = """
        __signed__ x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="__signed__")]
                        )
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ]
        )
    )


def test_gnu_signed_spelling_2() -> None:
    content = """
        __signed__ char x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="__signed__ char")]
                        )
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ]
        )
    )


def test_gnu_signed_spelling_3() -> None:
    content = """
        long __signed__ int x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="long __signed__ int")]
                        )
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ]
        )
    )


def test_gnu_signed_raw_keyword():
    lexer = PlyLexer()
    lexer.input("__signed__")
    token = lexer.token()
    assert (token.type, token.value) == ("__signed__", "__signed__")
