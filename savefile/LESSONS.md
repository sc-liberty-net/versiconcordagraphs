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
