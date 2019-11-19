#! /usr/bin/env python3

from yaml2json import optYaml2Json
import logging

def getAsExpected(json_string):
    json_string.pop('Function', None)
    return json_string

def transform_json(yaml_string):
    json_string = optYaml2Json(yaml_string)
    new_json_string = {}
    for each_pass in json_string:
        function = each_pass['Function']
        if function in new_json_string:
            new_json_string[function].append(getAsExpected(each_pass))
        else:
            new_json_string[function] = [getAsExpected(each_pass)]
    return new_json_string

if __name__ == "__main__":
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help='opt.yaml file to be converted')
    parser.add_argument("--g", help="enable logging of debug info for developement only", action='store_true', default=False)
    args = parser.parse_args()
    if args.g:
        logging.basicConfig(level=logging.DEBUG)
    f = open(args.file)
    g = f.read()
    pprint(transform_json(g))