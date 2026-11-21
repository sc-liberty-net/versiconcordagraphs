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

## Shipped, 16 Nov (Ethan: "ship it to the appropriate repo")

- Pushed to `versicon` and `liberty`, branch `kings-and-the-kingdom`, and published at
  https://sc-liberty-net.github.io/versiconcordagraphs/kings-and-the-kingdom/, with a
  card on the site's front page. See `../CLAUDE.md`, "Where It Ships".
- Added for the ship, all in this folder's page only (Taxes is unchanged):
  - favicon, home-screen icons and a preview card (`make_icons.py`). The crown emblem
    was Claude's draft; Ethan chose to keep it (16 Nov);
  - two-finger pinch zoom and pan; keyboard zoom (+, -, 0); 44 px zoom controls on
    touch screens, clear of the home bar; a one-time gesture hint on touch screens;
  - the view no longer refits when only the window's height changes, which on a phone
    threw away the reader's zoom whenever the address bar slid.
- `check_page.py` and `smoke_concordagraph.py`, baseline recorded (`SMOKE-RECORD.md`).
  The new checks were seen to fail on the page as committed in 626d368.

## Added 18 Nov (Ethan): Back and Resizable Columns

- A Back button in the top right of the details panel. Each time the panel moves
  off something (a new pick, a connection, Close, Show Everything Again), that thing
  is kept, newest last, and Back returns to it. On phones it sits in the sheet's bar
  beside Close.
- Both side columns resize by dragging their inner edges (desktop and tablet widths;
  hidden at 900 px and below, where the columns stack). Double-click or Home resets an
  edge; arrow keys move a focused edge. Widths are kept per reader in localStorage.
- Shipped 18 Nov: pushed to `versicon` and `liberty` (b1abdf8), live page gh-pages
  a4dd166, checked at desktop and phone width.

## Added 20 Nov (Ethan, "Do all eight"): Readability Pass

From a review of the live page (O1–O8):
- O1–O2: connection rows show the kind and strength as two chips; the note is in
  body ink, not green or orange text.
- O3: dropped. The review said the arcs were faint at rest; they are not. The haze
  is the intended dimming while something is selected.
- O4: phone, turned graph: passage names hidden until zoom makes them about 8 px.
- O5: touch screens: filter rows, headers, buttons and search at least 44 px;
  search at 16 px so iOS does not zoom.
- O6: phone: a picked passage or arc is moved into the strip above the sheet.
- O7: phone: less space between the folded filters and the graph.
- O8: Compare and Read In Full in a link colour (`--link`), a size up.
- Shipped 21 Nov: pushed to `versicon` and `liberty` (5375007), live page gh-pages
  ce48f79, checked at 1400 px and 375 px (216 passages, no sideways scroll, no page
  errors, 16 chips on John 18:36, phone names hidden at the fitted view).

## Not Done

- **No `lex` links.** `lemma.py` has not been run over this corpus. Some `con` links
  may share Hebrew or Greek wording, for example the "kings of the earth" passages.
- No motifs, no Word Study, no `findings.pdf`.
- The Taxes page has none of the touch additions above.
- Page template: the About panel still describes motifs and the Word Study, which
  this topic lacks. The Motifs bar hides itself when there are none.
- `build_graph.py` here has 13 more book abbreviations than the Biblography copy.
  The two copies have diverged by that much.
- Local copies kept out of git: `verses.json`, `chapters.json`, `nrsv.txt`,
  `strongs_index.json`, `verses.js`.
