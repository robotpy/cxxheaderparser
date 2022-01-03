# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Token,
    Type,
    Value,
    Variable,
)
from cxxheaderparser.simple import (
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_dups_in_different_ns() -> None:
    content = """
      
      namespace {
      int x = 4;
      }
      
      int x = 5;
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="5")]),
                )
            ],
            namespaces={
                "": NamespaceScope(
                    variables=[
                        Variable(
                            name=PQName(segments=[NameSpecifier(name="x")]),
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            value=Value(tokens=[Token(value="4")]),
                        )
                    ]
                )
            },
        )
    )


def test_correct_ns() -> None:
    content = """
      namespace a::b::c {
        int i1;
      }

      namespace a {
        namespace b {
          namespace c {
            int i2;
          }
        }
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "a": NamespaceScope(
                    name="a",
                    namespaces={
                        "b": NamespaceScope(
                            name="b",
                            namespaces={
                                "c": NamespaceScope(
                                    name="c",
                                    variables=[
                                        Variable(
                                            name=PQName(
                                                segments=[NameSpecifier(name="i1")]
                                            ),
                                            type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(name="int")
                                                    ]
                                                )
                                            ),
                                        ),
                                        Variable(
                                            name=PQName(
                                                segments=[NameSpecifier(name="i2")]
                                            ),
                                            type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(name="int")
                                                    ]
                                                )
                                            ),
                                        ),
                                    ],
                                )
                            },
                        )
                    },
                )
            }
        )
    )
