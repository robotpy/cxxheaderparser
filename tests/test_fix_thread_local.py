from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    ClassDecl,
    Field,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
    Variable,
)


def test_thread_storage_variant_01() -> None:
    content = """
        thread_local int x;
        static thread_local int local;
        extern thread_local int shared;
        thread_local static int reversed;
        int ordinary;
        struct S { static thread_local int member; static int ordinary; };
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
                            name="member",
                            static=True,
                            thread_local=True,
                        ),
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="ordinary",
                            static=True,
                        ),
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="local")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    static=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="shared")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    extern=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="reversed")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    static=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="ordinary")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ],
        )
    )


def test_thread_storage_variant_02() -> None:
    content = """
        __thread int x;
        static __thread int local;
        extern __thread int shared;
        __thread static int reversed;
        int ordinary;
        struct S { static __thread int member; static int ordinary; };
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
                            name="member",
                            static=True,
                            thread_local=True,
                        ),
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="ordinary",
                            static=True,
                        ),
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="local")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    static=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="shared")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    extern=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="reversed")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    static=True,
                    thread_local=True,
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="ordinary")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ],
        )
    )
