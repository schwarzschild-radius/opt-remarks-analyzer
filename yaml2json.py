#! /usr/bin/env python3

import yaml
# using C yaml version
from yaml import CLoader as Loader
import logging

def node2Json(node):
    if type(node) == tuple:
        tup = {}
        logging.debug("Tuple")
        tup[node2Json(node[0])] = node2Json(node[1])
        return tup
    value = node.value
    if type(node) == yaml.nodes.ScalarNode:
        logging.debug("ScalarNode")
        return value
    if type(node) == yaml.nodes.MappingNode:
        yml = {}
        logging.debug("MappingNode")
        for key in value:
            yml[node2Json(key[0])] = node2Json(key[1])
        return yml
    if type(node) == yaml.nodes.SequenceNode:
        logging.debug("SequenceNode")
        li = []
        for item in value:
            li.append(node2Json(item))
        return li
    return {}

def nodeTypes(root):
    if type(root) == tuple:
        return nodeTypes(root[1])
    print(type(root))

def multi_constructor(loader, tag, node):
    data = node2Json(node)
    data["status"] = tag
    return data

def optYaml2Json(yaml_string):
    yaml.add_multi_constructor("!", multi_constructor, Loader=Loader)
    data = []
    for i in yaml.load_all(yaml_string, Loader=Loader):
        data.append(i)
    return data

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
    js = {}
    js['2mm.c.opt.yaml'] = optYaml2Json(g)
    pprint(js)