from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    Method,
    NamespaceScope,
    ParsedData,
    Variable,
    parse_string,
)
from cxxheaderparser.types import (
    BaseClass,
    DecltypeSpecifier,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Parameter,
    TemplateArgument,
    TemplateDecl,
    TemplateSpecialization,
    TemplateTypeParam,
    Token,
    Type,
)


def test_base_initializer_parentheses() -> None:
    content = """
        template<class T> struct A { A(int); }; struct B : A<decltype(0)> { B() : A<decltype(0)>(0) {} void after(); }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="A")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="class", name="T")]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="A")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    )
                                )
                            ],
                            access="public",
                            constructor=True,
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="B")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="A",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    DecltypeSpecifier(
                                                                        tokens=[
                                                                            Token(
                                                                                value="0"
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="B")]),
                            parameters=[],
                            has_body=True,
                            access="public",
                            constructor=True,
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="after")]),
                            parameters=[],
                            access="public",
                        ),
                    ],
                ),
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


def test_base_initializer_braces() -> None:
    content = """
        template<class T> struct A { A(int); }; struct B : A<decltype(0)> { B() : A<decltype(0)>{0} {} void after(); }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="A")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="class", name="T")]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="A")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    )
                                )
                            ],
                            access="public",
                            constructor=True,
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="B")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="A",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    DecltypeSpecifier(
                                                                        tokens=[
                                                                            Token(
                                                                                value="0"
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="B")]),
                            parameters=[],
                            has_body=True,
                            access="public",
                            constructor=True,
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="after")]),
                            parameters=[],
                            access="public",
                        ),
                    ],
                ),
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


def test_base_initializer_nested_parentheses() -> None:
    content = """
        template<class T> struct A { A(int); }; struct B : A<decltype(0)> { B() : A<decltype((0))>(0) {} void after(); }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="A")], classkey="struct"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="class", name="T")]
                        ),
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="A")]),
                            parameters=[
                                Parameter(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    )
                                )
                            ],
                            access="public",
                            constructor=True,
                        )
                    ],
                ),
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="B")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(
                                    segments=[
                                        NameSpecifier(
                                            name="A",
                                            specialization=TemplateSpecialization(
                                                args=[
                                                    TemplateArgument(
                                                        arg=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    DecltypeSpecifier(
                                                                        tokens=[
                                                                            Token(
                                                                                value="0"
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="B")]),
                            parameters=[],
                            has_body=True,
                            access="public",
                            constructor=True,
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="after")]),
                            parameters=[],
                            access="public",
                        ),
                    ],
                ),
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
