# Working rules for this repository

Read `README.md` for the run order and `DESIGN.md` for open decisions.

Read `bible-sources/RULES.md` before using any original-language text or
lexicon in `bible-sources/`. Gesenius (Tregelles, 1857) is one of our
Hebrew sources and references: consult it alongside BDB for any claim about
what a Hebrew word means, reading its pages on demand as that file
describes.

## Where It Ships

Local `main` holds this topic, Taxes, Tithes, & Tribute. A ship pushes it to three
places, never with force:

- `versicon` (github.com/DrugsForRobots/versiconcordagraphs, private): `main` → its `taxes-and-tithes` branch.
- `liberty` (github.com/sc-liberty-net/versiconcordagraphs, **public**): `main` → its `taxes-and-tithes` branch.
- `preserve` (github.com/DrugsForRobots/taxes-tithes-tribute, private): `main` → its `main`.
  This repo holds this topic and nothing else. It is the preservation copy, made
  22 Oct 2026 in case the multi-topic repos are ever merged or scrambled. Never push
  another topic into it, and never delete it.

The live page is the public repo's `gh-pages` branch, folder `taxes-and-tithes/`:
take a fresh clone into the scratchpad, copy `concordagraph.html` in as `index.html`
(and `wordstudy.js` when it has changed, and the `icons/` folder when `make_icons.py`
has rewritten it), commit, push, wait for the Pages build, then
check https://sc-liberty-net.github.io/versiconcordagraphs/taxes-and-tithes/ at desktop
and phone width.

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
