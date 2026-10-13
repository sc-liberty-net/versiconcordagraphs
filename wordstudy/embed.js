/* The Word Study inside the concordagraph. build.py writes this file, preceded by the study data
   as window.WORDSTUDY, to ../wordstudy.js. The concordagraph loads it if it is there; without it
   the page shows its one-line summaries, as before.

   What it gives the page (window.WS):
     WS.has(id)          is this passage drafted? (bare ids: "k1", not "tithe:k1")
     WS.reading(id)      our literal English, every word a button, with the KJV beneath
     WS.study(wordId)    the full study of one word: grammar, renderings, Septuagint, lexicons
     WS.verseOf(wordId)  the passage a word belongs to
   Hover synonyms are handled here. Clicks are left to the page, which owns its panel:
   .ws-e[data-id] opens a word, [data-ws-goto] another word, [data-ws-step] the next or previous
   word, [data-ws-back] the passage again.

   The study functions follow template.html; keep the two in step when either changes. */
(function () {
  const DATA = window.WORDSTUDY;
  if (!DATA) return;
  const VERSES = DATA.verses, LEX = DATA.lex;
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const wrapHeb = s => s.replace(/([֐-׿][֐-׿\s־]*[֐-׿]|[֐-׿])/g, '<span lang="he" dir="rtl">$1</span>');
  const fmtSource = s => wrapHeb(esc(s))
    .replace(/\*([^*\n]+)\*/g, "<em>$1</em>")
    .replace(/\[\?\]/g, '<mark class="q" title="The transcriber was unsure of this reading">[?]</mark>')
    .replace(/\n/g, "<br>");
  const MINOR = /^(CONJ|PRT|PREP|COND|T-|P-|R-)|^(Tc|Tn|Td|To|Tr|R|Rd|C|c)$/;
  const vById = new Map(VERSES.map(v => [v.id, v]));
  const byId = new Map();
  VERSES.forEach(v => v.words.forEach((w, i) => byId.set(w.id, { v, w, i })));

  /* Greek and Hebrew need faces the page's Spectral does not carry. */
  const fonts = document.createElement("link");
  fonts.rel = "stylesheet";
  fonts.href = "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Noto+Serif+Hebrew:wght@400;500&display=swap";
  document.head.append(fonts);

  const css = document.createElement("style");
  css.textContent = `
.ws-label{display:block; font-family:Archivo,sans-serif; font-size:11.5px; letter-spacing:.03em; color:var(--ink-3); margin:0 0 3px}
.ws-reading{font-family:Spectral,Georgia,serif; font-size:17.5px; line-height:1.75; color:var(--ink); margin:0 0 12px}
.ws-e{appearance:none; border:0; margin:0; padding:0 1px; font:inherit; color:inherit; background:transparent; cursor:pointer;
  border-radius:3px; text-decoration:underline; text-decoration-color:var(--line); text-decoration-thickness:2px; text-underline-offset:5px}
.ws-e:hover{background:var(--sunk); text-decoration-color:var(--ink-3)}
.ws-sup{font-style:italic; color:var(--ink-2); cursor:help}
.ws-kjv{font-family:Spectral,Georgia,serif; font-size:15px; line-height:1.55; color:var(--ink-2); margin:0 0 12px}
.ws-trnote{font-size:12.5px; line-height:1.5; color:var(--ink-2); margin:0 0 12px}
.ws-hint{font-size:12.5px; color:var(--ink-3); margin:0 0 14px}
.ws-bar{display:flex; flex-wrap:wrap; align-items:center; gap:6px; margin:0 0 14px}
.ws-bar .ws-pos{flex:1 1 100%; font-size:12px; color:var(--ink-3)}
.ws-btn{appearance:none; border:1px solid var(--line); background:var(--paper); color:var(--ink); font:inherit; font-size:12.5px;
  border-radius:99px; padding:3px 11px; cursor:pointer; text-align:left}
.ws-btn:hover{border-color:var(--ink-3)}
.ws-btn[aria-current="true"]{background:var(--ink-2); border-color:var(--ink-2); color:var(--surface)}
.ws-study{display:grid; gap:20px}
.ws-study h3{margin:0 0 8px}
.ws-orig{margin:0; font-family:"EB Garamond",Spectral,Georgia,serif; font-size:34px; line-height:1.15}
.ws-orig[lang="he"]{font-family:"Noto Serif Hebrew","SBL Hebrew",serif; font-size:31px; line-height:1.4}
[lang="grc"]{font-family:"EB Garamond",Spectral,Georgia,serif}
.panel [lang="he"],.ws-tip [lang="he"]{font-family:"Noto Serif Hebrew","SBL Hebrew",serif}
.ws-lemma{margin:4px 0 0; font-size:13.5px; color:var(--ink-2)}
.ws-lemma b{font-size:16px; font-weight:500; color:var(--ink)}
.ws-facts{margin:12px 0 0; display:grid; grid-template-columns:max-content minmax(0,1fr); gap:5px 12px; font-size:13.5px}
.ws-facts dt{color:var(--ink-2)}
.ws-facts dd{margin:0}
.ws-mono{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; font-size:12.5px}
.ws-covers{display:flex; flex-wrap:wrap; align-items:center; gap:6px; margin:12px 0 0; font-size:12.5px; color:var(--ink-2)}
.ws-draft{border-left:3px solid var(--ink-3); padding-left:12px}
.ws-draft p{margin:0}
.ws-badge{display:inline-block; margin-bottom:8px; font-size:11.5px; color:var(--ink-2); background:var(--sunk); border-radius:99px; padding:1px 9px}
.ws-sense{font-family:Spectral,Georgia,serif; font-size:16px; line-height:1.45}
.ws-syn{list-style:none; margin:10px 0 0; padding:0; display:flex; flex-wrap:wrap; gap:5px}
.ws-syn li{border:1px solid var(--ink-3); border-radius:99px; padding:2px 10px; font-size:13px}
.ws-note{margin-top:10px !important; font-size:13.5px; line-height:1.5}
.ws-renders table{width:100%; border-collapse:collapse; font-size:13.5px}
.ws-renders td{padding:5px 0; vertical-align:top}
.ws-renders tr + tr td{border-top:1px solid var(--line)}
.ws-renders td:first-child{color:var(--ink-2); width:44%; padding-right:10px}
.ws-renders td:last-child{font-family:Spectral,Georgia,serif; font-size:15px}
.ws-renders .none{font-family:Archivo,sans-serif; font-size:12px; color:var(--ink-3); font-style:italic}
.ws-renders tr.ours td{color:var(--ink); font-weight:600}
.ws-built ol{list-style:none; margin:0; padding:0; display:grid; gap:7px}
.ws-built li{display:grid; grid-template-columns:4rem minmax(0,1fr); gap:10px; align-items:baseline; font-size:13.5px}
.ws-built .h{font-size:19px; text-align:right; direction:rtl}
.ws-built .m{color:var(--ink-3); font-size:12px; display:block}
.ws-built li.main .h{font-weight:600}
.ws-lxx-g{margin:0; font-size:23px; line-height:1.3}
.ws-lxx-d{margin:4px 0 0; font-size:13.5px; color:var(--ink-2)}
.ws-lxx-d b{font-size:16px; font-weight:500; color:var(--ink)}
.ws-links ul{list-style:none; margin:0; padding:0; display:grid; gap:9px}
.ws-links li{display:grid; gap:3px; justify-items:start; font-size:12px; color:var(--ink-2)}
.ws-lex{display:grid; gap:8px}
.ws-lex details{border:1px solid var(--line); border-radius:8px; background:var(--paper)}
.ws-lex summary{cursor:pointer; padding:9px 12px; display:flex; flex-wrap:wrap; gap:3px 9px; align-items:baseline}
.ws-lex summary b{font-weight:600; font-size:13.5px}
.ws-lex summary span{font-size:12px; color:var(--ink-2)}
.ws-lex .body{padding:0 12px 12px; font-size:13.5px; line-height:1.6; overflow-wrap:anywhere}
.ws-lex .body p{margin:0 0 8px}
.ws-lex .src{font-family:Spectral,Georgia,serif; font-size:15px; line-height:1.55}
.ws-lex ul{margin:6px 0 0; padding-left:18px}
.ws-flag{display:block; margin:0 0 9px; padding:7px 9px; border-radius:7px; background:var(--sunk); color:var(--ink); font-size:12px; line-height:1.45}
mark.q{background:var(--sunk); color:var(--ink); border-radius:3px; padding:0 2px}
.ws-credit{font-size:11.5px; line-height:1.5; color:var(--ink-3); border-top:1px solid var(--line); padding-top:10px; margin:0}
.ws-tip{position:fixed; z-index:30; max-width:280px; pointer-events:none; background:var(--ink); color:var(--surface);
  border-radius:9px; padding:9px 11px; font-size:13.5px; line-height:1.4; box-shadow:0 6px 20px rgba(0,0,0,.25)}
.ws-tip .tl{font-family:Spectral,Georgia,serif; font-size:15.5px}
.ws-tip .ts{margin-top:3px}
.ws-tip .th{margin-top:5px; font-size:11.5px; opacity:.8}
`;
  document.head.append(css);

  function countText(w) {
    const n = w.count, all = w.countAll;
    const one = k => `${k.toLocaleString()} verse${k === 1 ? "" : "s"}`;
    return n === all ? one(n) : `${one(n)} in this sense, ${one(all)} in all`;
  }

  function reading(id) {
    const v = vById.get(id);
    if (!v) return "";
    return `<p class="ws-reading"><span class="ws-label">This Project's Literal English · A Draft, Not Yet Reviewed</span>${v.en.map(s =>
        typeof s === "string" ? esc(s)
        : s.w ? `<button class="ws-e" type="button" data-id="${s.w[0]}">${esc(s.t)}</button>`
        : `<span class="ws-sup" title="${esc(s.sup)}" tabindex="0">${esc(s.t)}</span>`).join("")}</p>
      ${v.kjv ? `<p class="ws-kjv"><span class="ws-label">King James Version</span>${esc(v.kjv)}</p>` : ""}
      ${v.trNote ? `<p class="ws-trnote"><b>Textus Receptus:</b> ${esc(v.trNote)}</p>` : ""}
      <p class="ws-hint">Select any word for the ${v.lang === "H" ? "Hebrew" : "Greek"} behind it.</p>`;
  }

  function lexHTML(v, w) {
    const L = LEX[w.lk] || {}, out = [];
    if (L.fixNote) out.push(`<span class="ws-flag">Dictionary form corrected by this study. ${esc(L.fixNote)}</span>`);
    if (L.hideNote) out.push(`<span class="ws-flag">An entry matched to this word belongs to a different word spelled alike, so it is left out. ${esc(L.hideNote)}</span>`);
    if (v.lang === "H") {
      if (L.ges) {
        const flags = [];
        if (L.ges.partial) flags.push("Our parsed copy matched this word to a cross-reference or to part of a longer entry. Check the page scan for the full entry.");
        if (L.ges.check) flags.push("This word-to-entry match is marked doubtful in our parsed copy.");
        if (L.ges.unsure) flags.push(`The transcript holds ${L.ges.unsure} uncertain reading${L.ges.unsure > 1 ? "s" : ""}, marked [?]. The scan decides.`);
        out.push(`<details open><summary><b>Gesenius</b><span>Tregelles 1857, page ${esc(L.ges.page)}</span></summary><div class="body">
          ${flags.map(f => `<span class="ws-flag">${esc(f)}</span>`).join("")}
          <p class="src">${fmtSource(L.ges.text)}</p>
          <p><a href="${esc(L.ges.url)}" target="_blank" rel="noopener">${L.ges.more ? "Read the rest on the page scan" : "See the page scan"}</a></p></div></details>`);
      } else if (!L.hideNote) {
        out.push(`<details open><summary><b>Gesenius</b><span>no entry matched</span></summary><div class="body">
          <span class="ws-flag">No Gesenius entry is matched to this word in our parsed copy. It may sit under a related headword.</span></div></details>`);
      }
      if (L.bdb) {
        out.push(`<details${L.ges ? "" : " open"}><summary><b>Brown-Driver-Briggs</b><span>1906, ${esc(L.bdb.id)}</span></summary><div class="body">
          <p><span lang="he">${esc(L.bdb.head)}</span> ${esc(L.bdb.pos || "")}</p>
          ${L.bdb.primary ? `<p class="src"><em>${esc(L.bdb.primary)}</em>${L.bdb.desc ? `; ${esc(L.bdb.desc)}` : ""}</p>` : ""}
          ${L.bdb.senses.length ? `<ul>${L.bdb.senses.map(s => `<li>${wrapHeb(esc(s))}</li>`).join("")}</ul>` : ""}
        </div></details>`);
      }
      if (L.brief) out.push(`<details><summary><b>STEPBible brief lexicon</b><span>${esc(L.brief.gloss)}</span></summary><div class="body"><p>${fmtSource(L.brief.def)}</p></div></details>`);
    } else {
      if (L.brief) out.push(`<details open><summary><b>Abbott-Smith</b><span>Manual Greek Lexicon, 1922, via STEPBible</span></summary><div class="body"><p class="src">${fmtSource(L.brief.def)}</p></div></details>`);
      if (L.thayer) out.push(`<details><summary><b>Thayer</b><span>1889, machine-read</span></summary><div class="body">
        <span class="ws-flag">Read by machine from a scan. The English is reliable; the Greek letters inside the entry came out garbled.${L.thayer.check ? " This entry's match to the word is also marked doubtful." : ""}</span>
        <p>${esc(L.thayer.text)}</p></div></details>`);
    }
    return out.join("");
  }

  const bareG = s => (s || "").match(/^G\d{4}/)?.[0] || null;

  function lxxHTML(w) {
    const x = w.lxx;
    if (!x) return "";
    const flag = x.fit < 0.7 && !x.fixed ? '<span class="ws-flag">Loose match between Swete\'s word and the dictionary data. Read the dictionary form as a guess.</span>' : "";
    return `<section class="ws-lxx"><h3>In The Septuagint</h3>
      ${flag}
      <p class="ws-lxx-g" lang="grc">${esc(x.greek)}</p>
      <p class="ws-lxx-d">Dictionary form <b lang="grc">${esc(x.lemma)}</b>${x.gloss ? `, ${esc(x.gloss)}` : ""}${x.strong ? ` <span class="ws-mono">${esc(x.strong)}</span>` : ""}</p>
      <p class="ws-lxx-d">${x.strong ? `In the New Testament: ${x.nt.toLocaleString()} verse${x.nt === 1 ? "" : "s"}` : "Not used in the New Testament"}</p>
      ${x.note ? `<p class="ws-note">${wrapHeb(esc(x.note))}</p>` : ""}
    </section>`;
  }

  /* words in other passages that share a Greek word with this one, via the Septuagint */
  function linksHTML(v, w) {
    const mine = v.lang === "H" ? bareG(w.lxx?.strong) : bareG(w.strong);
    if (!mine || MINOR.test(w.code)) return "";
    const hits = [];
    VERSES.forEach(o => o.words.forEach(x => {
      if (x.id === w.id || MINOR.test(x.code)) return;
      const theirs = o.lang === "H" ? bareG(x.lxx?.strong) : bareG(x.strong);
      if (theirs === mine) {
        const seg = o.en.find(s => s.w && s.w.includes(x.id));
        hits.push(`<li><button class="ws-btn" type="button" data-ws-goto="${x.id}">${esc(o.ref)}: ${esc(seg ? seg.t : x.gloss)}</button>
          <span>${o.lang === "H" ? `Hebrew <span lang="he">${esc(x.orig)}</span>, Greek <span lang="grc">${esc(x.lxx.word)}</span> in the Septuagint` : `Greek <span lang="grc">${esc(x.orig)}</span>`}</span></li>`);
      }
    }));
    if (!hits.length) return "";
    return `<section class="ws-links"><h3>Same Greek Word In Other Passages</h3><ul>${hits.join("")}</ul></section>`;
  }

  function study(id) {
    const hit = byId.get(id);
    if (!hit) return "";
    const { v, w, i } = hit;
    const heb = v.lang === "H";
    const seg = v.en.find(s => s.w && s.w.includes(id));
    const covers = seg && seg.w.length > 1 ? `<p class="ws-covers">"${esc(seg.t)}" translates ${seg.w.length} words:
      ${seg.w.map(x => { const o = byId.get(x).w; return `<button class="ws-btn" type="button" data-ws-goto="${x}" aria-current="${x === id}"><span lang="${heb ? "he" : "grc"}">${esc(o.orig)}</span> ${esc(o.lgloss)}</button>`; }).join("")}</p>` : "";
    const renders = w.render.map(r => `<tr${r.ours ? ' class="ours"' : ""}><td>${esc(r.ours ? "This Edition (Draft)" : r.t)}</td><td>${r.r ? esc(r.r) : '<span class="none">not rendered</span>'}</td></tr>`).join("");
    const built = heb && w.built && w.built.length > 1 ? `<section class="ws-built"><h3>Built From</h3><ol>${w.built.map(p =>
      `<li class="${p.main ? "main" : ""}"><span class="h" lang="he">${esc(p.heb)}</span><span>${esc(p.eng)}<span class="m">${esc(p.gram)}</span></span></li>`).join("")}</ol></section>` : "";
    return `
      <div class="ws-bar">
        <span class="ws-pos">${esc(v.ref)}, word ${i + 1} of ${v.words.length}</span>
        <button class="ws-btn" type="button" data-ws-back>Back To The Passage</button>
        <button class="ws-btn" type="button" data-ws-step="-1" aria-label="Previous word"${i ? "" : " disabled"}>Prev</button>
        <button class="ws-btn" type="button" data-ws-step="1" aria-label="Next word"${i < v.words.length - 1 ? "" : " disabled"}>Next</button>
      </div>
      <div class="ws-study">
        <div>
          <p class="ws-orig" lang="${heb ? "he" : "grc"}" ${heb ? 'dir="rtl"' : ""}>${esc(w.orig)}</p>
          <p class="ws-lemma">Dictionary form <b lang="${heb ? "he" : "grc"}">${esc(w.lemma)}</b>, ${esc(w.lgloss)}</p>
          <dl class="ws-facts">
            <dt>Sounds Like</dt><dd class="ws-mono">${esc(w.tr)}</dd>
            <dt>Grammar</dt><dd>${esc(w.gram)}</dd>
            <dt>Strong's</dt><dd class="ws-mono">${esc(w.strong)}</dd>
            <dt>In The Bible</dt><dd>${countText(w)}</dd>
            ${w.trForm ? `<dt>KJV's Greek</dt><dd>The Textus Receptus reads <span lang="grc">${esc(w.trForm)}</span>${w.trGloss ? `, "${esc(w.trGloss)}"` : ""}</dd>`
              : w.trMoved ? "<dt>KJV's Greek</dt><dd>The Textus Receptus has this word in another position</dd>"
              : w.notTR ? "<dt>KJV's Greek</dt><dd>Not in the Textus Receptus, the Greek text the KJV translated</dd>" : ""}
          </dl>
          ${covers}
        </div>
        <section class="ws-draft">
          <h3>In This Verse</h3>
          <span class="ws-badge">Draft By Claude, Not Yet Reviewed</span>
          <p class="ws-sense">${esc(w.sense)}</p>
          <ul class="ws-syn" aria-label="Closest English">${w.syn.map(s => `<li>${esc(s)}</li>`).join("")}</ul>
          ${w.note ? `<p class="ws-note">${wrapHeb(esc(w.note))}</p>` : ""}
        </section>
        <section class="ws-renders"><h3>How The Translations Render It</h3><table>${renders}</table></section>
        ${built}
        ${lxxHTML(w)}
        ${linksHTML(v, w)}
        <section class="ws-lex"><h3>Lexicons</h3>${lexHTML(v, w)}</section>
        <p class="ws-credit">Word divisions, lemmas, grammar, counts and the brief lexicons (with Abbott-Smith) are from
          <a href="https://www.STEPBible.org" target="_blank" rel="noopener">STEP Bible</a>, Tyndale House Cambridge, CC BY 4.0, with this study's corrections marked.
          BDB: <a href="https://github.com/unfoldingWord/Brown-Driver-Briggs-Enhanced" target="_blank" rel="noopener">unfoldingWord's Brown-Driver-Briggs Enhanced</a>, CC BY.
          Gesenius (1857) and Thayer (1889) are public domain, read from archive.org scans.
          Septuagint: Swete's edition as digitised by the Open Greek and Latin Project's
          <a href="https://github.com/OpenGreekAndLatin/First1KGreek" target="_blank" rel="noopener">First1KGreek</a>, prepared by
          <a href="https://github.com/nathans/lxx-swete" target="_blank" rel="noopener">nathans/lxx-swete</a>, CC BY-SA 4.0; dictionary forms from the
          <a href="https://github.com/openscriptures/GreekResources" target="_blank" rel="noopener">Open Scriptures Septuagint Project</a>, CC BY 4.0.
          The King James (1769) and the other translations are public domain.</p>
      </div>`;
  }

  function step(id, d) {
    const hit = byId.get(id);
    const next = hit && hit.v.words[hit.i + d];
    return next ? next.id : null;
  }

  /* ---- hover synonyms: pointer devices only; touch goes straight to the study ---- */
  const tip = document.createElement("div");
  tip.className = "ws-tip"; tip.setAttribute("role", "tooltip"); tip.hidden = true;
  document.body.append(tip);
  const canHover = matchMedia("(hover: hover)");
  function showTip(el) {
    if (el.classList.contains("ws-sup")) {
      tip.innerHTML = `<div class="ts">${esc(el.title)}</div>`;
    } else {
      const hit = byId.get(el.dataset.id); if (!hit) return;
      const { v, w } = hit;
      tip.innerHTML = `<div class="tl"><span lang="${v.lang === "H" ? "he" : "grc"}">${esc(w.orig)}</span>, ${esc(w.lgloss)}</div>
        <div class="ts">${w.syn.slice(0, 5).map(esc).join(", ")}</div>
        <div class="th">Select for the full study</div>`;
    }
    tip.hidden = false;
    const r = el.getBoundingClientRect(), t = tip.getBoundingClientRect();
    let x = Math.min(Math.max(8, r.left + r.width / 2 - t.width / 2), innerWidth - t.width - 8);
    let y = r.top - t.height - 8;
    if (y < 8) y = r.bottom + 8;
    tip.style.left = x + "px"; tip.style.top = y + "px";
  }
  const hideTip = () => { tip.hidden = true; };
  document.addEventListener("mouseover", e => { const b = e.target.closest(".ws-e, .ws-sup"); if (b && canHover.matches) showTip(b); });
  document.addEventListener("mouseout", e => { if (e.target.closest(".ws-e, .ws-sup")) hideTip(); });
  document.addEventListener("focusin", e => { const b = e.target.closest(".ws-e, .ws-sup"); if (b && canHover.matches) showTip(b); else hideTip(); });
  document.addEventListener("focusout", hideTip);
  document.addEventListener("click", hideTip, true);
  addEventListener("scroll", hideTip, { passive: true, capture: true });

  window.WS = {
    has: id => vById.has(id),
    reading, study, step,
    verseOf: wordId => byId.get(wordId)?.v.id || null,
    count: VERSES.length
  };
  document.dispatchEvent(new Event("wordstudy:ready"));
})();
