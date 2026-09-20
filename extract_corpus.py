"""extract_corpus.py - pull the node and edge tables out of concordagraph.html."""
import re, csv, sys

html = open(sys.argv[1] if len(sys.argv) > 1 else 'concordagraph.html', encoding='utf-8').read()

nodes = re.findall(
    r'^\s*\["([a-z]+\d+)","((?:[1-4] )?[A-Z][A-Za-z]+ \d+:\d+)","([a-z]+)","([^"]*)"\]',
    html, re.M)
edges = re.findall(
    r'\["([a-z]+\d+)","([a-z]+\d+)","(lex|ref|con)","(states|supports|spec)","([^"]*)"\]',
    html)

with open('corpus_nodes.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['id', 'ref', 'cluster', 'gist']); w.writerows(nodes)
with open('corpus_edges.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['source', 'target', 'kind', 'warrant', 'note']); w.writerows(edges)

print(f'nodes {len(nodes)}  edges {len(edges)}')
