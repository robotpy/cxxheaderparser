#
# This file is not distributed with cxxheaderparser, it is only
# used from the web demo
#

import asyncio
import dataclasses
import io
import os
import traceback

import pyodide
from pyodide.http import pyfetch
import js


def webrepr(data, defaults: bool = False, mxlen: int = 88) -> str:
    """
    A dumb black-like formatter for use on the cxxheaderparser webpage, which cannot
    use black.

    No guarantees are provided for this dumper. It probably generates valid python
    most of the time.
    """

    fp = io.StringIO()

    def _format(item, curlen: int, indent: str):
        # see if the default representation fits
        r = repr(item)
        if len(r) + curlen <= mxlen:
            fp.write(r)
            return

        # got to expand the item. Depends on what it is
        newindent = indent + "  "
        if isinstance(item, list):
            fp.write("[\n")
            curlen = len(newindent)
            for li in item:
                fp.write(newindent)
                _format(li, curlen, newindent)
                fp.write(",\n")
            fp.write(f"{indent}]")
        elif isinstance(item, dict):
            fp.write("{\n")
            curlen = len(newindent)
            for k, v in item.items():
                curlen = fp.write(f"{newindent}{k!r}:")
                _format(v, curlen, newindent)
                fp.write(",\n")
            fp.write(f"{indent}}}")
        elif dataclasses.is_dataclass(item):
            # always write the name, then process like a dict
            fp.write(f"{item.__class__.__qualname__}(\n")
            fields = dataclasses.fields(item)
            written = False
            for field in fields:
                # check to see if this is a default value, exclude those
                v = getattr(item, field.name)
                if not defaults and field.repr and field.compare:
                    if field.default_factory is not dataclasses.MISSING:
                        default = field.default_factory()
                    else:
                        default = field.default
                    if v == default:
                        continue
                curlen = fp.write(f"{newindent}{field.name}=")
                _format(v, curlen, newindent)
                fp.write(",\n")
                written = True
            if written:
                fp.write(indent)
            fp.write(")")
        else:
            # I give up, just write it. It's probably fine.
            fp.write(r)

    _format(data, 0, "")
    return fp.getvalue()


def make_input_function():

    from cxxheaderparser.errors import CxxParseError
    from cxxheaderparser.options import ParserOptions
    from cxxheaderparser.simple import parse_string

    pp_options = None

    if js.pcpp.checked:
        from cxxheaderparser.preprocessor import make_pcpp_preprocessor

        pp_options = ParserOptions(preprocessor=make_pcpp_preprocessor())

    def on_input(*ignored):
        options = None
        if js.pcpp.checked:
            options = pp_options

        try:
            data = parse_string(js.editor.getValue(), options=options)
        except Exception as e:
            if not isinstance(e, CxxParseError) or js.verbose.checked:
                js.out.innerHTML = "Exception:\n" + "\n".join(
                    traceback.format_exception(e, chain=True)
                )
            else:
                js.out.innerHTML = str(e)
        else:
            js.out.innerHTML = webrepr(data)

    return on_input


async def dl(fname):
    response = await pyfetch(fname)
    with open(fname, "wb") as fp:
        fp.write(await response.bytes())

    js.addStatus(".. " + fname)


async def load_cxxheaderparser():
    os.mkdir("cxxheaderparser")
    os.mkdir("cxxheaderparser/_ply")

    files = [
        "cxxheaderparser/__init__.py",
        "cxxheaderparser/__main__.py",
        "cxxheaderparser/dump.py",
        "cxxheaderparser/errors.py",
        "cxxheaderparser/gentest.py",
        "cxxheaderparser/lexer.py",
        "cxxheaderparser/options.py",
        "cxxheaderparser/parser.py",
        "cxxheaderparser/preprocessor.py",
        "cxxheaderparser/parserstate.py",
        "cxxheaderparser/_ply/__init__.py",
        "cxxheaderparser/_ply/lex.py",
        "cxxheaderparser/simple.py",
        "cxxheaderparser/tokfmt.py",
        "cxxheaderparser/types.py",
        "cxxheaderparser/version.py",
        "cxxheaderparser/visitor.py",
    ]

    js.addStatus("Loading cxxheaderparser...")

    await asyncio.gather(*[dl(f) for f in files])

    js.addStatus("OK")
