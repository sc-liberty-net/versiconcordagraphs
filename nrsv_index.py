"""
nrsv_index.py - build a chapter/verse index over the extracted NRSV text.

Two fixes over the first version:

1. Chapter markers are found ANYWHERE, not only on their own line. The
   extractor sometimes runs a marker into the previous verse, e.g.
   "...went home, [John 8] 1 while Jesus went to the Mount of Olives."
   The old line-anchored regex silently dropped those chapters.

2. Verse numbers are chosen by longest-increasing-subsequence rather than
   by a greedy "must equal last+1" rule. The greedy rule broke at every
   verse the NRSV omits from the running text (Matt 17:21, Luke 23:17,
   John 5:4, Acts 24:7 ...), truncating the rest of the chapter. LIS
   tolerates the gap and keeps going.

Third fix, added after a silent regression: COUNT, THEN RECONCILE.

Careful reading of an extraction cannot find what the extraction dropped —
the dropped material is not there to be read. Only a count checked against an
independent expectation can. On 2026-09-20 a rebuild produced 37,465 verses
where an earlier build of the same PDF had produced 37,542, with 72 chapters
each missing a single interior verse. Nothing failed. Every query inside the
range the index kept answered with undiminished confidence, and the loss was
found only because an outside record of the earlier figure happened to exist.

So this script now keeps its own record. It writes index-baseline.json (counts
only, no scripture, safe to commit), and on every later run it reconciles
against it and exits non-zero if the totals have moved. The density check
below cannot do this job: a chapter missing one verse of twenty-eight sits at
96% and never trips it.

    python3 nrsv_index.py              build, then reconcile against baseline
    python3 nrsv_index.py --record     build, then RECORD this run as baseline
"""
import re, json, sys, os, argparse
from bisect import bisect_left

ap = argparse.ArgumentParser()
ap.add_argument('--record', action='store_true',
                help='write this run\'s counts as the baseline to reconcile against')
ap.add_argument('--baseline', default='index-baseline.json')
ap.add_argument('--src', default='nrsv.txt')
ap.add_argument('--out', default='verses.json')
a = ap.parse_args()

SRC = a.src
OUT = a.out

txt = open(SRC, encoding='utf-8', errors='replace').read()

# --- chapter markers, found anywhere in the stream -------------------------
CHAP = re.compile(r'\[((?:[1-4] )?[A-Z][A-Za-z]+(?: of [A-Z][a-z]+)?(?: [A-Z][a-z]+)?) (\d{1,3})\]')

marks = [(m.start(), m.end(), m.group(1).strip(), int(m.group(2)))
         for m in CHAP.finditer(txt)]

# --- noise the extractor leaves behind -------------------------------------
RUNHEAD = re.compile(r'^\x0c?[A-Z0-9 ,\.\'\-]{2,40} \d{1,4}\s*$', re.M)
PAGENUM = re.compile(r'^\s*\d{1,4}\s*$', re.M)

# The last chapter of a book runs into the NEXT book's front matter, which is
# full of stray numerals and inflated the verse ceiling. Cut at that seam.
BOOKINTRO = re.compile(
    r'(?:\b[A-Z][A-Z\'\- ]{2,30}\s+Introduction\b'
    r'|\bINTRODUCTION TO\b'
    r'|\bThe Minor Prophets\b'
    r'|\bCopyright \u00a9)')

def clean(body):
    cut = BOOKINTRO.search(body)
    if cut:
        body = body[:cut.start()]
    body = RUNHEAD.sub(' ', body)
    body = PAGENUM.sub(' ', body)
    body = body.replace('\x0c', ' ')
    return re.sub(r'\s+', ' ', body).strip()

# --- verse splitting -------------------------------------------------------
# A candidate is a standalone 1-3 digit integer followed by whitespace and a
# letter or quote. Excludes things like "2,000" and "1 Kings".
CAND = re.compile(r'(?<![\d\w,.\-])(\d{1,3})(?=\s+["\u201c\u2018\']?[A-Za-z])')

def lis(nums):
    """Indices of a longest strictly-increasing subsequence."""
    if not nums:
        return []
    tails, tails_idx, prev = [], [], [-1] * len(nums)
    for i, n in enumerate(nums):
        j = bisect_left(tails, n)
        if j == len(tails):
            tails.append(n); tails_idx.append(i)
        else:
            tails[j] = n; tails_idx[j] = i
        prev[i] = tails_idx[j - 1] if j else -1
    out, k = [], tails_idx[-1]
    while k != -1:
        out.append(k); k = prev[k]
    return out[::-1]

def split_verses(body, max_verse=180):
    toks = [(int(m.group(1)), m.start(), m.end())
            for m in CAND.finditer(body) if int(m.group(1)) <= max_verse]
    if not toks:
        return {}
    keep = lis([t[0] for t in toks])
    picks = [toks[i] for i in keep]
    # Drop a leading run that starts absurdly high (stray numeral before v1)
    while picks and picks[0][0] > 3 and len(picks) > 1:
        break
    out = {}
    for j, (n, s, e) in enumerate(picks):
        stop = picks[j + 1][1] if j + 1 < len(picks) else len(body)
        out[n] = body[e:stop].strip()
    return out

