Types
=====

parser types
------------

.. versionchanged:: 2.0
   Member object pointers and member function pointers are now represented by
   :py:class:`cxxheaderparser.types.MemberPointer`. Previously, member function
   pointers were represented by a :py:class:`cxxheaderparser.types.Pointer`
   containing a :py:class:`cxxheaderparser.types.FunctionType` whose
   ``classname`` attribute identified the owning class. This is a breaking
   change to the parsed type dataclasses.

   ``FunctionType`` is included in ``TypeId`` for contexts that accept a bare
   function type, including aliases, typedefs, template arguments, and
   ``parse_typename``. ``DecoratedType`` remains the set of object/declarator
   types used by variables, fields, adjusted parameters, and function returns.

.. automodule:: cxxheaderparser.types
   :members:
   :undoc-members:

exceptions
----------

.. automodule:: cxxheaderparser.errors
   :members:
   :undoc-members: