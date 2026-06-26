import typing

from cxxheaderparser.lexer import LexerTokenStream
from cxxheaderparser.simple import Include, NamespaceScope, ParsedData, parse_string


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
