from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    Field,
    NamespaceScope,
    ParsedData,
    Variable,
    parse_string,
)
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_c_static_assert_namespace() -> None:
    content = """
        _Static_assert(1, "ok"); int x;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ]
        )
    )


def test_c_static_assert_class() -> None:
    content = """
        struct S { _Static_assert(1, "ok"); int x; };
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        )
                    ),
                    fields=[
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="x",
                        )
                    ],
                )
            ]
        )
    )


def test_c_static_assert_raw_keyword():
    lexer = PlyLexer()
    lexer.input("_Static_assert")
    token = lexer.token()
    assert (token.type, token.value) == ("_Static_assert", "_Static_assert")
