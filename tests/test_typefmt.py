import typing

import pytest

from cxxheaderparser.tokfmt import Token
from cxxheaderparser.types import (
    Array,
    DecoratedType,
    FunctionType,
    FundamentalSpecifier,
    Method,
    MemberPointer,
    MoveReference,
    NameSpecifier,
    PQName,
    Parameter,
    Pointer,
    Reference,
    TemplateArgument,
    TemplateSpecialization,
    TemplateDecl,
    Type,
    TypeId,
    Value,
)


@pytest.mark.parametrize(
    "pytype,typestr,declstr",
    [
        (
            Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
            "int",
            "int name",
        ),
        (
            Type(
                typename=PQName(segments=[FundamentalSpecifier(name="int")]), const=True
            ),
            "const int",
            "const int name",
        ),
        (
            Type(
                typename=PQName(segments=[NameSpecifier(name="S")], classkey="struct")
            ),
            "struct S",
            "struct S name",
        ),
        (
            Pointer(
                ptr_to=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="int")])
                )
            ),
            "int*",
            "int* name",
        ),
        (
            Pointer(
                ptr_to=Pointer(
                    ptr_to=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    )
                )
            ),
            "int**",
            "int** name",
        ),
        (
            Reference(
                ref_to=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="int")])
                )
            ),
            "int&",
            "int& name",
        ),
        (
            Reference(
                ref_to=Array(
                    array_of=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    size=Value(tokens=[Token(value="3")]),
                )
            ),
            "int (&)[3]",
            "int (& name)[3]",
        ),
        (
            MoveReference(
                moveref_to=Type(
                    typename=PQName(
                        segments=[NameSpecifier(name="T"), NameSpecifier(name="T")]
                    )
                )
            ),
            "T::T&&",
            "T::T&& name",
        ),
        (
            Pointer(
                ptr_to=Array(
                    array_of=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    size=Value(tokens=[Token(value="3")]),
                )
            ),
            "int (*)[3]",
            "int (* name)[3]",
        ),
        (
            Pointer(
                ptr_to=Array(
                    array_of=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    size=Value(tokens=[Token(value="3")]),
                ),
                const=True,
            ),
            "int (* const)[3]",
            "int (* const name)[3]",
        ),
        (
            FunctionType(
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
            ),
            "int (int)",
            "int name(int)",
        ),
        (
            FunctionType(
                return_type=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="int")])
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
                const=True,
            ),
            "int (double) const",
            "int name(double) const",
        ),
        (
            FunctionType(
                return_type=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="int")])
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
                volatile=True,
                ref_qualifier="&&",
            ),
            "int (double) volatile &&",
            "int name(double) volatile &&",
        ),
        (
            MemberPointer(
                ptr_to=FunctionType(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
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
                    const=True,
                    ref_qualifier="&",
                ),
                classname=PQName(segments=[NameSpecifier(name="C")]),
            ),
            "int (C::*)(double) const &",
            "int (C::* name)(double) const &",
        ),
        (
            FunctionType(
                return_type=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="int")])
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
                has_trailing_return=True,
                const=True,
                ref_qualifier="&",
            ),
            "auto (double) const & -> int",
            "auto name(double) const & -> int",
        ),
        (
            FunctionType(
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
                has_trailing_return=True,
            ),
            "auto (int) -> int",
            "auto name(int) -> int",
        ),
        (
            FunctionType(
                return_type=Type(
                    typename=PQName(
                        segments=[FundamentalSpecifier(name="void")],
                    ),
                ),
                parameters=[
                    Parameter(
                        type=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="int")],
                            ),
                        ),
                        name="a",
                    ),
                    Parameter(
                        type=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="int")],
                            ),
                        ),
                        name="b",
                    ),
                ],
            ),
            "void (int a, int b)",
            "void name(int a, int b)",
        ),
        (
            Pointer(
                ptr_to=FunctionType(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            )
                        )
                    ],
                )
            ),
            "int (*)(int)",
            "int (* name)(int)",
        ),
        (
            MemberPointer(
                ptr_to=FunctionType(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="char")]
                                )
                            ),
                            name="x",
                        ),
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="float")]
                                )
                            ),
                            name="y",
                        ),
                    ],
                ),
                classname=PQName(segments=[NameSpecifier(name="Fred")]),
            ),
            "int (Fred::*)(char x, float y)",
            "int (Fred::* name)(char x, float y)",
        ),
        (
            Type(
                typename=PQName(
                    segments=[
                        NameSpecifier(name="std"),
                        NameSpecifier(
                            name="function",
                            specialization=TemplateSpecialization(
                                args=[
                                    TemplateArgument(
                                        arg=FunctionType(
                                            return_type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(name="int")
                                                    ]
                                                )
                                            ),
                                            parameters=[
                                                Parameter(
                                                    type=Type(
                                                        typename=PQName(
                                                            segments=[
                                                                FundamentalSpecifier(
                                                                    name="int"
                                                                )
                                                            ]
                                                        )
                                                    )
                                                )
                                            ],
                                        )
                                    )
                                ]
                            ),
                        ),
                    ]
                )
            ),
            "std::function<int (int)>",
            "std::function<int (int)> name",
        ),
        (
            Type(
                typename=PQName(
                    segments=[
                        NameSpecifier(
                            name="foo",
                            specialization=TemplateSpecialization(
                                args=[
                                    TemplateArgument(
                                        arg=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(name=""),
                                                    NameSpecifier(name="T"),
                                                ],
                                            )
                                        ),
                                    )
                                ]
                            ),
                        )
                    ]
                ),
            ),
            "foo<::T>",
            "foo<::T> name",
        ),
        (
            Type(
                typename=PQName(
                    segments=[
                        NameSpecifier(
                            name="foo",
                            specialization=TemplateSpecialization(
                                args=[
                                    TemplateArgument(
                                        arg=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(name=""),
                                                    NameSpecifier(name="T"),
                                                ],
                                                has_typename=True,
                                            )
                                        ),
                                    )
                                ]
                            ),
                        )
                    ]
                ),
            ),
            "foo<typename ::T>",
            "foo<typename ::T> name",
        ),
    ],
)
def test_typefmt(pytype: TypeId, typestr: str, declstr: str):
    # basic formatting
    assert pytype.format() == typestr

    # as a type declaration
    assert pytype.format_decl("name") == declstr


