"""Shared readers for the word-study pipeline: STEPBible tagged texts and lexicons, Gesenius,
BDB, Thayer, Swete's Septuagint, the public-domain translations, and grammar-code decoders.

Nothing here reads NRSV text.
"""
import csv, glob, json, os, re, unicodedata, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "bible-sources")

# English book name (as corpus_nodes.csv writes it) -> STEPBible code, tagged-text file, Septuagint book
BOOKS = {
    "Genesis": ("Gen", "TAHOT Gen-Deu", "Gen"), "Exodus": ("Exo", "TAHOT Gen-Deu", "Exod"),
    "Leviticus": ("Lev", "TAHOT Gen-Deu", "Lev"), "Numbers": ("Num", "TAHOT Gen-Deu", "Num"),
    "Deuteronomy": ("Deu", "TAHOT Gen-Deu", "Deut"), "Ruth": ("Rut", "TAHOT Jos-Est", "Ruth"),
    "1 Samuel": ("1Sa", "TAHOT Jos-Est", "1Sam"), "Nehemiah": ("Neh", "TAHOT Jos-Est", "2Esd"),
    "Psalm": ("Psa", "TAHOT Job-Sng", "Ps"), "Ezekiel": ("Ezk", "TAHOT Isa-Mal", "Ezek"),
    "Amos": ("Amo", "TAHOT Isa-Mal", "Amos"), "Haggai": ("Hag", "TAHOT Isa-Mal", "Hag"),
    "Zechariah": ("Zec", "TAHOT Isa-Mal", "Zech"), "Malachi": ("Mal", "TAHOT Isa-Mal", "Mal"),
    "Matthew": ("Mat", "TAGNT Mat-Jhn", None), "Mark": ("Mrk", "TAGNT Mat-Jhn", None),
    "Luke": ("Luk", "TAGNT Mat-Jhn", None), "John": ("Jhn", "TAGNT Mat-Jhn", None),
    "Acts": ("Act", "TAGNT Act-Rev", None), "Romans": ("Rom", "TAGNT Act-Rev", None),
    "1 Corinthians": ("1Co", "TAGNT Act-Rev", None), "2 Corinthians": ("2Co", "TAGNT Act-Rev", None),
    "1 Timothy": ("1Ti", "TAGNT Act-Rev", None), "Hebrews": ("Heb", "TAGNT Act-Rev", None),
    "James": ("Jas", "TAGNT Act-Rev", None), "1 Peter": ("1Pe", "TAGNT Act-Rev", None),
}


def lxx_ref(book, ch, vs):
    """English chapter:verse -> Septuagint (Swete) reference, where the numbering differs."""
    lb = BOOKS[book][2]
    if book == "Nehemiah":          # Nehemiah is 2 Esdras 11-23
        ch += 10
    if book == "Psalm" and 10 <= ch <= 112:  # Hebrew Psalms 10-113 run one behind in the Greek
        ch -= 1
    return f"{lb}.{ch}.{vs}"


TRANS_ORDER = ["KJV", "Geneva1599", "DRC", "JPS", "ASV", "YLT", "BSB"]
TRANS_NAMES = {"KJV": "King James", "Geneva1599": "Geneva 1599", "DRC": "Douay-Rheims",
               "JPS": "JPS 1917", "ASV": "American Standard", "YLT": "Young's Literal",
               "BSB": "Berean Standard"}

CANTILLATION = re.compile("[֑-ֽ֯]")
GPUNCT = "··;,.;"  # middle dot, Greek raised dot, Greek question mark, comma, full stop


def heb(s):
    """Drop cantillation marks and meteg; keep letters, vowel points, maqaf and sof pasuq."""
    return CANTILLATION.sub("", unicodedata.normalize("NFC", s or ""))


