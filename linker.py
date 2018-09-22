#!/usr/bin/env python3
import argparse
import csv
import json
import sys

import networkx as nx
from networkx.readwrite import json_graph


parser = argparse.ArgumentParser(description='Analyze Wikipedia links.')
parser.add_argument('page_links', type=argparse.FileType('r'),
                    help='CSV database of page links')
parser.add_argument('pages_from', type=argparse.FileType('r'),
                    help='list of articles from which to find links (PetScan JSON)')
parser.add_argument('pages_to', type=argparse.FileType('r'),
                    help='list of articles to which to find links (PetScan JSON)')
parser.add_argument('output', type=argparse.FileType('w'),
                    help='output file')
parser.add_argument('--reverse', action='store_true',
                    help='reverse edge direction in output graph')
args = parser.parse_args()


pages_from = set()  # page IDs
pages_to = set()  # page titles

# map from page IDs to titles
# since pl_from is given as IDs
id_to_title = {}

g = nx.DiGraph()

# load 'from' pages
f_data = json.load(args.pages_from)
for page in f_data['*'][0]['a']['*']:
    pages_from.add(page['id'])
    id_to_title[page['id']] = page['title']

# load 'to' pages
t_data = json.load(args.pages_to)
for page in t_data['*'][0]['a']['*']:
    pages_to.add(page['title'])

# search page links
reader = csv.reader(args.page_links)
for row in reader:
    pl_from = int(row[0])
    pl_from_namespace = row[1]
    pl_title = row[2]
    pl_namespace = row[3]

    # ignore links outside default namespace
    if pl_from_namespace is '0' and pl_namespace is '0' and \
       pl_from in pages_from and pl_title in pages_to:
        g.add_edge(id_to_title[pl_from], pl_title)

# process graph
if args.reverse:
    g.reverse(copy=False)
g = nx.convert_node_labels_to_integers(g, label_attribute='id')
g_json = json_graph.node_link_data(g, attrs={'name': 'index'})
json.dump(g_json, args.output, separators=(',', ':'))
