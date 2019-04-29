import argparse
import yaml_reader
from pprint import pprint
from functools import reduce

def optimization_frequency(opt_file):
    with open(opt_file) as f:
        summary = yaml_reader.get_json(f.read())
        opt_frequency = {"Passed" : {}, "Missed" : {}, "Analysis" : {}}
        for status, passes in summary.items():
            for each_pass in passes:
                name = each_pass["name"]
                if name not in opt_frequency[status]:
                    opt_frequency[status][name] = 0
                else:
                    opt_frequency[status][name] = opt_frequency[status][name] + 1
        pprint(opt_frequency)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("opt_yaml_file", help="opt yaml generated with -fsave-optimization-record")
    args = parser.parse_args()
    filename = args.opt_yaml_file
    optimization_frequency(filename)