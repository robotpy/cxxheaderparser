# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    BaseClass,
    ClassDecl,
    DecltypeSpecifier,
    Function,
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
    TemplateDecl,
    TemplateSpecialization,
    TemplateTypeParam,
    Token,
    Type,
    UsingAlias,
    UsingDecl,
    Value,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    UsingNamespace,
    parse_string,
    ParsedData,
)


def test_using_namespace() -> None:
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


def test_using_declaration() -> None:
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
def test_alias_declaration_1() -> None:
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


def test_alias_declaration_2() -> None:
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
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="T")
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
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ]
        )
    )


def test_alias_declaration_3() -> None:
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


def test_alias_declaration_4() -> None:
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
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="T")
                                                        ]
                                                    )
                                                )
                                            )
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


def test_alias_declaration_5() -> None:
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


def test_alias_declaration_6() -> None:
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
                                            TemplateArgument(
                                                arg=Type(
                                                    typename=PQName(
                                                        segments=[
                                                            NameSpecifier(name="T")
                                                        ]
                                                    )
                                                )
                                            )
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


def test_using_many_things() -> None:
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
                                                                arg=FunctionType(
                                                                    return_type=Type(
                                                                        typename=PQName(
                                                                            segments=[
                                                                                FundamentalSpecifier(
                                                                                    name="int"
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),
                                                                    parameters=[],
                                                                )
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
                                                        arg=FunctionType(
                                                            return_type=Type(
                                                                typename=PQName(
                                                                    segments=[
                                                                        FundamentalSpecifier(
                                                                            name="void"
                                                                        )
                                                                    ]
                                                                )
                                                            ),
                                                            parameters=[],
                                                        )
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


def test_using_template_in_class() -> None:
    content = """
      class X {
        template <typename T>
        using TT = U<T>;
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="X")], classkey="class"
                        )
                    ),
                    using_alias=[
                        UsingAlias(
                            alias="TT",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="U",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="T"
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
                            template=TemplateDecl(
                                params=[TemplateTypeParam(typekey="typename", name="T")]
                            ),
                            access="private",
                        )
                    ],
                )
            ]
        )
    )


def test_using_typename_in_class() -> None:
    content = """
      template <class D> class P {
      using A = typename f::TP<D>::A;
      public:
        using State = typename f::TP<D>::S;
        P(State st);
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="P")], classkey="class"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="class", name="D")]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="P")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[NameSpecifier(name="State")]
                                        )
                                    ),
                                    name="st",
                                )
                            ],
                            access="public",
                            constructor=True,
                        )
                    ],
                    using_alias=[
                        UsingAlias(
                            alias="A",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(name="f"),
                                        NameSpecifier(
                                            name="TP",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="D"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        ),
                                        NameSpecifier(name="A"),
                                    ],
                                    has_typename=True,
                                )
                            ),
                            access="private",
                        ),
                        UsingAlias(
                            alias="State",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(name="f"),
                                        NameSpecifier(
                                            name="TP",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="D"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        ),
                                        NameSpecifier(name="S"),
                                    ],
                                    has_typename=True,
                                )
                            ),
                            access="public",
                        ),
                    ],
                )
            ]
        )
    )


def test_using_enum_global() -> None:
    content = """
      namespace A {
      using enum B::C;
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "A": NamespaceScope(
                    name="A",
                    using=[
                        UsingDecl(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="B"),
                                    NameSpecifier(name="C"),
                                ],
                                classkey="enum",
                            )
                        )
                    ],
                )
            }
        )
    )


def test_grouped_member_function_pointer_conditional_noexcept_alias() -> None:
    content = """
        struct C {};
        struct Arg {};
        using U = int ((C::*)(Arg) noexcept(false));
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Arg")], classkey="struct"
                        )
                    )
                ),
            ],
            using_alias=[
                UsingAlias(
                    alias="U",
                    type=MemberPointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[NameSpecifier(name="Arg")]
                                        )
                                    )
                                )
                            ],
                            noexcept=Value(tokens=[Token(value="false")]),
                        ),
                        classname=PQName(segments=[NameSpecifier(name="C")]),
                    ),
                )
            ],
        )
    )


def test_function_type_noexcept_aliases() -> None:
    content = """
        struct C {};
        using F = int(double) noexcept;
        using FE = int(double) noexcept(false);
        using P = int (*)(double) noexcept;
        using M = int (C::*)(double) const & noexcept;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="F",
                    type=FunctionType(
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
                        noexcept=Value(tokens=[]),
                    ),
                ),
                UsingAlias(
                    alias="FE",
                    type=FunctionType(
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
                        noexcept=Value(tokens=[Token(value="false")]),
                    ),
                ),
                UsingAlias(
                    alias="P",
                    type=Pointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                FundamentalSpecifier(name="double")
                                            ]
                                        )
                                    )
                                )
                            ],
                            noexcept=Value(tokens=[]),
                        )
                    ),
                ),
                UsingAlias(
                    alias="M",
                    type=MemberPointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                FundamentalSpecifier(name="double")
                                            ]
                                        )
                                    )
                                )
                            ],
                            noexcept=Value(tokens=[]),
                            const=True,
                            ref_qualifier="&",
                        ),
                        classname=PQName(segments=[NameSpecifier(name="C")]),
                    ),
                ),
            ],
        )
    )


def test_qualified_function_type_aliases() -> None:
    content = """
        struct C {};
        using BareConst = int(double) const;
        using BareVolatileRvalue = int(double) volatile &&;
        using Member = int (C::*)(double) const &;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="BareConst",
                    type=FunctionType(
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
                ),
                UsingAlias(
                    alias="BareVolatileRvalue",
                    type=FunctionType(
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
                ),
                UsingAlias(
                    alias="Member",
                    type=MemberPointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                FundamentalSpecifier(name="double")
                                            ]
                                        )
                                    )
                                )
                            ],
                            const=True,
                            ref_qualifier="&",
                        ),
                        classname=PQName(segments=[NameSpecifier(name="C")]),
                    ),
                ),
            ],
        )
    )


def test_template_function_type_with_member_pointer_parameter() -> None:
    content = """
        template <typename T> struct Holder {};
        struct C {};
        using Nested = Holder<int(void (C::*)(double))>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Holder")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="T")]
                        ),
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                ),
            ],
            using_alias=[
                UsingAlias(
                    alias="Nested",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="Holder",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=FunctionType(
                                                    return_type=Type(
                                                        typename=PQName(
                                                            segments=[
                                                                FundamentalSpecifier(
                                                                    name="int"
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                    parameters=[
                                                        Parameter(
                                                            type=MemberPointer(
                                                                ptr_to=FunctionType(
                                                                    return_type=Type(
                                                                        typename=PQName(
                                                                            segments=[
                                                                                FundamentalSpecifier(
                                                                                    name="void"
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),
                                                                    parameters=[
                                                                        Parameter(
                                                                            type=Type(
                                                                                typename=PQName(
                                                                                    segments=[
                                                                                        FundamentalSpecifier(
                                                                                            name="double"
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            )
                                                                        )
                                                                    ],
                                                                ),
                                                                classname=PQName(
                                                                    segments=[
                                                                        NameSpecifier(
                                                                            name="C"
                                                                        )
                                                                    ]
                                                                ),
                                                            )
                                                        )
                                                    ],
                                                )
                                            )
                                        ]
                                    ),
                                )
                            ]
                        )
                    ),
                )
            ],
        )
    )


def test_bare_member_pointer_parameter_aliases() -> None:
    content = """
        struct C {};
        template <typename T> struct Holder {};
        using BareMemberParameter = int(int C::*);
        using NestedBareMemberParameter = Holder<int(int C::*)>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Holder")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="T")]
                        ),
                    )
                ),
            ],
            using_alias=[
                UsingAlias(
                    alias="BareMemberParameter",
                    type=FunctionType(
                        return_type=Type(
                            typename=PQName(segments=[FundamentalSpecifier(name="int")])
                        ),
                        parameters=[
                            Parameter(
                                type=MemberPointer(
                                    ptr_to=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    classname=PQName(
                                        segments=[NameSpecifier(name="C")]
                                    ),
                                )
                            )
                        ],
                    ),
                ),
                UsingAlias(
                    alias="NestedBareMemberParameter",
                    type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(
                                    name="Holder",
                                    specialization=TemplateSpecialization(
                                        args=[
                                            TemplateArgument(
                                                arg=FunctionType(
                                                    return_type=Type(
                                                        typename=PQName(
                                                            segments=[
                                                                FundamentalSpecifier(
                                                                    name="int"
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                    parameters=[
                                                        Parameter(
                                                            type=MemberPointer(
                                                                ptr_to=Type(
                                                                    typename=PQName(
                                                                        segments=[
                                                                            FundamentalSpecifier(
                                                                                name="int"
                                                                            )
                                                                        ]
                                                                    )
                                                                ),
                                                                classname=PQName(
                                                                    segments=[
                                                                        NameSpecifier(
                                                                            name="C"
                                                                        )
                                                                    ]
                                                                ),
                                                            )
                                                        )
                                                    ],
                                                )
                                            )
                                        ]
                                    ),
                                )
                            ]
                        )
                    ),
                ),
            ],
        )
    )


