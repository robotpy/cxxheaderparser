from cxxheaderparser.simple import (
    NamespaceScope,
    ParsedData,
    UsingAlias,
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


def test_constrained_alias() -> None:
    content = """
        template<class T> requires (true) using A = T; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="A",
                    type=Type(typename=PQName(segments=[NameSpecifier(name="T")])),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")],
                        raw_requires_pre=Value(
                            tokens=[
                                Token(value="("),
                                Token(value="true"),
                                Token(value=")"),
                            ]
                        ),
                    ),
                )
            ],
        )
    )
