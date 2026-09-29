# Codifying the concordagraph — what the design pass found

22 September 2026. Fourteen agents: five surveyed the machinery, three designed
the skill from different angles, three judged, one authored a draft, two attacked
it. ~1.8M tokens, no failures.

**Headline: the diagnosis is strong and the draft skill is not shippable.** I am
not installing it. Below is what was actually established, what broke, and the
five decisions that are yours.

---

## 1. The good news, and it is bigger than expected

One agent did the thing nobody had done: **it built a real second concordagraph.**
A "wages" module — 12 nodes, 2 clusters, its own hub, ids `g1`/`g2` deliberately
colliding with the tithe module's, six verses the tithe corpus already cites, and
a cross-module edge. Then it ran your actual `build_graph.py` on it.

Everything the three settled decisions promised, it delivered:

- **It built green with no edit to any script.** The machinery is genuinely
  module-agnostic now.
- **Namespaced ids did not collide.** Decision 1 works.
- **Per-module clusters and the `role` column worked.** Decision 2 works.
- **The same six verses carried different summaries and different groups in two
  modules without a single complaint.** Decision 3 works — reference is identity,
  everything else module-scoped.
- **Schema drift fails loudly.** Pointed at the pre-decision corpus, the build
  exits 1 and the lint exits 3. No silent wrong answer.

And it produced a real finding about the *form itself*:

> **Leviticus 27:30 has degree 5 in the tithe module and degree 2 in wages.
> Union: 7 — an argument that exists in neither reading.**

That is the thing you were hoping for, demonstrated rather than argued. It is also
the warning: a compiled graph asserts connections no module actually made.

---

## 2. Where the drafted modularity plan broke

Four places. Two are fatal to its own goal.

**The compile gate is unsatisfiable.** The draft says a module must "lint clean"
to be compiled. Measured: your live tithe module exits **2**, and the draft
forbids the only remedy. Separately, a module built to be perfectly clean exits 0
— until you add one cross-module link, after which it exits 1 forever. So passing
requires having no cross-module links, and having them is the entire point.

**Namespacing the cluster table kills the page.** `build_graph.py` emits cluster
keys bare and unquoted, so `tithe:anchor:{...}` is a syntax error. The draft calls
it one edit; it is three. And it does not fix the hub: two modules give two
`role:hub` rows, `Object.keys(CL).find(...)` takes the first, and module two's
declared centre gets flung onto the ring — **the exact failure the `role` column
was introduced to prevent.**

**It quietly contradicts Decision 1.** DESIGN.md says a cross-module reference is
written qualified inside `corpus_edges.csv`. The draft's linter refuses exactly
that syntax — while claiming to build on the settled three. DESIGN.md forbids
reopening them.

**The payoff needs none of the apparatus.** The agent computed the full
co-citation set across both modules **in eight lines from two `corpus_nodes.csv`
files** — no links file, no namespaced keys, no master format. It found all six
shared verses.

---

## 3. The honest answer on modularity

Smaller than what anyone drafted, and I think it is right:

1. **Keep namespaced ids.** Proven to work under collision.
2. **Do not build a master compile yet.** Build the co-citation *reporter* — eight
   lines, works today, answers "which passages does more than one topic claim, and
   what is each saying about them?" That is the actual research question.
3. **Do not namespace the cluster table** until the hub problem has an answer.
   It is three edits and a design decision, not one edit.
4. **Compare before you compile.** Two pages side by side with a shared
   co-citation list may simply be better than one canvas. Nobody knows, because
   until today nobody had two modules. Now the cheap experiment exists.

**What is genuinely hard** is not the plumbing. It is that a compiled graph
*makes claims no module made* — Leviticus 27:30's degree-7 union being the proof.
Every warrant tier is preserved and the union is still an argument nobody
advanced. That is the real problem, and no amount of id-namespacing touches it.

---

## 4. Why the draft skill is not installable

The completeness critic found it not runnable, with receipts:

- **No first step.** Its headline use is "start a new one on wages" — and nothing
  creates `module.json`, the CSVs, or an HTML with the `// <corpus>` markers.
- **Its own engine contradicts itself.** The expansion tool emits stems, the
  search tool matches whole words. Its showcase term `changer` returns 0 hits;
  the index has `changers`.
- **Every path in its quick start is wrong** for the only module that exists.
- **Step 0 is described as a check and is a destructive rebuild** that dies on a
  fresh clone, since `nrsv.txt` is gitignored.
- **Its strongest-advertised gate is weak**: the provenance check admits ~1,364
  references for a 151-node corpus.

None of that is unfixable. All of it means "not yet."

---

## 5. Three things about *your live corpus*, verified and logged

Room tasks **57, 58, 59**.

**57 — high, and silent.** A cluster key that is not a bare JS identifier builds
green and ships a **blank page**. Proved across four key shapes:
`money-changers`, `2nd-temple`, `temple.tax`, `money changers` — all exit 0,
all "wrote 151 nodes, 170 edges", all a JavaScript syntax error. Your sixteen
keys are single lowercase words, which is the only reason it has never fired.
**Two-line fix, not done** — you were away and it is live code.

**58** — three passages carry no connection at all: `i3` Luke 3:1, `c4` Matthew
10:3, `c13` Luke 15:1.

**59** — two passages can only ever carry one connection between them; the
duplicate check ignores the kind. Nothing lost yet (zero collisions today), but
it means a pair can never record both shared wording *and* a shared idea.

---

## 6. The five decisions that are yours

1. **Fix 57 now?** Two lines. Blocks any second concordagraph with a two-word
   group name.
2. **`i3`, `c4`, `c13`** — connect, remove, or keep and record why?
3. **One edge per pair, or several?** Either is defensible; it should be written
   down as a decision rather than left as tool behaviour.
4. **Compare or compile?** Build module two and the co-citation reporter, and let
   the answer come from looking.
5. **The first module has no discovery ledger** and cannot honestly get one — it
   predates any procedure. Exempt it, or accept that it never lints clean?
   Backfilling would forge exactly the evidence the check exists to provide.

---

## 7. What I would build next, in order

1. The two-line fix for 57.
2. The co-citation reporter — eight lines, real answers today.
3. A `versicon_init` that scaffolds module two. *Then* write the skill, from a
   procedure that has actually been run twice rather than described once.

The skill should be written after the second concordagraph exists, not before.
Everything that broke in this pass broke on contact with a second module — which
is the strongest possible argument for building one before codifying anything.
