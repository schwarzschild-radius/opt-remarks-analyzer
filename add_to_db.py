#! /usr/bin/env python3

from pymongo import MongoClient
import logging
from transform_json import transform_json
from yaml2json import optYaml2Json

def add_to_db(db, yaml_string):
    json_string = optYaml2Json(yaml_string)
    for each_pass in json_string:
        db.Test_Polybench_report.insert_one(each_pass)

def list_passes_from_db(db):
    cursor = db.Test_Polybench_report.find({"$all" : ['Pass']})
    return cursor

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
    client = MongoClient('127.0.0.1:27017')
    db = client.opt_remarks_analysis
    server_status_result = db.command('serverStatus')
    pprint(server_status_result)
    add_to_db(db, g)
    cursor = list_passes_from_db(db)
