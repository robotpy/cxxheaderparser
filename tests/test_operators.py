# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    ClassDecl,
    FundamentalSpecifier,
    NameSpecifier,
    Operator,
    PQName,
    Parameter,
    Reference,
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
                        Operator(
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
