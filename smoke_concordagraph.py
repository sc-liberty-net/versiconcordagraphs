"""smoke_concordagraph.py - load the built page in a real browser and print
what it actually produced.

WHY THIS EXISTS. On 25 Sept 2026 the published page rendered blank for three
pushes while every check passed. The checks read the served HTML for the right
strings - the biblehub URLs were present, all 25 book slugs resolved, META held
the right counts - and all of that was true of a file whose script never ran. A
second `const HUB` collided with the hub-cluster constant, and a duplicate
declaration is a PARSE error, so the whole script died before its first line.
Nothing that reads HTML as text can see that. Only running it can.

So this loads the page in Chromium and reports what the DOM contains afterwards.

WHAT IT PRINTS, AND WHY IT PRINTS POPULATIONS. Every line is `label: value`,
and every check prints the population it examined rather than a verdict. A
check that prints `ok` looks identical whether it read 164 nodes or none; a
check that prints `164` cannot. Pair this with smoke_diff.py from the
smoke-gate skill, which fails on any line that moves against a recorded
baseline - including lines no assertion covers.

DETERMINISM. Fixed viewport, no timings, no seeds, and the layout is seeded
from node index rather than Math.random, so the same corpus gives the same
output. Sizes are rounded to the nearest 10 px to keep sub-pixel noise out.

ISOLATION. The page is copied to a temporary directory WITHOUT verses.js, so
what runs is the published page - references and summaries only - not the local
copy that has the NRSV payload beside it.

    python smoke_concordagraph.py                     # defaults to concordagraph.html
    python smoke_concordagraph.py --page other.html
    python smoke_concordagraph.py > smoke.out         # then gate with smoke_diff.py

Exit 0 if the page ran, 1 if it did not (console errors, or nothing drawn).
The gate, not this script, decides whether an unchanged-but-different run is
acceptable.
"""
import sys, os, io, json, shutil, tempfile, argparse

sys.stdout.reconfigure(encoding='utf-8')

ap = argparse.ArgumentParser()
ap.add_argument('--page', default='concordagraph.html')
args = ap.parse_args()

if not os.path.exists(args.page):
    sys.exit('not found: %s' % args.page)

from playwright.sync_api import sync_playwright

tmp = tempfile.mkdtemp(prefix='concordagraph-smoke-')
shutil.copy(args.page, os.path.join(tmp, 'index.html'))
url = 'file:///' + os.path.join(tmp, 'index.html').replace('\\', '/')

errors, fatal = [], []


def P(label, value):
    print('%s: %s' % (label, value))


def ev(page, expr, default='UNAVAILABLE'):
    """Evaluate in the page, but never let a dead page crash the suite.

    When the script has not run, the elements it creates do not exist and
    probes like `#net g`.getBBox() throw. A suite that dies on a traceback
    gives the gate nothing to diff and the reader nothing to read - which is
    exactly the failure this file exists to report. So every probe degrades to
    a printed value instead.
    """
    try:
        return page.evaluate(expr)
    except Exception as exc:
        return '%s (%s)' % (default, str(exc).splitlines()[0][:60])


