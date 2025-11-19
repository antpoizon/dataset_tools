import argparse
import ujson
from collections import Counter
from csv import DictReader
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="The name of the file to fix", required=True)
parser.add_argument("--pull-headers", "-p", nargs="+", help="the headers that we want to extract data from", required=False)
parser.add_argument("--disregard", "-d", default=False, action='store_true', help="(Optional) If instead of specifying headers you WANT to inspect, this inverts it to ignore the headers you specify. Useful for when you want all but one header analyzed")
parser.add_argument("--all-headers", "-a", action='store_true', help="(Optional) use to check all headers", required=False)




'''
check_dataset.py Usage:
Produces a Counter object for each header in the input file, with the count of each value for that header.
Compatible with both json lines and csv files.

python check_dataset.py -i {Input File} -p {Whatever headers you want to look at}
    Optional: "-d" for "disregard" useful if you have a lot of headers, and you want to analyze most of them. Use "-p" to specify the headers you want to disregard, followed by "-d"
    ex. python check_dataset.py -i {Input File} -p {Whatever headers DONT want to analyze} -d
    Optional: "-a" for "all headers" useful if you want to analyze all headers
    ex. python check_dataset.py -i {Input File} -a

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
No output file is created by this script, it is only for sanity checking a json lines file
'''

def get_counter(fname, headers, disregard = False):
    #function for getting the counter of keys in a file
    if disregard:
        all_k_set = get_all_keys(fname)
        headers = list(all_k_set - set(headers))

    if fname.endswith(".json"):
        handle_json(fname, headers)
    elif fname.endswith(".csv"):
        handle_csv(fname, headers)

def get_all_keys(fname):
    #gets all keys in a file
    k_set = set()
    with open(fname, "r") as f:
        if fname.endswith(".csv"):
            dr = DictReader(f)
            return dr.fieldnames
        for line in f:
            d = ujson.loads(line)
            k_set.update(d.keys())
        return k_set

def handle_json(fname, headers):
    #handler function for json files
    out_d = {h:Counter() for h in headers}
    with open(fname, "r") as f:
        for i, line in enumerate(f, 1):
            temp_d = ujson.loads(line)
            for h in headers:
                v = temp_d[h]
                if isinstance(v, list):
                    out_d[h][f"list_length_{len(v)}"] += 1
                elif h in temp_d.keys():
                    out_d[h][v] += 1
            line_count = i
        #print(f"Final Value Counts per Header: \n{out_d}")
        for k in out_d:
            total_count = sum(out_d[k].values())
            check_sanity(line_count, total_count, k, out_d)

def handle_csv(fname, headers):
    #handler function for csv files
    out_d = {h:Counter() for h in headers}
    with open(fname, "r") as f:
        dr = DictReader(f)
        for i, line in enumerate(dr, 1):
            for h in headers:
                v = line[h]
                if isinstance(v, list):
                    out_d[h][f"list_length_{len(v)}"] += 1
                elif h in line.keys():
                    out_d[h][v] += 1
            line_count = i
        #print(f"Final Value Counts per Header: \n{out_d}")
        for k in out_d:
            total_count = sum(out_d[k].values())
            check_sanity(line_count, total_count, k, out_d)



def check_sanity(lc, tc, key, out_d):
    #Checks for missing values in the dataset for each key
    dif = lc - tc
    print(f"Total Line Count: {lc}\nTotal lines with key '{key}':{tc}")
    if dif > 0:
        print(f"% of Lines without data in '{key}': {round(float((dif / lc)*100), 2)}%")
    else:
        print(f"Values Count for key '{key}':{out_d[key]}\n")





if __name__ == "__main__":
    args = parser.parse_args()
    fname = args.input
    headers= args.pull_headers
    disregard= args.disregard
    all_heads = args.all_headers
    if all_heads:
        headers = get_all_keys(fname)
    print(f"Checking Keys: {headers}")
    get_counter(fname, headers, disregard)