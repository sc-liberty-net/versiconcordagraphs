"""build_lemmas.py - turn the STEPBible tagged text into a lemma index.

Reads the six TAHOT/TAGNT files in lemma-data/ and writes strongs_index.json:

    {"Matthew 6:19": ["G2343", "G2344", ...], ...}

plus a gloss table so a Strong's number can be named without opening the
source files again.

WHY THIS EXISTS. An edge tagged `lex` claims two passages share wording. On an
English index that claim is really about the translators' word choice, not
about Hebrew or Greek - "treasure" in two verses may render two unrelated
words, and a word shared in one translation can vanish in another. Keyed on a
Strong's number instead, "shared wording" becomes a checkable fact about the
source language, and a lex edge can carry `states` honestly.

SOURCE. github.com/STEPBible/STEPBible-Data, CC BY 4.0, Tyndale House
Cambridge. Their reference column states: "Versification as used by NRSV" -
which is why it lines up with verses.json. Fetch it with fetch_lemmas.py.
The data is gitignored: STEPBible ask that it be taken from their repository
rather than redistributed.

COVERAGE. The source is the Hebrew OT and Greek NT - 66 books. The
deuterocanonical books in verses.json have no lemma data and never will from
this source. build_lemmas.py prints exactly what it could not cover; read it.

    python build_lemmas.py
"""
import os, re, sys, json, glob, collections

DATA = 'lemma-data'
OUT = 'strongs_index.json'

# STEPBible book code -> the book name as verses.json spells it.
# Two names appear twice on purpose: the index splits Psalms and Galatians
# across two spellings (see the note build_lemmas.py prints).
BOOKS = {
    'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers',
    'Deu': 'Deuteronomy', 'Jos': 'Joshua', 'Jdg': 'Judges', 'Rut': 'Ruth',
    '1Sa': '1 Samuel', '2Sa': '2 Samuel', '1Ki': '1 Kings', '2Ki': '2 Kings',
    '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra',
    'Neh': 'Nehemiah', 'Est': 'Esther', 'Job': 'Job', 'Psa': 'Psalm',
    'Pro': 'Proverbs', 'Ecc': 'Ecclesiastes', 'Sng': 'Song of Solomon',
    'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'Lam': 'Lamentations',
    'Ezk': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea', 'Jol': 'Joel',
    'Amo': 'Amos', 'Oba': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah',
    'Nam': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah', 'Hag': 'Haggai',
    'Zec': 'Zechariah', 'Mal': 'Malachi',
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Corinthians',
    '2Co': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
    'Php': 'Philippians', 'Col': 'Colossians', '1Th': '1 Thessalonians',
    '2Th': '2 Thessalonians', '1Ti': '1 Timothy', '2Ti': '2 Timothy',
    'Tit': 'Titus', 'Phm': 'Philemon', 'Heb': 'Hebrews', 'Jas': 'James',
    '1Pe': '1 Peter', '2Pe': '2 Peter', '1Jn': '1 John', '2Jn': '2 John',
    '3Jn': '3 John', 'Jud': 'Jude', 'Rev': 'Revelation',
}

ROW = re.compile(r'^([1-9A-Za-z]{2,4})\.(\d+)\.(\d+)')
STRONG = re.compile(r'[GH]\d{1,5}[A-Za-z]?')

files = sorted(glob.glob(os.path.join(DATA, '*.txt')))
if not files:
    sys.exit('no files in %s/ - run fetch_lemmas.py first.' % DATA)

index = collections.defaultdict(list)
gloss = {}
rows = skipped_book = 0
unknown_books = collections.Counter()

for path in files:
    greek = 'TAGNT' in os.path.basename(path)
    # Strong's sits in a different column in the two formats.
    col_strong, col_gloss = (3, 4) if greek else (4, 12)
    col_english = 2 if greek else 3
    for line in open(path, encoding='utf-8-sig', errors='replace'):
        if not line or line[0] in '#\t\n':
            continue
        col = line.rstrip('\n').split('\t')
        if len(col) <= col_strong:
            continue
        m = ROW.match(col[0])
        if not m:
            continue
        code, ch, vs = m.group(1), m.group(2), m.group(3)
        book = BOOKS.get(code)
        if not book:
            unknown_books[code] += 1
            skipped_book += 1
            continue
        rows += 1
        ref = '%s %s:%s' % (book, ch, vs)
        found = STRONG.findall(col[col_strong])
        if not found:
            continue
        index[ref].extend(found)
        if len(col) > col_gloss and col[col_gloss].strip():
            # "<hebrew>=to create" or "{H1254A=<hebrew>=to create}"
            for num in found:
                if num in gloss:
                    continue
                parts = col[col_gloss].strip().strip('{}').split('=')
                if len(parts) >= 2:
                    g = parts[-1].split(';')[0].split('»')[0].strip()
                    if g and len(g) < 60:
                        gloss[num] = g
        elif len(col) > col_english and col[col_english].strip():
            for num in found:
                gloss.setdefault(num, col[col_english].strip()[:60])

# De-duplicate per verse but keep order of first appearance.
clean = {}
for ref, nums in index.items():
    seen, out = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n)
            out.append(n)
    clean[ref] = out

payload = {
    'source': 'STEPBible TAHOT/TAGNT, CC BY 4.0, Tyndale House Cambridge',
    'versification': 'NRSV, per the STEPBible reference column',
    'verses': clean,
    'gloss': gloss,
}
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

print('parsed %d word rows from %d files' % (rows, len(files)))
print('wrote %s: %d verses, %d distinct Strong numbers, %d glossed'
      % (OUT, len(clean), len({n for v in clean.values() for n in v}), len(gloss)))
if unknown_books:
    print('\nbook codes with no mapping (%d rows):' % skipped_book)
    for c, n in unknown_books.most_common():
        print('   %-6s %d' % (c, n))

# Reconcile against the verse index, the way nrsv_index.py reconciles counts.
if os.path.exists('verses.json'):
    refs = {r['ref'] for r in json.load(open('verses.json', encoding='utf-8'))}
    covered = refs & set(clean)
    missing = refs - set(clean)
    by_book = collections.Counter(r.rsplit(' ', 1)[0] for r in missing)
    print('\nRECONCILED against verses.json')
    print('   verses in index      : %d' % len(refs))
    print('   verses with lemmas   : %d  (%.1f%%)' % (len(covered), 100 * len(covered) / len(refs)))
    print('   verses without       : %d' % len(missing))
    print('\n   uncovered by book (top 20) - deuterocanon is expected:')
    for b, n in by_book.most_common(20):
        print('      %-24s %5d' % (b, n))
