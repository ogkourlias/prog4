# Assignment 5 (Final assignment)

This assignment consist of multiple modules and scripts, with final.py being the main script that uses all modules.
The goal of these modules is to do the following in order: 

1. Train a LocalOutlierFactor model on sensor data from April to june from a user provided CSV file  (File_handler and MLM Module)
2. Watch a user provided input directory for addition of new sensor .csv files. (Watcher module)
3. Load the .csv file and use the trained model to predict anomaly scores for each sample. (File_handler and MLM module)
4. Plot the anomaly identification in a user provided output directory for each sensor (Drawer module)
5. Write the anomaly identifiers to a new .csv file in a use provided output directory (File_handler module)
6. Log the files being handled to model.log

## Installation
```bash
pip install -r requirements.txt
```

## Usage

**As module**
```python
from drawer import Drawer
from file_hanlder import FileHandler
from mlm import MLM
from watcher import Watcher

csv_train_file = "path/to/csv_file.csv"
num_threads = 1 # Number of threads sklearn
input_dir = "path/to/input/directory/"
output_dir = "path/to/output/directory/"
image_dir = "path/to/image/output/directory/"

df = FileHandler(csv_train_file).run()
model = MLM(df, num_threads).run()
Watcher(model, inpu_dir, output_directory).run()
Drawer(df, image_ditr)
```

**As script**

**IMPORTANT**
For the BIN Network, make sure to set the number of OpenBLAS threads before running as a script:

```bash
export OPENBLAS_NUM_THREADS=1 # Any number of threads
```

```bash
python3 final.py -i input_dir -o output_dir -t train_file.csv -n num_threads
```

## License

[MIT](https://choosealicense.com/licenses/mit/)