from cxxheaderparser.simple import (
    Function,
    NamespaceScope,
    ParsedData,
    Typedef,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    FunctionType,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
)
import re
import pytest
from cxxheaderparser.errors import CxxParseError


def test_inherited_linkage_function_typedef() -> None:
    content = """
        extern "C" { typedef void F(); void f(); extern int x; } int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="f")]),
                    parameters=[],
                    extern='"C"',
                )
            ],
            typedefs=[
                Typedef(
                    type=FunctionType(
                        return_type=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="void")]
                            )
                        ),
                        parameters=[],
                    ),
                    name="F",
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    extern='"C"',
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ],
        )
    )


def test_explicit_extern_function_typedef_rejected() -> None:
    content = """
        typedef extern void F();
    """

    err = "<str>:1: parse error evaluating 'typedef': parsing typedef: unexpected 'extern'"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_string(content, cleandoc=True)
