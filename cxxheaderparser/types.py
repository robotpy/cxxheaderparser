import typing
from dataclasses import dataclass, field


@dataclass
class Token:
    """
    In an ideal world, this Token class would not be exposed via the user
    visible API. Unfortunately, getting to that point would take a significant
    amount of effort.

    It is not expected that these will change, but they might.

    At the moment, the only supported use of Token objects are in conjunction
    with the ``tokfmt`` function. As this library matures, we'll try to clarify
    the expectations around these. File an issue on github if you have ideas!
    """

    #: Raw value of the token
    value: str

    #: Lex type of the token
    type: str = field(repr=False, compare=False, default="")


@dataclass
class Value:
    """
    A unparsed list of tokens

    .. code-block:: c++

        int x = 0x1337;
                ~~~~~~
    """

    #: Tokens corresponding to the value
    tokens: typing.List[Token]


@dataclass
class NamespaceDecl:
    """
    Namespace declarations

    .. code-block:: c++

        namespace foo::bar {}
                  ~~~~~~~~
    """

    #: These are the names (split by ::) for this namespace declaration,
    #: but does not include any parent namespace names
    #:
    #: An anonymous namespace is an empty list
    names: typing.List[str]
    inline: bool = False


@dataclass
class DecltypeSpecifier:
    """
    Contents of a decltype (inside the parentheses)

    .. code-block:: c++

        decltype(Foo::Bar)
                 ~~~~~~~~
    """

    #: Unparsed tokens within the decltype
    tokens: typing.List[Token]


@dataclass
class FundamentalSpecifier:
    """
    A specifier that only contains fundamental types
    """

    name: str


@dataclass
class NameSpecifier:
    """
    An individual segment of a type name

    .. code-block:: c++

        Foo::Bar
        ~~~

    """

    name: str

    specialization: typing.Optional["TemplateSpecialization"] = None


@dataclass
class AutoSpecifier:
    """
    Used for an auto return type
    """

    name: str = "auto"


@dataclass
class AnonymousName:
    """
    A name for an anonymous class, such as in a typedef. There is no string
    associated with this name, only an integer id. Things that share the same
    anonymous name have anonymous name instances with the same id
    """

    #: Unique id associated with this name (only unique per parser instance!)
    id: int


PQNameSegment = typing.Union[
    AnonymousName, FundamentalSpecifier, NameSpecifier, DecltypeSpecifier, AutoSpecifier
]


@dataclass
class PQName:
    """
    Possibly qualified name of a C++ type.
    """

    #: All of the segments of the name. This is always guaranteed to have at
    #: least one element in it. Name is segmented by '::'
    #:
    #: If a name refers to the global namespace, the first segment will be an
    #: empty NameSpecifier
    segments: typing.List[PQNameSegment]

    #: Set if the name starts with class/enum/struct
    classkey: typing.Optional[str] = None

    #: Set to true if the type was preceded with 'typename'
    has_typename: bool = False


@dataclass
class Enumerator:
    """
    An individual value of an enumeration
    """

    #: The enumerator key name
    name: str

    #: None if not explicitly specified
    value: typing.Optional[Value] = None

    #: Documentation if present
    doxygen: typing.Optional[str] = None


@dataclass
class EnumDecl:
    """
    An enumeration type
    """

    typename: PQName

    values: typing.List[Enumerator]

    base: typing.Optional[PQName] = None

    #: Documentation if present
    doxygen: typing.Optional[str] = None

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None


@dataclass
class TemplateArgument:
    """
    A single argument for a template specialization

    .. code-block:: c++

        Foo<int, Bar...>
            ~~~

    """

    #: If this argument is a type, it is stored here as a DecoratedType,
    #: otherwise it's stored as an unparsed set of values
    arg: typing.Union["DecoratedType", "FunctionType", Value]

    param_pack: bool = False


@dataclass
class TemplateSpecialization:
    """
    Contains the arguments of a template specialization

    .. code-block:: c++

        Foo<int, Bar...>
            ~~~~~~~~~~~

    """

    args: typing.List[TemplateArgument]


