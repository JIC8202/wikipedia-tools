#!/usr/bin/env python3
import argparse
import json

from pymongo import MongoClient


parser = argparse.ArgumentParser(description='Import JSON graph to MongoDB.')
parser.add_argument('graph', type=argparse.FileType('r'),
                    help='JSON graph file to import')
parser.add_argument('uri', help='MongoDB Connection String URI')
args = parser.parse_args()

# load graph data
graph = json.load(args.graph)

# connect to mongodb
client = MongoClient(args.uri)
db = client.tmsdse

# clear and insert nodes
db.nodes.drop()
db.nodes.insert_many(graph['nodes'])

# clear and insert links
db.links.drop()
db.links.insert_many(graph['links'])