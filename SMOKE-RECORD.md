# Smoke baseline record

Every line `smoke_concordagraph.py` prints is gated against `smoke-baseline.out`.
A line that moves fails the run until the cause is written here. Append only —
each entry is the evidence for why a number is what it is.

Move the baseline with `baseline_guard.py`, never by overwriting the file:

```
python <skills>/smoke-gate/scripts/baseline_guard.py \
    --baseline smoke-baseline.out --new new.out \
    --cause "<what changed, and why the new value is right>" \
    --record SMOKE-RECORD.md
```

---

## 2026-09-25 — first baseline, 32 lines

Recorded after the page shipped blank three times running.

**The defect this exists to catch.** The Bible Hub link change declared
`const HUB` for its slug overrides. That identifier was already taken further up
the same inline script for the hub *cluster*. A duplicate `const` is a **parse**
error, so the whole script died before its first line: no graph, no panel, no
filters, on a page whose HTML contained every string anyone thought to check.

Three separate verifications passed against that broken page — the biblehub URLs
were present, 25 of 25 book slugs resolved live, `META` held the right counts.
All three read the served HTML **as text**. None of them ran it. Ethan found the
blank page by opening it.

**Proved before it was trusted.** `prove_smoke.py` reintroduces the exact `HUB`
collision into a copy of the page and asserts the suite fails on it:

```
RED   exit 1, console errors: 1, drawn nodes: 0, drawn arcs: 0, fatal: 4
GREEN exit 0, console errors: 0, drawn nodes: 164, drawn arcs: 199, fatal: 0
```

The first version of the suite *crashed* on the red page rather than reporting —
`#net g` does not exist when the script has not run, so `getBBox()` threw and the
suite died halfway through its own output. A crashed suite gives the gate nothing
to diff. Fixed by routing every probe through `ev()` and every dict read through
`pick()`.

**The baseline at this commit:** 164 nodes, 199 edges, 25 books, 16 clusters,
3 warrants, 3 kinds. Matthew 23:23 shows 12 connections. Matthew 9:9 to
Mark 2:14 carries 2 edges of kinds `con,lex` on 2 distinct arc lanes — the
first use of the Q5 change. `NRSV payload present: False`, because the suite
runs against an isolated copy with no `verses.js`, which is what gets published.

**Guards confirmed working at record time:** `smoke_diff.py` passes on an
identical run and fails on a single hand-edited digit (`drawn nodes: 164` →
`163`). `dead_selector_lint.py` checks 22 call sites and 19 distinct tokens
against the page and finds no dead selector.

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: treasure and metal material added: 2 clusters, 20 nodes, 24 edges. Haggai is a new book, hence one more tick and label; the two new clusters add two rail rows; bbox height grows with the extra arcs. Search still matches the same 8 verses (184-176 = 164-156 = 8).
moved: 13 changed, 0 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/new.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: motif filter added: a fourth rail group keyed on Strong's lemmas rather than on cluster. Seven new gated lines cover it. Ticking Treasure dims 170 and lights 14, which is exactly the node list corpus_motifs.csv records for that motif.
moved: 0 changed, 7 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/mo.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: UI pass: zoom clamped to the fitted view, title capitalised, dead arrangement control hidden, era label 10.5px to 34px, arcs thinned, group notes added for tooltips, reset moved over the canvas, motifs became pills in a bar. Twelve new gated lines. The tax motif lost Hebrews 7:3 because telos means end as well as toll.
moved: 2 changed, 12 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/ui.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: second UI pass: clicking a group name shows its passages in the panel, select-all and clear buttons above the group list, the opening view backed off by a 0.86 fit margin, and the header paragraph moved into an About dialog. Zoom floor moves 0.3271 to 0.2812 because the margin applies to the floor as well - the two are the same view by design.
moved: 5 changed, 14 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/ui2.out -> smoke-baseline.out

