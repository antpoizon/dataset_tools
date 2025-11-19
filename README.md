# dataset_tools

A Python toolkit for processing JSON Lines files: IO helpers for local filesystem operations (filename changes, directory traversal), row filtering (by key or key/value pair), dataset sanity checks, and conversion of JSON Lines to CSV.

## Table of Contents

- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  

## Features

- Process `.jsonl` (JSON Lines) files with ease  
- IO helpers: rename files, list files in a directory, filter files, etc.  
- Drop rows from JSON Lines based on keys or specific key/value pairs  
- Sanity-check dataset quality (e.g., missing keys, blank values)  
- Convert JSON Lines to CSV for easier downstream processing  

## Installation

```bash
# Clone the repository
git clone https://github.com/antpoizon/dataset_tools.git
cd dataset_tools

# (Optional) Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # on Linux/macOS
.\venv\Scripts\activate    # on Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

# check_dataset.py
--input, -i (Required): input filename  
--pull-headers, -p (Optional): headers you want to analyze the data of, separated by spaces  
--disregard, -d (Optional): Boolean for disregard, will analyze ALL headers EXCEPT those specified with -p  
--all-headers, -a (Optional): Boolean for all-headers, will analyze ALL headers  
```
python check_dataset.py  \
  -i {input file} \
  -d (optional)
  -p {headers separated by spaces}
#OR
python check_dataset.py  \
  -i {input file} \
  -a
#OR
from check_dataset import get_counter
get_counter(fname, header_to_analyze: list, disregard: bool)
```

# drop_rows.py
--input, -i (Required): input filename  
--ouput, -o (Optional): output filename, will default to input_dropped.ext  
--keys_to_look_at, -k (Optional): Keys to specify for dropping; if key has non-blank value, the row is dropped; accepts multiple values  
--val_to_look_at, -v (Optional): key/value pairs to specify for dropping; if the key has that specific value, the row is dropped; accepts multiple values  
```
python drop_rows.py \
  -i {input filename} \
  -o {ouput filename}
  -k {keys to drop row, separated by spaces}
#OR
python drop_rows.py \
  -i {input filename} \
  -o {ouput filename}
  -v {key/value pairs to drop row, format as key/value separated by spaces}
#OR
from drop_rows import drop_lines
drop_lines(fname, outname, keys, key_value_filters)
```

# io_helpers.py
change_filename: takes filename, extension, and optional suffix; returns string of changed filename  
get_sample: takes big list and sample size, returns list with number of values specified by sample_size from big list  
get_all_files_from_dir: takes directory name and optional file extension, returns list of full paths of all files from that directory  
```
from io_helpers import change_filename
og_fname = "full/parent/dir/or/just/basename/foo.txt"
new_fname = change_filename(og_fname, "csv", "bar")
print(new_fname)
#Output: full/parent/dir/or/just/basename/foo_bar.csv

from io_helpers import get_sample
big_list = [i for i in range(0, 100000)]
sample_size = 5000
sample = get_sample(big_list, sample_size)
print(len(sample))
#Output: 5000

from io_helpers import get_all_files_from_dir
dirname = "path/to/dir"
ext = "sql"
sql_files = get_all_files_from_dir(dirname, ext)
# Ouput: recursively, all files with "sql" extension in path/to/dir
```
# jlines_to_csv.py
--input, -i (Required): input filename
--ouput, -o (Optional): output filename, will default to input.csv
```
python jlines_to_csv.py \
  -i {input json or jsonl filename}
  -o {output csv filename}
#OR
from jlines_to_csv import jlines_to_csv
jlines_to_csv(input_json_filename, output_csv_filename)
```
