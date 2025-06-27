#!/usr/bin/env python3

"""
    usage:
        python3 final.py -i input_dir -o output_dir -t train_file.csv -n num_threads
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "0.1.0"

# IMPORTS
import os
# os.environ["OPENBLAS_NUM_THREADS"] = str(1)
import argparse
import pathlib
from file_handler import FileHandler
from mlm import MLM
from watcher import Watcher
import pandas as pd

pd.options.mode.chained_assignment = None  # default="warn"


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, type=pathlib.Path)
    parser.add_argument("--output", "-o", required=True, type=pathlib.Path)
    parser.add_argument("--trainfile", "-t", required=True, type=pathlib.Path)
    parser.add_argument("--num-threads", "-n", default=1, type=int)
    return parser.parse_args()


def main():
    args = argparser()
    df = FileHandler(args.trainfile).run()
    model = MLM(df, args.num_threads).run()
    Watcher(model, args.input, args.output).run()


if __name__ == "__main__":
    main()
