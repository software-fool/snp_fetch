import sys
import re
import gzip
from argparse import ArgumentParser


def process_file(fname: str, items: set, col: int = 0):
    with open(fname, "rt") as fob:
        for line in fob.readlines():
            line = line.strip()
            words = line.split()
            items.add(words[col])


def process_files(base_fnames: list[str], removed_fnames: list[str], base_col: int = 0, removed_col: int = 0):
    base_set = set()
    removed_set = set()
    for fname in base_fnames:
        process_file(fname, base_set, base_col)
    for fname in removed_fnames:
        process_file(fname, removed_set, removed_col)
    return base_set - removed_set


def main(cla):
    parser = ArgumentParser(
        description="Identify set of items in first set of files not in second set of files"
    )
    parser.add_argument(
        "-b",
        "--base",
        nargs="+",
        metavar="BASE-FILE",
        help="Files containing all the available ids",
    )
    parser.add_argument(
        "-r",
        "--removed",
        nargs="+",
        metavar="REMOVES-FILE",
        help="Files containing rejected/unused ids",
    )
    parser.add_argument(
        "-c",
        "--col",
        type=int,
        default=0,
        help="Column to use for both types of file",
    )
    parser.add_argument(
        "--base-col",
        type=int,
        default=None,
        help="Column to use for the base files",
    )
    parser.add_argument(
        "--removed-col",
        type=int,
        default=None,
        help="Column to use for the removed files",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename"
    )
    args = parser.parse_args(cla)
    if not args.base:
        print(f"{sys.argv[0]}: usage: must supply one or more base files")
        return 1
    if not args.removed:
        print(f"{sys.argv[0]}: usage: must supply one or more removed files")
        return 1
    if args.base_col is None:
        args.base_col = args.col
    if args.removed_col is None:
        args.removed_col = args.col
    unused_items = process_files(
        args.base, args.removed, args.base_col, args.removed_col)
    fob = sys.stdout
    if args.output:
        fob = open(args.output, "wt")
    for item in unused_items:
        print(f"{item}", file=fob)
    return 0
        

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
