# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    AnonymousName,
    Array,
    BaseClass,
    ClassDecl,
    EnumDecl,
    Enumerator,
    Field,
    ForwardDecl,
    Function,
    FundamentalSpecifier,
    Method,
    MoveReference,
    NameSpecifier,
    Operator,
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
    Typedef,
    UsingDecl,
    Value,
    Variable,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_doxygen_class() -> None:
    content = """
      // clang-format off
      
      /// cls comment
      class
      C {
          /// member comment
          void fn();
      
          /// var above
          int var_above;
      
          int var_after; /// var after
      };
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C")], classkey="class"
                        ),
                        doxygen="/// cls comment",
                    ),
                    fields=[
                        Field(
                            access="private",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="var_above",
                            doxygen="/// var above",
                        ),
                        Field(
                            access="private",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            name="var_after",
                            doxygen="/// var after",
                        ),
                    ],
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")]
                                )
                            ),
                            name=PQName(segments=[NameSpecifier(name="fn")]),
                            parameters=[],
                            doxygen="/// member comment",
                            access="private",
                        )
                    ],
                )
            ]
        )
    )


def test_doxygen_class_template() -> None:
    content = """
      // clang-format off
      
      /// template comment
      template <typename T>
      class C2 {};
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="C2")], classkey="class"
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="T")]
                        ),
                        doxygen="/// template comment",
                    )
                )
            ]
        )
    )


def test_doxygen_enum() -> None:
    content = """
      // clang-format off
      
      ///
      /// @brief Rino Numbers, not that that means anything
      ///
      typedef enum
      {
          RI_ZERO, /// item zero
          RI_ONE,  /** item one */
          RI_TWO,   //!< item two
          RI_THREE,
          /// item four
          RI_FOUR,
      } Rino;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            enums=[
                EnumDecl(
                    typename=PQName(segments=[AnonymousName(id=1)], classkey="enum"),
                    values=[
                        Enumerator(name="RI_ZERO", doxygen="/// item zero"),
                        Enumerator(name="RI_ONE", doxygen="/** item one */"),
                        Enumerator(name="RI_TWO", doxygen="//!< item two"),
                        Enumerator(name="RI_THREE"),
                        Enumerator(name="RI_FOUR", doxygen="/// item four"),
                    ],
                    doxygen="///\n/// @brief Rino Numbers, not that that means anything\n///",
                )
            ],
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(segments=[AnonymousName(id=1)], classkey="enum")
                    ),
                    name="Rino",
                )
            ],
        )
    )


def test_doxygen_fn_3slash() -> None:
    content = """
      // clang-format off
      
      /// fn comment
      void
      fn();
      
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
                    parameters=[],
                    doxygen="/// fn comment",
                )
            ]
        )
    )


def test_doxygen_fn_cstyle() -> None:
    content = """
      // clang-format off
      
      /**
       * fn comment
       */
      void
      fn();
      
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
                    parameters=[],
                    doxygen="/**\n* fn comment\n*/",
                )
            ]
        )
    )


def test_doxygen_var_above() -> None:
    content = """
      // clang-format off
      
      
      /// var comment
      int
      v1 = 0;
      
      
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="v1")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="0")]),
                    doxygen="/// var comment",
                )
            ]
        )
    )


def test_doxygen_var_after() -> None:
    content = """
      // clang-format off
      
      int
      v2 = 0; /// var2 comment
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="v2")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="0")]),
                    doxygen="/// var2 comment",
                )
            ]
        )
    )
