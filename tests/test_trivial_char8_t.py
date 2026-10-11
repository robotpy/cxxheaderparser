from cxxheaderparser.simple import (
    Function,
    NamespaceScope,
    ParsedData,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Parameter,
    Type,
)


def test_char8_t_is_fundamental() -> None:
    content = """
        char8_t x; char8_t f(char8_t);
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="char8_t")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="f")]),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="char8_t")]
                                )
                            )
                        )
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="char8_t")])
                    ),
                )
            ],
        )
    )
