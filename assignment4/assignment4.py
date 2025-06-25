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
import argparse
import gzip
import pathlib
import multiprocessing as mp

# CLASSES
class Counter():
    """ Desc """
    def __init__(self) -> None:
        self.args = self.argparser()
        self.window_size = self.args.window_size
        self.queue = mp.Queue()
        self.run()

    def read_fasta(self):
        with gzip.open(self.args.input, "rt") as fasta_f:
            buffer = ""
            total_len = 0
            for line in fasta_f:
                if line.startswith(">"):
                    continue
                line = line.strip()
                buffer += line
                total_len += len(line)
                while len(buffer) >= self.window_size:
                    chunk = buffer[:self.window_size]
                    start = total_len - len(buffer)
                    end = start + len(chunk)
                    self.queue.put((chunk, start, end))
                    # send chunk to worker
                    buffer = buffer[self.window_size:]

            # send trailing work to worker
            if buffer:
                self.queue.put((buffer, total_len - len(buffer), total_len))


    def worker(self, queue):
        while True:
            chunk = queue.get()
            if chunk[0] is None:
                break
            gc_count = sum(1 for nuc in chunk[0] if nuc in "GCgc")
            gc_content = gc_count / len(chunk[0])
            print(f'{chunk[1]} - {chunk[2]}: {gc_content:.2%}')

    def run(self):
        proc = mp.Process(target=self.worker, args=(self.queue,))
        proc.start()

        self.read_fasta()
        self.queue.put((None, None, None))

        proc.join()

    def argparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", required=True, type=pathlib.Path)
        parser.add_argument("--w", dest="window_size", required=True, type=int)
        return(parser.parse_args())
        
        

# MAIN
def main(args):
    """ Main function """
    counter = Counter()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
