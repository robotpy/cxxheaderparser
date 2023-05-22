# Note: testcases generated via `python -m cxxheaderparser.gentest`
from cxxheaderparser.simple import ClassScope
from cxxheaderparser.simple import NamespaceScope
from cxxheaderparser.simple import parse_string
from cxxheaderparser.simple import ParsedData
from cxxheaderparser.types import AnonymousName
from cxxheaderparser.types import ClassDecl
from cxxheaderparser.types import EnumDecl
from cxxheaderparser.types import Enumerator
from cxxheaderparser.types import Field
from cxxheaderparser.types import Function
from cxxheaderparser.types import FundamentalSpecifier
from cxxheaderparser.types import Method
from cxxheaderparser.types import NameSpecifier
from cxxheaderparser.types import PQName
from cxxheaderparser.types import TemplateDecl
from cxxheaderparser.types import TemplateTypeParam
from cxxheaderparser.types import Token
from cxxheaderparser.types import Type
from cxxheaderparser.types import Typedef
from cxxheaderparser.types import Value
from cxxheaderparser.types import Variable


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
                            segments=[NameSpecifier(name="C")],
                            classkey="class",
                        ),
                        doxygen="/// cls comment",
                    ),
                    fields=[
                        Field(
                            access="private",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")],
                                ),
                            ),
                            name="var_above",
                            doxygen="/// var above",
                        ),
                        Field(
                            access="private",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")],
                                ),
                            ),
                            name="var_after",
                            doxygen="/// var after",
                        ),
                    ],
                    methods=[
                        Method(
                            return_type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="void")],
                                ),
                            ),
                            name=PQName(segments=[NameSpecifier(name="fn")]),
                            parameters=[],
                            doxygen="/// member comment",
                            access="private",
                        ),
                    ],
                ),
            ],
        ),
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
                            segments=[NameSpecifier(name="C2")],
                            classkey="class",
                        ),
                        template=TemplateDecl(
                            params=[TemplateTypeParam(typekey="typename", name="T")],
                        ),
                        doxygen="/// template comment",
                    ),
                ),
            ],
        ),
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
                ),
            ],
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(
                            segments=[AnonymousName(id=1)],
                            classkey="enum",
                        ),
                    ),
                    name="Rino",
                ),
            ],
        ),
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
                        typename=PQName(segments=[FundamentalSpecifier(name="void")]),
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[],
                    doxygen="/// fn comment",
                ),
            ],
        ),
    )


def test_doxygen_fn_cstyle1() -> None:
    content = """
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
                        typename=PQName(segments=[FundamentalSpecifier(name="void")]),
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[],
                    doxygen="/**\n* fn comment\n*/",
                ),
            ],
        ),
    )


def test_doxygen_fn_cstyle2() -> None:
    content = """
      /*!
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
                        typename=PQName(segments=[FundamentalSpecifier(name="void")]),
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[],
                    doxygen="/*!\n* fn comment\n*/",
                ),
            ],
        ),
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
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    value=Value(tokens=[Token(value="0")]),
                    doxygen="/// var comment",
                ),
            ],
        ),
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
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    value=Value(tokens=[Token(value="0")]),
                    doxygen="/// var2 comment",
                ),
            ],
        ),
    )


def test_doxygen_multiple_variables() -> None:
    content = """
      int x; /// this is x
      int y; /// this is y
             /// this is also y
      int z; /// this is z
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    doxygen="/// this is x",
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="y")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    doxygen="/// this is y\n/// this is also y",
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="z")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    doxygen="/// this is z",
                ),
            ],
        ),
    )


def test_doxygen_namespace() -> None:
    content = """
      /**
       * x is a mysterious namespace
       */
      namespace x {}

      /**
       * c is also a mysterious namespace
       */
      namespace a::b::c {}
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "x": NamespaceScope(
                    name="x",
                    doxygen="/**\n* x is a mysterious namespace\n*/",
                ),
                "a": NamespaceScope(
                    name="a",
                    namespaces={
                        "b": NamespaceScope(
                            name="b",
                            namespaces={
                                "c": NamespaceScope(
                                    name="c",
                                    doxygen="/**\n* c is also a mysterious namespace\n*/",
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    )


def test_doxygen_declspec() -> None:
    content = """
      /// declspec comment
      __declspec(thread) int i = 1;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="i")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    value=Value(tokens=[Token(value="1")]),
                    doxygen="/// declspec comment",
                ),
            ],
        ),
    )


def test_doxygen_attribute() -> None:
    content = """
      /// hasattr comment
      [[nodiscard]]
      int hasattr();
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")]),
                    ),
                    name=PQName(segments=[NameSpecifier(name="hasattr")]),
                    parameters=[],
                    doxygen="/// hasattr comment",
                ),
            ],
        ),
    )
