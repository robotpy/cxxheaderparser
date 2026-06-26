import typing

from cxxheaderparser.lexer import LexerTokenStream
from cxxheaderparser.simple import (
    ClassScope,
    Include,
    NamespaceScope,
    ParsedData,
    parse_string,
)
from cxxheaderparser.types import (
    Array,
    ClassDecl,
    EnumDecl,
    Enumerator,
    Field,
    Function,
    FundamentalSpecifier,
    Method,
    NameSpecifier,
    Parameter,
    PQName,
    TemplateDecl,
    TemplateNonTypeParam,
    TemplateTypeParam,
    Token,
    Type,
    Value,
    Variable,
)


def _token_pairs(content: str) -> typing.List[typing.Tuple[str, str]]:
    stream = LexerTokenStream("<str>", content)
    pairs = []

    while True:
        tok = stream.token_eof_ok()
        if tok is None:
            break
        pairs.append((tok.type, tok.value))

    return pairs


def test_digraph_tokens_normalize_to_brackets_and_braces() -> None:
    assert _token_pairs("struct S <% int a<:3:>; %>;") == [
        ("struct", "struct"),
        ("NAME", "S"),
        ("{", "{"),
        ("int", "int"),
        ("NAME", "a"),
        ("[", "["),
        ("INT_CONST_DEC", "3"),
        ("]", "]"),
        (";", ";"),
        ("}", "}"),
        (";", ";"),
    ]


def test_digraph_double_square_brackets_normalize_to_attribute_tokens() -> None:
    assert _token_pairs("<:<:deprecated:>:> int x;") == [
        ("DBL_LBRACKET", "[["),
        ("NAME", "deprecated"),
        ("DBL_RBRACKET", "]]"),
        ("int", "int"),
        ("NAME", "x"),
        (";", ";"),
    ]


def test_less_colon_colon_stays_template_less_and_scope_operator() -> None:
    assert _token_pairs("std::vector<::Foo> value;") == [
        ("NAME", "std"),
        ("DBL_COLON", "::"),
        ("NAME", "vector"),
        ("<", "<"),
        ("DBL_COLON", "::"),
        ("NAME", "Foo"),
        (">", ">"),
        ("NAME", "value"),
        (";", ";"),
    ]


def test_parser_accepts_digraph_braces_and_array_bounds() -> None:
    assert parse_string("struct S <% int a<:3:>; %>;") == parse_string(
        "struct S { int a[3]; };"
    )


def test_parser_accepts_digraph_attribute_brackets() -> None:
    assert parse_string("<:<:deprecated:>:> int x;") == parse_string(
        "[[deprecated]] int x;"
    )


def test_digraph_include_directive_is_normalized() -> None:
    assert parse_string("%:include <vector>") == ParsedData(
        namespace=NamespaceScope(), includes=[Include(filename="<vector>")]
    )


def test_digraph_line_directive_is_normalized_for_locations() -> None:
    data = parse_string('%: 42 "generated.hpp"\nint value;')

    assert data == parse_string('# 42 "generated.hpp"\nint value;')


def test_canonical_tokens_unaffected() -> None:
    content = """
        namespace ns {
            struct Foo {
                int arr[5];
            };
        }
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "ns": NamespaceScope(
                    name="ns",
                    classes=[
                        ClassScope(
                            class_decl=ClassDecl(
                                typename=PQName(
                                    segments=[NameSpecifier(name="Foo")],
                                    classkey="struct",
                                )
                            ),
                            fields=[
                                Field(
                                    access="public",
                                    type=Array(
                                        array_of=Type(
                                            typename=PQName(
                                                segments=[
                                                    FundamentalSpecifier(name="int")
                                                ]
                                            )
                                        ),
                                        size=Value(tokens=[Token(value="5")]),
                                    ),
                                    name="arr",
                                )
                            ],
                        )
                    ],
                )
            }
        )
    )


def test_digraph_array_and_brace() -> None:
    content = """
        struct Grid
        <%
            float data<:4:>;
        %>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Grid")], classkey="struct"
                        )
                    ),
                    fields=[
                        Field(
                            access="public",
                            type=Array(
                                array_of=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="float")]
                                    )
                                ),
                                size=Value(tokens=[Token(value="4")]),
                            ),
                            name="data",
                        )
                    ],
                )
            ]
        )
    )


def test_digraph_array_subscript() -> None:
    content = """
        int arr<:10:>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="arr")]),
                    type=Array(
                        array_of=Type(
                            typename=PQName(segments=[FundamentalSpecifier(name="int")])
                        ),
                        size=Value(tokens=[Token(value="10")]),
                    ),
                )
            ]
        )
    )


def test_digraph_brace_open_close_function() -> None:
    content = """
        #include <iostream>
        int main()
        <%
            std::cout << "Hello, World!" << std::endl;
            return 0;
        %>
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="main")]),
                    parameters=[],
                    has_body=True,
                )
            ]
        ),
        includes=[Include(filename="<iostream>")],
    )


