# Lexicon

Coined terms used in this project. Each entry gives the word, its
construction, and what it means. Add new entries at the bottom with the
date they were coined.

---

## contaxt

*Portmanteau: context + tax.*

The standing token cost that project instructions and knowledge files
levy on every conversation in a project. Everything in the instructions
box loads before the user types anything, so it is charged once per
chat regardless of whether that chat needs it.

**Why it matters:** contaxt is a good trade for durable context (who
the audience is, what the standard for done is) and a bad trade for
anything that could be said in the moment. Per-task requests parked in
the instructions box are pure contaxt.

---

## ghost-citation

A chapter-and-verse reference — or any citation — that sounds right,
scans right, and either does not exist or does not say what is claimed
of it. The characteristic failure mode of a model asked to work from
memory rather than from retrieved text.

**Why it matters:** an honesty instruction does not prevent
ghost-citations, because the model producing one is not aware it is
inventing. Only a sourcing rule prevents them: quote solely from text
retrieved in that turn, and mark recalled references as recalled.

---

## warrant-tagging

Marking each proposed reading or connection with how much weight the
source text actually puts behind it, rather than presenting all
findings at one confidence level.

**Standard three tiers:**

- `[text states]` — the text says this directly.
- `[text supports]` — a reasonable reading, but inferred.
- `[speculation]` — constructed by the reader; the text does not link these.

**Why it matters:** instructions that reward associative reading
(metaphor, motif, unorthodox connection) reliably manufacture
connections. A fabricated *connection* is not a fabricated *fact* —
every citation can be real while the link between them belongs to the
reader. Warrant-tagging is the only counterweight that catches this.

---

## agentglut

*Portmanteau: agent + glut.*

Agentic tooling rules — subagent delegation, spawn limits, parallel
task budgets — sitting in instructions for a surface where those tools
do not exist. Pure contaxt: the rules cannot fire, but they load every
time.

**Why it matters:** instructions written for one surface get copied to
another. Rules should live where their tools live.

---

## folderscope

The act of choosing which folder an agentic session works in, and
staging that folder with the source materials, templates, and context
the task needs before starting.

**Why it matters:** the folder choice determines what the session can
see. A well-scoped folder is the difference between a revision pass
grounded in the whole evidence base and one working from a single
pasted draft.

---

## concordagraph

*Portmanteau: concordance + graph.*

A traversable network of source references in which nodes are
locatable citations and edges carry both a **type** and a **warrant**.

**Edge types:**

- `lexical` — shared vocabulary, phrasing, or names.
- `referential` — one passage explicitly invokes another.
- `conceptual` — thematic or structural parallel.

**Edge warrants:** the three tiers under warrant-tagging above.

**Rules of admissibility:** an edge is admissible only when it names its
type, carries its warrant tier, and both endpoints resolve to real,
retrieved references. Speculative edges are rendered differently from
stated ones and are never silently promoted.

**Why it matters:** a graph that renders all edge types identically
launders speculation into settled reference. The visual distinction is
not decoration — it is the verification surface.

---

## versicon

*Portmanteau: verse + lexicon.*

One self-contained subject module: a corpus of verse nodes, its connections,
its groups, and the graph rendered from them. Many versicons compile into a
Master Versicon.

**Note on origin:** the word arrived in the project without a traceable point
of coinage — it is not in this session's record. Recorded here as adopted
rather than attributed, because a wrong attribution is worse than an unknown
one.

**Why the distinction matters:** a *concordagraph* is the rendering; a
*versicon* is the thing rendered. The same versicon could be drawn as a graph,
an arc diagram, or a table without ceasing to be itself.
