# Working rules for this repository

This folder is the **Kings & The Kingdom** concordagraph, branch `kings-and-the-kingdom`,
slug `king`. Read `savefile/HANDOFF.md` first: the agreed plan and what is not done yet.
Read `READING.md` for what the corpus shows so far. The taxes-and-tithes topic lives in
`..\Biblography` and Swords & Words in `..\Swords & Words`, each on its own branch; do
not edit either from here.

## Where It Ships

This folder's branch `kings-and-the-kingdom` is pushed, never with force, to:

- `versicon` (github.com/DrugsForRobots/versiconcordagraphs, private): its `kings-and-the-kingdom` branch.
- `liberty` (github.com/sc-liberty-net/versiconcordagraphs, **public**): its `kings-and-the-kingdom` branch.

No `preserve` repo exists for this topic yet.

The live page is the public repo's `gh-pages` branch, folder `kings-and-the-kingdom/`:
take a fresh clone into the scratchpad, copy `concordagraph.html` in as `index.html` and
the `icons/` folder beside it, keep the root `index.html` card's counts current, commit,
push, wait for the Pages build, then check
https://sc-liberty-net.github.io/versiconcordagraphs/kings-and-the-kingdom/ at desktop
and phone width. Run `python check_page.py` first; never publish on a red.

**Overlaps (Ethan, 16 Nov 2026).** Where this topic meets another, record it for the
future merge: a cross-topic connection in `corpus_edges.csv` with the other topic's
prefix (`tithe:kg2`, `sword:x4`), tagged like any other. Then run `python overlaps.py`,
which rewrites `OVERLAPS.md`: shared verses and cross-topic connections, generated,
never typed.

**Labels follow Ethan's title-case rule** (the `title-case` skill): group names, the
title and every page label. Run its checker on the built page.

The original-language sources are in `..\Biblography\bible-sources\`. Read
`..\Biblography\bible-sources\RULES.md` before using any original-language
text or lexicon there. Gesenius (Tregelles, 1857) is one of our
Hebrew sources and references: consult it alongside BDB for any claim about
what a Hebrew word means, reading its pages on demand as that file
describes.

## Never

- **Never add a verse reference from memory.** Every reference must resolve in
  `verses.json`. If it does not resolve, the citation is wrong — do not adjust
  the reference until it matches something, and do not guess.
- **Never edit the block between `// <corpus>` and `// </corpus>` in
  `concordagraph.html`.** It is generated. Edit the CSVs and run
  `build_graph.py`.
- **Never commit or publish `verses.js`, `nrsv.txt`, `verses.json`,
  `chapters.json`, or the source PDF.** They contain NRSV text, which is under
  copyright. They are gitignored; do not override that.
- **Never read `verses.json` or `nrsv.txt` directly into context.** They are
  tens of megabytes. Query them with a script and print only what is needed.

## Always

- Run `python3 build_graph.py` after any corpus change. It refuses to write on
  a bad reference, a dangling edge, a duplicate id, a misspelled warrant
  tier, the same verse cited twice in one module, or a malformed cluster
  table. A refusal means the corpus is wrong, not the script.
- Tag every proposed connection with its warrant tier: `states`, `supports`,
  `spec`. Never promote a speculation to a statement.
- Summaries are paraphrase written for this project, never NRSV wording.
- Read the "check by eye" list `build_graph.py` prints. A resolvable reference
  is not a correct one — a node can cite a real verse and summarise a different
  one, and only that list will surface it.

- **A `nrsv_index.py` drift failure is a real failure.** It means this build of
  the index is not the one the corpus was checked against. Do not re-record the
  baseline to make it pass — `--record` is for when you have decided the new
  build is the correct one, not for clearing a red. An index that loses verses
  still answers confidently inside the range it kept.

- Check every summary and edge note for five-word runs shared with the NRSV before
  anything ships. Edge notes ship on the page too.
