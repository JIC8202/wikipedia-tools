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
parser.add_argument('A', type=argparse.FileType('r'),
                    help='list of articles for group A (PetScan JSON)')
parser.add_argument('B', type=argparse.FileType('r'),
                    help='list of articles for group B (PetScan JSON)')
parser.add_argument('output', type=argparse.FileType('w'),
                    help='output file')
args = parser.parse_args()


class PageSet:
    def __init__(self, data=None):
        self.ids = set()
        self.titles = set()
        self.title_by_id = dict()

        if data:
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

    def union(self, B):
        C = PageSet()
        C.ids = self.ids | B.ids
        C.titles = self.titles | B.titles
        C.title_by_id = {**self.title_by_id, **B.title_by_id}
        return C

A = PageSet(json.load(args.A))
B = PageSet(json.load(args.B))
All = A.union(B)

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
       pl_from in All and pl_title in All:
        g.add_edge(All.get_title(pl_from), pl_title)

# add group information to nodes
for node in g.nodes:
    group = (node in B) * 2 + (node in A) * 1
    # node in A:    1
    # node in B:    2
    # node in both: 3
    g.nodes[node]['group'] = group

# use numeric indices
g = nx.convert_node_labels_to_integers(g, label_attribute='id')
g_json = json_graph.node_link_data(g, attrs={'name': 'index'})

# write JSON to output
json.dump(g_json, args.output, separators=(',', ':'))
nx.write_gexf(g, "test.gexf")