"""Build the word-study pilot page.

    python extract.py   -> pilot_data.json  (word rows and lexicon matches, read from the sources)
    python build.py     -> word-study.html  (merges authored.json, the drafted readings)

Nothing here reads or writes NRSV text. The translations shown are the public-domain
ones in ../translations.json.
"""
import json, os, re, glob, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "bible-sources")

data = json.load(open(os.path.join(HERE, "pilot_data.json"), encoding="utf-8"))
authored = json.load(open(os.path.join(HERE, "authored.json"), encoding="utf-8"))

# BDB's Strong's map attaches homonyms and neighbours; these are the entries that are this word.
BDB_PICK = {"H3588": "BDB3995", "H7114": "BDB7547", "H7105": "BDB7548", "H7704": "BDB8171",
            "H6016": "BDB6172", "H3808": "BDB4266", "H7725": "BDB8502", "H1616": "BDB1565",
            "H1961": "BDB2145", "H1288": "BDB1330", "H3068": "BDB2100", "H0430": "BDB430",
            "H3605": "BDB4037", "H3027": "BDB3437"}

# Where STEPBible's brief lexicon files a form (σέ, εἶ) ahead of the dictionary entry, or keys the
# entry by its first column only: take the row whose first column is the number itself.
BRIEF_BY_ROW = {"G4771": ("G4771", "G4771"), "G1510": ("G1510", "G1510"), "H0430G": ("H0430", "H0430G")}

TRANS_NAMES = {"KJV": "King James", "Geneva1599": "Geneva 1599", "DRC": "Douay-Rheims",
               "JPS": "JPS 1917", "ASV": "American Standard", "YLT": "Young's Literal",
               "BSB": "Berean Standard"}

CANTILLATION = re.compile("[֑-ֽ֯]")


def heb(s):
    """Drop cantillation marks and meteg; keep letters, vowel points, maqaf and sof pasuq."""
    return CANTILLATION.sub("", unicodedata.normalize("NFC", s or ""))


def tbes_by_row(prefix, first, second):
    path = glob.glob(os.path.join(SRC, "stepbible", prefix + "*"))[0]
    for line in open(path, encoding="utf-8-sig"):
        c = line.rstrip("\n").split("\t")
        if len(c) >= 8 and c[0] == first and c[1].startswith(second):
            return {"lemma": c[3], "translit": c[4], "pos": c[5], "gloss": c[6], "def": c[7]}
    return None


def clean_def(s):
    s = re.sub(r"<br\s*/?>|<BR\s*/?>", "\n", s or "", flags=re.I)
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
G_VOICE = {"A": "active", "M": "middle", "P": "passive", "D": "middle", "O": "passive", "N": "middle or passive"}
G_MOOD = {"I": "indicative", "S": "subjunctive", "O": "optative", "M": "imperative", "N": "infinitive", "P": "participle"}
G_CASE = {"N": "nominative", "G": "genitive", "D": "dative", "A": "accusative", "V": "vocative"}
G_NUM = {"S": "singular", "P": "plural"}
G_GEN = {"M": "masculine", "F": "feminine", "N": "neuter"}
G_POS = {"N": "noun", "A": "adjective", "T": "article", "P": "personal pronoun"}


def greek_gram(code):
    if code == "CONJ": return "conjunction"
    if code == "ADV": return "adverb"
    if code == "PRT": return "particle"
    if code == "PRT-N": return "negative particle"
    m = re.match(r"V-(2?)([PIFARL])([AMPDON])([ISOMNP])-?(.*)", code)
    if m:
        second, t, v, md, rest = m.groups()
        out = [("second " if second else "") + G_TENSE[t], G_VOICE[v], G_MOOD[md]]
        if md == "P" and len(rest) == 3:
            out += [G_CASE[rest[0]], G_NUM[rest[1]], G_GEN[rest[2]]]
        elif len(rest) == 2:
            out += [{"1": "first", "2": "second", "3": "third"}[rest[0]] + " person", G_NUM[rest[1]]]
        return "verb: " + ", ".join(out)
    m = re.match(r"([NATP])-(\d?)([NGDAV])([SP])([MFN]?)", code)
    if m:
        pos, person, c, n, g = m.groups()
        bits = [G_CASE[c], G_NUM[n]] + ([G_GEN[g]] if g else [])
        label = G_POS[pos] + (f", {'first second third'.split()[int(person) - 1]} person" if person else "")
        return label + ": " + ", ".join(bits)
    return code


H_STEM = {"q": "Qal", "N": "Niphal", "p": "Piel", "P": "Pual", "h": "Hiphil", "H": "Hophal", "t": "Hithpael"}
H_FORM = {"p": "perfect", "q": "perfect with and (sequential)", "i": "imperfect", "w": "imperfect with and (sequential)",
          "h": "cohortative", "j": "jussive", "v": "imperative", "r": "participle", "s": "passive participle",
          "a": "infinitive absolute", "c": "infinitive construct"}
