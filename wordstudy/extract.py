"""Gather word-level data for every concordagraph verse.

    python extract.py          -> data/<node id>.json  (everything the page needs, from the sources)
                                  digest/<node id>.txt (a compact brief for drafting the readings)

Reads corpus_nodes.csv; never edits it. Nothing here reads NRSV text.
"""
import csv, json, os, re, glob, sys
from sources import (ROOT, BOOKS, TRANS_ORDER, TRANS_NAMES, GPUNCT, heb, clean_def, greek_gram, heb_part,
                     brief, gesenius, thayer, bdb, COUNT_E, COUNT_B, TRANSLATIONS, LXX, lxx_ref,
                     LXX_ABSENT)

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
os.makedirs(os.path.join(HERE, "digest"), exist_ok=True)

nodes = list(csv.DictReader(open(os.path.join(ROOT, "corpus_nodes.csv"), encoding="utf-8")))
clusters = {r["key"]: r for r in csv.DictReader(open(os.path.join(ROOT, "corpus_clusters.csv"), encoding="utf-8"))}
only = set(sys.argv[1:])

_files = {}


def tagged_rows(fileprefix, code):
    if fileprefix not in _files:
        path = glob.glob(os.path.join(ROOT, "lemma-data", fileprefix + "*"))[0]
        rows = {}
        for line in open(path, encoding="utf-8"):
            m = re.match(r"^([1-3]?[A-Za-z]+\.\d+\.\d+)(\([^)]*\))?#", line)
            if m:
                rows.setdefault(m.group(1), []).append(line.rstrip("\n").split("\t"))
        _files[fileprefix] = rows
    return _files[fileprefix].get(code, [])


def greek_words(rows):
    words, tr_extra = [], []
    for c in rows:
        eds = c[5]
        critical = "NA28" in eds or "SBL" in eds
        m = re.match(r"(.+?) \((.+)\)", c[1])
        st, gram = c[3].split("=", 1)
        lem, gl = c[4].split("=", 1)
        n = c[0].split("#")[1].split("=")[0]
        if not critical:
            if "TR" in eds.split("+"):
                tr_extra.append({"n": n, "orig": m.group(1).rstrip(GPUNCT), "eng": c[2]})
            continue
        toks = eds.split("+")
        in_tr = any(t == "TR" or t.startswith("TR»") or t.startswith("TR«") for t in toks)
        w = {"n": n, "orig": m.group(1).rstrip(GPUNCT), "punct": m.group(1)[len(m.group(1).rstrip(GPUNCT)):],
             "tr": m.group(2), "gloss": c[2].rstrip(GPUNCT + ";"), "lang": "G",
             "notTR": not in_tr, "trMoved": any(t.startswith(("TR»", "TR«")) for t in toks),
             "parts": [{"strong": st, "code": gram, "lemma": lem, "lgloss": gl, "main": True}]}
        # TAGNT's variant columns give the form the TR reads instead, e.g.
        # "ποιήσομεν (t=poiēsomen) we will do - G4160=V-FAI-1P in: TR+Byz"
        for col in (c[6] if len(c) > 6 else "", c[7] if len(c) > 7 else ""):
            for vm in re.finditer(r"(\S+) \(t=[^)]*\) (.*?) - (G\S+) in: ([^;]+)", col):
                if "TR" in vm.group(4).split("+"):
                    w["trForm"], w["trGloss"], w["notTR"] = vm.group(1), vm.group(2).strip(), True
        words.append(w)
    # A critical-text word "missing" from the Textus Receptus is often there in another spelling, form or
    # position: the TR's own row then carries the same Strong's number. Pair them, so the page says
    # "the TR reads X" rather than "not in the TR", and only true additions stay in tr_extra.
    for c in rows:
        if "NA28" in c[5] or "SBL" in c[5] or "TR" not in c[5].split("+"):
            continue
        st = c[3].split("=", 1)[0][:5]
        form = re.match(r"(.+?) \(", c[1]).group(1).rstrip(GPUNCT)
        n = c[0].split("#")[1].split("=")[0]
        # only near neighbours, and never the article or common pronouns, which recur and pair falsely
        if st in ("G3588", "G0846", "G1473", "G4771", "G2532", "G1161"):
            continue
        twin = next((w for w in words if w["notTR"] and not w.get("trForm") and w["parts"][0]["strong"][:5] == st
                     and abs(int(re.sub(r"\D", "", w["n"])) - int(re.sub(r"\D", "", n))) <= 3), None)
        if twin:
            twin["trForm"] = form
            tr_extra[:] = [x for x in tr_extra if x["n"] != n]
    return words, tr_extra


