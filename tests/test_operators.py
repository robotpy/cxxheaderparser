# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    ClassDecl,
    Function,
    FundamentalSpecifier,
    Method,
    MoveReference,
    NameSpecifier,
    Pointer,
    PQName,
    Parameter,
    Reference,
    TemplateArgument,
    TemplateDecl,
    TemplateSpecialization,
    TemplateTypeParam,
    Type,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_class_operators() -> None:
    content = r"""
      class OperatorClass {
      public:
        void operator=(const Sample25Class &);
        void operator-=(const Sample25Class &);
        void operator+=();
        void operator[]();
        bool operator==(const int &b);
        OperatorClass &operator+();
        void operator-();
        void operator*();
        void operator\();
        void operator%();
        void operator^();
        void operator|();
        void operator&();
        void operator~();
        void operator<<();
        void operator>>();
        void operator!=();
        void operator<();
        void operator>();
        void operator>=();
        void operator<=();
        void operator!();
        void operator&&();
        void operator||();
        void operator+=();
        void operator-=();
        void operator*=();
        void operator\=();
        void operator%=();
        void operator&=();
        void operator|=();
        void operator^=();
        void operator<<=();
        void operator>>=();
        void operator++();
        void operator--();
        void operator()();
        void operator->();
        void operator,();
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="OperatorClass")],
                            classkey="class",
                        )
                    ),
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator=")]),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(name="Sample25Class")
                                                ]
                                            ),
                                            const=True,
                                        )
                                    )
                                )
                            ],
                            access="public",
                            operator="=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator-=")]),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    NameSpecifier(name="Sample25Class")
                                                ]
                                            ),
                                            const=True,
                                        )
                                    )
                                )
                            ],
                            access="public",
                            operator="-=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator+=")]),
                            parameters=[],
                            access="public",
                            operator="+=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator[]")]),
                            parameters=[],
                            access="public",
                            operator="[]",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="bool")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator==")]),
                            parameters=[
                                Parameter(
                                    type=Reference(
                                        ref_to=Type(
                                            typename=PQName(
                                                segments=[
                                                    FundamentalSpecifier(name="int")
                                                ]
                                            ),
                                            const=True,
                                        )
                                    ),
                                    name="b",
                                )
                            ],
                            access="public",
                            operator="==",
                        ),
                        Method(
                            return_type=Reference(
                                ref_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="OperatorClass")]
                                    )
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator+")]),
                            parameters=[],
                            access="public",
                            operator="+",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator-")]),
                            parameters=[],
                            access="public",
                            operator="-",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator*")]),
                            parameters=[],
                            access="public",
                            operator="*",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator\\")]),
                            parameters=[],
                            access="public",
                            operator="\\",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator%")]),
                            parameters=[],
                            access="public",
                            operator="%",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator^")]),
                            parameters=[],
                            access="public",
                            operator="^",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator|")]),
                            parameters=[],
                            access="public",
                            operator="|",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator&")]),
                            parameters=[],
                            access="public",
                            operator="&",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator~")]),
                            parameters=[],
                            access="public",
                            operator="~",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator<<")]),
                            parameters=[],
                            access="public",
                            operator="<<",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator>>")]),
                            parameters=[],
                            access="public",
                            operator=">>",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator!=")]),
                            parameters=[],
                            access="public",
                            operator="!=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator<")]),
                            parameters=[],
                            access="public",
                            operator="<",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator>")]),
                            parameters=[],
                            access="public",
                            operator=">",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator>=")]),
                            parameters=[],
                            access="public",
                            operator=">=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator<=")]),
                            parameters=[],
                            access="public",
                            operator="<=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator!")]),
                            parameters=[],
                            access="public",
                            operator="!",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator&&")]),
                            parameters=[],
                            access="public",
                            operator="&&",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator||")]),
                            parameters=[],
                            access="public",
                            operator="||",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator+=")]),
                            parameters=[],
                            access="public",
                            operator="+=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator-=")]),
                            parameters=[],
                            access="public",
                            operator="-=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator*=")]),
                            parameters=[],
                            access="public",
                            operator="*=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator\\=")]),
                            parameters=[],
                            access="public",
                            operator="\\=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator%=")]),
                            parameters=[],
                            access="public",
                            operator="%=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator&=")]),
                            parameters=[],
                            access="public",
                            operator="&=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator|=")]),
                            parameters=[],
                            access="public",
                            operator="|=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator^=")]),
                            parameters=[],
                            access="public",
                            operator="^=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator<<=")]),
                            parameters=[],
                            access="public",
                            operator="<<=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator>>=")]),
                            parameters=[],
                            access="public",
                            operator=">>=",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator++")]),
                            parameters=[],
                            access="public",
                            operator="++",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator--")]),
                            parameters=[],
                            access="public",
                            operator="--",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator()")]),
                            parameters=[],
                            access="public",
                            operator="()",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator->")]),
                            parameters=[],
                            access="public",
                            operator="->",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator,")]),
                            parameters=[],
                            access="public",
                            operator=",",
                        ),
                    ],
                )
            ]
        )
    )


def test_conversion_operators() -> None:
    content = """
      
      class Foo
      {
      public:
          operator Type1() const { return SomeMethod(); }
          explicit operator Type2() const;
          virtual operator bool() const;
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Foo")], classkey="class"
                        )
                    ),
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(segments=[NameSpecifier(name="Type1")])
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            has_body=True,
                            access="public",
                            const=True,
                            operator="conversion",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(segments=[NameSpecifier(name="Type2")])
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            access="public",
                            const=True,
                            explicit=True,
                            operator="conversion",
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="bool")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            access="public",
                            const=True,
                            virtual=True,
                            operator="conversion",
                        ),
                    ],
                )
            ]
        )
    )


