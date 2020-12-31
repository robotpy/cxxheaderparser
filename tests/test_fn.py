# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    Array,
    AutoSpecifier,
    Function,
    FunctionType,
    FundamentalSpecifier,
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
)
from cxxheaderparser.simple import (
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_fn_returns_class():
    content = """
      class X *fn1();
      struct Y fn2();
      enum E fn3();
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[NameSpecifier(name="X")], classkey="class"
                            )
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn1")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(
                            segments=[NameSpecifier(name="Y")], classkey="struct"
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn2")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(
                            segments=[NameSpecifier(name="E")], classkey="enum"
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn3")]),
                    parameters=[],
                ),
            ]
        )
    )


def test_fn_pointer_params():
    content = """
      int fn1(int *);
      int fn2(int *p);
      int fn3(int(*p));
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn1")]),
                    parameters=[
                        Parameter(
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                )
                            ),
                        )
                    ],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn2")]),
                    parameters=[
                        Parameter(
                            name="p",
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                )
                            ),
                        )
                    ],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn3")]),
                    parameters=[
                        Parameter(
                            name="p",
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                )
                            ),
                        )
                    ],
                ),
            ]
        )
    )


def test_fn_void_is_no_params():
    content = """
      int fn(void);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[],
                )
            ]
        )
    )


def test_fn_array_param():
    content = """
      void fn(int array[]);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[
                        Parameter(
                            name="array",
                            type=Array(
                                array_of=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                ),
                                size=None,
                            ),
                        )
                    ],
                )
            ]
        )
    )


def test_fn_weird_refs():
    content = """
      int aref(int(&x));
      void ptr_ref(int(*&name));
      void ref_to_array(int (&array)[]);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="aref")]),
                    parameters=[
                        Parameter(
                            name="x",
                            type=Reference(
                                ref_to=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                )
                            ),
                        )
                    ],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="ptr_ref")]),
                    parameters=[
                        Parameter(
                            name="name",
                            type=Reference(
                                ref_to=Pointer(
                                    ptr_to=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    )
                                )
                            ),
                        )
                    ],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="ref_to_array")]),
                    parameters=[
                        Parameter(
                            name="array",
                            type=Reference(
                                ref_to=Array(
                                    array_of=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    size=None,
                                )
                            ),
                        )
                    ],
                ),
            ]
        )
    )


def test_fn_too_many_parens():
    content = """
      int fn1(int (x));
      void (fn2 (int (*const (name))));
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn1")]),
                    parameters=[
                        Parameter(
                            name="x",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                        )
                    ],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn2")]),
                    parameters=[
                        Parameter(
                            name="name",
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="int")]
                                    )
                                ),
                                const=True,
                            ),
                        )
                    ],
                ),
            ]
        )
    )


# TODO calling conventions
"""
void __stdcall fn();
void (__stdcall * fn)
"""


def test_fn_same_line():
    # multiple functions on the same line
    content = """
      void fn1(), fn2();
      void *fn3(), fn4();
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn1")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn2")]),
                    parameters=[],
                ),
                Function(
                    return_type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="void")]
                            )
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn3")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn4")]),
                    parameters=[],
                ),
            ]
        )
    )


def test_fn_auto_template():
    content = """
      template<class T, class U>
      auto add(T t, U u) { return t + u; }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(typename=PQName(segments=[AutoSpecifier()])),
                    name=PQName(segments=[NameSpecifier(name="add")]),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(segments=[NameSpecifier(name="T")])
                            ),
                            name="t",
                        ),
                        Parameter(
                            type=Type(
                                typename=PQName(segments=[NameSpecifier(name="U")])
                            ),
                            name="u",
                        ),
                    ],
                    has_body=True,
                    template=TemplateDecl(
                        params=[
                            TemplateTypeParam(typekey="class", name="T"),
                            TemplateTypeParam(typekey="class", name="U"),
                        ]
                    ),
                )
            ]
        )
    )


def test_fn_template_ptr():
    content = """
      std::vector<Pointer *> *fn(std::vector<Pointer *> *ps);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[
                                    NameSpecifier(name="std"),
                                    NameSpecifier(
                                        name="vector",
                                        specialization=TemplateSpecialization(
                                            args=[
                                                TemplateArgument(
                                                    arg=Pointer(
                                                        ptr_to=Type(
                                                            typename=PQName(
                                                                segments=[
                                                                    NameSpecifier(
                                                                        name="Pointer"
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    )
                                                )
                                            ]
                                        ),
                                    ),
                                ]
                            )
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[
                        Parameter(
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[
                                            NameSpecifier(name="std"),
                                            NameSpecifier(
                                                name="vector",
                                                specialization=TemplateSpecialization(
                                                    args=[
                                                        TemplateArgument(
                                                            arg=Pointer(
                                                                ptr_to=Type(
                                                                    typename=PQName(
                                                                        segments=[
                                                                            NameSpecifier(
                                                                                name="Pointer"
                                                                            )
                                                                        ]
                                                                    )
                                                                )
                                                            )
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ]
                                    )
                                )
                            ),
                            name="ps",
                        )
                    ],
                )
            ]
        )
    )


def test_fn_with_impl():
    content = """
      // clang-format off
      void termite(void)
      {
          return ((structA*) (Func())->element);
      }
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="void")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="termite")]),
                    parameters=[],
                    has_body=True,
                )
            ]
        )
    )


def test_fn_return_std_function():
    content = """
      std::function<void(int)> fn();
    """
    data1 = parse_string(content, cleandoc=True)

    content = """
      std::function<void((int))> fn();
    """
    data2 = parse_string(content, cleandoc=True)

    expected = ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
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
                                                    parameters=[
                                                        Parameter(
                                                            type=Type(
                                                                typename=PQName(
                                                                    segments=[
                                                                        FundamentalSpecifier(
                                                                            name="int"
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        )
                                                    ],
                                                )
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        )
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[],
                )
            ]
        )
    )

    assert data1 == expected
    assert data2 == expected
