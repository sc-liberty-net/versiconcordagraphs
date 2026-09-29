# bible-sources

Original-language texts and lexicons for building our own translation.
Downloaded 2026-09-25. Nothing here is committed except this README,
`RULES.md`, `parse_thayer.py` and `.gitignore`.

Standing rules for using these sources, including how to consult
Gesenius, are in `RULES.md`.

A translation we write from these sources is our own work. The sources
only put conditions on the sources themselves: credit where a licence asks
for it, and share-alike or GPL terms if we publish a changed copy of a
dataset that carries them.

## Quick answer: who must be credited

| Must credit | Wording | Where it applies |
|---|---|---|
| SBL and Logos | "Copyright 2010 by the Society of Biblical Literature and Logos Bible Software", CC BY 4.0 | Any use of the SBLGNT text or apparatus |
| STEP Bible | "STEP Bible", linked to www.STEPBible.org, CC BY 4.0 | Anything built from `stepbible/` |
| Open Scriptures Hebrew Bible | "Open Scriptures Hebrew Bible", CC BY 4.0 | Anything using OSHB lemma or morphology data |
| unfoldingWord BDB-Enhanced | link to github.com/unfoldingWord/Brown-Driver-Briggs-Enhanced, CC BY | Anything using their corrections or additions to BDB |
| Swete Septuagint digitization | "Open Greek and Latin Project, First1KGreek (github.com/OpenGreekAndLatin/First1KGreek), prepared by github.com/nathans/lxx-swete", CC BY-SA 4.0 | Any use of the Greek text in `greek/lxx-swete/` |

Credit asked for, not required: the Groves Center (WLC) and Tanach.us (UXLC).

## Watch out

- **GPL 3.0 — `lexicons/strongs/`.** Strong's own 1890 text is public
  domain, but this digital copy is GPL. Publishing a changed copy of these
  files, or data derived from them, puts that data under GPL. Reading them
  to write our own translation does not.
- **Share-alike (CC BY-SA 4.0): `greek/lxx-swete/`.** Swete's printed
  text (1909–1930) is public domain. The digital copy is CC BY-SA. If we
  publish the Greek text, changed or not, it must carry the same licence
  and credit. Our own English translation made from Swete's Greek is not
  bound by this.
- **Tanach.us site files — `hebrew/uxlc/`.** Only the biblical text
  (`Books/`) is free. The zip also carries Tanach.us's own pages and
  images (`Pages/`, `Images/`), which are copyrighted and need their
  written permission to reuse.
- **Modern "coded" or "new" editions of Strong's, Thayer's or Gesenius**
  (Hendrickson, Thomas Nelson) are copyrighted. Nothing here comes from them.

## By folder

### hebrew/

| Folder | What | Source | Status |
|---|---|---|---|
| `uxlc/` | Unicode/XML Leningrad Codex 2.5 — the Westminster Leningrad Codex, corrected against the manuscript since 2020 | tanach.us/Books/Tanach.xml.zip | Text public domain; site files copyrighted (see above) |
| `oshb-wlc/` | Open Scriptures Hebrew Bible — WLC 4.20 with lemma, Strong's-based lemma ids and morphology | github.com/openscriptures/morphhb | WLC text public domain; lemma and morphology CC BY 4.0 |

### greek/

| Folder | What | Source | Status |
|---|---|---|---|
| `sblgnt/` | SBL Greek New Testament (2010) with apparatus | github.com/LogosBible/SBLGNT | CC BY 4.0 (since Dec 2022) |
| `tischendorf/` | Tischendorf 8th edition, with morphology, Strong's and lemmas | github.com/morphgnt/tischendorf | Public domain (Sandborg-Petersen, Yale, Robinson) |
| `westcott-hort/` | Westcott-Hort 1881, parsed | github.com/byztxt/greektext-westcott-hort | Public domain |
| `tr-scrivener-1894/` | Textus Receptus, Scrivener 1894, parsed | github.com/byztxt/greektext-scrivener | Public domain |
| `tr-stephanus-1550/` | Textus Receptus, Stephanus 1550, parsed | github.com/byztxt/greektext-stephens | Public domain |
| `textus-receptus/` | Maurice Robinson's Textus Receptus edition, parsed | github.com/byztxt/greektext-textus-receptus | Public domain |
| `lxx-swete/` | Septuagint (Greek Old Testament), Swete's edition 1909–1930, one word per line with chapter and verse | github.com/nathans/lxx-swete, from github.com/OpenGreekAndLatin/First1KGreek (`data/tlg0527`) | Swete public domain; digital text CC BY-SA 4.0; build scripts MIT |

