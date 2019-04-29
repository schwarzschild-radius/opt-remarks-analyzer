#!/usr/bin/env python3
import yaml
import argparse
from pprint import pprint

def toDict(loader, tag_suffix, node):
    pass

class ToDict():
    def __init__(self):
        self.summary = {"Passed" : [], "Missed" : [], "Analysis" : []}
    def __call__(self, loader, tag_suffix, node):
        self.summary[tag_suffix].append({"name" : node.value[0][1].value})
        return tag_suffix
    def get_summary(self):
        return self.summary
        

def other(loader, node):
    print(node)

def get_json(yaml_string):
    toDict = ToDict()
    yaml.add_multi_constructor("!", toDict)
    [i for i in yaml.load_all(yaml_string)]
    return toDict.get_summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("opt_yaml_file", help="opt yaml generated with -fsave-optimization-record")
    args = parser.parse_args()
    filename = args.opt_yaml_file
    f_handle = open(filename)
    f_data = f_handle.read()
    get_json(f_data)