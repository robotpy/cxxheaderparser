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

.. automodule:: cxxheaderparser.types
   :members:
   :undoc-members:

exceptions
----------

.. automodule:: cxxheaderparser.errors
   :members:
   :undoc-members: