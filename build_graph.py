"""
build_graph.py - regenerate the data block inside concordagraph.html.

Reads corpus_nodes.csv, corpus_edges.csv and corpus_clusters.csv, checks every
reference against your verse index, refuses to write if anything fails, then
splices the generated block between the // <corpus> and // </corpus> markers.

    python3 build_graph.py
    python3 build_graph.py --no-verify      # skip the index check

Edit the CSVs, run this, reload the page. Do not hand-edit the block
between the markers — it is overwritten.

Three module rules, settled in DESIGN.md:

1. Ids are namespaced at build time from module.json. A bare id in a CSV
   (`g1`) becomes `tithe:g1`. An id that ALREADY carries a prefix is left
   alone, which is how a cross-module edge is written. Edges pointing out of
   this module are validated and held back from the single-module page,
   because it has no node to attach them to; the master compile is where they
   land.

2. Clusters live in corpus_clusters.csv, not in this script, so a second
   module needs no edit here. The `role` column carries layout meaning: the
   one cluster marked `hub` is drawn at the centre. The renderer asks for the
   role, it does not know any cluster by name.

3. Reference is identity; everything else is module-scoped. Within a module a
   verse appears at most once — enforced below. Across modules the same verse
   may appear once per module, each with its own cluster and its own summary,
   and each node carries its module so the renderer can tell them apart.
"""
import argparse, csv, json, os, sys
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument('--nodes', default='corpus_nodes.csv')
ap.add_argument('--edges', default='corpus_edges.csv')
ap.add_argument('--clusters', default='corpus_clusters.csv')
ap.add_argument('--module', default='module.json')
ap.add_argument('--graph', default='concordagraph.html')
ap.add_argument('--index', default='verses.json')
ap.add_argument('--no-verify', action='store_true')
a = ap.parse_args()

fail, warn, notes = [], [], []

# --- the module ------------------------------------------------------------
if not os.path.exists(a.module):
    sys.exit(f'{a.module} not found. It names this module: {{"slug": "...", "title": "..."}}')
mod = json.load(open(a.module, encoding='utf-8'))
SLUG, TITLE = mod.get('slug', ''), mod.get('title', '')
if not SLUG:
    sys.exit(f'{a.module}: no "slug".')
if ':' in SLUG:
    sys.exit(f'{a.module}: slug {SLUG!r} must not contain a colon — it is the namespace separator.')

def qualify(i):
    """Bare ids get this module's prefix. Already-qualified ids pass through."""
    i = i.strip()
    return i if ':' in i else f'{SLUG}:{i}'

# --- clusters: name, colours and layout role, per module -------------------
if not os.path.exists(a.clusters):
    sys.exit(f'{a.clusters} not found. Columns: key,name,light,dark,role')
CLUSTERS = []
for row in csv.DictReader(open(a.clusters, encoding='utf-8')):
    CLUSTERS.append((row['key'].strip(), row['name'], row['light'].strip(),
                     row['dark'].strip(), (row.get('role') or '').strip()))
for k, name, lt, dk, role in CLUSTERS:
    if role not in ('', 'hub'):
        fail.append(f'cluster {k}: unknown role {role!r} — use "hub" or leave it blank')
hubs = [k for k, _, _, _, role in CLUSTERS if role == 'hub']
if len(hubs) > 1:
    fail.append(f'more than one cluster marked hub: {", ".join(hubs)}')
dupcl = [k for k, c in Counter(k for k, *_ in CLUSTERS).items() if c > 1]
for k in dupcl:
    fail.append(f'duplicate cluster key: {k}')

nodes = list(csv.DictReader(open(a.nodes, encoding='utf-8')))
edges = list(csv.DictReader(open(a.edges, encoding='utf-8')))
known = {c[0] for c in CLUSTERS}

for n in nodes:
    n['id'] = qualify(n['id'])
for e in edges:
    e['source'], e['target'] = qualify(e['source']), qualify(e['target'])

ids = [n['id'] for n in nodes]
for d, c in Counter(ids).items():
    if c > 1: fail.append(f'duplicate node id: {d}')
for n in nodes:
    if n['cluster'] not in known: fail.append(f"{n['id']}: unknown cluster {n['cluster']}")

# Reference is identity: one module may not cite the same verse twice, or the
# master compile cannot tell a genuine cross-module sharing from a local typo.
for r, c in Counter(n['ref'].strip() for n in nodes).items():
    if c > 1:
        who = ', '.join(n['id'] for n in nodes if n['ref'].strip() == r)
        fail.append(f'{r} is cited by {c} nodes in this module ({who}) — reference is identity')

# A cluster nobody uses still takes a legend slot and a colour. Warn, do not
# fail: staging a cluster before populating it is legitimate.
used = {n['cluster'] for n in nodes}
for k, name, *_ in CLUSTERS:
    if k not in used:
        notes.append(f'cluster {k} ({name}) is defined but no node uses it')

