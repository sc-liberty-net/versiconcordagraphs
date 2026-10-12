"""Give every word of Swete's Septuagint its dictionary form (lemma), and a Strong's number where one exists.

Swete's text (greek/lxx-swete/) carries no lemmas. Open Scriptures' GreekResources
(greek/lxx-lemmas/, CC BY 4.0) carries a lemma for every word of the Septuagint, but in the
word order of Rahlfs's edition (the CATSS text), without the Greek words themselves. The two
editions agree on most words, so each verse is aligned: Swete's words against Rahlfs's lemma
list, by spelling similarity, with gaps allowed where the editions differ. A Swete word that
finds no plausible partner is left without a lemma rather than given a guess.

    python align_lxx.py            -> greek/lxx-swete-lemmas.json and greek/lxx-swete-lemmas-report.txt
    python align_lxx.py Deut.24.19 -> also print that verse's alignment

Strong's numbers come from GreekResources' Greek Word List, which gives them for words that
also occur in the New Testament. Credit if published: "Open Scriptures Septuagint Project"
(CC BY 4.0) for lemmas and Strong's numbers; Swete's digital text is CC BY-SA 4.0 (see README).
"""
import json, os, re, sys, glob, unicodedata, random
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
SWETE = os.path.join(HERE, "greek", "lxx-swete", "data")
LEMMAS = os.path.join(HERE, "greek", "lxx-lemmas")
OUT = os.path.join(HERE, "greek", "lxx-swete-lemmas.json")
REPORT = os.path.join(HERE, "greek", "lxx-swete-lemmas-report.txt")

# Swete file -> GreekResources book. Joshua and Judges come in two text forms there; Swete
# printed Codex Vaticanus, so the B forms. Swete's Tobit is the B/A text.
BOOKS = {
    "Genesis": "Gen", "Exodus": "Exod", "Leviticus": "Lev", "Numeri": "Num", "Deuteronomium": "Deut",
    "Josue": "JoshB", "Judices": "JudgB", "Ruth": "Ruth", "Regnorum_I": "1Sam", "Regnorum_II": "2Sam",
    "Regnorum_III": "1Kgs", "Regnorum_IV": "2Kgs", "Paralipomenon_I": "1Chr", "Paralipomenon_II": "2Chr",
    "Esdras_A": "1Esd", "Esdras_B": "2Esd", "Esther": "Esth", "Judith": "Jdt", "Tobias": "TobBA",
    "Machabaeorum_i": "1Macc", "Machabaeorum_ii": "2Macc", "Machabaeorum_iii": "3Macc", "Machabaeorum_iv": "4Macc",
    "Psalmi": "Ps", "Odae": "Odes", "Proverbia": "Prov", "Canticum": "Song", "Job": "Job",
    "Sapientia_Salomonis": "Wis", "Ecclesiasticus": "Sir", "Psalmi_Salomonis": "PsSol",
    "Osee": "Hos", "Amos": "Amos", "Michaeas": "Mic", "Joel": "Joel", "Abdias": "Obad", "Jonas": "Jonah",
    "Nahum": "Nah", "Habacuc": "Hab", "Sophonias": "Zeph", "Aggaeus": "Hag", "Zacharias": "Zech",
    "Malachias": "Mal", "Isaias": "Isa", "Jeremias": "Jer", "Baruch": "Bar", "Threni_seu_Lamentationes": "Lam",
    "Epistula_Jeremiae": "EpJer", "Ezechiel": "Ezek", "Susanna_translatio_Graeca": "SusOG",
    "Susanna_Theodotionis_versio": "SusTh", "Daniel_translatio_Graeca": "DanOG",
    "Daniel_Theodotionis_versio": "DanTh", "Bel_et_Draco_translatio_Graeca": "BelOG",
    "Bel_et_Draco_Theodotionis_versio": "BelTh",
}

