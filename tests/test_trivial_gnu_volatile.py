from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    Method,
    NamespaceScope,
    ParsedData,
    Typedef,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    FunctionType,
    FundamentalSpecifier,
    MemberPointer,
    NameSpecifier,
    PQName,
    Pointer,
    Type,
)
from cxxheaderparser.tokfmt import PlyLexer


def test_gnu_volatile_prefix() -> None:
    content = """
        __volatile__ int x;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                        volatile=True,
                    ),
                )
            ]
        )
    )


def test_gnu_volatile_suffix() -> None:
    content = """
        int __volatile__ x;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                        volatile=True,
                    ),
                )
            ]
        )
    )


def test_gnu_volatile_pointer() -> None:
    content = """
        int * __volatile__ p;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="p")]),
                    type=Pointer(
                        ptr_to=Type(
                            typename=PQName(segments=[FundamentalSpecifier(name="int")])
                        ),
                        volatile=True,
                    ),
                )
            ]
        )
    )


def test_gnu_volatile_method() -> None:
    content = """
        struct S { void f() __volatile__; };
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
                            access="public",
                            volatile=True,
                        )
                    ],
                )
            ]
        )
    )


def test_gnu_volatile_function_typedef() -> None:
    content = """
        typedef void F() __volatile__;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            typedefs=[
                Typedef(
                    type=FunctionType(
                        return_type=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="void")]
                            )
                        ),
                        parameters=[],
                        volatile=True,
                    ),
                    name="F",
                )
            ]
        )
    )


def test_gnu_volatile_member_pointer_typedef() -> None:
    content = """
        typedef void (S::*F)() __volatile__;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            typedefs=[
                Typedef(
                    type=MemberPointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            parameters=[],
                            volatile=True,
                        ),
                        classname=PQName(segments=[NameSpecifier(name="S")]),
                    ),
                    name="F",
                )
            ]
        )
    )


def test_gnu_volatile_raw_keyword():
    lexer = PlyLexer()
    lexer.input("__volatile__")
    token = lexer.token()
    assert (token.type, token.value) == ("__volatile__", "__volatile__")