def letters(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(ch for ch in s if "א" <= ch <= "ת" or "α" <= ch.lower() <= "ω")


def clean_def(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "", flags=re.I)
    s = re.sub(r"<ref='[^']*'>([^<]*)</ref>", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("__", "\n")
    s = re.sub(r"\s*\(AS\)\s*$", "", s)
    s = re.sub(r" (\d+[a-z]?\d*[a-z]?\d*\)) ", r"\n\1 ", s)  # TBESH's outline numbering onto new lines
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*", "\n", s).strip()


def clip(s, n):
    if len(s) <= n:
        return s, False
    cut = s.rfind(" ", 0, n)
    return s[: cut if cut > 0 else n].rstrip(" ,;") + " …", True


# ---- grammar codes, decoded to plain English -------------------------------------------
G_TENSE = {"P": "present", "I": "imperfect", "F": "future", "A": "aorist", "R": "perfect", "L": "pluperfect"}
G_VOICE = {"A": "active", "M": "middle", "P": "passive", "D": "middle", "O": "passive", "N": "middle or passive", "E": "middle or passive", "X": ""}
G_MOOD = {"I": "indicative", "S": "subjunctive", "O": "optative", "M": "imperative", "N": "infinitive", "P": "participle", "R": "participle (imperatival)"}
G_CASE = {"N": "nominative", "G": "genitive", "D": "dative", "A": "accusative", "V": "vocative"}
G_NUM = {"S": "singular", "P": "plural"}
G_GEN = {"M": "masculine", "F": "feminine", "N": "neuter"}
G_POS = {"N": "noun", "A": "adjective", "T": "article", "P": "personal pronoun", "R": "relative pronoun",
         "C": "reciprocal pronoun", "D": "demonstrative pronoun", "K": "correlative pronoun",
         "I": "interrogative pronoun", "X": "indefinite pronoun", "Q": "correlative or interrogative pronoun",
         "F": "reflexive pronoun", "S": "possessive pronoun"}
G_SIMPLE = {"CONJ": "conjunction", "ADV": "adverb", "PREP": "preposition", "PRT": "particle",
            "PRT-N": "negative particle", "PRT-I": "interrogative particle", "INJ": "interjection",
            "COND": "conditional particle", "ADV-I": "interrogative adverb", "ADV-N": "negative adverb",
            "ADV-C": "comparative adverb", "ADV-S": "superlative adverb", "CONJ-N": "negative conjunction",
            "HEB": "Hebrew word", "ARAM": "Aramaic word", "N-PRI": "proper name (not declined)",
            "A-NUI": "number (not declined)", "N-LI": "letter", "N-OI": "noun (not declined)"}


def greek_gram(code):
    if " + " in code:  # crasis, two words written as one (κἀκεῖνα = καί + ἐκεῖνα)
        return " + ".join(greek_gram(c.split("=")[-1]) for c in code.split(" + "))
    if code in G_SIMPLE:
        return G_SIMPLE[code]
    if code == "INJ-HEB":
        return "interjection (a Hebrew word)"
    m = re.match(r"V-(2?)([PIFARL])([AMPDONEX])([ISOMNPR])-?(.*)", code)
    if m:
        second, t, v, md, rest = m.groups()
        out = [("second " if second else "") + G_TENSE[t], G_VOICE[v], G_MOOD[md]]
        rest = rest.split("-")[0]
        if md == "P" and len(rest) == 3:
            out += [G_CASE.get(rest[0], ""), G_NUM.get(rest[1], ""), G_GEN.get(rest[2], "")]
        elif len(rest) == 2:
            out += [{"1": "first", "2": "second", "3": "third"}.get(rest[0], "") + " person", G_NUM.get(rest[1], "")]
        return "verb: " + ", ".join(x for x in out if x)
    m = re.match(r"([NATPRCDKIXQFS])-(\d?)([NGDAV])([SP])([MFN]?)", code)
    if m:
        pos, person, c, n, g = m.groups()
        bits = [G_CASE[c], G_NUM[n]] + ([G_GEN[g]] if g else [])
        label = G_POS[pos] + (f", {'first second third'.split()[int(person) - 1]} person" if person else "")
        return label + ": " + ", ".join(bits)
    m = re.match(r"([PFS])-(\d)([SP])?", code)  # pronoun with person only
    if m:
        return f"{G_POS[m.group(1)]}, {'first second third'.split()[int(m.group(2)) - 1]} person"
    return code


H_STEM = {"q": "Qal", "N": "Niphal", "p": "Piel", "P": "Pual", "h": "Hiphil", "H": "Hophal", "t": "Hithpael",
          "o": "Polel", "O": "Polal", "r": "Hithpolel", "m": "Poel", "M": "Poal", "k": "Palel", "K": "Pulal",
          "Q": "Qal passive", "l": "Pilpel", "L": "Polpal", "f": "Hithpalpel", "D": "Nithpael", "j": "Pealal",
          "i": "Pilel", "u": "Hothpaal", "c": "Tiphil", "v": "Hishtaphel", "w": "Nithpalel", "y": "Nithpoel",
          "z": "Hithpoel", "a": "Peal", "e": "Pael", "E": "Ithpaal", "b": "Peil", "s": "Haphel", "T": "Ithpeel"}
# Verb forms as STEPBible's own key (TEHMC) defines them. STEP's letters differ from OpenScriptures':
# "c" with a person is the cohortative imperfect ("let us ..."); "c" with no person is the infinitive construct.
H_FORM = {"p": "perfect", "q": "perfect with and (sequential)", "i": "imperfect (or cohortative)",
          "n": "imperfect", "u": "imperfect with and", "w": "imperfect with and (sequential)",
          "h": "cohortative", "j": "jussive", "v": "imperative", "r": "participle", "s": "passive participle",
          "a": "infinitive absolute", "c": "infinitive construct"}
H_PERS = {"1": "first person", "2": "second person", "3": "third person"}
H_GEN = {"m": "masculine", "f": "feminine", "b": "masculine or feminine", "c": "common"}
H_NUM = {"s": "singular", "p": "plural", "d": "dual"}
H_STATE = {"a": "absolute", "c": "construct (joined to the next word)", "d": "with the article"}
H_T = {"a": "particle of affirmation", "d": "definite article", "e": "particle of exhortation",
       "i": "interrogative particle", "j": "interjection", "m": "demonstrative particle", "n": "negative particle",
       "o": "direct-object marker", "r": "relative particle", "c": "particle (conjunction)"}
H_P = {"d": "demonstrative pronoun", "f": "indefinite pronoun", "i": "interrogative pronoun",
       "p": "personal pronoun", "r": "relative pronoun"}


def heb_part(code):
    if not code:
        return ""
    k = code[0]
    if k == "V" and len(code) >= 3:
        form, rest = code[2], code[3:]
        if form == "c" and rest[:1] in H_PERS:
            label = "imperfect, cohortative (let me / let us)"
        else:
            label = H_FORM.get(form, form)
            if form in "ac":
                rest = ""  # infinitives carry no person, gender or number
        bits = [H_STEM.get(code[1], code[1]), label]
        if rest and rest[0] in H_PERS:
            bits.append(H_PERS[rest[0]]); rest = rest[1:]
        bits += [H_GEN[ch] if ch in H_GEN else H_NUM.get(ch, ch) for ch in rest]
        return "verb: " + ", ".join(b for b in bits if b)
    if k == "N":
        if code[1:2] == "p":
            return "proper name"
        g, n, s = (code[2:3], code[3:4], code[4:5])
        return "noun: " + ", ".join(x for x in (H_GEN.get(g, ""), H_NUM.get(n, ""), H_STATE.get(s, "")) if x)
    if k == "A":
        kind = {"a": "adjective", "c": "number", "g": "gentilic adjective", "o": "ordinal number"}.get(code[1:2], "adjective")
        g, n, s = (code[2:3], code[3:4], code[4:5])
        return kind + ": " + ", ".join(x for x in (H_GEN.get(g, ""), H_NUM.get(n, ""), H_STATE.get(s, "")) if x)
    if k == "S":
        rest = code[2:]
        label = {"p": "pronoun suffix", "d": "directional ending (toward)", "h": "paragogic he", "n": "paragogic nun"}.get(code[1:2], "suffix")
        bits = [H_PERS.get(rest[:1], "")] + [H_GEN.get(c) or H_NUM.get(c, "") for c in rest[1:]]
        return label + (": " + ", ".join(b for b in bits if b) if any(bits) else "")
    if k == "P":
        return H_P.get(code[1:2], "pronoun")
    if k == "T":
        return H_T.get(code[1:2], "particle")
    if code == "R": return "preposition"
    if code == "Rd": return "preposition with the article"
    if code in ("C", "c"): return "conjunction (and)"
    if code == "D": return "adverb"
    if code == "Td": return "definite article"
    return code


# ---- lexicons ---------------------------------------------------------------------------
def _tbes(prefix):
    """Brief lexicon rows by Strong's number, ranked: general-sense row (G0068G), main row, any."""
    d = {}
    path = glob.glob(os.path.join(SRC, "stepbible", prefix + "*"))[0]
    for line in open(path, encoding="utf-8-sig"):
        c = line.rstrip("\n").split("\t")
        if len(c) < 8 or not re.match(r"^[HG]\d{4}", c[0]):
            continue
        key2 = c[1].split("=")[0].strip()  # e.g. G0068G, H7114B
        row = {"lemma": c[3].strip(), "translit": c[4], "pos": c[5], "gloss": c[6], "def": c[7]}
        d.setdefault(key2, row)  # by extended number
        base = c[0][:5]
        rank = 2 if key2 == base + "G" else 1 if key2 == base else 0
        if rank > d.get("~" + base, {}).get("rank", -1):
            d["~" + base] = dict(row, rank=rank)
    return d


TBESH, TBESG = _tbes("TBESH"), _tbes("TBESG")
BY_LEMMA = {}
for _tb in (TBESH, TBESG):
    for _k, _row in _tb.items():
        if _k.startswith("~"):
            BY_LEMMA.setdefault(letters(_row["lemma"]), _row)


def brief(estrong, lemma=None):
    """STEPBible brief lexicon entry for an extended Strong's number, checked against the lemma.
    Where the number's own entry is for another word (STEPBible files some pronoun forms, such as
    μου, under an entry for με), fall back to the entry for the lemma itself."""
    tb = TBESH if estrong.startswith("H") else TBESG
    base = estrong[:5]
    cands = [tb.get(estrong), tb.get(base), tb.get("~" + base)]
    for c in cands:
        if c and (not lemma or letters(c["lemma"]) == letters(lemma)):
            return c
    if not letters(lemma or ""):
        # a morpheme code such as "Op3m" (a pronoun suffix) has no letters to check: never fall back to
        # an entry that also has none, such as the maqaf
        return next((c for c in cands if c and letters(c["lemma"])), None)
    if letters(lemma) in BY_LEMMA:
        return BY_LEMMA[letters(lemma)]
    return next((c for c in cands if c), None)


GES = {}
for e in json.load(open(os.path.join(SRC, "lexicons", "gesenius", "gesenius-entries.json"), encoding="utf-8")):
    if e.get("strongs"):
        GES.setdefault(e["strongs"], e)

THAYER = {}
for e in json.load(open(os.path.join(SRC, "lexicons", "thayer", "thayer-entries.json"), encoding="utf-8")):
    if e.get("strongs"):
        THAYER.setdefault(e["strongs"], e)

BDBMAP = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(SRC, "lexicons", "bdb", "bdbToStrongsMapping.csv"), encoding="utf-8")):
    BDBMAP[r["strongs"]].append(r["bdb"])