@dataclass
class FunctionType:
    """
    A function type, currently only used in a function pointer

    .. note:: There can only be one of FunctionType or Type in a DecoratedType
              chain
    """

    return_type: "DecoratedType"
    parameters: typing.List["Parameter"]

    #: If a member function pointer
    # TODO classname: typing.Optional[PQName]

    #: Set to True if ends with ``...``
    vararg: bool = False

    #: True if function has a trailing return type (``auto foo() -> int``).
    #: In this case, the 'auto' return type is removed and replaced with
    #: whatever the trailing return type was
    has_trailing_return: bool = False

    noexcept: typing.Optional[Value] = None

    #: Only set if an MSVC calling convention (__stdcall, etc) is explictly
    #: specified.
    #:
    #: .. note::  If your code contains things like WINAPI, you will need to
    #:            use a preprocessor to transform it to the appropriate
    #:            calling convention
    msvc_convention: typing.Optional[str] = None


@dataclass
class Type:
    """
    A type with a name associated with it
    """

    typename: PQName

    const: bool = False
    volatile: bool = False


@dataclass
class Array:
    """
    Information about an array. Multidimensional arrays are represented as
    an array of array.
    """

    #: The type that this is an array of
    array_of: typing.Union["Array", "Pointer", Type]

    #: Size of the array
    #:
    #: .. code-block:: c++
    #:
    #:    int x[10];
    #:          ~~
    size: typing.Optional[Value]


@dataclass
class Pointer:
    """
    A pointer
    """

    #: Thing that this points to
    ptr_to: typing.Union[Array, FunctionType, "Pointer", Type]

    const: bool = False
    volatile: bool = False


@dataclass
class Reference:
    """
    A lvalue (``&``) reference
    """

    ref_to: typing.Union[Array, FunctionType, Pointer, Type]


@dataclass
class MoveReference:
    """
    An rvalue (``&&``) reference
    """

    moveref_to: typing.Union[Array, FunctionType, Pointer, Type]


#: A type or function type that is decorated with various things
#:
#: .. note:: There can only be one of FunctionType or Type in a DecoratedType
#:           chain
DecoratedType = typing.Union[Array, Pointer, MoveReference, Reference, Type]


@dataclass
class TemplateNonTypeParam:
    """

    .. code-block:: c++

       template <int T>
                 ~~~~~

       template <class T, typename T::type* U>
                          ~~~~~~~~~~~~~~~~~~~

       template <auto T>
                 ~~~~~~
    """

    type: DecoratedType
    name: typing.Optional[str] = None
    default: typing.Optional[Value] = None

    #: Contains a ``...``
    param_pack: bool = False


@dataclass
class TemplateTypeParam:
    """

    .. code-block:: c++

       template <typename T>
                 ~~~~~~~~~~
    """

    #: 'typename' or 'class'
    typekey: str

    name: typing.Optional[str] = None

    param_pack: bool = False

    default: typing.Optional[Value] = None

    #: A template-template param
    template: typing.Optional["TemplateDecl"] = None


#: A parameter for a template declaration
#:
#: .. code-block:: c++
#:
#:    template <typename T>
#:              ~~~~~~~~~~
TemplateParam = typing.Union[TemplateNonTypeParam, TemplateTypeParam]


@dataclass
class TemplateDecl:
    """
    Template declaration for a function or class

    .. code-block:: c++

        template <typename T>
        class Foo {};

        template <typename T>
        T fn();

    """

    params: typing.List[TemplateParam] = field(default_factory=list)


@dataclass
class ForwardDecl:
    """
    Represents a forward declaration of a user defined type
    """

    typename: PQName
    template: typing.Optional[TemplateDecl] = None
    doxygen: typing.Optional[str] = None

    #: Set if this is a forward declaration of an enum and it has a base
    enum_base: typing.Optional[PQName] = None

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None


@dataclass
class BaseClass:
    """
    Base class declarations for a class
    """

    #: access specifier for this base
    access: str

    #: possibly qualified type name for the base
    typename: PQName

    #: Virtual inheritance
    virtual: bool = False

    #: Contains a ``...``
    param_pack: bool = False


@dataclass
class ClassDecl:
    """
    A class is a user defined type (class/struct/union)
    """

    typename: PQName

    bases: typing.List[BaseClass] = field(default_factory=list)
    template: typing.Optional[TemplateDecl] = None

    explicit: bool = False
    final: bool = False

    doxygen: typing.Optional[str] = None

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None

    @property
    def classkey(self) -> typing.Optional[str]:
        return self.typename.classkey


