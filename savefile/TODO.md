# Todo — ranked by what it blocks

**Reconcile.** Close what ships, keep the numbers stable — they get referred to in
conversation — and add what is new.

**The ranking below is one agent's read of risk, not Ethan's priorities.** Ask him
which of these matters before working down it.

**The Mission Control Room is the authoritative queue**, not this file. Room tasks
49–59 are Biblography's and hold the full record of each — evidence, measurements,
sign-offs. This file says only *what each one blocks*, which the Room does not rank.
Where they disagree, the Room is right. Anything needing Ethan's authority rather than
an agent's work is in `QUESTIONS.md` instead.

---

## Blocking a second concordagraph

**1 · Quote the cluster key.**
`build_graph.py` emits cluster keys unquoted into a JS object literal; any key that is
not a bare identifier ships a blank page on a green build. Two lines — emit `{j(k)}`,
and widen `extract_corpus.py`'s cluster regex to accept a quoted key. Stops at Ethan's
go-ahead; it is live code.
*Blocks:* any concordagraph whose groups have two-word names, which is most of them.
Also blocks item 2, since a second module will want its own group names. Room 57,
`QUESTIONS.md` Q3.

**2 · Build the second module for real.**
"Wages" or similar, as its own branch of `versiconcordagraphs`. An agent built a
throwaway one during the design pass and it proved the three module decisions hold;
nothing of it was kept.
*Blocks:* the skill — everything that broke in the design pass broke on contact with a
second module. Also blocks 3 and `QUESTIONS.md` Q6.

**3 · Write the co-citation reporter.**
Eight lines over two `corpus_nodes.csv` files: which passages does more than one topic
claim, and what is each saying about them. An agent wrote and ran one during the
design pass; it found all six shared verses without any of the compile apparatus.
*Blocks:* the compare-or-compile decision (Q6). This is the cheap experiment that
answers it.

**4 · Then write the skill.**
Not before 2 and 3. The draft from 22 Sept is dead — see `DEAD-ENDS.md` — but its
diagnosis holds.
*Blocks:* a third and fourth concordagraph being built by hand, as the first three
were.

---

## Blocking a claim the project makes

**5 · Enforce "summaries are paraphrase, never NRSV wording."**
`../CLAUDE.md` states the rule and nothing checks it; 22 of 151 already break it.
`build_graph.py` already holds the verse text in `raw` during its verify pass, so the
check costs almost nothing — flag any summary sharing a run of N+ consecutive words
with its verse, as a note rather than a refusal.
*Blocks:* the README's claim that the page is freely shareable because it carries only
references and summaries. Related to Q2, which is the editorial half.

**6 · Give the check-by-eye list a memory.**
It prints the same eleven ids on every build and blocks nothing, so it stops being
read. Record the cleared ids with the reason each was cleared, diff against it, and go
red only on a node that is new or whose summary has changed since.
*Blocks:* the list being trustworthy at 400 nodes across four topics. At 151 it is
still readable; that will not last.

---

## Worth doing, not urgent

**7 · Recover the 114 missing verses**, or decide they stay missing. Needs a different
splitting approach in `nrsv_index.py`, not a different extractor — that is settled.
No corpus node cites one today. Room 55.

**8 · Delete the empty `files/` folder and the 22-byte `files.zip`.** Both committed
in `02e69ac`. Room 50.

**9 · Make `build_graph.py` importable** so a second tool can reuse its rules instead
of re-implementing them. `argparse` is parsed at module scope, which is what stops it.
Nothing needs this until a second validator exists.

---

## Discussed, not started

**10 · A master compile.** Explicitly not built, and probably should not be until Q6
is answered. The apparatus a compile needs is larger than the payoff it delivers,
which the co-citation reporter demonstrates.

**11 · Reconcile the two meanings of "versicon".** `QUESTIONS.md` Q8. Whichever way it
goes, the losing document needs a dated correction rather than a silent edit.
