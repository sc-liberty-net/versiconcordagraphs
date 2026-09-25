"""check_page.py - the gate. Run this before publishing the page.

Three steps, in order, stopping at the first failure:

  1. smoke_concordagraph.py     loads the built page in Chromium and prints what
                                the DOM actually contains
  2. smoke_diff.py              fails if ANY printed line moved against
                                smoke-baseline.out - including lines no
                                assertion covers
  3. dead_selector_lint.py      fails if the suite holds a selector no id or
                                class in the page can satisfy

WHY. On 25 Sept 2026 the page shipped blank three times. Every check passed,
because every check read the served HTML as text: the right strings were
present in a file whose script never ran. Reading HTML cannot see a parse
error. Running it can.

WHEN A LINE MOVES. It is a finding until you can explain it. Ask what changed
in the same edit, whether the new value follows from that change, and whether
anything else should have moved too. Once you can name the cause, move the
baseline with the guard - never by overwriting the file:

    python <skills>/smoke-gate/scripts/baseline_guard.py \\
        --baseline smoke-baseline.out --new new.out \\
        --cause "Hebrews 7 completed: six nodes, eleven edges" \\
        --record SMOKE-RECORD.md

The guard refuses a refresh with no cause, and the cause is the point.

    python check_page.py
"""
import os, sys, subprocess, tempfile

# The console here is cp1252 and the guards print box-drawing and dash
# characters. Without this the runner dies mid-report on a UnicodeEncodeError
# while telling you what moved - which is the least useful moment to crash.
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SKILL = os.path.expanduser(r'~\.claude\skills\smoke-gate\scripts')
BASELINE = 'smoke-baseline.out'
PAGE = 'concordagraph.html'


def run(label, cmd, capture_to=None):
    print('== %s' % label)
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding='utf-8', errors='replace')
    text = (out.stdout or '') + (out.returncode and (out.stderr or '') or '')
    if capture_to:
        open(capture_to, 'w', encoding='utf-8', newline='\n').write(out.stdout or '')
    for line in text.splitlines()[-14:]:
        print('   %s' % line)
    print('   exit %d' % out.returncode)
    print()
    return out.returncode


for path, what in ((PAGE, 'the built page'), (BASELINE, 'the baseline')):
    if not os.path.exists(path):
        sys.exit('missing %s (%s). Run build_graph.py, then record a baseline.'
                 % (path, what))

tmp = tempfile.mktemp(suffix='.out')

if run('1/3  run the page', [sys.executable, 'smoke_concordagraph.py'], capture_to=tmp):
    sys.exit('FAILED: the page did not run. Nothing else was checked.')

if run('2/3  gate every printed line',
       [sys.executable, os.path.join(SKILL, 'smoke_diff.py'), BASELINE, tmp]):
    sys.exit('FAILED: a printed line moved. Explain it before recording it.')

if run('3/3  lint the suite\'s selectors',
       [sys.executable, os.path.join(SKILL, 'dead_selector_lint.py'),
        'smoke_concordagraph.py', PAGE]):
    sys.exit('FAILED: the suite holds a selector the page cannot satisfy.')

os.remove(tmp)
print('PASSED - the page runs, nothing moved, no dead selectors.')
