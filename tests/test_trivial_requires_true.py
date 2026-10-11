from cxxheaderparser.simple import (
    Function,
    NamespaceScope,
    ParsedData,
    Value,
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


def test_boolean_constraint_leading_true() -> None:
    content = """
        template<class T> requires true void f();
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
                        raw_requires_pre=Value(tokens=[Token(value="true")]),
                    ),
                )
            ]
        )
    )


def test_boolean_constraint_leading_false() -> None:
    content = """
        template<class T> requires false void f();
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
                        raw_requires_pre=Value(tokens=[Token(value="false")]),
                    ),
                )
            ]
        )
    )


def test_boolean_constraint_leading_or() -> None:
    content = """
        template<class T> requires false || true void f();
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
                                Token(value="false"),
                                Token(value="||"),
                                Token(value="true"),
                            ]
                        ),
                    ),
                )
            ]
        )
    )


def test_boolean_constraint_leading_and() -> None:
    content = """
        template<class T> requires true && false void f();
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
                                Token(value="true"),
                                Token(value="&&"),
                                Token(value="false"),
                            ]
                        ),
                    ),
                )
            ]
        )
    )


def test_boolean_constraint_trailing_true() -> None:
    content = """
        template<class T> void f() requires true;
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
                    raw_requires=Value(tokens=[Token(value="true")]),
                )
            ]
        )
    )


def test_boolean_constraint_trailing_false() -> None:
    content = """
        template<class T> void f() requires false;
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
                    raw_requires=Value(tokens=[Token(value="false")]),
                )
            ]
        )
    )


def test_boolean_constraint_trailing_or() -> None:
    content = """
        template<class T> void f() requires false || true;
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
                    raw_requires=Value(
                        tokens=[
                            Token(value="false"),
                            Token(value="||"),
                            Token(value="true"),
                        ]
                    ),
                )
            ]
        )
    )


def test_boolean_constraint_trailing_and() -> None:
    content = """
        template<class T> void f() requires true && false;
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
                    raw_requires=Value(
                        tokens=[
                            Token(value="true"),
                            Token(value="&&"),
                            Token(value="false"),
                        ]
                    ),
                )
            ]
        )
    )
