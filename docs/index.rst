.. cxxheaderparser documentation master file, created by
   sphinx-quickstart on Thu Dec 31 00:46:02 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

cxxheaderparser
===============

A pure python C++ header parser that parses C++ headers in a mildly naive
manner that allows it to handle many C++ constructs, including many modern
(C++11 and beyond) features.

.. warning:: cxxheaderparser intentionally does not have a C preprocessor
             implementation! If you are parsing code with macros in it, use
             a conforming preprocessor like the pure python preprocessor
             `pcpp`_ or your favorite C++ compiler.

.. _pcpp: https://github.com/ned14/pcpp

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tools
   simple
   custom
   types



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

