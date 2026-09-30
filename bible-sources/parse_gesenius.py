"""Compile the Gesenius page transcripts (Tregelles 1857) into entries keyed
to Strong's numbers.

Input:  lexicons/gesenius/transcript/n020.txt ... n895.txt  (our transcripts)
        stepbible/TBESH ... .txt                    (Strong's numbers + Hebrew lemmas, CC BY)
        lexicons/bdb/bdbToStrongsMapping.csv        (BDB's own Strong's map, CC BY)
Output: lexicons/gesenius/gesenius-entries.json
        lexicons/gesenius/gesenius-report.txt

Images 896-903 are the Grammatical and Analytical Index, not the lexicon,
and are left out. Each transcript line becomes part of exactly one record;
the script refuses to write if any line is lost or used twice.

Matching: a headword is looked up in STEPBible's lemma list by its pointed
form, then by its letters alone. Both books run in Hebrew alphabetical
order, so of all the possible pairings the script keeps the best-scoring
set that stays in order on both sides; words spelled alike are told apart
that way. BDB's map is a second opinion. A pairing is marked check=true
where the evidence is weak or the two sources disagree.
"""
import json
import re
import sys
from pathlib import Path

from gesenius_pages import HEB, TRANSCRIPT, bare, label, norm

HERE = Path(__file__).parent
TBESH = next((HERE / 'stepbible').glob('TBESH*.txt'))
BDB_MAP = HERE / 'lexicons/bdb/bdbToStrongsMapping.csv'
OUT = HERE / 'lexicons/gesenius/gesenius-entries.json'
REPORT = HERE / 'lexicons/gesenius/gesenius-report.txt'
SCAN = 'https://archive.org/details/hebrewchaldeelex00geseuoft/page/n{}/mode/1up'

FIRST, LAST = 20, 895          # lexicon proper; 896-903 are the grammatical index
LAST_STRONGS = 8674
HOMONYM = re.compile(r'^([IV]{1,4})\.\s+')
LEAD = '[(* '                  # what may stand before a headword, as in check()
# A headword may be a compound joined by maqaf (אִישׁ־בֹּשֶׁת); HEB stops at the maqaf.
HEAD_WORD = re.compile(f'(?:{HEB.pattern})(?:־(?:{HEB.pattern}))*')
END = re.compile(r'[.\])"”]\s*$')

# Weight of each kind of evidence in the ordered chain.
W_POINTS_BDB, W_POINTS, W_LETTERS_BDB, W_LETTERS = 4.0, 3.0, 2.0, 1.0


def headword(line):
    """(homonym, headword) if the line opens an entry, else None."""
    s = line.lstrip(LEAD)
    hom = None
    m = HOMONYM.match(s)
    if m:
        hom, s = m.group(1), s[m.end():].lstrip(LEAD)
    m = HEAD_WORD.match(s)
    if not m:
        return None
    return hom, m.group(0)


def is_letter(line):
    """A line that is a single Hebrew letter: a letter-section heading."""
    s = norm(line.strip())
    return len(bare(s)) == 1 and HEB.fullmatch(s) is not None


# ---------------------------------------------------------------- reading
def read_lines():
    """Every transcript line of the lexicon, with where it came from and
    whether it is the first line of a column."""
    out, dropped = [], 0
    for n in range(FIRST, LAST + 1):
        first = True
        for raw in TRANSCRIPT.joinpath(f'n{n:03d}.txt').read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith('RUNNING HEADS:'):
                dropped += 1
                continue
            if line == '=== RIGHT COLUMN ===':
                dropped += 1
                first = True
                continue
            out.append({'image': n, 'text': line, 'col_start': first})
            first = False
    return out, dropped


