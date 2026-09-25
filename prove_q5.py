"""Prove the new duplicate rule in both directions before trusting it.

RED  : a second `con` edge between a pair that already has one must be REFUSED.
GREEN: a `con` edge between a pair that already has a `lex` edge must be ACCEPTED.

The corpus file is restored from a snapshot after each probe, so neither probe
survives this script.
"""
import io, shutil, subprocess, sys, os

PATH = 'corpus_edges.csv'
SNAP = os.path.join(os.environ.get('TEMP', '.'), 'edges.snapshot.csv')
shutil.copy(PATH, SNAP)


def build():
    r = subprocess.run([sys.executable, 'build_graph.py'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def safe(s):
    """The console here is cp1252; build_graph prints an en-dash."""
    return s.encode('ascii', 'replace').decode('ascii')


def probe(label, row, expect_fail):
    shutil.copy(SNAP, PATH)
    try:
        with io.open(PATH, 'a', encoding='utf-8', newline='') as f:
            f.write(row + '\n')
        code, out = build()
        failed = code != 0
        ok = (failed == expect_fail)
        print('%-58s %s' % (label, 'PASS' if ok else '*** FAIL ***'))
        print('     exit %d, expected %s' % (code, 'non-zero' if expect_fail else 'zero'))
        for line in out.splitlines():
            if 'duplicate' in line.lower() or line.startswith('wrote'):
                print('     %s' % safe(line.strip())[:96])
        return ok
    finally:
        # Restore even if printing blows up - the first run of this script did
        # exactly that and left a probe row in the corpus.
        shutil.copy(SNAP, PATH)


results = []
# h1-h2 already carries a con edge. A second con edge on that pair is a duplicate.
results.append(probe('RED  : second `con` on a pair that has one -> refused',
                     'h1,h2,con,supports,probe', True))
# c1-c8 carries a lex edge and no con edge. A con edge there is now legitimate.
results.append(probe('GREEN: `con` on a pair that has only a `lex` -> accepted',
                     'c1,c8,con,spec,probe', False))

shutil.copy(SNAP, PATH)
code, out = build()
print()
print('corpus restored; rebuild exit %d' % code)
for line in out.splitlines():
    if line.startswith('wrote'):
        print('   %s' % line.strip())
os.remove(SNAP)
sys.exit(0 if all(results) else 1)