def hebrew_words(rows):
    words = []
    for c in rows:
        hebs, tl, en = c[1].split("/"), c[2].split("/"), c[3].split("/")
        sts, grs = c[4].split("/"), c[5].split("/")
        exp = c[11].split("/") if len(c) > 11 else []
        parts = []
        for i, s in enumerate(sts):
            s2 = s.split("\\")[0]
            ex = exp[i] if i < len(exp) else ""
            exm = re.match(r"\{?(H\w+)=([^=]+)=([^}]*)\}?", ex.split("\\")[0])
            code = grs[i] if i < len(grs) else ""
            if i == 0 and code[:1] in "HA":
                code = code[1:]  # the first code carries the language letter (H Hebrew, A Aramaic)
            parts.append({"strong": s2.strip("{}"), "code": code, "heb": heb(hebs[i] if i < len(hebs) else ""),
                          "eng": en[i].strip() if i < len(en) else "", "lemma": heb(exm.group(2)) if exm else "",
                          "lgloss": (exm.group(3) if exm else "").split("»")[0].strip(": ").replace("_", " "),
                          "main": s2.startswith("{")})
        if not any(p["main"] for p in parts):
            # the last part that is a word, not punctuation (H9014-H9019: maqaf, paseq, sof pasuq and the like)
            real = [p for p in parts if not re.match(r"H901[4-9]", p["strong"])] or parts
            real[-1]["main"] = True
        words.append({"n": c[0].split("#")[1].split("=")[0], "orig": heb(c[1].replace("/", "").replace("\\", "")),
                      "tr": c[2].replace("/", "").replace(".", ""), "gloss": c[3].replace("/", " ").replace("  ", " ").strip(),
                      "lang": "H", "parts": parts, "punct": "", "aram": c[5][:1] == "A"})
    return words


def lexicon(w):
    main = next(p for p in w["parts"] if p["main"])
    est = main["strong"]
    num = re.match(r"[HG]\d{4}", est).group(0) if re.match(r"[HG]\d{4}", est) else est
    br = brief(est, main["lemma"])
    lex = {"brief": {"lemma": br["lemma"], "gloss": br["gloss"], "def": clean_def(br["def"])} if br else None}
    if w["lang"] == "H":
        lex["ges"] = gesenius(num)
        lex["bdb"] = bdb(num, main["lemma"], main["lgloss"], (br or {}).get("def", ""), main["code"].startswith("Np"), w.get("aram", False))
    else:
        lex["thayer"] = thayer(num)
    w["strong"], w["num"] = est, num
    w["lemma"], w["lgloss"], w["code"] = main["lemma"], main["lgloss"], main["code"]
    w["gram"] = heb_part(main["code"]) if w["lang"] == "H" else greek_gram(main["code"])
    if w["lang"] == "H":
        for p in w["parts"]:
            p["gram"] = heb_part(p["code"])
    w["count"], w["countAll"] = COUNT_E.get(est, 0), COUNT_B.get(num, 0)
    w["lex"] = lex


