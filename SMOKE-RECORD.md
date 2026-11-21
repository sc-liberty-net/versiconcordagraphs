# Smoke Baseline Record

Every change to `smoke-baseline.out` is recorded here with its cause, newest last.
Move the baseline only with the smoke-gate skill's `baseline_guard.py`, never by
overwriting the file.

## 16 Nov 2026: First Baseline

Recorded from the first run of `smoke_concordagraph.py`, adapted from the Taxes suite
for this topic: no motifs, no Word Study; pinch zoom, keyboard zoom, 44 px touch
controls, the first-visit gesture hint, and the height-only resize added. Proved
against the page as committed in 626d368 (before those changes): keyboard zoom, the
icons, the preview card and pinch all went red there, and the zoom buttons read 32 px.

## 2026-11-18 - baseline refreshed: smoke-baseline.out
cause: Back button in the details panel and draggable edges on both side columns (Ethan, 18 Nov): 15 new probe lines, no existing line moved. Proved against HEAD 92bdd6f, where the Back and resize probes went red.
moved: 0 changed, 15 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/0262951ad32e9d6c/8e68c5ec-effc-4133-93b4-9c1eba11a9d1/scratchpad/new.out -> smoke-baseline.out

## 2026-11-20 - baseline refreshed: smoke-baseline.out
cause: Readability pass O1-O8 (Ethan, 20 Nov): connection chips and body-ink notes, hidden passage names at the phone's fitted view, 44px touch filters, picked passage kept above the sheet, link-coloured Compare/Read. 8 new lines, none moved. Red on the committed page (HEAD 59012dc).
moved: 0 changed, 8 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/claude/0262951ad32e9d6c/8e68c5ec-effc-4133-93b4-9c1eba11a9d1/scratchpad/new.out -> smoke-baseline.out
