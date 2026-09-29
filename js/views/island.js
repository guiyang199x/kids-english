// Inside an island: its map, the stops along the road, and Pip walking to them.
(function () {
  const { app, bounce, reduceMotion, tween, zhLine } = LE.ui;
  const { lessonById, levelOf } = LE.lesson;
  const { stopStars } = LE.progress;
  const { aboveLevel, dialogHtml, nextStop, openCard, starsText, stopInfo, wireDialog } = LE.map;

  function island(isle, welcome) {
    const map = window.WORLD.isles[isle.id];
    const onRoad = isle.stops.slice(0, map.stops.length);
    const below = isle.stops.slice(map.stops.length);
    // The next stop: what Pip suggests if it's on this island; otherwise the first one without stars, not above
    // the child's level if there's a choice. An island of picture dictionaries only (no stars at all) starts at its first stop.
    const scored = isle.stops.filter((id) => stopStars(id) !== null);
    const suggested = nextStop();
    const unplayed = isle.stops.filter((id) => stopStars(id) === 0);
    const nextId = isle.stops.includes(suggested)
      ? suggested
      : scored.length
      ? unplayed.find((id) => !aboveLevel(id)) || unplayed[0]
      : isle.stops[0];
    const stopHtml = (id, i, pos) => {
      const st = stopInfo(id);
      const n = stopStars(id);
      const l = lessonById(id);
      const lv = l && levelOf(l);
      const above = aboveLevel(id);
      const label = (n === null ? st.title : `${st.title}, ${n} of 3 stars`) + (lv ? `, level ${lv.n}${above ? ", a challenge" : ""}` : "");
      const place = pos ? ` style="left:${(pos[0] / map.W) * 100}%;top:${(pos[1] / map.H) * 100}%"` : "";
      return `
        <div class="stop-abs${id === nextId ? " is-next" : ""}"${place}>
          <button class="node${n === 3 ? " done" : ""}${id === nextId ? " next" : ""}" style="${st.theme}" data-id="${id}" data-i="${i}" aria-haspopup="dialog" aria-label="${label}">
            <span class="node-art">${st.art}</span>
          </button>
          ${lv ? `<span class="node-level${above ? " above" : ""}" aria-hidden="true">${lv.icon}</span>` : ""}
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

  LE.views.island = island;
})();
