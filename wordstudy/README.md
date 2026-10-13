# Word Study — Taxes & Tithes

The concordagraph's passages in this project's own literal English (184 drafted; the 60 added on
13 Oct, kings, empires, inheritance and more tithe law, are not drafted yet), with the
KJV as supporting reference. Every word opens onto the Hebrew or Greek behind it: grammar, how
seven public-domain translations render it, the lexicons, the Textus Receptus reading (Greek), and
the Septuagint's Greek (Hebrew). Built 11-12 October 2026. Published as a private artifact:
https://claude.ai/artifact/DQw74wKDA56T6QWWQ8nPxT

## Run order

From this folder:

```
python extract.py     # data/<id>.json and digest/<id>.txt for every corpus node (reads, never edits, corpus_nodes.csv)
python check.py       # every authored/<id>.json against GUIDE.md's rules; must end "184 of 184 drafts pass"
python build.py       # word-study.html and ../wordstudy.js; reports drafted of total (184 of 244 on 13 Oct)
python test_page.py   # runs the page in Chromium, renders all 3,269 word panels; must end "PASSED"
```

`show.py <ids>` prints drafted English beside the KJV, for review.

## Files

| File | What it is |
|---|---|
| `GUIDE.md` | The drafting method and the **register** of fixed renderings. Read before changing any reading |
| `authored/<id>.json` | Our English (`en`), per-word synonyms, sense, notes and renderings (`words`), Septuagint pairing (`lxx`), Textus Receptus note (`tr_note`). The translation itself: commit these |
| `lexfix.json` | Corrections to the lexicon data: wrong-homonym entries hidden, mis-tagged dictionary forms fixed. Shown on the page |
| `sources.py` | Readers for STEPBible, Gesenius, BDB, Thayer, Swete, the translations; Greek and Hebrew grammar decoders (Hebrew by STEP's own TEHMC key) |
| `extract.py`, `build.py`, `check.py`, `test_page.py`, `template.html` | The pipeline |
| `embed.js` | The passage reading and word study inside the concordagraph; `build.py` prefixes it with the data to make `../wordstudy.js`. Its study functions follow `template.html`: keep the two in step |
| `data/`, `digest/`, `word-study.html` | Generated; not committed (see Licences) |

## Decisions already made

- Our literal English is the reading text; the KJV sits beneath it as supporting reference (Ethan, 12 Oct).
- Old Testament words always show the Septuagint's Greek (Ethan, 1 Oct).
- The register keeps apart what the original keeps apart: τελώνης "toll collector", φόρος
  "tribute", κῆνσος "census tax", δεκάτη "tenth"; נֶשֶׁךְ "interest", תַּרְבִּית "increase",
  מַשָּׁא "usury", the creditor verb נָשָׁה "exact". "The LORD" for the divine name.
- Matthew 23:23 and Luke 11:42 read identically except their last verb ("But these it was
  necessary to do, and those not to leave aside / neglect"), because their Greek does.
- Everything drafted is marked on the page as a draft; Ethan has not reviewed the readings.

## Licences, checked against the sources

- **STEPBible** (TAHOT, TAGNT, TBESH, TBESG): CC BY 4.0. Their licence allows including any part in
  software or publications without asking; credit "STEP Bible" linked to STEPBible.org; record
  changes (`lexfix.json`); do not redistribute the datasets themselves, which is why `data/` and
  `digest/` stay off GitHub. A page that quotes from them may be published.
- **Swete's Septuagint** (digital text): CC BY-SA 4.0. A public page quoting it must carry that
  licence and the credit in the footer.
- **KJV, the other six translations**: public domain. **NRSV**: never on any published page.

## Known gaps

- Luke 4:18-19: the Douay-Rheims divides these verses differently, so its renderings are left blank.
- Some Gesenius matches are wrong homonyms or part-entries (Room task 76); five are hidden via `lexfix.json`.
- `../STEP-email-draft.md` reports four tagging errors to STEP; Ethan has not sent it yet.
- The Strong's-tagged KJV (`../bible-sources/english/eng-kjv2006/`) is downloaded but not yet used:
  it could supply the KJV rendering of each word automatically, and the KJV's italic words.

## In the concordagraph (built 12 Oct)

Clicking a passage in `../concordagraph.html` shows our literal English with the KJV beneath and the
summary below; hovering a word shows its synonyms; selecting a word swaps the panel to its full study
("Back to the passage" returns). The data and code are `../wordstudy.js` (Ethan chose a separate file
over inlining, 12 Oct), loaded deferred with `onerror`, so without it the page shows summaries as before.
`../smoke_concordagraph.py` checks both: its first pass runs without `wordstudy.js`, its second with it,
at 1400x900 and 390x844.

Facts the work needed, checked 12 Oct:
- `../concordagraph.html` (104 KB) shows a passage in `renderNode(n)`; it already reads optional
  local verse text from `verses.js` through `<script src="verses.js" onerror="void 0">`.
- Concordagraph node ids are this module's slug plus the bare id (`tithe:k1`); Word Study ids are bare (`k1`).
- `word-study.html` is 4.8 MB; the concordagraph page is public and Ethan previews it from file:// in Firefox.
- The page is gated by `../check_page.py`, which fails if any smoke line moves. A UI change will move
  lines: re-record only with the guard and a cause (see `check_page.py`'s docstring), never by overwriting.
