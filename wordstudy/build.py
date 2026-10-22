"""Build the corpus Word Study page from the extracted data and the drafted readings.

    python extract.py   -> data/, digest/
    (draft authored/<id>.json per GUIDE.md; python check.py)
    python build.py     -> word-study.html

Only verses whose drafts pass check.py are included; the rest are listed as in progress.
Lexicon entries are stored once per word and shared, to keep the page small.
"""
import csv, json, os, subprocess, sys
from sources import ROOT, brief, COUNT_B, GPUNCT, clean_def, thayer, gesenius, bdb

LEXFIX = {k: v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexfix.json"),
                                          encoding="utf-8")).items() if not k.startswith("_")}

HERE = os.path.dirname(os.path.abspath(__file__))
nodes = list(csv.DictReader(open(os.path.join(ROOT, "corpus_nodes.csv"), encoding="utf-8")))
# Summaries come from the corpus, not from data/<id>.json: data/ is written by extract.py
# and keeps whatever summary the corpus had then. On 21 Oct the 24 summaries rewritten
# off the NRSV were still shipping in their old wording inside wordstudy.js (audit, 22 Oct).
GIST = {n["id"]: n["gist"] for n in nodes}
clusters = list(csv.DictReader(open(os.path.join(ROOT, "corpus_clusters.csv"), encoding="utf-8")))

drafted = [n["id"] for n in nodes if os.path.exists(os.path.join(HERE, "authored", n["id"] + ".json"))]
passing = []
for vid in drafted:
    r = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), vid], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if r.returncode == 0:
        passing.append(vid)
    else:
        print("left out, fails check.py:", vid)

