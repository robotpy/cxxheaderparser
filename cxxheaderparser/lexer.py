import contextlib
from collections import deque
import re
import typing
import sys

from ._ply import lex


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
        "NUMBER",
        "FLOAT_NUMBER",
        "NAME",
        "COMMENT_SINGLELINE",
        "COMMENT_MULTILINE",
        "PRECOMP_MACRO",
        "DIVIDE",
        "CHAR_LITERAL",
        "STRING_LITERAL",
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

    t_ignore = " \t\r?@\f"
    t_NUMBER = r"[0-9][0-9XxA-Fa-f]*"
    t_FLOAT_NUMBER = r"[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?"

    def t_NAME(self, t: LexToken) -> LexToken:
        r"[A-Za-z_~][A-Za-z0-9_]*"
        if t.value in self.keywords:
            t.type = t.value
        return t

    def t_PRECOMP_MACRO(self, t: LexToken) -> typing.Optional[LexToken]:
        r"\#.*"
        m = _line_re.match(t.value)
        if m:
            filename = m.group(2)
            if filename not in self._filenames_set:
                self.filenames.append(filename)
                self._filenames_set.add(filename)
            self.filename = filename

            self.line_offset = 1 + self.lex.lineno - int(m.group(1))
            return None
        else:
            return t

    def t_COMMENT_SINGLELINE(self, t: LexToken) -> LexToken:
        r"\/\/.*\n?"
        if t.value.startswith("///") or t.value.startswith("//!"):
            self.comments.append(t.value.lstrip("\t ").rstrip("\n"))
        t.lexer.lineno += t.value.count("\n")
        return t

    t_DIVIDE = r"/(?!/)"
    t_CHAR_LITERAL = "'.'"
    t_ELLIPSIS = r"\.\.\."
    t_DBL_LBRACKET = r"\[\["
    t_DBL_RBRACKET = r"\]\]"
    t_DBL_COLON = r"::"
    t_DBL_AMP = r"&&"
    t_ARROW = r"->"
    t_SHIFT_LEFT = r"<<"
    # SHIFT_RIGHT introduces ambiguity

    # found at http://wordaligned.org/articles/string-literals-and-regular-expressions
    # TODO: This does not work with the string "bla \" bla"
    t_STRING_LITERAL = r'"([^"\\]|\\.)*"'

    # Found at http://ostermiller.org/findcomment.html
    def t_COMMENT_MULTILINE(self, t: LexToken) -> LexToken:
        r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/\n?"
        if t.value.startswith("/**") or t.value.startswith("/*!"):
            # not sure why, but get double new lines
            v = t.value.replace("\n\n", "\n")
            # strip prefixing whitespace
            v = _multicomment_re.sub("\n*", v)
            self.comments = v.splitlines()
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_NEWLINE(self, t: LexToken) -> LexToken:
        r"\n+"
        t.lexer.lineno += len(t.value)
        del self.comments[:]
        return t

    def t_error(self, t: LexToken) -> None:
        print("Lex error: ", t)

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

        self.filenames: typing.List[str] = []
        self._filenames_set: typing.Set[str] = set()

        if filename:
            self.filenames.append(filename)
            self._filenames_set.add(filename)

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


if __name__ == "__main__":
    try:
        lex.runmain(lexer=Lexer(None))
    except EOFError:
        pass
