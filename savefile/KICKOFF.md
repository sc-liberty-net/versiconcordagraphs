# Kickoff — paste this to start the next session

Regenerated 25 September 2026. Paste the block below and nothing else. Do not paste the
savefile documents themselves: a path is read once, on demand; pasted text is re-read
on every turn forever.

---

```
This is a Bible-study research project. The artefact is an argument, not a
codebase, so read in this order before doing anything:

  CLAUDE.md          — loads on its own, but read it as the mechanism doc
  savefile/README.md — the read order for everything else

Then confirm the pipeline is sound before changing anything. There are FOUR
commands now, not three:

  python nrsv_index.py     — must end "reconciled against index-baseline.json:
                             no drift". A drift failure is a REAL failure; do not
                             re-record the baseline to clear it.
  python build_graph.py    — must write 184 nodes and 223 edges, and print 11
                             nodes to check by eye.
  python attach_verses.py  — must resolve all 184 with 0 unresolved.
  python check_page.py     — must end "PASSED - the page runs, nothing moved, no
                             dead selectors."

Any other number means something moved. Tell me before fixing it.

That fourth command is not optional and it is not a formality. On 25 September
this page shipped BLANK three times while every check passed, because every
check read the served HTML for the right strings — and they were all there, in a
file whose script never ran. A duplicate `const` is a parse error. Nothing that
reads HTML as text can see that. Only running it can.

Report those four and stop.

After I confirm: read savefile/QUESTIONS.md. Seven are open and Q10 is the one I
care about — whether the affirmation in Matthew 23:23 survives Hebrews 7:12. All
three readings are already drawn as edges; what is not decided is which is true,
and that is mine to decide, not yours.

Working rules that are easy to get wrong here:
- Never adjust a verse reference until it resolves. If it does not resolve, the
  citation is wrong, or the index has a hole — there are 114 known holes, plus
  two book-name splits and 161 duplicate Esther references.
- Never read verses.json, nrsv.txt or strongs_index.json into context. Query
  them with a script and print only what is needed.
- Edit the CSVs, never the block between // <corpus> and // </corpus>.
- The corpus is PUBLIC now. Anything committed is published.
- Unrelated problems get logged in the Mission Control Room, not fixed.
- Verify the page by RUNNING it. Reading it proves nothing.
```

---

## Why this block says what it says

**The four commands, with their expected output.** An agent that runs them and reports
numbers has read the project's state from the project rather than from a summary. The
fourth is spelled out with its reason because it is new, it is the expensive lesson of
25 September, and an agent that treats it as optional will repeat that failure.

**Q10 is named.** The previous kickoff named nine open questions and let the agent pick;
this one points at the single question Ethan has said he cares about, with the note that
the work is already drawn and only the judgement is missing.

**The index defects are named as a group.** An agent that hits `Galatians 6:1` failing to
resolve will otherwise conclude the reference is wrong, which is the exact failure the
114 holes were documented to prevent. There are now three classes of them.

**"The corpus is PUBLIC now"** is there because every prior instruction about copyright
assumed a private repo, and the consequence of a mistaken commit changed on 25 September.
