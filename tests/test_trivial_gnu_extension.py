from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    Field,
    NamespaceScope,
    ParsedData,
    Typedef,
    Variable,
    parse_string,
)
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_gnu_extension_preserves_doxygen_typedef() -> None:
    content = """
        /// Documentation
        __extension__ typedef int T;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name="T",
                )
            ]
        )
    )


def test_gnu_extension_preserves_doxygen_variable() -> None:
    content = """
        /// Documentation
        __extension__ int x;
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
                    doxygen="/// Documentation",
                )
            ]
        )
    )


def test_gnu_extension_preserves_doxygen_class() -> None:
    content = """
        /// Documentation
        __extension__ struct S { int x; };
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        ),
                        doxygen="/// Documentation",
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


def test_gnu_extension_raw_keyword():
    lexer = PlyLexer()
    lexer.input("__extension__")
    token = lexer.token()
    assert (token.type, token.value) == ("__extension__", "__extension__")
