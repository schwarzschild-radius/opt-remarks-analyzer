#! /usr/bin/env python3

'''
input: benchmark directory or benchmark descriptor(containing benchmark metadata)
output: 
    - plot of passes
        - stacked bar graph with misses, passes and analysis
    - csv output
        - for each function, list the successfull passes
'''

from list_passes import list_passes
from yaml2json import optYaml2Json
import logging
from os import listdir
from os.path import isfile, join
from pprint import pprint

def merge_dicts(dst, src):
    for key in src:
        if key in dst:
            if dst[key]['type'] == 'transformation':
                dst[key]['passed'] += src[key]['passed']
                dst[key]['missed'] += src[key]['missed']
                dst[key]['percentage'] = (dst[key]['percentage'] + src[key]['percentage']) / 2
            else:
                dst[key]['times'] += src[key]['times']
                dst[key]['percentage'] = (dst[key]['percentage'] + src[key]['percentage']) / 2
        else:
            dst[key] = src[key]
    return dst

def merge_passes(benchmark_dir):
    opt_yaml_files = [f for f in listdir(benchmark_dir) if isfile(join(benchmark_dir, f)) and "opt.yaml" in f]
    data = {}
    for yaml_file in opt_yaml_files:
        f = open(join(benchmark_dir, yaml_file)).read()
        merge_dicts(data, list_passes(optYaml2Json(f)))
    return data

def plot(data):
    from matplotlib import pyplot as plt
    import numpy as np
    import matplotlib 

    X = data.keys()
    Passed = [ data[key]['passed'] if data[key]['type'] == 'transformation' else data[key]['times'] for key in data]
    Missed = [ data[key]['missed'] if data[key]['type'] == 'transformation' else 0 for key in data]
    print("Passed: ", Passed)
    print("Missed: ", Missed)
    N = len(data)
    ind = np.arange(N)
    width = 0.35
    p1 = plt.bar(ind, Passed, width)
    p2 = plt.bar(ind, Missed, width, bottom=Passed)
    plt.xticks(ind, X)
    plt.ylabel('Percentage of Misses')
    plt.title('Benchmark analysis report')
    plt.legend((p1[0], p2[0]), ('Passed', 'Missed'))
    plt.show()

def process_function(func_data):
    data = {}
    for each_pass in func_data:
        if each_pass['Pass'] in data and (each_pass['status'] == "Passed" or each_pass['status'] == "Analysis"):
            data[each_pass['Pass']] += 1
        else:
            data[each_pass['Pass']] = 0
    return data

def function_wise(benchmark_dir):
    from transform_json import transform_json
    opt_yaml_files = [f for f in listdir(benchmark_dir) if isfile(join(benchmark_dir, f)) and "opt.yaml" in f]
    csv_data = []
    for yaml_file in opt_yaml_files:
        f = open(join(benchmark_dir, yaml_file)).read()
        data = transform_json(f)
        # pprint(data)
        for func in data:
            csv_data.append([func, process_function(data[func])])
    return csv_data

def csv(passes, function_wise_data):
    csv_data = []
    csv_data.append(["function_name"] + passes)
    for func_data in function_wise_data:
        function = func_data[0]
        pass_info = func_data[1]
        data = [function]
        for each_pass in passes:
            if each_pass in pass_info:
                data.append(pass_info[each_pass])
            else:
                data.append(0)
        csv_data.append(data)
    return csv_data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark_dir", help="place where the opt yaml files are generated")
    parser.add_argument("--plot", help="plot the summary as a stacked bar graph")
    parser.add_argument("--csv", help="dump the summary as csv")
    parser.add_argument("--g", help="enable logging of debug info for developement only", action='store_true', default=False)
    args = parser.parse_args()
    if args.g:
        logging.basicConfig(level=logging.INFO)
    data = merge_passes(args.benchmark_dir)
    csv_data = function_wise(args.benchmark_dir)
    pprint(csv_data)
    csv_data = csv(list(data.keys()), csv_data)
    pprint(csv_data)
    print(len(csv_data))
    # pprint(data)
    # plot(data)