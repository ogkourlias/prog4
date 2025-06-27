#!/usr/bin/env python3

"""
    usage:
        Only to be imported as module

    This module provides basic motif analysis utilities:
    - k-mer generation
    - k-mer frequency counting
    - top-k selection
    - GC content filtering
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# FUNCTIONS
def kmer_generator(seq: str, k: int):
    """
    Generates all k-mers of length `k` from a DNA sequence `seq`.

    Yields:
        str: A substring of length `k` from the input sequence.
    """
    i = 0
    while i <= len(seq) - k:
        yield seq[i : i + k]
        i += 1


def count_kmers(sequences: list[str], k: int):
    """
    Counts the frequency of each k-mer across a list of sequences.

    Args:
        sequences (list[str]): List of DNA sequences.
        k (int): Length of k-mers to count.

    Returns:
        dict[str, int]: Dictionary mapping k-mers to their counts.
    """
    kmer_dict = {}
    for sequence in sequences:
        for kmer in kmer_generator(sequence, k):
            if kmer in kmer_dict:
                kmer_dict[kmer] += 1
            else:
                kmer_dict[kmer] = 1
    return kmer_dict


def find_top_kmers(kmer_counts: dict[str, int], top_n: int = 10):
    """
    Returns the top N most frequent k-mers.

    Args:
        kmer_counts (dict[str, int]): Dictionary of k-mer counts.
        top_n (int): Number of top entries to return.

    Returns:
        list[tuple[str, int]]: List of (k-mer, count) tuples sorted by frequency.
    """
    return sorted(kmer_counts.items(), key=lambda key: key[1], reverse=True)[:top_n]


def gc_content(seq: str) -> float:
    """
    Calculates the GC content of a DNA sequence.

    Args:
        seq (str): DNA sequence.

    Returns:
        float: Proportion of G and C bases in the sequence.
    """
    gc_count = sum(1 for nuc in seq if nuc in "GCgc")
    return gc_count / len(seq)


def filter_kmers_by_gc(kmer_counts: dict[str, int], min_gc: float):
    """
    Filters k-mers based on a minimum GC content threshold.

    Args:
        kmer_counts (dict[str, int]): Dictionary of k-mer counts.
        min_gc (float): Minimum GC content required (between 0 and 1).

    Returns:
        list[str]: List of k-mers meeting the GC content requirement.
    """
    kmer_pass = []
    for kmer in kmer_counts.keys():
        if gc_content(kmer) > min_gc:
            kmer_pass.append(kmer)
    return kmer_pass
