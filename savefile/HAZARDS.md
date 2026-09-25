# Hazards — things that look right and are not

**Append only.** Correct an entry with a dated sequel beneath it, never by editing
the original. The original is the evidence.

Indexed by **symptom**, because you arrive holding a symptom and not a cause.
Nothing here repeats `HANDOFF.md` (state and decisions), `LESSONS.md` (what worked),
or `DEAD-ENDS.md` (what was abandoned). Where a hazard produced a method worth
keeping, the method is in `LESSONS.md` and this entry points at it.

All entries below are from the session of 20–22 September 2026 unless dated
otherwise.

---

## What you see on the page

**Green build, blank page.**
*You see:* `build_graph.py` prints `wrote 151 nodes, 170 edges` and exits 0. The page
opens white. No console error you would notice unless you look.
*Why:* cluster keys are emitted **unquoted** into a JavaScript object literal. Node
ids, refs, gists and the cluster *values* all go through `json.dumps`; the cluster
*key* does not. Any key that is not a bare JS identifier is a syntax error that kills
the whole generated block. Proved 22 Sept across four shapes — `money-changers`,
`2nd-temple`, `temple.tax`, `money changers` — each exit 0, each page broken.
*Do:* keep cluster keys to single lowercase words until the two-line fix lands (Room
task 57). The sixteen current keys are single words, which is the only reason this has
never fired in anger.

**Nothing on the graph responds to a click.**
*You see:* passages, arcs and book labels all look interactive, hover works, and
clicking does nothing at all. Shipped twice in this state.
*Why:* two unrelated causes at once. (1) The pan handler called
`svg.setPointerCapture` on pointerdown; pointer capture retargets the following
`click` to the capturing element, so arcs and labels never received their own. (2)
`hover()` re-appended the hovered node's `<g>` to lift its magnified label above
neighbours — SVG has no z-index — and detaching and re-inserting an element under the
cursor makes the browser never synthesise the click at all. Instrumenting `document`
showed `pointerdown`, `mousedown`, `pointerup`, `mouseup` all landing on the circle
with no `click` following.
*Do:* never grab the pointer on pointerdown if anything underneath needs a click, and
never re-append an element to fake z-index. See `LESSONS.md` for the testing mistake
that let it ship twice.

**An enormous rectangle appears when you click an arc.**
*You see:* a focus outline spanning most of the canvas.
*Why:* the browser draws a focus ring around an element's *bounding box*, and a long
arc's bounding box is huge.
*Do:* scope it with `:focus-visible` rather than removing it. Removing it outright
leaves keyboard users with nothing, because — see the next entry — the handlers that
would have replaced it do not run.

**Keyboard focus works and your focus handler never fires.**
*You see:* `document.activeElement` updates correctly, Tab moves, Enter activates —
and the `focus` handler attached to that SVG element is never called. `focusin` is not
dispatched either, not even on `document` with capture.
*Why:* at least one engine dispatches no focus events for SVG elements at all.
*Do:* do not make a focus event the only indicator on an SVG element. Treat any
focus-driven affordance there as unproven until you have watched it fire.

**Arc lines nearly invisible, and all the line styles look the same.**
*You see:* thin washed-out arcs; solid, dashed and dotted edges indistinguishable.
*Why:* stroke widths and dash arrays were in the drawing's own coordinates, so they
scaled with the zoom — and the graph opens fitted at roughly a fifth of full size. A
1.6-unit line lands under a third of a pixel, and the dash patterns collapse into
apparent solid lines, silently destroying the `lex`/`ref`/`con` distinction.
*Do:* use `vector-effect: non-scaling-stroke` for anything whose weight carries
meaning. Fixed in `66a6fa6`.

**The whole graph flickers while the pointer crosses arcs.**
*You see:* rapid light/dim strobing when sweeping across the arc field with nothing
selected.
*Why:* every crossing of a 12px hit stroke toggled a full lit/dim pass over 151 nodes
and 170 edges, and the gaps between arcs toggled it back.
*Do:* arc hover now drives the highlight only when something is already selected.
Discrete targets (passages, book labels) are fine to highlight on hover; a dense field
of thin targets is not.