BDB_ARAMAIC_FROM = 9264  # BDB9264 onward is BDB's Aramaic section


def bdb(num, lemma, gloss, definition="", proper=False, aramaic=False):
    """The BDB entry that is this word: same letters as the lemma; among several (homonyms such as
    קֹדֶשׁ holiness and קָדֵשׁ Kadesh), the one whose senses share most words with STEPBible's gloss and
    definition, and never a proper name for an ordinary word."""
    cands = []
    for b in BDBMAP.get(num, []):
        p = os.path.join(SRC, "lexicons", "bdb", "json_output", b + ".json")
        if os.path.exists(p):
            j = json.load(open(p, encoding="utf-8"))
            j["id"] = b
            cands.append(j)
    cands = [c for c in cands if (int(c["id"][3:]) >= BDB_ARAMAIC_FROM) == aramaic]
    same = [c for c in cands if letters(c.get("head_word")) == letters(lemma)]
    if not proper:
        same = [c for c in same if "proper name" not in (c.get("pos") or "")]
    if not same:
        return None  # better no entry than another word's
    stop = {"of", "the", "a", "an", "to", "and", "or", "in", "be", "is", "as", "for", "by", "on", "with"}
    gw = set(re.findall(r"[a-z]+", f"{gloss} {definition}".lower())) - stop

    def score(c):
        text = " ".join([c.get("primary") or "", c.get("description") or ""] +
                        [s.get("primary") or s.get("description") or "" for s in (c.get("senses") or [])])
        is_name = "proper name" in (c.get("pos") or "") or "n.pr" in (c.get("pos") or "")
        return (is_name == proper, len(gw & (set(re.findall(r"[a-z]+", text.lower())) - stop)))
    best = max(same, key=lambda c: (score(c), -int(c["id"][3:])))
    return {"id": best["id"], "head": best.get("head_word"), "pos": best.get("pos"), "primary": best.get("primary"),
            "desc": best.get("description"),
            "senses": [s.get("primary") or s.get("description") for s in (best.get("senses") or [])
                       if (s.get("primary") or s.get("description"))]}