def cut(lines):
    """Split the lines into records. Returns records and a list saying which
    record (or None, for a dropped line) each line went to."""
    records, owner = [], [None] * len(lines)
    letter = None
    for k, ln in enumerate(lines):
        t = ln['text']
        if is_letter(t):
            if bare(norm(t)) == letter:
                continue                      # the letter printed again over a column
            letter = bare(norm(t))
            records.append({'kind': 'letter', 'homonym': None, 'headword': norm(t),
                            'image': ln['image'], 'lines': [k]})
            owner[k] = len(records) - 1
            continue
        if not records:
            continue                          # the title "LEXICON." on page I
        hw = headword(t)
        prev_line = lines[records[-1]['lines'][-1]]['text']
        # A column may open in the middle of an entry, and that entry may
        # happen to go on with a Hebrew word. The entry before it had not
        # ended if its last line stops without closing punctuation.
        continues = ln['col_start'] and not END.search(prev_line)
        if hw and not continues:
            records.append({'kind': 'entry', 'homonym': hw[0], 'headword': norm(hw[1]),
                            'image': ln['image'], 'lines': [k]})
        else:
            records[-1]['lines'].append(k)
        owner[k] = len(records) - 1
    return records, owner


def join(lines, idx):
    parts = []
    for k in idx:
        t = lines[k]['text']
        if parts and lines[k]['col_start']:
            parts[-1] += ' ' + t              # an entry carried over a column or page
        else:
            parts.append(t)
    return '\n'.join(parts)


# ---------------------------------------------------------------- matching
def load_targets():
    """One row per Strong's number H0001-H8674. The lemma, gloss and language
    come from its first TBESH row; the spellings it may match come from all
    of its rows (Abner is אֲבִינֵר on one row and אַבְנֵר on another)."""
    rows = {}
    for line in TBESH.read_text(encoding='utf-8-sig').splitlines():
        f = line.split('\t')
        # STEPBible splits some numbers into rows (H1328a Bethuel the man,
        # H1328b the place); they are one Strong's number.
        if len(f) < 8 or not re.fullmatch(r'H\d{4}[a-z]?', f[0]) or int(f[0][1:5]) > LAST_STRONGS:
            continue
        f[0] = f[0][:5]
        # A lemma of two words (אַל תַּשְׁחֵת) is one form, not two: joined
        # with a maqaf it matches only the whole phrase.
        forms = ['־'.join(norm(w) for w in HEB.findall(part)) for part in f[3].split(',')]
        forms = [w for w in forms if w]
        if not forms:
            continue
        if f[0] in rows:
            rows[f[0]]['forms'] += [w for w in forms if w not in rows[f[0]]['forms']]
            continue
        rows[f[0]] = {'strongs': f[0], 'estrong': f[1].split()[0], 'lemma': forms[0],
                      'forms': forms, 'gloss': f[6], 'aramaic': f[5].startswith('A:'),
                      'defn': re.sub(r'<[^>]+>', ' ', f[7])}
    return rows


def load_bdb():
    """Headword (pointed, and letters only) -> Strong's numbers, from BDB's map."""
    pointed, letters = {}, {}
    for line in BDB_MAP.read_text(encoding='utf-8-sig').splitlines()[1:]:
        f = line.split(',')
        if len(f) < 3 or not re.fullmatch(r'H\d{4}', f[1]) or f[1] == 'H0000':
            continue
        for w in HEB.findall(f[2]):
            pointed.setdefault(norm(w), set()).add(f[1])
            letters.setdefault(bare(w), set()).add(f[1])
    return pointed, letters


SHIN, SIN = 'ׁ', 'ׂ'
CHALDEE = re.compile(r'\b(?:Ch|Chald|Chaldee)\b')


def dots(w):
    """The shin/sin dot on each ש, or None where the dot is not written."""
    out, w = [], norm(w)
    for k, c in enumerate(w):
        if c == 'ש':
            marks = ''
            for m in w[k + 1:]:
                if not ('֑' <= m <= 'ׇ'):
                    break
                marks += m
            out.append(SHIN if SHIN in marks else SIN if SIN in marks else None)
    return out


def same_sh(a, b):
    """Letters alike are one word only if no ש has shin in one and sin in the other."""
    return all(x is None or y is None or x == y for x, y in zip(dots(a), dots(b)))


SH_FIRST = 7579                # Strong's first ש word (שָׁאַב); ת begins at H8372


def gesenius_order(s, t):
    n = int(s[1:])
    if not SH_FIRST <= n < 8372:
        return (n, 0, n)
    return (SH_FIRST, 1 if dots(t['lemma'])[:1] == [SHIN] else 0, n)


