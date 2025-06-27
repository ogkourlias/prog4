#!/usr/bin/env python3

"""
Simple script to calculate GC content over a sliding window in a compressed FASTA file.
Can run in single-core or multiprocessing mode.

Usage:
    ./assignment4.py --input GCF_000005845.2_ASM584v2_genomic.fna.gz --w 10000
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# IMPORTS
import argparse
import gzip
import pathlib
import multiprocessing as mp
import time

# CLASSES
class Counter:
    """
    GC content counter using multiprocessing.
    """
    def __init__(self, input_file, window_size):
        """
        Set up input file, window size, and a multiprocessing queue.
        """
        self.input = input_file
        self.window_size = window_size
        self.queue = mp.Queue()

    def read_fasta(self):
        """
        Read compressed FASTA file, split sequence into chunks,
        and put them in a queue for processing.
        """
        with gzip.open(self.input, "rt") as fasta_f:
            buffer = ""
            total_len = 0
            for line in fasta_f:
                if line.startswith(">"):
                    continue
                line = line.strip()
                buffer += line
                total_len += len(line)
                while len(buffer) >= self.window_size:
                    chunk = buffer[: self.window_size]
                    start = total_len - len(buffer)
                    end = start + len(chunk)
                    self.queue.put((chunk, start, end))
                    buffer = buffer[self.window_size :]
            if buffer:
                self.queue.put((buffer, total_len - len(buffer), total_len))

    def worker(self, queue):
        """
        Get chunks from queue, calculate GC content, and print it.
        """
        while True:
            chunk = queue.get()
            if chunk[0] is None:
                break
            gc_count = sum(1 for nuc in chunk[0] if nuc in "GCgc")
            gc_content = gc_count / len(chunk[0])
            print(f"{chunk[1]} - {chunk[2]}: {gc_content:.2%}")

    def run(self):
        """
        Start worker process and read FASTA file.
        """
        proc = mp.Process(target=self.worker, args=(self.queue,))
        proc.start()
        self.read_fasta()
        self.queue.put((None, None, None))  # Signal to stop worker
        proc.join()


class Counter_single_core:
    """
    GC content counter using a single process.
    """
    def __init__(self, input_file, window_size):
        """
        Set up input file and window size.
        """
        self.input = input_file
        self.window_size = window_size

    def read_fasta(self):
        """
        Read compressed FASTA file, split sequence into chunks,
        and process each chunk.
        """
        with gzip.open(self.input, "rt") as fasta_f:
            buffer = ""
            total_len = 0
            for line in fasta_f:
                if line.startswith(">"):
                    continue
                line = line.strip()
                buffer += line
                total_len += len(line)
                while len(buffer) >= self.window_size:
                    chunk = buffer[: self.window_size]
                    start = total_len - len(buffer)
                    end = start + len(chunk)
                    self.process_chunk(chunk, start, end)
                    buffer = buffer[self.window_size :]
            if buffer:
                self.process_chunk(buffer, total_len - len(buffer), total_len)

    def process_chunk(self, seq, start, end):
        """
        Calculate and print GC content for one chunk.
        """
        gc_count = sum(1 for nuc in seq if nuc in "GCgc")
        gc_content = gc_count / len(seq)
        print(f"{start} - {end}: {gc_content:.2%}")

    def run(self):
        """
        Run the single-core GC content counter.
        """
        self.read_fasta()


def time_run(name, runner):
    """
    Measure and return the time it takes to run a counter.
    """
    start = time.time()
    runner.run()
    end = time.time()
    return f"{name} version took {end - start:.4f} seconds"


def main():
    """
    Parse arguments, run both single-core and multiprocessing versions, and print runtimes.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=pathlib.Path, help="Input gzipped FASTA file")
    parser.add_argument("--w", dest="window_size", required=True, type=int, help="Window size")
    args = parser.parse_args()

    solo = Counter_single_core(args.input, args.window_size)
    solo_time = time_run("Solo process", solo)

    parallel = Counter(args.input, args.window_size)
    mp_time = time_run("Multiprocessing", parallel)

    print(solo_time)
    print(mp_time)


if __name__ == "__main__":
    main()