def gesenius(num):
    g = GES.get(num)
    if not g:
        return None
    text = g["text"]
    partial = bool(re.match(r"^\S+ [א-ת]\S* (is used|pr\.)", text)) or (len(text) < 200 and " see " in text)
    t, more = clip(text, 2600)
    return {"page": g["page"], "url": g["url"], "text": t, "more": more, "check": g["check"],
            "unsure": g["unsure"], "partial": partial}


def thayer(num):
    th = THAYER.get(num)
    if not th:
        return None
    t, more = clip(th["text"], 900)
    return {"text": t, "more": more, "check": th["check"]}


# ---- counts, translations, Septuagint ---------------------------------------------------
_sidx = json.load(open(os.path.join(ROOT, "strongs_index.json"), encoding="utf-8"))["verses"]
COUNT_E, COUNT_B = collections.Counter(), collections.Counter()
for _ref, _ids in _sidx.items():
    for s in set(_ids):
        COUNT_E[s] += 1
    for s in {m.group(0) for m in (re.match(r"[HG]\d{4}", i) for i in _ids) if m}:
        COUNT_B[s] += 1

def _load_translations():
    """Every verse of the seven public-domain versions in translations-data/, keyed the way
    corpus_nodes.csv writes references (the same naming rules as fetch_translations.py)."""
    alias = {"Psalms": "Psalm", "Song of Songs": "Song of Solomon", "Canticles": "Song of Solomon",
             "Revelation of John": "Revelation", "The Revelation": "Revelation"}
    roman = (("III ", "3 "), ("II ", "2 "), ("I ", "1 "))

    def norm(name):
        for r, a in roman:
            if name.startswith(r):
                name = a + name[len(r):]
                break
        return alias.get(name, name)

    out = collections.defaultdict(dict)
    for v in TRANS_ORDER:
        data = json.load(open(os.path.join(ROOT, "translations-data", v + ".json"), encoding="utf-8-sig"))
        for book in data.get("books", []):
            name = norm(book["name"])
            for ch in book.get("chapters", []):
                for vs in ch.get("verses", []):
                    out[f"{name} {ch['chapter']}:{vs['verse']}"][v] = " ".join(vs["text"].split())
    return out


TRANSLATIONS = _load_translations()
LXX = json.load(open(os.path.join(SRC, "greek", "lxx-swete-lemmas.json"), encoding="utf-8"))