def test_function_type_fixed_parameter_and_varargs_format() -> None:
    dtype = FunctionType(
        return_type=Type(typename=PQName(segments=[FundamentalSpecifier(name="int")])),
        parameters=[
            Parameter(
                type=Type(typename=PQName(segments=[FundamentalSpecifier(name="char")]))
            )
        ],
        vararg=True,
    )

    assert dtype.format() == "int (char, ...)"
    assert dtype.format_decl("fn") == "int fn(char, ...)"


def test_function_type_noexcept_format() -> None:
    int_type = Type(typename=PQName(segments=[FundamentalSpecifier(name="int")]))
    parameters = [
        Parameter(
            type=Type(typename=PQName(segments=[FundamentalSpecifier(name="double")]))
        )
    ]

    plain = FunctionType(
        return_type=int_type,
        parameters=parameters,
        noexcept=Value(tokens=[]),
    )
    assert plain.format() == "int (double) noexcept"
    assert plain.format_decl("name") == "int name(double) noexcept"

    conditional = FunctionType(
        return_type=int_type,
        parameters=parameters,
        noexcept=Value(tokens=[Token(value="false")]),
        const=True,
        ref_qualifier="&",
    )
    assert conditional.format() == "int (double) const & noexcept(false)"
    assert conditional.format_decl("name") == "int name(double) const & noexcept(false)"

    trailing = FunctionType(
        return_type=int_type,
        parameters=parameters,
        has_trailing_return=True,
        noexcept=Value(tokens=[]),
    )
    assert trailing.format() == "auto (double) noexcept -> int"
    assert trailing.format_decl("name") == "auto name(double) noexcept -> int"


