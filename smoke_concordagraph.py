"""smoke_concordagraph.py - load the built page in a real browser and print
what it actually produced. Adapted on 16 Nov 2026 from the Taxes, Tithes, &
Tribute suite (../Biblography/smoke_concordagraph.py, which explains WHY a page
must be run, not read). This topic has no motifs and no Word Study, so those
probes are gone; the phone probes gained pinch zoom.

Every line is `label: value` and prints the population it examined, not a
verdict. check_page.py gates every line against smoke-baseline.out.

The page is copied to a temporary directory WITHOUT verses.js, so what runs is
the published page - references and summaries only.

    python smoke_concordagraph.py
    python smoke_concordagraph.py --page other.html

Exit 0 if the page ran, 1 if it did not, or if a fatal probe failed.
"""
import sys, os, json, shutil, tempfile, argparse

sys.stdout.reconfigure(encoding='utf-8')

ap = argparse.ArgumentParser()
ap.add_argument('--page', default='concordagraph.html')
args = ap.parse_args()
if not os.path.exists(args.page):
    sys.exit('not found: %s' % args.page)

from playwright.sync_api import sync_playwright

tmp = tempfile.mkdtemp(prefix='concordagraph-smoke-')
shutil.copy(args.page, os.path.join(tmp, 'index.html'))
base = os.path.dirname(os.path.abspath(args.page))
if os.path.isdir(os.path.join(base, 'icons')):
    shutil.copytree(os.path.join(base, 'icons'), os.path.join(tmp, 'icons'))
url = 'file:///' + os.path.join(tmp, 'index.html').replace('\\', '/')

errors, fatal = [], []
HUB_REF = 'John 18:36'
GROUP = 'Asking For A King'


def P(label, value):
    print('%s: %s' % (label, value))


def ev(page, expr, default='UNAVAILABLE', arg=None):
    """Evaluate in the page; a dead page degrades to a printed value."""
    try:
        return page.evaluate(expr, arg) if arg is not None else page.evaluate(expr)
    except Exception as exc:
        return '%s (%s)' % (default, str(exc).splitlines()[0][:60])


def pick(obj, key):
    return obj.get(key, 'MISSING') if isinstance(obj, dict) else obj


