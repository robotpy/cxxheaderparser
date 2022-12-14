import contextlib
from collections import deque
import re
import typing
import sys

from ._ply import lex
from ._ply.lex import TOKEN

from .errors import CxxParseError


class LexError(CxxParseError):
    pass


if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    Protocol = object

_line_re = re.compile(r'^#line (\d+) "(.*)"')
_multicomment_re = re.compile("\n[\\s]+\\*")


class Location(typing.NamedTuple):
    """
    Location that something was found at, takes #line directives into account
    """

    filename: str
    lineno: int


class LexToken(Protocol):
    """
    Token as emitted by PLY and modified by our lexer
    """

    #: Lexer type for this token
    type: str

    #: Raw value for this token
    value: str

    lineno: int
    lexpos: int

    #: Location token was found at
    location: Location

    #: private
    lexer: "Lexer"


PhonyEnding: LexToken = lex.LexToken()  # type: ignore
PhonyEnding.type = "PLACEHOLDER"
PhonyEnding.value = ""
PhonyEnding.lineno = 0
PhonyEnding.lexpos = 0


class Lexer:
    """
    This lexer is a combination of pieces from the PLY lexers that CppHeaderParser
    and pycparser have.
    """

    keywords = {
        "__attribute__",
        "alignas",
        "alignof",
        "asm",
        "auto",
        "bool",
        "break",
        "case",
        "catch",
        "char",
        "char8_t",
        "char16_t",
        "char32_t",
        "class",
        "const",
        "constexpr",
        "const_cast",
        "continue",
        "decltype",
        "__declspec",
        "default",
        "delete",
        "do",
        "double",
        "dynamic_cast",
        "else",
        "enum",
        "explicit",
        "export",
        "extern",
        "false",
        "final",
        "float",
        "for",
        "friend",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "mutable",
        "namespace",
        "new",
        "noexcept",
        "nullptr",
        "nullptr_t",  # not a keyword, but makes things easier
        "operator",
        "private",
        "protected",
        "public",
        "register",
        "reinterpret_cast",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "static_assert",
        "static_cast",
        "struct",
        "switch",
        "template",
        "this",
        "thread_local",
        "throw",
        "true",
        "try",
        "typedef",
        "typeid",
        "typename",
        "union",
        "unsigned",
        "using",
        "virtual",
        "void",
        "volatile",
        "wchar_t",
        "while",
    }

    tokens = [
        # constants
        "FLOAT_CONST",
        "HEX_FLOAT_CONST",
        "INT_CONST_HEX",
        "INT_CONST_BIN",
        "INT_CONST_OCT",
        "INT_CONST_DEC",
        "INT_CONST_CHAR",
        "CHAR_CONST",
        "WCHAR_CONST",
        "U8CHAR_CONST",
        "U16CHAR_CONST",
        "U32CHAR_CONST",
        # String literals
        "STRING_LITERAL",
        "WSTRING_LITERAL",
        "U8STRING_LITERAL",
        "U16STRING_LITERAL",
        "U32STRING_LITERAL",
        #
        "NAME",
        # Comments
        "COMMENT_SINGLELINE",
        "COMMENT_MULTILINE",
        "PRECOMP_MACRO",
        # misc
        "DIVIDE",
        "NEWLINE",
        "ELLIPSIS",
        "DBL_LBRACKET",
        "DBL_RBRACKET",
        "DBL_COLON",
        "DBL_AMP",
        "ARROW",
        "SHIFT_LEFT",
    ] + list(keywords)

    literals = [
        "<",
        ">",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        ";",
        ":",
        ",",
        "\\",
        "|",
        "%",
        "^",
        "!",
        "*",
        "-",
        "+",
        "&",
        "=",
        "'",
        ".",
    ]

    #
    # Regexes for use in tokens (taken from pycparser)
    #

    hex_prefix = "0[xX]"
    hex_digits = "[0-9a-fA-F]+"
    bin_prefix = "0[bB]"
    bin_digits = "[01]+"

    # integer constants (K&R2: A.2.5.1)
    integer_suffix_opt = (
        r"(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?"
    )
    decimal_constant = (
        "(0" + integer_suffix_opt + ")|([1-9][0-9]*" + integer_suffix_opt + ")"
    )
    octal_constant = "0[0-7]*" + integer_suffix_opt
    hex_constant = hex_prefix + hex_digits + integer_suffix_opt
    bin_constant = bin_prefix + bin_digits + integer_suffix_opt

    bad_octal_constant = "0[0-7]*[89]"

    # character constants (K&R2: A.2.5.2)
    # Note: a-zA-Z and '.-~^_!=&;,' are allowed as escape chars to support #line
    # directives with Windows paths as filenames (..\..\dir\file)
    # For the same reason, decimal_escape allows all digit sequences. We want to
    # parse all correct code, even if it means to sometimes parse incorrect
    # code.
    #
    # The original regexes were taken verbatim from the C syntax definition,
    # and were later modified to avoid worst-case exponential running time.
    #
    #   simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
    #   decimal_escape = r"""(\d+)"""
    #   hex_escape = r"""(x[0-9a-fA-F]+)"""
    #   bad_escape = r"""([\\][^a-zA-Z._~^!=&\^\-\\?'"x0-7])"""
    #
    # The following modifications were made to avoid the ambiguity that allowed backtracking:
    # (https://github.com/eliben/pycparser/issues/61)
    #
    # - \x was removed from simple_escape, unless it was not followed by a hex digit, to avoid ambiguity with hex_escape.
    # - hex_escape allows one or more hex characters, but requires that the next character(if any) is not hex
    # - decimal_escape allows one or more decimal characters, but requires that the next character(if any) is not a decimal
    # - bad_escape does not allow any decimals (8-9), to avoid conflicting with the permissive decimal_escape.
    #
    # Without this change, python's `re` module would recursively try parsing each ambiguous escape sequence in multiple ways.
    # e.g. `\123` could be parsed as `\1`+`23`, `\12`+`3`, and `\123`.

    simple_escape = r"""([a-wyzA-Z._~!=&\^\-\\?'"]|x(?![0-9a-fA-F]))"""
    decimal_escape = r"""(\d+)(?!\d)"""
    hex_escape = r"""(x[0-9a-fA-F]+)(?![0-9a-fA-F])"""
    bad_escape = r"""([\\][^a-zA-Z._~^!=&\^\-\\?'"x0-9])"""

    escape_sequence = (
        r"""(\\(""" + simple_escape + "|" + decimal_escape + "|" + hex_escape + "))"
    )

    # This complicated regex with lookahead might be slow for strings, so because all of the valid escapes (including \x) allowed
    # 0 or more non-escaped characters after the first character, simple_escape+decimal_escape+hex_escape got simplified to

    escape_sequence_start_in_string = r"""(\\[0-9a-zA-Z._~!=&\^\-\\?'"])"""

    cconst_char = r"""([^'\\\n]|""" + escape_sequence + ")"
    char_const = "'" + cconst_char + "'"
    wchar_const = "L" + char_const
    u8char_const = "u8" + char_const
    u16char_const = "u" + char_const
    u32char_const = "U" + char_const
    multicharacter_constant = "'" + cconst_char + "{2,4}'"
    unmatched_quote = "('" + cconst_char + "*\\n)|('" + cconst_char + "*$)"
    bad_char_const = (
        r"""('"""
        + cconst_char
        + """[^'\n]+')|('')|('"""
        + bad_escape
        + r"""[^'\n]*')"""
    )

    # string literals (K&R2: A.2.6)
    string_char = r"""([^"\\\n]|""" + escape_sequence_start_in_string + ")"
    string_literal = '"' + string_char + '*"'
    wstring_literal = "L" + string_literal
    u8string_literal = "u8" + string_literal
    u16string_literal = "u" + string_literal
    u32string_literal = "U" + string_literal
    bad_string_literal = '"' + string_char + "*" + bad_escape + string_char + '*"'

    # floating constants (K&R2: A.2.5.3)
    exponent_part = r"""([eE][-+]?[0-9]+)"""
    fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
    floating_constant = (
        "(((("
        + fractional_constant
        + ")"
        + exponent_part
        + "?)|([0-9]+"
        + exponent_part
        + "))[FfLl]?)"
    )
    binary_exponent_part = r"""([pP][+-]?[0-9]+)"""
    hex_fractional_constant = (
        "(((" + hex_digits + r""")?\.""" + hex_digits + ")|(" + hex_digits + r"""\.))"""
    )
    hex_floating_constant = (
        "("
        + hex_prefix
        + "("
        + hex_digits
        + "|"
        + hex_fractional_constant
        + ")"
        + binary_exponent_part
        + "[FfLl]?)"
    )

    t_ignore = " \t\r?@\f"

    # The following floating and integer constants are defined as
    # functions to impose a strict order (otherwise, decimal
    # is placed before the others because its regex is longer,
    # and this is bad)
    #
    @TOKEN(floating_constant)
    def t_FLOAT_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(hex_floating_constant)
    def t_HEX_FLOAT_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(hex_constant)
    def t_INT_CONST_HEX(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(bin_constant)
    def t_INT_CONST_BIN(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(bad_octal_constant)
    def t_BAD_CONST_OCT(self, t: LexToken) -> None:
        msg = "Invalid octal constant"
        self._error(msg, t)

    @TOKEN(octal_constant)
    def t_INT_CONST_OCT(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(decimal_constant)
    def t_INT_CONST_DEC(self, t: LexToken) -> LexToken:
        return t

    # Must come before bad_char_const, to prevent it from
    # catching valid char constants as invalid
    #
    @TOKEN(multicharacter_constant)
    def t_INT_CONST_CHAR(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(char_const)
    def t_CHAR_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(wchar_const)
    def t_WCHAR_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u8char_const)
    def t_U8CHAR_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u16char_const)
    def t_U16CHAR_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u32char_const)
    def t_U32CHAR_CONST(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(unmatched_quote)
    def t_UNMATCHED_QUOTE(self, t: LexToken) -> None:
        msg = "Unmatched '"
        self._error(msg, t)

    @TOKEN(bad_char_const)
    def t_BAD_CHAR_CONST(self, t: LexToken) -> None:
        msg = "Invalid char constant %s" % t.value
        self._error(msg, t)

    @TOKEN(wstring_literal)
    def t_WSTRING_LITERAL(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u8string_literal)
    def t_U8STRING_LITERAL(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u16string_literal)
    def t_U16STRING_LITERAL(self, t: LexToken) -> LexToken:
        return t

    @TOKEN(u32string_literal)
    def t_U32STRING_LITERAL(self, t: LexToken) -> LexToken:
        return t

    # unmatched string literals are caught by the preprocessor

    @TOKEN(bad_string_literal)
    def t_BAD_STRING_LITERAL(self, t):
        msg = "String contains invalid escape code"
        self._error(msg, t)

    @TOKEN(r"[A-Za-z_~][A-Za-z0-9_]*")
    def t_NAME(self, t: LexToken) -> LexToken:
        if t.value in self.keywords:
            t.type = t.value
        return t

    @TOKEN(r"\#.*")
    def t_PRECOMP_MACRO(self, t: LexToken) -> typing.Optional[LexToken]:
        m = _line_re.match(t.value)
        if m:
            self.filename = m.group(2)

            self.line_offset = 1 + self.lex.lineno - int(m.group(1))
            return None
        else:
            return t

    @TOKEN(r"\/\/.*\n?")
    def t_COMMENT_SINGLELINE(self, t: LexToken) -> LexToken:
        if t.value.startswith("///") or t.value.startswith("//!"):
            self.comments.append(t.value.lstrip("\t ").rstrip("\n"))
        t.lexer.lineno += t.value.count("\n")
        return t

    t_DIVIDE = r"/(?!/)"
    t_ELLIPSIS = r"\.\.\."
    t_DBL_LBRACKET = r"\[\["
    t_DBL_RBRACKET = r"\]\]"
    t_DBL_COLON = r"::"
    t_DBL_AMP = r"&&"
    t_ARROW = r"->"
    t_SHIFT_LEFT = r"<<"
    # SHIFT_RIGHT introduces ambiguity

    t_STRING_LITERAL = string_literal

    # Found at http://ostermiller.org/findcomment.html
    @TOKEN(r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/\n?")
    def t_COMMENT_MULTILINE(self, t: LexToken) -> LexToken:
        if t.value.startswith("/**") or t.value.startswith("/*!"):
            # not sure why, but get double new lines
            v = t.value.replace("\n\n", "\n")
            # strip prefixing whitespace
            v = _multicomment_re.sub("\n*", v)
            self.comments = v.splitlines()
        t.lexer.lineno += t.value.count("\n")
        return t

    @TOKEN(r"\n+")
    def t_NEWLINE(self, t: LexToken) -> LexToken:
        t.lexer.lineno += len(t.value)
        del self.comments[:]
        return t

    def t_error(self, t: LexToken) -> None:
        self._error(f"Illegal character {t.value!r}", t)

    def _error(self, msg: str, tok: LexToken):
        tok.location = self.current_location()
        raise LexError(msg, tok)

    _lexer = None
    lex: lex.Lexer
    lineno: int

    def __new__(cls, *args, **kwargs) -> "Lexer":
        # only build the lexer once
        inst = super().__new__(cls)
        if cls._lexer is None:
            cls._lexer = lex.lex(module=inst)

        inst.lex = cls._lexer.clone(inst)
        inst.lex.begin("INITIAL")
        return inst

    def __init__(self, filename: typing.Optional[str] = None):
        self.input: typing.Callable[[str], None] = self.lex.input

        # For tracking current file/line position
        self.filename = filename
        self.line_offset = 0

        # Doxygen comments
        self.comments = []

        self.lookahead = typing.Deque[LexToken]()

        # For 'set_group_of_tokens' support
        self._get_token: typing.Callable[[], LexToken] = self.lex.token
        self.lookahead_stack = typing.Deque[typing.Deque[LexToken]]()

    def current_location(self) -> Location:
        if self.lookahead:
            return self.lookahead[0].location
        return Location(self.filename, self.lex.lineno - self.line_offset)

    def get_doxygen(self) -> typing.Optional[str]:
        """
        This should be called after the first element of something has
        been consumed.

        It will lookahead for comments that come after the item, if prior
        comments don't exist.
        """

        # Assumption: This function is either called at the beginning of a
        # statement or at the end of a statement

        if self.comments:
            comments = self.comments
        else:
            comments = []
            # only look for comments until a newline (including lookahead)
            for tok in self.lookahead:
                if tok.type == "NEWLINE":
                    return None

            while True:
                tok = self._get_token()
                comments.extend(self.comments)

                if tok is None:
                    break

                tok.location = Location(self.filename, tok.lineno - self.line_offset)
                ttype = tok.type
                if ttype == "NEWLINE":
                    self.lookahead.append(tok)
                    break

                if ttype not in self._discard_types:
                    self.lookahead.append(tok)

                if ttype == "NAME":
                    break

                del self.comments[:]

        comment_str = "\n".join(comments)
        del self.comments[:]
        if comment_str:
            return comment_str

        return None

    _discard_types = {"NEWLINE", "COMMENT_SINGLELINE", "COMMENT_MULTILINE"}

    def _token_limit_exceeded(self) -> typing.NoReturn:
        from .errors import CxxParseError

        raise CxxParseError("no more tokens left in this group")

    @contextlib.contextmanager
    def set_group_of_tokens(
        self, toks: typing.List[LexToken]
    ) -> typing.Generator[typing.Deque[LexToken], None, None]:
        # intended for use when you have a set of tokens that you know
        # must be consumed, such as a paren grouping or some type of
        # lookahead case

        stack = self.lookahead_stack
        restore_fn = False

        if not stack:
            restore_fn = True
            self._get_token = self._token_limit_exceeded

        this_buf = typing.Deque[LexToken](toks)
        prev_buf = self.lookahead
        stack.append(prev_buf)
        self.lookahead = this_buf

        try:
            yield this_buf
        finally:
            buf = stack.pop()
            if prev_buf is not buf:
                raise ValueError("internal error")

            self.lookahead = prev_buf

            if restore_fn:
                self._get_token = self.lex.token

    def token(self) -> LexToken:
        tok = None
        while self.lookahead:
            tok = self.lookahead.popleft()
            if tok.type not in self._discard_types:
                return tok

        while True:
            tok = self._get_token()
            if tok is None:
                raise EOFError("unexpected end of file")

            if tok.type not in self._discard_types:
                tok.location = Location(self.filename, tok.lineno - self.line_offset)
                break

        return tok

    def token_eof_ok(self) -> typing.Optional[LexToken]:
        tok = None
        while self.lookahead:
            tok = self.lookahead.popleft()
            if tok.type not in self._discard_types:
                return tok

        while True:
            tok = self._get_token()
            if tok is None:
                break

            if tok.type not in self._discard_types:
                tok.location = Location(self.filename, tok.lineno - self.line_offset)
                break

        return tok

    def token_if(self, *types: str) -> typing.Optional[LexToken]:
        tok = self.token_eof_ok()
        if tok is None:
            return None
        if tok.type not in types:
            # put it back on the left in case it was retrieved
            # from the lookahead buffer
            self.lookahead.appendleft(tok)
            return None
        return tok

    def token_if_in_set(self, types: typing.Set[str]) -> typing.Optional[LexToken]:
        tok = self.token_eof_ok()
        if tok is None:
            return None
        if tok.type not in types:
            # put it back on the left in case it was retrieved
            # from the lookahead buffer
            self.lookahead.appendleft(tok)
            return None
        return tok

    def token_if_val(self, *vals: str) -> typing.Optional[LexToken]:
        tok = self.token_eof_ok()
        if tok is None:
            return None
        if tok.value not in vals:
            # put it back on the left in case it was retrieved
            # from the lookahead buffer
            self.lookahead.appendleft(tok)
            return None
        return tok

    def token_if_not(self, *types: str) -> typing.Optional[LexToken]:
        tok = self.token_eof_ok()
        if tok is None:
            return None
        if tok.type in types:
            # put it back on the left in case it was retrieved
            # from the lookahead buffer
            self.lookahead.appendleft(tok)
            return None
        return tok

    def token_peek_if(self, *types: str) -> bool:
        tok = self.token_eof_ok()
        if not tok:
            return False
        self.lookahead.appendleft(tok)
        return tok.type in types

    def return_token(self, tok: LexToken) -> None:
        self.lookahead.appendleft(tok)

    def return_tokens(self, toks: typing.Sequence[LexToken]) -> None:
        self.lookahead.extendleft(reversed(toks))


if __name__ == "__main__":  # pragma: no cover
    try:
        lex.runmain(lexer=Lexer(None))
    except EOFError:
        pass
