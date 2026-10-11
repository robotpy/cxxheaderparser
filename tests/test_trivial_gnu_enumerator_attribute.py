from cxxheaderparser.simple import (
    EnumDecl,
    NamespaceScope,
    ParsedData,
    Value,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    Attribute,
    AttributeStyle,
    Enumerator,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Token,
    Type,
)


def test_gnu_enumerator_attributes_implicit() -> None:
    content = """
        enum E { a __attribute__((deprecated)) __attribute__((unused)), b }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            enums=[
                EnumDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="E")], classkey="enum"
                    ),
                    values=[
                        Enumerator(
                            name="a",
                            attributes=[
                                Attribute(style=AttributeStyle.GCC, name="deprecated"),
                                Attribute(style=AttributeStyle.GCC, name="unused"),
                            ],
                        ),
                        Enumerator(name="b"),
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
        )
    )


def test_gnu_enumerator_attributes_explicit() -> None:
    content = """
        enum E { a __attribute__((deprecated)) __attribute__((unused)) = 3, b }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            enums=[
                EnumDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="E")], classkey="enum"
                    ),
                    values=[
                        Enumerator(
                            name="a",
                            value=Value(tokens=[Token(value="3")]),
                            attributes=[
                                Attribute(style=AttributeStyle.GCC, name="deprecated"),
                                Attribute(style=AttributeStyle.GCC, name="unused"),
                            ],
                        ),
                        Enumerator(name="b"),
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
        )
    )
