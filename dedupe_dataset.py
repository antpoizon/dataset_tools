import argparse
import ujson
from csv import DictReader, DictWriter
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The name of the file to fix", required=True)
parser.add_argument("--unique-key", "-u", help="The key/value which is unique across records; used to dedupe", required=True)
parser.add_argument("--output", "-o", help="The name of the file to output to", required=True)

'''
dedupe_dataset.py Usage:

python dedupe_dataset.py -i {Input File} -u {unique identifier column/key} -o {output filename}

Input file should be in the following format:
    {key1:value1, key2:value2}
    {key1:value3, key2:value4}
    {key1:value5, key2:value6}
    ...
    OR
    key1,key2,key3
    value1,value2,value3
    value4,value5,value6
    ...
'''

def dedupe(fname, unique_key, outname):
    with open(outname, "w") as wf, open(fname, "r") as f:
        if fname.endswith(".json"):
            handle_file(f, unique_key, wf, True)
        elif fname.endswith(".csv"):
            dr = DictReader(f)
            headers = dr.fieldnames
            dw = DictWriter(wf, fieldnames=headers)
            dw.writeheader()
            handle_file(dr, unique_key, dw)

def handle_file(f_handle, unique_key, wf, is_json=False):
    #handler function for json files
    seen_set = set()
    for i, line in enumerate(f_handle, 1):
        try:
            if is_json:
                temp_d = ujson.loads(line)
            else:
                temp_d = line
            v = temp_d[unique_key]
        except (KeyError, ujson.JSONDecodeError) as e:
            print(f"Line failed on: {i}\n")
            raise e
        if v in seen_set:
            continue
        else:
            seen_set.add(temp_d[unique_key])
            if is_json:
                wf.write(ujson.dumps(temp_d) + "\n")
            else:
                wf.writerow(temp_d)

if __name__ == "__main__":
    args = parser.parse_args()
    fname = args.input
    u_key= args.unique_key
    outfile = args.output
    dedupe(fname, u_key, outfile)