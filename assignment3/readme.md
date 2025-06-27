# Assignment 3

This assignment consists of a python module and a main assignment script.
The motiftools module contains methods to examine k-mer qualities of an input sequence fata file.

## Installation
```bash
pip install -r requirements.txt
```

## Usage

**As module**
```python
from assignment3 import Motiftools
```

**As script**
```bash
python3 motifcli.py --input path/to/file.fasta --k 6 --top 10 --min-gc 0.5
```

## License

[MIT](https://choosealicense.com/licenses/mit/)