# Note: testcases generated via `python -m cxxheaderparser.gentest`
import re

import pytest

from cxxheaderparser.errors import CxxParseError
from cxxheaderparser.simple import NamespaceScope
from cxxheaderparser.simple import parse_string
from cxxheaderparser.simple import ParsedData
from cxxheaderparser.types import ForwardDecl
from cxxheaderparser.types import FundamentalSpecifier
from cxxheaderparser.types import NamespaceAlias
from cxxheaderparser.types import NameSpecifier
from cxxheaderparser.types import PQName
from cxxheaderparser.types import Token
from cxxheaderparser.types import Type
from cxxheaderparser.types import Value
from cxxheaderparser.types import Variable


def test_dups_in_different_ns() -> None:
    content = """

      namespace {
      int x = 4;
      }

      int x = 5;

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
                    value=Value(tokens=[Token(value="5")]),
                ),
            ],
            namespaces={
                "": NamespaceScope(
                    variables=[
                        Variable(
                            name=PQName(segments=[NameSpecifier(name="x")]),
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")],
                                ),
                            ),
                            value=Value(tokens=[Token(value="4")]),
                        ),
                    ],
                ),
            },
        ),
    )


def test_correct_ns() -> None:
    content = """
      namespace a::b::c {
        int i1;
      }

      namespace a {
        namespace b {
          namespace c {
            int i2;
          }
        }
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "a": NamespaceScope(
                    name="a",
                    namespaces={
                        "b": NamespaceScope(
                            name="b",
                            namespaces={
                                "c": NamespaceScope(
                                    name="c",
                                    variables=[
                                        Variable(
                                            name=PQName(
                                                segments=[NameSpecifier(name="i1")],
                                            ),
                                            type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(
                                                            name="int",
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                        Variable(
                                            name=PQName(
                                                segments=[NameSpecifier(name="i2")],
                                            ),
                                            type=Type(
                                                typename=PQName(
                                                    segments=[
                                                        FundamentalSpecifier(
                                                            name="int",
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    )


def test_inline_namespace() -> None:
    content = """
      namespace Lib {
        inline namespace Lib_1 {
          class A;
        }
      }
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            namespaces={
                "Lib": NamespaceScope(
                    name="Lib",
                    namespaces={
                        "Lib_1": NamespaceScope(
                            name="Lib_1",
                            inline=True,
                            forward_decls=[
                                ForwardDecl(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="A")],
                                        classkey="class",
                                    ),
                                ),
                            ],
                        ),
                    },
                ),
            },
        ),
    )


def test_invalid_inline_namespace() -> None:
    content = """
      inline namespace a::b {}
    """
    err = "<str>:1: parse error evaluating 'inline': a nested namespace definition cannot be inline"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_string(content, cleandoc=True)


def test_ns_alias() -> None:
    content = """
      namespace ANS = my::ns;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            ns_alias=[NamespaceAlias(alias="ANS", names=["my", "ns"])],
        ),
    )


def test_ns_alias_global() -> None:
    content = """
      namespace ANS = ::my::ns;
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            ns_alias=[NamespaceAlias(alias="ANS", names=["::", "my", "ns"])],
        ),
    )
