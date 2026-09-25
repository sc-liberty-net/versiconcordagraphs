"""lemma.py - ask the lemma index what is actually shared between passages.

Built by build_lemmas.py from the STEPBible tagged text. Every answer here is
about Hebrew or Greek, not about the NRSV's English, which is the whole point:
an edge tagged `lex` claims shared wording, and on an English index that claim
is really about a translator's word choice.

    python lemma.py verse "Matthew 6:19"
    python lemma.py lemma G2344
    python lemma.py shared "Matthew 6:19" "James 5:3"
    python lemma.py word treasure
    python lemma.py audit

`audit` is the one to run first: it takes every `lex` edge in
corpus_edges.csv and asks whether the two passages share any Hebrew or Greek
word at all. An edge with no shared lemma is an English coincidence, whatever
the NRSV looks like.

DENOMINATORS. Every lemma is reported with the number of verses that carry it.
That number is the difference between evidence and noise: a lemma shared by
two passages and four others is a finding; a lemma shared by two passages and
four hundred others is vocabulary. The corpus has no field for this yet - see
the note in QUESTIONS.md about motif edges.

COVERAGE. 83% of verses.json. The source is the Hebrew OT and Greek NT, so the
deuterocanonical books have no lemma data. `lemma.py` says so rather than
returning an empty answer that looks like a finding.
"""
import os, re, sys, json, csv, argparse, collections

IDX = 'strongs_index.json'
DEUTERO = {'Sirach', '2 Esdras', '1 Maccabees', '2 Maccabees', '3 Maccabees',
           '4 Maccabees', 'Wisdom of Solomon', '1 Esdras', 'Judith', 'Tobit',
           'Baruch', 'Letter of Jeremiah'}


def load():
    if not os.path.exists(IDX):
        sys.exit('%s not found - run build_lemmas.py first.' % IDX)
    d = json.load(open(IDX, encoding='utf-8'))
    return d['verses'], d['gloss']


def denominators(verses):
    c = collections.Counter()
    for nums in verses.values():
        for n in set(nums):
            c[n] += 1
    return c


def base(num):
    """H7225G -> H7225. STEPBible disambiguates homographs with a letter."""
    return re.match(r'([GH]\d+)', num).group(1)


def say_missing(ref, verses):
    if ref in verses:
        return False
    book = ref.rsplit(' ', 1)[0]
    if book in DEUTERO:
        print('   %s - no lemma data: %s is deuterocanonical, and the source '
              'is the Hebrew OT and Greek NT only.' % (ref, book))
    else:
        print('   %s - not in the lemma index. Check the reference, or it may '
              'be one of the extraction artifacts nrsv_index.py reports as '
              'gappy.' % ref)
    return True


def cmd_verse(a, verses, gloss, den):
    for ref in a.refs:
        print('%s' % ref)
        if say_missing(ref, verses):
            continue
        for n in verses[ref]:
            print('   %-8s %-34s in %5d verse(s)'
                  % (n, gloss.get(n, '')[:34], den[n]))
        print()


def cmd_lemma(a, verses, gloss, den):
    want = a.num.upper()
    hits = [r for r, nums in verses.items() if want in nums]
    if not hits:
        loose = [r for r, nums in verses.items() if any(base(n) == want for n in nums)]
        if loose:
            print('%s exactly: 0 verses. As a base number (ignoring the '
                  'disambiguating letter): %d verses.' % (want, len(loose)))
            hits = loose
        else:
            sys.exit('%s appears in no verse.' % want)
    print('%s  %s' % (want, gloss.get(want, '')))
    print('%d verse(s)' % len(hits))
    by_book = collections.Counter(r.rsplit(' ', 1)[0] for r in hits)
    for b, n in by_book.most_common(15):
        print('   %-24s %4d' % (b, n))
    if a.list:
        print()
        for r in sorted(hits)[:a.limit]:
            print('   ' + r)
        if len(hits) > a.limit:
            print('   ... and %d more' % (len(hits) - a.limit))


def cmd_shared(a, verses, gloss, den):
    x, y = a.a, a.b
    if say_missing(x, verses) or say_missing(y, verses):
        return
    sx, sy = set(verses[x]), set(verses[y])
    both = sx & sy
    loose = {base(n) for n in sx} & {base(n) for n in sy}
    print('%s  (%d lemmas)' % (x, len(sx)))
    print('%s  (%d lemmas)' % (y, len(sy)))
    print()
    if not both and not loose:
        print('NO shared lemma. Any shared English here is the translator\'s, '
              'not the source text\'s.')
        return
    print('shared: %d exact, %d by base number' % (len(both), len(loose)))
    for n in sorted(both, key=lambda n: den[n]):
        print('   %-8s %-32s in %5d verse(s)' % (n, gloss.get(n, '')[:32], den[n]))
    extra = loose - {base(n) for n in both}
    for n in sorted(extra):
        print('   %-8s %-32s (base match only)' % (n, ''))


