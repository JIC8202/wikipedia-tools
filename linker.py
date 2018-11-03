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


class PageSet:
    def __init__(self, data):
        self.ids = set()
        self.titles = set()
        self.title_by_id = dict()

        for page in data['*'][0]['a']['*']:
            self.ids.add(page['id'])
            self.titles.add(page['title'])
            self.title_by_id[page['id']] = page['title']

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self.ids
        else:
            return item in self.titles

    def get_title(self, id):
        return self.title_by_id[id]


pages_from = PageSet(json.load(args.pages_from))
pages_to = PageSet(json.load(args.pages_to))

g = nx.DiGraph()

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
        g.add_edge(pages_from.get_title(pl_from), pl_title)

# add group information to nodes
for node in g.nodes:
    group = (node in pages_from) * 2 + (node in pages_to) * 1
    g.nodes[node]['group'] = group

# reverse direction of edges if requested
if args.reverse:
    g = g.reverse(copy=False)

# use numeric indices
g = nx.convert_node_labels_to_integers(g, label_attribute='id')
g_json = json_graph.node_link_data(g, attrs={'name': 'index'})

json.dump(g_json, args.output, separators=(',', ':'))