# Forms that share too few letters with their lemma for spelling to find them.
IRREGULAR = {
    "ο": "ο η το του της τω τη τον την οι αι τα των τοις ταις τουσ τους τας",
    "ειμι": "ειμι ει εστι εστιν ην ησαν εσται εσονται εσομαι εση εσμεν εστε εισι εισιν ων ουσα ον οντος οντες ουσης οντα οντων ουσιν ειναι ητω ω ης η ωσιν ημην ημεν ητε εσεσθε εσεσθαι εστω εστωσαν ουσαι",
    "λεγω": "ειπεν ειπον ειπας ειπατε ειπαν ειπε ειπη ειπης ειπω ειπων ειπουσα ειποντες ειπειν ερει ερω ερεις ερουσιν ερειτε ερουσι ειρηκα ειρηκεν ειρηται ρηθεν ελεχθη",
    "εγω": "εγω με εμε μου εμου μοι εμοι ημεις ημας ημων ημιν",
    "συ": "συ σε σου σοι υμεις υμας υμων υμιν",
    "οραω": "ειδον ειδεν ειδες ιδε ιδειν ιδων ιδουσα ιδοντες ιδη ιδωσιν οψεται οψομαι οψεσθε οψη ωφθη οφθησεται εωρακα εωρακας εωρακεν ειδετε",
    "ερχομαι": "ηλθεν ηλθον ηλθες ηλθοσαν ελθειν ελθων ελθουσα ελθοντες ελθη ελευσεται ελευσονται ελευσομαι εληλυθα εληλυθεν ελθε",
    "φερω": "ηνεγκεν ηνεγκαν ενεγκειν οισει οισω οισετε οισουσιν ενεγκε ενεχθη",
    "εσθιω": "εφαγεν εφαγον φαγειν φαγη φαγεται φαγεσθε φαγετε φαγων φαγοντες εδεται εδεσθε",
    "πινω": "επιεν επιον πιειν πιεται πιεσθε πιε πιων",
    "λαμβανω": "λαβειν λαβε λαβετε λαβων λαβοντες λαβουσα ελαβεν ελαβον ελαβες ελαβοσαν λαβη λαβωσιν λημψεται λημψομαι λημψη λημψονται ληψεται ληψομαι ειληφα ειληφεν ελημφθη",
    "ευρισκω": "ευρεν ευρον ευρες ευρειν ευρη ευρωσιν ευρησει ευρησεις ευρησουσιν ευρεθη ευρεθησεται",
    "αναβαινω": "ανεβη ανεβησαν ανεβην αναβηθι αναβησεται",
    "καταβαινω": "κατεβη κατεβησαν καταβηθι καταβησεται",
    "εξερχομαι": "εξηλθεν εξηλθον εξηλθοσαν εξελθειν εξελθων εξελευσεται εξελευσονται",
    "εισερχομαι": "εισηλθεν εισηλθον εισηλθοσαν εισελθειν εισελθων εισελευσεται εισελευσονται",
    "αποστελλω": "απεστειλεν απεστειλα αποστελω αποστειλον",
    "εχω": "εσχεν εσχον εξει εξεις εξουσιν εξετε σχη",
    "αιρω": "ηρεν ηραν αρον αρει αρατε",
    "πιπτω": "επεσεν επεσον πεσειται πεσουνται πεσων",
    "βαλλω": "εβαλεν εβαλον βαλειν βαλει",
    "αποθνησκω": "απεθανεν απεθανον αποθανειται αποθανη αποθανειν αποθανουνται",
    "γινωσκω": "εγνω εγνων εγνωσαν γνωσεσθε γνωσεται γνωναι γνωθι γνωσονται εγνωκα",
    "αγω": "ηγαγεν ηγαγον αξει",
    "τρεχω": "εδραμεν δραμων",
    "διδωμι": "εδωκεν εδωκα εδωκας εδωκαν δωσω δωσει δωσεις δωσουσιν δος δουναι δους δοτε δεδωκα δεδωκεν εδοθη δοθησεται",
    "τιθημι": "εθηκεν εθηκα εθετο θησω θησει θες θειναι τεθεικα",
    "ιστημι": "εστη εστησεν εστησαν στησον στησει στηναι εστηκεν εστηκως εστως",
    "ιημι": "",
    "γυνη": "γυναικα γυναικος γυναικι γυναικες γυναικων γυναιξιν γυναιξι γυναικας",
    "ανηρ": "ανδρος ανδρι ανδρα ανδρες ανδρων ανδρασιν ανδρασι ανδρας ανερ",
    "πατηρ": "πατρος πατρι πατερα πατερες πατερων πατρασιν πατρασι πατερας πατερ",
    "μητηρ": "μητρος μητρι μητερα",
    "θυγατηρ": "θυγατρος θυγατρι θυγατερα θυγατερες θυγατερων θυγατερας",
    "υδωρ": "υδατος υδατι υδατα υδατων",
    "χειρ": "χειρος χειρι χειρα χειρες χειρων χερσιν χερσι χειρας",
    "πας": "παντα παντος παντι παντες παντων πασιν πασι πασα πασης παση πασαν πασαι πασων πασαις πασας παν",
    "μεγας": "μεγαλη μεγαλην μεγαλης μεγαλου μεγαλω μεγαλοι μεγαλα μεγαλων μεγαλοις μεγαλους μεγαλας μεγα",
    "πολυς": "πολλη πολλην πολλης πολλου πολλω πολλοι πολλα πολλων πολλοις πολλους πολλας πολυ",
    "εις.1": "μια μιαν μιας ενα ενος ενι εν",
    "δυο": "δυσιν δυσι",
    "ος": "ος η ο ου ης ω η ον ην οι αι α ων οις αις ους ας",
}
IRREG = {}
for k, forms in IRREGULAR.items():
    for f in forms.split():
        IRREG.setdefault(f, set()).add(k)


