import sys
import typing

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    Protocol = object


from .types import (
    EnumDecl,
    Field,
    ForwardDecl,
    FriendDecl,
    Function,
    Method,
    Typedef,
    UsingAlias,
    UsingDecl,
    Variable,
)

from .parserstate import (
    State,
    EmptyBlockState,
    ClassBlockState,
    ExternBlockState,
    NamespaceBlockState,
)


class CxxVisitor(Protocol):
    """
    Defines the interface used by the parser to emit events
    """

    def on_define(self, state: State, content: str) -> None:
        """
        .. warning:: cxxheaderparser intentionally does not have a C preprocessor
                     implementation. If you are parsing code with macros in it,
                     use a conforming preprocessor like ``pcpp``
        """

    def on_pragma(self, state: State, content: str) -> None:
        """
        Called once for each ``#pragma`` directive encountered
        """

    def on_include(self, state: State, filename: str) -> None:
        """
        Called once for each ``#include`` directive encountered
        """

    def on_empty_block_start(self, state: EmptyBlockState) -> None:
        """
        Called when a ``{`` is encountered that isn't associated with or
        consumed by other declarations.

        .. code-block:: c++

            {
                // stuff
            }
        """

    def on_empty_block_end(self, state: EmptyBlockState) -> None:
        ...

    def on_extern_block_start(self, state: ExternBlockState) -> None:
        """
        .. code-block:: c++

            extern "C" {

            }

        """

    def on_extern_block_end(self, state: ExternBlockState) -> None:
        ...

    def on_namespace_start(self, state: NamespaceBlockState) -> None:
        """
        Called when a ``namespace`` directive is encountered
        """

    def on_namespace_end(self, state: NamespaceBlockState) -> None:
        """
        Called at the end of a ``namespace`` block
        """

    def on_forward_decl(self, state: State, fdecl: ForwardDecl) -> None:
        """
        Called when a forward declaration is encountered
        """

    def on_variable(self, state: State, v: Variable) -> None:
        ...

    def on_function(self, state: State, fn: Function) -> None:
        ...

    def on_typedef(self, state: State, typedef: Typedef) -> None:
        """
        Called for each typedef instance encountered. For example:

        .. code-block:: c++

            typedef int T, *PT;

        Will result in ``on_typedef`` being called twice, once for ``T`` and
        once for ``*PT``
        """

    def on_using_namespace(self, state: State, namespace: typing.List[str]) -> None:
        """
        .. code-block:: c++

            using namespace std;
        """

    def on_using_alias(self, state: State, using: UsingAlias) -> None:
        """
        .. code-block:: c++

            using foo = int;

            template <typename T>
            using VectorT = std::vector<T>;

        """

    def on_using_declaration(self, state: State, using: UsingDecl) -> None:
        """
        .. code-block:: c++

            using NS::ClassName;

        """

    #
    # Enums
    #

    def on_enum(self, state: State, enum: EnumDecl) -> None:
        """
        Called after an enum is encountered
        """

    #
    # Class/union/struct
    #

    def on_class_start(self, state: ClassBlockState) -> None:
        """
        Called when a class/struct/union is encountered

        When part of a typedef:

        .. code-block:: c++

            typedef struct { } X;

        This is called first, followed by on_typedef for each typedef instance
        encountered. The compound type object is passed as the type to the
        typedef.
        """

    def on_class_field(self, state: ClassBlockState, f: Field) -> None:
        """
        Called when a field of a class is encountered
        """

    def on_class_friend(self, state: ClassBlockState, friend: FriendDecl) -> None:
        """
        Called when a friend declaration is encountered
        """

    def on_class_method(self, state: ClassBlockState, method: Method) -> None:
        """
        Called when a method of a class is encountered
        """

    def on_class_end(self, state: ClassBlockState) -> None:
        """
        Called when the end of a class/struct/union is encountered.

        When a variable like this is declared:

        .. code-block:: c++

            struct X {

            } x;

        Then ``on_class_start``, .. ``on_class_end`` are emitted, along with
        ``on_variable`` for each instance declared.
        """
