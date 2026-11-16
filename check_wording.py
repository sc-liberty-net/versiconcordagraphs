"""Refuse summaries and edge notes that share a run of five or more words with
the NRSV text of a verse they describe. Both ship on the public page.

    python check_wording.py      # exit 0 clean, 1 with a list of runs
"""
import csv, json, re, sys
RUN = 5
words = lambda s: re.findall(r"[a-z0-9']+", s.lower().replace('’', "'"))
V = {r['ref']: r['text'] for r in json.load(open('verses.json', encoding='utf-8'))}
nodes = list(csv.DictReader(open('corpus_nodes.csv', encoding='utf-8')))
ref = {n['id']: n['ref'] for n in nodes}

def runs(text, refs):
    g, hits = words(text), set()
    for r in refs:
        v = words(V[r])
        vs = {tuple(v[i:i + RUN]) for i in range(len(v) - RUN + 1)}
        hits |= {' '.join(g[i:i + RUN]) for i in range(len(g) - RUN + 1) if tuple(g[i:i + RUN]) in vs}
    return sorted(hits)

bad = []
for n in nodes:
    if h := runs(n['gist'], [n['ref']]):
        bad.append(f"node {n['id']} ({n['ref']}): {h}")
for e in csv.DictReader(open('corpus_edges.csv', encoding='utf-8')):
    ends = [ref[x] for x in (e['source'], e['target']) if x in ref]
    if h := runs(e['note'], ends):
        bad.append(f"edge {e['source']}-{e['target']}: {h}")
if bad:
    print(f'{len(bad)} item(s) share {RUN}-word runs with the NRSV:')
    print('\n'.join('  ' + b for b in bad))
    sys.exit(1)
print(f'wording: {len(nodes)} summaries and all edge notes clear of {RUN}-word NRSV runs')
