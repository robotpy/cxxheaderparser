import pytest

from cxxheaderparser import simple
from cxxheaderparser.errors import CxxParseError
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    TemplateArgument,
    TemplateSpecialization,
    Type,
)


@pytest.mark.parametrize(
    "text, segments",
    [
        ("foo", ["foo"]),
        (" :: name :: Bar :: count ", ["", "name", "Bar", "count"]),
        ("C::C", ["C", "C"]),
        ("C::~C", ["C", "~C"]),
        ("C::~ C", ["C", "~C"]),
    ],
)
def test_parse_name(text, segments):
    assert simple.parse_name(text) == PQName([NameSpecifier(s) for s in segments])


def test_parse_name_nested_template():
    argument = Type(PQName([NameSpecifier("ns"), NameSpecifier("T")]))
    inner = Type(
        PQName(
            [
                NameSpecifier(
                    "Inner", TemplateSpecialization([TemplateArgument(argument)])
                )
            ]
        )
    )
    assert simple.parse_name("Outer< Inner< ns :: T > >::member") == PQName(
        [
            NameSpecifier("Outer", TemplateSpecialization([TemplateArgument(inner)])),
            NameSpecifier("member"),
        ]
    )


@pytest.mark.parametrize(
    "text, name",
    [
        ("operator +", "operator+"),
        ("operator ()", "operator()"),
        ("operator [ ]", "operator[]"),
        ("operator <<", "operator<<"),
        ("operator &&", "operator&&"),
        ("operator ||", "operator||"),
        ("operator ->", "operator->"),
        ("operator ->*", "operator->*"),
        ("operator <=>", "operator<=>"),
        ("operator ~", "operator~"),
        ("operator new []", "operatornew[]"),
        ("operator delete", "operatordelete"),
        ("operator co_await", "operatorco_await"),
        ('operator "" _suffix', 'operator""_suffix'),
        ("operator bool", "operator bool"),
        ("operator int const *", "operator const int*"),
        ("operator ns :: T &", "operator ns::T&"),
        ("operator Container< ns::T >", "operator Container<ns::T>"),
    ],
)
def test_parse_name_operator(text, name):
    assert simple.parse_name("C::" + text) == PQName(
        [NameSpecifier("C"), NameSpecifier(name)]
    )
    assert simple.parse_name(text) == PQName([NameSpecifier(name)])


@pytest.mark.parametrize(
    "text",
    [
        "",
        "::",
        "n::",
        "C<",
        "C<int",
        "C::operator",
        "int",
        "C*",
        "C const",
        "f()",
        "C::operator+()",
        "C::operator bool()",
        "C::operator[",
        "C::operator.",
        "C::operator?",
        "C::operator+::x",
        "C::operator int[2]",
        "C::operator bool extra",
        "auto",
    ],
)
def test_parse_name_invalid(text):
    with pytest.raises(CxxParseError):
        simple.parse_name(text)


@pytest.mark.parametrize("operator", ["()", "+", "<<", "<", '""_suffix'])
def test_parse_name_operator_template(operator):
    assert simple.parse_name("C::operator" + operator + " <int>") == PQName(
        [
            NameSpecifier("C"),
            NameSpecifier(
                "operator" + operator,
                TemplateSpecialization(
                    [TemplateArgument(Type(PQName([FundamentalSpecifier("int")])))]
                ),
            ),
        ]
    )


def test_parse_name_rejects_empty_pack():
    with pytest.raises(CxxParseError):
        simple.parse_name("C<...>")


def test_parse_typename_still_rejects_operators():
    with pytest.raises(CxxParseError):
        simple.parse_typename("C::operator bool")
