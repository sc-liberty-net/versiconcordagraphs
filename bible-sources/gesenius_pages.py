"""Page tool for transcribing Gesenius (Tregelles 1857) one page at a time.

    python gesenius_pages.py status          next unread page, and totals so far
    python gesenius_pages.py prepare N [N…]  fetch images at full resolution, cut 4 crops each
    python gesenius_pages.py check N         check transcript N (page number, headwords, citations)
    python gesenius_pages.py pages           every transcript's page number against the arithmetic;
                                             exits non-zero if any is wrong
    python gesenius_pages.py run COUNT [PER_RUN]
                                             transcribe the next COUNT unread pages with the
                                             lean reader, PER_RUN pages per run (default 1),
                                             logging each; token detail in transcript/runs.jsonl
    python gesenius_pages.py done N TOKENS SECONDS
                                             log page N in PROGRESS.md, remove its crops

Image N (0-based, as archive.org numbers them) is printed page N - 19; the
lexicon runs from image 20 (page I) to image 903 (page DCCCLXXXIV). See
RULES.md for why pages are read from crops, and by an Opus-class model.
"""
import datetime
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).parent
G = HERE / 'lexicons/gesenius'
CROPS = G / 'crops'
TRANSCRIPT = G / 'transcript'
PROGRESS = TRANSCRIPT / 'PROGRESS.md'
ITEM = 'hebrewchaldeelex00geseuoft'
FIRST, LAST, OFFSET = 20, 903, 19


