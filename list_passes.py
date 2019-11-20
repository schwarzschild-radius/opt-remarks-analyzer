#! /usr/bin/env python3

'''
Given an opt.yaml file -> list of passes occurred grouped by Passed, Missed, Analysis, AnalysisFPCommute, AnalysisAliasing and Failure

input: opt.yaml file
output:
    if transformation pass
        { pass | transformation | n(pass) | n(miss) | total percentage }
    else analysis pass
        { pass | analysis | n(times)| total percentage }
'''

from yaml2json import optYaml2Json
import logging
from pprint import pprint
import pandas as pd

def emplace_to_dict(init, op):
    def emplace_back(key, value, dict):
        if key in dict:
            dict[key] = op(dict[key], value)
        else:
            dict[key] = init
        return dict
    return emplace_back


def list_passes(opt_json):
    data = {}
    npasses = len(opt_json)
    emplace_back_int = emplace_to_dict(0, lambda x, y: x + y)
    for opt_pass in opt_json:
        logging.info(opt_pass["Pass"])
        pass_name = opt_pass["Pass"]
        if pass_name not in data:
            data[pass_name] = {}
            data[pass_name]["type"] = "analysis" if opt_pass["status"] == "Analysis" else "transformation"
            data[pass_name]["percentage"] = 0
        data_pass = data[pass_name]
        data_pass["percentage"] += 1
        if opt_pass["status"] == "Analysis":
            data_pass = emplace_back_int("times", 1, data_pass)
        elif opt_pass["status"] in ["Passed", "Missed"]:
            data_pass['passed'] = 0
            data_pass['missed'] = 0
            data_pass = emplace_back_int(opt_pass["status"].lower(), 1, data_pass)
    for key in data:
        data[key]["percentage"] /= npasses / 100
    return data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("opt_yaml_file", help="opt yaml generated with -fsave-optimization-record")
    parser.add_argument("--g", help="enable logging of debug info for developement only", action='store_true', default=False)
    args = parser.parse_args()
    if args.g:
        logging.basicConfig(level=logging.INFO)
    filename = args.opt_yaml_file
    f = open(filename).read()
    passes = list_passes(optYaml2Json(f))
    pprint(passes)
    percent = 0.0
    for key in passes:
        percent += passes[key]['percentage']
    print(percent)