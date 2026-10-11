from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    BaseClass,
    ClassDecl,
    FundamentalSpecifier,
    Method,
    NameSpecifier,
    PQName,
    TemplateDecl,
    TemplateTypeParam,
    Type,
    UsingDecl,
)


def test_using_pack_expansion() -> None:
    content = """
        template<class... T> struct S : T... { using T::f...; };
        struct B { void f(); };
        struct D : B { using B::f; };
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
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(segments=[NameSpecifier(name="T")]),
                                param_pack=True,
                            )
                        ],
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(
                                    typekey="class", name="T", param_pack=True
                                )
                            ]
                        ),
                    ),
                    using=[
                        UsingDecl(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="T"),
                                    NameSpecifier(name="f"),
                                ]
                            ),
                            access="public",
                            param_pack=True,
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="B")], classkey="struct"
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
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="D")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(segments=[NameSpecifier(name="B")]),
                            )
                        ],
                    ),
                    using=[
                        UsingDecl(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="B"),
                                    NameSpecifier(name="f"),
                                ]
                            ),
                            access="public",
                        )
                    ],
                ),
            ]
        )
    )
