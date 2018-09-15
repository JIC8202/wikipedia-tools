#!/usr/bin/env python3
import argparse
import csv
import json
import sys

parser = argparse.ArgumentParser(description='Analyze Wikipedia links.')
parser.add_argument('page_links', type=argparse.FileType('r'),
                    help='CSV database of page links')
parser.add_argument('pages_from', type=argparse.FileType('r'),
                    help='list of articles from which to find links (PetScan JSON)')
parser.add_argument('pages_to', type=argparse.FileType('r'),
                    help='list of articles to which to find links (PetScan JSON)')
parser.add_argument('output', type=argparse.FileType('w'), default=sys.stdout,
                    help='output file')

args = parser.parse_args()

pages_from = set() # page IDs
pages_to = set() # page titles

id_to_title = {}

# load 'from' pages
data = json.load(args.pages_from)
for page in data['*'][0]['a']['*']:
    pages_from.add(page['id'])
    id_to_title[page['id']] = page['title']

# load 'to' pages
data = json.load(args.pages_to)
for page in data['*'][0]['a']['*']:
    pages_to.add(page['title'])

# search page links
reader = csv.reader(args.page_links)
for row in reader:
    pl_from = int(row[0])
    pl_from_namespace = row[1]
    pl_title = row[2]
    pl_namespace = row[3]

    # only consider links within main namespace
    if pl_from_namespace is not '0' or pl_namespace is not '0':
        continue

    if pl_from in pages_from and pl_title in pages_to:
        print('%s => %s' % (id_to_title[pl_from], pl_title), file=args.output)
