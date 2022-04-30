import argparse
import dataclasses
import inspect
import subprocess
import typing

from .options import ParserOptions
from .simple import parse_string, ParsedData


def nondefault_repr(data: ParsedData) -> str:
    """
    Similar to the default dataclass repr, but exclude any
    default parameters or parameters with compare=False
    """

    is_dataclass = dataclasses.is_dataclass
    get_fields = dataclasses.fields
    MISSING = dataclasses.MISSING

    def _inner_repr(o: typing.Any) -> str:
        if is_dataclass(o):
            vals = []
            for f in get_fields(o):
                if f.repr and f.compare:
                    v = getattr(o, f.name)
                    if f.default_factory is not MISSING:
                        default = f.default_factory()
                    else:
                        default = f.default

                    if v != default:
                        vals.append(f"{f.name}={_inner_repr(v)}")

            return f"{o.__class__.__qualname__ }({', '.join(vals)})"

        elif isinstance(o, list):
            return f"[{','.join(_inner_repr(l) for l in o)}]"
        elif isinstance(o, dict):
            vals = []
            for k, v in o.items():
                vals.append(f'"{k}": {_inner_repr(v)}')
            return "{" + ",".join(vals) + "}"
        else:
            return repr(o)

    return _inner_repr(data)


def gentest(infile: str, name: str, outfile: str, verbose: bool) -> None:
    # Goal is to allow making a unit test as easy as running this dumper
    # on a file and copy/pasting this into a test

    with open(infile, "r") as fp:
        content = fp.read()

    options = ParserOptions(verbose=verbose)

    data = parse_string(content, options=options)

    stmt = nondefault_repr(data)

    content = content.replace("\n", "\n              ")

    stmt = inspect.cleandoc(
        f'''
    
        def test_{name}() -> None:
            content = """
              {content}
            """
            data = parse_string(content, cleandoc=True)

            assert data == {stmt}
    
    '''
    )

    # format it with black
    stmt = subprocess.check_output(
        ["black", "-", "-q"], input=stmt.encode("utf-8")
    ).decode("utf-8")

    if outfile == "-":
        print(stmt)
    else:
        with open(outfile, "w") as fp:
            fp.write(stmt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("header")
    parser.add_argument("name", nargs="?", default="TODO")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")
    parser.add_argument("-o", "--output", default="-")
    args = parser.parse_args()

    gentest(args.header, args.name, args.output, args.verbose)
