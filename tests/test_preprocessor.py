from cxxheaderparser.options import ParserOptions
from cxxheaderparser.preprocessor import make_pcpp_preprocessor
from cxxheaderparser.simple import NamespaceScope, ParsedData, parse_string
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Token, Type, Value, Variable


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