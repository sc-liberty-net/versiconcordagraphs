"""Parse the machine-read text of Thayer's lexicon (1889) into entries keyed
to Strong's numbers.

Input:  lexicons/thayer/thayer-1889_djvu.txt  (archive.org OCR, public domain)
        stepbible/TBESG ... .txt               (Strong's numbers + Greek lemmas, CC BY)
Output: lexicons/thayer/thayer-entries.json
        lexicons/thayer/thayer-report.txt

The OCR read Thayer's Greek as Latin letters (ἐνισχύω came out "év-toxvw"),
so headwords cannot be looked up directly. Both Thayer's and Strong's run in
Greek alphabetical order, so the parser scores every plausible pairing by
letter shape and then keeps the best-scoring set of pairings that stays in
order on both sides. Order does most of the work; shape breaks ties.

A candidate entry that wins no pairing is not an entry: it is folded into
the entry before it. Every kept pairing carries its score so weak ones can
be checked by eye.
"""
import bisect
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).parent
OCR = HERE / 'lexicons/thayer/thayer-1889_djvu.txt'
TBESG = next((HERE / 'stepbible').glob('TBESG*.txt'))
OUT = HERE / 'lexicons/thayer/thayer-entries.json'
REPORT = HERE / 'lexicons/thayer/thayer-report.txt'

BODY_START = 'A, a, '        # first line of the lexicon proper
BODY_END = 'APPENDIX, '      # first line after it
BAND = 0.08                  # how far (as a fraction) positions may drift
MIN_SCORE = 0.55             # weakest pairing considered at all
WINDOW = 80                  # second pass: Strong's rows either side of the expected spot
GAP_SCORE = 0.75             # gap-fill: weakest reading accepted between neighbours

# Letter-shape classes. The OCR confuses some Greek letters with the same
# Latin ones, so each class holds what the eye (and the OCR) cannot tell
# apart. Coarse on purpose: order, not shape, carries the matching.
GREEK_CLASS = {
    'α': 'A', 'β': 'B', 'γ': 'V', 'δ': 'A', 'ε': 'E', 'ζ': 'F', 'η': 'N',
    'θ': 'O', 'ι': 'I', 'κ': 'K', 'λ': 'A', 'μ': 'P', 'ν': 'V', 'ξ': 'E',
    'ο': 'O', 'π': 'P', 'ρ': 'P', 'σ': 'O', 'ς': 'S', 'τ': 'I', 'υ': 'V',
    'φ': 'P', 'χ': 'K', 'ψ': 'V', 'ω': 'W',
}
LATIN_CLASS = {
    'a': 'A', 'd': 'A', '@': 'A', 'g': 'A', '5': 'A',
    'b': 'B', '8': 'B', 'ß': 'B',
    'v': 'V', 'u': 'V', 'y': 'V',
    'e': 'E', 'c': 'E', '€': 'E', '£': 'E',
    'f': 'F', '¢': 'F',
    'n': 'N', '7': 'N', 'h': 'N',
    'o': 'O', '6': 'O', '0': 'O', 'q': 'O',
    'i': 'I', 'l': 'I', 't': 'I', 'r': 'I', '1': 'I', '!': 'I', 'j': 'I',
    'k': 'K', 'x': 'K',
    'p': 'P', 'm': 'P', 'z': 'P',
    's': 'S',
    'w': 'W',
}


# What each Greek letter was read as, gathered from pairings the English
# confirms. Used for the final score, where a Greek letter read as any of
# its usual stand-ins costs nothing.
READ_AS = {
    'α': 'adg&@o', 'β': 'b8ß', 'γ': 'yv', 'δ': 'ds5b6', 'ε': 'e€¢c',
    'ζ': 'lfz¢', 'η': 'nyif7hq', 'θ': '0ob6s®', 'ι': 'iltruv1!', 'κ': 'kx',
    'λ': 'axhrtld', 'μ': 'pum', 'ν': 'vui', 'ξ': 'ek£', 'ο': 'oed60',
    'π': 'mzrt', 'ρ': 'ph', 'σ': 'ocsez', 'ς': 's', 'τ': 'tr',
    'υ': 'vudiy', 'φ': 'dp', 'χ': 'xy', 'ψ': 'ypw', 'ω': 'wadoe',
}
OCR_KEEP = set(''.join(READ_AS.values()))


def strip_marks(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if not unicodedata.combining(c))


def greek_shape(lemma):
    s = strip_marks(lemma.lower())
    return ''.join(GREEK_CLASS.get(c, '') for c in s)


