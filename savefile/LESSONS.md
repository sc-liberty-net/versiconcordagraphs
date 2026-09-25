# Lessons — how to work here

**Append only.** Correct an entry with a dated sequel beneath it.

This is what *worked*. `HAZARDS.md` is what went wrong — where an incident produced
both, the symptom lives there and the method lives here, with a pointer. Nothing here
repeats `../CLAUDE.md` or `HANDOFF.md`.

Entries are from the session of 20–22 September 2026 unless dated otherwise.

---

## Working With Ethan

**He runs nothing himself.** Execute it and report the outcome, not the incantation.
If he explicitly asks for a command, it goes in a `powershell`-tagged block, tested
with the PowerShell tool first — the Run button in his panel is locked to PowerShell
regardless of the tag, so a bash-syntax block gets a button that fails.

**Give him a link, not a path.** Anything he can look at gets a URL he can open from
his phone, in the same reply that reports the change. "Pull it up" means his Firefox,
opened on the local file — not the browser pane, which is for Claude's own checking.

**Unrelated problems get logged, not fixed.** This is the rule most likely to be
broken by a capable agent, because fixing the thing in front of you feels like
service. It is not: it widens a change he did not ask for, while he is not watching.
Log it in the Mission Control Room with the evidence and say so in a line. Task 57 —
a two-line fix for a bug that ships a blank page — was deliberately left undone for
exactly this reason.

**He reads the numbers.** Vague confidence gets caught. "The arcs are thicker now" is
worth less than "2.4 / 1.9 / 1.4 screen pixels at any zoom, measured". This cuts both
ways: it means a number you have not actually measured will be noticed.

**Labels, when there are three or more of anything.** F1, D1, O1, R1, Q1, A1 for
findings, decisions, options, risks, questions, actions — and keep them stable across
the conversation once assigned.

**Ask before saving anything to memory.**

---

## Technique That Earned Its Place

**Drive the gesture, not the handler.** The single most expensive mistake of the
session. Clicking was verified by calling `select()` directly, which passed, and
shipped — twice — while every real click was being swallowed before it reached the
function. Testing the API is not testing the interaction. If the thing under test is a
click, something has to click; if it is a drag, something has to drag. When a
verification and a user disagree, suspect the layer the verification never touched.

**Prove a check red before trusting it.** Twelve new validation rules were each run
against a build constructed to violate them — two hubs, a misspelled role, a duplicate
cluster key, a verse cited twice, a dangling edge, a colon in the slug, each config
file missing. All twelve refused; the suite is in the session scratchpad and was not
kept. The same discipline caught the index reconciliation: it was run against a forged
baseline carrying the old figure and seen to exit 1 naming `verses -77`, `Mark -5`,
`Acts -4`. A check nobody has watched fail proves nothing.

**Label a hypothesis as a hypothesis, and then go kill it.** The missing verses looked
obviously caused by having the wrong `pdftotext`. That was reported as a hypothesis,
not a cause — and testing it showed the opposite (`DEAD-ENDS.md`). Had it been
reported as the answer, the "fix" would have been to install the other extractor,
which makes the index measurably worse, and everyone would have believed it repaired.

**Count, then reconcile.** You cannot read what is missing; the dropped material is
not there to be read. Only a count compared against a number recorded earlier finds a
silent loss. Where the data itself cannot be kept — here, because it is copyrighted —
**keep its measurements**. `index-baseline.json` holds counts only, commits cleanly,
and is what turns an invisible regression into a failed build.

**Classify a failure rather than thresholding it.** The old health check summed two
unlike things into one "gappy" number. Separating *a gap of one or two between present
items* (a dropped verse) from *a long run of absent ones* (a known tail artifact) made
both legible: 114 verses in 110 places, against 23 harmless runs.

**Ask the corpus, do not recall it.** Every reference in the analysis was pulled from
`corpus_nodes.csv` and checked against the index by script. The one claim that came
from an earlier session's memory — "tithing was abolished" — turned out to be already
in the graph, correctly tagged `spec`, and repeating it as a finding would have been
the exact promotion the warrant tiers exist to prevent.

**Read the whole published version before republishing.** The gate is mechanical and
a diff is not accepted as evidence. It cost roughly 45k tokens twice. Both times it
was right: another session had genuinely changed something.

---

## Tooling, Specifically In This Environment

- **`pdftotext` here is Xpdf 4.06**, shipped with Git for Windows at
  `C:\Program Files\Git\mingw64\bin`. It is *not* Poppler, and the two extract
  differently. `nrsv_index.py` was written against Xpdf's reflowed output.
- **Poppler 25.07.0 is also installed now** (winget, `oschwartz10612.Poppler`), on
  PATH. Harmless; `pdfinfo` and `pdfimages` are occasionally useful. Remove with
  `winget uninstall --id oschwartz10612.Poppler`.
