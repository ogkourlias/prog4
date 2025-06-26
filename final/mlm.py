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
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, type=pathlib.Path)
    return parser.parse_args()

# CLASSES

class MLM:
    def __init__(self, df):
        self.df = df

    def split(self):
        self.df = self.df.set_index('timestamp')
        self.train_df = self.df[(self.df.index >= "2018-04-01") & (self.df.index < "2018-07-01")]
        self.test_df = self.df[(self.df.index >= "2018-07-01") & (self.df.index < "2018-09-01")]
    
    def training_process(self):
        self.train_df = self.train_df.drop(['sensor_15', 'sensor_50'],axis=1)
        normal_rows = self.train_df[self.train_df['machine_status']=='NORMAL']
        self.numerical_cols = self.train_df.columns[:-1]
        self.train_df[self.numerical_cols]=self.train_df[self.numerical_cols].fillna(self.train_df[self.numerical_cols].mean())
        self.test_df[self.numerical_cols]=self.test_df[self.numerical_cols].fillna(self.test_df[self.numerical_cols].mean())
        scaler=StandardScaler()
        self.train_df[self.numerical_cols] = scaler.fit_transform(self.train_df[self.numerical_cols])
        outliers_fraction = 1 - (len(normal_rows) / len(self.train_df))
        numerical_df = self.train_df[self.numerical_cols]
        return outliers_fraction, numerical_df

    def train(self):
        self.split()
        outliers_fraction, numerical_df = self.training_process()
        alg = LocalOutlierFactor(novelty=True, contamination=outliers_fraction, n_jobs=-1)
        self.model = alg.fit(numerical_df)
        self.test_df["LocalOutlierFactor"] = self.model.predict(self.test_df[self.numerical_cols])
        return self.test_df

    def run(self):
        return self.train()


def main():
    pass

if __name__ == '__main__':
    main()
