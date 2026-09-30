# Standing rules for bible-sources

Read this before using anything in this folder. Credit and licence
terms for each source are in `README.md`.

## Gesenius: read on demand, never in bulk

Gesenius's *Hebrew and Chaldee Lexicon*, Tregelles translation (1857), is
one of our Hebrew sources and references. Consult it alongside BDB whenever
a claim rests on what a Hebrew word means. Where the two disagree, report
both; do not pick one silently.

**Look the word up first in `lexicons/gesenius/gesenius-entries.json`**,
built by `parse_gesenius.py` from our own page transcripts (2026-09-30; see
`README.md`, "Gesenius, parsed"). It is keyed to Strong's numbers, carries
each entry's page and scan link, and marks doubtful pairings `check: true`.
The transcripts were checked by script, and only a few pages by eye: where
an entry matters, or holds [?] marks, **the page scan decides.** This
replaces the decision of 2026-09-25 that there be no parsed copy, which was
made when the only text was the machine-read one.

The machine-read text in `lexicons/gesenius/` has garbled Hebrew and mixed
columns: use it only to search the English. To read an entry from the page
scan:

1. **Page image address.** Image n is at
   `https://archive.org/download/hebrewchaldeelex00geseuoft/page/n{n}_w1400.jpg`
   (n counts from 0). The lexicon's printed pages are Roman numerals, from I
   (the letter Aleph, image n20) to DCCCLXXXIV (image n903).
   **Image n = printed page + 19.** Checked: n470 is page CCCCLI.
2. **Finding the page.** Pages run in Hebrew alphabetical order. The
   running heads at the top of each page give its first and last word
   (n470 reads מדי–מה). Start from an estimate — page ≈ Strong's Hebrew
   number ÷ 8674 × 884 — and step forward or back by the running heads.
   The estimate can be off by 40 pages or more, so expect two to four
   images.
3. **Reading the entry.** Use the 1400-pixel image only to find the page.
   To read the entry, fetch the full-resolution image (the same address
   without `_w1400`, 2466×3396), cut it into four overlapping pieces (each
   column, top half and bottom half; Pillow is installed), and read the
   piece that holds the entry. Check the headword against BDB or Strong's
   before relying on the reading.
   **Only an Opus-class model reads the Hebrew.** A test on five pages
   (2026-09-25) found Haiku's Hebrew mostly invented. Sonnet matched Opus
   on the English, but it swapped Hebrew letters and invented words without
   marking any doubt. Even Opus supplied expected vowel points unless told
   not to, so give any helper that rule in writing: transcribe only the
   points you can see, and mark doubt with [?].
4. **Citing it.** Give the printed page and the image link, e.g.
   *Gesenius (Tregelles 1857), p. CCCCLI* —
   `https://archive.org/details/hebrewchaldeelex00geseuoft/page/n470/mode/1up`.
   Gesenius is public domain, so quoting it is fine.
5. **Keep what you read.** Add each entry read to
   `lexicons/gesenius/lookups.md`: Strong's number, headword, printed page,
   image number, and the entry as read. Check that file first, so a page is
   never read twice. Every page is transcribed in
   `lexicons/gesenius/transcript/` (`n###.txt`, images 20–903, listed in
   `PROGRESS.md`; finished 2026-09-29). `gesenius_pages.py` prepares crops
   and checks a transcript; re-reading a page with the lean reader
   (`.claude/agents/gesenius-reader.md`) costs about $0.50 of plan usage
   per page. If you correct a transcript, rerun `python parse_gesenius.py`.

Never download the full scan (110 MB PDF, 675 MB images).
