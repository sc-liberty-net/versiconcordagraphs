"""Prove the smoke suite fails on the bug it was written for.

A check nobody has seen go red proves nothing. This reintroduces the exact
defect - a second `const HUB` colliding with the hub-cluster constant - into a
COPY of the page, runs the suite against that copy, and asserts it fails.
The real concordagraph.html is never touched.
"""
import io, os, shutil, subprocess, sys, tempfile

SRC = 'concordagraph.html'
tmp = tempfile.mkdtemp(prefix='smoke-red-')
broken = os.path.join(tmp, 'broken.html')

html = io.open(SRC, encoding='utf-8').read()
OLD = 'const BIBLEHUB_SLUG = {'
if html.count(OLD) != 1:
    sys.exit('REFUSED - could not find the slug map to sabotage')
# exactly the original defect: reuse the identifier already taken by the hub cluster
html_broken = html.replace(OLD, 'const HUB = {', 1).replace(
    'return BIBLEHUB_SLUG[book]', 'return HUB[book]', 1)
io.open(broken, 'w', encoding='utf-8', newline='').write(html_broken)

def run(page):
    r = subprocess.run([sys.executable, 'smoke_concordagraph.py', '--page', page],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, r.stdout or ''

code_red, out_red = run(broken)
code_green, out_green = run(SRC)
shutil.rmtree(tmp, ignore_errors=True)

def line(out, label):
    for l in out.splitlines():
        if l.startswith(label + ':'):
            return l
    return '(no %s line)' % label

print('RED  - page with the HUB collision reintroduced')
print('   exit %d  (must be non-zero)' % code_red)
for lbl in ('console errors', 'drawn nodes', 'drawn arcs', 'fatal'):
    print('   %s' % line(out_red, lbl))
print()
print('GREEN - the real page')
print('   exit %d  (must be zero)' % code_green)
for lbl in ('console errors', 'drawn nodes', 'drawn arcs', 'fatal'):
    print('   %s' % line(out_green, lbl))
print()
ok = code_red != 0 and code_green == 0
print('PROOF %s' % ('PASSED - the suite sees the defect it was built for'
                    if ok else '*** FAILED ***'))
sys.exit(0 if ok else 1)