def bare(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = s.replace("ς", "σ").replace("ϲ", "σ")
    return re.sub(r"[^α-ω]", "", s)


def sim(word, key):
    """Plausibility, 0..1, that a Swete word form is an instance of a lemma key."""
    s, k = bare(word), bare(key.split(".")[0])
    if not s or not k:
        return 0.0
    if s == k:
        return 1.0
    if key in IRREG.get(s, ()) or key.split(".")[0] in IRREG.get(s, ()):
        return 0.95
    best = 0.0
    for cand in {s, s[1:] if s[0] in "εη" and len(s) > 3 else s}:
        n = 0
        while n < min(len(cand), len(k)) and cand[n] == k[n]:
            n += 1
        if n >= 4 or (n >= 2 and n >= len(k) - 2) or (len(cand) <= 2 and k.startswith(cand)):
            best = max(best, 0.6 + 0.4 * n / max(len(k), len(cand)))
        best = max(best, 0.8 * SequenceMatcher(None, cand, k).ratio())
    return best


THRESH = 0.5


def align(words, lemmas):
    """Needleman-Wunsch, maximising summed similarity; gaps are free, weak pairs are not allowed."""
    n, m = len(words), len(lemmas)
    S = [[sim(w, l["key"]) for l in lemmas] for w in words]
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        P[i][0] = "u"
    for j in range(1, m + 1):
        P[0][j] = "l"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opts = [(D[i - 1][j], "u"), (D[i][j - 1], "l")]
            if S[i - 1][j - 1] >= THRESH:
                opts.append((D[i - 1][j - 1] + S[i - 1][j - 1], "d"))
            D[i][j], P[i][j] = max(opts)
    pairs, i, j = {}, n, m
    while i > 0 or j > 0:
        p = P[i][j]
        if p == "d":
            pairs[i - 1] = (j - 1, S[i - 1][j - 1]); i -= 1; j -= 1
        elif p == "u":
            i -= 1
        else:
            j -= 1
    return pairs


def load_wordlist():
    wl = {}
    for line in open(os.path.join(LEMMAS, "GreekWordList.js"), encoding="utf-8-sig"):
        m = re.match(r'\s*"([^"]+)": (\{.*\}),?\s*$', line)
        if m:
            wl[m.group(1)] = json.loads(m.group(2))
    return wl


def strong_for(key, wl):
    seen = set()
    while key in wl and key not in seen:
        seen.add(key)
        e = wl[key]
        if e.get("strong"):
            return "G" + e["strong"].zfill(4)
        key = e.get("v", "")
    return None


def main():
    wl = load_wordlist()
    out, lines, shifted = {}, [], []
    totals = {"words": 0, "matched": 0, "exact": 0, "verses": 0, "verses_missing": 0, "strong": 0}
    for path in sorted(glob.glob(os.path.join(SWETE, "*.txt"))):
        name = re.sub(r"^\d+\.", "", os.path.basename(path))[:-4]
        book = BOOKS.get(name)
        if not book:
            lines.append(f"{name}: no lemma book mapped, skipped"); continue
        lem = json.load(open(os.path.join(LEMMAS, "LxxLemmas", book + ".js"), encoding="utf-8-sig"))
        prefix = next(iter(lem)).split(".")[0]  # the lemma files use their own abbreviations (Josh, 1Esdr, Cant)
        verses = {}
        for line in open(path, encoding="utf-8-sig"):
            parts = line.rstrip("\n").split(" ", 1)
            if len(parts) == 2 and re.match(r"^\d+\.\d+\.\d+$", parts[0]):
                _, ch, vs = parts[0].split(".")
                if book == "EpJer" and ch == "0":  # Swete numbers the Letter of Jeremiah as chapter 0
                    ch = "1"
                verses.setdefault((f"{book}.{ch}.{vs}", f"{prefix}.{ch}.{vs}"), []).append(parts[1])
        b = {"words": 0, "matched": 0, "exact": 0, "verses": 0, "missing": 0}
        for (ref, lref), words in verses.items():
            b["verses"] += 1
            lemmas = lem.get(lref)
            rows = []
            if not lemmas:
                b["missing"] += 1
                rows = [{"w": w, "lemma": None, "key": None, "strong": None, "fit": 0} for w in words]
            else:
                pairs = align(words, lemmas)
                # Swete's digital text sometimes numbers a stretch one verse off (its "Deut 14:28" holds
                # verse 29). If this verse matches badly, try the neighbouring verses' lemma lists.
                if len(pairs) < 0.5 * len(words):
                    _, ch2, vs2 = lref.split(".")
                    for nb in (f"{prefix}.{ch2}.{int(vs2) + 1}", f"{prefix}.{ch2}.{int(vs2) - 1}"):
                        if lem.get(nb):
                            p2 = align(words, lem[nb])
                            if len(p2) >= 0.75 * len(words) and len(p2) > len(pairs):
                                pairs, lemmas = p2, lem[nb]
                                shifted.append(f"{ref} -> {nb}")
                                break
                for i, w in enumerate(words):
                    if i in pairs:
                        j, s = pairs[i]
                        key = lemmas[j]["key"]
                        st = strong_for(key, wl)
                        rows.append({"w": w, "lemma": lemmas[j]["lemma"], "key": key, "strong": st, "fit": round(s, 2)})
                        b["matched"] += 1; b["exact"] += s >= 0.95; totals["strong"] += bool(st)
                    else:
                        rows.append({"w": w, "lemma": None, "key": None, "strong": None, "fit": 0})
            b["words"] += len(words)
            if not lemmas:
                totals["words_in_missing"] = totals.get("words_in_missing", 0) + len(words)
            out[ref] = rows
        for k in ("words", "matched", "exact", "verses"):
            totals[k] += b[k]
        totals["verses_missing"] += b["missing"]
        lines.append(f"{book:7} {b['verses']:5} verses  {b['words']:7} words  matched {b['matched'] / max(b['words'], 1):6.1%}"
                     f"  exact {b['exact'] / max(b['words'], 1):6.1%}  verses with no lemma list {b['missing']}")
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    head = (f"Swete words: {totals['words']:,} in {totals['verses']:,} verses\n"
            f"Given a lemma: {totals['matched']:,} ({totals['matched'] / totals['words']:.1%}); "
            f"spelled exactly or a listed irregular form: {totals['exact'] / totals['words']:.1%}\n"
            f"Carrying a Strong's number (words also in the New Testament): {totals['strong']:,}\n"
            f"Verses with no lemma list at that reference: {totals['verses_missing']:,} "
            f"({totals.get('words_in_missing', 0):,} words)\n"
            f"Given a lemma, counting only verses that have a lemma list: "
            f"{totals['matched'] / (totals['words'] - totals.get('words_in_missing', 0)):.1%}\n"
            f"A fit under 0.7 is a loose pairing: read it as a guess.\n")
    head += f"Verses matched against a neighbouring verse's lemma list (numbering off by one): {len(shifted)}\n"
    open(REPORT, "w", encoding="utf-8").write(head + "\n" + "\n".join(lines) + "\n\nShifted verses:\n" +
                                              "\n".join(shifted) + "\n")
    print(head)
    rng = random.Random(7)
    show = sys.argv[1:] or []
    for ref in show + rng.sample(sorted(out), 3):
        print(ref)
        for r in out.get(ref, []):
            print(f"   {r['w']:18} {r['lemma'] or '-':16} {r['strong'] or '':7} {r['fit']}")


if __name__ == "__main__":
    main()