def latin_shape(word):
    s = strip_marks(word.lower())
    return ''.join(LATIN_CLASS.get(c, '') for c in s)


def greek_letters(lemma):
    return ''.join(c for c in strip_marks(lemma.lower()) if c in READ_AS)


def ocr_letters(word):
    return ''.join(c for c in strip_marks(word.lower()) if c in OCR_KEEP)


def read_score(greek, ocr):
    """1 - edit distance / length, where a usual misreading is free."""
    if not greek or not ocr:
        return 0.0
    prev = list(range(len(ocr) + 1))
    for i, g in enumerate(greek, 1):
        ok = READ_AS[g]
        cur = [i] + [0] * len(ocr)
        for j, o in enumerate(ocr, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1,
                         prev[j - 1] + (0 if o in ok else 1))
        prev = cur
    return 1 - prev[-1] / max(len(greek), len(ocr))


def load_targets():
    """Strong's rows from TBESG, in Strong's order, numbers G0001-G5624."""
    rows, seen = [], set()
    for line in TBESG.read_text(encoding='utf-8-sig').splitlines():
        f = line.split('\t')
        if len(f) < 8 or not re.fullmatch(r'G\d{4}', f[0]):
            continue
        if int(f[0][1:]) > 5624:
            continue
        estrong = f[1].split()[0]
        lemma = f[3].split(',')[-1].strip()  # "α, Ἀλφα" -> "Ἀλφα"
        key = (f[0], lemma)
        if key in seen:
            continue
        seen.add(key)
        rows.append({'strongs': f[0], 'estrong': estrong, 'lemma': lemma,
                     'translit': f[4], 'gloss': f[6], 'defn': f[7],
                     'shape': greek_shape(lemma),
                     'letters': greek_letters(lemma)})
    return rows


HEAD = re.compile(r'''^[*"'‘’`“”\[]*([^\s,;:.(\[]{1,30}(?:-[^\s,;:.(\[]{1,20})?)(?:,|;|:| \[| \()''')


def load_candidates():
    lines = OCR.read_text(encoding='utf-8').splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith(BODY_START))
    end = next(i for i, l in enumerate(lines) if l.startswith(BODY_END))
    body = lines[start:end]
    cands, cur = [], None
    for n, line in enumerate(body):
        # An entry starts after a blank line, or straight after the line
        # that ends the one before it: Thayer closes most entries with *,
        # the rest with a reference ("vi. 4." or "26)."). A line ending in
        # an abbreviation ("cf.") does not close an entry.
        prev = body[n - 1].rstrip() if n else ''
        opens = not prev or prev.endswith('*') or re.search(r'[\d)\]]\.$', prev)
        m = HEAD.match(line) if opens and len(line.strip()) > 12 else None
        if m and len(re.findall(r'[^\W\d_]|[@&€¢]', m.group(1))) >= 2:
            cur = {'line': start + n + 1, 'head': m.group(1), 'lines': [line]}
            cands.append(cur)
        elif cur:
            cur['lines'].append(line)
    for c in cands:
        c['shape'] = latin_shape(c['head'])
        c['letters'] = ocr_letters(c['head'])
    return cands, body, start


# The opening words of a real entry: gender article, genitive ending,
# verb parts, "indecl.", a cross-reference. A candidate Strong's has no
# number for is kept as its own entry only if it opens like this.
ENTRY_OPENING = re.compile(
    r'-[a-z@]{1,4}[,;]| [67]\b| 76\b| 7[dé]\b| r[dé]\b| 1d\b|indecl|\bsee\b|'
    r'fut\.|aor\.|\badv\b|prop\. name|depon|pres\.|\bpass\.|\bmid\.')


