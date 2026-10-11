from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    ClassDecl,
    Function,
    FundamentalSpecifier,
    Method,
    NameSpecifier,
    PQName,
    Type,
)


def test_consteval_functions_and_methods() -> None:
    content = """
        consteval int f();
        constexpr int g();
        int ordinary();
        struct S {
            consteval int f() const { return 1; }
            static consteval int g() { return 2; }
            int ordinary();
        };
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
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="f")]),
                            parameters=[],
                            has_body=True,
                            consteval=True,
                            access="public",
                            const=True,
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="g")]),
                            parameters=[],
                            static=True,
                            has_body=True,
                            consteval=True,
                            access="public",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="ordinary")]),
                            parameters=[],
                            access="public",
                        ),
                    ],
                )
            ],
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="f")]),
                    parameters=[],
                    consteval=True,
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="g")]),
                    parameters=[],
                    constexpr=True,
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="ordinary")]),
                    parameters=[],
                ),
            ],
        )
    )