def test_relational_expression_member_pointer_alias() -> None:
    content = """
        struct C {};
        using RelationalScope = int (decltype((1 < 2, C{}))::*)(double);
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="struct"
                        )
                    )
                )
            ],
            using_alias=[
                UsingAlias(
                    alias="RelationalScope",
                    type=MemberPointer(
                        ptr_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                FundamentalSpecifier(name="double")
                                            ]
                                        )
                                    )
                                )
                            ],
                        ),
                        classname=PQName(
                            segments=[
                                DecltypeSpecifier(
                                    tokens=[
                                        Token(value="("),
                                        Token(value="1"),
                                        Token(value="<"),
                                        Token(value="2"),
                                        Token(value=","),
                                        Token(value="C"),
                                        Token(value="{"),
                                        Token(value="}"),
                                        Token(value=")"),
                                    ]
                                )
                            ]
                        ),
                    ),
                )
            ],
        )
    )


def test_rvalue_function_reference_alias() -> None:
    content = """
        using RvalueFunctionReference = int (&&)(double);
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="RvalueFunctionReference",
                    type=MoveReference(
                        moveref_to=FunctionType(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[
                                                FundamentalSpecifier(name="double")
                                            ]
                                        )
                                    )
                                )
                            ],
                        )
                    ),
                )
            ]
        )
    )


def test_member_pointer_to_function_pointer() -> None:
    content = """
        using X = int (* C::*)();
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            using_alias=[
                UsingAlias(
                    alias="X",
                    type=MemberPointer(
                        ptr_to=Pointer(
                            ptr_to=FunctionType(
                                return_type=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                ),
                                parameters=[],
                            )
                        ),
                        classname=PQName(segments=[NameSpecifier(name="C")]),
                    ),
                )
            ]
        )
    )


def test_array_and_trailing_return_type_aliases() -> None:
    content = """
        struct C {};
        using A = int[3];
        using P = auto (*)() -> int;
        using M = auto (C::*)() -> int;
    """

    data = parse_string(content, cleandoc=True)
    aliases = {alias.alias: alias.type for alias in data.namespace.using_alias}

    assert aliases["A"].format() == "int[3]"

    pointer = aliases["P"]
    assert isinstance(pointer, Pointer)
    assert isinstance(pointer.ptr_to, FunctionType)
    assert pointer.ptr_to.has_trailing_return
    assert pointer.format() == "auto (*)() -> int"

    member = aliases["M"]
    assert isinstance(member, MemberPointer)
    assert isinstance(member.ptr_to, FunctionType)
    assert member.ptr_to.has_trailing_return
    assert member.format() == "auto (C::*)() -> int"


def test_using_enum_in_struct() -> None:
    content = """
      struct S {
        using enum fruit;
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        )
                    ),
                    using=[
                        UsingDecl(
                            typename=PQName(
                                segments=[NameSpecifier(name="fruit")], classkey="enum"
                            ),
                            access="public",
                        )
                    ],
                )
            ]
        )
    )