@dataclass
class Parameter:
    """
    A parameter of a function/method
    """

    type: DecoratedType
    name: typing.Optional[str] = None
    default: typing.Optional[Value] = None
    param_pack: bool = False


@dataclass
class Function:
    """
    A function declaration, potentially with the function body
    """

    #: Only constructors and destructors don't have a return type
    return_type: typing.Optional[DecoratedType]

    name: PQName
    parameters: typing.List[Parameter]

    #: Set to True if ends with ``...``
    vararg: bool = False

    doxygen: typing.Optional[str] = None

    constexpr: bool = False
    extern: typing.Union[bool, str] = False
    static: bool = False
    inline: bool = False

    #: If true, the body of the function is present
    has_body: bool = False

    #: True if function has a trailing return type (``auto foo() -> int``).
    #: In this case, the 'auto' return type is removed and replaced with
    #: whatever the trailing return type was
    has_trailing_return: bool = False

    template: typing.Optional[TemplateDecl] = None

    throw: typing.Optional[Value] = None
    noexcept: typing.Optional[Value] = None

    #: Only set if an MSVC calling convention (__stdcall, etc) is explictly
    #: specified.
    #:
    #: .. note::  If your code contains things like WINAPI, you will need to
    #:            use a preprocessor to transform it to the appropriate
    #:            calling convention
    msvc_convention: typing.Optional[str] = None


@dataclass
class Method(Function):
    """
    A method declaration, potentially with the method body
    """

    access: str = ""

    const: bool = False
    volatile: bool = False

    #: ref-qualifier for this method, either lvalue (&) or rvalue (&&)
    #:
    #: .. code-block:: c++
    #:
    #:   void foo() &&;
    #:              ~~
    #:
    ref_qualifier: typing.Optional[str] = None

    constructor: bool = False
    explicit: bool = False
    default: bool = False
    deleted: bool = False

    destructor: bool = False

    pure_virtual: bool = False
    virtual: bool = False
    final: bool = False
    override: bool = False


@dataclass
class Operator(Method):
    """
    Represents an operator method
    """

    #: The operator type (+, +=, etc).
    #:
    #: In the case of a conversion operator (such as 'operator bool'), this
    #: is the string "conversion" and the full Type is found in return_type
    operator: str = ""


@dataclass
class FriendDecl:
    """
    Represents a friend declaration -- friends can only be classes or functions
    """

    cls: typing.Optional[ForwardDecl] = None

    fn: typing.Optional[Function] = None


@dataclass
class Typedef:
    """
    A typedef specifier. A unique typedef specifier is created for each alias
    created by the typedef.

    .. code-block:: c++

        typedef type name, *pname;

    """

    #: The aliased type or function type
    #:
    #: .. code-block:: c++
    #:
    #:    typedef type *pname;
    #:            ~~~~~~
    type: typing.Union[DecoratedType, FunctionType]

    #: The alias introduced for the specified type
    #:
    #: .. code-block:: c++
    #:
    #:    typedef type *pname;
    #:                  ~~~~~
    name: str

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None


@dataclass
class Variable:
    """
    A variable declaration
    """

    name: PQName
    type: DecoratedType

    value: typing.Optional[Value] = None

    constexpr: bool = False
    extern: typing.Union[bool, str] = False
    static: bool = False
    inline: bool = False

    #: Can occur for a static variable for a templated class
    template: typing.Optional[TemplateDecl] = None

    doxygen: typing.Optional[str] = None


@dataclass
class Field:
    """
    A field of a class
    """

    #: public/private/protected
    access: str

    type: DecoratedType
    name: typing.Optional[str] = None

    value: typing.Optional[Value] = None
    bits: typing.Optional[int] = None

    constexpr: bool = False
    mutable: bool = False
    static: bool = False

    doxygen: typing.Optional[str] = None


@dataclass
class UsingDecl:
    """
    .. code-block:: c++

        using NS::ClassName;
    """

    typename: PQName

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None


@dataclass
class UsingAlias:
    """
    .. code-block:: c++

        using foo = int;

        template <typename T>
        using VectorT = std::vector<T>;

    """

    alias: str
    type: DecoratedType

    template: typing.Optional[TemplateDecl] = None

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None