- **`node` is available** and `node --check` on the extracted `<script>` block is the
  fastest way to catch a broken generated page. Worth running after any change to
  `build_graph.py`'s emit.
- **The shell guards block two things** that will otherwise waste a cycle: a heredoc
  piped into an interpreter, and a multi-line `-c` / `-Command` script. Write the
  script to the scratchpad and run the file. This is also better practice — the
  project's own history has three incidents of mangled backslashes.
- **The browser pane's screenshot frame is not the viewport.** Take a screenshot, read
  the reported frame size, get `innerWidth` from the page, scale, and confirm with
  `elementFromPoint` before clicking. See `HAZARDS.md`.
- **Never read `verses.json` or `nrsv.txt` into context.** Tens of megabytes of
  copyrighted text. Query with a script and print only counts or the few lines needed.

---

## About This Project Specifically

The numbers that anchor most conversations:

| | |
|---|---|
| Corpus | 151 passages, 170 connections, 25 books, 16 groups |
| Warrants | 93 `states`, 57 `supports`, 20 `spec` |
| Edge kinds | 129 `con`, 26 `lex`, 15 `ref` |
| Index | 37,465 verses, 1,406 chapter markers, 114 known holes |
| Check by eye | 11 nodes, unchanged across every build this session |

**The corpus is 46 Old Testament passages out of 151.** The project's own page called
itself New Testament for months. It is not, and the finding depends on that: the
tangle starts at 1 Samuel 8:15, where the king takes a tenth.

**Eight of the eleven check-by-eye nodes are synoptic parallels** and are almost
certainly fine — the heuristic fires when a summary shares no content word with its
verse, and "Mark's form of the ruling" legitimately shares none. The list is not a bug
list. It has printed the same eleven ids on every build this session.

**The Mission Control Room is the task list**, not this savefile. Room tasks 49–59 are
Biblography's. `TODO.md` here ranks them by what they block; the Room holds the full
record of each.

---

## Appended 25 September 2026

**Ethan takes the blame for your errors. Do not let him.** Twice in one session he
wrote "I misspoke" about a mislabel that was mine. I had called the Alphaeus link "the
Matthew/Levi question" when the shared name is James and Levi; he adopted my wrong
label, then caught it and attributed the slip to himself. The same shape recurred with
"you said the three readings are rivals" — again my framing, not his. *Why it matters:*
if you accept the correction as his, the wrong label stays in your head and goes into
the next note. Check whose sentence it was before agreeing. 25 Sept.

**He argues back on substance, and he is often right.** He rejected "the three Hebrews
readings are rivals" and was correct: readings 1 and 3 contradict, reading 2 is
downstream of either. He rejected the cheap-herbs pushback twice and forced a reading of
Hebrews 7 that held up. *Do:* when he disagrees, read the chapter before restating your
position. The two times this session the disagreement was resolved by reading rather
than arguing, he was right and the corpus got better.

**"Can we not do all of the above?" is usually the right answer.** Offered a three-way
choice about which reading to encode as an edge, he asked why not all three. He was
right: the three targeted different nodes, so the one-edge-per-pair rule did not apply,
and an edge at `spec` records a connection rather than asserting a conclusion. *Do:*
before presenting a forced choice, check whether the format actually forces it.

**Verify by running the artifact, not by reading it.** Three consecutive "verified
live" reports were false because they grepped the served HTML for strings. See the
blank-page hazard. The general form: a check that reads a representation of the thing
proves something about the representation. 25 Sept.

**Print the population a check examined, never its verdict.** A boolean cannot say why
it is false. Two checks this session failed for reasons invisible until they were
rewritten to print numbers — a float comparison at 1e-9, and a motif probe measuring
selection dimming and motif dimming at once. Both looked like page bugs and were probe
bugs. This is the smoke-gate rule and it earned its place twice in one day.

**Prove a new assertion red on the build where it must fail.** The Q5 duplicate-edge
rule and the whole smoke suite were both proved by deliberately reintroducing the defect
and confirming the check fails. `prove_smoke.py` and `prove_q5.py` are the artefacts. An assertion nobody has seen fail proves nothing — and proving it caught a
real flaw in the suite, which crashed rather than reporting on the broken page.

**Trust the project's own checker over one you wrote to predict it.** A hand-rolled
gist checker passed a summary that `build_graph.py` then flagged, because the build
compares content words and the checker compared all words. If you write a pre-check,
say which instrument is weaker.

**Use `asserted-patch` for text files, and a CSV parser for the corpus tables.** Four
hand-rolled "count occurrences, refuse if not one" guards were written this session
before reaching for the skill that is exactly that. Its `zero` and `many` refusals
caught two real errors. It is the wrong tool for the corpus tables — Python's csv writer quotes fields
and a string patch then matches nothing, which is how one patch failed.