def cmd_word(a, verses, gloss, den):
    """Which lemmas sit under an English word, across the whole index."""
    if not os.path.exists('verses.json'):
        sys.exit('verses.json not found - this one needs the NRSV index.')
    rx = re.compile(r'\b%s' % re.escape(a.text), re.I)
    hits = [r['ref'] for r in json.load(open('verses.json', encoding='utf-8'))
            if rx.search(r['text'])]
    print('"%s" appears in %d verse(s) of the English index.' % (a.text, len(hits)))
    covered = [r for r in hits if r in verses]
    print('%d of those have lemma data.' % len(covered))
    c = collections.Counter()
    for r in covered:
        for n in set(verses[r]):
            c[n] += 1
    print('\nlemmas present in those verses, commonest first.')
    print('NOTE: this is co-occurrence in the verse, not word alignment - the')
    print('lemma list is per verse, so common particles rank high. Read it as')
    print('a shortlist to check, never as "this word means that lemma".\n')
    for n, k in c.most_common(a.limit):
        print('   %-8s %-32s in %4d of these / %5d overall'
              % (n, gloss.get(n, '')[:32], k, den[n]))


def cmd_audit(a, verses, gloss, den):
    if not os.path.exists('corpus_edges.csv'):
        sys.exit('corpus_edges.csv not found - run from the project root.')
    nodes = {r['id']: r['ref'] for r in
             csv.DictReader(open('corpus_nodes.csv', encoding='utf-8'))}
    edges = [e for e in csv.DictReader(open('corpus_edges.csv', encoding='utf-8'))
             if e['kind'] == a.kind]
    print('Auditing %d `%s` edge(s) against the lemma index.\n' % (len(edges), a.kind))
    backed = bare = skipped = 0
    for e in edges:
        rx, ry = nodes.get(e['source']), nodes.get(e['target'])
        if not rx or not ry:
            continue
        label = '%s -> %s   %s / %s' % (e['source'], e['target'], rx, ry)
        if rx not in verses or ry not in verses:
            which = rx if rx not in verses else ry
            print('  SKIP    %s\n          no lemma data for %s' % (label, which))
            skipped += 1
            continue
        both = set(verses[rx]) & set(verses[ry])
        if not both:
            print('  NO      %s\n          warrant is `%s`; no shared lemma'
                  % (label, e['warrant']))
            bare += 1
            continue
        rarest = min(both, key=lambda n: den[n])
        print('  SHARED  %s\n          %d lemma(s); rarest %s %s in %d verse(s)'
              % (label, len(both), rarest, gloss.get(rarest, '')[:24], den[rarest]))
        backed += 1
    print('\n%d backed by a shared lemma, %d with none, %d not checkable'
          % (backed, bare, skipped))
    if bare:
        print('\nAn edge with no shared lemma is not necessarily wrong - two')
        print('passages can make the same argument in different words. But it')
        print('is not a `lex` edge, and `states` is the wrong warrant for it.')


p = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest='cmd', required=True)

s = sub.add_parser('verse', help='lemmas in one or more verses')
s.add_argument('refs', nargs='+')
s.set_defaults(fn=cmd_verse)

s = sub.add_parser('lemma', help='where a Strong number appears')
s.add_argument('num')
s.add_argument('--list', action='store_true', help='print the references')
s.add_argument('--limit', type=int, default=40)
s.set_defaults(fn=cmd_lemma)

s = sub.add_parser('shared', help='the lex test: what two passages share')
s.add_argument('a')
s.add_argument('b')
s.set_defaults(fn=cmd_shared)

s = sub.add_parser('word', help='which lemmas sit under an English word')
s.add_argument('text')
s.add_argument('--limit', type=int, default=25)
s.set_defaults(fn=cmd_word)

s = sub.add_parser('audit', help='check the corpus edges against the lemmas')
s.add_argument('--kind', default='lex', choices=['lex', 'ref', 'con'])
s.set_defaults(fn=cmd_audit)

args = p.parse_args()
v, g = load()
args.fn(args, v, g, denominators(v))
