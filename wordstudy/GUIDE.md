# Drafting guide: the word-study readings

This is the method of the Biblography Word Study, written down so that every verse is
drafted the same way, by whoever drafts it. The pilot (`../study-pilot/`) is where it was
worked out; `authored/p2.json`, `authored/q4.json` and `authored/h5.json` are finished
examples in the current format. Read one Greek and one Hebrew example before drafting.

For each verse you get a brief, `digest/<id>.txt`, built from the sources by `extract.py`.
You write one file, `authored/<id>.json`. Then run `python check.py <id> ...` and fix
everything it reports. A draft that does not pass `check.py` is not finished.

## What you write

```json
{
  "id": "p2",
  "en":  [ {"t": "Then", "w": ["02"]}, " ", {"t": "the one", "w": ["04"]}, ... ".’" ],
  "words": {
    "01": {"s": ["came forward", "approached"], "r": "One sentence: what it means here.",
           "n": "Optional note.", "t": ["came", "came", "came", "came", "having come", "came"]},
    ...
  },
  "lxx": { ... }        // Hebrew verses only
  "tr_note": "..."      // optional, Greek verses only
}
```

### `en`: our English sentence

This is **our own literal translation** of the verse, built as a list of pieces:

- `{"t": "came forward", "w": ["01"]}`: English that translates the original word(s) listed.
  When one English phrase covers several original words, list them all, the main word
  first: `{"t": "you did not sow", "w": ["20", "19"]}`.
- `{"t": "one", "sup": "Supplied in English. The Greek leaves the subject unstated."}`:
  English that adds meaning nothing in the original carries. It is shown in italics, as
  the KJV prints its added words. Use it sparingly and give the reason.
- `" and "`, `", "`, `".’"`: plain strings are punctuation, spaces, and small English
  glue (an "a", an "and" joining a participle to its verb) that adds no meaning.

**Every original word must appear in exactly one piece.** Articles, conjunctions and
particles included: put them in their own piece or in the piece they belong to.

How to translate:

- **Literal, but English.** Follow the original's wording and, where English allows, its
  order. Keep tense, voice and person. Do not paraphrase, smooth, or explain in the text;
  explanations go in notes. Where a literal rendering would mislead a modern reader, use
  the closest faithful English and say in a note what the literal form is.
- **Modern English.** "you", not "thou"; "look", not "behold"; no archaic verb endings.
- **Consistent.** Use the renderings in the register below. The point of the register is
  that our English keeps apart what the original keeps apart: if the Greek has three
  different words for taxes, the reader of our English must be able to see three.
- Proper names in their usual English spelling.
- Never use an em dash or an en dash anywhere. Use commas, colons, parentheses or full stops.

### `words`: one entry per original word, keyed by its number in the brief

- `s`: 2 to 5 other English words or phrases that could stand in **this** sentence, closest
  first. These are the hover. They must fit the context, not list every sense in the
  lexicon. For a plain function word, one or two are enough ("the"; "and", "now").
- `r`: one sentence, what the word means **in this verse**. Plain words.
- `n` (optional): a note, at most three sentences, only where there is something a careful
  reader would want: a sense the lexicons record, a translation that diverges, a grammatical
  form that matters, a Greek or Hebrew word the English hides. Rules for notes:
  - Attribute lexicon facts by name (Gesenius, BDB, Abbott-Smith, Thayer) **only** when the
    brief shows that lexicon saying it. Never cite a lexicon from memory.
  - **Never add a Bible reference from memory.** You may name this verse, or another verse
    in the brief's lexicon text. Nothing else.
  - Mark your own inferences as such ("a reasonable reading", "likely"), and never present
    one as what the text states.
- `t`: how each translation in the brief renders this word, **in the brief's order**, copied
  exactly from that translation's text (its spelling, its capitals). `null` when a
  translation does not render the word. When its rendering is split, join the parts with
  `" ... "`. `check.py` verifies that every rendering occurs in that translation's text.

### `lxx`: the Septuagint (Hebrew verses only)

For each Hebrew word, the Swete Greek words that translate it, by their index in the brief:

```json
"lxx": {
  "_extra": {"1": "δὲ (and, but): added by the Greek translators; nothing in the Hebrew answers to it."},
  "01": {"i": [0], "m": 0},
  "09": {"i": [16], "m": 16, "lemma": "ἀναστρέφω", "strong": "G0390", "n": "Why the override."},
  "11": {"i": [19, 20], "m": 20, "n": "Note on the Greek choice."}
}
```

- `i`: the indices of the Greek words that translate this Hebrew word; `m`: the main one.
- A Hebrew word with no Greek counterpart is left out. A Greek word with no Hebrew
  counterpart goes in `_extra` with a short note. Every Greek index must be either paired
  once or listed in `_extra`, except where the brief says the verse is merged with its
  neighbour: then pair only this verse's words.
- `lemma` and `strong`: only to correct a dictionary form the brief marks as loose or missing
  and that you are sure of. Explain it in `n`.
