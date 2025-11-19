from csv import DictWriter
import ujson
import os
import argparse
from io_helpers import get_sample, change_filename
from check_dataset import get_all_keys
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The name of the file to fix", required=True)
parser.add_argument("--output", "-o", help="The name of the file to output to", required=False)


def jlines_to_csv(infile, outfile=None):
    # converts a json lines file to a csv file
    # infile: the name of the input file
    # outfile: the name of the output file
    # returns: None
    # raises: ValueError if the input file is not a json lines file
    if not outfile:
        outfile = change_filename(infile, "csv")

    if not infile.endswith(".json"):
        raise ValueError("Input file is not a json lines file")
    if not outfile.endswith(".csv"):
        raise ValueError("Output file is not a csv file")
    heads = list(get_all_keys(infile))
    with open(infile, 'r') as f, open(outfile, "w") as wf:
        dw = DictWriter(wf, fieldnames=heads)
        dw.writeheader()
        for line in f:
            try:
                dw.writerow(ujson.loads(line))
            except ValueError as e:
                print(line)
                raise e

if __name__ == '__main__':
    args = parser.parse_args()
    infile = args.input
    outfile = args.output
    if os.path.exists(outfile):
        if input(f"please enter anything if you want to first delete the existing output file {outfile}: \n"):
            os.remove(outfile)
    jlines_to_csv(infile, outfile)