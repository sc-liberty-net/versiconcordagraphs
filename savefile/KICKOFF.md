# Kickoff — paste this to start the next session

Regenerated 12 October 2026, for embedding the Word Study in the concordagraph. Paste the
block below and nothing else.

---

```
Project: Biblography — Ethan's Bible-study research; the Taxes & Tithes concordagraph
(a public interactive graph of 184 passages) and its Word Study (our own literal English,
every word opening onto the Hebrew or Greek).
Working folder: C:\Users\ethan\Desktop\Biblography (on this machine).

Read first, in this order:
  CLAUDE.md                — loads on its own; the rules for the corpus and the NRSV
  wordstudy\README.md      — the Word Study: run order, decisions, licences, and the
                             facts about the concordagraph that this job needs
  savefile\HAZARDS.md      — what has broken before; read the first hazard
  check_page.py (docstring) — the page gate, and how a moved smoke line is recorded

Mode: building. The Word Study's readings are drafted and checked (184 of 184 pass);
do not redraft or re-review them, and do not touch the translation choices.

Definition of done — all must pass, in this order:
  cd wordstudy: python extract.py; python check.py; python build.py; python test_page.py
  root: python nrsv_index.py; python build_graph.py; python attach_verses.py; python check_page.py
build_graph.py must still write 184 nodes and 223 edges. check_page.py diffs every
smoke line against smoke-baseline.out: a line your change moves is recorded with the
guard and a named cause; a line that moved without you moving it is the finding.
If any fails, fix the cause. Never loosen an assertion to make it green.

To see your work: open concordagraph.html in Firefox from file:// (no server), and run
it in Chromium the way check_page.py does. Click a passage: it should show our English
with the KJV beneath it, hover synonyms on desktop, and the full study on click, on
desktop and at phone width. Without verses.js the page must still work, as now.

Off limits: the block between // <corpus> and // </corpus>; NRSV text on any published
page or commit; wordstudy\data\ and digest\ in any commit; pushing or publishing the
live site without my yes; editing authored\ readings.

Manual override: if I write "manual override" I am suspending Mode and Off Limits for
that request. Name the specific consequence and ask before you act on it.

What I want changed:
  1. Clicking a passage in the concordagraph shows the passage itself, in our literal
     English, with hover synonyms and the Word Study panel, instead of only a one-line
     summary.

Ask before making a change I have not asked for.
Report what you verified, not what you intended.
```

---

## Still To Fill In

- Nothing guessed in the block. How the Word Study data reaches the page (inline, or a
  separate file loaded on demand like `verses.js`) is left to the agent: the 4.8 MB size and
  the file:// previews are stated in `wordstudy/README.md` so it can choose.
- Open, and not part of this job: Q12 (record Ethan's answer to Q10 and Q11, "reading 3, with
  reading 2 as its consequence; giving binds, the tenth a target, arguably a minimum expected,
  but by no means the limit, and not compelled"), the STEP email, Leviticus 27:31 and the
  sowing verses as possible new nodes.
- The rest of the savefile (`HANDOFF.md`, `TODO.md`, `QUESTIONS.md`) was last written
  25 September and does not yet cover the Gesenius, Septuagint or Word Study work.

## Notes On This Version

The previous kickoff (25 Sept) opened a Q10 session; Q10 has since been argued through and
awaits only Ethan's go to record it. This one exists because the embedding job needs facts
about two pipelines at once, so they were written into `wordstudy/README.md` rather than
into the prompt.