- `n`: only where the translators' choice is worth knowing (a Greek word that shifts the
  meaning, an English word descended from it, the same Greek word used in the New Testament).

### `tr_note` (optional, Greek verses only)

When the brief lists Textus Receptus words, one or two sentences on what the KJV's Greek
text adds or reads differently here.

## The register: fixed renderings for this corpus

Use these unless the context makes them wrong; if you depart, say why in a note.

**Money, tax and tithe: keep these apart**

| Original | Our English | Not |
|---|---|---|
| τέλος (in a money sense) | toll | tax, custom |
| τελώνης | toll collector | tax collector, publican |
| τελώνιον | toll booth | tax office |
| φόρος | tribute | tax |
| κῆνσος | census tax | tribute, tax |
| δίδραχμον | double drachma | temple tax |
| στατήρ | stater | shekel, coin |
| δηνάριον | denarius (plural denarii) | penny |
| τάλαντον | talent | |
| μνᾶ | mina | pound |
| ἀργύριον | silver (money) | money |
| χρυσός, χρυσίον | gold | |
| δεκάτη | tenth | tithe |
| ἀποδεκατόω, δεκατόω | tithe (verb), take a tenth | |
| ἐλεημοσύνη | alms | charity, giving |
| θησαυρός | treasure; θησαυρίζω: store up treasure | |
| γαζοφυλάκιον | treasury | |
| ὀφείλω | owe; ὀφειλή, ὀφείλημα: debt | |
| τόκος | interest | usury |
| μισθός | wage(s) | reward, unless the context is not pay |
| ἀποδίδωμι | give back (render, where it is an obligation) | |
| Καῖσαρ | Caesar | |
| מַעֲשֵׂר | tithe | tenth |
| עָשַׂר (verb) | tithe | |
| תְּרוּמָה | contribution | heave offering |
| מִנְחָה | offering (note when it means tribute to a ruler) | |
| נֶשֶׁךְ | interest (note: from a root meaning "bite") | usury |
| תַּרְבִּית, מַרְבִּית | increase | |
| מַס | forced labour, levy (follow the brief's lexicons) | tribute, unless they say so |
| כֶּסֶף | silver | money |
| שֶׁקֶל | shekel | |
| עֵרֶךְ | valuation | estimation |
| פָּדָה | redeem | |
| נַחֲלָה | inheritance | |

Added 13 Oct 2026, for the kings, empires and inheritance passages:

| Original | Our English | Not |
|---|---|---|
| מִנְחָה where STEPBible tags it H4503I (tribute to a ruler) | tribute, with a note that the word is the one rendered "offering" elsewhere | |
| מִדָּה, מִנְדָּה (Aramaic) | tribute | tax |
| בְּלוֹ (Aramaic) | duty | tax, custom |
| הֲלָךְ (Aramaic) | road toll, with a note that the Greek τέλος is "toll" elsewhere | |
| סֵבֶל | burden-labour | |
| עֹנֶשׁ | fine | tribute |
| נָגַשׂ | press, drive; the participle: taskmaster | exact (kept for the creditor verb נָשָׁה) |
| עָרַךְ (of a levy) | assess | |
| חֵלֶק | portion | share, unless the context is a division |
| נָחַל | inherit, take as an inheritance | possess |
| אֲחֻזָּה | holding | possession |
| κληρονομία, κληρονόμος, κληρονομέω | inheritance, heir, inherit | |
| μερίς | portion | |
| οὐσία | property | goods, substance |

**People and God**

| Original | Our English |
|---|---|
| יהוה | the LORD (small capitals in print; write "the LORD") |
| אֱלֹהִים | God |
| אֲדֹנָי | the Lord |
| κύριος | Lord (of God or Jesus); master (of a human owner) |
| θεός | God |
| Ἰησοῦς, Χριστός | Jesus, Christ |
| ὁ υἱὸς τοῦ ἀνθρώπου | the Son of Man |
| ἡ βασιλεία τῶν οὐρανῶν | the kingdom of the heavens |
| ἡ βασιλεία τοῦ θεοῦ | the kingdom of God |
| גֵּר | sojourner |
| יָתוֹם | fatherless (one) |
| אַלְמָנָה | widow |
| עָנִי | poor (note "afflicted" where it matters) |
| ἁμαρτωλός | sinner |
| Φαρισαῖος, γραμματεύς | Pharisee, scribe |
| ἱερεύς, Λευίτης, ἀρχιερεύς | priest, Levite, high priest |
| ἱερόν, ναός | temple, sanctuary |
| ἐκκλησία | assembly (note "church" where the reader will expect it) |
| δοῦλος, עֶבֶד | slave (note "servant" where the context is service) |

**Common words**

| Original | Our English |
|---|---|
| ἀμήν | Amen (as the word itself; "truly" goes in the hover) |
| ἰδού, הִנֵּה | look |
| λέγω, εἶπον | say, said |
| ἄνθρωπος | man, human (person where the text means anyone) |
| ψυχή, נֶפֶשׁ | soul, life (choose by context and note it) |
| καρδία, לֵב | heart |
| πᾶς, כֹּל | all, every |
