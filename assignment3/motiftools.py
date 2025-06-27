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


# FUNCTIONS
def kmer_generator(seq: str, k: int):
    i = 0
    while i <= len(seq) - k:
        yield seq[i : i + k]
        i += 1


def count_kmers(sequences: list[str], k: int):
    kmer_dict = {}
    for sequence in sequences:
        for kmer in kmer_generator(sequence, k):
            if kmer in kmer_dict:
                kmer_dict[kmer] += 1
            else:
                kmer_dict[kmer] = 1

    return kmer_dict


def find_top_kmers(kmer_counts: dict[str, int], top_n: int = 10):
    return sorted(kmer_counts.items(), key=lambda key: key[1], reverse=True)[:top_n]


def gc_content(seq: str) -> float:
    gc_count = sum(1 for nuc in seq if nuc in "GCgc")
    return gc_count / len(seq)


def filter_kmers_by_gc(kmer_counts: dict[str, int], min_gc: float):
    kmer_pass = []
    for kmer in kmer_counts.keys():
        if gc_content(kmer) > min_gc:
            kmer_pass.append(kmer)
    return kmer_pass


# MAIN
def main(args):
    """Main function"""
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