H_PERS = {"1": "first person", "2": "second person", "3": "third person"}
H_GEN = {"m": "masculine", "f": "feminine", "b": "masculine or feminine", "c": "common"}
H_NUM = {"s": "singular", "p": "plural", "d": "dual"}
H_STATE = {"a": "absolute", "c": "construct (joined to the next word)", "d": "with the article"}


def heb_part(code):
    if not code: return ""
    k = code[0]
    if k == "V" and len(code) >= 3:
        rest = "" if code[2] in "ac" else code[3:]  # infinitives carry no person, gender or number
        bits = [H_STEM.get(code[1], code[1]), H_FORM.get(code[2], code[2])]
        if rest and rest[0] in H_PERS:
            bits.append(H_PERS[rest[0]]); rest = rest[1:]
        bits += [H_GEN[ch] if ch in H_GEN else H_NUM.get(ch, ch) for ch in rest]
        return "verb: " + ", ".join(b for b in bits if b)
    if k == "N":
        if code[1:2] == "p":
            return "proper name"
        g, n, s = (code[2:3], code[3:4], code[4:5])
        return "noun: " + ", ".join(x for x in (H_GEN.get(g, ""), H_NUM.get(n, ""), H_STATE.get(s, "")) if x)
    if k == "S" and code[1:2] == "p":
        rest = code[2:]
        return "pronoun suffix: " + ", ".join([H_PERS.get(rest[:1], "")] + [H_GEN.get(c) or H_NUM.get(c, c) for c in rest[1:]])
    if code == "R": return "preposition"
    if code == "Rd": return "preposition with the article"
    if code in ("C", "c"): return "conjunction (and)"
    if code == "Tn": return "negative particle"
    if code == "Tc": return "particle (conjunction)"
    return code


GPUNCT = "··;,.;"  # middle dot, Greek raised dot, Greek question mark, comma, full stop
CODES = {"Matthew 25:24": "Mat.25.24", "Deuteronomy 24:19": "Deu.24.19", "Hebrews 7:8": "Heb.7.8"}


# ---- Septuagint: Swete's words with lemmas, Strong's glosses, New Testament verse counts ----
LXX = json.load(open(os.path.join(SRC, "greek", "lxx-swete-lemmas.json"), encoding="utf-8"))
TBESG = {}
for line in open(glob.glob(os.path.join(SRC, "stepbible", "TBESG*"))[0], encoding="utf-8-sig"):
    c = line.rstrip("\n").split("\t")
    if len(c) >= 8 and re.match(r"^G\d{4}$", c[0]) and c[1].strip().startswith(c[0]):
        # prefer the general-sense row (G0068G "field"), then the main row (G0068 "Field of"), then any
        rank = 2 if c[1].strip() == c[0] + "G =" else 1 if c[1].strip() == c[0] + " =" else 0
        if rank > TBESG.get(c[0], {}).get("rank", -1):
            TBESG[c[0]] = {"lemma": c[3], "gloss": c[6], "rank": rank}
NT_COUNT = {}
for ref, ids in json.load(open(os.path.join(ROOT, "strongs_index.json"), encoding="utf-8"))["verses"].items():
    for s in {re.match(r"G\d{4}", i).group(0) for i in ids if re.match(r"G\d{4}", i)}:
        NT_COUNT[s] = NT_COUNT.get(s, 0) + 1

