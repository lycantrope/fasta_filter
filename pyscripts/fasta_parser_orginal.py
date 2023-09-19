#!/usr/bin/env python3
# @Author Peter Carlton

import sys
import re


def parse_fasta(file_path):
    with open(file_path, "r") as f:
        sequences = {}
        header = None
        seq = ""
        for line in f:
            if line.startswith(">"):
                if header:
                    sequences[header] = seq
                header = line.strip()
                seq = ""
            else:
                seq += line.strip()
        if header:
            sequences[header] = seq
    return sequences


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: ./fasta_filter_simple.py <FASTA file> <search term 1> <search term 2> ..."
        )
        sys.exit(1)

    fasta_file = sys.argv[1]
    search_terms = sys.argv[2:]

    sequences = parse_fasta(fasta_file)

    for header, seq in sequences.items():
        if any(re.search(term, header) for term in search_terms):
            print(header)
            print(seq)


if __name__ == "__main__":
    main()
