import argparse
import ujson
from io_helpers import change_filename
from csv import DictReader, DictWriter
import os
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The name of the label", required=True)
parser.add_argument("--output", "-o", help="The name of the file to output to", required=False)
parser.add_argument("--keys_to_look_at", "-k", nargs="+", help="key(s) specified for dropping lines", required=False)
parser.add_argument("--val_to_look_at", "-v", nargs="+", help="value(s) specified for dropping lines, format as 'key/value key/value etc'", required=False)


def drop_lines(fname, outname, keys=None, key_value_filters=None):
    if fname.endswith(".json") or fname.endswith(".jsonl"):
        drop_lines_json(fname, outname, keys, key_value_filters)
    elif fname.endswith(".csv"):
        drop_lines_csv(fname, outname, keys, key_value_filters)
    else:
        raise ValueError(f"Unsupported file type: {fname}")

def drop_lines_json(fname, outname, keys=None, key_value_filters=None):
    # drops lines from a json lines file based on the keys and value filters
    keys = keys or []
    key_value_filters = key_value_filters or []
    with open(fname, "r") as f, open(outname, "w") as wf:
        for line in f:
            d = ujson.loads(line)
            skip = check_skip(d, keys, key_value_filters)

            if not skip:
                wf.write(f"{ujson.dumps(d, ensure_ascii=False)}\n")


def drop_lines_csv(fname, outname, keys=None, key_value_filters=None):
    keys = keys or []
    key_value_filters = key_value_filters or []
    with open(fname, "r") as f, open(outname, "w") as wf:
        f = DictReader(f)
        dw = DictWriter(wf, fieldnames=f.fieldnames)
        dw.writeheader()
        for line in f:
            d = dict(line)
            skip = check_skip(d, keys, key_value_filters)
            if not skip:
                dw.writerow(d)

def check_skip(d, keys=None, key_value_filters=None):
    skip = False
    if keys:
        for k in keys:
            if k in d:
                skip = True
                break
    if key_value_filters:
        for key, val in key_value_filters:
            if key in d and str(d[key]).lower() == val:
                skip = True
                break
    return skip

if __name__ == '__main__':
    args = parser.parse_args()
    infile = args.input
    outfile = args.output
    keys = args.keys_to_look_at
    vals = args.val_to_look_at
    if not outfile:
        outfile = change_filename(infile, os.path.splitext(infile)[1].lstrip("."), "dropped")
    key_value_filters = []
    if vals:
        for v in vals:
            key, val = v.split("/", 1)
            val = val.lower()
            key_value_filters.append((key, val))
            print(f"Dropping all lines from {infile} where {key} == {val}")
    if keys:
        print(f"Dropping all lines from {infile} containing keys: {', '.join(keys)}")
    drop_lines(infile, outfile, keys=keys, key_value_filters=key_value_filters)

    print(f"Outputting to file: {outfile}")


