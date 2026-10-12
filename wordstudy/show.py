"""Print drafted English sentences beside the KJV, for review.   python show.py b1 b2 ..."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for vid in sys.argv[1:]:
    v = json.load(open(os.path.join(HERE, "data", vid + ".json"), encoding="utf-8"))
    a = json.load(open(os.path.join(HERE, "authored", vid + ".json"), encoding="utf-8"))
    en = "".join(s if isinstance(s, str) else (f"[{s['t']}]" if "sup" in s else s["t"]) for s in a["en"])
    kjv = next((t["text"] for t in v["translations"] if t["key"] == "KJV"), "")
    notes = sum(1 for e in a["words"].values() if e.get("n"))
    print(f"{vid} {v['ref']}\n  OURS: {en}\n  KJV:  {kjv}\n  notes: {notes}  tr_note: {a.get('tr_note', '')[:160]}\n")
