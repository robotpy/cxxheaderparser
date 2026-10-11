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


def test_requires_expression_without_parameters() -> None:
    content = """
        template<class T> requires requires { typename T::type; } void f(); int after;
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
                        params=[TemplateTypeParam(typekey="class", name="T")],
                        raw_requires_pre=Value(
                            tokens=[
                                Token(value="requires"),
                                Token(value="{"),
                                Token(value="typename"),
                                Token(value="T"),
                                Token(value="::"),
                                Token(value="type"),
                                Token(value=";"),
                                Token(value="}"),
                            ]
                        ),
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


def test_requires_expression_with_parameters() -> None:
    content = """
        template<class T> requires requires (T t) { t.f(); } void f(); int after;
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
                        params=[TemplateTypeParam(typekey="class", name="T")],
                        raw_requires_pre=Value(
                            tokens=[
                                Token(value="requires"),
                                Token(value="("),
                                Token(value="T"),
                                Token(value="t"),
                                Token(value=")"),
                                Token(value="{"),
                                Token(value="t"),
                                Token(value="."),
                                Token(value="f"),
                                Token(value="("),
                                Token(value=")"),
                                Token(value=";"),
                                Token(value="}"),
                            ]
                        ),
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