def score(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def align(cands, targets):
    """Two passes. The first shortlists by coarse shape over a wide band and
    finds confident pairings; those fix where each candidate should sit in
    Strong's order, and the second pass scores every Strong's number within
    a narrow window of that spot."""
    nc, nt = len(cands), len(targets)
    pairs = []
    for i, c in enumerate(cands):
        lo = max(0, int((i / nc - BAND) * nt))
        hi = min(nt, int((i / nc + BAND) * nt) + 1)
        near = sorted(((score(c['shape'], targets[j]['shape']), j)
                       for j in range(lo, hi)), reverse=True)[:40]
        for _, j in near:
            s = read_score(targets[j]['letters'], c['letters'])
            if s >= MIN_SCORE:
                pairs.append((i, j, s))
    first = chain(pairs, nt)

    anchors = [(i, j) for i, j, s in first if s >= 0.85]
    ai = [a[0] for a in anchors]
    pairs = []
    for i, c in enumerate(cands):
        k = bisect.bisect_left(ai, i)
        (i0, j0) = anchors[max(0, k - 1)]
        (i1, j1) = anchors[min(len(anchors) - 1, k)]
        expect = j0 if i1 == i0 else j0 + (j1 - j0) * (i - i0) / (i1 - i0)
        lo = max(0, int(expect) - WINDOW)
        hi = min(nt, int(expect) + WINDOW + 1)
        for j in range(lo, hi):
            s = read_score(targets[j]['letters'], c['letters'])
            if s >= MIN_SCORE:
                pairs.append((i, j, s))
    return chain(pairs, nt)


def chain(pairs, nt):
    """Best-scoring set of pairings increasing in both sequences."""
    # Weighted longest increasing chain: process by i, and within one i by
    # descending j so two pairs from the same candidate cannot chain.
    pairs.sort(key=lambda p: (p[0], -p[1]))
    size = nt + 1
    tree = [(0.0, -1)] * (size + 1)          # Fenwick tree of (best, pair)

    def query(j):                              # best chain ending before j
        best, k = (0.0, -1), j
        while k > 0:
            best = max(best, tree[k])
            k -= k & -k
        return best

    def update(j, val):
        k = j + 1
        while k <= size:
            tree[k] = max(tree[k], val)
            k += k & -k

    back = []
    for idx, (i, j, s) in enumerate(pairs):
        prev_best, prev_idx = query(j)
        # Weight rewards strong shape matches far more than weak ones.
        total = prev_best + (s - MIN_SCORE + 0.05) ** 2
        back.append(prev_idx)
        update(j, (total, idx))
    best_total, idx = query(size)
    picked = []
    while idx != -1:
        picked.append(pairs[idx])
        idx = back[idx]
    return picked[::-1]


def clean(lines):
    text = '\n'.join(lines)
    text = re.sub(r'-\n(?=[a-z])', '', text)      # rejoin hyphenated words
    text = re.sub(r'\s*\n\s*', ' ', text)
    return re.sub(r' {2,}', ' ', text).strip()


STOP = set('''which with from that this they them their have been were also used
when then than into only some such very more most other same what where
whose there these those upon being after before under over word words
often note sense place thing things'''.split())


def english(text):
    return {w for w in re.findall(r'[a-z]{4,}', text.lower()) if w not in STOP}


# Looser than HEAD, for the gap-fill pass only: the headword may be split by
# a stray space, and may be followed by "and", "or", an edition siglum or a
# genitive ending instead of punctuation.
GAP_HEAD = re.compile(
    r'''^[*"'‘’`“”\[]*(\S{2,30}?)(?: (\S{1,12}?))?'''
    r'''(?:[,;:]| \[| \(| and | or | -\S{1,4}[,;]| RG| T | L | WH)''')


def gap_fill(pairing, cands, targets, body, start):
    """For each Strong's number still without an entry, look only between
    the entries of its paired neighbours for a line whose opening word (or
    first two words, when a stray space split the headword) reads as it."""
    have = {j: cands[i]['line'] for i, j, s in pairing}
    js = sorted(have)
    taken = set(have.values())
    found = []
    for j in range(len(targets)):
        if j in have:
            continue
        k = bisect.bisect_left(js, j)
        if k == 0 or k == len(js):
            continue
        lo = max(have[js[k - 1]], max((l for l, jj, *_ in found if jj < j), default=0))
        hi = have[js[k]]
        best = (0.0, None, None)
        for line_no in range(lo + 1, hi):
            n = line_no - start - 1
            prev = body[n - 1].rstrip()
            opens = not prev or prev.endswith('*') or re.search(r'[\d)\]]\.$', prev)
            if not opens or line_no in taken or len(body[n].strip()) <= 12:
                continue
            m = GAP_HEAD.match(body[n])
            if not m:
                continue
            # A second word before the punctuation means the headword was
            # split; score only the rejoined form, or half of it can pass
            # for a shorter word ("mpeo Pela" is πρεσβεία, not πρέπω).
            second = m.group(2) if m.group(2) not in (None, 'and', 'or') else ''
            head = m.group(1) + second
            s = read_score(targets[j]['letters'], ocr_letters(head))
            if s > best[0]:
                best = (s, line_no, head)
        if best[0] >= GAP_SCORE:
            found.append((best[1], j, best[0], best[2]))
            taken.add(best[1])
    return found


def main():
    targets = load_targets()
    cands, body, start = load_candidates()
    pairing = align(cands, targets)
    matched = {i: (j, s) for i, j, s in pairing}

    # Where each entry starts: paired candidates, gap-fill finds, and
    # unpaired candidates that open like an entry (Thayer has words Strong's
    # lacks; those are kept with no number). Other unpaired candidates are
    # false starts and stay inside the entry before them.
    starts = []
    for i, c in enumerate(cands):
        if i in matched:
            j, s = matched[i]
            starts.append((c['line'], j, s, c['head'], 'order'))
        elif ENTRY_OPENING.search(c['lines'][0][len(c['head']):][:40]):
            starts.append((c['line'], None, None, c['head'], None))
    gaps = gap_fill(pairing, cands, targets, body, start)
    starts += [(l, j, s, h, 'gap') for l, j, s, h in gaps]
    starts.sort(key=lambda st: (st[0], st[1] is None))
    # A gap find may land on a line already kept as an unnumbered entry.
    dedup = {}
    for st in starts:
        if st[0] not in dedup or st[1] is not None:
            dedup[st[0]] = st
    starts = sorted(dedup.values(), key=lambda st: st[0])

    entries = []
    end_line = start + len(body)
    for k, (line_no, j, s, head, how) in enumerate(starts):
        nxt = starts[k + 1][0] if k + 1 < len(starts) else end_line + 1
        t = targets[j] if j is not None else {}
        entries.append({
            'strongs': t.get('strongs'), 'estrong': t.get('estrong'),
            'lemma': t.get('lemma'), 'translit': t.get('translit'),
            'ocr_headword': head, 'score': round(s, 3) if s else None,
            'found_by': how, 'ocr_line': line_no,
            'lines': body[line_no - start - 1:nxt - start - 1]})

    # Check: the English of a paired Thayer entry should share words with
    # STEPBible's own definition far more often than a random pairing does.
    by_e = {t['estrong']: t for t in targets}
    for e in entries:
        e['text'] = clean(e.pop('lines'))
        e['english_overlap'] = None
    keyed = [e for e in entries if e['strongs']]
    for e in keyed:
        t = by_e[e['estrong']]
        a, b = english(e['text']), english(t['gloss'] + ' ' + t['defn'])
        e['english_overlap'] = round(len(a & b) / max(1, min(len(a), len(b))), 3)
    base = []
    for k, e in enumerate(keyed):
        a = english(keyed[(k + 37) % len(keyed)]['text'])
        b = english(by_e[e['estrong']]['gloss'] + ' ' + by_e[e['estrong']]['defn'])
        base.append(len(a & b) / max(1, min(len(a), len(b))))

    # Flag pairings neither check supports. Spot checks found most of these
    # correct (STEPBible words the definition differently), but this is
    # where the wrong ones are: usually a word Strong's lacks that took a
    # neighbour's number. Short cross-references ("see ...") have no
    # English to compare, so they are only flagged on a weak score.
    for e in entries:
        e['check'] = bool(e['strongs']) and (
            e['score'] < 0.7 or (e['english_overlap'] == 0 and len(e['text']) >= 80))

    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding='utf-8')

    ov = sorted(e['english_overlap'] for e in keyed)
    sc = [e['score'] for e in keyed]
    have = {e['strongs'] for e in keyed}
    all_nums = {t['strongs'] for t in targets}
    flagged = [e for e in keyed if e['check']]
    lines = [
        f"candidate entries found in OCR: {len(cands)}",
        f"entries paired to a Strong's number: {len(keyed)}",
        f"  of which found by the gap-fill pass: {sum(e['found_by'] == 'gap' for e in keyed)}",
        f"entries kept with no Strong's number: {len(entries) - len(keyed)}",
        f"Strong's numbers (G0001-G5624) with a Thayer entry: {len(have)} of {len(all_nums)}",
        f"shape score: median {sorted(sc)[len(sc)//2]:.2f}, under 0.7: {sum(s < 0.7 for s in sc)}",
        f"English overlap with STEPBible definition: median {ov[len(ov)//2]:.2f}"
        f" (random pairing median {sorted(base)[len(base)//2]:.2f})",
        f"flagged check=true (score < 0.7, or no shared English): {len(flagged)}",
        '',
        "Flagged pairings, check by eye (line, OCR headword, Strong's, lemma, text):",
    ]
    lines += [f"  {e['ocr_line']}\t{e['ocr_headword']}\t{e['strongs']}\t{e['lemma']}\t{e['text'][:70]}"
              for e in flagged]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[:8]))


if __name__ == '__main__':
    sys.exit(main())
