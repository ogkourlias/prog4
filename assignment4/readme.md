# Assignment 3

This assignment consists a script and two modules.
The Counter module calculates and returns GC percentages for a window size as provided by the user.
The Counter_single_core module does the same, but with a single thread instead of dividing the work to workers.

The timer script generates random window sizes and performs a number of runs provided by the user.
It then returns the average times for the multiprocessing and single proessing approaches.

## Installation
```bash
pip install -r requirements.txt
```

## Usage

**As module**
```python
from assignment4 import Counter
```

**As script**
```bash
python3 timer_script.py --input GCF_000005845.2_ASM584v2_genomic.fna.gz --num-runs 35
```

## License

[MIT](https://choosealicense.com/licenses/mit/)