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
import os
import time
import logging
from drawer import Drawer
from file_handler import FileHandler

# CLASSES
class Watcher:
    """
    Watcher monitors a specified input directory for new CSV files, processes them using a provided model,
    generates visualizations, and writes the results to an output directory.

    Attributes:
        model: An object with a `predict_df` method for making predictions on DataFrames.
        input_dir (str): Path to the directory to monitor for new CSV files.
        output_dir (str): Path to the directory where output files and images will be saved.
        log_file (str): Path to the log file for recording events (default: "model.log").
        polling_interval (int): Time interval in seconds between directory scans (default: 5).
        img_dir (str): Path to the directory where generated images will be saved.
        logger (logging.Logger): Logger instance for recording events.

    Methods:
        run():
            Continuously monitors the input directory for new CSV files, processes each file only once,
            applies the model's prediction, generates visualizations, saves the results, and logs actions.
    """
    def __init__(
        self, model, input_dir, output_dir, log_file="model.log", polling_interval=5
    ):
        self.model = model
        self.polling_interval = polling_interval
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.img_dir = f"{self.output_dir}/img"

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.img_dir, exist_ok=True)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info(f"Monitoring {self.input_dir} for new files...")
        finished_tracker = set()  # Moved here
        while True:
            for filename in os.listdir(self.input_dir):
                if filename.endswith(".csv") and filename not in finished_tracker:
                    file_path = os.path.join(self.input_dir, filename)
                    print(f"Processing {file_path}")
                    df = FileHandler(file_path).run()
                    df = self.model.predict_df(df)
                    Drawer(df, self.img_dir).run()
                    FileHandler(f"{self.output_dir}/{filename}-predicted").write_csv(df)
                    finished_tracker.add(filename)
            time.sleep(self.polling_interval)
