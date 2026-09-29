(function () {
  const app = document.getElementById("app");
  const ROUNDS = 5;
  const PRAISE = ["Great job!", "Well done!", "Super!", "You got it!", "Awesome!"];
  const MIC =
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';

  // ---------- helpers ----------
  const lessonById = (id) => window.LESSONS.find((l) => l.id === id);
  const sceneById = (id) => window.SCENES.find((s) => s.id === id);
  // An item shows ART[item.art] when its word is already taken by another picture (e.g. the fruit "orange").
  // Counting items ({count, thing}) show that many copies of ART[thing].
  const pic = (it) => (it.count ? many(it.thing, it.count) : ART[it.art || it.word]);
  const cover = (l) => ART[l.cover] || pic(l.items.find((it) => it.word === l.cover));
  // The lesson's main game: most lessons use the listen game, "How many?" uses the count game.
  const mainGame = (l) =>
    l.game === "count"
      ? { view: "count", label: "Count", key: "count-" + l.id }
      : l.game === "blend"
      ? { view: "blend", label: "Blend", key: "blend-" + l.id }
      : { view: "play", label: "Listen", key: l.id };
  // Phonics: "bat" = onset "b" + family (rime) "at", and how to say each part on its own.
  const onsetOf = (it) => it.word.slice(0, it.word.length - it.family.length);
  const onsetSound = (o) => window.ONSET_SOUNDS[o] || o;
  const rimeSound = (lesson, rime) => (lesson.families.find((f) => f.rime === rime) || { sound: rime }).sound;
  const NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];
  const ZH_NUMBERS = ["一", "两", "三", "四", "五", "六", "七", "八", "九", "十"];

  // Scale one ART picture into the box (x, y, w, h) as a <g>, so it can sit inside another SVG.
  function fit(svg, x, y, w, h) {
    const [vx, vy, vw, vh] = svg.match(/viewBox="([^"]+)"/)[1].split(" ").map(Number);
    const s = Math.min(w / vw, h / vh);
    const dx = x + (w - vw * s) / 2 - vx * s;
    const dy = y + (h - vh * s) / 2 - vy * s;
    const inner = svg.slice(svg.indexOf(">") + 1, svg.lastIndexOf("</svg>"));
    return `<g transform="translate(${dx.toFixed(1)} ${dy.toFixed(1)}) scale(${s.toFixed(3)})">${inner}</g>`;
  }

  // n copies of a picture in rows of up to 5, as one SVG that sizes like any other picture.
  // Picks the number of columns that draws each copy biggest (pictures are about 6:5).
  function many(key, n, W = 164, H = 136) {
    const size = (c) => Math.min(W / c, (H / Math.ceil(n / c)) * 1.2);
    let cols = 1;
    for (let c = 2; c <= Math.min(n, 5); c++) if (size(c) >= size(cols)) cols = c;
    const rows = Math.ceil(n / cols);
    const cw = W / cols;
    const ch = H / rows;
    let out = "";
    for (let i = 0; i < n; i++) {
      const r = Math.floor(i / cols);
      const x = (W - Math.min(cols, n - r * cols) * cw) / 2 + (i % cols) * cw;
      const y = r * ch;
      out +=
        `<g class="thing" data-x="${(x + cw).toFixed(1)}" data-y="${y.toFixed(1)}" data-r="${Math.min(14, Math.min(cw, ch) * 0.17).toFixed(1)}">` +
        `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${cw.toFixed(1)}" height="${ch.toFixed(1)}" fill="transparent"/>` +
        fit(ART[key], x + cw * 0.04, y + ch * 0.04, cw * 0.92, ch * 0.92) +
        `</g>`;
    }
    return `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${out}</svg>`;
  }
  const bestScore = (key) => Number(localStorage.getItem("le-best-" + key) || 0);
  const showZh = () => localStorage.getItem("le-zh") === "1";
  const zhLine = (text, cls = "zh") =>
    text ? `<span class="${cls}" lang="zh-CN"${showZh() ? "" : " hidden"}>${text}</span>` : "";
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
  const praise = () => PRAISE[Math.floor(Math.random() * PRAISE.length)];
  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  const stars = (n, total = ROUNDS) =>
    `<span class="stars" aria-label="${n} of ${total} stars">${"★".repeat(n)}<span class="dim">${"★".repeat(total - n)}</span></span>`;
  // Round progress as dots: done, current, still to come. The text is kept for screen readers.
  const progress = (label, i, total) =>
    `<span class="dots" aria-hidden="true">${Array.from({ length: total }, (_, k) =>
      `<i class="${k < i ? "done" : k === i ? "now" : ""}"></i>`
    ).join("")}</span><span class="sr-only">${label} ${i + 1} of ${total}</span>`;

  // ---------- lesson colors ----------
  // Each lesson has one bright color, but white labels and colored text on it are often too faint to read
  // (yellow most of all). So each lesson also gets readable shades: --accent-strong is the fill behind button
  // labels (in --on-accent), and --accent-text is colored text on the lesson's pale --tint.
  const rgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
  const toHex = (c) => "#" + c.map((v) => v.toString(16).padStart(2, "0")).join("");
  const luminance = (c) => {
    const [r, g, b] = c.map((v) => ((v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const contrast = (a, b) => {
    const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  // The color darkened in small steps until it reaches `min` contrast against `bg`.
  const darken = (c, bg, min) => {
    let d = c;
    for (let k = 1; contrast(d, bg) < min && k > 0.3; ) {
      k -= 0.02;
      d = c.map((v) => Math.round(v * k));
    }
    return d;
  };
  const WHITE = [255, 255, 255];
  const INK = rgb("#3f3345");
  const themes = new Map();
  function theme({ color, tint }) {
    const key = color + tint;
    if (!themes.has(key)) {
      const c = rgb(color);
      // A light color like yellow keeps its fill and takes dark text instead of turning brown.
      const light = contrast(c, WHITE) < 3 && contrast(c, INK) >= 4.5;
      const strong = light ? c : darken(c, WHITE, 4.5);
      themes.set(
        key,
        `--accent:${color};--tint:${tint};--accent-strong:${toHex(strong)};` +
          `--on-accent:${light ? "var(--ink)" : "#fff"};--accent-text:${toHex(darken(c, rgb(tint), 4.5))}`
      );
    }
    return themes.get(key);
  }

  // Pip sits in the corner of the game pages and cheers whenever something is right.
  const BUDDY = () =>
    `<div class="buddy" aria-hidden="true"><span class="buddy-bubble"></span>` +
    `<span class="buddy-pip think">${ART._pip_think}</span><span class="buddy-pip cheer">${ART._pip_cheer}</span></div>`;
  let buddyTimer = 0;
  function cheer() {
    const b = app.querySelector(".buddy");
    if (!b) return;
    b.querySelector(".buddy-bubble").textContent = praise();
    b.classList.remove("happy");
    void b.offsetWidth;
    b.classList.add("happy");
    clearTimeout(buddyTimer);
    buddyTimer = setTimeout(() => b.classList.remove("happy"), 1800);
  }

  // A right answer: Pip cheers and paper confetti bursts from the middle of `el`.
  const COLORS = ["#ef5b56", "#ffd23f", "#4a9be8", "#5e9a2e", "#d65b9a", "#8150c4"];
  function celebrate(el, n = 26) {
    cheer();
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const r = el.getBoundingClientRect();
    const box = document.createElement("div");
    box.className = "confetti";
    box.setAttribute("aria-hidden", "true");
    box.style.left = r.left + r.width / 2 + "px";
    box.style.top = r.top + r.height / 2 + "px";
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      const angle = Math.random() * Math.PI * 2;
      const dist = 90 + Math.random() * 130;
      p.style.cssText =
        `--dx:${(Math.cos(angle) * dist).toFixed(0)}px;--dy:${(Math.sin(angle) * dist - 60).toFixed(0)}px;` +
        `--turn:${(Math.random() * 720 - 360).toFixed(0)}deg;background:${COLORS[i % COLORS.length]};` +
        `animation-delay:${(Math.random() * 0.08).toFixed(2)}s`;
      box.appendChild(p);
    }
    document.body.appendChild(box);
    setTimeout(() => box.remove(), 1400);
  }

  const said = new Set(JSON.parse(localStorage.getItem("le-said") || "[]"));
  const markSaid = (lessonId, word) => {
    said.add(lessonId + ":" + word);
    localStorage.setItem("le-said", JSON.stringify([...said]));
  };
  const saidCount = (lesson) => lesson.items.filter((it) => said.has(lesson.id + ":" + it.word)).length;
  const written = new Set(JSON.parse(localStorage.getItem("le-written") || "[]"));
  const markWritten = (ch) => {
    written.add(ch);
    localStorage.setItem("le-written", JSON.stringify([...written]));
  };
  const spellable = (lesson) => lesson.items.filter((it) => /^[a-z]+$/.test(it.word) && it.word.length <= 7);

  // A sentence split into word tiles. A multi-word item ("next to", "in front of") stays one tile,
  // except counting items, where the number and the noun are separate so the plural matters.
  function sentenceTiles(it) {
    const text = it.sentence.replace(/[.!?]$/, "");
    let words = text.split(" ");
    const key = it.word.toLowerCase().split(" ");
    if (key.length > 1 && !it.count) {
      const at = words.findIndex((_, k) => key.every((w, j) => (words[k + j] || "").toLowerCase() === w));
      if (at >= 0) words = [...words.slice(0, at), words.slice(at, at + key.length).join(" "), ...words.slice(at + key.length)];
    }
    return { words, end: it.sentence.slice(text.length) };
  }
  // One short sentence (3 to 6 tiles), no commas and no second sentence.
  const buildable = (lesson) =>
    lesson.items.filter((it) => {
      if (!it.sentence || /[.!?,;:]/.test(it.sentence.slice(0, -1))) return false;
      const n = sentenceTiles(it).words.length;
      return n >= 3 && n <= 6;
    });

  function bounce(el, cls = "pop") {
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
  }

  // ---------- settings ----------
  for (const [id, key, def] of [["accent", "le-accent", "en-US"], ["speed", "le-speed", "0.7"]]) {
    const el = document.getElementById(id);
    el.value = localStorage.getItem(key) || def;
    el.addEventListener("change", () => {
      localStorage.setItem(key, el.value);
      Speech.say("Hello!");
    });
  }
  const zhToggle = document.getElementById("zh");
  zhToggle.checked = showZh();
  zhToggle.addEventListener("change", () => {
    localStorage.setItem("le-zh", zhToggle.checked ? "1" : "0");
    document.querySelectorAll(".zh, .zh-sub").forEach((el) => (el.hidden = !zhToggle.checked));
  });
  // The voice panel closes on a tap outside it or on Escape.
  const more = document.querySelector(".more");
  document.addEventListener("click", (e) => {
    if (more.open && !more.contains(e.target)) more.open = false;
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && more.open) {
      more.open = false;
      more.querySelector("summary").focus();
    }
  });
  if (!Speech.supported) document.getElementById("no-speech").hidden = false;

  // ---------- islands ----------
  // The islands in the order Pip sails them, and the stops on each in order along its road.
  // "write" is the tracing pad; "scene-<id>" are the picture dictionaries (window.SCENES).
  // Each island's picture and where its stops sit are drawn in tools/art/build16.py (window.WORLD).
  // A lesson that isn't listed here goes on the last island, below the map if the road has no room for it.
  const ISLANDS = [
    { id: "abc", title: "ABC Island", zh: "字母岛", stops: ["alphabet", "phonics", "write", "scene-classroom"] },
    { id: "num", title: "Rainbow Island", zh: "数字彩虹岛", stops: ["numbers", "howmany", "shapes", "colors"] },
    { id: "town", title: "My Town", zh: "我的小镇", stops: ["feelings", "body", "actions", "family", "clothes", "room", "scene-kitchen"] },
    { id: "nature", title: "Nature Island", zh: "自然岛", stops: ["animals", "bugs", "fruits", "vegetables", "weather", "scene-sunny", "scene-farm", "scene-park"] },
    { id: "city", title: "City Island", zh: "城市岛", stops: ["vehicles", "jobs", "food", "where", "scene-market"] },
    { id: "beach", title: "Beach Island", zh: "海滩岛", stops: ["scene-beach", "sea", "toys"] },
  ];
  const PENCIL =
    '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16v4ZM13.5 6.5l4 4"/></svg>';

  // 0 to 3 stars for a stop: how much of the best game scores (for Write: of the 52 letters) is done.
  // The picture dictionary has no score, so it gets none (null).
  function stopStars(id) {
    const l = lessonById(id);
    let done;
    if (l) {
      const keys = [mainGame(l).key];
      if (spellable(l).length >= 3) keys.push("spell-" + l.id);
      if (buildable(l).length >= 3) keys.push("build-" + l.id);
      // Moves (act) can't go wrong, so they'd hand out free stars.
      if (l.pipSays && l.pipSays.type !== "act") keys.push("do-" + l.id);
      done = keys.reduce((sum, k) => sum + bestScore(k), 0) / (keys.length * ROUNDS);
    } else if (id === "write") done = written.size / 52;
    else return null;
    return done >= 0.9 ? 3 : done >= 0.5 ? 2 : done > 0 ? 1 : 0;
  }

  // What a stop shows, and the card that opens when it's tapped.
  function stopInfo(id) {
    const game = (href, label, best) =>
      `<a class="game" href="${href}" aria-label="${label} game, best score ${best} of ${ROUNDS} stars"><span>${label}</span>${stars(best)}</a>`;
    const l = lessonById(id);
    if (l) {
      const g = mainGame(l);
      const n = saidCount(l);
      return {
        title: l.title,
        art: cover(l),
        theme: theme(l),
        card: `
      <article class="tile" style="${theme(l)}">
        <span class="tile-badge${n ? "" : " zero"}"><span class="sr-only">Said</span>${MIC}${n}/${l.items.length}</span>
        <a class="tile-art" href="#/learn/${l.id}" tabindex="-1" aria-hidden="true">${cover(l)}</a>
        <h3>${l.title}</h3>
        <p>${l.subtitle}</p>
        <a class="btn primary learn" href="#/learn/${l.id}">Learn</a>
        <div class="games">
          ${game(`#/${g.view}/${l.id}`, g.label, bestScore(g.key))}
          ${spellable(l).length >= 3 ? game(`#/spell/${l.id}`, "Spell", bestScore("spell-" + l.id)) : ""}
          ${buildable(l).length >= 3 ? game(`#/build/${l.id}`, "Build", bestScore("build-" + l.id)) : ""}
          ${l.pipSays ? game(`#/do/${l.id}`, "Pip says", bestScore("do-" + l.id)) : ""}
        </div>
      </article>`,
      };
    }
    if (id === "write") {
      const t = theme({ color: "#7550d2", tint: "#efe8ff" });
      return {
        title: "Write",
        art: `<span class="write-cover">Aa</span>`,
        theme: t,
        card: `
      <article class="tile" style="${t}">
        <span class="tile-badge${written.size ? "" : " zero"}"><span class="sr-only">Written</span>${PENCIL}${written.size}/52</span>
        <a class="tile-art write-cover" href="#/write/0" tabindex="-1" aria-hidden="true">Aa</a>
        <h3>Write</h3>
        <p>Trace the letters A to Z</p>
        <a class="btn primary learn" href="#/write/0">Write</a>
      </article>`,
      };
    }
    const s = id.startsWith("scene-") && sceneById(id.slice(6));
    if (s)
      return {
        title: s.title,
        art: ART[s.icon],
        theme: theme(s),
        card: `
      <article class="tile" style="${theme(s)}">
        <a class="tile-art scene-thumb" href="#/scene/${s.id}" tabindex="-1" aria-hidden="true">${ART[s.art]}</a>
        <h3>${s.title}</h3>
        <p>${s.subtitle}</p>
        <a class="btn primary learn" href="#/scene/${s.id}">Explore</a>
      </article>`,
      };
    return null;
  }

  // The islands with their stops; anything nobody listed joins the last island.
  const ISLES = (() => {
    const all = [...window.LESSONS.map((l) => l.id), "write", ...window.SCENES.map((s) => "scene-" + s.id)];
    const listed = new Set(ISLANDS.flatMap((i) => i.stops));
    const extra = all.filter((id) => !listed.has(id));
    return ISLANDS.map((isle, k) => ({
      ...isle,
      stops: [...isle.stops, ...(k === ISLANDS.length - 1 ? extra : [])].filter((id) => all.includes(id)),
    }));
  })();
  const isleOf = (stopId) => ISLES.find((i) => i.stops.includes(stopId));
  const backToIsle = (stopId) => {
    const isle = isleOf(stopId);
    return isle ? `<nav class="crumbs"><a href="#/island/${isle.id}">← ${isle.title}</a></nav>` : `<nav class="crumbs"><a href="#/">← World map</a></nav>`;
  };
  // Stars on an island: the stops' stars added up (picture dictionaries have none).
  function isleStars(isle) {
    const scored = isle.stops.map(stopStars).filter((n) => n !== null);
    return { got: scored.reduce((a, b) => a + b, 0), total: scored.length * 3 };
  }
  const starsText = (isle) => {
    const { got, total } = isleStars(isle);
    return total ? `★ ${got}/${total}` : "★ Explore";
  };

  // Islands a child has sailed to. The FAR ones (drawn on the horizon) come closer once visited,
  // or once any of their lessons has been played.
  const seen = new Set(JSON.parse(localStorage.getItem("le-isles") || "[]"));
  const markSeen = (id) => {
    seen.add(id);
    localStorage.setItem("le-isles", JSON.stringify([...seen]));
  };
  const FAR = Object.keys(window.WORLD.wide.farDocks).map(Number);
  const isNear = (k) => !FAR.includes(k) || seen.has(ISLES[k].id) || ISLES[k].stops.some((id) => stopStars(id) > 0);

  // Moving things along: fn(t) with t from 0 to 1, eased; at once when the system asks for less motion.
  const reduceMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2);
  function tween(ms, step, done) {
    if (reduceMotion()) {
      step(1);
      if (done) done();
      return;
    }
    const t0 = performance.now();
    const frame = (now) => {
      const t = Math.min(1, (now - t0) / ms);
      step(ease(t));
      if (t < 1) requestAnimationFrame(frame);
      else if (done) done();
    };
    requestAnimationFrame(frame);
  }

  // The card for a stop, in a dialog over the page.
  function openCard(dlg, st) {
    if (!dlg.isConnected) return;
    dlg.setAttribute("aria-label", st.title);
    dlg.innerHTML = `<button class="level-close" aria-label="Close">✕</button>${st.card}`;
    dlg.querySelector(".level-close").addEventListener("click", () => dlg.close());
    dlg.showModal();
    Speech.say(st.title.replace("…", ""));
  }
  function dialogHtml() {
    return `<dialog class="level"></dialog>`;
  }
  function wireDialog() {
    const dlg = app.querySelector(".level");
    // A tap on the dimmed page around the card closes it.
    dlg.addEventListener("click", (e) => {
      if (e.target === dlg) dlg.close();
    });
    return dlg;
  }

  // ---------- home: the world map ----------
  let arriving = false; // true while Pip sails into an island, so the island page plays its welcome
  function world() {
    const next = ISLES.findIndex((isle) => isle.stops.some((id) => stopStars(id) === 0));
    // Pip's boat waits where it last moored, or at the island with the next thing to play.
    let at = Number(localStorage.getItem("le-boat"));
    if (!(at >= 0 && at < ISLES.length && isNear(at))) at = next >= 0 && isNear(next) ? next : 0;

    const plate = (isle, k, L) => `
        <button class="isle-label" data-i="${k}" style="left:${L.labels[k][0]}%;top:${L.labels[k][1]}%"${isNear(k) ? "" : " hidden"}>
          <b>${isle.title}</b>${zhLine(isle.zh, "zh-sub")}<span class="isle-stars">${starsText(isle)}</span>
        </button>`;
    const farPlate = (k, L) => `
        <button class="isle-label far-label" data-i="${k}" style="left:${L.farLabels[k][0]}%;top:${L.farLabels[k][1]}%"${isNear(k) ? " hidden" : ""}>
          <b>${ISLES[k].title}</b>${zhLine(ISLES[k].zh, "zh-sub")}<span class="isle-new">New!</span>
        </button>`;
    const layer = (name) => {
      const L = window.WORLD[name];
      return `<div class="world world-${name}" data-layout="${name}">${ART["_world-" + name]}
        ${ISLES.map((isle, k) => plate(isle, k, L)).join("")}${FAR.map((k) => farPlate(k, L)).join("")}</div>`;
    };
    app.innerHTML = `
      <section class="map-hero">
        <span class="hero-pip" aria-hidden="true">${next >= 0 ? ART._pip : ART._pip_cheer}</span>
        <div class="hero-bubble">
          <h1>Let's learn English!</h1>
          <p>Hi, I'm Pip! Which island shall we visit?</p>
          ${zhLine("你好，我是 Pip！今天去哪个岛？", "zh-sub")}
        </div>
      </section>
      ${layer("wide")}${layer("tall")}`;

    const worlds = [...app.querySelectorAll(".world")];
    const moor = (w, [x, y]) => {
      w._pos = [x, y];
      w.querySelector(".boat").setAttribute("transform", `translate(${x} ${y})`);
    };
    // Far islands nobody has been to stand on the horizon; the route only joins islands that are near.
    const showRoutes = (w) =>
      w.querySelectorAll(".seg").forEach((sg) => sg.classList.toggle("far-seg", !(isNear(+sg.dataset.a) && isNear(+sg.dataset.b))));
    worlds.forEach((w) => {
      FAR.forEach((k) => {
        w.querySelector(`.isle-g[data-i="${k}"]`).classList.toggle("far-hidden", !isNear(k));
        w.querySelector(`.far[data-i="${k}"]`).classList.toggle("gone", isNear(k));
      });
      showRoutes(w);
      moor(w, window.WORLD[w.dataset.layout].docks[at]);
    });

    function sailTo(w, [x1, y1], done) {
      const boat = w.querySelector(".boat");
      const [x0, y0] = w._pos;
      w._pos = [x1, y1];
      const dist = Math.hypot(x1 - x0, y1 - y0);
      if (dist < 1) return done();
      // a gentle curve, not a straight line
      const mx = (x0 + x1) / 2 + (y1 - y0) * 0.25;
      const my = (y0 + y1) / 2 - (x1 - x0) * 0.25;
      boat.querySelector(".boat-flip").classList.toggle("left", x1 < x0);
      boat.classList.add("sailing");
      tween(
        Math.min(2400, Math.max(800, dist * 3)),
        (t) => {
          const x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1;
          const y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1;
          boat.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        },
        () => {
          boat.classList.remove("sailing");
          done();
        }
      );
    }
    // A far island comes closer: its silhouette fades, and the island glides into its place on the map.
    function reveal(k) {
      markSeen(ISLES[k].id);
      worlds.forEach((w) => {
        w.querySelector(`.far[data-i="${k}"]`).classList.add("gone");
        w.querySelector(`.far-label[data-i="${k}"]`).hidden = true;
        const g = w.querySelector(`.isle-g[data-i="${k}"]`);
        g.classList.add("revealing");
        g.classList.remove("far-hidden");
        setTimeout(() => g.classList.remove("revealing"), 1400);
        setTimeout(() => {
          const plate = w.querySelector(`.isle-label[data-i="${k}"]:not(.far-label)`);
          plate.hidden = false;
          plate.querySelector(".isle-stars").classList.add("fresh");
        }, reduceMotion() ? 0 : 900);
        showRoutes(w);
      });
    }
    // Into an island: the map zooms towards it, then the island's page opens.
    function enter(w, k) {
      localStorage.setItem("le-boat", k);
      markSeen(ISLES[k].id);
      const L = window.WORLD[w.dataset.layout];
      w.style.transformOrigin = `${(L.pos[k][0] / L.W) * 100}% ${(L.pos[k][1] / L.H) * 100}%`;
      w.classList.add("zoom");
      setTimeout(() => {
        arriving = true;
        location.hash = "#/island/" + ISLES[k].id;
      }, reduceMotion() ? 0 : 750);
    }
    let busy = false;
    function go(k) {
      if (busy) return;
      busy = true;
      const w = worlds.find((x) => x.offsetParent);
      const L = window.WORLD[w.dataset.layout];
      const done = () => setTimeout(() => enter(w, k), 250);
      if (isNear(k)) return sailTo(w, L.docks[k], done);
      // out to the horizon first; the island comes closer, and the boat follows it in
      sailTo(w, L.farDocks[k], () => {
        reveal(k);
        setTimeout(() => sailTo(w, L.docks[k], done), reduceMotion() ? 0 : 1100);
      });
    }
    worlds.forEach((w) =>
      w.querySelectorAll(".isle-g, .isle-label, .far").forEach((el) => el.addEventListener("click", () => go(+el.dataset.i)))
    );
  }

  // ---------- inside an island ----------
  function island(isle, welcome) {
    const map = window.WORLD.isles[isle.id];
    const onRoad = isle.stops.slice(0, map.stops.length);
    const below = isle.stops.slice(map.stops.length);
    // The next stop: the first one without stars. An island of picture dictionaries only (no stars at all) starts at its first stop.
    const scored = isle.stops.filter((id) => stopStars(id) !== null);
    const nextId = scored.length ? isle.stops.find((id) => stopStars(id) === 0) : isle.stops[0];
    const stopHtml = (id, i, pos) => {
      const st = stopInfo(id);
      const n = stopStars(id);
      const label = n === null ? st.title : `${st.title}, ${n} of 3 stars`;
      const place = pos ? ` style="left:${(pos[0] / map.W) * 100}%;top:${(pos[1] / map.H) * 100}%"` : "";
      return `
        <div class="stop-abs${id === nextId ? " is-next" : ""}"${place}>
          <button class="node${n === 3 ? " done" : ""}${id === nextId ? " next" : ""}" style="${st.theme}" data-id="${id}" data-i="${i}" aria-haspopup="dialog" aria-label="${label}">
            <span class="node-art">${st.art}</span>
          </button>
          <span class="node-label" aria-hidden="true">${st.title}${
            n === null ? "" : `<span class="lbl-stars">${"★".repeat(n)}<span class="dim">${"★".repeat(3 - n)}</span></span>`
          }</span>
        </div>`;
    };
    app.innerHTML = `
      <div class="isle-head">
        <nav class="crumbs"><a href="#/">← World map</a></nav>
        <h1 class="sign"><span>${isle.title}</span>${zhLine(isle.zh, "zh-sub")}</h1>
        <span class="isle-badge">${starsText(isle).replace("★", '<span class="star">★</span>')}</span>
      </div>
      <div class="isle${welcome ? " arrive" : ""}">
        ${ART["_isle-" + isle.id]}
        ${onRoad.map((id, i) => stopHtml(id, i, map.stops[i])).join("")}
        <span class="walker" aria-hidden="true"><span class="bubble-sm">${nextId ? "Let's go!" : "Well done!"}</span><span class="pip-body">${
          nextId ? ART._pip : ART._pip_cheer
        }</span></span>
      </div>
      ${below.length ? `<section class="isle-more"><h2>More on this island</h2><div class="stops">${below.map((id) => stopHtml(id, -1)).join("")}</div></section>` : ""}
      ${dialogHtml()}`;
    const dlg = wireDialog();

    // Pip walks along the road. Each stop's place on the road is where the road passes closest to it.
    const road = app.querySelector(".isle-art .road-line");
    const total = road.getTotalLength();
    const stopLen = map.stops.slice(0, onRoad.length).map(([x, y]) => {
      let best = 0;
      let bestD = Infinity;
      for (let l = 0; l <= total; l += 4) {
        const p = road.getPointAtLength(l);
        const d = (p.x - x) ** 2 + (p.y - y) ** 2;
        if (d < bestD) [bestD, best] = [d, l];
      }
      return best;
    });
    const walker = app.querySelector(".walker");
    let pipLen = 0;
    const placeAt = (l) => {
      pipLen = Math.max(0, Math.min(total, l));
      const p = road.getPointAtLength(pipLen);
      walker.style.left = (p.x / map.W) * 100 + "%";
      walker.style.top = (p.y / map.H) * 100 + "%";
    };
    // Pip stands on the road just before a stop, with his "Let's go!" bubble at his upper right (or left). Where exactly
    // is measured on the page, since the circles and name plates keep a minimum size on small screens: going back
    // along the road from the stop, the place where Pip and the bubble cover the least of any stop.
    const stopEls = [...app.querySelectorAll(".stop-abs > *")];
    const bubble = walker.querySelector(".bubble-sm");
    const pipSvg = walker.querySelector(".pip-body svg");
    const overlap = (l, left) => {
      placeAt(l);
      walker.classList.toggle("bubble-left", left);
      const w = walker.getBoundingClientRect();
      // offsets ignore the bubble's pop-in transform, so this is where it ends up
      const bl = w.left + bubble.offsetLeft, bt = w.top + bubble.offsetTop;
      const boxes = [{ left: bl, top: bt, right: bl + bubble.offsetWidth, bottom: bt + bubble.offsetHeight }, pipSvg.getBoundingClientRect()];
      let area = 0;
      for (const el of stopEls) {
        const r = el.getBoundingClientRect();
        // a circle's box is empty at the corners: only count the middle of it
        const k = el.classList.contains("node") ? r.width * 0.15 : 0;
        for (const q of boxes) {
          const ox = Math.min(q.right, r.right - k) - Math.max(q.left, r.left + k);
          const oy = Math.min(q.bottom, r.bottom - k) - Math.max(q.top, r.top + k);
          if (ox > 0 && oy > 0) area += ox * oy;
        }
      }
      return area;
    };
    const spots = [];
    const standAt = (i) => {
      if (!spots[i]) {
        const [keepLen, keepLeft] = [pipLen, walker.classList.contains("bubble-left")];
        let best = { l: Math.max(0, stopLen[i] - 90), left: false, area: Infinity };
        // (nothing to measure while the page isn't laid out)
        if (app.querySelector(".isle-art").getBoundingClientRect().width) {
          for (let back = 60; back <= 360 && best.area > 0; back += 10) {
            const l = Math.max(0, stopLen[i] - back);
            for (const left of [false, true]) {
              const area = overlap(l, left);
              if (area < best.area) best = { l, left, area };
              if (!area) break;
            }
            if (!l) break;
          }
        }
        placeAt(keepLen);
        walker.classList.toggle("bubble-left", keepLeft);
        spots[i] = best;
      }
      return spots[i].l;
    };
    const sideBubble = (i) => walker.classList.toggle("bubble-left", standAt(i) >= 0 && spots[i].left);
    let walking = false;
    function walkTo(i, done) {
      if (walking) return;
      const from = pipLen;
      const target = standAt(i);
      walking = true;
      walker.classList.remove("arrived");
      walker.classList.add("walking");
      tween(
        Math.min(3200, Math.max(400, Math.abs(target - from) * 3.2)),
        (t) => {
          const l = from + (target - from) * t;
          const a = road.getPointAtLength(l);
          const b = road.getPointAtLength(Math.min(total, l + 2));
          walker.classList.toggle("flip", (b.x - a.x) * Math.sign(target - from || 1) < 0);
          placeAt(l);
        },
        () => {
          walking = false;
          walker.classList.remove("walking", "flip");
          sideBubble(i);
          walker.classList.add("arrived");
          if (done) done();
        }
      );
    }
    const goal = nextId ? onRoad.indexOf(nextId) : onRoad.length - 1;
    if (welcome && goal >= 0) {
      // straight off the boat: Pip walks from the dock to the next stop
      Speech.say(`Welcome to ${isle.title}!`);
      placeAt(0);
      setTimeout(() => walkTo(goal), reduceMotion() ? 0 : 700);
    } else if (goal >= 0) {
      placeAt(standAt(goal));
      sideBubble(goal);
      walker.classList.add("arrived");
    }

    app.querySelectorAll(".node").forEach((b) =>
      b.addEventListener("click", () => {
        const st = stopInfo(b.dataset.id);
        const i = Number(b.dataset.i);
        if (i < 0 || walking) return openCard(dlg, st);
        bounce(b);
        if (Math.abs(standAt(i) - pipLen) < 2) return openCard(dlg, st);
        walkTo(i, () => openCard(dlg, st));
      })
    );
  }

  // ---------- learn (cards) ----------
  function learn(lesson) {
    const sayLabel = Speech.canListen || Speech.canRecord ? "Say it" : "";
    const cardHtml = (it, i) => `
      <div class="card ${said.has(lesson.id + ":" + it.word) ? "said" : ""}" style="${theme(lesson)}" data-i="${i}">
        <span class="said-badge" title="You said it!" aria-hidden="true">★</span>
        <button class="card-main" aria-label="Hear ${it.word}">
          ${it.letter ? `<span class="letter">${it.letter}</span>` : ""}
          <span class="card-art">${pic(it)}</span>
          <span class="word" ${it.text ? `style="color:${it.text}"` : ""}>${wordLetters(it)}</span>
          ${zhLine(it.zh)}
          ${lesson.showSentence ? `<span class="card-sentence">${it.sentence}${zhLine(it.sentenceZh, "zh-sub")}</span>` : ""}
        </button>
        <div class="card-actions">
          <button class="mini spell">${it.family ? "Sound it" : "Spell it"}</button>
          ${sayLabel ? `<button class="mini say">${MIC}<span>${sayLabel}</span></button>` : ""}
          ${it.letter ? `<a class="mini" href="#/write/${i}">Write</a>` : ""}
        </div>
        <p class="say-msg" aria-live="polite"></p>
      </div>`;
    const cards = lesson.families
      ? lesson.families
          .map(
            (f) =>
              `<button class="family-head" style="${theme(lesson)}" data-rime="${f.rime}" aria-label="Hear the ${f.rime} family">-${f.rime}</button>` +
              lesson.items.map((it, i) => (it.family === f.rime ? cardHtml(it, i) : "")).join("")
          )
          .join("")
      : lesson.items.map(cardHtml).join("");
    const spellBtn = spellable(lesson).length >= 3 ? `<a class="btn primary" href="#/spell/${lesson.id}">Spell game</a>` : "";
    const buildBtn = buildable(lesson).length >= 3 ? `<a class="btn primary" href="#/build/${lesson.id}">Build a sentence</a>` : "";
    const doBtn = lesson.pipSays ? `<a class="btn primary" href="#/do/${lesson.id}">Pip says</a>` : "";
    const g = mainGame(lesson);
    const tip = lesson.tip ? `<p class="tip">${lesson.tip}${zhLine(lesson.tipZh, "zh-sub")}</p>` : "";
    app.innerHTML = `
      ${backToIsle(lesson.id)}
      <section class="lesson-head" style="${theme(lesson)}">
        <div class="head-main">
          <span class="head-pip" aria-hidden="true">${ART._pip}</span>
          <div><h1>${lesson.title}</h1><p>Tap a card to hear it. Tap “Say it” and say the word.</p>${tip}</div>
        </div>
        <div class="tile-actions"><a class="btn primary" href="#/${g.view}/${lesson.id}">${g.label} game</a>${spellBtn}${buildBtn}${doBtn}</div>
      </section>
      <div class="cards">${cards}</div>`;

    app.querySelectorAll(".card").forEach((card) => {
      const it = lesson.items[card.dataset.i];
      const main = card.querySelector(".card-main");
      main.addEventListener("click", () => {
        bounce(main);
        if (it.move) bounce(main.querySelector(".card-art"), "move-" + it.move);
        Speech.say([it.word, it.sentence], { gap: 350 });
      });
      card.querySelector(".spell").addEventListener("click", () => (it.family ? soundOut(card, it, lesson) : spellOut(card, it)));
      const sayBtn = card.querySelector(".say");
      if (sayBtn) sayBtn.addEventListener("click", () => sayIt(card, sayBtn, it, lesson));
    });
    // Tapping a family heading chants the family: "at: cat, hat, bat, mat".
    app.querySelectorAll(".family-head").forEach((h) =>
      h.addEventListener("click", () => {
        bounce(h);
        const rime = h.dataset.rime;
        Speech.say([rimeSound(lesson, rime), ...lesson.items.filter((it) => it.family === rime).map((it) => it.word)], { gap: 300 });
      })
    );
  }

  // One span per letter (for "Spell it"). In "two apples" the plural ending is marked so it can be highlighted,
  // and in phonics words the first sound ("b" in "bat").
  function wordLetters(it) {
    const at = it.count > 1 ? it.word.lastIndexOf(it.thing) : -1;
    const ending = at >= 0 ? at + it.thing.length : it.word.length;
    const onset = it.family ? onsetOf(it).length : 0;
    return it.word
      .split("")
      .map((c, k) =>
        /[a-z]/i.test(c)
          ? `<span class="l${k >= ending ? " plural" : ""}${k < onset ? " onset" : ""}">${c}</span>`
          : c === " "
          ? "&nbsp;"
          : c
      )
      .join("");
  }

  // "Sound it": the first sound, then the family ending, then the whole word (buh… at… bat).
  function soundOut(card, it, lesson) {
    const letters = [...card.querySelectorAll(".word .l")];
    const n = onsetOf(it).length;
    const show = (from, to) => letters.forEach((s, k) => s.classList.toggle("on", k >= from && k < to));
    Speech.say([onsetSound(onsetOf(it)), rimeSound(lesson, it.family), it.word], {
      gap: 350,
      onPart: (k) => (k === 0 ? show(0, n) : k === 1 ? show(n, letters.length) : show(0, letters.length)),
    }).then(() => setTimeout(() => show(0, 0), 400));
  }

  function spellOut(card, it) {
    const letters = [...card.querySelectorAll(".word .l")];
    const clear = () => letters.forEach((s) => s.classList.remove("on"));
    Speech.say([...letters.map((s) => s.textContent), it.word], {
      gap: 180,
      onPart: (k) => {
        clear();
        if (k < letters.length) letters[k].classList.add("on");
        else letters.forEach((s) => s.classList.add("on"));
      },
    }).then(() => setTimeout(clear, 400));
  }

  // ---------- say it (speaking practice) ----------
  let busy = false;
  async function sayIt(card, btn, it, lesson) {
    if (busy) return;
    busy = true;
    const msg = card.querySelector(".say-msg");
    const label = btn.querySelector("span");
    const setState = (state, text) => {
      btn.classList.toggle("listening", state === "listening");
      label.textContent = state === "listening" ? "Listening…" : "Say it";
      msg.className = "say-msg " + (state === "good" ? "good" : state === "retry" ? "retry" : "");
      msg.innerHTML = text || "";
    };
    try {
      if (Speech.canListen) {
        await Speech.say(it.word);
        setState("listening", "Now you say it!" + zhLine("现在你来说！", "zh-sub"));
        const r = await Speech.listen();
        if (r.heard && Speech.matches(r.heard, it)) {
          setState("good", "★ " + praise());
          card.classList.add("said");
          bounce(card, "pop");
          celebrate(card.querySelector(".card-art"), 18);
          markSaid(lesson.id, it.word);
          await Speech.say([praise(), it.word], { gap: 200 });
        } else if (r.heard) {
          setState("retry", `I heard “${esc(r.heard[0])}”. Try again!` + zhLine("再试一次！", "zh-sub"));
          await Speech.say(["Try again.", it.word], { gap: 250 });
        } else if (r.error === "not-allowed" || r.error === "service-not-allowed") {
          setState("retry", "Please allow the microphone." + zhLine("请允许使用麦克风。", "zh-sub"));
        } else if (r.error === "network") {
          setState("retry", "Speech check needs the internet." + zhLine("跟读检查需要联网。", "zh-sub"));
        } else {
          setState("retry", "I didn't hear you. Try again!" + zhLine("没听到，再试一次！", "zh-sub"));
        }
      } else {
        // No recognition (e.g. Safari/Firefox): record, then compare by ear.
        await Speech.say(it.word);
        setState("listening", "Now you say it!");
        const url = await Speech.record(2500);
        setState("", "Listen: first the teacher, then you.");
        await Speech.say(it.word);
        await new Promise((res) => {
          const a = new Audio(url);
          a.onended = a.onerror = res;
          a.play().catch(res);
        });
        setState("", "Do they sound the same?" + zhLine("听起来一样吗？", "zh-sub"));
      }
    } catch (err) {
      setState("retry", "Please allow the microphone." + zhLine("请允许使用麦克风。", "zh-sub"));
    } finally {
      busy = false;
    }
  }

  // ---------- scene ----------
  function scene(s) {
    app.innerHTML = `
      ${backToIsle("scene-" + s.id)}
      <section class="lesson-head" style="${theme(s)}">
        <div><h1>${s.title}</h1><p>${s.subtitle}.</p></div>
      </section>
      <div class="scene">${ART[s.art]}</div>
      <p class="caption" aria-live="polite">&nbsp;</p>`;
    const caption = app.querySelector(".caption");
    const activate = (tag) => {
      app.querySelectorAll(".tag.on").forEach((t) => t.classList.remove("on"));
      tag.classList.add("on");
      const w = tag.dataset.word;
      caption.innerHTML = s.sentences[w] + zhLine(s.sentencesZh[w], "zh caption-zh");
      Speech.say([w, s.sentences[w]], { gap: 350 });
    };
    app.querySelectorAll(".tag").forEach((tag) => {
      tag.addEventListener("click", () => activate(tag));
      tag.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate(tag);
        }
      });
    });
  }

  // ---------- shared results screen ----------
  function results(box, { score, total, key, lesson, again, note }) {
    localStorage.setItem("le-best-" + key, String(Math.max(score, bestScore(key))));
    const msg = score === total ? "Perfect!" : score >= 3 ? "Great work!" : "Good try!";
    // Stars pop in one at a time, the earned ones first.
    const bigStars = Array.from({ length: total }, (_, k) => `<i class="${k < score ? "" : "dim"}" style="--i:${k}">★</i>`).join("");
    app.querySelector(".buddy")?.remove();
    box.innerHTML = `
      <div class="done">
        <span class="done-pip" aria-hidden="true">${score >= 3 ? ART._pip_cheer : ART._pip}</span>
        <h1>${msg}</h1>
        <p class="big-stars"><span class="stars" aria-label="${score} of ${total} stars">${bigStars}</span></p>
        <p>${note}</p>
        <div class="tile-actions">
          <a class="btn" href="#/learn/${lesson.id}">Learn again</a>
          <button class="btn primary again">Play again</button>
        </div>
      </div>`;
    box.querySelector(".again").addEventListener("click", again);
    if (score) celebrate(box.querySelector(".big-stars"), 20 + score * 8);
    Speech.say(msg);
  }

  // ---------- listen game ----------
  function play(lesson) {
    const rounds = shuffle(lesson.items).slice(0, ROUNDS);
    const nOptions = lesson.items.length >= 6 ? 4 : 3;
    let round = 0;
    let score = 0;
    let firstTry = true;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <button class="btn primary listen">▶ Listen again</button>
        <div class="options"></div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const prompt = () =>
      lesson.askSentence ? Speech.say(rounds[round].sentence) : Speech.say(["Tap", rounds[round].word], { gap: 60 });
    $(".listen").addEventListener("click", prompt);

    function showRound() {
      const target = rounds[round];
      const others = shuffle(lesson.items.filter((x) => x !== target)).slice(0, nOptions - 1);
      const opts = shuffle([target, ...others]);
      firstTry = true;
      locked = false;
      $(".progress").innerHTML = progress("Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".options").innerHTML = opts
        .map((o) => `<button class="option" data-word="${o.word}" aria-label="${o.word}">${pic(o)}</button>`)
        .join("");
      $(".options").querySelectorAll(".option").forEach((b) => b.addEventListener("click", () => choose(b)));
      prompt();
    }

    function choose(btn) {
      if (locked) return;
      const target = rounds[round];
      if (btn.dataset.word === target.word) {
        locked = true;
        if (firstTry) score++;
        btn.classList.add("right");
        btn.insertAdjacentHTML("beforeend", `<span class="option-word">${target.word}${zhLine(target.zh)}</span>`);
        celebrate(btn);
        $(".score").innerHTML = stars(score, rounds.length);
        Speech.say([praise(), target.sentence], { gap: 250 }).then(() => {
          round++;
          round < rounds.length ? showRound() : finish();
        });
      } else {
        firstTry = false;
        bounce(btn, "wrong");
        if (lesson.askSentence) {
          const picked = lesson.items.find((x) => x.word === btn.dataset.word);
          Speech.say([picked.sentence, "Try again.", target.sentence], { gap: 250 });
        } else {
          Speech.say(["That is " + btn.dataset.word + ".", "Try again. Tap " + target.word + "."], { gap: 200 });
        }
      }
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: lesson.id,
        lesson,
        again: () => play(lesson),
        note: `You got ${score} of ${rounds.length} on the first try.`,
      });

    showRound();
  }

  // ---------- spell game ----------
  function spellGame(lesson) {
    const pool = spellable(lesson);
    const rounds = shuffle(pool).slice(0, Math.min(ROUNDS, pool.length));
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz spellgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="slots" aria-live="polite"></div>
        <div class="letter-tiles"></div>
        <div class="tile-actions">
          <button class="btn hear">▶ Hear the word</button>
          <button class="btn hint">Hint</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const letters = it.word.split("");
      const abc = "abcdefghijklmnopqrstuvwxyz".split("").filter((c) => !letters.includes(c));
      const tiles = shuffle([...letters, ...shuffle(abc).slice(0, 2)]);
      let pos = 0;
      let perfect = true;
      let locked = false;

      $(".progress").innerHTML = progress("Word", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".slots").innerHTML = letters.map(() => `<span class="slot"></span>`).join("");
      $(".letter-tiles").innerHTML = tiles
        .map((c) => `<button class="ltile" data-c="${c}" aria-label="letter ${c}">${c}</button>`)
        .join("");
      const slots = [...app.querySelectorAll(".slot")];
      slots[0].classList.add("next");

      app.querySelectorAll(".ltile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.disabled) return;
          if (t.dataset.c === letters[pos]) {
            t.disabled = true;
            t.classList.add("used");
            slots[pos].textContent = letters[pos];
            slots[pos].classList.remove("next");
            slots[pos].classList.add("filled");
            pos++;
            if (pos < letters.length) {
              slots[pos].classList.add("next");
              Speech.say(t.dataset.c, { rateScale: 1.1 });
            } else {
              locked = true;
              if (perfect) score++;
              $(".score").innerHTML = stars(score, rounds.length);
              bounce($(".slots"), "pop");
              celebrate($(".slots"));
              Speech.say([it.word, praise()], { gap: 250 }).then(() => {
                round++;
                round < rounds.length ? showRound() : finish();
              });
            }
          } else {
            perfect = false;
            bounce(t, "wrong");
            Speech.say(t.dataset.c);
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.word);
      $(".hint").onclick = () => {
        if (locked) return;
        perfect = false;
        const tile = [...app.querySelectorAll(".ltile:not(.used)")].find((x) => x.dataset.c === letters[pos]);
        if (tile) bounce(tile, "glow");
        Speech.say(letters[pos]);
      };
      Speech.say(["Spell", it.word], { gap: 80 });
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "spell-" + lesson.id,
        lesson,
        again: () => spellGame(lesson),
        note: `You spelled ${score} of ${rounds.length} with no mistakes.`,
      });

    showRound();
  }

  // ---------- build game (put the words of a sentence in order) ----------
  function buildGame(lesson) {
    const pool = buildable(lesson);
    const rounds = shuffle(pool).slice(0, Math.min(ROUNDS, pool.length));
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz buildgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="wslots" aria-live="polite"></div>
        <div class="word-tiles"></div>
        <div class="tile-actions">
          <button class="btn hear">▶ Hear it</button>
          <button class="btn hint">Hint</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const { words, end } = sentenceTiles(it);
      // One extra tile, so the picture decides which word fits: another card's word,
      // or for counting items the other form of the noun ("car" next to "cars").
      const lower = words.map((w) => w.toLowerCase());
      const other = shuffle(lesson.items).find((x) => x !== it && !lower.includes(x.word.toLowerCase()));
      const plural = it.count && (window.COUNT_THINGS.find((t) => t.word === it.thing) || {}).plural;
      const extra = it.count ? (it.count === 1 ? plural : it.thing) : other && other.word;
      const tiles = shuffle(extra ? [...words, extra] : words);
      let pos = 0;
      let perfect = true;
      let locked = false;

      $(".progress").innerHTML = progress("Sentence", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".wslots").innerHTML = words.map(() => `<span class="wslot"></span>`).join("") + `<span class="wend">${end}</span>`;
      $(".word-tiles").innerHTML = tiles.map((w) => `<button class="wtile">${esc(w)}</button>`).join("");
      const slots = [...app.querySelectorAll(".wslot")];
      slots[0].classList.add("next");

      app.querySelectorAll(".wtile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.disabled) return;
          if (t.textContent === words[pos]) {
            t.disabled = true;
            t.classList.add("used");
            slots[pos].textContent = words[pos];
            slots[pos].classList.remove("next");
            slots[pos].classList.add("filled");
            pos++;
            if (pos < words.length) {
              slots[pos].classList.add("next");
              Speech.say(t.textContent);
            } else {
              locked = true;
              if (perfect) score++;
              $(".score").innerHTML = stars(score, rounds.length);
              bounce($(".wslots"), "pop");
              celebrate($(".wslots"));
              app.querySelectorAll(".wtile:not(.used)").forEach((x) => x.classList.add("leftover"));
              if (it.sentenceZh) $(".wslots").insertAdjacentHTML("beforeend", zhLine(it.sentenceZh, "zh-sub"));
              Speech.say([it.sentence, praise()], { gap: 300 }).then(() => {
                round++;
                round < rounds.length ? showRound() : finish();
              });
            }
          } else {
            perfect = false;
            bounce(t, "wrong");
            Speech.say(t.textContent);
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.sentence);
      $(".hint").onclick = () => {
        if (locked) return;
        perfect = false;
        const tile = [...app.querySelectorAll(".wtile:not(.used)")].find((x) => x.textContent === words[pos]);
        if (tile) bounce(tile, "glow");
        Speech.say(words[pos]);
      };
      Speech.say(it.sentence);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "build-" + lesson.id,
        lesson,
        again: () => buildGame(lesson),
        note: `You built ${score} of ${rounds.length} sentences with no mistakes.`,
      });

    showRound();
  }

  // ---------- blend game (phonics: pick the first sound) ----------
  function blendGame(lesson) {
    const rounds = shuffle(lesson.items).slice(0, ROUNDS);
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz blendgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="blend-word" aria-live="polite"></div>
        <p class="count-msg"></p>
        <div class="letter-tiles"></div>
        <button class="btn hear">▶ Hear it</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const rime = it.family;
      const family = lesson.items.filter((x) => x.family === rime);
      // Every choice makes a real word in the family, so a wrong pick is a rhyming word to hear.
      const choices = shuffle(family.map(onsetOf));
      let firstTry = true;
      let locked = false;

      $(".progress").innerHTML = progress("Word", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".blend-word").innerHTML = `<span class="slot bslot next"></span><span class="rime">${rime}</span>`;
      const msg = $(".count-msg");
      msg.className = "count-msg";
      msg.innerHTML = "What is the first sound?" + zhLine("第一个音是什么？", "zh-sub");
      $(".letter-tiles").innerHTML = choices
        .map((o) => `<button class="ltile otile" data-o="${o}" aria-label="${o}">${o}</button>`)
        .join("");
      const slot = $(".bslot");

      app.querySelectorAll(".otile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked) return;
          const o = t.dataset.o;
          const made = family.find((x) => onsetOf(x) === o);
          slot.textContent = o;
          if (made === it) {
            locked = true;
            if (firstTry) score++;
            slot.classList.remove("next", "wrongword");
            slot.classList.add("filled");
            t.classList.add("used");
            $(".score").innerHTML = stars(score, rounds.length);
            msg.className = "count-msg good";
            msg.innerHTML = `★ ${o}-${rime}, ${it.word}!`;
            bounce($(".blend-word"), "pop");
            celebrate($(".blend-word"));
            Speech.say([onsetSound(o), rimeSound(lesson, rime), it.word, praise()], { gap: 300 }).then(() => {
              round++;
              round < rounds.length ? showRound() : finish();
            });
          } else {
            firstTry = false;
            locked = true;
            slot.classList.add("wrongword");
            bounce(t, "wrong");
            msg.className = "count-msg retry";
            msg.innerHTML = `That says “${made.word}”. Find “${it.word}”!` + zhLine(`这是 ${made.word}，再找找 ${it.word}！`, "zh-sub");
            Speech.say(["That says " + made.word + ".", "Find " + it.word + "."], { gap: 250 }).then(() => {
              if (rounds[round] !== it) return;
              locked = false;
              slot.textContent = "";
              slot.classList.remove("wrongword");
            });
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.word);
      Speech.say(it.word);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "blend-" + lesson.id,
        lesson,
        again: () => blendGame(lesson),
        note: `You found ${score} of ${rounds.length} first sounds on the first try.`,
      });

    showRound();
  }

  // ---------- count game ----------
  function countGame(lesson) {
    const things = shuffle(window.COUNT_THINGS).slice(0, ROUNDS);
    const counts = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).slice(0, ROUNDS);
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz countgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="count-pic"></div>
        <p class="count-msg" aria-live="polite"></p>
        <div class="num-options"></div>
        <button class="btn listen">▶ Listen again</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const thing = things[round];
      const n = counts[round];
      const name = (k) => (k === 1 ? thing.word : thing.plural);
      const near = shuffle([n - 2, n - 1, n + 1, n + 2].filter((k) => k >= 1 && k <= 10));
      const opts = shuffle([n, ...near.slice(0, 2)]);
      let tapped = 0;
      let firstTry = true;
      let locked = false;
      const msg = $(".count-msg");
      const setMsg = (cls, html) => {
        msg.className = "count-msg " + cls;
        msg.innerHTML = html;
      };

      $(".progress").innerHTML = progress("Question", round, ROUNDS);
      $(".score").innerHTML = stars(score, ROUNDS);
      $(".count-pic").innerHTML = many(thing.word, n, 320, 150);
      setMsg("", `How many ${thing.plural}? Tap each one to count.` + zhLine("有几个？点一点，数一数。", "zh-sub"));
      $(".num-options").innerHTML = opts
        .map((k) => `<button class="num" data-n="${k}" aria-label="${NUMBERS[k - 1]}">${k}</button>`)
        .join("");

      // Tapping a picture counts it out loud and puts a number on it.
      const svg = $(".count-pic svg");
      const clearCount = () => {
        tapped = 0;
        svg.querySelectorAll(".count-badge").forEach((b) => b.remove());
        svg.querySelectorAll(".thing").forEach((t) => t.classList.remove("counted"));
      };
      svg.querySelectorAll(".thing").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.classList.contains("counted")) return;
          tapped++;
          t.classList.add("counted");
          const { x, y, r } = t.dataset;
          t.insertAdjacentHTML(
            "afterend",
            `<g class="count-badge"><circle cx="${x - r * 1.2}" cy="${+y + r * 1.2}" r="${r}"/>` +
              `<text x="${x - r * 1.2}" y="${+y + r * 1.2}" font-size="${r * 1.3}" text-anchor="middle" dominant-baseline="central">${tapped}</text></g>`
          );
          Speech.say(NUMBERS[tapped - 1], { rateScale: 1.1 });
        })
      );

      app.querySelectorAll(".num").forEach((b) =>
        b.addEventListener("click", () => {
          if (locked) return;
          const k = Number(b.dataset.n);
          if (k === n) {
            locked = true;
            if (firstTry) score++;
            b.classList.add("right");
            $(".score").innerHTML = stars(score, ROUNDS);
            const phrase = `${NUMBERS[n - 1]} ${name(n)}`;
            setMsg("good", `★ ${n} ${name(n)}` + zhLine(ZH_NUMBERS[n - 1] + thing.unit + thing.zh, "zh-sub"));
            bounce($(".count-pic"), "pop");
            celebrate(b);
            Speech.say([phrase[0].toUpperCase() + phrase.slice(1) + "!", praise()], { gap: 250 }).then(() => {
              round++;
              round < ROUNDS ? showRound() : finish();
            });
          } else {
            firstTry = false;
            bounce(b, "wrong");
            clearCount();
            setMsg("retry", "Let's count again! Tap each one." + zhLine("我们再数一遍！一个一个点。", "zh-sub"));
            Speech.say([NUMBERS[k - 1] + "?", "Let's count again."], { gap: 200 });
          }
        })
      );
      $(".listen").onclick = () => Speech.say(`How many ${thing.plural}?`);
      Speech.say(`How many ${thing.plural}?`);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: ROUNDS,
        key: "count-" + lesson.id,
        lesson,
        again: () => countGame(lesson),
        note: `You counted ${score} of ${ROUNDS} right on the first try.`,
      });

    showRound();
  }

  // ---------- Pip says ----------
  // Pip asks and the child does it on the picture: touches a part of Pip ("Touch Pip's nose.", type "tap"), drags
  // the cat somewhere ("Put the cat under the table.", type "drag") or colors a thing with a crayon ("Color the ball
  // blue.", type "paint"). The zones are drawn in tools/art/build17.py and build19.py. Doing the wrong thing reads
  // out what the child did ("The cat is on the table."); after two misses the right zone (and crayon) glows.
  // The cat can also be tapped, then tapped where it should go, for fingers that can't drag yet.
  // Type "act" is for the body: Pip says a move and does it (build20.py), the child does it too and taps "I did it!".
  const svgPoint = (svg, e) => new DOMPoint(e.clientX, e.clientY).matrixTransform(svg.getScreenCTM().inverse());

  function pipSays(lesson) {
    const game = lesson.pipSays;
    const colorZh = (c) => lesson.items.find((it) => it.word === c).zh;
    // Coloring: what the page says when `thing` is colored `c`, and the asks (each thing once, each color once).
    const painted = (thing, c) => ({ is: `The ${thing.zone} is ${c}.`, isZh: `${thing.zh}是${colorZh(c)}的。` });
    const colors = game.paint ? shuffle(Object.keys(game.paint)) : [];
    const rounds =
      game.type === "paint"
        ? shuffle(game.things)
            .slice(0, ROUNDS)
            .map((th, i) => ({
              zone: th.zone,
              color: colors[i],
              say: `Color the ${th.zone} ${colors[i]}.`,
              zh: `把${th.zh}涂成${colorZh(colors[i])}。`,
              ...painted(th, colors[i]),
            }))
        : shuffle(game.tasks).slice(0, ROUNDS);
    let round = 0;
    let score = 0;
    let misses = 0;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz pipsays pipsays-${game.type}" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <p class="do-ask" aria-live="polite"><span class="do-say"></span><span class="do-note"></span></p>
        <div class="do-pic">${ART[game.art]}</div>
        ${game.paint ? `<div class="crayons">${Object.keys(game.paint)
          .map((c) => `<button class="crayon" data-color="${c}" aria-label="${c}" aria-pressed="false">${ART[c]}</button>`)
          .join("")}</div>` : ""}
        ${game.type === "act" ? `<button class="btn primary did" disabled>I did it!</button>` : ""}
        <button class="btn listen">▶ Listen again</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const svg = $(".do-pic svg");
    // Pip acts out what was touched (blinks, wiggles his ears...), or giggles; one at a time.
    const react = (cls) => {
      svg.classList.remove(...[...svg.classList].filter((c) => c.startsWith("react-") || c === "tickle"));
      bounce(svg, cls);
    };
    const task = () => rounds[round];
    const taskFor = (zone) => game.tasks.find((t) => t.zone === zone);
    const note = (cls, text, zh) => {
      const el = $(".do-note");
      el.className = "do-note " + cls;
      el.innerHTML = text ? text + zhLine(zh, "zh-sub") : "";
    };
    $(".listen").addEventListener("click", () => Speech.say(task().say));
    let startRound = () => Speech.say(task().say);

    function showRound() {
      misses = 0;
      locked = false;
      app.querySelectorAll(".pipsays .hint").forEach((el) => el.classList.remove("hint"));
      $(".progress").innerHTML = progress(game.type === "act" ? "Move" : "Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".do-say").innerHTML = task().say + zhLine(task().zh, "zh-sub");
      note("", "");
      startRound();
    }

    // `ok`: the child did what Pip asked. `did` says what they did ({is, isZh}); `el` is where the confetti comes from.
    function answer(ok, did, el) {
      const t = task();
      if (ok) {
        locked = true;
        if (!misses) score++;
        $(".score").innerHTML = stars(score, rounds.length);
        note("good", "★ " + t.is, t.isZh);
        app.querySelectorAll(".pipsays .hint").forEach((z) => z.classList.remove("hint"));
        celebrate(el);
        if (game.type === "tap") react("react-" + t.zone);
        Speech.say([praise(), t.is], { gap: 250 }).then(() => {
          if (!svg.isConnected) return;
          round++;
          round < rounds.length ? showRound() : finish();
        });
      } else {
        misses++;
        note("retry", did.is + " Try again!", did.isZh + "再试一次！");
        if (misses >= 2)
          app.querySelectorAll(`.pipsays [data-zone="${t.zone}"], .crayon[data-color="${t.color}"]`).forEach((z) => z.classList.add("hint"));
        Speech.say([did.is, "Try again.", t.say], { gap: 250 });
      }
    }

    // ----- tap: touch a part of Pip -----
    if (game.type === "tap") {
      const spots = [...svg.querySelectorAll(".do-spot")];
      svg.addEventListener("click", (e) => {
        if (locked) return;
        const p = svgPoint(svg, e);
        // The nearest part, measured in part sizes, so the small nose is as easy to hit as a big ear.
        let hit = null;
        let best = 1.8;
        for (const s of spots) {
          const d = Math.hypot(p.x - s.getAttribute("cx"), p.y - s.getAttribute("cy")) / s.getAttribute("r");
          if (d < best) [hit, best] = [s, d];
        }
        if (!hit) {
          react("tickle");
          return Speech.say("Hee hee! That tickles!");
        }
        const zone = hit.dataset.zone;
        const ring = zone === task().zone ? "on" : "miss";
        const same = spots.filter((s) => s.dataset.zone === zone);
        same.forEach((s) => bounce(s, ring));
        setTimeout(() => same.forEach((s) => s.classList.remove(ring)), 1200);
        answer(zone === task().zone, taskFor(zone), hit);
      });
    }

    // ----- drag: move the cat around the room -----
    if (game.type === "drag") {
      const cat = svg.querySelector(".do-thing");
      const layer = svg.querySelector(".do-drag");
      const zones = [...svg.querySelectorAll(".do-zone")];
      const slotPos = (slot) => ({ x: +slot.dataset.x, y: +slot.dataset.y, s: +slot.dataset.s });
      let slot = cat.parentNode;
      let pos = slotPos(slot);
      const place = () => cat.setAttribute("transform", `translate(${pos.x.toFixed(1)} ${pos.y.toFixed(1)}) scale(${pos.s.toFixed(3)})`);
      const glide = (to, done) => {
        const from = { ...pos };
        tween(280, (t) => {
          pos = { x: from.x + (to.x - from.x) * t, y: from.y + (to.y - from.y) * t, s: from.s + (to.s - from.s) * t };
          place();
        }, done);
      };
      // The zone under a point, or the nearest one if the point is just outside.
      const inZone = (z, p, pad = 0) => {
        const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => +z.getAttribute(a));
        return p.x >= x - pad && p.x <= x + w + pad && p.y >= y - pad && p.y <= y + h + pad;
      };
      const zoneAt = (p) => zones.find((z) => inZone(z, p)) || zones.find((z) => inZone(z, p, 24));

      let drag = null; // {off, start, moved} while a finger is on the cat
      let carrying = false; // the cat was tapped and waits for a tap where it should go
      let busy = false; // the cat is gliding to its place
      const pickUp = () => {
        layer.appendChild(cat);
        cat.classList.add("lifted");
      };
      function drop(p) {
        carrying = false;
        cat.classList.remove("lifted", "carry");
        const z = zoneAt(p);
        busy = true;
        if (!z) {
          // dropped nowhere in particular: back where it was
          return glide(slotPos(slot), () => {
            slot.appendChild(cat);
            busy = false;
            Speech.say(task().say);
          });
        }
        const to = svg.querySelector(`.do-slot[data-slot="${z.dataset.slot}"]`);
        glide(slotPos(to), () => {
          to.appendChild(cat);
          slot = to;
          busy = false;
          answer(z.dataset.zone === task().zone, taskFor(z.dataset.zone), cat);
        });
      }

      svg.addEventListener("pointerdown", (e) => {
        if (locked || busy || e.button > 0) return;
        const p = svgPoint(svg, e);
        const onCat = e.target.closest(".do-thing");
        if (!onCat) {
          if (carrying) drop(p);
          return;
        }
        e.preventDefault();
        svg.setPointerCapture(e.pointerId);
        if (!carrying) pickUp();
        drag = { off: { x: pos.x - p.x, y: pos.y - p.y }, start: p, moved: false };
      });
      svg.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const p = svgPoint(svg, e);
        if (!drag.moved && Math.hypot(p.x - drag.start.x, p.y - drag.start.y) < 8) return;
        drag.moved = true;
        cat.classList.remove("carry");
        pos = { ...pos, x: p.x + drag.off.x, y: p.y + drag.off.y };
        place();
      });
      const release = () => {
        if (!drag) return;
        const { moved } = drag;
        drag = null;
        if (moved) return drop(pos);
        // a tap on the cat picks it up (or puts it back down)
        if (carrying) {
          carrying = false;
          cat.classList.remove("lifted", "carry");
          slot.appendChild(cat);
        } else {
          carrying = true;
          cat.classList.add("carry");
          Speech.say("Where does the cat go? Tap there.");
        }
      };
      svg.addEventListener("pointerup", release);
      svg.addEventListener("pointercancel", () => {
        if (!drag) return;
        drag = null;
        drop({ x: -999, y: -999 });
      });
    }

    // ----- paint: pick a crayon, then tap the thing to color -----
    if (game.type === "paint") {
      let crayon = null;
      app.querySelectorAll(".crayon").forEach((b) =>
        b.addEventListener("click", () => {
          app.querySelectorAll(".crayon").forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
          crayon = b.dataset.color;
          bounce(b);
          Speech.say(crayon);
        })
      );
      svg.querySelectorAll(".do-paint").forEach((g) =>
        g.addEventListener("click", () => {
          if (locked) return;
          if (!crayon) {
            bounce($(".crayons"));
            note("retry", "Pick a crayon first!", "先选一支蜡笔！");
            return Speech.say("Pick a crayon first.");
          }
          // Whatever the child does gets colored, right or not.
          g.querySelectorAll(".pf").forEach((el) => (el.style.fill = game.paint[crayon]));
          const thing = game.things.find((th) => th.zone === g.dataset.zone);
          answer(thing.zone === task().zone && crayon === task().color, painted(thing, crayon), g);
        })
      );
    }

    // ----- act: Pip says a move and does it; the child does it too -----
    if (game.type === "act") {
      const did = $(".did");
      startRound = () => {
        const t = task();
        svg.querySelectorAll(".act-prop").forEach((p) => (p.style.display = p.dataset.move === t.zone ? "" : "none"));
        svg.setAttribute("class", "act-" + t.zone);
        did.disabled = true;
        // Pip starts moving on "Go!" and keeps going until the child says they did it.
        Speech.say([t.say, "Ready? Go!"], { gap: 300 }).then(() => {
          if (!svg.isConnected || task() !== t || locked) return;
          svg.classList.add("moving");
          did.disabled = false;
        });
      };
      did.addEventListener("click", () => {
        if (locked) return;
        did.disabled = true;
        svg.classList.remove("moving");
        answer(true, task(), did);
      });
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "do-" + lesson.id,
        lesson,
        again: () => pipSays(lesson),
        note:
          game.type === "act"
            ? `You did ${score} moves with Pip!`
            : `You did ${score} of ${rounds.length} right on the first try.`,
      });

    showRound();
  }

  // ---------- write (letter tracing) ----------
  let activeWriter = null;
  function write(index) {
    const lesson = lessonById("alphabet");
    const it = lesson.items[index];
    const upper = it.letter[0];
    const lower = it.letter[1];
    const prev = (index + 25) % 26;
    const next = (index + 1) % 26;
    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/alphabet">← ABC</a></nav>
      <section class="write" style="${theme(lesson)}">
        <div class="write-head">
          <a class="btn round" href="#/write/${prev}" aria-label="Previous letter">‹</a>
          <div class="case-tabs" role="group" aria-label="Choose a letter">
            <button class="case" data-c="${upper}">${upper}<span class="case-star">★</span></button>
            <button class="case" data-c="${lower}">${lower}<span class="case-star">★</span></button>
          </div>
          <a class="btn round" href="#/write/${next}" aria-label="Next letter">›</a>
        </div>
        <div class="write-body">
          <div class="pad-wrap"><canvas class="pad" aria-label="Writing pad. Trace the letter with your finger or mouse."></canvas></div>
          <aside class="write-word">
            <span class="card-art">${pic(it)}</span>
            <span class="word">${it.word}</span>
            ${zhLine(it.zh)}
          </aside>
        </div>
        <p class="write-msg" aria-live="polite"></p>
        <div class="tile-actions">
          <button class="btn primary show">✎ Show me</button>
          <button class="btn hear">▶ Hear it</button>
          <button class="btn clear">Clear</button>
          <button class="btn primary check">Done</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const msg = $(".write-msg");
    const writer = (activeWriter = Writer.mount($(".pad"), { color: lesson.color }));
    let ch = upper;
    const cases = [...app.querySelectorAll(".case")];
    const refreshTabs = () =>
      cases.forEach((b) => {
        b.classList.toggle("on", b.dataset.c === ch);
        b.classList.toggle("done", written.has(b.dataset.c));
        b.setAttribute("aria-pressed", b.dataset.c === ch);
      });
    const choose = (c) => {
      ch = c;
      writer.setChar(c);
      refreshTabs();
      setTip();
    };
    const setTip = () => {
      msg.className = "write-msg";
      msg.innerHTML =
        "Start at the green dot 1. Follow the numbers." + zhLine("从绿色的 1 号点开始，按数字顺序描。", "zh-sub");
    };
    const showMe = () => {
      const n = writer.strokeCount();
      msg.className = "write-msg";
      msg.innerHTML = `Watch! ${letterName(ch)} has ${n} stroke${n > 1 ? "s" : ""}.` + zhLine(`看好了！这个字母有 ${n} 笔。`, "zh-sub");
      Speech.say(`Watch. ${letterName(ch)}.`);
      writer.playDemo().then((finished) => {
        if (!finished || activeWriter !== writer) return;
        msg.innerHTML = "Now you try!" + zhLine("现在轮到你了！", "zh-sub");
        Speech.say("Now you try!");
      });
    };
    const letterName = (c) => (c === upper ? "Big " + upper : "Small " + lower);
    cases.forEach((b) =>
      b.addEventListener("click", () => {
        choose(b.dataset.c);
        if (written.has(ch)) Speech.say(letterName(ch));
        else showMe();
      })
    );
    $(".show").addEventListener("click", showMe);
    $(".hear").addEventListener("click", () => Speech.say([letterName(ch), it.sentence], { gap: 300 }));
    $(".clear").addEventListener("click", () => writer.clear());
    $(".check").addEventListener("click", () => {
      const r = writer.check();
      if (r.empty) {
        msg.className = "write-msg retry";
        msg.innerHTML = "Draw on the letter first!" + zhLine("先在字母上描一描！", "zh-sub");
        return;
      }
      if (r.pass) {
        markWritten(ch);
        refreshTabs();
        msg.className = "write-msg good";
        msg.innerHTML = r.orderOk
          ? "★ " + praise() + zhLine("写得真好！", "zh-sub")
          : "★ Good! Next time, start at dot 1 and follow the numbers." +
            zhLine("写得不错！下次从 1 号点开始，按数字顺序写。", "zh-sub");
        bounce($(".pad-wrap"), "pop");
        celebrate($(".pad-wrap"));
        const other = ch === upper ? lower : upper;
        Speech.say([praise(), letterName(ch)], { gap: 250 }).then(() => {
          if (activeWriter !== writer) return;
          if (!written.has(other)) {
            choose(other);
            showMe();
          }
        });
      } else {
        msg.className = "write-msg retry";
        const hint =
          r.coverage < 0.72
            ? ["Keep going! Cover the whole gray letter.", "继续描，把整个灰色字母都描满。"]
            : ["Try to stay inside the gray letter.", "尽量描在灰色字母里面。"];
        msg.innerHTML = hint[0] + zhLine(hint[1], "zh-sub");
        Speech.say(hint[0]);
      }
    });
    choose(written.has(upper) && !written.has(lower) ? lower : upper);
    if (written.has(ch)) Speech.say(letterName(ch));
    else requestAnimationFrame(showMe);
  }

  // ---------- router ----------
  function route() {
    Speech.stop();
    if (activeWriter) {
      activeWriter.destroy();
      activeWriter = null;
    }
    const welcome = arriving;
    arriving = false;
    const [, view, id] = location.hash.replace(/^#/, "").split("/");
    const lesson = id && lessonById(id);
    if (view === "learn" && lesson) learn(lesson);
    else if (view === "play" && lesson) play(lesson);
    else if (view === "spell" && lesson && spellable(lesson).length >= 3) spellGame(lesson);
    else if (view === "build" && lesson && buildable(lesson).length >= 3) buildGame(lesson);
    else if (view === "count" && lesson && lesson.game === "count") countGame(lesson);
    else if (view === "blend" && lesson && lesson.game === "blend") blendGame(lesson);
    else if (view === "do" && lesson && lesson.pipSays) pipSays(lesson);
    else if (view === "write" && /^\d+$/.test(id) && Number(id) < 26) write(Number(id));
    else if (view === "scene" && sceneById(id || "sunny")) scene(sceneById(id || "sunny"));
    else if (view === "island" && ISLES.some((i) => i.id === id)) island(ISLES.find((i) => i.id === id), welcome);
    else world();
    if (app.querySelector(".quiz:not(.pipsays-tap):not(.pipsays-act), .write")) app.insertAdjacentHTML("beforeend", BUDDY());
    window.scrollTo(0, 0);
    app.focus({ preventScroll: true });
  }
  window.addEventListener("hashchange", route);
  route();
})();
