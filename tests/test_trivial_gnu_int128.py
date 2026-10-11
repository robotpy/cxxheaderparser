from cxxheaderparser.simple import NamespaceScope, ParsedData, Variable, parse_string
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_int128_spelling_1() -> None:
    content = """
        __int128 x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="__int128")]
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


def test_int128_spelling_2() -> None:
    content = """
        unsigned __int128 x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="unsigned __int128")]
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


def test_int128_spelling_3() -> None:
    content = """
        signed __int128 x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="signed __int128")]
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


def test_gnu_int128_raw_keyword():
    lexer = PlyLexer()
    lexer.input("__int128")
    token = lexer.token()
    assert (token.type, token.value) == ("__int128", "__int128")
