# Design decisions — the versicon module format

A **versicon** is one self-contained subject module: a corpus of verse nodes,
its connections, its groups, and the graph built from them. This module
(tax, tithe and tribute) is the first. The long-term goal is to compile many
versicons into a Master Versicon.

Three decisions have to be made before the second versicon exists, because
each one is cheap now and expensive to retrofit. My recommendation is given
for each; none is settled.

---

## 1. Node ids must be namespaced

**Problem.** Ids are currently bare: `g1`, `u1`, `z9`. Two versicons will
both have a `g1`, and compiling them produces silent collisions — edges
attaching to the wrong node with no error raised.

**Recommendation.** Prefix every id with the module slug: `tithe:g1`,
`sacrifice:g1`. Keep the prefix out of the CSV and add it at build time from
a module name, so the CSVs stay readable and no one has to type it.

**Consequence if deferred.** Every existing corpus has to be rewritten later,
and any edge that silently bound to the wrong node has to be found by hand.

---

## 2. Cluster definitions must move out of the build script

**Problem.** `build_graph.py` hardcodes the sixteen groups and their colours.
Every versicon needs its own groups, so the script currently cannot build a
second module without being edited.

**Recommendation.** A third per-module file, `corpus_clusters.csv`, with
columns `key, name, light, dark`. The build script reads it and validates
that every node's cluster appears in it — which it already does against the
hardcoded table, so the check survives the move.

**Open sub-question.** Whether the Master Versicon keeps each module's groups
or re-groups globally. Keeping them means sixteen groups times N modules,
which no legend can carry. Probably the master needs a second, coarser
grouping layer, with module identity as the primary colour.

---

## 3. Shared nodes need a merge rule

**Problem.** Leviticus 27:30 belongs in a tithe versicon and in a sacrifice
versicon, with a different summary in each, written for a different argument.
When the two compile, what happens?

**Three options.**

- **Union by reference.** One node per verse; summaries concatenated or one
  chosen. Produces a genuine graph but flattens the fact that the same verse
  does different work in different arguments.
- **Keep both, link them.** Two nodes, joined by an automatic `same-verse`
  edge. Preserves each module's reading; inflates node count and makes the
  master denser than any module.
- **Reference as identity, summary as module-scoped.** One node, carrying a
  summary per module, shown according to which module the reader has active.
  More work in the renderer; the only option that loses nothing.

**Recommendation.** The third. The whole point of the corpus is that a verse
means different things in different frames — a merge rule that discards that
would be throwing away the finding.

---

## What is already decided and should not be reopened

- **Warrant tiers** (`states` / `supports` / `spec`) and **edge kinds**
  (`lex` / `ref` / `con`) are stable. They are validated fields, not prose
  conventions.
- **The build script refuses to write on any validation failure.** This has
  caught real errors twice. It is not a warning system.
- **Verse text never travels with the graph.** References and summaries ship;
  the NRSV payload is generated locally and stays there.
- **The corpus lives in CSVs, not in the HTML.** The block between the
  `// <corpus>` markers is generated output.

---

## Known residual hole

The validator proves a reference **resolves**. It does not prove the summary
**describes** the verse it points at. A node could cite a real verse and
summarise a different one, and nothing would catch it. Worth a check that
flags a node when no content word of its summary appears in the indexed
verse — crude, but it would catch the worst cases.
