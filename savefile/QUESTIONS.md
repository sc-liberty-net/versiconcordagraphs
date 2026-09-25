# Questions — what is not the agent's to decide

**Reconcile.** When one is answered, the answer moves to `HANDOFF.md`'s decisions
section and the question is struck here with a date.

Everything below needs authority, taste, or a reading nobody has done. Anything an
agent could settle by measuring is in `TODO.md` instead — that boundary is the whole
point of this file.

---

## Blocking the research finding

**~~Q1 · Do Matthew 23:23 and Luke 11:42 rebuke tithing, or affirm it while
relativising it?~~ ANSWERED 25 September 2026 — affirmed but relativised.**

Ethan's ruling, in his words: it is not a pure rebuke of tithing; it acknowledges
that tithing is a matter of law, but not equivalent to the weightier matters of
love, justice, mercy and faith. Affirmed, and subordinated.

The reasoning, because it is better than the question anticipated: *weightier* is a
comparative, so the phrase presupposes lighter matters **of the law**. "These" and
"the others" are therefore two species of one genus, not two unrelated referents —
and "the others", the lighter matters, is what the closing clause tells them to keep
doing. The affirmation is in the sentence.

Applied the same day: the `critique` cluster is renamed **"Tithing weighed"** (the key
stays `critique`, so Q3's unquoted-key bug is untouched); the `k1` and `k2` gists were
rewritten to carry the closing clause and the weightier/lighter structure, taking
verse-word coverage from 14/40 to 19/40 and 16/36 to 18/36. The decision is recorded
in `HANDOFF.md`.

Left open, and noted here rather than struck: whether the affirmation says anything
about what binds **after** the change of priesthood argued in Hebrews 7. That is a
separate question from what the sentence means, and the corpus's path runs straight
through it.

<details><summary>The question as it stood</summary>
The summary of Matthew 23:23 accounts for 13 of the verse's 40 words and stops at the
woe; Luke 11:42's covers 16 of 36. Nobody has read what the remaining words say — this
was deliberately not guessed. The cluster is named "Tithing rebuked" and sits directly
on the path from the tithe statutes to the Hebrews 7 argument, so *rebuked* versus
*affirmed but relativised* changes the trajectory the whole corpus traces. Neither
node appears on the check-by-eye list, because that heuristic only fires when a
summary shares **no** content word with its verse.
*Needs:* Ethan, reading the two verses. This is his research, not a measurement.
Room task 54.
</details>

**Q10 · Does the affirmation in Matthew 23:23 survive Hebrews 7:12?**
Opened 25 September 2026, the moment Q1 was answered. Q1 settled what the woes
*mean* — tithing is affirmed as a lighter matter of the law. It did not settle what
that affirmation *obliges now*, and the two are different questions. Jesus speaks
under the Mosaic covenant, while the Temple stands and Levi collects. Hebrews 7:12
says a change of priesthood requires a change of law as well.

Answering Q1 sharpened this rather than resolving it. While the cluster read
"Tithing rebuked", Hebrews 7 was finishing what the woes started. Now that the woes
affirm, Hebrews 7 is arguing out of force something Jesus upheld.

Three positions, each already fully supported by nodes in this corpus:

1. **The affirmation lapsed with the law it belonged to.** Covenant-specific.
   `k1` Matthew 23:23, against `h7` Hebrews 7:11 and `h8` Hebrews 7:12.
2. **The affirmation was of a principle that outlived its statutory form**, and
   Paul's collection is what it became — weekly, proportionate, uncompelled, no
   rate. `k1`, against `v13`–`v16` (1 Corinthians 16:1–2, 2 Corinthians 9:7,
   Romans 15:27).
3. **The question is malformed.** Hebrews 7:5 argues about who may *receive* —
   Levi's descendants "have a commandment in the law **to collect** tithes from the
   people" — not about whether the giver owes. On that reading the change of
   priesthood retires the collector and says nothing about the tenth. `h3` Hebrews
   7:5 and `t3` Matthew 17:26, against `n1` Numbers 18:21.

**The corpus needs no new verses for any of this.** Every passage the three
positions turn on is already a node. Checked 25 Sept: all twelve resolve.

**DRAWN 25 September 2026 — all three, not one.** Ethan's call, and the right one.
The three readings target three different nodes, so Q5's one-edge-per-pair refusal
does not apply, and an edge at `spec` records a connection rather than asserting a
conclusion. All three connections hold whichever reading eventually wins. The format
was built for this: speculative edges render differently and are never silently
promoted, so the graph can carry a live dispute visibly instead of burying it behind
one chosen answer.

- `k1`→`h8`, `con`/`spec` — reading 1
- `k1`→`v14`, `con`/`spec` — reading 2
- `k1`→`h3`, `con`/`spec` — reading 3

**They are not three rivals, and the notes were corrected the same day to say so.**
Ethan caught it: readings 1 and 3 genuinely contradict — did the tenth lapse with
the law, or was the tenth never what Hebrews was arguing about? Reading 2
contradicts neither. It answers a different question, *what does giving look like
now*, and sits downstream of whichever of 1 or 3 holds. If the tenth lapsed, Paul's
collection is what replaced it; if Hebrews only retired the collector, Hebrews is
silent on the giver and Paul is where that gets answered.

So the shape is **one disagreement (1 against 3), plus one consequence (2) that
attaches to either.** The notes now say exactly that.

All three sit at `spec` on purpose: no text links Matthew 23:23 to any of them, and
pre-weighting one by warrant would decide the question the edges exist to keep
open.

Matthew 23:23 now has eleven connections and reaches `hebrews` for the first time.

**The question itself stays open.** What was settled is how the corpus represents
it, not which reading is true. That is still Ethan's, and it is the one place here
where the answer is a theological judgement rather than a measurement. Room task 66.

**Q2 · Should the 22 summaries that reuse NRSV wording be rewritten?**
22 of 151 contain a run of five or more consecutive words lifted from the verse; the
longest are nine ("Is it lawful to pay taxes to the emperor?", "the patriarch gave him
a tenth of the spoils"). `../CLAUDE.md` says summaries are paraphrase, never NRSV
wording. Nothing continuous is reconstructable, so the copyright exposure is small —
but these are the files that ship, and the README's claim that the page is shareable
*because* it carries only references and summaries is less clean than it reads.
*Needs:* Ethan. Rewriting a summary is an editorial act on his own argument. Room
task 51.

---

## Blocking a second concordagraph

**Q3 · Fix the unquoted cluster key now?**
Two lines: emit `{j(k)}` in `build_graph.py`, and widen `extract_corpus.py`'s cluster
regex to accept a quoted key. Left undone because it is live code and he was away.
Until it lands, any group name that is not a single lowercase word ships a blank page
on a green build.
*Needs:* Ethan's go-ahead. Room task 57, and it blocks Q6.

**~~Q4 · `i3`, `c4`, `c13` carry no connection at all — connect, remove, or keep?~~
ANSWERED 25 September 2026 — connect. All three.**

None was a boundary marker; each had a neighbour already in the corpus sharing a
word rare enough to check. Four edges added, not three:

- `i3`→`i1` (Luke 3:1 → Luke 2:1), `lex`/`states` — Luke's two imperial dating
  formulae share a form of *Caesar* occurring in two verses.
- `c4`→`c1` (Matthew 10:3 → Matthew 9:9), `lex`/`states` — *Matthaios*, five verses.
- `c13`→`c2` (Luke 15:1 → Matthew 9:10), `lex`/`states` — the fixed
  tax-collectors-and-sinners pairing.
- `c4`→`c8` (Matthew 10:3 → Mark 2:14), `lex`/`spec` — *Alphaios*, five verses.

The fourth carries a question of its own, recorded on the edge. Alphaeus fathers
**James** in Matthew 10:3 and **Levi** in Mark 2:14 — so the open question there is
whether *James and Levi* are one man, two brothers, or two men who happen to share
a common patronymic. Levi appears in no apostle list; James appears in all four.

That is a different question from whether *Matthew and Levi* are one man, which
turns on the near-identical call narratives rather than on the name. That note went
on `c1`→`c8`, the pair where Matthew and Levi are the same figure, which already
existed tagged only "The same call story."

Checked and left out: STEPBible's apparatus records **no manuscript variant** on
"Levi" in Mark 2:14 — every word of the verse is attested across the Nestlé-Aland,
Traditional and Other traditions alike. A half-remembered Bezae reading of "James"
there could not be confirmed from the data, so it is not in the note.

Not done, and worth considering: Mark 3:18, Luke 6:15 and Acts 1:13 each list
Matthew and James son of Alphaeus as separate men, which is the other half of that
puzzle. None is a node.

<details><summary>The question as it stood</summary>

Luke 3:1, Matthew 10:3, Luke 15:1. Each has obvious neighbours. A concordagraph is a
claim about connections, and a node with none is either an unfinished thought or a
deliberate boundary marker; the corpus does not say which.
*Needs:* Ethan. Cheaper to settle at 151 nodes than at 400. Room task 58.
</details>

**~~Q5 · Can two passages carry more than one connection between them?~~
ANSWERED 25 September 2026 — yes. One edge per pair, per kind.**

Ethan's ruling. `build_graph.py` now keys its duplicate check on the node pair
**plus the kind**, so a pair may carry up to three edges — one `lex`, one `ref`,
one `con` — and a second edge of the same kind is still refused. Two `con` edges
between one pair would assert the same relation at two warrants, which is a
contradiction rather than a finding.

**The renderer needed no change.** `assignLanes` already lifts each arc until it
clears every arc it overlaps, so two edges with identical endpoints are drawn as
two stacked arcs, styled by their own kind and warrant. The picture was ready
before the validator was.

**Proved both ways before it was trusted**, on the build where each must hold: a
second `con` edge on a pair that already had one was refused (exit 1, *"duplicate
con edge"*); a `con` edge on a pair carrying only a `lex` edge was accepted. The
probes were appended, built against, and rolled back — the corpus is unchanged by
them.

**It was costing a real edge, and that edge is now split.** Matthew 9:9 to Mark
2:14 had been carrying two claims in one note: a `lex`/`states` claim that the call
narratives are one scene, and a `con`/`spec` claim about whether Levi and Matthew
are one man. They are different kinds at different warrants and now sit in
different rows. Room task 59.

<details><summary>The question as it stood</summary>

The duplicate check keys on the node pair alone — undirected, kind-blind — so a
finding that two verses *both* share wording and make the same argument cannot be
recorded. Zero pairs collide today, so nothing has been lost yet. One line either way.
*Needs:* Ethan. It is a decision about what the corpus can say, and it should be
written into `DESIGN.md` whichever way it goes. Room task 59.
</details>

**Q6 · Compare, or compile?**
The settled module decisions hold under a real second module — that is proven. What is
not settled is whether many topics should be *compiled* onto one canvas at all. A
compiled graph asserts connections no module made: Leviticus 27:30 has degree 5 in
tithes and 2 in wages, union 7, an argument existing in neither reading. Two pages
side by side with a shared co-citation list may simply be better.
*Needs:* Ethan, after someone builds module two and the eight-line co-citation
reporter. The honest answer comes from looking, not arguing. Depends on Q3.

**Q7 · The first module can never have an honest discovery ledger — exempt it, or
accept that it never lints clean?**
It was built before any procedure existed. Backfilling a ledger would forge exactly
the evidence such a check exists to provide.
*Needs:* Ethan, and only once a skill with a ledger actually exists. Parked.

---

## Blocking nothing yet, but it will fester

**Q8 · "Versicon" means two incompatible things and nobody has reconciled them.**
The Lexiconomicon — where the word is filed — defines a versicon as *the addressable
index itself*: a fixed corpus converted once into a unit-addressable form so every
citation is retrieved rather than recalled. That is `verses.json`. This project's
`DESIGN.md` and `lexicon.md` use it for *a subject module*. The project's own entry
admits the word "arrived without a traceable point of coinage". Under the register's
definition this project has exactly one versicon and what `DESIGN.md` calls versicons
have no name.
*Needs:* Ethan, as register-keeper. Note the register's entry is `archived`, so the
word is not in force in conversation either way. Whichever wins, the loser's
documents need a dated correction rather than a silent edit.

**Q9 · How do the branches of `versiconcordagraphs` relate to `main`?**
Deferred deliberately on 22 Sept. `main` holds the branch rule and nothing else; each
topic is an independent branch with unrelated history. The live question is whether
they ever compile, which is Q6 in another costume.
*Needs:* Ethan, after Q6.

---

**The question worth asking him first:** *which of these actually matters to you this
month?* Q1 is the only one that changes what the research says. Q3 is the only one
that is currently costing anything. The rest can wait, and the ranking above is one
agent's read of risk, not his priorities.
