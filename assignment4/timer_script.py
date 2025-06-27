#!/usr/bin/env python3

"""
    usage:
        ./timer_script.py --input GCF_000005845.2_ASM584v2_genomic.fna.gz --num-runs 35
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.3"

# IMPORTS
import sys
import argparse
import pathlib
import multiprocessing as mp
import time
import random
from assignment4 import Counter, Counter_single_core


def time_run(runner):
    start = time.time()
    runner.run()
    end = time.time()
    return end - start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=pathlib.Path)
    parser.add_argument("--num-runs", required=True, type=int)
    args = parser.parse_args()

    solo_times = []
    mp_times = []
    window_sizes = []

    for _ in range(args.num_runs):
        w = random.randint(50, 1400)
        window_sizes.append(w)

        solo = Counter_single_core(args.input, w)
        mp_counter = Counter(args.input, w)

        solo_t = time_run(solo)
        mp_t = time_run(mp_counter)

        solo_times.append(solo_t)
        mp_times.append(mp_t)

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
