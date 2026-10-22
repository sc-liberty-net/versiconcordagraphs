# Savefile — Biblography

Started 22 September 2026; **last updated 25 September 2026** at the end of the session
"Biblography — Q1 tithing reading, the lemma layer and the motif report". Read in this
order and stop when you have what you need. Nothing here repeats `../CLAUDE.md`, which
loads on its own.

| Read | File | Answers | Write mode |
|---|---|---|---|
| 1 | [`QUESTIONS.md`](QUESTIONS.md) | What is not yours to decide — **ten, of which three are answered and struck** | reconcile |
| 2 | [`HANDOFF.md`](HANDOFF.md) | What this is for, where it stands, what is settled | regenerate |
| 3 | [`HAZARDS.md`](HAZARDS.md) | "I am seeing X" — indexed by symptom | append only |
| 4 | [`TODO.md`](TODO.md) | What is worth doing, by what it unblocks | reconcile |
| — | [`LESSONS.md`](LESSONS.md) | How to work here, and how to work with Ethan | append only |
| — | [`DEAD-ENDS.md`](DEAD-ENDS.md) | Tried, abandoned, and whether the reason still holds | append only |
| — | [`KICKOFF.md`](KICKOFF.md) | The opening message for the next session | regenerate |

**Your five minutes:** `QUESTIONS.md`, then the "What you see on the page" and "What
the data does" sections of `HAZARDS.md`. Between them they cover everything that will
otherwise cost you an hour.

**If you read one hazard, read the first one.** The page shipped **blank** three times
on 25 September while every check passed, because every check read the served HTML as
text. A duplicate `const` is a parse error and nothing that reads HTML can see it.

## What the agent should do first

From the project root, before changing anything:

```powershell
python nrsv_index.py
python build_graph.py
python attach_verses.py
python check_page.py
```

Expect, in order: `reconciled against index-baseline.json: no drift`;
`wrote 184 nodes, 223 edges` followed by `11 node(s) to check by eye`;
`unresolved     : 0`; and `PASSED - the page runs, nothing moved, no dead selectors`.
Any other numbers mean something moved — say so before fixing it.

**`check_page.py` is new and is now part of the definition of done.** It loads the
built page in Chromium and gates all 32 lines it prints against `smoke-baseline.out`.
A line that moves fails the run until its cause is written into `SMOKE-RECORD.md`
using the smoke-gate skill's baseline guard — never by overwriting the baseline.

An index drift failure is a **real** failure. Do not run `--record` to clear it.

## How to start the next session

Paste the block in [`KICKOFF.md`](KICKOFF.md). **Do not paste these files into a new
session.** Pasted context is re-read on every turn of that session, forever; a path is
read once, on demand, and only if the agent needs it. That is the economics the whole
savefile depends on.

## Deliberately absent, with where that material lives instead

- **Mechanism** — `../CLAUDE.md` (the rules and refusals) and `../README.md` (the run
  order and the data contract). Both load or are read on arrival; duplicating them
  here would create a second copy to drift.
- **Design decisions about the module format** — `../DESIGN.md`.
- **Vocabulary** — `../lexicon.md` holds this project's terms, and the Lexiconomicon
  at `~/Desktop/Lexicon` is the register of record with its own tooling. Note that
  "versicon" is defined incompatibly in the two; see `QUESTIONS.md` Q8. Nothing is
  filed from here.
- **Baseline history** — `../SMOKE-RECORD.md`, append only, one entry per baseline
  move with the cause that justified it.
- **The task queue** — the Mission Control Room, tasks 49–66. `TODO.md` ranks them by
  what they block; the Room holds each full record.

## Where these files belong

`C:\Users\ethan\Desktop\Biblography\savefile\`. They are committed on `main`, which is
pushed to the `taxes-and-tithes` branch of **two** repositories: the private
github.com/DrugsForRobots/versiconcordagraphs and, since 25 September, the
**public** github.com/sc-liberty-net/versiconcordagraphs. The built page is served from that repo's
`gh-pages` branch at
https://sc-liberty-net.github.io/versiconcordagraphs/taxes-and-tithes/.

*22 Oct 2026:* a third, private repo, github.com/DrugsForRobots/taxes-tithes-tribute,
holds this topic alone on its `main`, as a preservation copy. `../CLAUDE.md`, "Where It
Ships", lists all three.

**Anything committed here is now public.** The whole history was scanned before the
repo went public and no verse-text file was ever committed; keep it that way.

**Append-only means append only.** Correct a hazard, lesson or dead end by adding a
dated sequel beneath it. The original is the evidence.