## 2026-10-12 - baseline refreshed: smoke-baseline.out
cause: Word Study in the concordagraph (12 Oct 2026): a passage shows this project's literal English with the KJV beneath, hover synonyms and the full word study on click. 30 new lines from a second smoke pass that loads the page with wordstudy.js at 1400x900 and 390x844; no existing line moved (the first pass, without wordstudy.js, is the page's fallback).
moved: 0 changed, 30 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan, 13 Oct: hovering an arc while a group or passage is selected no longer replaces the selection's highlight (group stays 92/44 lit; the hovered arc is drawn full, .ehov), and 'Trace a motif' has a real tooltip on hover, focus and tap instead of a title attribute. 7 new lines; on the previous page (da03bde) the hover line reads 2/1 and the tooltip lines fail. No existing line moved.
moved: 0 changed, 7 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new2.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan's /title-case, 13 Oct: titles and labels shown in Title Case with & (a titleCase() display helper; the CSV names are unchanged). Three lines change case only: the panel heading, the group panel's ref and tag. The suite's group probe now finds 'Tithe Statutes', the name as displayed.
moved: 3 changed, 0 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new3.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan's O1-O3, 13 Oct: 60 passages and 76 connections added; two new groups (kings: Kings and their levies, 20 incl. 1 Samuel 8:15 moved from anchor; inherit: Portion and inheritance, 20); 13 empires passages in imperial; Deuteronomy 14:22-28 and Malachi 3:10 in anchor (18-1+8=25). 244 nodes, 299 edges, 38 books (26 + 12 new; ticks = books + 1), 20 groups. Dependent counts follow: treasure motif still lights 14 (dims 244-14, edges 299-9); search 'tithe' leaves 13 (5 new summaries use the word); anchor group lit 119/60 and held during arc hover; bbox h and zoom move with the taller arc field.
moved: 29 changed, 0 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new4.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Word Study readings drafted for the 60 passages added 13 Oct (kings, empires, inheritance, Deuteronomy 14:22-28, Malachi 3:10): wordstudy.js now carries 244 of 244. Only the two 'study ... passages' lines move.
moved: 2 changed, 0 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new5.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan's G4 (book labels), 13 Oct: labels counter-scaled to stay 11.5px on screen at any zoom and thinned where they would overlap (20 of 38 at the fitted desktop view; old page: all 38 at an 8px box). Fit now measures the graph without the labels (graphBBox), so the zoom lines do not move; the suite's own bbox includes the screen-size labels and grows 2490x1480 -> 2530x1540. Two new lines, red on the previous page.
moved: 2 changed, 2 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new6.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan, 13 Oct: on phones (under 768px) the graph is turned 90 degrees clockwise, Genesis at the top, arcs bulging right and squeezed to 0.55, text upright; it opens fitted to the width at Genesis (zoom 0.37 against 0.13 before, 23 labels against 13), the fit button shows it whole. Four new phone lines, which read NONE/False/0.13/13 on the previous page. No desktop line moved.
moved: 0 changed, 4 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new7.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Ethan's C2 (detail panel), 13 Oct: the panel grows with the window, clamp(320px, 28vw, 440px), 392px at 1400 (was 320), so the graph is 72px narrower and every zoom line scales by 772/844 (0.2816 -> 0.2575); the suite's bbox grows slightly with the counter-scaled labels at the smaller zoom. On phones the panel is a bottom sheet. Two new lines (desktop panel column 392px; phone panel sheet on screen), which read 320px / column 390px on the previous page.
moved: 7 changed, 2 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new8.out -> smoke-baseline.out

## 2026-10-13 - baseline refreshed: smoke-baseline.out
cause: Bottom-sheet tap leak, 13 Oct: two taps on the sheet handle opened a word's study, because the handle snapped away before the tap's click fired. Fixed in 6e0b788 (taps act on click). New line reads True on e384610 (the leaking version) and False now.
moved: 0 changed, 1 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new9.out -> smoke-baseline.out

