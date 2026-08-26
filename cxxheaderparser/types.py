import typing
from enum import Enum
from dataclasses import dataclass, field

from .tokfmt import tokfmt, Token


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

    def format(self) -> str:
        return tokfmt(self.tokens)


class AttributeStyle(Enum):
    """
    Indicates what style of attribute was found
    """

    #: ``[[deprecated]]``
    CXX = "cxx"

    #: ``__attribute__((deprecated))``
    GCC = "gcc"

    #: ``__declspec(deprecated)``
    MSVC = "msvc"


@dataclass
class Attribute:
    """
    An attribute

    .. code-block:: c++

        [[deprecated("message")]]
          ~~~~~~~~~  ~~~~~~~~~~~
    """

    #: Indicates what style of attribute this is
    style: AttributeStyle

    name: str

    #: Portion of the attribute inside the parens
    value: typing.Optional[Value] = None


@dataclass
class NamespaceAlias:
    """
    A namespace alias

    .. code-block:: c++

        namespace ANS = my::ns;
                  ~~~   ~~~~~~

    """

    alias: str

    #: These are the names (split by ::) for the namespace that this alias
    #: refers to, but does not include any parent namespace names. It may
    #: include a leading "::", but does not include a following :: string.
    names: typing.List[str]


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

    #: Documentation if present
    doxygen: typing.Optional[str] = None


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

    def format(self) -> str:
        return f"decltype({tokfmt(self.tokens)})"


@dataclass
class FundamentalSpecifier:
    """
    A specifier that only contains fundamental types.

    Fundamental types include various combinations of the following: unsigned,
    signed, short, int, long, float, double, char, bool, char16_t, char32_t,
    nullptr_t, wchar_t, void
    """

    name: str

    def format(self) -> str:
        return self.name


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

    def format(self) -> str:
        if self.specialization:
            return f"{self.name}{self.specialization.format()}"
        else:
            return self.name


@dataclass
class AutoSpecifier:
    """
    Used for an auto return type
    """

    name: str = "auto"

    def format(self) -> str:
        return self.name


@dataclass
class AnonymousName:
    """
    A name for an anonymous class, such as in a typedef. There is no string
    associated with this name, only an integer id. Things that share the same
    anonymous name have anonymous name instances with the same id
    """

    #: Unique id associated with this name (only unique per parser instance!)
    id: int

    def format(self) -> str:
        # TODO: not sure what makes sense here, subject to change
        return f"<<id={self.id}>>"


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

    def format(self) -> str:
        tn = "typename " if self.has_typename else ""
        if self.classkey:
            return f"{tn}{self.classkey} {'::'.join(seg.format() for seg in self.segments)}"
        else:
            return tn + "::".join(seg.format() for seg in self.segments)


@dataclass
class TemplateArgument:
    """
    A single argument for a template specialization

    .. code-block:: c++

        Foo<int, Bar...>
            ~~~

    """

    #: If this argument is a type, it is stored here as a TypeId, otherwise
    #: it's stored as an unparsed set of values
    arg: typing.Union["TypeId", Value]

    param_pack: bool = False

    def format(self) -> str:
        if self.param_pack:
            return f"{self.arg.format()}..."
        else:
            return self.arg.format()


@dataclass
class TemplateSpecialization:
    """
    Contains the arguments of a template specialization

    .. code-block:: c++

        Foo<int, Bar...>
            ~~~~~~~~~~~

    """

    args: typing.List[TemplateArgument]

    def format(self) -> str:
        return f"<{', '.join(arg.format() for arg in self.args)}>"


def _join_prefix(prefix: str, declarator: str) -> str:
    separator = " " if declarator and declarator[0] not in "*&[" else ""
    return f"{prefix}{separator}{declarator}"


def _format_prefixed_type(target: typing.Any, prefix: str, name: str) -> str:
    declarator = _join_prefix(prefix, name)
    if isinstance(target, (Array, FunctionType)):
        declarator = f"({declarator})"
    return target.format_decl(declarator)


