# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    BaseClass,
    ClassDecl,
    Function,
    FundamentalSpecifier,
    Method,
    NameSpecifier,
    PQName,
    Parameter,
    Pointer,
    Reference,
    TemplateArgument,
    TemplateDecl,
    TemplateSpecialization,
    TemplateTypeParam,
    Token,
    Type,
    UsingAlias,
    UsingDecl,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    UsingNamespace,
    parse_string,
    ParsedData,
)


def test_using_namespace():
    content = """
      using namespace foo;
      using namespace foo::bar;
      using namespace ::foo;
      using namespace ::foo::bar;
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_ns=[
                UsingNamespace(ns="foo"),
                UsingNamespace(ns="foo::bar"),
                UsingNamespace(ns="::foo"),
                UsingNamespace(ns="::foo::bar"),
            ]
        )
    )


def test_using_declaration():
    content = """
      using ::foo;
      using foo::bar;
      using ::foo::bar;
      using typename ::foo::bar;
      using typename foo::bar;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using=[
                UsingDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name=""), NameSpecifier(name="foo")]
                    )
                ),
                UsingDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="foo"), NameSpecifier(name="bar")]
                    )
                ),
                UsingDecl(
                    typename=PQName(
                        segments=[
                            NameSpecifier(name=""),
                            NameSpecifier(name="foo"),
                            NameSpecifier(name="bar"),
                        ]
                    )
                ),
                UsingDecl(
                    typename=PQName(
                        segments=[
                            NameSpecifier(name=""),
                            NameSpecifier(name="foo"),
                            NameSpecifier(name="bar"),
                        ]
                    )
                ),
                UsingDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="foo"), NameSpecifier(name="bar")]
                    )
                ),
            ]
        )
    )


# alias-declaration
def test_alias_declaration_1():
    content = """
      using alias = foo;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(typename=PQName(segments=[NameSpecifier(name="foo")])),
                )
            ]
        )
    )


def test_alias_declaration_2():
    content = """
      template <typename T> using alias = foo<T>;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="foo",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(tokens=[Token(value="T")])
                                        ]
                                    ),
                                )
                            ]
                        )
                    ),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ]
        )
    )


def test_alias_declaration_3():
    content = """
      using alias = ::foo::bar;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name=""),
                                NameSpecifier(name="foo"),
                                NameSpecifier(name="bar"),
                            ]
                        )
                    ),
                )
            ]
        )
    )


def test_alias_declaration_4():
    content = """
      template <typename T> using alias = ::foo::bar<T>;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name=""),
                                NameSpecifier(name="foo"),
                                NameSpecifier(
                                    name="bar",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(tokens=[Token(value="T")])
                                        ]
                                    ),
                                ),
                            ]
                        )
                    ),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ]
        )
    )


def test_alias_declaration_5():
    content = """
      using alias = foo::bar;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name="foo"),
                                NameSpecifier(name="bar"),
                            ]
                        )
                    ),
                )
            ]
        )
    )


def test_alias_declaration_6():
    content = """
      template <typename T> using alias = foo<T>::bar;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="alias",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="foo",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(tokens=[Token(value="T")])
                                        ]
                                    ),
                                ),
                                NameSpecifier(name="bar"),
                            ]
                        )
                    ),
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ]
        )
    )


def test_using_many_things():
    content = """
      // clang-format off
      
      using std::thing;
      using MyThing = SomeThing;
      namespace a {
          using std::string;
          using VoidFunction = std::function<void()>;
      
          void fn(string &s, VoidFunction fn, thing * t);
      
          class A : public B {
          public:
              using B::B;
              using IntFunction = std::function<int()>;
      
              void a(string &s, IntFunction fn, thing * t);
          };
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using=[
                UsingDecl(
                    typename=PQName(
                        segments=[
                            NameSpecifier(name="std"),
                            NameSpecifier(name="thing"),
                        ]
                    )
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="MyThing",
                    type=Type(
                        typename=PQName(segments=[NameSpecifier(name="SomeThing")])
                    ),
                )
            ],
            namespaces={
                "a": NamespaceScope(
                    name="a",
                    classes=[
                        ClassScope(
                            class_decl=ClassDecl(
                                typename=PQName(
                                    segments=[NameSpecifier(name="A")], classkey="class"
                                ),
                                bases=[
                                    BaseClass(
                                        access="public",
                                        typename=PQName(
                                            segments=[NameSpecifier(name="B")]
                                        ),
                                    )
                                ],
                            ),
                            methods=[
                                Method(
                                    return_type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="void")]
                                        )
                                    ),
                                    name=PQName(segments=[NameSpecifier(name="a")]),
                                    parameters=[
                                        Parameter(
                                            type=Reference(
                                                ref_to=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="string")
                                                        ]
                                                    )
                                                )
                                            ),
                                            name="s",
                                        ),
                                        Parameter(
                                            type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        NameSpecifier(
                                                            name="IntFunction"
                                                        )
                                                    ]
                                                )
                                            ),
                                            name="fn",
                                        ),
                                        Parameter(
                                            type=Pointer(
                                                ptr_to=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="thing")
                                                        ]
                                                    )
                                                )
                                            ),
                                            name="t",
                                        ),
                                    ],
                                    access="public",
                                )
                            ],
                            using=[
                                UsingDecl(
                                    typename=PQName(
                                        segments=[
                                            NameSpecifier(name="B"),
                                            NameSpecifier(name="B"),
                                        ]
                                    ),
                                    access="public",
                                )
                            ],
                            using_alias=[
                                UsingAlias(
                                    alias="IntFunction",
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="std"),
                                                NameSpecifier(
                                                    name="function",
                                                    specialization=TemplateSpecialization(
                                                        args=[
                                                            TemplateArgument(
                                                                tokens=[
                                                                    Token(value="int"),
                                                                    Token(value="("),
                                                                    Token(value=")"),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                    access="public",
                                )
                            ],
                        )
                    ],
                    functions=[
                        Function(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="fn")]),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[NameSpecifier(name="string")]
                                            )
                                        )
                                    ),
                                    name="s",
                                ),
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                NameSpecifier(name="VoidFunction")
                                            ]
                                        )
                                    ),
                                    name="fn",
                                ),
                                Parameter(
                                    type=Pointer(
                                        ptr_to=Type(
                                            typename=PQName(
                                                segments=[NameSpecifier(name="thing")]
                                            )
                                        )
                                    ),
                                    name="t",
                                ),
                            ],
                        )
                    ],
                    using=[
                        UsingDecl(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="std"),
                                    NameSpecifier(name="string"),
                                ]
                            )
                        )
                    ],
                    using_alias=[
                        UsingAlias(
                            alias="VoidFunction",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(name="std"),
                                        NameSpecifier(
                                            name="function",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        tokens=[
                                                            Token(value="void"),
                                                            Token(value="("),
                                                            Token(value=")"),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ),
                                    ]
                                )
                            ),
                        )
                    ],
                )
            },
        )
    )
