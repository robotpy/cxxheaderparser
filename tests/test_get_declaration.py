import pytest

from cxxheaderparser import simple
from cxxheaderparser.types import (
    FundamentalSpecifier,
    Function,
    Method,
    NameSpecifier,
    Parameter,
    PQName,
    Type,
)


def test_get_declaration_doxygen():
    data = simple.parse_string("""
        namespace name {
        /** @brief My first function. */
        int foo(int a);
        /** This is a class */
        class Bar {
        public:
            /** @brief Some counter */
            int count();
        };
        }
        """)
    assert simple.get_declaration(data, "name::foo") == Function(
        return_type=Type(PQName([FundamentalSpecifier("int")])),
        name=PQName([NameSpecifier("foo")]),
        parameters=[
            Parameter(type=Type(PQName([FundamentalSpecifier("int")])), name="a")
        ],
        doxygen="/** @brief My first function. */",
    )
    ns = data.namespace.namespaces["name"]
    assert simple.get_declaration(data, "name::foo") is ns.functions[0]
    assert simple.get_declaration(data, "name::Bar::count") is ns.classes[0].methods[0]
    cls = simple.get_declaration(data, "name::Bar")
    assert cls is data.namespace.namespaces["name"].classes[0]
    assert cls.class_decl.doxygen == "/** This is a class */"
    assert simple.get_declaration(data, "name::Bar::count") == Method(
        return_type=Type(PQName([FundamentalSpecifier("int")])),
        name=PQName([NameSpecifier("count")]),
        parameters=[],
        access="public",
        doxygen="/** @brief Some counter */",
    )


@pytest.mark.parametrize("prefix", ["", "::"])
def test_get_declaration_nested_scopes(prefix):
    data = simple.parse_string(
        "namespace a { namespace b { struct Outer { struct Inner { int x; }; }; } }"
    )
    ns = data.namespace.namespaces["a"].namespaces["b"]
    inner = ns.classes[0].classes[0]
    assert simple.get_declaration(data, prefix + "a::b") is ns
    assert simple.get_declaration(data, prefix + "a::b::Outer::Inner") is inner
    assert (
        simple.get_declaration(data, prefix + "a::b::Outer::Inner::x")
        is inner.fields[0]
    )


@pytest.mark.parametrize(
    "name", ["missing", "n::missing", "x::member", "", "::", "n::"]
)
def test_get_declaration_missing(name):
    data = simple.parse_string("int x; namespace n { int x; }")
    with pytest.raises(KeyError) as exc:
        simple.get_declaration(data, name)
    assert name in str(exc.value)


@pytest.mark.parametrize(
    "source, name",
    [
        ("void f(); void f(int);", "f"),
        ("void f(); void f();", "f"),
        ("struct C { void f(); void f(int); };", "C::f"),
        ("struct C; struct C {};", "C"),
    ],
)
def test_get_declaration_ambiguous(source, name):
    data = simple.parse_string(source)
    with pytest.raises(LookupError, match=name) as exc:
        simple.get_declaration(data, name)
    assert isinstance(exc.value, simple.AmbiguousNameError)


def test_get_declaration_named_declarations():
    data = simple.parse_string("""
        namespace n {
            int v;
            typedef int T;
            using A = int;
            struct F;
            enum E { one };
            namespace alias = n;
            template<typename T> concept C = true;
            struct S { typedef int T; using A = int; struct F; enum E { one }; };
        }
        """)
    ns = data.namespace.namespaces["n"]
    for scope, prefix in [(ns, "n"), (ns.classes[0], "n::S")]:
        for name, expected in [
            ("T", scope.typedefs[0]),
            ("A", scope.using_alias[0]),
            ("F", scope.forward_decls[0]),
            ("E", scope.enums[0]),
            ("E::one", scope.enums[0].values[0]),
        ]:
            assert simple.get_declaration(data, prefix + "::" + name) is expected
    assert simple.get_declaration(data, "n::v") is ns.variables[0]
    assert simple.get_declaration(data, "n::alias") is ns.ns_alias[0]
    assert simple.get_declaration(data, "n::C") is ns.concepts[0]
    with pytest.raises(KeyError):
        simple.get_declaration(data, "n::alias::v")


