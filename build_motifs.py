"""build_motifs.py - write the motif table into corpus_motifs.csv.

A motif is a Hebrew or Greek word that recurs across the corpus, and it is a
DIFFERENT axis from a cluster. A node sits in exactly one cluster, because a
cluster is a topic and a passage is about one thing. A node carries as many
motifs as it has words, because a motif cuts across topics by construction:
argyrion runs through `entrusted`, `giving`, `price` and `metal`; denarion
through `debt`, `imperial` and `wages`. Filing either as a cluster would mean
pulling verses out of the topic they belong to.

So this generates a third table, keyed on Strong's numbers rather than on
editorial judgement, and build_graph.py writes it into the page beside the
clusters. The rail gets a fourth filter group.

THE DENOMINATOR IS THE POINT. Each motif records how many verses in the whole
Bible carry its lemma. A motif shared by four verses is evidence; one shared by
four hundred is vocabulary, and the page should not render them alike. That
number is printed in the legend.

    python build_motifs.py            # -> corpus_motifs.csv
    python build_motifs.py --report   # also print what each motif caught

Edit MOTIFS below to add one. Everything else is derived.
"""
import json, csv, sys, collections, io

# key, label, and the lemmas it is made of. Hebrew and Greek are listed
# together on purpose: Strong's numbers do not cross between them, so a motif
# that runs through both testaments must name both sides by hand. That is a
# limitation of the index, recorded here rather than hidden.
MOTIFS = [
    ('treasure', 'Treasure', ['G2344', 'G2343', 'G1049', 'H0214'],
     'What is stored, and where.'),
    ('silver', 'Silver and gold', ['G0694', 'G5553', 'G0696', 'H3701', 'H2091'],
     'The metal itself, as price, offering and ransom.'),
    ('coin', 'The daily coin', ['G1220', 'G4715', 'G3546'],
     "A day's wage, the tax coin and the debt unit are one piece of silver."),
    ('tithe', 'The tenth', ['G0586', 'G1183', 'G1181', 'H4643', 'H6237'],
     'Every word for a tenth, given or collected.'),
    # G5056 telos was here and is deliberately gone. It means toll - the NRSV
    # uses that word for it in Matthew 17:25 - but it also means END, and it
    # was pulling Hebrews 7:3, 'neither beginning of days nor end of life',
    # into a fiscal motif. Both genuine fiscal verses are already caught:
    # Matthew 17:25 by kensos, Romans 13:7 by phoros. A lemma that resolves
    # is not a lemma in the right sense.
    ('tax', 'Tax and tribute', ['G2778', 'G5411', 'G1323', 'H4522', 'H4061'],
     'The fiscal vocabulary proper, across two Greek words and two Hebrew.'),
    ('collector', 'The collector', ['G5057', 'G0754', 'G5058'],
     'The trade, the office, and the booth.'),
    ('debt', 'Debt and what is owed', ['G3781', 'G3784', 'G3782', 'G5533', 'H5378'],
     'Owing, and the one who owes.'),
    ('gift', 'Gift and offering', ['G1435', 'G2878', 'G1654', 'H7133', 'H4503'],
     'What is handed over as a gift rather than as a payment.'),
    ('poor', 'The poor and the landless', ['G4434', 'G3993', 'H0034', 'H6041', 'H1616', 'H3490', 'H0490'],
     'The alien, the orphan, the widow and the poor.'),
    ('blessing', 'Blessing', ['G2127', 'G2129', 'H1288'],
     'Who blesses whom, which Hebrews 7:7 turns into an argument about rank.'),
]

idx = json.load(open('strongs_index.json', encoding='utf-8'))
verses, gloss = idx['verses'], idx['gloss']

den = collections.Counter()
for nums in verses.values():
    for n in set(nums):
        den[n] += 1

nodes = list(csv.DictReader(io.open('corpus_nodes.csv', encoding='utf-8')))

rows, report = [], []
for key, label, lemmas, note in MOTIFS:
    hits = [n for n in nodes
            if any(L in verses.get(n['ref'], []) for L in lemmas)]
    if not hits:
        print('SKIPPED %s: no node carries any of %s' % (key, ','.join(lemmas)))
        continue
    # Bible-wide denominator: verses carrying ANY of this motif's lemmas.
    scope = len({r for r, nums in verses.items() if any(L in nums for L in lemmas)})
    rows.append((key, label, ' '.join(sorted(n['id'] for n in hits)), scope, note))
    report.append((key, label, hits, scope, lemmas))

with io.open('corpus_motifs.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['key', 'name', 'nodes', 'scope', 'note'])
    w.writerows(rows)

print('wrote corpus_motifs.csv: %d motifs over %d nodes'
      % (len(rows), len({i for r in rows for i in r[2].split()})))

if '--report' in sys.argv:
    clusters = {c['key']: c['name'] for c in
                csv.DictReader(io.open('corpus_clusters.csv', encoding='utf-8'))}
    byid = {n['id']: n for n in nodes}
    print()
    for key, label, hits, scope, lemmas in report:
        cl = sorted({h['cluster'] for h in hits})
        print('%-10s %-24s %3d node(s) across %d cluster(s), %4d verses Bible-wide'
              % (key, label, len(hits), len(cl), scope))
        print('           groups: %s' % ', '.join(clusters.get(c, c) for c in cl))
        for L in lemmas:
            if den[L]:
                print('           %-8s %-24s %4d verses' % (L, gloss.get(L, '')[:24], den[L]))
        print()