def candidates(rec, text, targets, by_points, by_letters, bdb_p, bdb_l):
    h = rec['headword'].replace('[?]', '')
    hp, hl = norm(h), bare(h)
    bdb = bdb_p.get(hp, set()) | bdb_l.get(hl, set())
    # Gesenius marks Chaldee words "Ch." or "Chald." right after the headword.
    chaldee = bool(CHALDEE.search(text.split('\n')[0][len(h):len(h) + 60]))
    out = {}
    for s in by_points.get(hp, ()):
        out[s] = [W_POINTS_BDB if s in bdb else W_POINTS, 'points']
    for s in by_letters.get(hl, ()):
        if s not in out and any(same_sh(h, w) for w in targets[s]['forms']):
            out[s] = [W_LETTERS_BDB if s in bdb else W_LETTERS, 'letters']
    # BDB knows spellings Strong's does not use (Abner is אֲבִינֵר in Strong's,
    # אַבְנֵר in Gesenius and BDB): a pointed BDB match proposes its number too.
    for s in bdb_p.get(hp, ()):
        if s not in out and s in targets:
            out[s] = [W_LETTERS_BDB, 'bdb']
    # Words spelled alike (the noun אִישׁ "man" and the verb אִישׁ) are told
    # apart by language and by how much English the two definitions share.
    words = english(text)
    for s, c in out.items():
        c[0] += 0.5 if targets[s]['aramaic'] == chaldee else -0.5
        c[0] += overlap(words, targets[s]['english'])
    return out, bdb


def chain(pairs, size):
    """Best-weighted set of pairings increasing in both sequences."""
    pairs.sort(key=lambda p: (p[0], -p[1]))
    tree = [(0.0, -1)] * (size + 2)

    def query(j):
        best, k = (0.0, -1), j
        while k > 0:
            best = max(best, tree[k])
            k -= k & -k
        return best

    def update(j, val):
        k = j + 1
        while k <= size + 1:
            tree[k] = max(tree[k], val)
            k += k & -k

    back = []
    for idx, (i, j, w) in enumerate(pairs):
        prev_best, prev_idx = query(j)
        back.append(prev_idx)
        update(j, (prev_best + w, idx))
    _, idx = query(size + 1)
    picked = []
    while idx != -1:
        picked.append(pairs[idx])
        idx = back[idx]
    return picked[::-1]


STOP = set('''which with from that this they them their have been were also used
when then than into only some such very more most other same what where whose
there these those upon being after before under over word words often sense
place thing things comp compare root arab chald syr'''.split())


def english(text):
    return {w for w in re.findall(r'[a-z]{4,}', text.lower()) if w not in STOP}


def overlap(a, b):
    return round(len(a & b) / max(1, min(len(a), len(b))), 3)


