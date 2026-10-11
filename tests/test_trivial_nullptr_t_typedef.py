from cxxheaderparser.simple import (
    NamespaceScope,
    ParsedData,
    Typedef,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    DecltypeSpecifier,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Token,
    Type,
)


def test_nullptr_t_typedef_name() -> None:
    content = """
        typedef decltype(nullptr) nullptr_t; nullptr_t x;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(
                            segments=[
                                DecltypeSpecifier(tokens=[Token(value="nullptr")])
                            ]
                        )
                    ),
                    name="nullptr_t",
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(
                            segments=[FundamentalSpecifier(name="nullptr_t")]
                        )
                    ),
                )
            ],
        )
    )
