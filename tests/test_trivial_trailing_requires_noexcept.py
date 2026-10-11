from cxxheaderparser.simple import (
    Function,
    NamespaceScope,
    ParsedData,
    Value,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    TemplateDecl,
    TemplateTypeParam,
    Token,
    Type,
)
import re
import pytest
from cxxheaderparser.errors import CxxParseError


def test_sequential_function_suffixes_noexcept() -> None:
    content = """
        template<class T> void f() noexcept requires (true); int after;
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
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    noexcept=Value(tokens=[]),
                    raw_requires=Value(
                        tokens=[Token(value="("), Token(value="true"), Token(value=")")]
                    ),
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


def test_sequential_function_suffixes_conditional_noexcept() -> None:
    content = """
        template<class T> void f() noexcept(false) requires (true); int after;
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
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    noexcept=Value(tokens=[Token(value="false")]),
                    raw_requires=Value(
                        tokens=[Token(value="("), Token(value="true"), Token(value=")")]
                    ),
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


def test_sequential_function_suffixes_return_type() -> None:
    content = """
        template<class T> auto f() -> int requires (true); int after;
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
                    has_trailing_return=True,
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    raw_requires=Value(
                        tokens=[Token(value="("), Token(value="true"), Token(value=")")]
                    ),
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


def test_sequential_function_suffixes_noexcept_return_type() -> None:
    content = """
        template<class T> auto f() noexcept -> int requires (true); int after;
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
                    has_trailing_return=True,
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    noexcept=Value(tokens=[]),
                    raw_requires=Value(
                        tokens=[Token(value="("), Token(value="true"), Token(value=")")]
                    ),
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


def test_non_template_constraint_still_rejected() -> None:
    content = """
        void f() noexcept requires (true);
    """

    err = "<str>:1: parse error evaluating 'requires': unexpected 'requires'"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_string(content, cleandoc=True)
