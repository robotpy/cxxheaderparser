import argparse
import dataclasses
import json
import pprint
import subprocess
import sys

from .options import ParserOptions
from .simple import parse_file


def dumpmain() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("header")
    parser.add_argument(
        "-w",
        "--width",
        default=80,
        type=int,
        help="Width of output when in pprint mode",
    )
    parser.add_argument("-v", "--verbose", default=False, action="store_true")
    parser.add_argument(
        "--mode", choices=["json", "pprint", "repr", "brepr"], default="pprint"
    )

    args = parser.parse_args()

    options = ParserOptions(verbose=args.verbose)
    data = parse_file(args.header, options=options)

    if args.mode == "pprint":
        ddata = dataclasses.asdict(data)
        pprint.pprint(ddata, width=args.width, compact=True)

    elif args.mode == "json":
        ddata = dataclasses.asdict(data)
        json.dump(ddata, sys.stdout, indent=2)

    elif args.mode == "brepr":
        stmt = repr(data)
        stmt = subprocess.check_output(
            ["black", "-", "-q"], input=stmt.encode("utf-8")
        ).decode("utf-8")

        print(stmt)

    elif args.mode == "repr":
        print(data)

    else:
        parser.error("Invalid mode")