def pick(obj, key):
    """Read a key whether the probe returned a dict or an error string.

    ev() degrades to a string when the page is dead. Indexing that string
    raised TypeError and killed the suite halfway through its own report -
    caught while proving the suite against the HUB defect it was built for.
    """
    return obj.get(key, 'MISSING') if isinstance(obj, dict) else obj


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append('pageerror: %s' % e))
        page.goto(url, wait_until='load')
        page.wait_for_timeout(1200)

        # --- did the script run at all --------------------------------------
        # verses.js is deliberately absent, so its 404 is expected and is not
        # a script failure. Anything else is.
        real = [e for e in errors if 'verses.js' not in e
                and 'Failed to load resource' not in e]
        P('console errors', len(real))
        for e in real:
            P('console error', e[:150])
            fatal.append(e)

        # --- the corpus, as the page holds it --------------------------------
        meta = ev(page, '() => (typeof META !== "undefined") ? META : null', None)
        P('META', json.dumps(meta, sort_keys=True) if meta else 'UNDEFINED - script did not run')
        if not meta:
            fatal.append('META undefined')
        P('corpus N length', ev(page, '() => (typeof N !== "undefined") ? N.length : -1'))
        P('corpus E length', ev(page, '() => (typeof E !== "undefined") ? E.length : -1'))

        # --- what was actually drawn -----------------------------------------
        drawn = ev(page, '''() => ({
            nodes: document.querySelectorAll('.node').length,
            arcs: document.querySelectorAll('path.edge').length,
            hits: document.querySelectorAll('path.hit').length,
            labels: document.querySelectorAll('.booklab').length,
            ticks: document.querySelectorAll('.tick').length
        })''')
        for k in ('nodes', 'arcs', 'hits', 'labels', 'ticks'):
            P('drawn %s' % k, pick(drawn, k))
        if pick(drawn, 'nodes') in (0, 'MISSING') or pick(drawn, 'arcs') in (0, 'MISSING'):
            fatal.append('graph drew nothing')

        # --- the rail --------------------------------------------------------
        rail = ev(page, '''() => ({
            clusters: document.querySelectorAll('#clusters .row').length,
            warrants: document.querySelectorAll('#warrants .row').length,
            kinds: document.querySelectorAll('#types .row').length,
            groupLensHidden: document.getElementById('mGroup').classList.contains('hide')
        })''')
        for k in ('clusters', 'warrants', 'kinds'):
            P('rail %s' % k, pick(rail, k))
        P('rail group lens hidden', pick(rail, 'groupLensHidden'))

        # --- the header writes itself from the generated counts ---------------
        P('header', ev(page, '() => document.getElementById("hSub").textContent.slice(0,64)'))
        P('title', page.title())

        # --- the graph occupies space ----------------------------------------
        box = ev(page, '''() => {
            const b = document.querySelector('#net g').getBBox();
            return {w: Math.round(b.width/10)*10, h: Math.round(b.height/10)*10};
        }''')
        P('graph bbox w', pick(box, 'w'))
        P('graph bbox h', pick(box, 'h'))
        if pick(box, 'w') in (0, 'MISSING') or pick(box, 'h') in (0, 'MISSING'):
            fatal.append('graph bbox is empty')

        # --- the published copy must not show verse text ----------------------
        P('NRSV payload present', ev(page, '() => typeof window.NRSV !== "undefined"'))
        P('empty panel note', ev(page,
            '() => (document.querySelector(".panel .note")||{}).textContent?.slice(0,46) || "NONE"'))

        # --- clicking a passage ----------------------------------------------
        panel = ev(page, '''() => {
            const n = [...document.querySelectorAll('.node')]
                .find(g => g.getAttribute('aria-label') === 'Matthew 23:23');
            if (!n) return {found: false};
            n.dispatchEvent(new MouseEvent('click', {bubbles: true}));
            const a = document.querySelector('.ref a');
            const c = document.querySelector('.ref .chap');
            return {
                found: true,
                ref: a && a.textContent,
                verseHref: a && a.getAttribute('href'),
                chapterHref: c && c.getAttribute('href'),
                connections: document.querySelectorAll('.panel .link').length,
                heading: (document.querySelector('.panel h3')||{}).textContent
            };
        }''')
        for key, label in (('found', 'found node'), ('ref', 'ref'),
                           ('verseHref', 'verse href'), ('chapterHref', 'chapter href'),
                           ('connections', 'connections'), ('heading', 'heading')):
            P('panel %s' % label, pick(panel, key))
        if not pick(panel, 'found') or pick(panel, 'verseHref') in (None, 'MISSING'):
            fatal.append('clicking a passage produced no panel')

        # --- one pair, two arcs: the Q5 change --------------------------------
        P('edges on Matthew 9:9 to Mark 2:14', ev(page,
            '() => E.filter(e => (e[0]==="tithe:c1"&&e[1]==="tithe:c8")'
            '||(e[0]==="tithe:c8"&&e[1]==="tithe:c1")).length'))
        P('kinds on that pair', ev(page,
            '() => E.filter(e => (e[0]==="tithe:c1"&&e[1]==="tithe:c8")'
            '||(e[0]==="tithe:c8"&&e[1]==="tithe:c1")).map(e=>e[2]).sort().join(",")'))
        P('distinct arc lanes on that pair', ev(page,
            '() => new Set(edges.filter(e => (e.s.id==="tithe:c1"&&e.t.id==="tithe:c8")'
            '||(e.s.id==="tithe:c8"&&e.t.id==="tithe:c1")).map(e=>e.lane)).size'))

        # --- filtering still filters ------------------------------------------
        filt = ev(page, '''() => {
            const cb = document.querySelector('#clusters .row input');
            cb.checked = false; cb.dispatchEvent(new Event('change'));
            const hidden = document.querySelectorAll('.node.hide').length;
            cb.checked = true; cb.dispatchEvent(new Event('change'));
            return {hiddenWhenUnticked: hidden,
                    shownAgain: document.querySelectorAll('.node.hide').length};
        }''')
        P('filter hid', pick(filt, 'hiddenWhenUnticked'))
        P('filter restored', pick(filt, 'shownAgain'))
        if pick(filt, 'hiddenWhenUnticked') in (0, 'MISSING'):
            fatal.append('unticking a cluster hid nothing')

        # --- the zoom floor ---------------------------------------------------
        # There is nothing to see past the fitted view: further out is empty
        # canvas around a shrinking blob. Both the buttons and the wheel must
        # stop there, and zooming IN must still work.
        z = ev(page, '''() => {
            document.getElementById('zfit').click();
            const fitted = vs;
            for (let i = 0; i < 8; i++) document.getElementById('zout').click();
            const afterButtons = vs;
            for (let i = 0; i < 3; i++) svg.dispatchEvent(new WheelEvent('wheel',
                {deltaY: 200, clientX: 300, clientY: 300, bubbles: true, cancelable: true}));
            const afterWheel = vs;
            document.getElementById('zin').click();
            const zoomedIn = vs;
            document.getElementById('zfit').click();
            const r4 = x => Math.round(x * 10000) / 10000;
            return {
                floor: r4(minScale),
                fitted: r4(fitted),
                afterButtons: r4(afterButtons),
                afterWheel: r4(afterWheel),
                zoomedIn: r4(zoomedIn)
            };
        }''', {})
        for key in ('floor', 'fitted', 'afterButtons', 'afterWheel', 'zoomedIn'):
            P('zoom %s' % key, pick(z, key))
        floor, ab, aw = pick(z, 'floor'), pick(z, 'afterButtons'), pick(z, 'afterWheel')
        if not isinstance(floor, (int, float)) or ab < floor - 1e-6 or aw < floor - 1e-6:
            fatal.append('zoom-out went below the fitted floor: floor %s, buttons %s, wheel %s'
                         % (floor, ab, aw))

        # --- the chrome -------------------------------------------------------
        P('page heading', ev(page, '() => document.getElementById("hTitle").textContent'))
        P('arrangement group hidden', ev(page,
            '() => document.querySelector(".grp").classList.contains("hide")'))
        P('reset sits over the canvas', ev(page,
            '() => !!document.querySelector(".canvas > .reset.floating")'))
        P('era label font-size', ev(page,
            '() => getComputedStyle(document.querySelector(".eralab")).fontSize'))
        P('arc stroke-width states', ev(page,
            '() => { const e = edges.find(x => x.wa === "states");'
            ' return e && e.el.getAttribute("stroke-width"); }'))
        P('groups carrying a note', ev(page,
            '() => Object.values(CL).filter(c => c.note && c.note.length).length'))
        P('group row tooltips', ev(page,
            '() => [...document.querySelectorAll("#clusters .row")]'
            '.filter(r => r.title && r.title.length > 20).length'))

        # --- the motif axis ---------------------------------------------------
        P('motif rows', ev(page, '() => document.querySelectorAll("#motifs .row").length'))
        P('motif keys', ev(page,
            '() => (typeof MO !== "undefined" ? Object.keys(MO).join(",") : "NONE")'))
        P('motif nodes covered', ev(page,
            '() => (typeof MO === "undefined") ? -1 : new Set('
            'Object.values(MO).flatMap(o => o.nodes.split(" "))).size'))
        mo = ev(page, '''() => {
            // Clear any selection left by an earlier probe. Without this the
            // node picked further up keeps its own neighbours lit, and the
            // counts below measure selection dimming and motif dimming
            // together - which is stable, but is not what the label says.
            picked = null; hovered = null; draw();
            const row = [...document.querySelectorAll('#motifs .row')]
                .find(r => r.textContent.startsWith('Treasure'));
            if (!row) return {found: false};
            const cb = row.querySelector('input');
            cb.checked = true; cb.dispatchEvent(new Event('change'));
            const dimmed = document.querySelectorAll('.node.dim').length;
            const lit = document.querySelectorAll('.node:not(.dim):not(.hide)').length;
            const edgesDimmed = document.querySelectorAll('path.edge.dim').length;
            cb.checked = false; cb.dispatchEvent(new Event('change'));
            return {found: true, dimmed: dimmed, lit: lit,
                    edgesDimmed: edgesDimmed,
                    restored: document.querySelectorAll('.node.dim').length};
        }''', {})
        P('motif treasure dims', pick(mo, 'dimmed'))
        P('motif treasure lights', pick(mo, 'lit'))
        P('motif treasure dims edges', pick(mo, 'edgesDimmed'))
        P('motif unticked restores to', pick(mo, 'restored'))
        if pick(mo, 'found') is not True or pick(mo, 'lit') in (0, 'MISSING'):
            fatal.append('the motif filter lit nothing')

        # --- search -----------------------------------------------------------
        P('search "tithe" hides', ev(page, '''() => {
            const q = document.getElementById('q');
            q.value = 'tithe'; q.dispatchEvent(new Event('input'));
            const n = document.querySelectorAll('.node.hide').length;
            q.value = ''; q.dispatchEvent(new Event('input'));
            return n;
        }'''))

        browser.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

P('fatal', len(fatal))
for f in fatal:
    P('fatal reason', f[:150])
sys.exit(1 if fatal else 0)