def digest(v):
    L = [f"NODE {v['id']} | {v['ref']} | {'Hebrew' if v['lang'] == 'H' else 'Greek'} | group: {v['cluster']}",
         f"Concordagraph summary (ours): {v['gist']}", "",
         "TRANSLATIONS, in the order your \"t\" list must follow:"]
    for i, t in enumerate(v["translations"]):
        L.append(f"  [{i}] {t['key']}: {t['text']}")
    L += ["", f"WORDS ({len(v['words'])}), in {'Hebrew (right-to-left) ' if v['lang'] == 'H' else ''}text order:"]
    for w in v["words"]:
        b = (w["lex"].get("brief") or {})
        L.append(f"#{w['n']} {w['orig']} ({w['tr']})  STEP: \"{w['gloss']}\"  | dictionary {w['lemma']} = {w['lgloss']}"
                 f" | {w['strong']} | {w['gram']} | verses using it: {w['count']}")
        if w["lang"] == "H" and len(w["parts"]) > 1:
            L.append("    built from: " + " + ".join(f"{p['heb']} ({p['eng']}; {p['gram']})" for p in w["parts"]))
        d = b.get("def", "").replace("\n", " ")
        if d:
            L.append("    brief lexicon: " + d[:260] + (" …" if len(d) > 260 else ""))
        g = w["lex"].get("ges")
        if g:
            flag = " [match starts mid-entry or is a cross-reference]" if g["partial"] else ""
            L.append(f"    Gesenius p.{g['page']}{flag}: " + g["text"].replace("\n", " ")[:420] + " …")
        bd = w["lex"].get("bdb")
        if bd:
            L.append(f"    BDB {bd['id']}: {bd.get('primary')}; " + "; ".join((bd.get('senses') or [])[:4]))
        if w.get("trForm"):
            same = w["trForm"] == w["orig"]
            gl = f" '{w['trGloss']}'" if w.get("trGloss") else ""
            L.append(f"    (the Textus Receptus, the KJV's Greek, reads {'this word in another position' if same else w['trForm'] + gl} here)")
        elif w.get("trMoved"):
            L.append("    (the Textus Receptus, the KJV's Greek, has this word in another position)")
        elif w.get("notTR"):
            L.append("    (not in the Textus Receptus, the KJV's Greek)")
    if v.get("tr_extra"):
        L.append("")
        L.append("TEXTUS RECEPTUS ONLY (the KJV's Greek has these; our critical text does not): " +
                 ", ".join(f"{x['orig']} '{x['eng']}'" for x in v["tr_extra"]))
    if v.get("lxx"):
        L += ["", f"SEPTUAGINT (Swete, {v['lxx_ref']}), indexed for your \"lxx\" pairing:"]
        if v.get("lxx_shifted"):
            L.append(f"  NOTE: Swete's digital text numbers this verse {v['lxx_shifted']} (its numbering runs one"
                     " behind here); the list below is this verse.")
        L.append("  " + "  ".join(f"[{i}] {r['w']} ({r['lemma'] or '?'}{', loose' if r['lemma'] and r['fit'] < 0.7 else ''})"
                                  for i, r in enumerate(v["lxx"])))
    elif v["lang"] == "H":
        L += ["", f"SEPTUAGINT: no Swete text found at {v.get('lxx_ref')}"]
    return "\n".join(L) + "\n"