**The panel keeps showing a selection you just cleared.**
*You see:* "Show everything again" clears the graph and the detail panel still shows
the old passage.
*Why:* the reset handler set `picked = null` and called `draw()` but never `render()`.
*Do:* when state has two renderers, clear through both. Pre-existing; fixed in
`f083569`.

**The page is blank and the HTML is perfect.**
*You see:* the served file contains every string you thought to check — the right
URLs, the right counts in `META`, all 25 book slugs resolving — and the page renders
nothing. No graph, no rail, no panel.
*Why:* a second `const HUB` collided with the hub-cluster constant further up the same
inline script. A duplicate `const` is a **parse** error, so not one line of the script
ran. Nothing that reads HTML as text can see this, and three separate verifications
passed against it across three pushes on 25 Sept. Ethan found it by opening the page.
*Do:* verify by **running** the page, not by reading it — `python check_page.py`. That
suite exists because of this incident, and `prove_smoke.py` reintroduces the defect to
prove the suite still catches it. Fixed in `dc5f849`.

**You fixed the blank page, deployed, and it is still blank.**
*You see:* your own re-check reports the old broken content minutes after a successful
deploy.
*Why:* GitHub Pages caches for about ten minutes and the browser caches on top of
that. A `curl` immediately after the push already showed the fix; the browser did not.
*Do:* append a cache-buster (`?v=2`) when checking, and tell Ethan to hard-refresh.
Do not re-fix a bug you have already fixed. 25 Sept.

**The header is enormous and the title wraps to four lines.**
*You see:* a 193px header where you expected 76px.
*Why:* measured inside the Claude browser pane, which was 468px wide. At desktop width
the title is one line. This was reported to Ethan as a defect before being checked at a
real width, which cost a round trip.
*Do:* measure layout at a stated viewport. `smoke_concordagraph.py` fixes 1400x900 for
exactly this reason. 25 Sept.

**A control does nothing in your test and works fine for a user.**
*You see:* clicking a group name appears to toggle its checkbox, which the code
explicitly prevents.
*Why:* the probe dispatched `new MouseEvent('click', {bubbles:true})`. That event is
**not cancelable** by default, so the handler's `preventDefault()` was a no-op and the
label's default activation fired. A real click is cancelable.
*Do:* `{bubbles:true, cancelable:true}` in any synthetic click testing a handler that
calls `preventDefault`. 25 Sept.

---

---

## What the data does

**The index loses verses and nothing fails.**
*You see:* a rebuild completes cleanly. Every lookup still answers confidently.
*Why:* the rebuild produced **37,465** verses where an earlier build of the same PDF
produced **37,542**. Nothing in the pipeline recorded a count, so nothing could
compare. The existing health check was a density threshold — flag a chapter under 90%
full — and a chapter of 28 that loses one verse sits at 96% and sails through. 114
verses are missing across 110 isolated places.
*Do:* `nrsv_index.py` now records `index-baseline.json` and reconciles every run
against it, exiting non-zero on drift. **A drift failure is a real failure** — do not
re-record the baseline to clear a red. It was caught only because an unrelated project
happened to record the old number in prose.

**A reference that is real and still will not resolve.**
*You see:* `build_graph.py` refuses a citation you can see in a printed Bible.
*Why:* the index has holes. Hebrews 7:19 is absent; so are 1 Kings 9:16, 2 Samuel
1:18, 1 Corinthians 7:11 and ~110 others, in books where the NRSV omits nothing.
*Do:* before adjusting a reference to make it pass, check whether the *index* is
missing it. Adjusting the citation until something matches is the exact failure
`CLAUDE.md` forbids.

