#!/usr/bin/env python3

"""
    usage:
        ./assignment4.py --input GCF_000005845.2_ASM584v2_genomic.fna.gz --w 10000
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
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from preprocessing import Preprocessor
from mlm import MLM
from drawer import Drawer

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, type=pathlib.Path)
    return parser.parse_args()

def main():
    args = argparser()
    preprocessor = Preprocessor(args.input)
    df = preprocessor.run()
    mlm = MLM(df)
    tested_df = mlm.run()
    drawer = Drawer(tested_df)
    drawer.run()
    
if __name__ == '__main__':
    main()
