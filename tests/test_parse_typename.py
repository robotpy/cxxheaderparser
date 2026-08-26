import re

import pytest

from cxxheaderparser.errors import CxxParseError
from cxxheaderparser.simple import parse_string, parse_typename
from cxxheaderparser.types import (
    Array,
    FundamentalSpecifier,
    FunctionType,
    MemberPointer,
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


def test_parse_typename_qualified_function() -> None:
    dtype = parse_typename("int(double) volatile &&")

    assert dtype == FunctionType(
        return_type=Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
        parameters=[
            Parameter(
                type=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="double")])
                )
            )
        ],
        volatile=True,
        ref_qualifier="&&",
    )


def test_parse_typename_function_with_bare_member_pointer_parameter() -> None:
    dtype = parse_typename("int(int C::*)")

    assert dtype == FunctionType(
        return_type=Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
        parameters=[
            Parameter(
                type=MemberPointer(
                    ptr_to=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    classname=PQName(segments=[NameSpecifier(name="C")]),
                )
            )
        ],
    )


def test_parse_typename_qualified_function_with_member_pointer_parameter() -> None:
    dtype = parse_typename("int(void (C::*)(double)) const")

    assert dtype == FunctionType(
        return_type=Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
        parameters=[
            Parameter(
                type=MemberPointer(
                    ptr_to=FunctionType(
                        return_type=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="void")]
                            )
                        ),
                        parameters=[
                            Parameter(
                                type=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="double")]
                                    )
                                )
                            )
                        ],
                    ),
                    classname=PQName(segments=[NameSpecifier(name="C")]),
                )
            )
        ],
        const=True,
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


def test_parse_typename_trailing_return_function_pointer() -> None:
    content = """
        auto (*)() -> int
    """

    dtype = parse_typename(content.strip())

    assert dtype == Pointer(
        ptr_to=FunctionType(
            return_type=Type(
                typename=PQName(segments=[FundamentalSpecifier(name="int")])
            ),
            parameters=[],
            has_trailing_return=True,
        )
    )
    assert dtype.format() == "auto (*)() -> int"


def test_member_pointer_owner_template_argument_classification() -> None:
    dtype = parse_typename("int Owner<int(T)>::*")
    parameter_type = (
        parse_string("void f(int Owner<int(T)>::*);")
        .namespace.functions[0]
        .parameters[0]
        .type
    )

    assert dtype == parameter_type


def test_parse_typename_rejects_modifiers() -> None:
    content = """
        static int
    """

    err = "parsing type name: unexpected 'static'"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_typename(content.strip())