@dataclass
class FunctionType:
    """
    A function type. It may be used bare in a TypeId or wrapped by a
    pointer-like DecoratedType.

    Its return type is always a DecoratedType; functions cannot return bare
    function types.
    """

    return_type: "DecoratedType"
    parameters: typing.List["Parameter"]

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

    const: bool = False
    volatile: bool = False

    #: Ref qualifier, either ``&`` or ``&&``.
    ref_qualifier: typing.Optional[str] = None

    def _format_qualifiers(self) -> str:
        qualifiers = []
        if self.const:
            qualifiers.append("const")
        if self.volatile:
            qualifiers.append("volatile")
        if self.ref_qualifier:
            qualifiers.append(self.ref_qualifier)
        return f" {' '.join(qualifiers)}" if qualifiers else ""

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        params = [p.format() for p in self.parameters]
        if self.vararg:
            params.append("...")
        params_str = ", ".join(params)
        qualifiers = self._format_qualifiers()
        noexcept = ""
        if self.noexcept is not None:
            noexcept = " noexcept"
            if self.noexcept.tokens:
                noexcept += f"({self.noexcept.format()})"
        if self.has_trailing_return:
            return f"auto {name}({params_str}){qualifiers}{noexcept} -> {self.return_type.format()}"
        else:
            return self.return_type.format_decl(
                f"{name}({params_str}){qualifiers}{noexcept}"
            )


@dataclass
class Type:
    """
    A type with a name associated with it
    """

    typename: PQName

    const: bool = False
    volatile: bool = False

    def format(self) -> str:
        c = "const " if self.const else ""
        v = "volatile " if self.volatile else ""
        return f"{c}{v}{self.typename.format()}"

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        c = "const " if self.const else ""
        v = "volatile " if self.volatile else ""
        separator = " " if name and name[0] not in "*&[" else ""
        return f"{c}{v}{self.typename.format()}{separator}{name}"


@dataclass
class Array:
    """
    Information about an array. Multidimensional arrays are represented as
    an array of array.
    """

    #: The type that this is an array of
    array_of: typing.Union["Array", "MemberPointer", "Pointer", Type]

    #: Size of the array
    #:
    #: .. code-block:: c++
    #:
    #:    int x[10];
    #:          ~~
    size: typing.Optional[Value]

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        size = self.size.format() if self.size else ""
        return self.array_of.format_decl(f"{name}[{size}]")


@dataclass
class Pointer:
    """
    A pointer
    """

    #: Thing that this points to
    ptr_to: typing.Union[Array, FunctionType, "MemberPointer", "Pointer", Type]

    const: bool = False
    volatile: bool = False
    restrict: bool = False

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        c = " const" if self.const else ""
        v = " volatile" if self.volatile else ""
        r = " __restrict__" if self.restrict else ""
        return _format_prefixed_type(self.ptr_to, f"*{r}{c}{v}", name)


@dataclass
class MemberPointer:
    """
    A pointer to a class member. The member may be an object or a function.
    """

    #: Thing that this points to
    ptr_to: typing.Union[Array, FunctionType, "MemberPointer", Pointer, Type]

    #: Class that owns the member
    classname: PQName

    const: bool = False
    volatile: bool = False
    restrict: bool = False

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        c = " const" if self.const else ""
        v = " volatile" if self.volatile else ""
        r = " __restrict__" if self.restrict else ""
        return _format_prefixed_type(
            self.ptr_to, f"{self.classname.format()}::*{r}{c}{v}", name
        )


@dataclass
class Reference:
    """
    A lvalue (``&``) reference
    """

    ref_to: typing.Union[Array, FunctionType, MemberPointer, Pointer, Type]
    restrict: bool = False

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        r = " __restrict__" if self.restrict else ""
        return _format_prefixed_type(self.ref_to, f"&{r}", name)


