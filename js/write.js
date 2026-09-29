// Letter tracing pad: draws a guide letter from stroke-order data (js/strokes.js) on four-line
// paper, animates how to write it, records the child's strokes, and scores the tracing.
(function () {
  const L = 300; // logical canvas size (square)
  const TOP = 52; // y of the top line; 1 design unit = SCALE px (see strokes.js for units)
  const SCALE = 1.6;
  const LINES = { top: TOP, mid: TOP + 50 * SCALE, base: TOP + 100 * SCALE, bottom: TOP + 140 * SCALE };
  const PEN = 14; // child's pen width
  const GUIDE = 26; // width of the pale guide letter
  const START_R = 11; // numbered start dot radius

  // ---------- geometry: sample each stroke path into points ----------
  const cache = {};
  let sampler = null;
  function samplePath(d) {
    if (!sampler) {
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("width", "0");
      svg.setAttribute("height", "0");
      svg.style.position = "absolute";
      sampler = document.createElementNS("http://www.w3.org/2000/svg", "path");
      svg.appendChild(sampler);
      document.body.appendChild(svg);
    }
    sampler.setAttribute("d", d);
    const len = sampler.getTotalLength();
    const n = Math.max(1, Math.ceil(len / 2));
    const pts = [];
    for (let i = 0; i <= n; i++) {
      const p = sampler.getPointAtLength((len * i) / n);
      pts.push({ x: p.x, y: p.y });
    }
    return { pts, len };
  }

  // Returns strokes in canvas coordinates, horizontally centered: [{ pts, len, dot }]
  function letterStrokes(ch) {
    if (cache[ch]) return cache[ch];
    const raw = (window.STROKES[ch] || []).map(samplePath);
    let minX = Infinity, maxX = -Infinity;
    raw.forEach((s) => s.pts.forEach((p) => ((minX = Math.min(minX, p.x)), (maxX = Math.max(maxX, p.x)))));
    const dx = L / 2 - ((minX + maxX) / 2) * SCALE;
    cache[ch] = raw.map((s) => ({
      pts: s.pts.map((p) => ({ x: dx + p.x * SCALE, y: TOP + p.y * SCALE })),
      len: s.len * SCALE,
      dot: s.len < 3,
    }));
    return cache[ch];
  }

  // ---------- drawing helpers ----------
  function path(ctx, pts, upTo = pts.length) {
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    if (upTo <= 1) ctx.lineTo(pts[0].x + 0.1, pts[0].y);
    for (let i = 1; i < upTo; i++) ctx.lineTo(pts[i].x, pts[i].y);
    ctx.stroke();
  }
  function pen(ctx, width, color) {
    ctx.lineWidth = width;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = color;
  }
  function drawUser(ctx, strokes, width, color = "#000") {
    pen(ctx, width, color);
    for (const s of strokes) path(ctx, s);
  }
  function arrowHead(ctx, pts, color) {
    // small chevron just after the start dot, pointing along the stroke
    const a = pts[0];
    const b = pts[Math.min(pts.length - 1, 12)];
    const ang = Math.atan2(b.y - a.y, b.x - a.x);
    ctx.save();
    ctx.translate(a.x + Math.cos(ang) * 22, a.y + Math.sin(ang) * 22);
    ctx.rotate(ang);
    pen(ctx, 3, color);
    ctx.beginPath();
    ctx.moveTo(-5, -6);
    ctx.lineTo(2, 0);
    ctx.lineTo(-5, 6);
    ctx.stroke();
    ctx.restore();
  }
  function offscreen() {
    const c = document.createElement("canvas");
    c.width = c.height = L;
    return c.getContext("2d", { willReadFrequently: true });
  }

  function mount(canvas, { color = "#ef5b56" } = {}) {
    const ctx = canvas.getContext("2d");
    let ch = "A";
    let strokes = [];
    let current = null;
    let demo = null; // { stroke, progress } while animating
    let raf = 0;

    function resize() {
      const css = canvas.clientWidth || L;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = canvas.height = Math.round(css * dpr);
      ctx.setTransform((css * dpr) / L, 0, 0, (css * dpr) / L, 0, 0);
      render();
    }

    function render() {
      const guide = letterStrokes(ch);
      ctx.clearRect(0, 0, L, L);
      ctx.fillStyle = "#fff";
      ctx.fillRect(0, 0, L, L);

      // four-line handwriting paper
      const line = (y, c, dash) => {
        ctx.setLineDash(dash || []);
        pen(ctx, 2, c);
        ctx.lineCap = "butt";
        ctx.beginPath();
        ctx.moveTo(12, y);
        ctx.lineTo(L - 12, y);
        ctx.stroke();
      };
      line(LINES.top, "#9cc3ea");
      line(LINES.mid, "#f4a3a3", [8, 8]);
      line(LINES.base, "#9cc3ea");
      line(LINES.bottom, "#cfe0f0");
      ctx.setLineDash([]);

      // pale guide letter with a dotted center line
      for (const s of guide) {
        pen(ctx, GUIDE, "#efe8dc");
        path(ctx, s.pts);
      }
      ctx.setLineDash([2, 7]);
      for (const s of guide) {
        if (s.dot) continue;
        pen(ctx, 2.5, "#b7aa94");
        path(ctx, s.pts);
      }
      ctx.setLineDash([]);

      // demo animation strokes
      if (demo) {
        for (let i = 0; i <= demo.stroke && i < guide.length; i++) {
          const s = guide[i];
          const upTo = i < demo.stroke ? s.pts.length : Math.max(1, Math.round(s.pts.length * demo.progress));
          pen(ctx, PEN + 2, "#7ccb6b");
          path(ctx, s.pts, upTo);
          if (i === demo.stroke) {
            const tip = s.pts[upTo - 1];
            ctx.fillStyle = "#2f9a44";
            ctx.beginPath();
            ctx.arc(tip.x, tip.y, 9, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      // the child's strokes
      drawUser(ctx, strokes, PEN, color);

      // numbered start dots and direction arrows (on top so they stay visible)
      const placed = [];
      guide.forEach((s, i) => {
        let p = s.pts[0];
        if (placed.some((q) => Math.hypot(q.x - p.x, q.y - p.y) < START_R * 2.2)) {
          // overlaps an earlier dot: slide this badge backwards from the stroke direction
          const b = s.pts[Math.min(s.pts.length - 1, 12)];
          const ang = Math.atan2(b.y - p.y, b.x - p.x);
          const q = { x: p.x - Math.cos(ang) * 24, y: p.y - Math.sin(ang) * 24 };
          pen(ctx, 2, "#2f9a44");
          ctx.beginPath();
          ctx.moveTo(q.x, q.y);
          ctx.lineTo(p.x, p.y);
          ctx.stroke();
          p = q;
        }
        placed.push(p);
        if (!s.dot) arrowHead(ctx, s.pts, "#2f9a44");
        ctx.fillStyle = "#2f9a44";
        ctx.beginPath();
        ctx.arc(p.x, p.y, START_R, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.font = "700 14px system-ui, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(String(i + 1), p.x, p.y + 1);
      });
    }

    // ---------- demo animation ----------
    // Resolves true when the demo finishes, false if it was interrupted.
    function playDemo() {
      stopDemo();
      strokes = [];
      const guide = letterStrokes(ch);
      let i = 0;
      let t0 = null;
      const token = {};
      demo = { stroke: 0, progress: 0, token };
      return new Promise((resolve) => {
        const alive = () => demo && demo.token === token;
        const step = (now) => {
          if (!alive()) return resolve(false);
          const s = guide[i];
          const dur = s.dot ? 250 : Math.max(500, s.len * 6);
          if (t0 === null) t0 = now;
          const k = Math.min(1, (now - t0) / dur);
          demo.stroke = i;
          demo.progress = k;
          render();
          if (k < 1) {
            raf = requestAnimationFrame(step);
          } else if (i < guide.length - 1) {
            i++;
            t0 = null;
            setTimeout(() => (alive() ? (raf = requestAnimationFrame(step)) : resolve(false)), 350);
          } else {
            setTimeout(() => {
              if (!alive()) return resolve(false);
              demo = null;
              render();
              resolve(true);
            }, 700);
          }
        };
        raf = requestAnimationFrame(step);
      });
    }
    function stopDemo() {
      if (!demo) return;
      cancelAnimationFrame(raf);
      demo = null;
      render();
    }

    // ---------- input ----------
    function toLogical(e) {
      const r = canvas.getBoundingClientRect();
      const x = e.clientX - r.left - canvas.clientLeft;
      const y = e.clientY - r.top - canvas.clientTop;
      return { x: (x / canvas.clientWidth) * L, y: (y / canvas.clientHeight) * L };
    }
    canvas.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      stopDemo();
      try {
        canvas.setPointerCapture(e.pointerId);
      } catch (err) {}
      current = [toLogical(e)];
      strokes.push(current);
      render();
    });
    canvas.addEventListener("pointermove", (e) => {
      if (!current) return;
      const coalesced = e.getCoalescedEvents ? e.getCoalescedEvents() : [];
      const events = coalesced.length ? coalesced : [e];
      for (const ev of events) current.push(toLogical(ev));
      render();
    });
    const end = () => (current = null);
    canvas.addEventListener("pointerup", end);
    canvas.addEventListener("pointercancel", end);

    // ---------- scoring ----------
    // Returns { pass, coverage, outside, orderOk, empty }
    function check() {
      const guide = letterStrokes(ch);
      if (!strokes.length) return { pass: false, empty: true, coverage: 0, outside: 0, orderOk: true };
      const glyph = offscreen();
      pen(glyph, GUIDE, "#000");
      guide.forEach((s) => path(glyph, s.pts));

      const zone = offscreen();
      pen(zone, GUIDE + 30, "#000");
      guide.forEach((s) => path(zone, s.pts));

      const ink = offscreen();
      drawUser(ink, strokes, PEN);
      const fat = offscreen();
      drawUser(fat, strokes, 36);

      const px = (c) => c.getImageData(0, 0, L, L).data;
      const [g, z, k, f] = [px(glyph), px(zone), px(ink), px(fat)];
      let glyphN = 0, covered = 0, inkN = 0, out = 0;
      for (let i = 3; i < g.length; i += 8) {
        if (g[i] > 128) {
          glyphN++;
          if (f[i] > 128) covered++;
        }
        if (k[i] > 128) {
          inkN++;
          if (z[i] < 128) out++;
        }
      }
      const coverage = glyphN ? covered / glyphN : 0;
      const outside = inkN ? out / inkN : 1;

      // Gentle stroke-order check: the child's strokes should start near the numbered dots,
      // in order. Tiny taps are ignored unless the letter has a dot (i, j).
      const hasDot = guide.some((gs) => gs.dot);
      const real = strokes.filter((s) => s.length >= 3 || hasDot);
      const near = (a, b) => Math.hypot(a.x - b.x, a.y - b.y) < 34;
      const orderOk = guide.every((gs, i) => !real[i] || near(real[i][0], gs.pts[0]));

      return { pass: coverage >= 0.72 && outside <= 0.25, coverage, outside, orderOk, empty: false };
    }

    window.addEventListener("resize", resize);
    requestAnimationFrame(resize);

    return {
      setChar(c) {
        stopDemo();
        ch = c;
        strokes = [];
        render();
      },
      clear() {
        stopDemo();
        strokes = [];
        render();
      },
      playDemo,
      strokeCount: () => letterStrokes(ch).length,
      check,
      destroy: () => {
        stopDemo();
        window.removeEventListener("resize", resize);
      },
    };
  }

  window.Writer = { mount };
})();