## 2026-10-14 - baseline refreshed: smoke-baseline.out
cause: Ethan's A4 (group names), 14 Oct: group rows lose their hover text by design (20 -> 0; it showed only after a still pointer and never on a phone, and the panel shows a group's note on click). The name shows 'Show ->' on hover and focus, and the selected group's row is marked. The groups fold away on phones (closed by default), open on desktop. Three new lines, which read NONE / 0 / NONE on the previous page.
moved: 1 changed, 3 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new10.out -> smoke-baseline.out

## 2026-10-14 - baseline refreshed: smoke-baseline.out
cause: Phone checklist fixes F1/F3/F6, 14 Oct: a finger drag left the click-swallow flag set and ate the next tap (now cleared on every press); a touch tap that misses selects the nearest passage within 22px (it used to select an arc); the readout no longer stays lit after a tap (cleared on touch lift, and focus lights it only for keyboard focus). Three new phone lines, which read False / an arc / True on the previous page. No desktop line moved.
moved: 0 changed, 3 new, 0 gone (0 allowed, not counted)
source: C:\Users\ethan\AppData\Local\Temp/claude/C--Users-ethan-Desktop-Biblography/4247ac7d-27d5-45cb-9f65-2e89e9d758c8/scratchpad/new11.out -> smoke-baseline.out

## 2026-10-21 - baseline refreshed: smoke-baseline.out
cause: Ethan, 21 Oct: How Strong Is The Link, What Kind Of Link and the motifs now fold like the groups (open on desktop, closed on phones), with counts. Three new lines; they read NONE on the previous page. The phone motif-tip tap still reads shown: it went to hidden once the folds made the phone page short (a tap at the page bottom nudged the scroll and the click missed), and the help button now acts on touchend.
moved: 0 changed, 3 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/C--Users-ethan-Desktop-Biblography/17e8bdf6-db9e-4e8a-bb09-e91292949cb3/scratchpad/new11.out -> smoke-baseline.out

## 2026-10-21 - baseline refreshed: smoke-baseline.out
cause: Ethan, 21 Oct: (1) the hidden 'by group' network view and its Arrangement control removed (relax() cost ~60 ms per load, ~250 ms at 4x throttle): 'rail group lens hidden' and 'arrangement group hidden' gone, 'rail group lens gone' and 'first rail section: Find A Passage' new. (2) Old/New Testament brackets past the book names replace the 'New Testament begins' label: 'era label font-size' gone, two bracket lines new (both read NONE on the previous page). The brackets are drawn at screen offsets, so graph bbox h grows 1550 -> 1650 at the fitted zoom; fit() now reserves 72 px for them on a phone, so the phone graph opens at zoom 0.30 (was 0.37) with 22 book names shown (was 23). Desktop zoom unchanged.
moved: 3 changed, 4 new, 3 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/C--Users-ethan-Desktop-Biblography/17e8bdf6-db9e-4e8a-bb09-e91292949cb3/scratchpad/new12.out -> smoke-baseline.out

## 2026-10-22 - baseline refreshed: smoke-baseline.out
cause: Ethan, 22 Oct: favicon, home-screen icons and link preview card added (make_icons.py writes icons/). Three new lines: every icon the head links exists beside the page, the card is 1200x630, and the og:image tag names the live folder. Proved: a copy of the page without icons/ reports all four missing and the card MISSING; the previous page reports 0 linked and NONE.
moved: 0 changed, 3 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/C--Users-ethan-Desktop-Biblography/17e8bdf6-db9e-4e8a-bb09-e91292949cb3/scratchpad/new14.out -> smoke-baseline.out

## 2026-10-22 - baseline refreshed: smoke-baseline.out
cause: Audit F3, 22 Oct: the desktop pass counted console errors only right after load, so a handler that threw during the probes (wheel, filters, groups, About) went unseen and the run passed. New line counts errors raised during the probes and makes each one fatal. Proved: a copy whose wheel handler throws after its first call printed 'console errors during the probes: 2' and exited 1; the real page prints 0 and exits 0.
moved: 0 changed, 1 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/C--Users-ethan-Desktop-Biblography/17e8bdf6-db9e-4e8a-bb09-e91292949cb3/scratchpad/new15.out -> smoke-baseline.out
