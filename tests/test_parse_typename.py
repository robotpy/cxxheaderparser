import re

import pytest

from cxxheaderparser.errors import CxxParseError
from cxxheaderparser.simple import parse_typename
from cxxheaderparser.types import (
    Array,
    FundamentalSpecifier,
    FunctionType,
    NameSpecifier,
    Parameter,
    Pointer,
    PQName,
    Reference,
    TemplateArgument,
    TemplateSpecialization,
    Token,
    Type,
    Value,
)


def test_parse_typename_basic() -> None:
    content = """
        const int
    """

    dtype = parse_typename(content.strip())

    assert dtype == Type(
        typename=PQName(segments=[FundamentalSpecifier(name="int")]), const=True
    )


def test_parse_typename_template_ref() -> None:
    content = """
        const std::vector<int>&
    """

    dtype = parse_typename(content.strip())

    assert dtype == Reference(
        ref_to=Type(
            typename=PQName(
                segments=[
                    NameSpecifier(name="std"),
                    NameSpecifier(
                        name="vector",
                        specialization=TemplateSpecialization(
                            args=[
                                TemplateArgument(
                                    arg=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    )
                                )
                            ]
                        ),
                    ),
                ]
            ),
            const=True,
        )
    )


def test_parse_typename_function_pointer() -> None:
    content = """
        int (*)(int)
    """

    dtype = parse_typename(content.strip())

    assert dtype == Pointer(
        ptr_to=FunctionType(
            return_type=Type(
                typename=PQName(segments=[FundamentalSpecifier(name="int")])
            ),
            parameters=[
                Parameter(
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    )
                )
            ],
        )
    )


def test_parse_typename_array() -> None:
    content = """
        int[3]
    """

    dtype = parse_typename(content.strip())

    assert dtype == Array(
        array_of=Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
        size=Value(tokens=[Token(value="3")]),
    )


def test_parse_typename_rejects_modifiers() -> None:
    content = """
        static int
    """

    err = "parsing type name: unexpected 'static'"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_typename(content.strip())