The SBLGNT copy at github.com/morphgnt/sblgnt was left out on purpose. Its
parsing layer is CC BY-SA, and its README still points to the SBLGNT licence
from before the 2022 change. STEPBible's TAGNT covers the same ground under
plain CC BY.

### lexicons/

| Folder | What | Source | Status |
|---|---|---|---|
| `strongs/` | Strong's Hebrew and Greek dictionaries (1890) | github.com/openscriptures/strongs | Strong's public domain; **this digitization GPL 3.0** |
| `bdb/` | Brown-Driver-Briggs (1906), unabridged, with corrections and a BDB-to-Strong's map | github.com/unfoldingWord/Brown-Driver-Briggs-Enhanced | BDB public domain; additions CC BY |

| `thayer/` | Thayer's Greek-English Lexicon (1889), machine-read text of a scanned copy | archive.org/details/greekenglishlexi00grimuoft | Public domain (Internet Archive: NOT_IN_COPYRIGHT) |
| `gesenius/` | Gesenius's Hebrew and Chaldee Lexicon, Tregelles translation (1857), machine-read text of a scanned copy | archive.org/details/hebrewchaldeelex00geseuoft | Public domain (Internet Archive: NOT_IN_COPYRIGHT) |

The Thayer's and Gesenius files are raw machine-read text, not structured
data. The English reads well. In Thayer's, the Greek came out as Latin
letters (ἐνισχύω reads `év-toxvw`). In Gesenius, the Hebrew is mostly
unreadable and some pages have their columns mixed together. The page scans
(about 100 MB each) are not downloaded; they are at the same archive.org
addresses.

#### Thayer's, parsed — `lexicons/thayer/thayer-entries.json`

Built by `parse_thayer.py` (in this folder; run `python parse_thayer.py`,
about 80 seconds). One record per Thayer's entry:

| Field | Meaning |
|---|---|
| `strongs`, `estrong` | Strong's number and STEPBible's extended number; empty for words Strong's lacks |
| `lemma`, `translit` | The Greek headword and transliteration, from STEPBible's TBESG |
| `text` | The entry's machine-read text. English is reliable; Greek inside it is still garbled |
| `ocr_headword`, `ocr_line` | The headword as the OCR read it, and its line in `thayer-1889_djvu.txt` |
| `score`, `english_overlap` | How well the garbled headword reads as the lemma, and how much of the entry's English appears in STEPBible's definition |
| `check` | `true` where neither check supports the pairing — read these by eye before relying on them |

Result: 5,094 entries carry a Strong's number, covering 5,092 of the 5,523
Strong's numbers G0001–G5624. Another 373 entries are words Strong's does
not have. Most of the rest of the Strong's numbers are forms of other words
(ἐμέ, ἦν) that Thayer's files under the main word. In a random spot-check,
about 1 pairing in 30 was wrong. The wrong ones are mostly among the 446
marked `check: true`, typically a word Strong's lacks that took a
neighbour's number. `thayer-report.txt` lists those 446.

Credit if published: Thayer's text is public domain. The Greek headwords and
Strong's numbers come from STEPBible (CC BY): credit "STEP Bible".

### stepbible/

From github.com/STEPBible/STEPBible-Data, all CC BY 4.0 (Tyndale House
Cambridge, curated by STEP Bible). Credit "STEP Bible" linked to
www.STEPBible.org.

| File | What |
|---|---|
| `TAHOT *` (4 files) | Hebrew OT, every word tagged with lemma, morphology and meaning (copied from `../lemma-data/`) |
| `TAGNT *` (2 files) | Greek NT, same tagging, with variants across the editions (copied from `../lemma-data/`) |
| `TBESH`, `TBESG` | Short Hebrew and Greek lexicons keyed to Extended Strong's numbers |
| `TIPNR` | Every proper name, told apart and with all references |
| `TVTMS` | Verse-numbering map between Hebrew, Greek, Latin and English traditions |

STEPBible asks that its data be fetched from their GitHub rather than
re-hosted, which is one more reason this folder is not committed.

## Rebuilding

Every source above is a GitHub repository or a public URL. Download the
repository zip from its default branch into the folder named, or for UXLC
download `Tanach.xml.zip` and unzip it.
