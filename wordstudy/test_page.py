"""Run the built Word Study page in headless Chromium and render every word's study panel.

    python test_page.py     # exits non-zero on any script error or panel that fails to render

The page is gated by running it, not by reading it (see ../savefile/HAZARDS.md: the concordagraph
shipped blank three times while every text check passed).
"""
import os, sys, json
from playwright.sync_api import sync_playwright

PAGE = "file:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "word-study.html").replace("\\", "/")
PROBE = """() => {
  let n = 0, errs = [];
  for (const v of VERSES) for (const w of v.words) {
    try { render(w.id); n++; if (!document.querySelector('.s-orig')) errs.push(w.id + ': no panel'); }
    catch (e) { errs.push(w.id + ': ' + e.message); }
  }
  const groups = [...document.querySelectorAll('.groups .g')];
  let shown = 0;
  for (const g of groups) { if (!g.disabled) { g.click(); shown += document.querySelectorAll('.verse').length; } }
  return {verses: VERSES.length, rendered: n, errors: errs, groups: groups.length, versesShownAcrossGroups: shown,
          englishPieces: document.querySelectorAll('.e').length, progress: document.getElementById('progress').textContent};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(PAGE)
    pg.wait_for_timeout(1500)
    r = pg.evaluate(PROBE)
    b.close()
print(json.dumps({k: (v[:10] if isinstance(v, list) else v) for k, v in r.items()}, ensure_ascii=False, indent=1))
print("page errors:", errors[:5])
bad = errors or r["errors"] or r["versesShownAcrossGroups"] != r["verses"]
print("FAILED" if bad else "PASSED - every word renders, every group shows its verses")
sys.exit(1 if bad else 0)
