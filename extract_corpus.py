"""extract_corpus.py - pull the node, edge and cluster tables out of
concordagraph.html. Recovery tool: use it when the CSVs are lost and the
generated block in the HTML is the only surviving copy of the corpus.

Ids are written back UNPREFIXED for this module, matching the shape you hand
edit. An id carrying some other module's prefix is left qualified, because
that is a cross-module reference and the prefix is part of it.
"""
import re, csv, sys, json, os

html = open(sys.argv[1] if len(sys.argv) > 1 else 'concordagraph.html', encoding='utf-8').read()

SLUG = ''
if os.path.exists('module.json'):
    SLUG = json.load(open('module.json', encoding='utf-8')).get('slug', '')
if not SLUG:
    m = re.search(r'^const MOD = "([^"]+)";', html, re.M)
    SLUG = m.group(1) if m else ''

ID = r'(?:[a-z][a-z0-9_-]*:)?[a-z]+\d+'          # optional module prefix


def bare(i):
    """Drop this module's prefix; leave any other module's prefix in place."""
    return i[len(SLUG) + 1:] if SLUG and i.startswith(SLUG + ':') else i


nodes = re.findall(
    r'^\s*\["(' + ID + r')","((?:[1-4] )?[A-Z][A-Za-z]+ \d+:\d+)","([a-z]+)","([^"]*)"',
    html, re.M)
edges = re.findall(
    r'\["(' + ID + r')","(' + ID + r')","(lex|ref|con)","(states|supports|spec)","([^"]*)"\]',
    html)
clusters = re.findall(
    r'^\s*([a-z]+):\{name:"([^"]*)",light:"([^"]*)",dark:"([^"]*)"(?:,role:"([^"]*)")?\},',
    html, re.M)

with open('corpus_nodes.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['id', 'ref', 'cluster', 'gist'])
    w.writerows([bare(i), r, c, g] for i, r, c, g in nodes)
with open('corpus_edges.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['source', 'target', 'kind', 'warrant', 'note'])
    w.writerows([bare(s), bare(t), k, wa, note] for s, t, k, wa, note in edges)
if clusters:
    with open('corpus_clusters.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['key', 'name', 'light', 'dark', 'role'])
        w.writerows(clusters)

print(f'module {SLUG or "(none found)"}')
print(f'nodes {len(nodes)}  edges {len(edges)}  clusters {len(clusters)}')