def roman(n):
    out = ''
    for v, s in ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
                 (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v:
            out, n = out + s, n - v
    return out


def label(n):
    # The book prints hundreds as CCCC, not CD (image 470 is page CCCCLI).
    return roman(n - OFFSET).replace('CD', 'CCCC')


def transcript(n):
    return TRANSCRIPT / f'n{n:03d}.txt'


# ---------------------------------------------------------------- page number
# The reader miscounted repeated letters in the printed numeral 34 times across
# six runs: images 90-94 read LXXXI for LXXI, 295-298 CCLXXXVI for CCLXXVI,
# 420-429 dropped a C (CCCI for CCCCI), 535-539 and 585-589 gained an X, 670-674
# gained a C. Each run carried the wrong reading forward until the next batch.
# The cause is in the crops, not the reader: the numeral sits at the top centre
# of the page, so the left and right crops each show only part of it ("LV" plus
# "VI"), and a half-seen run of X's or C's is a guess. The arithmetic is exact --
# image = printed page + 19 -- so the numeral never needed to be read at all.
EXEMPT = {
    20: 'the opening page prints no running heads',
    896: 'the Grammatical and Analytical Index opens here and prints no numeral',
}


def page_field(first_line):
    """The page-number field of a RUNNING HEADS line, or None if there is none."""
    if not first_line.startswith('RUNNING HEADS:'):
        return None
    parts = first_line[len('RUNNING HEADS:'):].split('|')
    return parts[1].strip() if len(parts) >= 3 else None


def page_number_issue(n, first_line):
    """None when the header's page number is right, else a line saying why not.

    Takes the line rather than the file so it can be tested against the 34 real
    slips without writing a transcript: see test_page_numbers.py.
    """
    field = page_field(first_line)
    if field is None:
        return (f'image {n}: the first line is not a RUNNING HEADS line with '
                f'three |-separated fields')
    got = field.strip()
    while True:                       # a doubt marker and a printed stop are
        stripped = got                # decoration, not a different number
        for suffix in ('[?]', '.'):
            if stripped.endswith(suffix):
                stripped = stripped[:-len(suffix)].strip()
        if stripped == got:
            break
        got = stripped
    want = label(n)
    if got in ('', '[none]'):
        if n in EXEMPT:
            return None
        return (f'image {n}: the page-number field is empty, but the scan prints '
                f'{want}')
    if got != want:
        return (f'image {n}: the header says {field.strip()!r}, the page is {want} '
                f'(image {n} - {OFFSET}). Read the numeral off the arithmetic, not '
                f'the crop: it is split across the left and right halves.')
    return None


def page_numbers(quiet=False):
    """Every transcript's header against label(n). Returns the problems."""
    bad = []
    for n in range(FIRST, LAST + 1):
        p = transcript(n)
        if not p.exists():
            continue
        first = p.read_text(encoding='utf-8').splitlines()
        issue = page_number_issue(n, first[0] if first else '')
        if issue:
            bad.append(issue)
    if not quiet:
        checked = sum(1 for n in range(FIRST, LAST + 1) if transcript(n).exists())
        for x in bad:
            print(' ', x)
        print(f'{checked} transcripts checked, {len(bad)} page number(s) wrong'
              + (f', {len(EXEMPT)} image(s) exempt: '
                 + ', '.join(f'{k} ({v})' for k, v in EXEMPT.items()) if not bad else ''))
    return bad


# ---------------------------------------------------------------- prepare
def prepare(n):
    from PIL import Image
    CROPS.mkdir(parents=True, exist_ok=True)
    full = CROPS / f'n{n:03d}_full.jpg'
    url = f'https://archive.org/download/{ITEM}/page/n{n}.jpg'
    with urllib.request.urlopen(url, timeout=120) as r:
        full.write_bytes(r.read())
    im = Image.open(full)
    x0, y0, x1, y1, gutter = text_area(im)
    ym = (y0 + y1) // 2
    # Cut at the gutter found in the page, not at the image's midline, and
    # leave out the blank margins: fewer pixels per crop, same text.
    boxes = {'L1': (x0, y0, gutter + 12, ym + 60), 'L2': (x0, ym - 60, gutter + 12, y1),
             'R1': (gutter - 12, y0, x1, ym + 60), 'R2': (gutter - 12, ym - 60, x1, y1)}
    for k, b in boxes.items():
        im.crop(b).save(CROPS / f'n{n:03d}_{k}.jpg', quality=92)
    kept = (x1 - x0) * (y1 - y0) / (im.size[0] * im.size[1])
    im.close()
    full.unlink()
    print(f'image {n} (page {label(n)}): crops in {CROPS} ({kept:.0%} of the scan kept)')


def text_area(im, pad=30):
    """Bounding box of the printed text and the x of the column gutter.
    Rows and columns count as text where more than a sliver of them is ink;
    the outer 2% of the scan is ignored, as it holds page edges and shadow."""
    import numpy as np
    a = np.asarray(im.convert('L')) < 110
    h, w = a.shape
    ex, ey = int(w * 0.02), int(h * 0.02)
    cols = a[ey:h - ey].mean(axis=0)
    rows = a[:, ex:w - ex].mean(axis=1)
    xs = np.where(cols[ex:w - ex] > 0.004)[0] + ex
    ys = np.where(rows[ey:h - ey] > 0.004)[0] + ey
    if len(xs) == 0 or len(ys) == 0:
        return 0, 0, w, h, w // 2
    x0, x1 = max(0, xs[0] - pad), min(w, xs[-1] + pad)
    y0, y1 = max(0, ys[0] - pad), min(h, ys[-1] + pad)
    # The gutter: the emptiest band of columns in the middle fifth of the text.
    lo, hi = x0 + (x1 - x0) * 2 // 5, x0 + (x1 - x0) * 3 // 5
    band = np.convolve(a[y0:y1, lo:hi].mean(axis=0), np.ones(15) / 15, mode='same')
    gutter = lo + int(np.argmin(band))
    return int(x0), int(y0), int(x1), int(y1), gutter


# ---------------------------------------------------------------- check
HEB = re.compile(r'[א-תְ-ׇּׁׂװ-ײֽ֑-֯͏]+')
DROP = re.compile(r'[֑-ֽ֯͏׀׃ׅׄ]')
POINTS = re.compile(r'[ְ-ׇּׁׂ]')
BOOKS = {
    'Gen': 'Genesis', 'Ex': 'Exodus', 'Exod': 'Exodus', 'Lev': 'Leviticus', 'Levit': 'Leviticus',
    'Num': 'Numbers', 'Deu': 'Deuteronomy', 'Deut': 'Deuteronomy', 'Josh': 'Joshua',
    'Jos': 'Joshua', 'Jud': 'Judges', 'Judg': 'Judges', 'Ruth': 'Ruth', '1Sa': 'Samuel_1',
    '1Sam': 'Samuel_1', '2Sa': 'Samuel_2', '2Sam': 'Samuel_2', '1Ki': 'Kings_1',
    '1K': 'Kings_1', '2Ki': 'Kings_2', '2K': 'Kings_2', '1Ch': 'Chronicles_1',
    '1Chr': 'Chronicles_1', '2Ch': 'Chronicles_2', '2Chr': 'Chronicles_2', 'Ezr': 'Ezra',
    'Ezra': 'Ezra', 'Neh': 'Nehemiah', 'Est': 'Esther', 'Esth': 'Esther', 'Job': 'Job',
    'Ps': 'Psalms', 'Psa': 'Psalms', 'Prov': 'Proverbs', 'Pro': 'Proverbs',
    'Ecc': 'Ecclesiastes', 'Eccl': 'Ecclesiastes', 'Cant': 'Song_of_Songs', 'Isa': 'Isaiah',
    'Jer': 'Jeremiah', 'Lam': 'Lamentations', 'Eze': 'Ezekiel', 'Ezek': 'Ezekiel',
    'Dan': 'Daniel', 'Hos': 'Hosea', 'Joel': 'Joel', 'Am': 'Amos', 'Amos': 'Amos',
    'Obad': 'Obadiah', 'Ob': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah', 'Nah': 'Nahum',
    'Hab': 'Habakkuk', 'Zeph': 'Zephaniah', 'Hag': 'Haggai', 'Zech': 'Zechariah',
    'Zec': 'Zechariah', 'Mal': 'Malachi',
}
REF = re.compile(r'(?:(\d?\s?[A-Z][a-z]{1,5})\.?\s*)?(\d{1,3})\s?:\s?(\d{1,3})')
_verses = {}


def norm(w):
    return DROP.sub('', unicodedata.normalize('NFC', w))


def bare(w):
    return POINTS.sub('', norm(w)).translate(str.maketrans('ךםןףץ', 'כמנפצ'))


def lemmas():
    pointed, letters = set(), set()
    for f in (HERE / 'stepbible').glob('TBESH*.txt'):
        for line in f.read_text(encoding='utf-8-sig').splitlines():
            c = line.split('\t')
            if len(c) > 4 and re.fullmatch(r'H\d{4}', c[0]):
                for w in HEB.findall(c[3]):
                    pointed.add(norm(w))
                    letters.add(bare(w))
    return pointed, letters


def verse(book, c, v):
    if book not in _verses:
        d = {}
        for ch in ET.parse(HERE / 'hebrew/uxlc/Books' / f'{book}.xml').iter('c'):
            for vv in ch.iter('v'):
                d[(int(ch.get('n')), int(vv.get('n')))] = [
                    ''.join(w.itertext()) for w in vv.iter() if w.tag in ('w', 'k', 'q')]
        _verses[book] = d
    return _verses[book].get((c, v))


def check(n, quiet=False):
    """Headwords found in STEPBible's Hebrew lemma list, and Hebrew quoted
    before a verse reference found in that verse of the Leningrad Codex.
    'letters' means the letters match but the points do not: often a
    real misreading, sometimes Gesenius citing a different form."""
    text = transcript(n).read_text(encoding='utf-8')
    pointed, letters = lemmas()
    hw = {'points': 0, 'letters': 0, 'missing': 0}
    for line in text.splitlines():
        m = HEB.match(line.lstrip('[(* '))
        if m and not line.startswith('RUNNING'):
            h = m.group(0).split('־')[0]
            hw['points' if norm(h) in pointed else 'letters' if bare(h) in letters else 'missing'] += 1
    ct = {'points': 0, 'letters': 0, 'missing': 0}
    misses = []
    book = None
    for seg in re.split(r'[;\n]', text):
        for m in REF.finditer(seg):
            if m.group(1):
                book = BOOKS.get(m.group(1).replace(' ', ''))
            if not book:
                continue
            words = verse(book, int(m.group(2)), int(m.group(3)))
            if not words:
                continue
            vp = [norm(w).replace('־', '') for w in words]
            vb = [bare(w).replace('־', '') for w in words]
            for w in HEB.findall(seg[max(0, m.start() - 45):m.start()]):
                for part in w.split('־'):
                    if len(bare(part)) < 2:
                        continue
                    if any(norm(part) in x for x in vp):
                        ct['points'] += 1
                    elif any(bare(part) in x for x in vb):
                        ct['letters'] += 1
                        misses.append(f'{part} {book} {m.group(2)}:{m.group(3)} (points differ)')
                    else:
                        ct['missing'] += 1
                        misses.append(f'{part} {book} {m.group(2)}:{m.group(3)} (not in verse)')
    unsure = text.count('[?]')
    entries = sum(1 for line in text.splitlines() if HEB.match(line.lstrip('[(* ')))
    lines = text.splitlines()
    issue = page_number_issue(n, lines[0] if lines else '')
    if not quiet:
        print(f'image {n} (page {label(n)}): {entries} entry lines, {unsure} [?]')
        print('  page no.  :', issue or f'{label(n)} as printed')
        print('  headwords :', hw)
        print('  citations :', ct)
        for x in misses:
            print('   ', x)
    return entries, unsure, hw, ct


# ---------------------------------------------------------------- progress
HEADER = """# Gesenius transcription — progress

Read by `python gesenius_pages.py status`. One row per finished page. The
next unread page is the image after the last row. Transcripts are
`n###.txt` in this folder; a row is written only after the page's
transcript exists and has been checked.

| image | page | entry lines | [?] | headwords pts/letters/miss | citations pts/letters/miss | tokens | seconds | date |
|---|---|---|---|---|---|---|---|---|
"""


def rows():
    if not PROGRESS.exists():
        return []
    out = []
    for line in PROGRESS.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\| (\d+) \|', line)
        if m:
            cells = [c.strip() for c in line.strip('|').split('|')]
            out.append({'image': int(cells[0]), 'tokens': int(cells[6]), 'seconds': int(cells[7])})
    return out


def done(n, tokens, seconds):
    if not transcript(n).exists():
        sys.exit(f'no transcript for image {n}; nothing logged')
    if any(r['image'] == n for r in rows()):
        sys.exit(f'image {n} is already logged')
    # Refuse here rather than only warning in check(): this is where a page stops
    # being a file and becomes a logged fact, and a wrong numeral carried forward
    # six times before anyone noticed. Correct the transcript's first line, then
    # run this again.
    issue = page_number_issue(n, transcript(n).read_text(encoding='utf-8').splitlines()[0])
    if issue:
        sys.exit(f'not logged -- {issue}')
    entries, unsure, hw, ct = check(n, quiet=True)
    TRANSCRIPT.mkdir(parents=True, exist_ok=True)
    if not PROGRESS.exists():
        PROGRESS.write_text(HEADER, encoding='utf-8')
    row = (f"| {n} | {label(n)} | {entries} | {unsure} | "
           f"{hw['points']}/{hw['letters']}/{hw['missing']} | "
           f"{ct['points']}/{ct['letters']}/{ct['missing']} | {tokens} | {seconds} | "
           f"{datetime.date.today()} |\n")
    with PROGRESS.open('a', encoding='utf-8') as f:
        f.write(row)
    for c in CROPS.glob(f'n{n:03d}_*.jpg'):
        c.unlink()
    print('logged:', row.strip())


RUNS = TRANSCRIPT / 'runs.jsonl'
READER = ['claude', '-p', '--agent', 'gesenius-reader', '--tools', 'Read', 'Write',
          '--allowedTools', 'Read', 'Write', '--strict-mcp-config',
          '--disable-slash-commands', '--no-session-persistence', '--output-format', 'json']


def run(count, per_run=1):
    """Transcribe the next COUNT unread pages, PER_RUN pages to each run of
    the lean reader (.claude/agents/gesenius-reader.md, driven through the
    claude command line so it loads only Read and Write). Stops at the
    first failure."""
    import json
    import subprocess
    start = max((x['image'] for x in rows()), default=FIRST - 1) + 1
    pages = list(range(start, min(LAST, start + count - 1) + 1))
    for k in range(0, len(pages), per_run):
        chunk = pages[k:k + per_run]
        for n in chunk:
            prepare(n)
        prompt = 'Images ' + ', '.join(str(n) for n in chunk) + '.'
        t0 = datetime.datetime.now()
        p = subprocess.run(READER[:2] + [prompt] + READER[2:], cwd=HERE.parent,
                           capture_output=True, text=True, encoding='utf-8')
        secs = int((datetime.datetime.now() - t0).total_seconds())
        try:
            d = json.loads(p.stdout)
        except ValueError:
            sys.exit(f'reader failed on {chunk}: {p.stderr[-500:]}')
        u = d.get('usage', {})
        tokens = sum(u.get(x, 0) for x in ('input_tokens', 'cache_creation_input_tokens',
                                           'cache_read_input_tokens', 'output_tokens'))
        with RUNS.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'images': chunk, 'seconds': secs, 'tokens': tokens,
                                'cost_usd_list': d.get('total_cost_usd'), 'usage': u,
                                'result': d.get('result'), 'error': d.get('is_error')}) + '\n')
        missing = [n for n in chunk if not transcript(n).exists()]
        if d.get('is_error') or missing:
            sys.exit(f'reader stopped: error={d.get("is_error")} missing={missing}')
        for n in chunk:
            done(n, tokens // len(chunk), secs // len(chunk))


def status():
    r = rows()
    nxt = max((x['image'] for x in r), default=FIRST - 1) + 1
    if nxt > LAST:
        print('all pages done')
    else:
        print(f'next unread: image {nxt} (page {label(nxt)})')
    if r:
        t = sum(x['tokens'] for x in r)
        s = sum(x['seconds'] for x in r)
        left = LAST - nxt + 1
        print(f'done {len(r)} pages: {t:,} tokens, {s / 60:.0f} min; '
              f'average {t // len(r):,} tokens, {s // len(r)} s per page')
        print(f'remaining {left} pages at that rate: {t // len(r) * left / 1e6:.1f}M tokens, '
              f'{s / len(r) * left / 3600:.1f} h')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        status()
    elif cmd == 'prepare':
        for a in sys.argv[2:]:
            prepare(int(a))
    elif cmd == 'check':
        check(int(sys.argv[2]))
    elif cmd == 'pages':
        sys.exit(1 if page_numbers() else 0)
    elif cmd == 'run':
        run(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == 'done':
        done(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        sys.exit(__doc__)
