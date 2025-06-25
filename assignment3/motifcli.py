#!/usr/bin/env python3

"""
    usage:
        python3 orfeas_gkourlias_deelopdracht01.py
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.1"

# IMPORTS
import sys
import motiftools
import argparse
import pathlib

# CLASSES
class Motifcli():
    """ Desc """
    def __init__(self) -> None:
        self.args = self.argparser()
        self.sequences = self.read_fasta()
        self.kmers = self.count_kmers()
        self.top = self.get_top()
        self.min_filtered = None
        if self.args.min_gc:
            self.min_filtered = self.get_filtered()
        self.print_info()

    def read_fasta(self):
        with open(self.args.input, "r") as fasta_f:
            sequences = [line.strip() for line in fasta_f if ">" not in line]
        return sequences
    
    def count_kmers(self):
        return motiftools.count_kmers(self.sequences, self.args.k)
    
    def get_top(self):
        return motiftools.find_top_kmers(self.kmers, self.args.top)
    
    def get_filtered(self):
        return motiftools.filter_kmers_by_gc(self.kmers, self.args.min_gc)
    
    def print_info(self):
        print(f"Top {self.args.top} motifs (k={self.args.k}):")
        for kmer in self.top:
            print(f"{kmer[0]} - {kmer[1]}")

        if self.min_filtered:
            print(f"Filtered by GC content > {int(self.args.min_gc * 100)}%:")
            print("\n".join(self.min_filtered))


    def argparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True, type=pathlib.Path)
        parser.add_argument("--k", required=True, type=int)
        parser.add_argument("--top", required=True, type=int)
        parser.add_argument("--min-gc", type=float)
        return(parser.parse_args())
    
# MAIN
def main(args):
    """ Main function """
    motifcli = Motifcli()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