count = 0
for nd in nodes:
    if only and nd["id"] not in only:
        continue
    book, cv = nd["ref"].rsplit(" ", 1)
    ch, vs = (int(x) for x in cv.split(":"))
    code, fileprefix, lb = BOOKS[book]
    rows = tagged_rows(fileprefix, f"{code}.{ch}.{vs}")
    if not rows:
        print("NO TAGGED ROWS:", nd["id"], nd["ref"]); continue
    lang = "H" if fileprefix.startswith("TAHOT") else "G"
    if lang == "G":
        words, tr_extra = greek_words(rows)
    else:
        words, tr_extra = hebrew_words(rows), []
    for w in words:
        lexicon(w)
    tr = dict(TRANSLATIONS.get(nd["ref"], {}))
    if book == "Matthew" and ch == 17 and vs >= 22:  # the Douay-Rheims numbers Matthew 17:22-27 one ahead
        t2 = TRANSLATIONS.get(f"Matthew 17:{vs - 1}", {}).get("DRC")
        if t2:
            tr["DRC"] = t2
    # The JPS follows the Hebrew Bible's numbering: Exodus 22:2-31 is its 22:1-30, Deuteronomy 23:1-25 its 23:2-26.
    jps_shift = {("Exodus", 22): -1, ("Deuteronomy", 23): +1}.get((book, ch))
    if jps_shift:
        t2 = TRANSLATIONS.get(f"{book} {ch}:{vs + jps_shift}", {}).get("JPS")
        if t2:
            tr["JPS"] = t2
    # The JPS also numbers 1 Kings 4:21-5:18 as the Hebrew does: 4:21-34 is its 5:1-14, 5:1-18 its 5:15-32.
    jps_kings = {4: (21, 34, lambda v: (5, v - 20)), 5: (1, 18, lambda v: (5, v + 14))}.get(ch) if book == "1 Kings" else None
    if jps_kings and jps_kings[0] <= vs <= jps_kings[1]:
        jc, jv = jps_kings[2](vs)
        t2 = TRANSLATIONS.get(f"1 Kings {jc}:{jv}", {}).get("JPS")
        if t2:
            tr["JPS"] = t2
    if book == "Haggai" and ch == 2:  # Geneva and Douay-Rheims start chapter 2 a verse early: their 2:9 is our 2:8
        for k in ("Geneva1599", "DRC"):
            t2 = TRANSLATIONS.get(f"Haggai 2:{vs + 1}", {}).get(k)
            if t2:
                tr[k] = t2
    if book == "Psalm" and 10 <= ch <= 113:  # the Douay-Rheims numbers Psalms 10-113 one behind, as the Latin does
        drc = TRANSLATIONS.get(f"Psalm {ch - 1}:{vs}", {}).get("DRC")
        if drc:
            tr["DRC"] = drc
    v = {"id": nd["id"], "ref": nd["ref"], "lang": lang, "cluster": clusters[nd["cluster"]]["name"],
         "clusterKey": nd["cluster"], "gist": nd["gist"],
         "translations": [{"key": k, "t": TRANS_NAMES[k], "text": tr[k]} for k in TRANS_ORDER if k in tr],
         "words": words, "tr_extra": tr_extra}
    if lang == "H" and (book, ch, vs) in LXX_ABSENT:
        v["lxx_ref"], v["lxx"] = lxx_ref(book, ch, vs), None
    elif lang == "H" and book == "Deuteronomy" and ch == 14 and 20 <= vs <= 29:
        # Swete's digital Deuteronomy 14 runs one verse behind from 14:20 to the end of the chapter, and
        # every one of those numbers exists, so the fallback below never fires for 14:20-28: its 14:21 is
        # the Hebrew 14:22 (checked 13 Oct). Recorded as shifted, exactly as the fallback records 14:29.
        v["lxx_ref"] = lxx_ref(book, ch, vs)
        prev = lxx_ref(book, ch, vs - 1)
        v["lxx"], v["lxx_shifted"] = LXX.get(prev), prev
    elif lang == "H":
        v["lxx_ref"] = lxx_ref(book, ch, vs)
        v["lxx"] = LXX.get(v["lxx_ref"])
        if not v["lxx"]:  # Swete's digital text sometimes numbers a stretch one verse behind (its "Deut 14:28" is verse 29)
            lb, lc, lv = v["lxx_ref"].split(".")
            prev = f"{lb}.{lc}.{int(lv) - 1}"
            if LXX.get(prev):
                v["lxx"], v["lxx_shifted"] = LXX[prev], prev
    json.dump(v, open(os.path.join(HERE, "data", nd["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    open(os.path.join(HERE, "digest", nd["id"] + ".txt"), "w", encoding="utf-8").write(digest(v))
    count += 1
print(count, "verses extracted")
