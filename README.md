# FASTA Filter CLI Tools Documentation

## Overview

The FASTA Filter CLI Tools crate is a command-line utility designed for filtering FASTA format files based on user-defined search terms. FASTA files are commonly used in bioinformatics to represent nucleotide or protein sequences. This crate allows users to specify one or more search terms, and it will filter the input FASTA file to retain only those sequences whose headers (lines starting with ">") contain at least one of the specified search terms by regex expression. The filtered sequences can be saved to a separate output file.

## Usage

To use this crate, you should have Rust installed on your system. You can run the crate from the command line as follows:

```bash
cargo run -r -- <FASTA file> <Search term> [--output <output file>]
```

### Arguments

- `<FASTA file>`: The path to the input FASTA file that you want to filter. You can also use a pipe (`|`) to provide input from standard input (STDIN).

- `<Search term>`: One or more search terms to filter the FASTA file. The crate will retain sequences whose headers contain at least one of these terms.

- `--output <output file>` or `-o <output file>` (optional): If provided, this argument specifies the name of the output file where the filtered FASTA sequences will be saved. If not provided, the filtered sequences will only be printed to the standard output.

### Example Usage

Here are some example usages of the crate:

1. Filter a FASTA file named `input.fasta` to retain sequences with headers containing the term "gene1" and save the filtered sequences to `output.fasta`:

    ```bash
    cargo run -r -- input.fasta gene1 --output output.fasta
    ```

2. Filter a FASTA file from STDIN (piped input):

    ```bash
    cat input.fasta | cargo run -r -- - unc --output output.fasta
    ```

3. Filter a FASTA GZIP file from STDIN (piped input) :

    ```bash
    cat input.fasta.gz | gzip -d | cargo run -r -- - unc --output output.fasta
    ```

## Example Output

When the crate is run, it prints the headers and sequences of the filtered sequences to the standard output (or the specified output file, if provided). Here's an example of the output:

```
>sequence1
ATCGATCGATCG
>sequence2
GATCGATCGATC
```

## Dependencies

This Rust command-line tool relies on several external crates:

- `clap`: For parsing command-line arguments.
- `clap_stdin`: For handling input from STDIN.
- `regex`: For regular expression matching.
- `seq_io`: For reading and writing FASTA sequences efficiently.

These dependencies are managed using Cargo, Rust's package manager.

## License

This crate is distributed under the MIT License.

## Author

This crate was authored by Chung-Kuan Chen (b97b01045@gmail.com).

---

**Note**: Replace `<FASTA file>`, `<Search term>`, and `<output file>` with the actual file paths and search terms you want to use.