def real_errors(lst):
    return [e for e in lst if 'verses.js' not in e and 'wordstudy.js' not in e
            and 'Failed to load resource' not in e]


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append('pageerror: %s' % e))
        page.goto(url, wait_until='load')
        page.wait_for_timeout(1200)

        real = real_errors(errors)
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

        rail = ev(page, '''() => ({
            clusters: document.querySelectorAll('#clusters .row').length,
            warrants: document.querySelectorAll('#warrants .row').length,
            kinds: document.querySelectorAll('#types .row').length,
            motifs: document.querySelectorAll('#motifs .row').length
        })''')
        for k in ('clusters', 'warrants', 'kinds', 'motifs'):
            P('rail %s' % k, pick(rail, k))
        P('group names', ev(page,
            '() => [...document.querySelectorAll("#clusters .gname")].map(g => g.textContent).join(" | ")'))

        P('header', ev(page, '() => document.getElementById("hSub").textContent.slice(0,64)'))
        P('title', page.title())
        P('page heading', ev(page, '() => document.getElementById("hTitle").textContent'))

        box = ev(page, '''() => {
            const b = document.querySelector('#net g').getBBox();
            return {w: Math.round(b.width/10)*10, h: Math.round(b.height/10)*10};
        }''')
        P('graph bbox w', pick(box, 'w'))
        P('graph bbox h', pick(box, 'h'))
        if pick(box, 'w') in (0, 'MISSING') or pick(box, 'h') in (0, 'MISSING'):
            fatal.append('graph bbox is empty')

        bl = ev(page, '''() => {
            const shown = [...document.querySelectorAll('.booklab')]
                .filter(l => getComputedStyle(l).display !== 'none');
            return {shown: shown.length,
                    px: shown.length ? Math.round(shown[0].getBoundingClientRect().height) : 0};
        }''')
        P('book labels shown at fit', pick(bl, 'shown'))
        P('book label height on screen px', pick(bl, 'px'))

        # --- the published copy must not show verse text ----------------------
        P('NRSV payload present', ev(page, '() => typeof window.NRSV !== "undefined"'))

        # --- clicking the hub passage ----------------------------------------
        panel = ev(page, '''() => {
            const n = [...document.querySelectorAll('.node')]
                .find(g => g.getAttribute('aria-label') === '%s');
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
        }''' % HUB_REF)
        for key, label in (('found', 'found node'), ('ref', 'ref'),
                           ('verseHref', 'verse href'), ('chapterHref', 'chapter href'),
                           ('connections', 'connections'), ('heading', 'heading')):
            P('panel %s' % label, pick(panel, key))
        if not pick(panel, 'found') or pick(panel, 'verseHref') in (None, 'MISSING'):
            fatal.append('clicking a passage produced no panel')
        ev(page, '() => { picked = null; hovered = null; render(); draw(); }')

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

        # --- the zoom floor, and keyboard zoom --------------------------------
        z = ev(page, '''() => {
            document.getElementById('zfit').click();
            const fitted = vs, floorThen = minScale;
            for (let i = 0; i < 8; i++) document.getElementById('zout').click();
            const afterButtons = vs;
            for (let i = 0; i < 3; i++) svg.dispatchEvent(new WheelEvent('wheel',
                {deltaY: 200, clientX: 300, clientY: 300, bubbles: true, cancelable: true}));
            const afterWheel = vs;
            document.getElementById('zin').click();
            const zoomedIn = vs;
            document.getElementById('zfit').click();
            document.body.dispatchEvent(new KeyboardEvent('keydown', {key: '+', bubbles: true}));
            const keyIn = vs > fitted;
            document.body.dispatchEvent(new KeyboardEvent('keydown', {key: '0', bubbles: true}));
            const keyFit = Math.abs(vs - fitted) < 1e-6;
            const r4 = x => Math.round(x * 10000) / 10000;
            return {floor: r4(floorThen), fitted: r4(fitted), afterButtons: r4(afterButtons),
                    afterWheel: r4(afterWheel), zoomedIn: r4(zoomedIn), keyIn, keyFit};
        }''', {})
        for key in ('floor', 'fitted', 'afterButtons', 'afterWheel', 'zoomedIn', 'keyIn', 'keyFit'):
            P('zoom %s' % key, pick(z, key))
        floor, ab, aw = pick(z, 'floor'), pick(z, 'afterButtons'), pick(z, 'afterWheel')
        if not isinstance(floor, (int, float)) or ab < floor - 1e-6 or aw < floor - 1e-6:
            fatal.append('zoom-out went below the fitted floor')
        if pick(z, 'keyIn') is not True or pick(z, 'keyFit') is not True:
            fatal.append('keyboard zoom did not work')

        # --- icons and the link preview card ---------------------------------
        heads = ev(page, '''() => [...document.querySelectorAll('link[rel~="icon"], link[rel="apple-touch-icon"], link[rel="manifest"]')]
            .map(l => l.getAttribute('href'))''')
        missing = [h for h in (heads if isinstance(heads, list) else []) if not os.path.isfile(os.path.join(base, h))]
        P('head icon links', '%d linked, %s' % (len(heads) if isinstance(heads, list) else 0,
                                               'all present' if not missing else 'missing ' + ', '.join(missing)))
        if missing or not heads:
            fatal.append('icon files missing: %s' % missing)
        card = os.path.join(base, 'icons', 'og-card.png')
        if os.path.isfile(card):
            with open(card, 'rb') as f:
                hdr = f.read(24)
            P('preview card size', '%dx%d' % (int.from_bytes(hdr[16:20], 'big'), int.from_bytes(hdr[20:24], 'big')))
        else:
            P('preview card size', 'MISSING')
            fatal.append('preview card missing')
        P('preview card tag', ev(page, '''() => (document.querySelector('meta[property="og:image"]')||{}).content || "NONE"'''))
        P('preview url tag', ev(page, '''() => (document.querySelector('meta[property="og:url"]')||{}).content || "NONE"'''))
        P('reset sits over the canvas', ev(page,
            '() => !!document.querySelector(".canvas > .reset.floating")'))
        P('testament brackets', ev(page, '''() => {
            const t = [...document.querySelectorAll('.testament .tlab')];
            return t.map(x => x.textContent).join(' / ') || 'NONE'; }'''))
        P('gesture hint on desktop', ev(page,
            '() => { const h = document.getElementById("gestureHint"); return h ? (h.hidden ? "hidden" : "shown") : "NONE"; }'))

        # --- the About panel --------------------------------------------------
        ab = ev(page, '''() => {
            const dlg = document.getElementById('about');
            document.getElementById('aboutBtn').click();
            const opened = !dlg.hidden;
            const headings = document.querySelectorAll('#about h3').length;
            document.getElementById('scrim').click();
            const closedByScrim = dlg.hidden;
            document.getElementById('aboutBtn').click();
            document.getElementById('aboutX').click();
            return {opened, headings, closedByScrim, closedByX: dlg.hidden};
        }''', {})
        for key, label in (('opened', 'opens'), ('closedByScrim', 'closes on click-off'),
                           ('closedByX', 'closes on X'), ('headings', 'sections')):
            P('about %s' % label, pick(ab, key))
        if pick(ab, 'opened') is not True or pick(ab, 'closedByX') is not True:
            fatal.append('the About panel does not open and close')

        # --- select all / clear, and a group by its name ----------------------
        gr = ev(page, '''() => {
            document.getElementById('clNone').click();
            const hiddenAfterClear = document.querySelectorAll('.node.hide').length;
            document.getElementById('clAll').click();
            const hiddenAfterAll = document.querySelectorAll('.node.hide').length;
            const gn = [...document.querySelectorAll('#clusters .gname')]
                .find(g => g.textContent === '%s');
            if (!gn) return {found: false};
            const tickBefore = gn.parentElement.querySelector('input').checked;
            gn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            const out = {
                found: true, hiddenAfterClear, hiddenAfterAll,
                tickUnchanged: gn.parentElement.querySelector('input').checked === tickBefore,
                tag: (document.querySelector('.panel .tag') || {}).textContent,
                rows: document.querySelectorAll('.panel .link').length,
                lit: document.querySelectorAll('.node.lit').length
            };
            gn.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            out.deselects = !document.querySelector('.panel .link');
            return out;
        }''' % GROUP, {})
        for key, label in (('found', 'found'), ('hiddenAfterClear', 'clear hides'),
                           ('hiddenAfterAll', 'select all hides'),
                           ('tickUnchanged', 'name click leaves tick alone'),
                           ('tag', 'panel tag'), ('rows', 'panel rows'), ('lit', 'lights'),
                           ('deselects', 'second click deselects')):
            P('group %s' % label, pick(gr, key))
        if pick(gr, 'rows') in (0, 'MISSING') or pick(gr, 'tickUnchanged') is not True:
            fatal.append('clicking a group name did not show its passages cleanly')

        # --- search -----------------------------------------------------------
        P('search "sword" hides', ev(page, '''() => {
            const q = document.getElementById('q');
            q.value = 'sword'; q.dispatchEvent(new Event('input'));
            const n = document.querySelectorAll('.node.hide').length;
            q.value = ''; q.dispatchEvent(new Event('input'));
            return n;
        }'''))
        P('desktop overflowX', ev(page, '() => document.documentElement.scrollWidth - innerWidth'))

        after = real_errors(errors)[len(real):]
        P('console errors during the probes', len(after))
        for e in after:
            P('console error', e[:150])
            fatal.append('desktop probes: %s' % e)

        # --- the phone: real touch through CDP --------------------------------
        ctx = browser.new_context(viewport={'width': 390, 'height': 844},
                                  is_mobile=True, has_touch=True)
        wp = ctx.new_page()
        werr = []
        wp.on('console', lambda m: werr.append(m.text) if m.type == 'error' else None)
        wp.on('pageerror', lambda e: werr.append('pageerror: %s' % e))
        wp.goto(url, wait_until='load')
        wp.wait_for_timeout(1500)
        pre = 'phone '
        tg = ev(wp, '''() => {
            const b = document.querySelector('#net g').getBBox();
            return {turned: typeof VERT !== 'undefined' ? VERT : 'NONE', taller: b.height > b.width};
        }''')
        P(pre + 'graph turned', pick(tg, 'turned'))
        P(pre + 'graph taller', pick(tg, 'taller'))
        P(pre + 'gesture hint on first visit', ev(wp,
            '() => { const h = document.getElementById("gestureHint"); return h ? (h.hidden ? "hidden" : h.textContent) : "NONE"; }'))
        P(pre + 'zoom button size px', ev(wp,
            '() => [...document.querySelectorAll(".zoom button")].map(b => Math.round(b.getBoundingClientRect().width) + "x" + Math.round(b.getBoundingClientRect().height)).join(" ")'))
        P(pre + 'overflowX', ev(wp, '() => document.documentElement.scrollWidth - innerWidth'))
        try:
            cdp = wp.context.new_cdp_session(wp)
            T = lambda kind, pts: cdp.send('Input.dispatchTouchEvent', {'type': kind,
                'touchPoints': [{'x': x, 'y': y, 'id': i} for i, (x, y) in enumerate(pts)]})
            ev(wp, "() => document.querySelector('.stage').scrollIntoView()")
            wp.wait_for_timeout(300)
            sx, sy = ev(wp, "() => { const r = document.querySelector('svg#net').getBoundingClientRect(); return [r.left + r.width * 0.5, r.top + r.height * 0.5]; }")
            # one finger drags the graph, and the hint goes on that first touch
            v0 = ev(wp, '() => [vx, vy, vs]')
            T('touchStart', [(sx, sy)])
            for k in range(1, 10):
                T('touchMove', [(sx, sy - 8 * k)])
            T('touchEnd', [])
            wp.wait_for_timeout(500)
            v1 = ev(wp, '() => [vx, vy, vs]')
            P(pre + 'one-finger drag moves the graph', v1[1] != v0[1] and v1[2] == v0[2])
            P(pre + 'gesture hint after first touch', ev(wp,
                '() => { const h = document.getElementById("gestureHint"); return h ? (h.hidden ? "hidden" : "shown") : "NONE"; }'))
            # two fingers spread apart: the scale grows, about the midpoint
            s0 = ev(wp, '() => vs')
            gpt = ev(wp, '''([x, y]) => { const r = svg.getBoundingClientRect();
                return [(x - r.left - vx) / vs, (y - r.top - vy) / vs]; }''', arg=[sx, sy])
            T('touchStart', [(sx, sy - 30), (sx, sy + 30)])
            for k in range(1, 11):
                T('touchMove', [(sx, sy - 30 - 9 * k), (sx, sy + 30 + 9 * k)])
            wp.wait_for_timeout(100)
            s1 = ev(wp, '() => vs')
            gpt1 = ev(wp, '''([x, y]) => { const r = svg.getBoundingClientRect();
                return [(x - r.left - vx) / vs, (y - r.top - vy) / vs]; }''', arg=[sx, sy])
            T('touchEnd', [])
            wp.wait_for_timeout(500)
            ratio = round(s1 / s0, 1) if isinstance(s1, (int, float)) and isinstance(s0, (int, float)) and s0 else 'NONE'
            P(pre + 'pinch out zoom ratio', ratio)
            held = (isinstance(gpt, list) and isinstance(gpt1, list)
                    and abs(gpt[0] - gpt1[0]) < 2 and abs(gpt[1] - gpt1[1]) < 2)
            P(pre + 'pinch keeps the point under the fingers', held)
            P(pre + 'pinch selects nothing', ev(wp, '() => !picked'))
            if not isinstance(ratio, float) or ratio < 2.5 or not held:
                fatal.append('pinch did not zoom in on a phone')
            # two fingers pinch in: back down, never under the floor
            T('touchStart', [(sx, sy - 120), (sx, sy + 120)])
            for k in range(1, 11):
                T('touchMove', [(sx, sy - 120 + 11 * k), (sx, sy + 120 - 11 * k)])
            T('touchEnd', [])
            wp.wait_for_timeout(500)
            P(pre + 'pinch in zooms out', ev(wp, '() => vs < %r' % s1))
            T('touchStart', [(sx, sy - 120), (sx, sy + 120)])
            for k in range(1, 11):
                T('touchMove', [(sx, sy - 120 + 11 * k), (sx, sy + 120 - 11 * k)])
            T('touchEnd', [])
            wp.wait_for_timeout(500)
            P(pre + 'pinch stops at the floor', ev(wp, '() => vs >= minScale - 1e-9'))
            # a tap on a dot opens the sheet
            ev(wp, "() => document.getElementById('zfit').click()")
            ev(wp, '() => { picked = null; render(); draw(); }')
            wp.wait_for_timeout(300)
            d = ev(wp, '''() => { const st = document.querySelector('svg#net').getBoundingClientRect();
                const c = nodes.map(n => ({n, r: n.circle.getBoundingClientRect()}))
                    .filter(o => o.r.top > st.top + 80 && o.r.bottom < st.top + 300);
                const o = c[Math.floor(c.length / 2)];
                return {x: o.r.left + o.r.width / 2, y: o.r.top + o.r.height / 2}; }''')
            for _ in range(2):
                T('touchStart', [(d['x'], d['y'])]); T('touchEnd', [])
                wp.wait_for_timeout(500)
                if ev(wp, '() => !!picked'):
                    break
            P(pre + 'tap selects', ev(wp, '() => !!picked'))
            P(pre + 'sheet', ev(wp, '''() => {
                const p = document.getElementById('panel'), r = p.getBoundingClientRect();
                return getComputedStyle(p).position === 'fixed'
                    ? 'sheet ' + (r.top < innerHeight - 40 ? 'on screen' : 'off screen')
                    : 'column ' + Math.round(r.width) + 'px'; }'''))
            ev(wp, '() => { picked = null; render(); draw(); }')
            wp.wait_for_timeout(400)
            T('touchStart', [(d['x'] + 12, d['y'])]); T('touchEnd', [])
            wp.wait_for_timeout(500)
            P(pre + 'near-miss tap selects', ev(wp,
                "() => !picked ? 'nothing' : picked.ref ? 'a passage' : picked.s ? 'an arc' : 'other'"))
            ev(wp, '() => { picked = null; render(); draw(); }')
            # the address bar sliding away changes only the height: the view must stay
            ev(wp, "() => document.getElementById('zin').click()")
            before = ev(wp, '() => [vx, vy, vs].map(x => Math.round(x))')
            wp.set_viewport_size({'width': 390, 'height': 760})
            wp.wait_for_timeout(300)
            P(pre + 'height-only resize keeps the zoom', ev(wp, '() => [vx, vy, vs].map(x => Math.round(x))') == before)
            wp.set_viewport_size({'width': 390, 'height': 844})
        except Exception as exc:
            P(pre + 'touch probe failed', str(exc).splitlines()[0][:80])
            fatal.append('phone touch probe failed')
        real2 = real_errors(werr)
        P(pre + 'console errors', len(real2))
        for e in real2:
            fatal.append('phone: %s' % e)
        ctx.close()

        browser.close()
finally:
    shutil.rmtree(tmp, ignore_errors=True)

P('fatal', len(fatal))
for f in fatal:
    P('fatal reason', f[:150])
sys.exit(1 if fatal else 0)