def test_decorated_member_function_pointer_format() -> None:
    member_pointer = MemberPointer(
        ptr_to=FunctionType(
            return_type=Type(
                typename=PQName(segments=[FundamentalSpecifier(name="int")])
            ),
            parameters=[],
        ),
        classname=PQName(segments=[NameSpecifier(name="C")]),
    )

    cases: typing.List[typing.Tuple[DecoratedType, str, str]] = [
        (Pointer(member_pointer), "int (C::**)()", "int (C::** name)()"),
        (Reference(member_pointer), "int (C::*&)()", "int (C::*& name)()"),
        (
            Reference(member_pointer, restrict=True),
            "int (C::*& __restrict__)()",
            "int (C::*& __restrict__ name)()",
        ),
        (MoveReference(member_pointer), "int (C::*&&)()", "int (C::*&& name)()"),
        (
            Array(member_pointer, Value(tokens=[Token(value="3")])),
            "int (C::*[3])()",
            "int (C::* name[3])()",
        ),
    ]

    for dtype, typestr, declstr in cases:
        assert dtype.format() == typestr
        assert dtype.format_decl("name") == declstr


def test_recursive_member_pointer_declarator_format() -> None:
    dtype = MemberPointer(
        ptr_to=Pointer(
            ptr_to=Pointer(
                ptr_to=FunctionType(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
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
                )
            )
        ),
        classname=PQName(segments=[NameSpecifier(name="C")]),
    )

    assert dtype.format() == "int (** C::*)(double)"
    assert dtype.format_decl("p") == "int (** C::* p)(double)"


def _recursive_declarator_cases() -> (
    typing.List[typing.Tuple[DecoratedType, str, str, str]]
):
    int_type = Type(typename=PQName(segments=[FundamentalSpecifier(name="int")]))
    function_type = FunctionType(
        return_type=int_type,
        parameters=[
            Parameter(
                type=Type(
                    typename=PQName(segments=[FundamentalSpecifier(name="double")])
                )
            )
        ],
    )
    size = Value(tokens=[Token(value="3")])
    classname = PQName(segments=[NameSpecifier(name="C")])

    return [
        (
            Pointer(ptr_to=Pointer(ptr_to=Array(array_of=int_type, size=size))),
            "array_pointer",
            "int (**)[3]",
            "int (** array_pointer)[3]",
        ),
        (
            Array(
                array_of=MemberPointer(
                    ptr_to=Pointer(ptr_to=Pointer(ptr_to=function_type)),
                    classname=classname,
                ),
                size=size,
            ),
            "array_member",
            "int (** C::*[3])(double)",
            "int (** C::* array_member[3])(double)",
        ),
        (
            Pointer(ptr_to=Pointer(ptr_to=function_type), const=True),
            "qualified_pointer",
            "int (** const)(double)",
            "int (** const qualified_pointer)(double)",
        ),
        (
            Reference(ref_to=Pointer(ptr_to=function_type)),
            "lvalue_reference",
            "int (*&)(double)",
            "int (*& lvalue_reference)(double)",
        ),
        (
            MoveReference(moveref_to=Pointer(ptr_to=function_type)),
            "rvalue_reference",
            "int (*&&)(double)",
            "int (*&& rvalue_reference)(double)",
        ),
        (
            Pointer(
                ptr_to=MemberPointer(
                    ptr_to=FunctionType(
                        return_type=int_type,
                        parameters=[
                            Parameter(
                                type=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="double")]
                                    )
                                )
                            )
                        ],
                        const=True,
                        ref_qualifier="&",
                    ),
                    classname=classname,
                )
            ),
            "qualified_member_pointer",
            "int (C::**)(double) const &",
            "int (C::** qualified_member_pointer)(double) const &",
        ),
    ]


@pytest.mark.parametrize(
    "dtype,name,typestr,declstr",
    _recursive_declarator_cases(),
    ids=[
        "nested-pointer-array",
        "array-member-pointer-function",
        "qualified-pointer-function",
        "reference-pointer-function",
        "move-reference-pointer-function",
        "qualified-member-function-pointer",
    ],
)
def test_recursive_declarator_chain_format(
    dtype: DecoratedType, name: str, typestr: str, declstr: str
) -> None:
    assert dtype.format() == typestr
    assert dtype.format_decl(name) == declstr
