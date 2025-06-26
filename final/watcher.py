import os
import time
import logging
from drawer import Drawer
from file_handler import FileHandler

class Watcher:
    def __init__(self, model, input_dir, output_dir, log_file="model.log", polling_interval=5):
        self.model = model
        self.polling_interval = polling_interval
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.img_dir = f"{self.output_dir}/img"

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.img_dir , exist_ok=True)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s  %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
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