idset = set(ids)
is_external = set()                          # indices into edges, not copies
for i, e in enumerate(edges):
    for end in ('source', 'target'):
        v = e[end]
        if v.split(':', 1)[0] != SLUG:
            is_external.add(i)               # points out of this module
        elif v not in idset:
            fail.append(f"edge {end} missing: {v}")
    if e['kind'] not in ('lex','ref','con'): fail.append(f"bad kind: {e['kind']}")
    if e['warrant'] not in ('states','supports','spec'): fail.append(f"bad warrant: {e['warrant']}")
seen = set()
for e in edges:
    k = tuple(sorted((e['source'], e['target'])))
    if k in seen: fail.append(f'duplicate edge: {k[0]}–{k[1]}')
    seen.add(k)
external = [e for i, e in enumerate(edges) if i in is_external]
local = [e for i, e in enumerate(edges) if i not in is_external]

if not a.no_verify:
    if not os.path.exists(a.index):
        sys.exit(f'{a.index} not found. Run nrsv_index.py, or pass --no-verify.')
    raw = {r['ref']: r['text'] for r in json.load(open(a.index))}
    index = set(raw)
    for n in nodes:
        if n['ref'] not in index:
            fail.append(f"{n['id']}: {n['ref']} does not resolve in the index")

    # A resolvable reference is not a correct one. This catches the case where a
    # summary describes a different verse than the one it cites: no content word
    # in common between the summary and the verse. It WARNS rather than fails,
    # because meta-summaries ("Mark's form of the ruling") legitimately share no
    # vocabulary with the text. Read the list; do not ignore it.
    import re as _re
    STOP = set("""the and for with that this from they them their there then than have has
    had was were will would shall should could been being into onto upon what which who whom
    whose when where while because before after over under again more most other some such
    only own same both each all any are but not you your his her its our out off down about
    against form account version repeated cited together""".split())
    _stem = lambda w: _re.sub(r'(ies|es|s)$', '', w)
    def _words(s):
        return {_stem(w) for w in _re.findall(r"[a-z']+", s.lower())
                if len(w) > 3 and w not in STOP}
    for n in nodes:
        t = raw.get(n['ref'])
        if t and not (_words(n['gist']) & _words(t)):
            warn.append(f"{n['id']} ({n['ref']}): summary shares no wording with the verse "
                        f"— check it names the right passage")

if fail:
    print('refusing to write:', file=sys.stderr)
    for f in fail: print('  ', f, file=sys.stderr)
    sys.exit(1)

j = lambda s: json.dumps(s, ensure_ascii=False)
out = ['// <corpus>  generated by build_graph.py — edit the CSVs, not this block']
out.append(f'const MOD = {j(SLUG)};')
out.append('const MODS = {')
out.append(f'  {SLUG}:{{title:{j(TITLE)}}},')
out.append('};')
out.append('const CL = {')
for k, name, lt, dk, role in CLUSTERS:
    out.append(f'  {k}:{{name:{j(name)},light:{j(lt)},dark:{j(dk)},role:{j(role)}}},')
out.append('};')
out.append('const N = [')
for n in nodes:
    out.append(f"  [{j(n['id'])},{j(n['ref'])},{j(n['cluster'])},{j(n['gist'])},{j(SLUG)}],")
out.append('];')
out.append('const E = [')
for e in local:
    out.append(f"  [{j(e['source'])},{j(e['target'])},{j(e['kind'])},{j(e['warrant'])},{j(e['note'])}],")
out.append('];')
out.append('// </corpus>')
block = '\n'.join(out)

html = open(a.graph, encoding='utf-8').read()
s, t = html.find('// <corpus>'), html.find('// </corpus>')
if s < 0 or t < 0:
    sys.exit('markers // <corpus> and // </corpus> not found in the graph file.')
html = html[:s] + block + html[t + len('// </corpus>'):]
open(a.graph, 'w', encoding='utf-8').write(html)

print(f'module: {SLUG} — {TITLE}')
print(f'wrote {len(nodes)} nodes, {len(local)} edges into {a.graph}')
if external:
    print(f'{len(external)} cross-module edge(s) held back — they have no node to attach to here:')
    for e in external: print(f"   {e['source']} -> {e['target']}")
if warn:
    print(f'\n{len(warn)} node(s) to check by eye:')
    for w in warn: print('  ', w)
if notes:
    print(f'\n{len(notes)} corpus note(s):')
    for n_ in notes: print('  ', n_)
print('clusters:', ', '.join(f'{k}={v}' for k, v in
      sorted(Counter(n["cluster"] for n in nodes).items(), key=lambda x: -x[1])))
hub = hubs[0] if hubs else None
print('hub cluster:', hub if hub else '(none — nothing drawn at the centre)')
