from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_string
from cxxheaderparser.tokfmt import Token
from cxxheaderparser.types import (
    Concept,
    Function,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Parameter,
    TemplateArgument,
    TemplateDecl,
    TemplateNonTypeParam,
    TemplateSpecialization,
    TemplateTypeParam,
    Type,
    Value,
    Variable,
)


def test_concept_basic_constraint() -> None:
    content = """
      template <class T, class U>
      concept Derived = std::is_base_of<U, T>::value;

      template <Derived<Base> T> void f(T); // T is constrained by Derived<T, Base>
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
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(segments=[NameSpecifier(name="T")])
                            )
                        )
                    ],
                    template=TemplateDecl(
                        params=[
                            TemplateNonTypeParam(
                                type=Type(
                                    typename=PQName(
                                        segments=[
                                            NameSpecifier(
                                                name="Derived",
                                                specialization=TemplateSpecialization(
                                                    args=[
                                                        TemplateArgument(
                                                            arg=Type(
                                                                typename=PQName(
                                                                    segments=[
                                                                        NameSpecifier(
                                                                            name="Base"
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),
                                            )
                                        ]
                                    )
                                ),
                                name="T",
                            )
                        ]
                    ),
                )
            ],
            concepts=[
                Concept(
                    template=TemplateDecl(
                        params=[
                            TemplateTypeParam(typekey="class", name="T"),
                            TemplateTypeParam(typekey="class", name="U"),
                        ]
                    ),
                    name="Derived",
                    raw_constraint=Value(
                        tokens=[
                            Token(value="std"),
                            Token(value="::"),
                            Token(value="is_base_of"),
                            Token(value="<"),
                            Token(value="U"),
                            Token(value=","),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="::"),
                            Token(value="value"),
                        ]
                    ),
                )
            ],
        )
    )


def test_concept_basic_constraint2() -> None:
    content = """
      template <class T> constexpr bool is_meowable = true;

      template <class T> constexpr bool is_cat = true;

      template <class T>
      concept Meowable = is_meowable<T>;

      template <class T>
      concept BadMeowableCat = is_meowable<T> && is_cat<T>;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="is_meowable")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="bool")])
                    ),
                    value=Value(tokens=[Token(value="true")]),
                    constexpr=True,
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="is_cat")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="bool")])
                    ),
                    value=Value(tokens=[Token(value="true")]),
                    constexpr=True,
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                ),
            ],
            concepts=[
                Concept(
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    name="Meowable",
                    raw_constraint=Value(
                        tokens=[
                            Token(value="is_meowable"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                        ]
                    ),
                ),
                Concept(
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    name="BadMeowableCat",
                    raw_constraint=Value(
                        tokens=[
                            Token(value="is_meowable"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="&&"),
                            Token(value="is_cat"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                        ]
                    ),
                ),
            ],
        )
    )


def test_concept_basic_requires() -> None:
    content = """
      template <typename T>
      concept Hashable = requires(T a) {
        { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
      };

      template <Hashable T> void f(T) {}
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
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(segments=[NameSpecifier(name="T")])
                            )
                        )
                    ],
                    has_body=True,
                    template=TemplateDecl(
                        params=[
                            TemplateNonTypeParam(
                                type=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="Hashable")]
                                    )
                                ),
                                name="T",
                            )
                        ]
                    ),
                )
            ],
            concepts=[
                Concept(
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                    name="Hashable",
                    raw_constraint=Value(
                        tokens=[
                            Token(value="requires"),
                            Token(value="("),
                            Token(value="T"),
                            Token(value="a"),
                            Token(value=")"),
                            Token(value="{"),
                            Token(value="{"),
                            Token(value="std"),
                            Token(value="::"),
                            Token(value="hash"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="{"),
                            Token(value="}"),
                            Token(value="("),
                            Token(value="a"),
                            Token(value=")"),
                            Token(value="}"),
                            Token(value="->"),
                            Token(value="std"),
                            Token(value="::"),
                            Token(value="convertible_to"),
                            Token(value="<"),
                            Token(value="std"),
                            Token(value="::"),
                            Token(value="size_t"),
                            Token(value=">"),
                            Token(value=";"),
                            Token(value="}"),
                        ]
                    ),
                )
            ],
        )
    )


def test_concept_nested_requirements() -> None:
    content = """
      template<class T>
      concept Semiregular = DefaultConstructible<T> &&
          CopyConstructible<T> && CopyAssignable<T> && Destructible<T> &&
      requires(T a, std::size_t n)
      {
          requires Same<T*, decltype(&a)>; // nested: "Same<...> evaluates to true"
          { a.~T() } noexcept; // compound: "a.~T()" is a valid expression that doesn't throw
          requires Same<T*, decltype(new T)>; // nested: "Same<...> evaluates to true"
          requires Same<T*, decltype(new T[n])>; // nested
          { delete new T }; // compound
          { delete new T[n] }; // compound
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            concepts=[
                Concept(
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    name="Semiregular",
                    raw_constraint=Value(
                        tokens=[
                            Token(value="DefaultConstructible"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="&&"),
                            Token(value="CopyConstructible"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="&&"),
                            Token(value="CopyAssignable"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="&&"),
                            Token(value="Destructible"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value=">"),
                            Token(value="&&"),
                            Token(value="requires"),
                            Token(value="("),
                            Token(value="T"),
                            Token(value="a"),
                            Token(value=","),
                            Token(value="std"),
                            Token(value="::"),
                            Token(value="size_t"),
                            Token(value="n"),
                            Token(value=")"),
                            Token(value="{"),
                            Token(value="requires"),
                            Token(value="Same"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value="*"),
                            Token(value=","),
                            Token(value="decltype"),
                            Token(value="("),
                            Token(value="&"),
                            Token(value="a"),
                            Token(value=")"),
                            Token(value=">"),
                            Token(value=";"),
                            Token(value="{"),
                            Token(value="a"),
                            Token(value="."),
                            Token(value="~T"),
                            Token(value="("),
                            Token(value=")"),
                            Token(value="}"),
                            Token(value="noexcept"),
                            Token(value=";"),
                            Token(value="requires"),
                            Token(value="Same"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value="*"),
                            Token(value=","),
                            Token(value="decltype"),
                            Token(value="("),
                            Token(value="new"),
                            Token(value="T"),
                            Token(value=")"),
                            Token(value=">"),
                            Token(value=";"),
                            Token(value="requires"),
                            Token(value="Same"),
                            Token(value="<"),
                            Token(value="T"),
                            Token(value="*"),
                            Token(value=","),
                            Token(value="decltype"),
                            Token(value="("),
                            Token(value="new"),
                            Token(value="T"),
                            Token(value="["),
                            Token(value="n"),
                            Token(value="]"),
                            Token(value=")"),
                            Token(value=">"),
                            Token(value=";"),
                            Token(value="{"),
                            Token(value="delete"),
                            Token(value="new"),
                            Token(value="T"),
                            Token(value="}"),
                            Token(value=";"),
                            Token(value="{"),
                            Token(value="delete"),
                            Token(value="new"),
                            Token(value="T"),
                            Token(value="["),
                            Token(value="n"),
                            Token(value="]"),
                            Token(value="}"),
                            Token(value=";"),
                            Token(value="}"),
                        ]
                    ),
                )
            ]
        )
    )