def test_conversion_operators_decorated() -> None:
    content = """
      struct S {
        operator const native_handle_t*() const;
        operator const native_handle_t&() const;
        operator const native_handle_t&&() const;
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
                    methods=[
                        Method(
                            return_type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="native_handle_t")]
                                    ),
                                    const=True,
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            access="public",
                            const=True,
                            operator="conversion",
                        ),
                        Method(
                            return_type=Reference(
                                ref_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="native_handle_t")]
                                    ),
                                    const=True,
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            access="public",
                            const=True,
                            operator="conversion",
                        ),
                        Method(
                            return_type=MoveReference(
                                moveref_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="native_handle_t")]
                                    ),
                                    const=True,
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="operator")]),
                            parameters=[],
                            access="public",
                            const=True,
                            operator="conversion",
                        ),
                    ],
                )
            ]
        )
    )


def test_qualified_conversion_operator_impls() -> None:
    content = """
      foo::operator bool() const { return bar; }
      foo::operator bar() {;}

      Foo::operator Type1() { return SomeMethod(); }
      const Foo::operator Type2() const { return SomeMethod(); }
      volatile Foo::operator Type3() const { return SomeMethod(); }

      Foo::operator Foo::Type4() { return SomeMethod(); }
      const Foo::operator Foo::Type5() const { return SomeMethod(); }
      volatile Foo::operator Foo::Type6() const { return SomeMethod(); }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            method_impls=[
                Method(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="bool")])
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                    const=True,
                ),
                Method(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="bar")])
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                ),
                Method(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="Type1")])
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                ),
                Method(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="Type2")]),
                        const=True,
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                    const=True,
                ),
                Method(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="Type3")]),
                        volatile=True,
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                    const=True,
                ),
                Method(
                    return_type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name="Foo"),
                                NameSpecifier(name="Type4"),
                            ]
                        )
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                ),
                Method(
                    return_type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name="Foo"),
                                NameSpecifier(name="Type5"),
                            ]
                        ),
                        const=True,
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                    const=True,
                ),
                Method(
                    return_type=Type(
                        typename=PQName(
                            segments=[
                                NameSpecifier(name="Foo"),
                                NameSpecifier(name="Type6"),
                            ]
                        ),
                        volatile=True,
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(name="Foo"),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    operator="conversion",
                    const=True,
                ),
            ]
        )
    )


def test_template_conversion_operator_impl() -> None:
    content = """
      template <class T> ON_SimpleArray<T>::operator T *() {
        return (m_count > 0) ? m_a : 0;
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            method_impls=[
                Method(
                    return_type=Pointer(
                        ptr_to=Type(typename=PQName(segments=[NameSpecifier(name="T")]))
                    ),
                    name=PQName(
                        segments=[
                            NameSpecifier(
                                name="ON_SimpleArray",
                                specialization=TemplateSpecialization(
                                    args=[
                                        TemplateArgument(
                                            arg=Type(
                                                typename=PQName(
                                                    segments=[NameSpecifier(name="T")]
                                                )
                                            )
                                        )
                                    ]
                                ),
                            ),
                            NameSpecifier(name="operator"),
                        ]
                    ),
                    parameters=[],
                    has_body=True,
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="class", name="T")]
                    ),
                    operator="conversion",
                )
            ]
        )
    )


def test_free_operator() -> None:
    content = """
      std::ostream& operator<<(std::ostream& os, const MyDate& dt);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Reference(
                        ref_to=Type(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="std"),
                                    NameSpecifier(name="ostream"),
                                ]
                            )
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="operator<<")]),
                    parameters=[
                        Parameter(
                            type=Reference(
                                ref_to=Type(
                                    typename=PQName(
                                        segments=[
                                            NameSpecifier(name="std"),
                                            NameSpecifier(name="ostream"),
                                        ]
                                    )
                                )
                            ),
                            name="os",
                        ),
                        Parameter(
                            type=Reference(
                                ref_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="MyDate")]
                                    ),
                                    const=True,
                                )
                            ),
                            name="dt",
                        ),
                    ],
                    operator="<<",
                )
            ]
        )
    )
