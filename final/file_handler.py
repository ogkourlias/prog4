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
import pandas as pd


# CLASSES
class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        self.full_df = pd.read_csv(self.file_path, index_col=0)
        self.full_df["timestamp"] = pd.to_datetime(self.full_df["timestamp"])
        self.full_df = self.full_df.set_index("timestamp")
        return self.full_df

    def qc(self):
        missing_fraction = self.full_df.isnull().mean()
        cols_to_drop = missing_fraction[missing_fraction > 0.10].index
        self.full_df.drop(columns=cols_to_drop, inplace=True, errors="ignore")

        # Separate numerical columns (excluding 'machine_status')
        self.numerical_cols = self.full_df.drop(columns=["machine_status"]).columns

        # Fill missing values in train and test with column means
        self.full_df[self.numerical_cols] = self.full_df[self.numerical_cols].fillna(
            self.full_df[self.numerical_cols].mean()
        )
        self.full_df[self.numerical_cols] = self.full_df[self.numerical_cols].fillna(
            self.full_df[self.numerical_cols].mean()
        )
        return self.full_df

    def write_csv(self, df):
        df.to_csv(self.file_path)

    def run(self):
        self.read_csv()
        self.qc()
        return self.qc()
