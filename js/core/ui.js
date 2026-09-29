// Shared bits of the page: pictures, stars, Chinese lines, lesson colors, Pip's cheer, confetti, motion.
(function () {
  const { ROUNDS } = LE.lesson;

  const app = document.getElementById("app");
  const PRAISE = ["Great job!", "Well done!", "Super!", "You got it!", "Awesome!"];
  const MIC =
    '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';

  // An item shows ART[item.art] when its word is already taken by another picture (e.g. the fruit "orange").
  // Counting items ({count, thing}) show that many copies of ART[thing].
  const pic = (it) => (it.count ? many(it.thing, it.count) : ART[it.art || it.word]);
  const cover = (l) => ART[l.cover] || pic(l.items.find((it) => it.word === l.cover));

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
  // A story page's picture as one SVG: ART[page.bg], then each sprite on top (see js/content/stories.js for x, y
  // and w). Sprites with a `word` can be tapped. `attrs` go on the <svg>.
  const viewBox = (svg) => svg.match(/viewBox="([^"]+)"/)[1].split(" ").map(Number);
  function storyPic(page, attrs = "") {
    const [vx, vy, W, H] = viewBox(ART[page.bg]);
    const sprites = (page.sprites || []).map((s, i) => {
      const [, , sw, sh] = viewBox(ART[s.art]);
      const w = (s.w / 100) * W;
      const h = (w * sh) / sw;
      const x = vx + (s.x / 100) * W - w / 2;
      const y = vy + (s.y / 100) * H - h / 2;
      const tap = s.word ? ` class="sprite tap" data-i="${i}" tabindex="0" role="button" aria-label="${esc(s.word)}"` : ` class="sprite"`;
      return `<g${tap}><g class="sprite-move">${fit(ART[s.art], x, y, w, h)}</g></g>`;
    });
    return `<svg viewBox="${vx} ${vy} ${W} ${H}" ${attrs} xmlns="http://www.w3.org/2000/svg">${fit(ART[page.bg], vx, vy, W, H)}${sprites.join("")}</svg>`;
  }

  const showZh = () => Store.setting("zh") === "1";
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


  function bounce(el, cls = "pop") {
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
  }

  const PENCIL =
    '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16v4ZM13.5 6.5l4 4"/></svg>';

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

  LE.ui = { app, MIC, PENCIL, pic, cover, many, fit, storyPic, viewBox, showZh, zhLine, esc, praise, shuffle, stars, progress, theme,
    BUDDY, celebrate, bounce, reduceMotion, tween };
})();
