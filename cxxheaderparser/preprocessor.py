"""
Contains optional preprocessor support via pcpp
"""

import io
import re
import os
from os.path import relpath
import typing
from .options import PreprocessorFunction

from time import monotonic

from pcpp import Preprocessor, OutputDirective, Action


class PreprocessorError(Exception):
    pass


class _CustomPreprocessor(Preprocessor):
    def __init__(self, encoding: typing.Optional[str]):
        Preprocessor.__init__(self)
        self.errors: typing.List[str] = []
        self.assume_encoding = encoding

    def on_error(self, file, line, msg):
        self.errors.append(f"{file}:{line} error: {msg}")

    def on_include_not_found(self, *ignored):
        raise OutputDirective(Action.IgnoreAndPassThrough)

    def on_comment(self, *ignored):
        return True


def _filter_self(fname: str, fp: typing.TextIO) -> str:
    # the output of pcpp includes the contents of all the included files, which
    # isn't what a typical user of cxxheaderparser would want, so we strip out
    # the line directives and any content that isn't in our original file

    line_ending = f'{fname}"\n'

    new_output = io.StringIO()
    keep = True

    for line in fp:
        if line.startswith("#line"):
            keep = line.endswith(line_ending)

        if keep:
            new_output.write(line)

    new_output.seek(0)
    return new_output.read()


class PPTime:
    def __init__(self) -> None:
        self.start = monotonic()
        self.files = 0
        self.parse_total: float = 0
        self.write_total: float = 0
        self.filter_total: float = 0

    def report(self):
        total = monotonic() - self.start
        print("-- report --")
        print(f" files={self.files} total_time={total:.5f}")
        print(
            f" preprocessor: parse={self.parse_total:.5f}, write={self.write_total:.5f}, filter={self.filter_total:.5f}"
        )


def make_pcpp_preprocessor(
    pptime: PPTime,
    *,
    defines: typing.List[str] = [],
    include_paths: typing.List[str] = [],
    retain_all_content: bool = False,
    encoding: typing.Optional[str] = None,
) -> PreprocessorFunction:
    """
    Creates a preprocessor function that uses pcpp (which must be installed
    separately) to preprocess the input text.

    :param encoding: If specified any include files are opened with this encoding

    .. code-block:: python

        pp = make_pcpp_preprocessor()
        options = ParserOptions(preprocessor=pp)

        parse_file(content, options=options)

    """

    def _preprocess_file(filename: str, content: str) -> str:
        pp = _CustomPreprocessor(encoding)
        if include_paths:
            for p in include_paths:
                pp.add_path(p)

        for define in defines:
            pp.define(define)

        if not retain_all_content:
            pp.line_directive = "#line"

        pptime.files += 1

        now = monotonic()
        pp.parse(content, filename)
        pptime.parse_total += monotonic() - now

        if pp.errors:
            raise PreprocessorError("\n".join(pp.errors))
        elif pp.return_code:
            raise PreprocessorError("failed with exit code %d" % pp.return_code)

        now = monotonic()
        fp = io.StringIO()
        pp.write(fp)
        fp.seek(0)
        pptime.write_total += monotonic() - now
        if retain_all_content:
            return fp.read()
        else:
            now = monotonic()

            # pcpp emits the #line directive using the filename you pass in
            # but will rewrite it if it's on the include path it uses. This
            # is copied from pcpp:
            abssource = os.path.abspath(filename)
            for rewrite in pp.rewrite_paths:
                temp = re.sub(rewrite[0], rewrite[1], abssource)
                if temp != abssource:
                    filename = temp
                    if os.sep != "/":
                        filename = filename.replace(os.sep, "/")
                    break

            flt = _filter_self(filename, fp)
            pptime.filter_total += monotonic() - now
            return flt

    return _preprocess_file
