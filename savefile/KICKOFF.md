# Kickoff — the opening message for the next session

Paste the block below into a new session opened in
`C:\Users\ethan\Desktop\Biblography`. **Do not paste the savefile itself.** Pasted
context is re-read on every turn of that session, forever; a path is read once, on
demand, and only if the agent needs it.

---

```
This is a Bible-study research project. The artefact is an argument, not a
codebase, so read in this order before doing anything:

  CLAUDE.md          — loads on its own, but read it as the mechanism doc
  savefile/README.md — the read order for everything else

Then confirm the pipeline is sound before changing anything:

  python nrsv_index.py     — must end "reconciled against index-baseline.json:
                             no drift". A drift failure is a REAL failure; do not
                             re-record the baseline to clear it.
  python build_graph.py    — must write 151 nodes and 170 edges, and print 11
                             nodes to check by eye. Any other number means
                             something moved; tell me before fixing it.
  python attach_verses.py  — must resolve all 151 with 0 unresolved.

Report those three and stop.

After I confirm: read savefile/QUESTIONS.md and tell me which of the nine you
think matters most this month, and why. Do not start work on any of them until
I answer — several are mine to decide, not yours.

Working rules that are easy to get wrong here:
- Never adjust a verse reference until it resolves. If it does not resolve, the
  citation is wrong, or the index has a hole — there are 114 known holes.
- Never read verses.json or nrsv.txt into context. Query them with a script.
- Edit the CSVs, never the block between // <corpus> and // </corpus>.
- Unrelated problems get logged in the Mission Control Room, not fixed.
```

---

## If the session is for a specific piece of work

Replace the last paragraph of the block with the one item, and name what it blocks.
The three most likely:

**Quoting the cluster key** — two lines, blocks every future concordagraph.
`savefile/TODO.md` item 1, Room task 57.

**Building the second module** — blocks the skill and the compare-or-compile
decision. `savefile/TODO.md` item 2.

**Reading Matthew 23:23 and Luke 11:42** — Ethan's own reading; it is the only open
item that changes what the research says. `savefile/QUESTIONS.md` Q1.