# ---------------------------------------------------------------- main
def main():
    lines, dropped = read_lines()
    records, owner = cut(lines)

    # Guard: every line is in exactly one record, apart from the repeated
    # letter headings and the title on page I.
    used = [k for r in records for k in r['lines']]
    if len(used) != len(set(used)):
        sys.exit('refused: a transcript line landed in two records')
    skipped = [lines[k]['text'] for k, o in enumerate(owner) if o is None]
    if any(not (is_letter(t) or t == 'LEXICON.') for t in skipped):
        sys.exit(f'refused: lines in no record: {[t for t in skipped if not is_letter(t)][:5]}')

    targets = load_targets()
    for t in targets.values():
        t['english'] = english(t['gloss'] + ' ' + t['defn'])
    by_points, by_letters = {}, {}
    for s, t in targets.items():
        for w in t['forms']:
            by_points.setdefault(w, set()).add(s)
            by_letters.setdefault(bare(w), set()).add(s)
    bdb_p, bdb_l = load_bdb()

    cand = {}
    for i, r in enumerate(records):
        if r['kind'] == 'entry':
            cand[i] = candidates(r, join(lines, r['lines']), targets,
                                 by_points, by_letters, bdb_p, bdb_l)
    # A number some entry matches in full, points and all, is not open to
    # entries that only share its letters: a root and its noun are often
    # spelled alike, and the noun is the one Strong's numbered.
    claimed = {s for c, _ in cand.values() for s, (_, how) in c.items() if how == 'points'}
    pairs = []
    for i, (c, _) in cand.items():
        for s, (w, how) in list(c.items()):
            if how == 'letters' and s in claimed:
                del c[s]
            else:
                pairs.append((i, int(s[1:]), w))
    # Chain in Gesenius's order, not Strong's: Gesenius puts every word that
    # begins with שׂ before those that begin with שׁ; Strong's mixes them.
    order = sorted(targets, key=lambda s: gesenius_order(s, targets[s]))
    rank = {s: k + 1 for k, s in enumerate(order)}
    pairs = [(i, rank['H%04d' % j], w) for i, j, w in pairs]
    picked = {i: order[j - 1] for i, j, _ in chain(pairs, len(order))}

    # An entry the ordered chain left out keeps a pointed match only when
    # it is the sole one and no other entry holds that number; it is marked
    # for checking, as it sits out of order.
    taken = set(picked.values())
    for i, (c, bdb) in cand.items():
        if i not in picked:
            exact = [s for s, (_, how) in c.items() if how == 'points' and s not in taken]
            if len(exact) == 1:
                picked[i] = exact[0]
                taken.add(exact[0])
                c[exact[0]][1] = 'out of order'

    entries = []
    for i, r in enumerate(records):
        text = join(lines, r['lines'])
        s = picked.get(i)
        t = targets.get(s, {})
        c, bdb = cand.get(i, ({}, set()))
        how = c[s][1] if s else None
        if s and s in bdb and how != 'bdb':
            how += '+bdb'
        shared = overlap(english(text), t['english']) if s else None
        # Doubtful: BDB maps the word elsewhere, or the only evidence is a
        # match out of order or by letters alone that BDB does not back.
        check = bool(s) and (
            (bool(bdb) and s not in bdb)
            or how in ('out of order', 'letters')
            or (how == 'bdb' and shared == 0))
        entries.append({
            'kind': r['kind'], 'headword': r['headword'], 'homonym': r['homonym'],
            'strongs': s, 'estrong': t.get('estrong'), 'lemma': t.get('lemma'),
            'page': label(r['image']), 'image': r['image'], 'url': SCAN.format(r['image']),
            'found_by': how, 'english_overlap': shared, 'check': check,
            'unsure': text.count('[?]'), 'text': text})

    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding='utf-8')

    keyed = [e for e in entries if e['strongs']]
    ways = {}
    for e in keyed:
        ways[e['found_by']] = ways.get(e['found_by'], 0) + 1
    have = {e['strongs'] for e in keyed}
    flagged = [e for e in keyed if e['check']]
    report = [
        f"transcript lines read: {len(lines)} (plus {dropped} running heads and column markers left out)",
        f"records: {len(entries)} ({sum(e['kind'] == 'letter' for e in entries)} letter headings)",
        f"entries with a Strong's number: {len(keyed)}",
        '  found by: ' + ', '.join(f'{k} {v}' for k, v in sorted(ways.items(), key=lambda kv: -kv[1])),
        f"entries with no Strong's number: {sum(e['kind'] == 'entry' and not e['strongs'] for e in entries)}",
        f"Strong's numbers (H0001-H{LAST_STRONGS}) with a Gesenius entry: {len(have)} of {len(targets)}",
        f"entries holding [?] marks: {sum(e['unsure'] > 0 for e in entries)}",
        f"flagged check=true: {len(flagged)}",
        '',
        "Flagged pairings, check by eye (page, headword, Strong's, lemma, found by, text):",
    ]
    report += [f"  {e['page']}\t{e['headword']}\t{e['strongs']}\t{e['lemma']}\t{e['found_by']}\t"
               f"{e['text'][:70].replace(chr(10), ' ')}" for e in flagged]
    REPORT.write_text('\n'.join(report) + '\n', encoding='utf-8')
    print('\n'.join(report[:8]))


if __name__ == '__main__':
    sys.exit(main())
