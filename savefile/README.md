# Savefile — Biblography

Written 22 September 2026 at the end of the session "Biblography — pipeline check and
versicon decisions". This is the first savefile for this project. Read in this order
and stop when you have what you need. Nothing here repeats `../CLAUDE.md`, which loads
on its own.

| Read | File | Answers | Write mode |
|---|---|---|---|
| 1 | [`QUESTIONS.md`](QUESTIONS.md) | What is not yours to decide — **nine of them, and three block the current work** | reconcile |
| 2 | [`HANDOFF.md`](HANDOFF.md) | What this is for, where it stands, what is settled | regenerate |
| 3 | [`HAZARDS.md`](HAZARDS.md) | "I am seeing X" — indexed by symptom | append only |
| 4 | [`TODO.md`](TODO.md) | What is worth doing, by what it unblocks | reconcile |
| — | [`LESSONS.md`](LESSONS.md) | How to work here, and how to work with Ethan | append only |
| — | [`DEAD-ENDS.md`](DEAD-ENDS.md) | Tried, abandoned, and whether the reason still holds | append only |
| — | [`KICKOFF.md`](KICKOFF.md) | The opening message for the next session | regenerate |

**Your five minutes:** `QUESTIONS.md`, then the "What you see on the page" and "What
the data does" sections of `HAZARDS.md`. Between them they cover everything that will
otherwise cost you an hour.

## What the agent should do first

From the project root, before changing anything:

```powershell
python nrsv_index.py
python build_graph.py
python attach_verses.py
```

Expect, in order: `reconciled against index-baseline.json: no drift`;
`wrote 151 nodes, 170 edges` followed by `11 node(s) to check by eye`; and
`unresolved     : 0`. Any other numbers mean something moved — say so before fixing
it.

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
- **Design decisions about the module format** — `../DESIGN.md`, which records the
  three settled ones with their reasoning and the cost of revisiting.
- **Vocabulary** — `../lexicon.md` holds this project's terms, and the Lexiconomicon
  at `~/Desktop/Lexicon` is the register of record with its own tooling. Note that
  "versicon" is defined incompatibly in the two; see `QUESTIONS.md` Q8. Nothing is
  filed from here.
- **The task queue** — the Mission Control Room, tasks 49–59. `TODO.md` ranks them by
  what they block; the Room holds each full record.

## Where these files belong

`C:\Users\ethan\Desktop\Biblography\savefile\`. They supersede nothing — this is the
first set. They are committed on `main`, which is pushed to the `taxes-and-tithes`
branch of the private repository at
https://github.com/DrugsForRobots/versiconcordagraphs — so they travel with the
corpus.

**Append-only means append only.** Correct a hazard, lesson or dead end by adding a
dated sequel beneath it. The original is the evidence.
