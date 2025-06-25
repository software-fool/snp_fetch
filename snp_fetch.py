import sys
import gzip
from warnings import warn

from argparse import ArgumentParser

from Bio import Entrez
import numpy as np

class LookupError(Exception):
    pass


Entrez.email = "foo@gmail.com"
Entrez.api_key = None

def spew(s: str):
    print(s, file=sys.stderr)


def get_rsid(chromosome: str, base_position: str, search_term: str, verbose: bool = False) -> str:
    def _do_search(search_term: str):

        query = f'((({chromosome}[Chromosome]) AND {base_position}[{search_term}]) AND "snv"[SNP Class]) NOT "merged rs"[Filter]'
        if verbose:
            spew(f"Sending query '{query}'")
        eShandle = Entrez.esearch(
            db="snp",
            term=query,
            sort="SNP_ID",
            usehistory="y",
            retmax=20)
        res = Entrez.read(eShandle)
        if verbose:
            for k in res.keys():
                spew(f"  key={k}: value={res[k]}")
        return res

    res = _do_search(search_term)
    if verbose:
        spew(f"search for {chromosome} and {base_position}[{search_term}] yielded {res['IdList']}")
    if len(res["IdList"]) > 0:
        return f"rs{res["IdList"][0]}"
    else:
        return ""


def process_one_file(fname, verbose=False):
    # old name is XXXXXX.txt.gz, ".txt.gz" is 7 characters so
    # drop the last 7 characters, replace with "_new.txt.gz
    new_fname = fname[:-7] + "_new.txt.gz"
    new_lines = []
    data_lines = False
    search_term = None
    errors = []
    with gzip.open(new_fname, "wt") as outfob:
        with gzip.open(fname, "rt") as infob:
            if verbose:
                spew(f"opening {fname} for in, {new_fname} for out")
            for idx, line in enumerate(infob.readlines()):
                if line.startswith("#"):
                    if "genome_build" in line:
                        wds = line[:-1].split("=")
                        if wds[1] in ("GRCh37", "hg19"):
                            search_term = "Base Position Previous"
                        else:
                            search_term = "Base Position"
                        print(f"found genome build {wds[1]} using {search_term}")
                    new_lines.append(line[:-1])
                elif line.startswith("chr"):
                    new_lines.append(f"rsID\t{line[:-1]}")
                    data_lines = True
                elif data_lines:
                    words = line.split()
                    chromosome, base_position = words[0], words[1]
                    rs_id = get_rsid(chromosome, base_position, search_term, verbose)
                    if not rs_id:
                        errors.append(line[:-1])
                    new_line = "\t".join([rs_id] + words)
                    new_lines.append(new_line)
        for err in errors:
            new_lines.append(f"#{err}")
        print(f"Number of missing rsIDs {len(errors)}")
        outfob.write("\n".join(new_lines) + "\n")


def process_files(fnames, verbose=False):
    for fname in fnames:
        process_one_file(fname, verbose)


def main(cla):
    parser = ArgumentParser(description="Retrieve the rs IDs from the SNP database for chromosome names and positions")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Explain what is happening when running")
    parser.add_argument(
        "files",
        metavar="FILES",
        nargs="+",
        help="Files that need processing, new files will be insert '_new' before txt.gz"
    )
    args = parser.parse_args(cla)
    return process_files(args.files, args.verbose)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