**Twelve passages sorted before Genesis.**
*You see:* in Bible order, a dozen dots crowded at the far left with no label under
them.
*Why:* the page hardcoded an 18-book list; the corpus cites 25. `BOOKS.indexOf()`
returned −1 for the seven absent books, and −1 sorts before Genesis's 0.
*Do:* fixed in `66a6fa6` — the book order is now generated from the index in document
order, and the build refuses if a cited book cannot be placed.

**Summaries that quote the scripture they cite.**
*You see:* nothing. They read as ordinary paraphrase.
*Why:* 22 of 151 summaries contain a run of five or more consecutive words lifted from
the verse; the longest are nine, at nodes `i5` and `h2`. `CLAUDE.md` forbids NRSV
wording in summaries and nothing enforces it. These are in the files that **ship**,
while the copyright machinery guards only the payload that never leaves.
*Do:* Room task 51. Check a new summary against its verse before committing it.

**A motif catches a verse with nothing to do with it.**
*You see:* Hebrews 7:3 — "neither beginning of days nor end of life" — inside a motif
about tax and tribute.
*Why:* G5056 *telos* means **toll**, which is how the NRSV renders it in Matthew 17:25,
and it also means **end**. The lemma resolved; the sense did not. A Strong's number is
not a sense.
*Do:* when a motif catches something surprising, read the verse before defending the
lemma. Dropped from the tax motif in `8b9ccb1`; both genuine fiscal verses were already
caught by *kensos* and *phoros*, so nothing was lost. 25 Sept.

**Your gist checker passes and `build_graph.py` still flags the node.**
*You see:* a hand-rolled check reports the summary shares five words with its verse;
the build puts it on the check-by-eye list anyway.
*Why:* `build_graph.py` compares **content** words. A checker comparing all words counts
stopwords and reports a match that the build does not see. 1 Peter 1:18 shared only
"you", "not", "with".
*Do:* trust the build's list over your own. If you write a pre-check, exclude stopwords
or expect it to be the weaker instrument. 25 Sept.

**A whole book's verses are unreachable and every count looks right.**
*You see:* `Galatians` has 124 verses and `Galations` has 24; `Psalm` has 2,455 and
`Psalms` has 6. Both totals are correct.
*Why:* the extractor read a running head or heading variant as a second book name. The
verses are all present, filed under two spellings, and the ~30 in the smaller bucket
cannot be cited by any sanely written reference.
*Do:* do not add a node citing one. Room task 63. Fixing it means re-extracting and
deliberately re-recording `index-baseline.json`, which is Ethan's call. 25 Sept.

**One reference, two rows, and the lookup silently keeps the second.**
*You see:* `verses.json` holds 37,465 records but only 37,304 distinct references.
*Why:* 161 duplicates, every one in Esther, because the NRSV prints both the Hebrew
Esther and the Greek. `attach_verses.py` builds its lookup as a dict comprehension, and
a repeated key keeps the last value — so an Esther lookup returns one of two different
texts with no error anywhere. `nrsv_index.py` counts records, not distinct references,
so its reconciliation cannot see it either.
*Do:* no node cites Esther today. Room task 64 proposes asserting
`len(set(refs)) == len(records)` so the collision becomes a red. 25 Sept.

---

---

## What the tooling does

**A PDF that is fine on disk and broken in every clone.**
*You see:* nothing, until someone opens it. `git status` is clean.
*Why:* `core.autocrlf=true` and git guessed `findings.pdf` was text. A checkout
returned 11,554 bytes against 11,411 on disk — 143 inserted CRLFs into a format
indexed by byte offset. The warning does appear, worded like a formatting note and
buried among a dozen harmless ones.
*Do:* name binaries in `.gitattributes` (`*.pdf binary`) and prove it with
`git checkout-index --prefix=/tmp/co/ -a` then `cmp`. Caught before the first commit.

**`git check-ignore` tells you the opposite of the truth.**
*You see:* it prints the rule a file matched, which reads as confirmation that the
file is ignored.
*Why:* for a file matched by a `!` un-ignore rule it prints the rule **and** sets its
exit code to "not ignored". A script judging by whether output appeared gets it
backwards.
*Do:* judge by exit code, or just read `git status`.