def test_get_declaration_qualified_declarations():
    data = simple.parse_string(
        "namespace n {} struct n::C { void f(); }; void n::C::f() {}"
    )
    assert simple.get_declaration(data, "n::C") is data.namespace.classes[0]
    with pytest.raises(simple.AmbiguousNameError):
        simple.get_declaration(data, "n::C::f")


def test_get_declaration_absolute_declaration():
    data = simple.parse_string(
        "namespace n { namespace m { struct C; } struct ::n::m::C { int x; }; }"
    )
    cls = data.namespace.namespaces["n"].classes[0]
    assert simple.get_declaration(data, "n::m::C::x") is cls.fields[0]
    with pytest.raises(KeyError):
        simple.get_declaration(data, "n::n::m::C::x")


def test_get_declaration_skips_anonymous_declarations():
    data = simple.parse_string(
        "namespace { int hidden; } struct { int hidden; } value; "
        "enum { hidden }; struct C { int : 1; int x; };"
    )
    assert simple.get_declaration(data, "value") is data.namespace.variables[0]
    assert simple.get_declaration(data, "C::x") is data.namespace.classes[1].fields[1]
    with pytest.raises(KeyError):
        simple.get_declaration(data, "hidden")


def test_get_declaration_specialization():
    data = simple.parse_string(
        "template<typename T> struct C {}; template<> struct C<int> { int x; };"
    )
    assert simple.get_declaration(data, "C") is data.namespace.classes[0]
    assert (
        simple.get_declaration(data, "C<int>::x") is data.namespace.classes[1].fields[0]
    )


@pytest.mark.parametrize("target", ["bool", "const int*", "n::T"])
def test_get_declaration_conversion_operator(target):
    data = simple.parse_string(
        "struct C { operator bool(); operator const int*(); operator n::T(); };"
    )
    index = ["bool", "const int*", "n::T"].index(target)
    assert (
        simple.get_declaration(data, "C::operator " + target)
        is data.namespace.classes[0].methods[index]
    )


@pytest.mark.parametrize("name", [" C < int > :: x ", "::C<int>::x"])
def test_get_declaration_normalizes_template_name(name):
    data = simple.parse_string("template<> struct C<int> { int x; };")
    assert simple.get_declaration(data, name) is data.namespace.classes[0].fields[0]


@pytest.mark.parametrize(
    "name, index",
    [
        (" C :: C ", 0),
        ("C :: ~C", 1),
        ("C :: ~ C", 1),
        (" C :: operator + ", 2),
        ("C :: operator ( )", 3),
        ("C :: operator [ ]", 4),
        ("C :: operator int const *", 5),
    ],
)
def test_get_declaration_normalizes_method_name(name, index):
    data = simple.parse_string(
        "struct C { C(); ~C(); int operator+(int); int operator()(); "
        "int operator[](int); operator const int*(); };"
    )
    assert (
        simple.get_declaration(data, name) is data.namespace.classes[0].methods[index]
    )


@pytest.mark.parametrize(
    "name", ["C<", "C<...>", "C*", "C::operator.", "C::operator bool()"]
)
def test_get_declaration_invalid_name(name):
    data = simple.parse_string("struct C {};")
    with pytest.raises(KeyError) as exc:
        simple.get_declaration(data, name)
    assert exc.value.args == (name,)


def test_get_declaration_operator_template():
    data = simple.parse_string("struct C { template<> int operator()<int>(); };")
    assert (
        simple.get_declaration(data, "C::operator () < int >")
        is data.namespace.classes[0].methods[0]
    )


def test_get_declaration_does_not_search_unrelated_scopes():
    data = simple.parse_string("int x; namespace n { int x; } struct C { int x; };")
    assert simple.get_declaration(data, "x") is data.namespace.variables[0]
    assert (
        simple.get_declaration(data, "n::x")
        is data.namespace.namespaces["n"].variables[0]
    )
    assert simple.get_declaration(data, "C::x") is data.namespace.classes[0].fields[0]
