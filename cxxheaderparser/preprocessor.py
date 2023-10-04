"""
Contains optional preprocessor support via pcpp
"""

import io
import re
import os
import typing
from .options import PreprocessorFunction

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


def make_pcpp_preprocessor(
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

        pp.parse(content, filename)

        if pp.errors:
            raise PreprocessorError("\n".join(pp.errors))
        elif pp.return_code:
            raise PreprocessorError("failed with exit code %d" % pp.return_code)

        fp = io.StringIO()
        pp.write(fp)
        fp.seek(0)
        if retain_all_content:
            return fp.read()
        else:
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

            return _filter_self(filename, fp)

    return _preprocess_file
