# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    BaseClass,
    ClassDecl,
    Function,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Parameter,
    Token,
    Type,
    Value,
    Variable,
)
from cxxheaderparser.simple import (
    ClassScope,
    Include,
    NamespaceScope,
    Pragma,
    parse_string,
    ParsedData,
    Define,
)

#
# minimal preprocessor support
#


def test_define() -> None:
    content = """
        #define simple
        #define complex(thing) stuff(thing)
        #  define spaced
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        defines=[
            Define(content="simple"),
            Define(content="complex(thing) stuff(thing)"),
            Define(content="spaced"),
        ],
    )


def test_includes() -> None:
    content = """
        #include <global.h>
        #include "local.h"
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(includes=[Include("<global.h>"), Include('"local.h"')])


def test_pragma() -> None:
    content = """

        #pragma once

    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(pragmas=[Pragma(content="once")])


#
# extern "C"
#


def test_extern_c() -> None:
    content = """
      extern "C" {
      int x;
      };
      
      int y;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="y")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ]
        )
    )


def test_misc_extern_inline() -> None:
    content = """
      extern "C++" {
      inline HAL_Value HAL_GetSimValue(HAL_SimValueHandle handle) {
        HAL_Value v;
        return v;
      }
      } // extern "C++"
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="HAL_Value")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="HAL_GetSimValue")]),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[NameSpecifier(name="HAL_SimValueHandle")]
                                )
                            ),
                            name="handle",
                        )
                    ],
                    inline=True,
                    has_body=True,
                )
            ]
        )
    )


#
# Misc
#


def test_static_assert_1() -> None:
    # static_assert should be ignored
    content = """
        static_assert(x == 1);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData()


def test_static_assert_2() -> None:
    # static_assert should be ignored
    content = """
        static_assert(sizeof(int) == 4, 
                      "integer size is wrong"
                      "for some reason");
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData()


def test_comment_eof() -> None:
    content = """
      namespace a {} // namespace a"""
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(namespaces={"a": NamespaceScope(name="a")})
    )


def test_final() -> None:
    content = """
      // ok here
      int fn(const int final);
      
      // ok here
      int final = 2;
      
      // but it's a keyword here
      struct B final : A {};
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="B")], classkey="struct"
                        ),
                        bases=[
                            BaseClass(
                                access="public",
                                typename=PQName(segments=[NameSpecifier(name="A")]),
                            )
                        ],
                        final=True,
                    )
                )
            ],
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="fn")]),
                    parameters=[
                        Parameter(
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                ),
                                const=True,
                            ),
                            name="final",
                        )
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="final")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="2")]),
                )
            ],
        )
    )