LEX, verses = {}, []
for vid in passing:
    v = json.load(open(os.path.join(HERE, "data", vid + ".json"), encoding="utf-8"))
    a = json.load(open(os.path.join(HERE, "authored", vid + ".json"), encoding="utf-8"))
    pre = lambda n: f"{vid}-{n}"
    en = [dict(s, w=[pre(n) for n in s["w"]]) if isinstance(s, dict) and "w" in s else s for s in a["en"]]
    lx = a.get("lxx") or {}
    words = []
    for w in v["words"]:
        e = a["words"][w["n"]]
        seg = next(s for s in en if isinstance(s, dict) and pre(w["n"]) in s.get("w", []))
        # corrections: a draft's own "fix" (Luke 11:42 παρίημι), or lexfix.json's fix / hide for this word
        lf = LEXFIX.get(pre(w["n"]), {})
        fix = e.get("fix") or lf.get("fix")
        why = (e.get("fix") or {}).get("why") or lf.get("why")
        lk = w["strong"]
        if fix:
            num = fix["strong"][:5]
            b = brief(fix["strong"], fix["lemma"])
            w = dict(w, lemma=fix["lemma"], strong=fix["strong"], num=num, lgloss=b["gloss"] if b else "",
                     count=COUNT_B.get(num, 0), countAll=COUNT_B.get(num, 0))
            lex = {"brief": {"lemma": b["lemma"], "gloss": b["gloss"], "def": clean_def(b["def"])} if b else None}
            if w["lang"] == "G":
                lex["thayer"] = thayer(num)
            else:
                lex["ges"], lex["bdb"] = gesenius(num), bdb(num, fix["lemma"], lex["brief"]["gloss"] if b else "",
                                                            lex["brief"]["def"] if b else "")
            lex["fixNote"] = why
            w["lex"], lk = lex, fix["strong"] + "~fix"
        if lf.get("hide"):
            w = dict(w, lex={k: (None if k in lf["hide"] else val) for k, val in w["lex"].items()})
            w["lex"]["hideNote"] = why
            lk = f"{lk}~{pre(w['n'])}"
        LEX.setdefault(lk, w["lex"])
        out = {"id": pre(w["n"]), "n": w["n"], "orig": w["orig"], "tr": w["tr"], "gloss": w["gloss"],
               "lemma": w["lemma"], "lgloss": w["lgloss"], "strong": w["strong"], "code": w["code"],
               "gram": w["gram"], "count": w["count"], "countAll": w["countAll"], "lk": lk,
               "punct": w.get("punct", ""), "notTR": w.get("notTR", False), "trMoved": w.get("trMoved", False),
               "trForm": w.get("trForm"), "trGloss": w.get("trGloss"),
               "syn": e["s"], "sense": e["r"], "note": e.get("n"),
               "render": [{"t": "This edition (draft)", "r": seg["t"], "ours": True}] +
                         [{"t": tr["t"], "r": r} for tr, r in zip(v["translations"], e["t"])]}
        if v["lang"] == "H":
            out["built"] = [{"heb": p["heb"], "eng": p["eng"], "gram": p["gram"], "main": p["main"]} for p in w["parts"]]
            m = lx.get(w["n"])
            if m and v.get("lxx"):
                rows = v["lxx"]
                main = rows[m["m"]]
                st = m.get("strong") or main["strong"]
                b = brief(st) if st else None
                out["lxx"] = {"greek": " ".join(rows[i]["w"] for i in m["i"]).rstrip(GPUNCT),
                              "word": main["w"].rstrip(GPUNCT), "lemma": m.get("lemma") or main["lemma"],
                              "strong": st, "fit": main["fit"], "fixed": bool(m.get("lemma")),
                              "gloss": b["gloss"] if b else None, "nt": COUNT_B.get(st, 0) if st else 0,
                              "note": m.get("n")}
        words.append(out)
    lxx_verse = None
    if v["lang"] == "H" and v.get("lxx"):
        lxx_verse = {"text": " ".join(r["w"] for r in v["lxx"]), "ref": v.get("lxx_shifted") or v["lxx_ref"],
                     "shifted": bool(v.get("lxx_shifted")), "extra": list((lx.get("_extra") or {}).values())}
    kjv = next((t["text"] for t in v["translations"] if t["key"] == "KJV"), "")
    verses.append({"id": vid, "ref": v["ref"], "lang": v["lang"], "cluster": v["cluster"], "group": v["clusterKey"],
                   "gist": GIST[vid], "en": en, "kjv": kjv, "lxx": lxx_verse, "trNote": a.get("tr_note"),
                   "trExtra": v.get("tr_extra") or [],
                   "translations": [{"t": t["t"], "r": t["text"]} for t in v["translations"]], "words": words})

groups = [{"key": c["key"], "name": c["name"],
           "ids": [n["id"] for n in nodes if n["cluster"] == c["key"]]} for c in clusters]
refs = {n["id"]: n["ref"] for n in nodes}
blob = json.dumps({"verses": verses, "lex": LEX, "groups": groups, "refs": refs, "total": len(nodes)},
                  ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
page = open(os.path.join(HERE, "template.html"), encoding="utf-8").read().replace("/*DATA*/{}", blob)
open(os.path.join(HERE, "word-study.html"), "w", encoding="utf-8").write(page)
print(f"{len(verses)} of {len(nodes)} verses on the page ({sum(len(v['words']) for v in verses)} words, "
      f"{len(LEX)} lexicon entries) -> word-study.html ({len(page):,} bytes)")

# The same study for the concordagraph: data plus embed.js, loaded beside ../concordagraph.html.
# The whole-verse translations feed only this page's "Compare" list, so they stay here.
embed = json.dumps({"verses": [{k: val for k, val in v.items() if k != "translations"} for v in verses], "lex": LEX},
                   ensure_ascii=False, separators=(",", ":"))
js = ("/* Generated by wordstudy/build.py from authored/ and data/. Do not edit; edit embed.js. */\n"
      "window.WORDSTUDY = " + embed + ";\n" + open(os.path.join(HERE, "embed.js"), encoding="utf-8").read())
open(os.path.join(ROOT, "wordstudy.js"), "w", encoding="utf-8", newline="\n").write(js)
print(f"{len(verses)} verses -> ../wordstudy.js ({len(js.encode('utf-8')):,} bytes)")
