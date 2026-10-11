from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    Attribute,
    AttributeStyle,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
    UsingAlias,
    Variable,
)


def test_alias_attribute_variant_01() -> None:
    content = """
        using T __attribute__((deprecated)) = int; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="T",
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    attributes=[Attribute(style=AttributeStyle.GCC, name="deprecated")],
                )
            ],
        )
    )


def test_alias_attribute_variant_02() -> None:
    content = """
        using T [[deprecated]] = int; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="T",
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    attributes=[Attribute(style=AttributeStyle.CXX, name="deprecated")],
                )
            ],
        )
    )
