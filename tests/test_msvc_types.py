from cxxheaderparser.types import (
    Function,
    Type,
    PQName,
    NameSpecifier,
)
from cxxheaderparser.simple import (
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_msvc_types() -> None:
    content = """
      __int64 test_int64();
      __int32 test_int32();
      __int16 test_int16();
      __int8 test_int8();
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="__int64")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="test_int64")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="__int32")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="test_int32")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="__int16")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="test_int16")]),
                    parameters=[],
                ),
                Function(
                    return_type=Type(
                        typename=PQName(segments=[NameSpecifier(name="__int8")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="test_int8")]),
                    parameters=[],
                ),
            ]
        )
    )