# ---- assemble --------------------------------------------------------------------------
order = authored["_order"]
verses = []
for v in data:
    lang = v["lang"]
    tkeys = order[lang]
    words = []
    for w in v["words"]:
        a = authored[f"{CODES[v['ref']]}#{w['n']}"]
        main = next(p for p in w["parts"] if p["main"])
        L = main["lex"]
        estrong = main["strong"]
        brief = L.get("brief")
        if estrong in BRIEF_BY_ROW:
            brief = tbes_by_row("TBESH" if lang == "H" else "TBESG", *BRIEF_BY_ROW[estrong])
        lex = {}
        if brief:
            lex["brief"] = {"lemma": brief["lemma"], "gloss": brief["gloss"], "def": clean_def(brief["def"])}
        if lang == "H":
            g = L.get("gesenius")
            if g:
                text = g["text"]
                # a sub-entry ("כִּי אִם is used ...") or a bare cross-reference ("see ...")
                partial = bool(re.match(r"^\S+ [א-ת]\S* (is used|pr\.)", text)) or (len(text) < 200 and " see " in text)
                t, more = clip(text, 2600)
                lex["ges"] = {"page": g["page"], "url": g["url"], "text": t, "more": more, "check": g["check"],
                              "unsure": g["unsure"], "partial": partial}
            pick = BDB_PICK.get(L["strongs"])
            for b in L.get("bdb", []):
                if (pick and b["id"] == pick) or (not pick and len(L["bdb"]) == 1):
                    lex["bdb"] = {"id": b["id"], "head": b["head_word"], "pos": b.get("pos"),
                                  "primary": b.get("primary"), "desc": b.get("description"),
                                  "senses": [s.get("primary") or s.get("description") for s in (b.get("senses") or [])
                                             if (s.get("primary") or s.get("description"))]}
        else:
            th = L.get("thayer")
            if th:
                t, more = clip(th["text"], 900)
                lex["thayer"] = {"text": t, "more": more, "check": th["check"]}
        if lang == "H":
            gram_codes = [p["gram"] for p in w["parts"]]
            # the first part's code carries the language prefix H
            decoded = [heb_part(c[1:] if i == 0 and c.startswith("H") else c) for i, c in enumerate(gram_codes)]
            built = [{"heb": heb(p["heb"]), "eng": p["eng"], "gram": d, "main": p["main"]}
                     for p, d in zip(w["parts"], decoded)]
            gram = next(d for p, d in zip(w["parts"], decoded) if p["main"])
            orig, gloss = heb(w["orig"]), w["eng"].replace("/", " ").replace("  ", " ").strip()
        else:
            built = None
            gram = greek_gram(main["gram"])
            orig, gloss = w["orig"].rstrip(GPUNCT), w["eng"].rstrip(GPUNCT + ";")
        words.append({
            "id": f"{v['id']}-{w['n']}", "n": w["n"], "orig": orig, "tr": w["translit"].replace(".", ""),
            "gloss": gloss, "lemma": heb(main["lemma"]) if lang == "H" else main["lemma"],
            "lgloss": main["gloss"].split("»")[0].strip(": ").replace("_", " "),
            "strong": estrong, "code": main["gram"], "gram": gram, "built": built,
            "count": L["count_e"], "countAll": L["count_b"],
            "syn": a["s"], "sense": a["r"], "note": a.get("n"),
            "render": [{"t": TRANS_NAMES[k], "r": r} for k, r in zip(tkeys, a["t"])],
            "lex": lex, "punct": (w["orig"][len(w["orig"].rstrip(GPUNCT)):] if lang == "G" else ""),
        })
    # the Septuagint's Greek for each Hebrew word (pairing drafted by hand; lemmas from align_lxx.py)
    lxx_verse = None
    lx = authored.get("_lxx", {}).get(CODES[v["ref"]])
    if lx:
        rows = LXX[lx["_ref"]]
        lxx_verse = {"text": " ".join(r["w"] for r in rows), "extra": list(lx.get("_extra", {}).values())}
        for w in words:
            m = lx.get(w["n"])
            if not m:
                continue
            main = rows[m["m"]]
            st = m.get("strong") or main["strong"]
            brief = TBESG.get(st) if st else None
            w["lxx"] = {
                "greek": " ".join(rows[i]["w"] for i in m["i"]).rstrip(GPUNCT),
                "word": main["w"].rstrip(GPUNCT),
                "lemma": m.get("lemma") or main["lemma"],
                "strong": st, "fit": main["fit"], "fixed": bool(m.get("lemma")),
                "gloss": brief["gloss"] if brief else None,
                "nt": NT_COUNT.get(st, 0) if st else 0,
                "note": m.get("n"),
            }
    # our literal rendering: plain strings are English glue; {t, w} links to words; {t, sup} is supplied
    en = []
    for seg in authored["_en"][CODES[v["ref"]]]:
        if isinstance(seg, dict) and "w" in seg:
            en.append({"t": seg["t"], "w": [f"{v['id']}-{n}" for n in seg["w"]]})
        else:
            en.append(seg)
    linked = [i for s in en if isinstance(s, dict) for i in s.get("w", [])]
    missing = [w["id"] for w in words if w["id"] not in linked]
    assert not missing, f"{v['ref']}: words with no English: {missing}"
    for w in words:
        seg = next(s for s in en if isinstance(s, dict) and w["id"] in s.get("w", []))
        w["render"].insert(0, {"t": "This edition (draft)", "r": seg["t"], "ours": True})
    verses.append({
        "id": v["id"], "ref": v["ref"], "lang": lang, "cluster": v["cluster"], "gist": v["gist"],
        "en": en, "lxx": lxx_verse,
        "translations": [{"t": TRANS_NAMES[k], "r": v["translations"][k]} for k in tkeys if k in v["translations"]],
        "words": words,
    })

page = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
blob = json.dumps(verses, ensure_ascii=False).replace("</", "<\\/")
out = page.replace("/*DATA*/[]", blob)
open(os.path.join(HERE, "word-study.html"), "w", encoding="utf-8").write(out)

# report what the page will flag
n = sum(len(v["words"]) for v in verses)
print(f"{len(verses)} verses, {n} words -> word-study.html ({len(out):,} bytes)")
for v in verses:
    for w in v["words"]:
        g = w["lex"].get("ges")
        if v["lang"] == "H" and not g:
            print("  no Gesenius entry:", v["ref"], w["n"], w["lemma"])
        elif g and g["partial"]:
            print("  Gesenius match starts mid-entry or is a cross-reference:", v["ref"], w["n"], w["lemma"])
        if not w["lex"].get("brief"):
            print("  no brief lexicon entry:", v["ref"], w["n"], w["lemma"])
dash = [s for v in verses for w in v["words"] for s in [w["sense"], w.get("note") or ""] + w["syn"] if "—" in s or "–" in s]
print("  dashes in drafted text:", len(dash))
