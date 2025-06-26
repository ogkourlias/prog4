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

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, type=pathlib.Path)
    return parser.parse_args()

# CLASSES
class Preprocessor:
    def __init__(self, input_file):
        self.input =  input_file
        self.queue = mp.Queue()

    def read_csv(self):
        self.full_df = pd.read_csv(self.input, index_col=0)
        self.full_df["timestamp"] = pd.to_datetime(self.full_df["timestamp"])
        return self.full_df

    def qc(self):
        self.full_df = self.full_df.set_index('timestamp')
        self.full_df = self.full_df.drop(['sensor_15', 'sensor_50'],axis=1)
        broken_rows = self.full_df[self.full_df['machine_status']=='BROKEN']
        recovery_rows = self.full_df[self.full_df['machine_status']=='RECOVERING']
        normal_rows = self.full_df[self.full_df['machine_status']=='NORMAL']
        numerical_cols = self.full_df.columns[:-1]
        self.full_df[numerical_cols]=self.full_df[numerical_cols].fillna(self.full_df[numerical_cols].mean())
        scaler=StandardScaler()
        self.full_df[numerical_cols] = scaler.fit_transform(self.full_df[numerical_cols])
        return self.full_df
    
    def run(self):
        return self.read_csv()
    
def main():
    args = argparser()
    preprocessor = Preprocessor(args.input)
    preprocessor.read_csv()
    preprocessor.qc()

if __name__ == '__main__':
    main()
