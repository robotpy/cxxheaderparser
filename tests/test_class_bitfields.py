# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    ClassDecl,
    Field,
    Function,
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Parameter,
    Pointer,
    Type,
    Typedef,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    parse_string,
    ParsedData,
)


def test_class_bitfield_1() -> None:
    content = """
      struct S {
        // will usually occupy 2 bytes:
        // 3 bits: value of b1
        // 2 bits: unused
        // 6 bits: value of b2
        // 2 bits: value of b3
        // 3 bits: unused
        unsigned char b1 : 3, : 2, b2 : 6, b3 : 2;
      };
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
                    fields=[
                        Field(
                            name="b1",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        FundamentalSpecifier(name="unsigned char")
                                    ]
                                )
                            ),
                            access="public",
                            bits=3,
                        ),
                        Field(
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        FundamentalSpecifier(name="unsigned char")
                                    ]
                                )
                            ),
                            access="public",
                            bits=2,
                        ),
                        Field(
                            name="b2",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        FundamentalSpecifier(name="unsigned char")
                                    ]
                                )
                            ),
                            access="public",
                            bits=6,
                        ),
                        Field(
                            name="b3",
                            type=Type(
                                typename=PQName(
                                    segments=[
                                        FundamentalSpecifier(name="unsigned char")
                                    ]
                                )
                            ),
                            access="public",
                            bits=2,
                        ),
                    ],
                )
            ]
        )
    )


def test_class_bitfield_2() -> None:
    content = """
      struct HAL_ControlWord {
        int x : 1;
        int y : 1;
      };
      typedef struct HAL_ControlWord HAL_ControlWord;
      int HAL_GetControlWord(HAL_ControlWord *controlWord);
    """
    data = parse_string(content, cleandoc=True)

    assert data == ParsedData(
        namespace=NamespaceScope(
            classes=[
                ClassScope(
                    class_decl=ClassDecl(
                        typename=PQName(
                            segments=[NameSpecifier(name="HAL_ControlWord")],
                            classkey="struct",
                        )
                    ),
                    fields=[
                        Field(
                            name="x",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            access="public",
                            bits=1,
                        ),
                        Field(
                            name="y",
                            type=Type(
                                typename=PQName(
                                    segments=[FundamentalSpecifier(name="int")]
                                )
                            ),
                            access="public",
                            bits=1,
                        ),
                    ],
                )
            ],
            functions=[
                Function(
                    return_type=Type(
                        typename=PQName(segments=[FundamentalSpecifier(name="int")])
                    ),
                    name=PQName(segments=[NameSpecifier(name="HAL_GetControlWord")]),
                    parameters=[
                        Parameter(
                            type=Pointer(
                                ptr_to=Type(
                                    typename=PQName(
                                        segments=[NameSpecifier(name="HAL_ControlWord")]
                                    )
                                )
                            ),
                            name="controlWord",
                        )
                    ],
                )
            ],
            typedefs=[
                Typedef(
                    type=Type(
                        typename=PQName(
                            segments=[NameSpecifier(name="HAL_ControlWord")],
                            classkey="struct",
                        )
                    ),
                    name="HAL_ControlWord",
                )
            ],
        )
    )
