from cxxheaderparser.simple import (
    ClassDecl,
    ClassScope,
    FriendDecl,
    Method,
    NamespaceScope,
    ParsedData,
    Variable,
    parse_string,
)
from cxxheaderparser.types import FundamentalSpecifier, NameSpecifier, PQName, Type
import re
import pytest
from cxxheaderparser.errors import CxxParseError


def test_friend_after_return_type() -> None:
    content = """
        struct S { void friend f(); }; int after;
    """

    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="S")], classkey="struct"
                        )
                    ),
                    friends=[
                        FriendDecl(
                            fn=Method(
                                return_type=Type(
                                    typename=PQName(
                                        segments=[FundamentalSpecifier(name="void")]
                                    )
                                ),
                                name=PQName(segments=[NameSpecifier(name="f")]),
                                parameters=[],
                                access="public",
                            )
                        )
                    ],
                )
            ],
            variables=[
                Variable(
                    name=PQName(segments=[NameSpecifier(name="after")]),
                    type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                )
            ],
        )
    )


def test_friend_outside_class_rejected() -> None:
    content = """
        void friend f();
    """

    err = "<str>:1: parse error evaluating 'friend': unexpected 'friend'"
    with pytest.raises(CxxParseError, match=re.escape(err)):
        parse_string(content, cleandoc=True)
