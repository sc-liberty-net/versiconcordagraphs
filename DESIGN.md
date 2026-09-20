# Design decisions — the versicon module format

A **versicon** is one self-contained subject module: a corpus of verse nodes,
its connections, its groups, and the graph built from them. This module
(tax, tithe and tribute) is the first. The long-term goal is to compile many
versicons into a Master Versicon.

Three decisions had to be made before the second versicon existed, because
each one was cheap then and expensive to retrofit. **All three are settled and
implemented.** What follows is what was decided, and where the decision
differs from the recommendation originally written here.

---

## 1. Node ids are namespaced — SETTLED

**Problem.** Ids were bare: `g1`, `u1`, `z9`. Two versicons would both have a
`g1`, and compiling them produces silent collisions — edges attaching to the
wrong node with no error raised.

**Decided.** Ids are prefixed with the module slug at build time: `tithe:g1`.
The CSVs stay bare and readable; nobody types the prefix.

**Two changes from the original recommendation.**

The recommendation said "keep the prefix out of the CSV". As stated that makes
a cross-module edge inexpressible — every id in the edges CSV would receive
this module's prefix, so no edge could ever point at another module. That is
the whole purpose of a Master Versicon. The rule implemented is narrower:
**a bare id gets the prefix; an id that already contains a colon passes
through untouched.** Cross-module references are therefore written by
qualifying them by hand (`sacrifice:g1`), and they read as obviously
cross-module in the CSV.

The recommendation also did not say where the module slug lives. A
command-line flag would mean the same CSVs build to different ids depending on
how the script was invoked — the same silent-collision failure, relocated. The
slug lives in **`module.json`** (`slug`, `title`), which travels with the
module and cannot be forgotten.

Edges pointing out of this module are validated but **held back** from the
single-module page, which has no node to attach them to; the build prints how
many it held. The master compile is where they land.

Separator: `:` is safe. Node ids reach the renderer only as JavaScript object
keys and Set members, never as DOM ids or CSS selectors, so nothing needs
escaping.

---

## 2. Cluster definitions live in a per-module CSV — SETTLED

**Problem.** `build_graph.py` hardcoded the sixteen groups and their colours,
so it could not build a second module without being edited.

**Decided.** `corpus_clusters.csv`, with columns `key, name, light, dark,
role`. The build script reads it and still validates that every node's cluster
appears in it.

**The important change from the original recommendation.** Moving the colour
table was the easy half and would not have unblocked a second module. The
renderer hardcoded the cluster key `bridge` in two load-bearing places
*outside* the generated block, where `build_graph.py` never reached it: the
layout pinned that cluster to the centre (radius 0 while every other cluster
sits on a 320 ring) and gave its nodes a fixed larger dot. **`bridge` was a
layout role, not a colour.** A second module naming its hub anything else
would have had its centre flung onto the ring and the graph's whole shape
would have collapsed.

Hence the `role` column. Exactly one cluster may be marked `hub`; the renderer
asks which cluster holds the role and no longer knows any cluster by name. A
module that marks none gets a ring with an empty centre, which is legitimate.

Two smaller additions:

- A cluster defined but used by no node is reported as a **corpus note**, not
  a failure — staging a cluster before populating it is legitimate, but a dead
  legend entry burning a colour slot should not pass unremarked. These notes
  are counted separately from the check-by-eye list so neither number pollutes
  the other.
- **Row order is now an editorial control.** Cluster order drives both the
  legend and the position of each cluster around the layout ring. Order the
  CSV deliberately.

**The open sub-question is closed by folding it into decision 3.** Whether the
Master Versicon keeps each module's groups or re-groups globally is a
rendering decision, not a data-format one, and every module carrying its own
clusters file keeps it fully open. It is the same question as "what colour is
a shared node when two modules are active", which decision 3 answers.

---

## 3. Reference is identity; everything else is module-scoped — SETTLED

**Problem.** Leviticus 27:30 belongs in a tithe versicon and in a sacrifice
versicon, with a different summary in each, written for a different argument.
When the two compile, what happens?

**Decided.** The third of the three options originally listed — reference as
identity, the module's reading scoped to the module. The reasoning stands: the
whole finding of the corpus is that a verse does different work in different
frames, and a merge rule that discards that throws away the result.

**The change from the original recommendation is that it said "a summary per
module", and summary is not the only module-scoped field.** Three are:

- **Summary.** As originally stated.
- **Cluster.** The same verse sits in a different cluster in each module, so
  with two modules active a shared node had no defined colour. The original
  wording did not cover this.
- **Edge membership.** Both modules' edges bind to the one node, so its degree
  becomes the union of two arguments — and dot size is computed from degree.
  It would render as a hub existing in neither module's actual reading.

So the rule is stated as **reference is identity; everything else is
module-scoped.** The node is a bare shared anchor and each module hangs its
own reading on it. Warrant needs no rule because edges are never merged —
worth writing down rather than leaving to be inferred.

**Enforced now, with one module:** within a module a verse may be cited at
most once. The build refuses otherwise, because a second citation inside one
module is indistinguishable from a typo, and the master compile could not tell
genuine cross-module sharing from local duplication. Every node carries its
module in the generated block, and the renderer groups nodes by reference, so
the multi-module path exists and is exercised — it simply finds one reading
per verse today.

When more than one module is active, module identity becomes the primary
colour and cluster becomes secondary. That is the answer to decision 2's
sub-question.

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
summarise a different one, and nothing would catch it. The check-by-eye list
flags a node when no content word of its summary appears in the indexed verse
— crude, and it catches only the worst cases. Read it; do not ignore it.
