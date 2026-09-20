# Working rules for this repository

Read `README.md` for the run order and `DESIGN.md` for open decisions.

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
