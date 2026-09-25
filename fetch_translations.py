"""fetch_translations.py - build translations.json for the corpus references.

Downloads eight PUBLIC DOMAIN English versions and keeps only the verses the
corpus actually cites, so the working file stays small:

    {"Matthew 23:23": {"KJV": "...", "ASV": "...", ...}, ...}

WHY THESE EIGHT. Not for coverage - for disagreement. Where translations of one
verse diverge, the English is doing interpretive work, and any `lex` edge
resting on that English is resting on a translator's choice. The spread is
deliberate: three centuries, and three textual/confessional traditions.

    KJV         1769   the text Strong's numbers are keyed to
    Geneva1599  1599   pre-KJV Protestant, the Bible of the Puritans
    DRC         1899   translated from the Latin Vulgate - a different base text
    JPS         1917   Jewish Publication Society; Hebrew Bible, outside the
                       Christian translation tradition entirely
    ASV         1901   literal; the direct ancestor of the RSV and NRSV
    YLT         1898   Young's Literal; preserves Hebrew and Greek tense and
                       word order at the cost of English
    WEB         2000s  modern public domain
    BSB         2022   modern; STEPBible's own English glosses derive from it

NOT INCLUDED, and why: NASB, NIV and ESV are all under copyright. The corpus
cites 158 verses, which is inside every one of those publishers' free-use
quotas - but a quota is permission to quote, not a source to download from, and
scraping Bible Hub or Bible Gateway would breach their terms. Adding them
properly means an API key from api.bible or Crossway, which is Ethan's to
obtain. LEB was also skipped: freely licensed, but not public domain.

Source: github.com/scrollmapper/bible_databases (MIT). The bulk downloads land
in translations-data/ and are gitignored; translations.json is the small
extract everything else reads.

    python fetch_translations.py
"""
import os, sys, json, csv, urllib.request

BASE = 'https://raw.githubusercontent.com/scrollmapper/bible_databases/master/sources/en/%s/%s.json'
VERSIONS = ['KJV', 'Geneva1599', 'DRC', 'JPS', 'ASV', 'YLT', 'BSB']

RAW = 'translations-data'
OUT = 'translations.json'

# The corpus spells some books differently from these editions. The big one is
# the numbered books: every edition here writes "I Samuel" and "II Corinthians"
# in Roman numerals, where the corpus writes "1 Samuel" and "2 Corinthians".
# Missing that cost all eight numbered-book references on the first run.
ALIAS = {
    'Psalms': 'Psalm',
    'Song of Songs': 'Song of Solomon', 'Canticles': 'Song of Solomon',
    'Revelation of John': 'Revelation', 'The Revelation': 'Revelation',
}
ROMAN = (('III ', '3 '), ('II ', '2 '), ('I ', '1 '))


def normalise(name):
    for r, a in ROMAN:            # III before II before I, or the prefixes collide
        if name.startswith(r):
            name = a + name[len(r):]
            break
    return ALIAS.get(name, name)

os.makedirs(RAW, exist_ok=True)

refs = {r['ref'] for r in csv.DictReader(open('corpus_nodes.csv', encoding='utf-8'))}
print('corpus cites %d distinct references\n' % len(refs))

out = {r: {} for r in refs}
report = []

for v in VERSIONS:
    dest = os.path.join(RAW, '%s.json' % v)
    if not (os.path.exists(dest) and os.path.getsize(dest) > 500_000):
        url = BASE % (v, v)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'biblography'})
            with urllib.request.urlopen(req, timeout=240) as r, open(dest, 'wb') as f:
                f.write(r.read())
        except Exception as e:
            print('%-12s DOWNLOAD FAILED  %s' % (v, e))
            report.append((v, 0, 'download failed'))
            continue
    try:
        data = json.load(open(dest, encoding='utf-8-sig'))
    except Exception as e:
        print('%-12s PARSE FAILED  %s' % (v, e))
        report.append((v, 0, 'parse failed'))
        continue

    got = 0
    for book in data.get('books', []):
        name = normalise(book['name'])
        for ch in book.get('chapters', []):
            for vs in ch.get('verses', []):
                ref = '%s %s:%s' % (name, ch['chapter'], vs['verse'])
                if ref in out:
                    out[ref][v] = ' '.join(vs['text'].split())
                    got += 1
    size = os.path.getsize(dest) / 1e6
    print('%-12s %5.1f MB   %3d / %d corpus verses' % (v, size, got, len(refs)))
    report.append((v, got, ''))

json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

full = sum(1 for r in out if len(out[r]) == len(VERSIONS))
print()
print('wrote %s' % OUT)
print('   %d of %d references carry all %d versions' % (full, len(refs), len(VERSIONS)))
thin = {r: sorted(set(VERSIONS) - set(out[r])) for r in out if len(out[r]) < len(VERSIONS)}
if thin:
    print('\n   references missing a version (expected: JPS is Hebrew Bible only,')
    print('   and the older editions differ on a few verse divisions):')
    for r in sorted(thin)[:14]:
        print('      %-22s missing %s' % (r, ', '.join(thin[r])))
    if len(thin) > 14:
        print('      ... and %d more' % (len(thin) - 14))
