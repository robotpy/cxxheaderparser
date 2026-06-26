import pytest

from cxxheaderparser.errors import CxxParseError
from cxxheaderparser.lexer import LexToken, LexerTokenStream
from cxxheaderparser.parserstate import ParsedTypeModifiers


def _token(value: str) -> LexToken:
    stream = LexerTokenStream(None, f"{value} int x;")
    return stream.token()


def test_parsed_type_modifiers_validation_uses_explicit_fields() -> None:
    mods = ParsedTypeModifiers(mutable=_token("mutable"), virtual=_token("virtual"))

    with pytest.raises(CxxParseError, match="test: unexpected 'mutable'"):
        mods.validate(var_ok=False, meth_ok=True, msg="test")

    with pytest.raises(CxxParseError, match="test: unexpected 'virtual'"):
        mods.validate(var_ok=True, meth_ok=False, msg="test")

    mods = ParsedTypeModifiers(static=_token("static"))
    with pytest.raises(CxxParseError, match="test: unexpected 'static'"):
        mods.validate(var_ok=False, meth_ok=False, msg="test")
