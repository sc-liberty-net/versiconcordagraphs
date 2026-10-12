"""Gather per-word data for the study-layer pilot. Reads only; writes pilot_data.json in the scratchpad."""
import json, csv, re, os, glob, collections

ROOT = r"C:\Users\ethan\Desktop\Biblography"
SRC = os.path.join(ROOT, "bible-sources")
OUT = os.path.join(os.path.dirname(__file__), "pilot_data.json")

VERSES = [
    ("p2", "Matthew 25:24", "Mat.25.24", "G", "TAGNT Mat-Jhn"),
    ("q4", "Deuteronomy 24:19", "Deu.24.19", "H", "TAHOT Gen-Deu"),
    ("h5", "Hebrews 7:8", "Heb.7.8", "G", "TAGNT Act-Rev"),
]

nodes = {r["id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "corpus_nodes.csv"), encoding="utf-8"))}
clusters = {r["key"]: r for r in csv.DictReader(open(os.path.join(ROOT, "corpus_clusters.csv"), encoding="utf-8"))}
trans = json.load(open(os.path.join(ROOT, "translations.json"), encoding="utf-8"))
sidx = json.load(open(os.path.join(ROOT, "strongs_index.json"), encoding="utf-8"))["verses"]

# Bible-wide verse counts per extended Strong's id, and per bare number
count_e, count_b = collections.Counter(), collections.Counter()
for ref, ids in sidx.items():
    for s in set(ids):
        count_e[s] += 1
    for s in set(re.match(r"[HG]\d+", i).group(0) for i in ids if re.match(r"[HG]\d+", i)):
        count_b[s] += 1

def lexfile(prefix):
    return glob.glob(os.path.join(SRC, "stepbible", prefix + "*"))[0]

def load_tbes(prefix):
    d = {}
    for line in open(lexfile(prefix), encoding="utf-8-sig"):
        c = line.rstrip("\n").split("\t")
        if len(c) >= 8 and re.match(r"^[HG]\d", c[0]):
            d.setdefault(c[2].strip(), {"lemma": c[3], "translit": c[4], "pos": c[5], "gloss": c[6], "def": c[7]})
    return d

tbesh, tbesg = load_tbes("TBESH"), load_tbes("TBESG")
ges = {}
for e in json.load(open(os.path.join(SRC, "lexicons", "gesenius", "gesenius-entries.json"), encoding="utf-8")):
    if e.get("strongs"):
        ges.setdefault(e["strongs"], e)
thayer = {}
for e in json.load(open(os.path.join(SRC, "lexicons", "thayer", "thayer-entries.json"), encoding="utf-8")):
    if e.get("strongs"):
        thayer.setdefault(e["strongs"], e)
bdbmap = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(SRC, "lexicons", "bdb", "bdbToStrongsMapping.csv"), encoding="utf-8")):
    bdbmap[r["strongs"]].append(r["bdb"])

def bdb(num):
    out = []
    for b in bdbmap.get(num, []):
        p = os.path.join(SRC, "lexicons", "bdb", "json_output", b + ".json")
        if os.path.exists(p):
            j = json.load(open(p, encoding="utf-8"))
            j["id"] = b
            out.append(j)
    return out

def bare(s):
    m = re.match(r"([HG])(\d+)", s)
    return f"{m.group(1)}{int(m.group(2)):04d}" if m else s

def strip_ref(s):
    return re.sub(r"<[^>]+>", " ", s or "").replace("  ", " ").strip()

def lexicon_for(estrong, lang):
    b = bare(estrong)
    rec = {"estrong": estrong, "strongs": b,
           "count_e": count_e.get(estrong, 0), "count_b": count_b.get(b, 0)}
    tb = (tbesh if lang == "H" else tbesg)
    t = tb.get(estrong) or tb.get(b) or next((v for k, v in tb.items() if k.startswith(b)), None)
    rec["brief"] = t
    if lang == "H":
        g = ges.get(b)
        rec["gesenius"] = {k: g[k] for k in ("headword", "page", "image", "url", "text", "check", "unsure", "found_by")} if g else None
        rec["bdb"] = bdb(b)
    else:
        th = thayer.get(b)
        rec["thayer"] = {k: th[k] for k in ("lemma", "text", "check", "score")} if th else None
    return rec

