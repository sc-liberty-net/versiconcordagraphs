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
