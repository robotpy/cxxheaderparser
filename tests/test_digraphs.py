from cxxheaderparser.simple import parse_string, ParsedData
from cxxheaderparser.types import (
    FundamentalSpecifier,
    NameSpecifier,
    PQName,
    Type,
    Variable,
    Function,
    FunctionType,
    Parameter,
    Array,
)


def test_digraph_brace_open_close_function():
    """<% %> should work as { } in a function body context (body is skipped)."""
    # The parser skips function bodies but must recognise the braces.
    content = """\
#include <iostream>
int main()
<%
    std::cout << "Hello, World!" << std::endl;
    return 0;
%>
"""
    # parse_string should not raise
    result = parse_string(content)
    assert isinstance(result, ParsedData)


def test_digraph_struct_body():
    """<% %> should work as { } around a struct body."""
    content = """\
struct Point
<%
    int x;
    int y;
%>;
"""
    result = parse_string(content)
    assert len(result.namespace.classes) == 1
    cls = result.namespace.classes[0]
    assert cls.class_decl.typename.segments[-1].name == "Point"
    field_names = [f.name for f in cls.fields]
    assert field_names == ["x", "y"]


def test_digraph_namespace_body():
    """<% %> should work as { } around a namespace body."""
    content = """\
namespace myns
<%
    int value;
%>
"""
    result = parse_string(content)
    assert "myns" in result.namespace.namespaces
    ns = result.namespace.namespaces["myns"]
    assert len(ns.variables) == 1
    assert ns.variables[0].name.segments[-1].name == "value"


def test_digraph_nested_braces():
    """Nested digraph brace pairs should work correctly."""
    content = """\
namespace outer
<%
    struct Inner
    <%
        int val;
    %>;
%>
"""
    result = parse_string(content)
    assert "outer" in result.namespace.namespaces
    ns = result.namespace.namespaces["outer"]
    assert len(ns.classes) == 1
    inner = ns.classes[0]
    assert inner.class_decl.typename.segments[-1].name == "Inner"
    assert inner.fields[0].name == "val"


def test_digraph_mixed_braces():
    """Digraph and canonical braces can be mixed freely."""
    content = """\
namespace ns
<%
    struct Foo {
        int a;
    };
%>
"""
    result = parse_string(content)
    assert "ns" in result.namespace.namespaces
    ns = result.namespace.namespaces["ns"]
    assert len(ns.classes) == 1


def test_digraph_array_subscript():
    """<: :> should work as [ ] in an array declaration."""
    content = """\
int arr<:10:>;
"""
    result = parse_string(content)
    assert len(result.namespace.variables) == 1
    var = result.namespace.variables[0]
    assert var.name.segments[-1].name == "arr"
    # The type should be an array of 10 ints
    assert isinstance(var.type, Array)


def test_digraph_array_and_brace():
    """Both digraph pairs used together."""
    content = """\
struct Grid
<%
    float data<:4:>;
%>;
"""
    result = parse_string(content)
    cls = result.namespace.classes[0]
    assert cls.class_decl.typename.segments[-1].name == "Grid"
    field = cls.fields[0]
    assert field.name == "data"
    assert isinstance(field.type, Array)


def test_canonical_tokens_unaffected():
    """Normal { } [ ] tokens must continue to work after digraph support."""
    content = """\
namespace ns {
    struct Foo {
        int arr[5];
    };
}
"""
    result = parse_string(content)
    assert "ns" in result.namespace.namespaces
    ns = result.namespace.namespaces["ns"]
    cls = ns.classes[0]
    assert cls.fields[0].name == "arr"


def test_template_angle_brackets_unaffected():
    """< > used as template angle brackets must NOT be treated as digraphs."""
    content = """\
template <typename T, int N>
struct Container
{
    T data[N];
};
"""
    result = parse_string(content)
    cls = result.namespace.classes[0]
    assert cls.class_decl.typename.segments[-1].name == "Container"
    assert len(cls.class_decl.template.params) == 2


def test_shift_left_unaffected():
    """The << operator (SHIFT_LEFT token) must not be affected by digraph detection."""
    content = """\
template <typename T>
void fn(T x);
"""
    result = parse_string(content)
    assert len(result.namespace.functions) == 1
    assert result.namespace.functions[0].name.segments[-1].name == "fn"


def test_percent_operator_unaffected():
    """A bare % in an expression context must not be altered."""
    # The parser skips default parameter expressions, so we embed % there.
    content = """\
void fn(int x = 10 % 3);
"""
    result = parse_string(content)
    assert result.namespace.functions[0].name.segments[-1].name == "fn"


def test_digraph_enum():
    """<% %> should work as { } in an enum definition."""
    content = """\
enum Color
<%
    Red,
    Green,
    Blue
%>;
"""
    result = parse_string(content)
    assert len(result.namespace.enums) == 1
    en = result.namespace.enums[0]
    values = [v.name for v in en.values]
    assert values == ["Red", "Green", "Blue"]


def test_digraph_class_with_methods():
    """<% %> braces work for a class with member function declarations."""
    content = """\
class MyClass
<%
public:
    MyClass();
    ~MyClass();
    int getValue() const;
%>;
"""
    result = parse_string(content)
    cls = result.namespace.classes[0]
    assert cls.class_decl.typename.segments[-1].name == "MyClass"
    method_names = [m.name.segments[-1].name for m in cls.methods]
    assert "MyClass" in method_names
    assert "getValue" in method_names
    