def test_digraph_class_with_methods() -> None:
    content = """
        class MyClass
        <%
        public:
            MyClass();
            ~MyClass();
            int getValue() const;
        %>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="MyClass")], classkey="class"
                        )
                    ),
                    methods=[
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="MyClass")]),
                            parameters=[],
                            access="public",
                            constructor=True,
                        ),
                        Method(
                            return_type=None,
                            name=PQName(segments=[NameSpecifier(name="~MyClass")]),
                            parameters=[],
                            access="public",
                            destructor=True,
                        ),
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="getValue")]),
                            parameters=[],
                            access="public",
                            const=True,
                        ),
                    ],
                )
            ]
        )
    )


def test_digraph_enum() -> None:
    content = """
        enum Color
        <%
            Red,
            Green,
            Blue
        %>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            enums=[
                EnumDecl(
                    typename=PQName(
                        segments=[NameSpecifier(name="Color")], classkey="enum"
                    ),
                    values=[
                        Enumerator(name="Red"),
                        Enumerator(name="Green"),
                        Enumerator(name="Blue"),
                    ],
                )
            ]
        )
    )


def test_digraph_mixed_braces() -> None:
    content = """
        namespace ns
        <%
            struct Foo {
                int a;
            };
        %>
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "ns": NamespaceScope(
                    name="ns",
                    classes=[
                        ClassScope(
                            class_decl=ClassDecl(
                                typename=PQName(
                                    segments=[NameSpecifier(name="Foo")],
                                    classkey="struct",
                                )
                            ),
                            fields=[
                                Field(
                                    access="public",
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    name="a",
                                )
                            ],
                        )
                    ],
                )
            }
        )
    )


def test_digraph_namespace_body() -> None:
    content = """
        namespace myns
        <%
            int value;
        %>
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "myns": NamespaceScope(
                    name="myns",
                    variables=[
                        Variable(
                            name=PQName(segments=[NameSpecifier(name="value")]),
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                        )
                    ],
                )
            }
        )
    )


def test_digraph_nested_braces() -> None:
    content = """
        namespace outer
        <%
            struct Inner
            <%
                int val;
            %>;
        %>
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "outer": NamespaceScope(
                    name="outer",
                    classes=[
                        ClassScope(
                            class_decl=ClassDecl(
                                typename=PQName(
                                    segments=[NameSpecifier(name="Inner")],
                                    classkey="struct",
                                )
                            ),
                            fields=[
                                Field(
                                    access="public",
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    name="val",
                                )
                            ],
                        )
                    ],
                )
            }
        )
    )


def test_digraph_struct_body() -> None:
    content = """
        struct Point
        <%
            int x;
            int y;
        %>;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Point")], classkey="struct"
                        )
                    ),
                    fields=[
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="x",
                        ),
                        Field(
                            access="public",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="y",
                        ),
                    ],
                )
            ]
        )
    )


def test_percent_operator_unaffected() -> None:
    content = """
        void fn(int x = 10 % 3);
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
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="x",
                            default=Value(
                                tokens=[
                                    Token(value="10"),
                                    Token(value="%"),
                                    Token(value="3"),
                                ]
                            ),
                        )
                    ],
                )
            ]
        )
    )


def test_shift_left_unaffected() -> None:
    content = """
        template <typename T>
        void fn(T x);
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
                            type=Type(
                                typename=PQName(segments=[NameSpecifier(name="T")])
                            ),
                            name="x",
                        )
                    ],
                    template=TemplateDecl(
                        params=[TemplateTypeParam(typekey="typename", name="T")]
                    ),
                )
            ]
        )
    )


def test_template_angle_brackets_unaffected() -> None:
    content = """
        template <typename T, int N>
        struct Container
        {
            T data[N];
        };
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="Container")],
                            classkey="struct",
                        ),
                        template=TemplateDecl(
                            params=[
                                TemplateTypeParam(typekey="typename", name="T"),
                                TemplateNonTypeParam(
                                    type=Type(
                                        typename=PQName(
                                            segments=[FundamentalSpecifier(name="int")]
                                        )
                                    ),
                                    name="N",
                                ),
                            ]
                        ),
                    ),
                    fields=[
                        Field(
                            access="public",
                            type=Array(
                                array_of=Type(
                                    typename=PQName(segments=[NameSpecifier(name="T")])
                                ),
                                size=Value(tokens=[Token(value="N")]),
                            ),
                            name="data",
                        )
                    ],
                )
            ]
        )
    )
