#!/usr/bin/env python3

"""
    usage:
        python3 motifcli.py --input path/to/file.fasta --k 6 --top 10 [--min-gc 0.5]

    This script analyzes DNA sequences to identify frequent k-mers (motifs).
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# IMPORTS
import sys
import motiftools
import argparse
import pathlib


# CLASSES
class Motifcli:
    """
    Command-line interface for motif analysis in DNA sequences.

    This class reads DNA sequences from a FASTA file, counts k-mers of a specified length,
    identifies the most frequent k-mers (motifs), and optionally filters motifs by minimum GC content.
    """

    def __init__(self) -> None:
        # Parse command-line arguments
        self.args = self.argparser()

        # Read sequences from FASTA file
        self.sequences = self.read_fasta()

        # Count all k-mers
        self.kmers = self.count_kmers()

        # Get top N most frequent k-mers
        self.top = self.get_top()

        # Optionally filter by GC content
        self.min_filtered = None
        if self.args.min_gc:
            self.min_filtered = self.get_filtered()

        # Output results
        self.print_info()

    def read_fasta(self):
        """
        Reads DNA sequences from a FASTA file, ignoring header lines.
        """
        with open(self.args.input, "r") as fasta_f:
            sequences = [line.strip() for line in fasta_f if ">" not in line]
        return sequences

    def count_kmers(self):
        """
        Counts k-mers in the sequences using motiftools.
        """
        return motiftools.count_kmers(self.sequences, self.args.k)

    def get_top(self):
        """
        Finds the top k-mers by frequency.
        """
        return motiftools.find_top_kmers(self.kmers, self.args.top)

    def get_filtered(self):
        """
        Filters k-mers by a minimum GC content threshold.
        """
        return motiftools.filter_kmers_by_gc(self.kmers, self.args.min_gc)

    def print_info(self):
        """
        Prints the most frequent k-mers and any that meet the GC content filter.
        """
        print(f"Top {self.args.top} motifs (k={self.args.k}):")
        for kmer in self.top:
            print(f"{kmer[0]} - {kmer[1]}")  # (k-mer, count)

        if self.min_filtered:
            print(f"Filtered by GC content > {int(self.args.min_gc * 100)}%:")
            print("\n".join(self.min_filtered))

    def argparser(self):
        """
        Parses command-line arguments.
        """
        parser = argparse.ArgumentParser(
            description="Find and filter DNA motifs from a FASTA file."
        )
        parser.add_argument(
            "--input",
            required=True,
            type=pathlib.Path,
            help="Path to FASTA input file.",
        )
        parser.add_argument(
            "--k", required=True, type=int, help="Length of k-mers to search for."
        )
        parser.add_argument(
            "--top", required=True, type=int, help="Number of top motifs to return."
        )
        parser.add_argument(
            "--min-gc", type=float, help="Minimum GC content for filtering (0–1)."
        )
        return parser.parse_args()


# MAIN
def main(args):
    """
    Entry point for the script.
    """
    motifcli = Motifcli()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