index, chapters = [], []
for i, (s, e, book, ch) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
    body = clean(txt[e:end])
    chapters.append((book, ch, body))
    for v, text in split_verses(body).items():
        index.append({'ref': f'{book} {ch}:{v}', 'book': book,
                      'ch': ch, 'v': v, 'text': text})

json.dump(index, open(OUT, 'w'))
json.dump([{'book': b, 'ch': c, 'body': t} for b, c, t in chapters],
          open('chapters.json', 'w'))

# --- self-check ------------------------------------------------------------
from collections import defaultdict
per = defaultdict(list)
for x in index:
    per[(x['book'], x['ch'])].append(x['v'])

thin = [(b, c, max(v)) for (b, c), v in per.items() if max(v) < 8]
gappy = [(b, c, len(v), max(v)) for (b, c), v in per.items()
         if max(v) >= 8 and len(v) / max(v) < 0.9]

# Isolated interior holes: a verse number absent between two verses that ARE
# present. Classified by the size of each gap rather than by chapter density,
# because the two failures look nothing alike. A gap of one or two is a
# dropped verse — the extractor glued its number onto the previous verse. A
# long run is the known tail artifact, where a stray numeral in the next
# book's front matter inflates the ceiling and invents verses that were never
# claimed. Only the first kind is a loss.
holes, runs = [], []
for (b, c), vs in per.items():
    s = sorted(vs)
    for lo, hi in zip(s, s[1:]):
        missing = list(range(lo + 1, hi))
        if not missing:
            continue
        (holes if len(missing) <= 2 else runs).append((b, c, missing))

hole_count = sum(len(m) for _, _, m in holes)

per_book = defaultdict(int)
for x in index:
    per_book[x['book']] += 1

now = {'markers': len(marks), 'verses': len(index),
       'isolated_holes': hole_count, 'books': dict(sorted(per_book.items()))}

print(f'chapter markers : {len(marks)}')
print(f'verses indexed  : {len(index)}')
print(f'thin chapters   : {len(thin)}')
print(f'gappy chapters  : {len(gappy)}')
print(f'isolated holes  : {hole_count} verse(s) in {len(holes)} place(s)')
print(f'tail runs       : {len(runs)} (ceiling artifacts, not losses)')
for t in sorted(thin)[:20]:
    print('   thin ', t)
for g in sorted(gappy)[:20]:
    print('   gappy', g)
for b, c, m in sorted(holes)[:20]:
    print(f'   hole  {b} {c}:{",".join(map(str, m))}')
if len(holes) > 20:
    print(f'   ... and {len(holes) - 20} more holes')

# --- count, then reconcile -------------------------------------------------
if a.record:
    json.dump(now, open(a.baseline, 'w'), indent=1)
    print(f'\nrecorded {a.baseline}: {now["verses"]} verses, '
          f'{now["markers"]} markers, {now["isolated_holes"]} isolated holes.')
    print('Every later run reconciles against this and fails if the totals move.')
    sys.exit(0)

if not os.path.exists(a.baseline):
    print(f'\nNo {a.baseline} to reconcile against, so this run proves nothing '
          f'about what the extraction dropped.')
    print(f'If these numbers are right, record them:  python3 nrsv_index.py --record')
    sys.exit(0)

was = json.load(open(a.baseline, encoding='utf-8'))
drift = []
for k in ('markers', 'verses', 'isolated_holes'):
    if was.get(k) != now[k]:
        drift.append(f'{k}: {was.get(k)} -> {now[k]}  ({now[k] - was.get(k, 0):+d})')
moved = {b: (was['books'].get(b, 0), n) for b, n in now['books'].items()
         if was['books'].get(b, 0) != n}
for b in was['books']:
    if b not in now['books']:
        moved[b] = (was['books'][b], 0)

if not drift and not moved:
    print(f'\nreconciled against {a.baseline}: no drift.')
    sys.exit(0)

print(f'\nDRIFT against {a.baseline} — the extraction is not what it was.', file=sys.stderr)
for d in drift:
    print('  ', d, file=sys.stderr)
for b, (o, n) in sorted(moved.items()):
    print(f'   {b}: {o} -> {n}  ({n - o:+d})', file=sys.stderr)
print('\nThe index was still written. Decide which build is right before trusting it:',
      file=sys.stderr)
print('  a lower count means verses were dropped and every query inside the range',
      file=sys.stderr)
print('  it kept will still answer confidently. If this build is the correct one,',
      file=sys.stderr)
print('  re-record with:  python3 nrsv_index.py --record', file=sys.stderr)
sys.exit(1)
