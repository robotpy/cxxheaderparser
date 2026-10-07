import pytest

from cxxheaderparser.lexer import LexerTokenStream, Location
from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    Pointer,
    PQName,
    Token,
    Type,
    Value,
    Variable,
)


# Generated from C++ headers via `python -m cxxheaderparser.gentest`.
def test_multiline_raw_string_header() -> None:
    content = """
        const char* s = R"(
        )";
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="s")]),
                    type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="char")]
                            ),
                            const=True,
                        )
                    ),
                    value=Value(tokens=[Token(value='R"(\n)"')]),
                )
            ]
        )
    )


def test_prefixed_raw_string_delimiter_header() -> None:
    content = """
        const char16_t* message = uR"tag(first "quoted"
        )"
        last)tag";
        int next;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="message")]),
                    type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="char16_t")]
                            ),
                            const=True,
                        )
                    ),
                    value=Value(
                        tokens=[Token(value='uR"tag(first "quoted"\n)"\nlast)tag"')]
                    ),
                ),
                Variable(
                    name=PQName(segments=[NameSpecifier(name="next")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                ),
            ]
        )
    )


@pytest.mark.parametrize(
    "literal",
    [
        'R"()"',
        'R"(\n)"',
        'R"(first\nsecond\nthird)"',
        'R"tag(first\n)wrong"\n)"\nlast)tag"',
        'R"(quotes: "hello", backslashes: \\q\\n\n/* not a comment */)"',
        'R".*[tag](\n)other"\n).*[tag]"',
        'R"abcdefghijklmnop(\n)abcdefghijklmnop"',
    ],
)
def test_raw_string_initializer(literal: str) -> None:
    data = parse_string(f"const char* s = {literal};")

    assert data == ParsedData(
        namespace=NamespaceScope(
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="s")]),
                    type=Pointer(
                        ptr_to=Type(
                            typename=PQName(
                                segments=[FundamentalSpecifier(name="char")]
                            ),
                            const=True,
                        )
                    ),
                    value=Value(tokens=[Token(value=literal)]),
                )
            ]
        )
    )


@pytest.mark.parametrize(
    "prefix, token_type",
    [
        ("", "STRING_LITERAL"),
        ("L", "WSTRING_LITERAL"),
        ("u8", "U8STRING_LITERAL"),
        ("u", "U16STRING_LITERAL"),
        ("U", "U32STRING_LITERAL"),
    ],
)
def test_raw_string_prefix_and_token_boundaries(prefix: str, token_type: str) -> None:
    literal = prefix + 'R"(\n)"'
    stream = LexerTokenStream("<str>", literal + literal + ' "ordinary"')

    for _ in range(2):
        token = stream.token()
        assert (token.type, token.value) == (token_type, literal)
    token = stream.token()
    assert (token.type, token.value) == ("STRING_LITERAL", '"ordinary"')
    assert stream.token_eof_ok() is None


def test_raw_string_user_defined_literal() -> None:
    stream = LexerTokenStream("<str>", 'R"(\n)"_suffix')

    token = stream.token()
    assert (token.type, token.value) == ("UD_STRING_LITERAL", 'R"(\n)"_suffix')
    assert stream.token_eof_ok() is None


def test_raw_string_preserves_following_token_location() -> None:
    stream = LexerTokenStream("test.h", 'R"(first\nsecond\nthird)";\nint next;')

    assert stream.token().value == 'R"(first\nsecond\nthird)"'
    semicolon = stream.token()
    assert (semicolon.value, semicolon.location) == (";", Location("test.h", 3))
    next_token = stream.token()
    assert (next_token.value, next_token.location) == ("int", Location("test.h", 4))
