"""Check drafted readings against the rules in GUIDE.md.

    python check.py            # every authored/<id>.json
    python check.py p2 q4      # just these

Exits non-zero if any draft breaks a rule. A rendering must occur in its translation's text;
every original word must be translated exactly once; no dashes; no Bible reference that the
brief does not supply; Septuagint pairings must be complete and in range.
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKNAMES = ("Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|Samuel|Kings|Chronicles|Ezra|"
             "Nehemiah|Esther|Job|Psalm|Psalms|Proverbs|Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|"
             "Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|"
             "Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|"
             "Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|Revelation")
REF = re.compile(rf"\b(?:[123] )?(?:{BOOKNAMES})\.? \d+(?::\d+(?:[-,]\d+)*)?|\b[A-Z][a-z]{{1,3}}\. ?\d+:\d+")


import csv
CORPUS = {r["ref"] for r in csv.DictReader(open(os.path.join(os.path.dirname(HERE), "corpus_nodes.csv"), encoding="utf-8"))}


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", re.sub(r"[^\w' ]", " ", s)).strip()


def check(vid):
    errs = []
    dpath = os.path.join(HERE, "data", vid + ".json")
    apath = os.path.join(HERE, "authored", vid + ".json")
    if not os.path.exists(apath):
        return [f"no draft at authored/{vid}.json"]
    v = json.load(open(dpath, encoding="utf-8"))
    try:
        a = json.load(open(apath, encoding="utf-8"))
    except Exception as e:
        return [f"not valid JSON: {e}"]
    digest = open(os.path.join(HERE, "digest", vid + ".txt"), encoding="utf-8").read()
    nums = [w["n"] for w in v["words"]]
    trans = v["translations"]

    # every string, for the dash and reference rules
    def strings(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, list):
            for y in x: yield from strings(y)
        elif isinstance(x, dict):
            for y in x.values(): yield from strings(y)
    for s in strings(a):
        if "—" in s or "–" in s:
            errs.append(f"dash in: {s[:70]}")

    # en: each word exactly once
    seen = {}
    for seg in a.get("en", []):
        if isinstance(seg, dict):
            if "w" in seg:
                for n in seg["w"]:
                    seen[n] = seen.get(n, 0) + 1
                    if n not in nums:
                        errs.append(f"en piece '{seg['t']}' names word {n}, which the verse does not have")
            elif "sup" not in seg:
                errs.append(f"en piece without w or sup: {seg}")
            if not seg.get("t"):
                errs.append(f"en piece with no text: {seg}")
    for n in nums:
        if seen.get(n, 0) != 1:
            errs.append(f"word {n} appears {seen.get(n, 0)} times in en (must be once)")

    # words
    W = a.get("words", {})
    for n in nums:
        e = W.get(n)
        if not e:
            errs.append(f"word {n}: no entry"); continue
        if not e.get("s") or not isinstance(e["s"], list):
            errs.append(f"word {n}: no synonyms")
        if not e.get("r"):
            errs.append(f"word {n}: no sense line")
        t = e.get("t")
        if not isinstance(t, list) or len(t) != len(trans):
            errs.append(f"word {n}: t has {len(t) if isinstance(t, list) else 0} entries, the verse has {len(trans)} translations")
            continue
        for r, tr in zip(t, trans):
            if r is None:
                continue
            for part in r.split(" ... "):
                if norm(part) and norm(part) not in norm(tr["text"]):
                    errs.append(f"word {n}: '{part}' is not in the {tr['key']} text")
        note = e.get("n") or ""
        for m in REF.finditer(note):
            ref = m.group(0)
            if ref.replace(" ", "") not in digest.replace(" ", "") and ref not in CORPUS:
                errs.append(f"word {n}: note cites '{ref}', which the brief does not supply")
    for n in W:
        if n not in nums:
            errs.append(f"words has an entry for {n}, which the verse does not have")

    # Septuagint
    if v["lang"] == "H" and v.get("lxx"):
        lx = a.get("lxx")
        if not lx:
            errs.append("no lxx pairing")
        else:
            used = {}
            for k, m in lx.items():
                if k == "_extra":
                    for i in m:
                        used[int(i)] = used.get(int(i), 0) + 1
                    continue
                if k not in nums:
                    errs.append(f"lxx pairs Hebrew word {k}, which the verse does not have")
                for i in m.get("i", []):
                    used[i] = used.get(i, 0) + 1
                    if not 0 <= i < len(v["lxx"]):
                        errs.append(f"lxx {k}: index {i} out of range")
                if m.get("m") not in m.get("i", []):
                    errs.append(f"lxx {k}: main index not among its indices")
            for i, c in used.items():
                if c > 1:
                    errs.append(f"lxx: Greek word {i} used {c} times")
            if True:
                missing = [i for i in range(len(v["lxx"])) if i not in used]
                if missing:
                    errs.append(f"lxx: Greek words not paired or listed in _extra: {missing}")
    return errs


ids = sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(HERE, "authored", "*.json")))
bad = 0
for vid in ids:
    errs = check(vid)
    if errs:
        bad += 1
        print(f"{vid}: {len(errs)} problem(s)")
        for e in errs[:40]:
            print("   ", e)
print(f"{len(ids) - bad} of {len(ids)} drafts pass")
sys.exit(1 if bad else 0)
