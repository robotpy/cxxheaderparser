from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    Attribute,
    AttributeStyle,
    Function,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
    Value,
    Variable,
)


def test_noexcept_attribute_before_trailing_return() -> None:
    content = """
        auto f() noexcept [[vendor::tag]] -> int; int after;
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
                    attributes=[
                        Attribute(style=AttributeStyle.CXX, name="vendor::tag")
                    ],
                    has_trailing_return=True,
                    noexcept=Value(tokens=[]),
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
