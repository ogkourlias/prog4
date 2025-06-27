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
import pandas as pd


# CLASSES
class FileHandler:
    """
    FileHandler is a utility class for reading, cleaning, and writing CSV files with time series data.

    Attributes:
        file_path (str): Path to the CSV file.
        full_df (pd.DataFrame): The loaded and processed DataFrame.
        numerical_cols (pd.Index): Index of numerical columns in the DataFrame (excluding 'machine_status').

    Methods:
        __init__(file_path):
            Initializes the FileHandler with the specified file path.

        read_csv():
            Reads the CSV file at self.file_path into a pandas DataFrame, parses the 'timestamp' column as datetime,
            and sets it as the DataFrame index.
            Returns:
                pd.DataFrame: The loaded DataFrame.

        qc():
            Performs quality control on self.full_df:
                - Drops columns with more than 10% missing values.
                - Identifies numerical columns (excluding 'machine_status').
                - Fills missing values in numerical columns with their respective column means.
            Returns:
                pd.DataFrame: The cleaned DataFrame.

        write_csv(df):
            Writes the provided DataFrame to self.file_path as a CSV file.

        run():
            Executes the full pipeline: reads the CSV, performs quality control, and returns the cleaned DataFrame.
            Returns:
                pd.DataFrame: The cleaned DataFrame after processing.
    """
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
