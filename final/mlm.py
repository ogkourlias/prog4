#!/usr/bin/env python3

"""
    usage:
        Import as module
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# IMPORTS
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor


# CLASSES
class MLM:
    """
    MLM class for anomaly detection using Local Outlier Factor (LOF) on time-indexed data.

    Attributes:
        df (pd.DataFrame): Input dataframe with time-indexed rows and a 'machine_status' column.
        n_threads (int): Number of threads to use for parallel processing.
        train_df (pd.DataFrame): Training subset of the data.
        test_df (pd.DataFrame): Testing subset of the data.
        numerical_cols (pd.Index): Columns containing numerical features.
        model (LocalOutlierFactor): Trained LOF model.

    Methods:
        split():
            Splits the dataframe into training and testing sets based on date ranges.

        training_process():
            Preprocesses the training and testing data:
                - Identifies numerical columns.
                - Filters normal machine status rows.
                - Standardizes numerical features.
                - Calculates the fraction of outliers.
            Returns:
                outliers_fraction (float): Estimated fraction of outliers in the training set.
                numerical_df (pd.DataFrame): Standardized numerical features of the training set.

        train():
            Runs the full training pipeline:
                - Splits the data.
                - Preprocesses and standardizes features.
                - Trains the LOF model.
            Returns:
                self (MLM): The fitted MLM instance.

        predict_df(df):
            Predicts outliers in a given dataframe using the trained LOF model.
            Args:
                df (pd.DataFrame): Dataframe to predict on.
            Returns:
                pd.DataFrame: Dataframe with an added 'LocalOutlierFactor' prediction column.

        run():
            Executes the training pipeline.
            Returns:
                self (MLM): The fitted MLM instance.
    """
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
