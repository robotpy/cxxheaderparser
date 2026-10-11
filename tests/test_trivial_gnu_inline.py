from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    Function,
    Method,
    NamespaceScope,
    ParsedData,
    Variable,
    parse_string,
)
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
from cxxheaderparser.tokfmt import PlyLexer


def test_gnu_inline_definition() -> None:
    content = """
        __inline__ void f() {}
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="f")]),
                    parameters=[],
                    inline=True,
                    has_body=True,
                )
            ]
        )
    )


def test_gnu_inline_static() -> None:
    content = """
        static __inline__ int f();
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="f")]),
                    parameters=[],
                    static=True,
                    inline=True,
                )
            ]
        )
    )


def test_gnu_inline_method() -> None:
    content = """
        struct S { __inline__ void f(); };
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
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="f")]),
                            parameters=[],
                            inline=True,
                            access="public",
                        )
                    ],
                )
            ]
        )
    )


def test_gnu_inline_namespace() -> None:
    content = """
        __inline__ namespace N { int x; }
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "N": NamespaceScope(
                    name="N",
                    inline=True,
                    variables=[
                        Variable(
                            name=PQName(segments=[NameSpecifier(name="x")]),
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                        )
                    ],
                )
            }
        )
    )


def test_gnu_inline_raw_keyword():
    lexer = PlyLexer()
    lexer.input("__inline__")
    token = lexer.token()
    assert (token.type, token.value) == ("__inline__", "__inline__")