@dataclass
class MoveReference:
    """
    An rvalue (``&&``) reference
    """

    moveref_to: typing.Union[Array, FunctionType, MemberPointer, Pointer, Type]

    def format(self) -> str:
        return self.format_decl("")

    def format_decl(self, name: str) -> str:
        """Format as a named declaration"""
        return _format_prefixed_type(self.moveref_to, "&&", name)


#: An object/declarator type decorated with arrays, pointers, or references.
#: FunctionType can occur as the target of a pointer-like wrapper, but is not
#: itself a DecoratedType.
DecoratedType = typing.Union[
    Array, MemberPointer, Pointer, MoveReference, Reference, Type
]

#: A type-id, including a bare FunctionType in contexts that accept one.
TypeId = typing.Union[DecoratedType, FunctionType]


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

    #: Any attributes attached to this enumerator
    attributes: typing.List[Attribute] = field(default_factory=list)


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
    #: Any attributes attached to this enum declaration
    attributes: typing.List[Attribute] = field(default_factory=list)

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None


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

       // abbreviated template parameters are converted to this and param_idx is set
       void fn(C auto p)
               ~~~~~~

       // abbreviated template parameters that are return types have param_idx = -1
       C auto fn()
       ~~~~~~
    """

    type: DecoratedType
    name: typing.Optional[str] = None
    default: typing.Optional[Value] = None

    #: If this was promoted, the parameter index that this corresponds with. Return
    #: types are set to -1
    param_idx: typing.Optional[int] = None

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

    # Currently don't interpret requires, if that changes in the future
    # then this API will change.

    #: template <typename T> requires ...
    raw_requires_pre: typing.Optional[Value] = None


#: If no template, this is None. This is a TemplateDecl if this there is a single
#: declaration:
#:
#: .. code-block:: c++
#:
#:    template <typename T>
#:    struct C {};
#:
#: If there are multiple template declarations, then this is a list of
#: declarations in the order that they're encountered:
#:
#: .. code-block:: c++
#:
#:    template<>
#:    template<class U>
#:    struct A<char>::C {};
#:
TemplateDeclTypeVar = typing.Union[None, TemplateDecl, typing.List[TemplateDecl]]


@dataclass
class TemplateInst:
    """
    Explicit template instantiation

    .. code-block:: c++

        template class MyClass<1,2>;

        extern template class MyClass<2,3>;
    """

    typename: PQName
    extern: bool
    doxygen: typing.Optional[str] = None


@dataclass
class Concept:
    """
    Preliminary support for consuming headers that contain concepts, but
    not trying to actually make sense of them at this time. If this is
    something you care about, pull requests are welcomed!

    .. code-block:: c++

        template <class T>
        concept Meowable = is_meowable<T>;

        template<typename T>
        concept Addable = requires (T x) { x + x; };
    """

    template: TemplateDecl
    name: str

    #: In the future this will be removed if we fully parse the expression
    raw_constraint: Value

    doxygen: typing.Optional[str] = None


@dataclass
class ForwardDecl:
    """
    Represents a forward declaration of a user defined type
    """

    typename: PQName
    template: TemplateDeclTypeVar = None
    doxygen: typing.Optional[str] = None
    #: Any attributes attached to this forward declaration
    attributes: typing.List[Attribute] = field(default_factory=list)

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
    #: Any attributes attached to this base specifier
    attributes: typing.List[Attribute] = field(default_factory=list)


@dataclass
class ClassDecl:
    """
    A class is a user defined type (class/struct/union)
    """

    typename: PQName

    bases: typing.List[BaseClass] = field(default_factory=list)
    template: TemplateDeclTypeVar = None

    explicit: bool = False
    final: bool = False

    doxygen: typing.Optional[str] = None
    #: Any attributes attached to this class declaration
    attributes: typing.List[Attribute] = field(default_factory=list)

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

    #: Indicates that this parameter is the parameter used for cxx23 deducing-this
    deduces_this: bool = False

    def format(self) -> str:
        default = f" = {self.default.format()}" if self.default else ""
        pp = "... " if self.param_pack else ""
        name = self.name
        if name:
            return f"{self.type.format_decl(f'{pp}{name}')}{default}"
        else:
            return f"{self.type.format()}{pp}{default}"


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
    #: Any attributes attached to this function declaration
    attributes: typing.List[Attribute] = field(default_factory=list)

    constexpr: bool = False
    extern: typing.Union[bool, str] = False
    static: bool = False
    inline: bool = False
    deleted: bool = False

    #: If true, the body of the function is present
    has_body: bool = False

    #: True if function has a trailing return type (``auto foo() -> int``).
    #: In this case, the 'auto' return type is removed and replaced with
    #: whatever the trailing return type was
    has_trailing_return: bool = False

    template: TemplateDeclTypeVar = None

    #: Value of any throw specification for this function. The value omits the
    #: outer parentheses.
    throw: typing.Optional[Value] = None

    #: Value of any noexcept specification for this function. The value omits
    #: the outer parentheses.
    noexcept: typing.Optional[Value] = None

    #: Only set if an MSVC calling convention (__stdcall, etc) is explictly
    #: specified.
    #:
    #: .. note::  If your code contains things like WINAPI, you will need to
    #:            use a preprocessor to transform it to the appropriate
    #:            calling convention
    msvc_convention: typing.Optional[str] = None

    #: The operator type (+, +=, etc).
    #:
    #: If this object is a Function, then this is a free operator function. If
    #: this object is a Method, then it is an operator method.
    #:
    #: In the case of a conversion operator (such as 'operator bool'), this
    #: is the string "conversion" and the full Type is found in return_type
    operator: typing.Optional[str] = None

    #: A requires constraint following the function declaration. If you need the
    #: prior, look at TemplateDecl.raw_requires_pre. At the moment this is just
    #: a raw value, if we interpret it in the future this will change.
    #:
    #: template <typename T> int main() requires ...
    raw_requires: typing.Optional[Value] = None


@dataclass
class Method(Function):
    """
    A method declaration, potentially with the method body
    """

    #: If parsed within a class, the access level for this method
    access: typing.Optional[str] = None

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

    #: True if the method was declared ``explicit``. For C++20
    #: ``explicit(<expr>)``, this holds the expression as a Value (omitting
    #: the outer parentheses).
    explicit: typing.Union[bool, Value] = False
    default: bool = False

    destructor: bool = False

    pure_virtual: bool = False
    virtual: bool = False
    final: bool = False
    override: bool = False


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
    type: TypeId

    #: The alias introduced for the specified type
    #:
    #: .. code-block:: c++
    #:
    #:    typedef type *pname;
    #:                  ~~~~~
    name: str

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None
    #: Any attributes attached to this typedef
    attributes: typing.List[Attribute] = field(default_factory=list)


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
    #: Any attributes attached to this variable
    attributes: typing.List[Attribute] = field(default_factory=list)


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
    bits: typing.Union[None, int, Value] = None

    constexpr: bool = False
    mutable: bool = False
    static: bool = False
    inline: bool = False

    doxygen: typing.Optional[str] = None
    #: Any attributes attached to this field
    attributes: typing.List[Attribute] = field(default_factory=list)


@dataclass
class UsingDecl:
    """
    .. code-block:: c++

        using NS::ClassName;
    """

    typename: PQName

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None

    #: Documentation if present
    doxygen: typing.Optional[str] = None


@dataclass
class UsingAlias:
    """
    .. code-block:: c++

        using foo = int;

        template <typename T>
        using VectorT = std::vector<T>;

    """

    alias: str
    type: TypeId

    template: typing.Optional[TemplateDecl] = None

    #: If within a class, the access level for this decl
    access: typing.Optional[str] = None

    #: Documentation if present
    doxygen: typing.Optional[str] = None


@dataclass
class DeductionGuide:
    """
    .. code-block:: c++

    template <class T>
    MyClass(T) -> MyClass(int);
    """

    #: Only constructors and destructors don't have a return type
    result_type: typing.Optional[DecoratedType]

    name: PQName
    parameters: typing.List[Parameter]

    doxygen: typing.Optional[str] = None
