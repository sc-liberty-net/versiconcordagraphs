"""make_icons.py - write the concordagraph's favicon, home-screen icons and link
preview card into icons/.

    python make_icons.py

The emblem (Ethan, 22 Oct 2026) is ten passages along the spine, three nested
arcs landing on them, and the outer arc, dashed gold, reaching the tenth: the
graph's own shape and the tithe's one in ten. Green is "the text states it",
gold "the text supports it", as on the page.

The preview card's arcs are the real ones: the script loads the built
concordagraph.html and reads every passage's place on the spine and every
connection's warrant from it, so the card is redrawn from the corpus each time
this runs. It prints no counts on the card, because a number typed into an
image is a number that drifts (HANDOFF.md: counts are generated, not typed).

Files written (all served beside the page, in its icons/ folder):
  favicon.svg            browser tab, any size
  favicon-32.png         browser tab, for browsers without SVG favicons
  apple-touch-icon.png   iPhone / iPad home screen, 180 px, full-bleed (iOS rounds it)
  icon-192.png, icon-512.png   Android home screen, via site.webmanifest
  site.webmanifest
  og-card.png            link preview, 1200 x 630
"""
import json, os, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'icons'
PAGE = ROOT / 'concordagraph.html'

SLATE, LIGHT, GREEN, GOLD = '#36454F', '#ECEFF1', '#5FBF9F', '#E0A552'


def emblem(rounded=True):
    """The emblem as SVG on a 64-unit square. rounded=False fills the square,
    for home-screen icons the phone rounds itself."""
    dots = [(10, 2.3), (14.8, 2.1), (19.6, 1.9), (24.4, 2.1), (29.2, 1.9),
            (34, 1.9), (38.8, 2.1), (43.6, 1.9), (48.2, 2.1)]
    circles = ''.join(f'<circle cx="{x}" cy="41.5" r="{r}"/>' for x, r in dots)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="{14 if rounded else 0}" fill="{SLATE}"/>'
        f'<path d="M10 41.5 A21.5 21.5 0 0 1 53 41.5" fill="none" stroke="{GOLD}" stroke-width="3.4" stroke-dasharray="5.2 3.4"/>'
        f'<path d="M14.8 41.5 A16.7 16.7 0 0 1 48.2 41.5" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        f'<path d="M24.4 41.5 A7.2 7.2 0 0 1 38.8 41.5" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        f'<g fill="{LIGHT}">{circles}</g>'
        f'<circle cx="53" cy="41.5" r="4.4" fill="{GOLD}"/>'
        '</svg>')


CARD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@600&family=Archivo:wght@400;600&display=swap">
<style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#1B2228}
.t{position:absolute;left:72px;top:64px;width:900px}
.k{display:flex;align-items:center;gap:16px;font:600 17px Archivo,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#96A4AD}
.k svg{width:56px;height:56px;box-shadow:0 0 0 1px #3C4750;border-radius:12px}
h1{font:600 80px/1.05 Spectral,Georgia,serif;color:#ECEFF1;margin:22px 0 14px}
p{font:400 25px/1.4 Archivo,sans-serif;color:#B4C0C8;margin:0;width:820px}
svg.arcs{position:absolute;left:0;top:0}
</style></head><body>
<svg class="arcs" width="1200" height="630" id="a"></svg>
<div class="t"><div class="k">__EMBLEM__Concordagraph</div>
<h1>Taxes, Tithes, &amp; Tribute</h1>
<p>Tax and tithe across the Bible, passage by passage. Every link names its kind and how much weight the text puts behind it.</p></div>
<script>
const D = __DATA__, NS = 'http://www.w3.org/2000/svg', a = document.getElementById('a');
const L = 56, R = 1144, Y = 560, lo = Math.min(...D.xs), hi = Math.max(...D.xs);
const X = x => L + (x - lo) / (hi - lo) * (R - L);
const el = (n, at) => { const e = document.createElementNS(NS, n); for (const k in at) e.setAttribute(k, at[k]); a.append(e); return e; };
const style = {spec: ['#8A9199', 1.3, '1.5 4'], supports: ['#E0A552', 1.7, ''], states: ['#5FBF9F', 2.1, '']};
for (const w of ['spec', 'supports', 'states']) for (const [s, t, wa] of D.edges) {
  if (wa !== w) continue;
  const x1 = X(Math.min(s, t)), x2 = X(Math.max(s, t)), h = 12 + Math.sqrt(x2 - x1) * 7.4;
  const [c, sw, dash] = style[w];
  el('path', {d: `M ${x1} ${Y} C ${x1} ${Y - h}, ${x2} ${Y - h}, ${x2} ${Y}`, fill: 'none', stroke: c,
              'stroke-width': sw, 'stroke-dasharray': dash, 'stroke-opacity': w === 'spec' ? .7 : .85});
}
el('line', {x1: L - 8, y1: Y, x2: R + 8, y2: Y, stroke: '#96A4AD', 'stroke-width': 1.5});
for (const x of D.xs) el('circle', {cx: X(x), cy: Y, r: 1.6, fill: '#ECEFF1'});
const nt = X(D.nt) - 6;
for (const [x1, x2, name] of [[L, nt - 6, 'Old Testament'], [nt + 6, R, 'New Testament']]) {
  el('path', {d: `M ${x1} ${Y + 14} v 8 H ${x2} v -8`, fill: 'none', stroke: '#96A4AD', 'stroke-width': 1.5});
  const tx = el('text', {x: (x1 + x2) / 2, y: Y + 48, 'text-anchor': 'middle', fill: '#B4C0C8',
                         'font-family': 'Archivo, sans-serif', 'font-size': 17, 'font-weight': 600});
  tx.textContent = name;
}
</script></body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'favicon.svg').write_text(emblem(True), encoding='utf-8')
    manifest = {
        'name': 'Taxes, Tithes, & Tribute', 'short_name': 'Tithe & Tax',
        'start_url': '../', 'display': 'browser',
        'background_color': '#EEF0F2', 'theme_color': SLATE,
        'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'}]}
    (OUT / 'site.webmanifest').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, px, rounded in (('favicon-32.png', 32, True), ('apple-touch-icon.png', 180, False),
                                  ('icon-192.png', 192, False), ('icon-512.png', 512, False)):
            pg = b.new_page(viewport={'width': px, 'height': px})
            pg.set_content('<style>html,body{margin:0;background:transparent}svg{display:block;width:%dpx;height:%dpx}</style>%s'
                           % (px, px, emblem(rounded)))
            pg.screenshot(path=str(OUT / name), omit_background=rounded)
            pg.close()

        pg = b.new_page()
        pg.goto(PAGE.resolve().as_uri()); pg.wait_for_timeout(800)
        data = pg.evaluate("""() => ({
            xs: nodes.map(n => n.ax),
            edges: edges.map(e => [e.s.ax, e.t.ax, e.wa]),
            nt: Math.min(...nodes.filter(n => n.ord >= BOOKS.indexOf(NT_FIRST)).map(n => n.ax)) })""")
        pg.close()
        card = CARD.replace('__EMBLEM__', emblem(True)).replace('__DATA__', json.dumps(data))
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        pg.set_content(card); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / 'og-card.png'))
        b.close()
    print(f"wrote {', '.join(sorted(f.name for f in OUT.iterdir()))}")
    print(f"card drawn from {len(data['xs'])} passages and {len(data['edges'])} connections")


if __name__ == '__main__':
    main()
