"""Download the six STEPBible TAHOT/TAGNT files into lemma-data/.

Source: github.com/STEPBible/STEPBible-Data, CC BY 4.0 (Tyndale House Cambridge).
STEPBible ask that the data not be redistributed -- so these land in a
gitignored folder and are re-fetched from source, never committed.
"""
import os, sys, urllib.request, urllib.parse

BASE = ('https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/'
        + urllib.parse.quote('Translators Amalgamated OT+NT') + '/')

FILES = [
    'TAHOT Gen-Deu - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt',
    'TAHOT Jos-Est - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt',
    'TAHOT Job-Sng - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt',
    'TAHOT Isa-Mal - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt',
    'TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt',
    'TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt',
]

OUT = 'lemma-data'
os.makedirs(OUT, exist_ok=True)

total = 0
for name in FILES:
    dest = os.path.join(OUT, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 1_000_000:
        print('have   %8.1f MB  %s' % (os.path.getsize(dest) / 1e6, name[:44]))
        total += os.path.getsize(dest)
        continue
    url = BASE + urllib.parse.quote(name)
    req = urllib.request.Request(url, headers={'User-Agent': 'biblography-lemma-layer'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r, open(dest, 'wb') as f:
            data = r.read()
            f.write(data)
        print('got    %8.1f MB  %s' % (len(data) / 1e6, name[:44]))
        total += len(data)
    except Exception as e:
        print('FAILED %s\n       %s' % (name[:44], e))
        sys.exit(1)

print()
print('%d files, %.1f MB in %s/' % (len(FILES), total / 1e6, OUT))
