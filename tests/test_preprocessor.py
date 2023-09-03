import pathlib

from cxxheaderparser.options import ParserOptions
from cxxheaderparser.preprocessor import make_pcpp_preprocessor
from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_file, parse_string
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Token,
    Type,
    Value,
    Variable,
)


def test_basic_preprocessor() -> None:
    content = """
      #define X 1
      int x = X;
    """
    options = ParserOptions(preprocessor=make_pcpp_preprocessor())
    data = parse_string(content, cleandoc=True, options=options)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="1")]),
                )
            ]
        )
    )


def test_preprocessor_omit_content(tmp_path: pathlib.Path) -> None:
    """Ensure that content in other headers is omitted"""
    h_content = '#include "t2.h"' "\n" "int x = X;\n"
    h2_content = "#define X 2\n" "int omitted = 1;\n"

    with open(tmp_path / "t1.h", "w") as fp:
        fp.write(h_content)

    with open(tmp_path / "t2.h", "w") as fp:
        fp.write(h2_content)

    options = ParserOptions(preprocessor=make_pcpp_preprocessor())
    data = parse_file(tmp_path / "t1.h", options=options)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="2")]),
                )
            ]
        )
    )


def test_preprocessor_encoding(tmp_path: pathlib.Path) -> None:
    """Ensure we can handle alternate encodings"""
    h_content = b"// \xa9 2023 someone\n" b'#include "t2.h"' b"\n" b"int x = X;\n"

    h2_content = b"// \xa9 2023 someone\n" b"#define X 3\n" b"int omitted = 1;\n"

    with open(tmp_path / "t1.h", "wb") as fp:
        fp.write(h_content)

    with open(tmp_path / "t2.h", "wb") as fp:
        fp.write(h2_content)

    options = ParserOptions(preprocessor=make_pcpp_preprocessor(encoding="cp1252"))
    data = parse_file(tmp_path / "t1.h", options=options, encoding="cp1252")

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="x")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    value=Value(tokens=[Token(value="3")]),
                )
            ]
        )
    )