**A publish refused, and forcing it would destroy someone's work.**
*You see:* "a newer version published elsewhere is live and this publish was not built
on it."
*Why:* another session had republished the same artifact mid-task. Happened twice this
session — once on the Fieldbook, once on the concordagraph.
*Do:* read the saved version **in full** — the gate is mechanical and a diff is not
accepted as evidence — then merge your edits onto it and publish again. Never pass
`force`. On the concordagraph the only change was a page title, and adopting it cost
nothing; assuming that without reading would have been luck, not judgement.

**The markdown source and the published page drift apart.**
*You see:* both look complete and healthy.
*Why:* the Fieldbook's markdown was two entries ahead of its published page — appended
by a session that never mirrored or republished. The skill keeps one copy precisely to
prevent this, and it happened anyway.
*Do:* compare entry counts on both sides before adding to either.

**Browser-pane coordinates do not match the viewport.**
*You see:* a click lands somewhere other than where you aimed, or produces no events
at all.
*Why:* the pane's screenshot frame and the live viewport are different sizes, and
`computer` clicks are in screenshot coordinates. A click computed from
`getBoundingClientRect` lands wrong.
*Do:* take a screenshot, read the reported frame size, get `innerWidth` from the page,
and scale. Verify with `elementFromPoint` before clicking.

---

**A multi-line patch matches nothing, and the text is plainly there.**
*You see:* `asserted-patch` refuses with `zero` on a pattern you can see in the file.
*Why:* `concordagraph.html` is **CRLF**; the patch was written with LF newlines. Single-line
patterns still match, so the failure looks arbitrary until you check. `build_graph.py`
and the Python files are LF, so the same patch file works on one and not the other.
*Do:* check the file's line endings first, then convert the patch's text fields.
`tools_crlfify.py` does exactly that, and did it for every page patch on 25 Sept.

**A test crashes and leaves its probe row in the real corpus.**
*You see:* `corpus_edges.csv` has 199 rows where it should have 198, and one of them
says `probe`.
*Why:* the red/green proof for the Q5 rule appended a deliberate duplicate, ran the
build, and restored from a snapshot — but the restore was after the print, and the
print died on a `UnicodeEncodeError` first.
*Do:* restore in a `finally`, not on the happy path. Any probe that mutates a real file
should be unable to leave it dirty. Caught and restored the same minute; the corpus was
verified back at 198. 25 Sept.

**An equality assertion fails on two numbers that are equal.**
*You see:* `zoom buttonsHeld: False` where the scales print identically to four decimals.
*Why:* the check asserted `Math.abs(a - b) < 1e-9` on floating-point scale factors that
agree to about 1e-4. A **verdict cannot say why it is false** — it took rewriting the
check to print the five scales before the cause was visible.
*Do:* print the numbers a check examined, not its opinion of them. That is the
smoke-gate rule and this is what it is for. 25 Sept.

**A probe returns a string and everything below it explodes.**
*You see:* `TypeError: string indices must be integers` halfway through the smoke
suite's own report, on a page that had already failed.
*Why:* the suite degrades a failed `page.evaluate` to a printed string, and the next
line did `box['w']`. On a dead page `#net g` does not exist, so `getBBox()` threw and
the suite died while reporting the very failure it exists to report.
*Do:* `ev()` degrades and `pick()` reads a key from either a dict or a string. A suite
that crashes gives the gate nothing to diff. 25 Sept.

## The pattern behind most of these

**Almost every entry above is a green check over a broken thing.** A build that exits
0 and writes a blank page. A commit that stores a file it will hand back corrupted. An
index that loses a sixth of a book and answers confidently. A verification that passes
because it tested the wrong layer.

None of them announce themselves, because each is a *check pointed slightly to the
left of what it is supposed to guard*. When something here surprises you, the useful
question is not "what is broken" but **"what did the check that passed actually
measure?"**
