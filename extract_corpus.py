"""extract_corpus.py - pull the node, edge and cluster tables out of
concordagraph.html. Recovery tool: use it when the CSVs are lost and the
generated block in the HTML is the only surviving copy of the corpus.

Ids are written back UNPREFIXED for this module, matching the shape you hand
edit. An id carrying some other module's prefix is left qualified, because
that is a cross-module reference and the prefix is part of it.

The tables are read as the JSON build_graph.py wrote them, not matched field by
field, so a summary containing a quote, a book name with spaces, or a cluster
key that is not one lowercase word comes back intact. The cluster table used to
be matched by a pattern that stopped matching when the note column was added,
and from then on recovered no clusters at all without saying so (QUESTIONS.md
Q3). It now refuses rather than writing a partial table.

    python extract_corpus.py [page.html] [--out DIR]     # DIR defaults to .
"""
import re, csv, sys, json, os

args = [x for x in sys.argv[1:]]
out = '.'
if '--out' in args:
    i = args.index('--out'); out = args[i + 1]; del args[i:i + 2]
page = args[0] if args else 'concordagraph.html'
html = open(page, encoding='utf-8').read()

SLUG = ''
if os.path.exists('module.json'):
    SLUG = json.load(open('module.json', encoding='utf-8')).get('slug', '')
if not SLUG:
    m = re.search(r'^const MOD = "([^"]+)";', html, re.M)
    SLUG = m.group(1) if m else ''


def bare(i):
    """Drop this module's prefix; leave any other module's prefix in place."""
    return i[len(SLUG) + 1:] if SLUG and i.startswith(SLUG + ':') else i


def block(start, end):
    """The lines between `start` and the first line equal to `end`."""
    m = re.search('^' + re.escape(start) + r'\r?\n(.*?)^' + re.escape(end) + r'\r?$',
                  html, re.M | re.S)
    if not m:
        sys.exit(f'refused: no "{start}" table found in {page}')
    return m.group(1)


def array(start):
    body = block(start, '];').strip().rstrip(',')
    return json.loads('[' + body + ']')


nodes = array('const N = [')
edges = array('const E = [')

STR = r'"(?:[^"\\]|\\.)*"'
CLUSTER = re.compile(
    r'^\s*(' + STR + r'|[A-Za-z_$][\w$]*):\{name:(' + STR + r'),light:(' + STR + r'),'
    r'dark:(' + STR + r')(?:,role:(' + STR + r'))?(?:,note:(' + STR + r'))?\},\s*$')
clusters, bad = [], []
for line in block('const CL = {', '};').splitlines():
    if not line.strip():
        continue
    m = CLUSTER.match(line)
    if not m:
        bad.append(line.strip()[:80]); continue
    key = m.group(1)
    key = json.loads(key) if key.startswith('"') else key
    clusters.append([key] + [json.loads(g) if g else '' for g in m.groups()[1:]])
if bad:
    sys.exit('refused: cluster lines not understood, nothing written:\n  ' + '\n  '.join(bad))

with open(os.path.join(out, 'corpus_nodes.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['id', 'ref', 'cluster', 'gist'])
    w.writerows([bare(n[0]), n[1], n[2], n[3]] for n in nodes)
with open(os.path.join(out, 'corpus_edges.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['source', 'target', 'kind', 'warrant', 'note'])
    w.writerows([bare(s), bare(t), k, wa, note] for s, t, k, wa, note in edges)
with open(os.path.join(out, 'corpus_clusters.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['key', 'name', 'light', 'dark', 'role', 'note'])
    w.writerows(clusters)

print(f'module {SLUG or "(none found)"}')
print(f'nodes {len(nodes)}  edges {len(edges)}  clusters {len(clusters)}')
