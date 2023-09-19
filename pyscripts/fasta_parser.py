#!/usr/bin/env python3

import argparse
import io
import re
import typing
import textwrap


def parse_fasta(
    file: typing.TextIO,
    predicate: typing.Callable[[str], bool],
) -> typing.Generator[typing.Tuple[str, str], None, None]:
    header = ""
    seq = io.StringIO("")
    keep = False
    for line in file:
        if line.startswith(">"):
            if keep:
                # yield the previous entry
                yield header, seq.getvalue()
            header = line.strip()
            # check whether it is true by filtered predicate
            keep = predicate(header)
            seq = io.StringIO("")
        elif keep:
            # if predicate true keep all the sequence
            seq.write(line.strip())
        else:
            # otherwise drop the line
            continue
    if keep:
        yield header, seq.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser("fasta_filter")
    parser.add_argument(
        "inputfile",
        metavar="<FASTA file>",
        type=argparse.FileType("r"),
        default="-",
        help="input FASTA file (support pipe from STDIN)",
    )
    parser.add_argument(
        "terms",
        metavar="<Search term>",
        type=str,
        nargs="+",
        help="Terminolgy to search the candidate gene",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="",
        type=argparse.FileType("w+"),
        help="Save filtered FASTA to text file",
    )

    args = parser.parse_args()

    # compile the search terms to reduce the overhead
    # the empty term will be filtered
    regex_all = [re.compile(term) for term in args.terms if term.strip()]

    if not regex_all:
        parser.error("No terminolgy was provided.")

    # predicate function using regex compile
    pred = lambda header: any(regex.search(header) for regex in regex_all)

    for header, seq in parse_fasta(args.inputfile, pred):
        print(header)
        print(seq)
        if args.output is not None:
            print(header, file=args.output)
            print("\n".join(textwrap.wrap(seq, width=80)), file=args.output)


if __name__ == "__main__":
    main()
