"""crossexam.py - read the corpus through seven translations at once.

Three questions, each answerable only now that translations.json and
strongs_index.json both exist:

  hidden   Pairs that share a RARE Hebrew or Greek word but almost no English
           word in common. The connection is real and the translations bury it.
           These are the strongest candidates for new `lex` edges.

  fragile  Existing `lex` edges whose shared wording survives in few
           translations. The edge may still be right - the lemma decides that -
           but "shared wording" is a claim about a word, and if six translators
           disagree about which word, the claim needs the lemma to stand on.

  false    Pairs that share distinctive ENGLISH across many translations while
           sharing no lemma at all. Translation artefacts: exactly the kind of
           connection associative reading manufactures.

    python crossexam.py hidden
    python crossexam.py fragile
    python crossexam.py false
"""
import json, csv, sys, re, itertools, collections

TRANS = json.load(open('translations.json', encoding='utf-8'))
LEM = json.load(open('strongs_index.json', encoding='utf-8'))
verses, gloss = LEM['verses'], LEM['gloss']

nodes = list(csv.DictReader(open('corpus_nodes.csv', encoding='utf-8')))
byid = {n['id']: n for n in nodes}
clusters = {r['key']: r['name'] for r in
            csv.DictReader(open('corpus_clusters.csv', encoding='utf-8'))}
edges = list(csv.DictReader(open('corpus_edges.csv', encoding='utf-8')))
linked = {tuple(sorted((e['source'], e['target']))) for e in edges}

den = collections.Counter()
for nums in verses.values():
    for n in set(nums):
        den[n] += 1

WORD = re.compile(r"[A-Za-z']+")


def words(ref, version):
    t = TRANS.get(ref, {}).get(version)
    return set(w.lower() for w in WORD.findall(t)) if t else set()


VERSIONS = ['KJV', 'Geneva1599', 'DRC', 'ASV', 'YLT', 'BSB']

# A word in many of the 158 corpus verses is not distinctive, whatever it means.
df = collections.Counter()
for ref in TRANS:
    seen = set()
    for v in VERSIONS:
        seen |= words(ref, v)
    for w in seen:
        df[w] += 1
COMMON = {w for w, c in df.items() if c > 24}      # >15% of the corpus


def distinctive(ref, version):
    return words(ref, version) - COMMON


def english_overlap(a, b):
    """In how many translations do these two verses share a distinctive word?"""
    n, shared = 0, set()
    for v in VERSIONS:
        s = distinctive(a, v) & distinctive(b, v)
        if s:
            n += 1
            shared |= s
    return n, shared


def label(n):
    return '%-20s [%s]' % (n['ref'], clusters.get(n['cluster'], n['cluster']))


have = [n for n in nodes if n['ref'] in verses and n['ref'] in TRANS]
mode = sys.argv[1] if len(sys.argv) > 1 else 'hidden'

if mode == 'hidden':
    print('HIDDEN - a rare shared lemma the English mostly does not show\n')
    rows = []
    for a, b in itertools.combinations(have, 2):
        if tuple(sorted((a['id'], b['id']))) in linked:
            continue
        shared = set(verses[a['ref']]) & set(verses[b['ref']])
        rare = sorted([L for L in shared if den[L] <= 40], key=lambda L: den[L])
        if not rare:
            continue
        n_eng, eng = english_overlap(a['ref'], b['ref'])
        if n_eng <= 2:
            rows.append((den[rare[0]], n_eng, a, b, rare, eng))
    rows.sort(key=lambda r: (r[0], r[1]))
    print('%d pair(s).\n' % len(rows))
    for d, n_eng, a, b, rare, eng in rows[:25]:
        print('%s\n%s' % (label(a), label(b)))
        for L in rare[:3]:
            print('     %-8s %-26s %3d verses' % (L, gloss.get(L, '')[:26], den[L]))
        print('     shared distinctive English in %d of %d translations%s'
              % (n_eng, len(VERSIONS), (': ' + ', '.join(sorted(eng))) if eng else ''))
        print()

elif mode == 'fragile':
    print('FRAGILE - existing `lex` edges, and how well the English holds up\n')
    for e in edges:
        if e['kind'] != 'lex':
            continue
        a, b = byid[e['source']], byid[e['target']]
        if a['ref'] not in TRANS or b['ref'] not in TRANS:
            continue
        n_eng, eng = english_overlap(a['ref'], b['ref'])
        shared = set(verses.get(a['ref'], [])) & set(verses.get(b['ref'], []))
        rare = sorted([L for L in shared if den[L] <= 200], key=lambda L: den[L])
        flag = '' if n_eng >= 4 else ('   <-- thin' if n_eng >= 1 else '   <-- ENGLISH SHOWS NOTHING')
        print('%-18s %-18s  english %d/%d, rarest lemma %s%s'
              % (a['ref'], b['ref'], n_eng, len(VERSIONS),
                 ('%s in %d verses' % (rare[0], den[rare[0]])) if rare else 'NONE', flag))

elif mode == 'false':
    # WITHIN ONE TESTAMENT ONLY. Strong's numbers do not cross between Hebrew
    # and Greek, so every Old-to-New pair trivially "shares no lemma" - the
    # first run of this mode ranked Genesis 14:20 against Hebrews 7:6 at the
    # top, which is Hebrews quoting Genesis and about as real as a link gets.
    # Across that boundary the test is not weak, it is meaningless.
    OT = {'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Ruth',
          '1 Samuel', 'Nehemiah', 'Psalm', 'Ezekiel', 'Amos', 'Zechariah',
          'Malachi'}
    PRONOUNS = {'me', 'my', 'him', 'his', 'her', 'them', 'they', 'thee', 'thou',
                'thy', 'ye', 'you', 'your', 'us', 'we', 'our', 's', 'up', 'out',
                'also', 'had', 'have', 'haue', 'where', 'when', 'said', 'saith',
                'unto', 'shall', 'came', 'went', 'go', 'one', 'man', 'men'}

    def testament(n):
        return 'OT' if n['ref'].rsplit(' ', 1)[0] in OT else 'NT'

    print('FALSE FRIENDS - distinctive English shared widely, no shared lemma')
    print('Within one testament only, and ignoring pronouns and common verbs.\n')
    rows = []
    for a, b in itertools.combinations(have, 2):
        if tuple(sorted((a['id'], b['id']))) in linked:
            continue
        if testament(a) != testament(b):
            continue
        if set(verses[a['ref']]) & set(verses[b['ref']]):
            continue
        n_eng, eng = english_overlap(a['ref'], b['ref'])
        eng -= PRONOUNS
        if n_eng >= 4 and len(eng) >= 2:
            rows.append((n_eng, a, b, eng))
    rows.sort(key=lambda r: -r[0])
    print('%d pair(s).\n' % len(rows))
    for n_eng, a, b, eng in rows[:20]:
        print('%s\n%s' % (label(a), label(b)))
        print('     %d/%d translations share: %s'
              % (n_eng, len(VERSIONS), ', '.join(sorted(eng))))
        print('     no shared lemma at all.')
        print()
else:
    sys.exit('modes: hidden | fragile | false')
