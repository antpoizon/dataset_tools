import os
from random import randint
def change_filename(fname, ext: str, suffix = ""):
    # changes the extension of a file, and optionally adds a suffix i.e change_filename("foo.json", "csv", "bar") -> "foo_bar.csv"
    if suffix:
        suffix = "_" + suffix
    b_name = os.path.basename(fname)
    p_path = os.path.dirname(fname)
    split_name = b_name.split(".")
    n_name = ".".join(split_name[:-1]) + suffix + "." + ext
    return os.path.join(p_path, n_name)

def get_sample(big_list, samp_size):
    # gets a random sample of size samp_size from a list
    if samp_size > len(big_list):
        raise ValueError("Sample size is greater than the length of the list")
    sample_start = randint(1, len(big_list)-samp_size)
    small_list = big_list[sample_start:sample_start + samp_size]

    return small_list

def get_all_files_from_dir(dirname, ext = ""):
    # gets list of all files in directory, optionally filtered by extension
    all_fnames = []
    for root, _, files in os.walk(dirname):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))
            if os.path.isfile(full_path):
                if ext and full_path.endswith(ext):
                    all_fnames.append(full_path)
                elif not ext:
                    all_fnames.append(full_path)
    return all_fnames
