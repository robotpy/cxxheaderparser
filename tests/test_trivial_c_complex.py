from cxxheaderparser.simple import NamespaceScope, ParsedData, Variable, parse_string
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_complex_spelling_1() -> None:
    content = """
        float _Complex x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="float _Complex")]
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


def test_complex_spelling_2() -> None:
    content = """
        _Complex double x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="_Complex double")]
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


def test_complex_spelling_3() -> None:
    content = """
        long double _Complex x; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="long double _Complex")]
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


def test_c_complex_raw_keyword():
    lexer = PlyLexer()
    lexer.input("_Complex")
    token = lexer.token()
    assert (token.type, token.value) == ("_Complex", "_Complex")
