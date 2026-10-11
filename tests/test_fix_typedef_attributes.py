from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    AnonymousName,
    Attribute,
    AttributeStyle,
    ClassDecl,
    Field,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
    Typedef,
    Variable,
)


def test_gnu_typedef_struct_attribute() -> None:
    content = """
        typedef struct { int x; } S __attribute__((aligned)); int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[AnonymousName(id=1)], classkey="struct"
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
            ],
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(
                            segments=[AnonymousName(id=1)], classkey="struct"
                        )
                    ),
                    name="S",
                    attributes=[Attribute(style=AttributeStyle.GCC, name="aligned")],
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
