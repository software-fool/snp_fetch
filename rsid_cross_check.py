import sys
import re
import gzip
from argparse import ArgumentParser
from collections import defaultdict


def process_files(files: list[str]):
    id_map = defaultdict(list)
    for fname in files:
        with gzip.open(fname, "rt") as fob:
            for line in fob.readlines():
                line = line.strip()
                if line.startswith("#"):
                    continue
                words = line.split()
                rsid = words[0]
                if re.match(r"^rs\d+", rsid):
                    id_map[rsid].append(fname)
    return id_map

def summarize_results(id_map: dict[str, list[str]], filter: int = 2):
    order = defaultdict(list)
    for k, v in id_map.items():
        if len(v) >= filter:
            order[len(v)].append((k, v))
    return order


def main(cla):
    parser = ArgumentParser(
        description="Tool to cross check which rsIDs occur in different score files"
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List the files the rsID is found in as well as count",
    )
    parser.add_argument(
        "-t",
        "--table",
        action="store_true",
        help="Print results as a tab delimited table for easier ingestion to other tools",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="Files to search for rsIDs",
    )                        
    args = parser.parse_args(cla)
    if args.list and args.table:
        print(f"{sys.argv[0]}: cannot specify both table and list together")
        return 1
    id_map = process_files(args.files)
    order = summarize_results(id_map)
    count = 0
    if args.table:
        print("rsID\tcount")
    for k in sorted(order.keys()):
        entry = order[k]
        for e in entry:
            if args.table:
                print(f"{e[0]}\t{k}")
            else:
                print(f"{e[0]}: {k}")
            if args.list:
                for fn in set(e[1]):
                    print(f"    {fn}")
        count += len(entry)
    if not args.table:
        print(f"{count} rsIDs found across {len(args.files)} files")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
