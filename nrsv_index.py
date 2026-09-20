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
"""
import re, json, sys
from bisect import bisect_left

SRC = 'nrsv.txt'
OUT = 'verses.json'

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

print(f'chapter markers : {len(marks)}')
print(f'verses indexed  : {len(index)}')
print(f'thin chapters   : {len(thin)}')
print(f'gappy chapters  : {len(gappy)}')
for t in sorted(thin)[:20]:
    print('   thin ', t)
for g in sorted(gappy)[:20]:
    print('   gappy', g)
