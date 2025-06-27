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
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor


# CLASSES
class MLM:
    def __init__(self, df, threads):
        self.df = df
        self.n_threads = threads

    def split(self):
        self.train_df = self.df[
            (self.df.index >= "2018-04-01") & (self.df.index < "2018-07-01")
        ]
        self.test_df = self.df[
            (self.df.index >= "2018-07-01") & (self.df.index < "2018-09-01")
        ]

    def training_process(self):
        self.numerical_cols = self.df.drop(columns=["machine_status"]).columns

        # Filter rows with normal machine status
        normal_rows = self.train_df[self.train_df["machine_status"] == "NORMAL"]

        # Standardize numerical features
        scaler = StandardScaler()
        self.train_df[self.numerical_cols] = scaler.fit_transform(
            self.train_df[self.numerical_cols]
        )
        self.test_df[self.numerical_cols] = scaler.transform(
            self.test_df[self.numerical_cols]
        )

        # Calculate outlier fraction
        outliers_fraction = 1.0 - (len(normal_rows) / len(self.train_df))

        # Return the processed numerical features
        numerical_df = self.train_df[self.numerical_cols]
        return outliers_fraction, numerical_df

    def train(self):
        self.split()
        outliers_fraction, numerical_df = self.training_process()
        alg = LocalOutlierFactor(
            novelty=True, contamination=outliers_fraction, n_jobs=self.n_threads
        )
        self.model = alg.fit(numerical_df)
        # self.test_df["LocalOutlierFactor"] = self.model.predict(self.test_df[self.numerical_cols])
        return self

    def predict_df(self, df):
        df["LocalOutlierFactor"] = self.model.predict(df[self.numerical_cols])
        return df

    def run(self):
        return self.train()