data = []
for nid, ref, code, lang, fprefix in VERSES:
    path = glob.glob(os.path.join(ROOT, "lemma-data", fprefix + "*"))[0]
    words = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith(code + "#"):
            continue
        c = line.rstrip("\n").split("\t")
        if lang == "G":
            if "SBL" not in c[5] and "NA28" not in c[5]:
                continue
            m = re.match(r"(.+?) \((.+)\)", c[1])
            st, gram = c[3].split("=", 1)
            lem, gl = c[4].split("=", 1)
            words.append({"n": c[0].split("#")[1].split("=")[0], "orig": m.group(1), "translit": m.group(2),
                          "eng": c[2], "parts": [{"strong": st, "gram": gram, "lemma": lem, "gloss": gl, "main": True}],
                          "submeaning": c[9] if len(c) > 9 else ""})
        else:
            hebs, tl, en = c[1].split("/"), c[2].split("/"), c[3].split("/")
            sts, grs = c[4].split("/"), c[5].split("/")
            exp = c[11].split("/") if len(c) > 11 else []
            parts = []
            for i, s in enumerate(sts):
                s2 = s.split("\\")[0]
                main = s2.startswith("{")
                ex = exp[i] if i < len(exp) else ""
                exm = re.match(r"\{?(H\w+)=([^=]+)=([^}]*)\}?", ex.split("\\")[0])
                parts.append({"strong": s2.strip("{}"), "gram": grs[i] if i < len(grs) else "",
                              "heb": hebs[i] if i < len(hebs) else "", "eng": en[i].strip() if i < len(en) else "",
                              "lemma": exm.group(2) if exm else "", "gloss": exm.group(3) if exm else "", "main": main})
            words.append({"n": c[0].split("#")[1].split("=")[0], "orig": c[1].replace("/", "").replace("\\", ""),
                          "translit": c[2].replace("/", ""), "eng": c[3].replace("/", ""), "parts": parts})
    for w in words:
        for p in w["parts"]:
            if p["main"]:
                p["lex"] = lexicon_for(p["strong"], lang)
    node = nodes[nid]
    data.append({"id": nid, "ref": ref, "lang": lang, "cluster": clusters[node["cluster"]]["name"],
                 "gist": node["gist"], "translations": trans.get(ref, {}), "words": words})

json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Compact digest for authoring
for v in data:
    print("=" * 70)
    print(v["ref"], "|", v["cluster"], "|", v["gist"])
    for k, t in v["translations"].items():
        print(f"  {k}: {t}")
    for w in v["words"]:
        for p in w["parts"]:
            if not p["main"]:
                continue
            L = p["lex"]
            br = L["brief"] or {}
            print(f" #{w['n']} {w['orig']} [{w['translit']}] '{w['eng']}' | {p['strong']} {p['gram']} | {p['lemma']}={p['gloss']} | n={L['count_e']}/{L['count_b']}")
            print("     brief:", strip_ref(br.get("def", ""))[:260])
            if v["lang"] == "H":
                g = L.get("gesenius")
                if g:
                    print(f"     ges p.{g['page']} check={g['check']} unsure={g['unsure']}:", g["text"][:260].replace("\n", " "))
                for b in L.get("bdb", [])[:2]:
                    print(f"     bdb {b['id']}: {b.get('primary')} | senses={len(b.get('senses') or [])}")
            else:
                th = L.get("thayer")
                if th:
                    print(f"     thayer check={th['check']}:", th["text"][:200].replace("\n", " "))
