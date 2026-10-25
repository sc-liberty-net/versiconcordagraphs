"""Prove the page-number assertion against the 34 slips it exists to catch.

    python test_page_numbers.py

Every case below is real. The wrong values were recovered from the reader's own
run log, transcript/runs.jsonl, where each run reports the pages it wrote as
"- 090 (LXXXI) - 11 entries, 2 [?]"; 34 of the 324 labels it reported disagree
with label(n). The shipped transcripts carry the corrected values, so the log is
the only remaining record of what the reader actually said.

The slips come in six contiguous runs -- 90-94, 295-298, 420-429, 535-539,
585-589, 670-674 -- because the reader latched onto a wrong reading and carried
it forward until the next batch. All 34 are a miscounted run of repeated letters
(X or C). The cause is in the crops: the numeral is printed at the top centre, so
the left and right halves each show part of it, and "LV" + "VI" is a guess rather
than a reading. The arithmetic is exact, image = printed page + 19, which is what
the assertion uses.

An assertion nobody has watched fail proves nothing, so this also checks that the
real headers still pass: the four pages that carry a printed stop or a doubt
marker, and the two images that legitimately print no numeral at all.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gesenius_pages import (EXEMPT, FIRST, LAST, label, page_number_issue,   # noqa: E402
                            transcript)

# (image, what the reader said, what the page actually is)
SLIPS = [
    (90, 'LXXXI', 'LXXI'), (91, 'LXXXII', 'LXXII'), (92, 'LXXXIII', 'LXXIII'),
    (93, 'LXXXIV', 'LXXIV'), (94, 'LXXXV', 'LXXV'),
    (295, 'CCLXXXVI', 'CCLXXVI'), (296, 'CCLXXXVII', 'CCLXXVII'),
    (297, 'CCLXXXVIII', 'CCLXXVIII'), (298, 'CCLXXXIX', 'CCLXXIX'),
    (420, 'CCCI', 'CCCCI'), (421, 'CCCII', 'CCCCII'), (422, 'CCCIII', 'CCCCIII'),
    (423, 'CCCIV', 'CCCCIV'), (424, 'CCCV', 'CCCCV'), (425, 'CCCVI', 'CCCCVI'),
    (426, 'CCCVII', 'CCCCVII'), (427, 'CCCVIII', 'CCCCVIII'),
    (428, 'CCCIX', 'CCCCIX'), (429, 'CCCX', 'CCCCX'),
    (535, 'DXXVI', 'DXVI'), (536, 'DXXVII', 'DXVII'), (537, 'DXXVIII', 'DXVIII'),
    (538, 'DXXIX', 'DXIX'), (539, 'DXXX', 'DXX'),
    (585, 'DLXXVI', 'DLXVI'), (586, 'DLXXVII', 'DLXVII'),
    (587, 'DLXXVIII', 'DLXVIII'), (588, 'DLXXIX', 'DLXIX'), (589, 'DLXXX', 'DLXX'),
    (670, 'DCCLI', 'DCLI'), (671, 'DCCLII', 'DCLII'), (672, 'DCCLIII', 'DCLIII'),
    (673, 'DCCLIV', 'DCLIV'), (674, 'DCCLV', 'DCLV'),
]

# Decoration that appears on correct pages and must not be read as a wrong number.
DECORATED = [(69, 'L.'), (360, 'CCCXLI.'), (55, 'XXXVI[?]'), (70, 'LI[?]'),
             (123, ' CIV '), (200, 'CLXXXI.[?]')]

# Headers that are not a page number at all.
MALFORMED = [(100, 'RUNNING HEADS: left | right'), (100, 'אב the first line of a page'),
             (100, ''), (100, 'RUNNING HEADS: left |  | right')]


def head(page, left='אב', right='אג'):
    return f'RUNNING HEADS: {left} | {page} | {right}'


def main():
    ok = bad = 0

    def case(good, label_text, detail=''):
        nonlocal ok, bad
        if good:
            ok += 1
        else:
            bad += 1
            print('  FAIL  %s%s' % (label_text, detail))

    print('the 34 slips the reader actually made')
    for n, said, want in SLIPS:
        if label(n) != want:
            case(False, 'n%03d' % n,
                 ': fixture says the page is %s, label() says %s' % (want, label(n)))
            continue
        issue = page_number_issue(n, head(said))
        case(bool(issue) and said in issue and want in issue, 'n%03d' % n,
             ': %r was not caught (%s)' % (said, issue or 'no issue reported'))
    print('  %d of %d caught' % (ok, len(SLIPS)))

    print('\ncorrect pages, including printed stops and doubt markers')
    before = ok
    for n, written in DECORATED:
        issue = page_number_issue(n, head(written))
        case(issue is None, 'n%03d %r' % (n, written), ': %s' % issue)
    for n, why in EXEMPT.items():
        for written in ('[none]', '', ' '):
            issue = page_number_issue(n, head(written))
            case(issue is None, 'n%03d exempt %r' % (n, written),
                 ': %s (%s)' % (issue, why))
    case(page_number_issue(300, head(label(300))) is None, 'a plain correct page')
    print('  %d accepted' % (ok - before))

    print('\nheaders that are not a page number')
    before = ok
    for n, line in MALFORMED:
        case(page_number_issue(n, line) is not None, 'malformed %r' % line[:40],
             ': accepted')
    case(page_number_issue(300, head('')) is not None,
         'an empty field on a page that is not exempt', ': accepted')
    print('  %d rejected' % (ok - before))

    print('\nthe shipped transcripts')
    before = ok
    shipped = 0
    for n in range(FIRST, LAST + 1):
        p = transcript(n)
        if not p.exists():
            continue
        shipped += 1
        lines = p.read_text(encoding='utf-8').splitlines()
        issue = page_number_issue(n, lines[0] if lines else '')
        case(issue is None, 'shipped n%03d' % n, ': %s' % issue)
    print('  %d of %d pass' % (ok - before, shipped))

    print('\n%d passed, %d failed' % (ok, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
