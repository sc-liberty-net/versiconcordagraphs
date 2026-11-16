# Handoff: Kings & The Kingdom

Started 16 November 2026, as the third concordagraph. The first is Taxes, Tithes, &
Tribute (`..\Biblography`); the second is Swords & Words (`..\Swords & Words`).

## The Agreed Plan (With Ethan, 16 Nov)

- **Topic:** the rulers of the earth, and how man governs compared with how God
  governs. It covers decrees, conquest, war, plunder and the slain; human violence and
  vengeance; force compared with how God acts and directs; how Jesus acts compared with
  us ("my kingdom is not from this world"); and government, oppression and law.
- **Title:** `Kings & The Kingdom`, in Ethan's title case. **Slug:** `king`. **Branch
  and web folder:** `kings-and-the-kingdom`.
- **Where:** this folder, with its own git history, on branch `kings-and-the-kingdom`.
  On GitHub it is a branch of `versiconcordagraphs`, like the other topics (Q9). It has
  its own folder only so the shared Biblography folder never switches branch; Ethan
  asked about this and agreed after it was explained. Remotes `liberty` and `versicon`
  are set. **Nothing has been pushed or published.** No `preserve` repo exists for this
  topic.
- **Groups:** the 14 in `corpus_clusters.csv`, which Ethan approved as listed, with
  "Not Of This World" at the centre.
- **Overlaps:** both kinds are recorded, as Ethan chose. Cross-topic connections go in
  `corpus_edges.csv`, and `overlaps.py` generates `OVERLAPS.md`. See `../CLAUDE.md`.
- **Title case** on every label. The checker passed with 0 violations.

## State, 16 Nov

- **216 passages, 236 connections**, 46 books. 215 connections are on the page; 21
  point into Taxes (13) or Swords & Words (8) and are held back for the merge.
  Warrant: 91 `states`, 113 `supports`, 32 `spec`. Kind: 230 `con`, 6 `ref`, **0
  `lex`**.
- `build_graph.py` passes with no corpus notes. The check-by-eye list has 7 passages
  (Luke 22:51, James 4:2, Acts 4:26, Matthew 21:5, Matthew 5:38, 1 Peter 2:23,
  Luke 9:55), and each was read against its verse and is correct.
- `check_wording.py` is clean for summaries and edge notes. It was seen to fail on a
  planted copied run.
- `nrsv_index.py` reconciles with no drift.
- **The page was checked** at 1400 px and 375 px in Chromium:
  - all 216 passages and 215 arcs drew;
  - there is no sideways scroll;
  - a desktop click opens the panel;
  - a phone tap opens the sheet.

  The one console error is a missing optional file (`wordstudy.js` or `icons/`).
- **Shared verse:** only Acts 5:37, with Taxes. Taxes and Swords & Words share no
  verse with each other.
- `READING.md` holds the first reading: findings F1–F10 and the test of the Hugo
  saying.

## Not Done

- **No `lex` links.** `lemma.py` has not been run over this corpus. Some `con` links
  may share Hebrew or Greek wording, for example the "kings of the earth" passages.
- No `check_page.py` or smoke suite with a baseline here. The Taxes suite tests
  Taxes-specific passages. Do not publish without one.
- No motifs, no Word Study, no `icons/` (`make_icons.py`), no `findings.pdf`.
- Page template: the About panel still describes motifs and the Word Study, which
  this topic lacks. The Motifs bar hides itself when there are none.
- `build_graph.py` here has 13 more book abbreviations than the Biblography copy.
  The two copies have diverged by that much.
- Local copies kept out of git: `verses.json`, `chapters.json`, `nrsv.txt`,
  `strongs_index.json`, `verses.js`.
