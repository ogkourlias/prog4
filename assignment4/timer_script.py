#!/usr/bin/env python3

"""
Benchmark script to compare GC content counting using single-core and multiprocessing.
Runs both methods multiple times with random window sizes.

Usage:
    ./timer_script.py --input GCF_000005845.2_ASM584v2_genomic.fna.gz --num-runs 35
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# IMPORTS
import sys
import argparse
import pathlib
import multiprocessing as mp
import time
import random
from assignment4 import Counter, Counter_single_core


def time_run(runner):
    """
    Measure how long it takes to run the given runner object.
    """
    start = time.time()
    runner.run()
    end = time.time()
    return end - start


def main():
    """
    Run multiple benchmarks with random window sizes.
    Compare single-core and multiprocessing runtimes.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=pathlib.Path, help="Input gzipped FASTA file")
    parser.add_argument("--num-runs", required=True, type=int, help="Number of times to run each method")
    args = parser.parse_args()

    solo_times = []
    mp_times = []
    window_sizes = []

    for _ in range(args.num_runs):
        w = random.randint(50, 1400)  # Choose a random window size
        window_sizes.append(w)

        solo = Counter_single_core(args.input, w)
        mp_counter = Counter(args.input, w)

        solo_t = time_run(solo)
        mp_t = time_run(mp_counter)

        solo_times.append(solo_t)
        mp_times.append(mp_t)

    # Print results
    print("\nWindow sizes:")
    print(window_sizes)

    print("\nSolo run times:")
    print(solo_times)

    print("\nMultiprocessing run times:")
    print(mp_times)

    print("\nAverage times:")
    print(f"Solo: {sum(solo_times) / len(solo_times):.4f} seconds")
    print(f"MP:   {sum(mp_times) / len(mp_times):.4f} seconds")


if __name__ == "__main__":
    main()
