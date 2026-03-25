import inspect

from cxxheaderparser.simple import parse_string


def test_lineno_basic() -> None:
    content = """
    namespace N {
        typedef char *ABC;
        using Str = const char*;
        enum Color { RED, GREEN };
        extern int g;
        void f(int x);
        class C { public: int m; void meth(); };
    }
    """

    data = parse_string(content, cleandoc=True)
    ns = data.namespace.namespaces.get("N", data.namespace)
    lines = inspect.cleandoc(content).splitlines()

    def lineno_for(substr: str) -> int:
        for i, l in enumerate(lines):
            if substr in l:
                return i + 1
        raise AssertionError(f"could not find {substr!r} in sample")

    # typedef
    assert len(ns.typedefs) >= 1
    assert getattr(ns.typedefs[0], "lineno", None) == lineno_for("typedef char *ABC")

    # using alias
    assert len(ns.using_alias) >= 1
    assert getattr(ns.using_alias[0], "lineno", None) == lineno_for("using Str =")

    # enum
    assert len(ns.enums) >= 1
    assert getattr(ns.enums[0], "lineno", None) == lineno_for("enum Color")

    # variable
    assert len(ns.variables) >= 1
    assert getattr(ns.variables[0], "lineno", None) == lineno_for("extern int g")

    # function
    assert len(ns.functions) >= 1
    assert getattr(ns.functions[0], "lineno", None) == lineno_for("void f(int x)")

    # class + class members
    assert len(ns.classes) >= 1
    cls = ns.classes[0]
    assert getattr(cls, "lineno", None) == lineno_for("class C")
    # fields and methods
    assert len(cls.fields) >= 1
    assert getattr(cls.fields[0], "lineno", None) == lineno_for("int m")
    assert len(cls.methods) >= 1
    assert getattr(cls.methods[0], "lineno", None) == lineno_for("void meth")
