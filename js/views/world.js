// Home: the sea with the islands, and Pip's boat sailing between them.
(function () {
  const { app, reduceMotion, theme, tween, zhLine } = LE.ui;
  const { lessonById, LEVELS } = LE.lesson;
  const { childLevel, dueWords, REVIEW } = LE.progress;
  const { FAR, isleOf, ISLES, isNear, markSeen, nextStop, starsText } = LE.map;
  const { unanswered } = LE.home;

  let arriving = false; // true while Pip sails into an island, so the island page plays its welcome
  function world() {
    // What Pip suggests next, and on which island.
    const suggested = nextStop();
    const next = suggested ? ISLES.indexOf(isleOf(suggested)) : -1;
    // Pip's boat waits where it last moored, or at the island with the next thing to play.
    let at = Store.boat();
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
    // The child's level, and Pip's suggestion: a button that sails there.
    const level = childLevel();
    const lv = LEVELS[level.n - 1];
    const levelLine =
      `<p class="hero-level"><span aria-hidden="true">${lv.icon}</span> Level ${lv.n}: ${lv.title} <b>${level.done}/${level.total}</b></p>` +
      zhLine(`第 ${lv.n} 级：${lv.zh}，已完成 ${level.done}/${level.total} 课`, "zh-sub");
    const nextBtn = suggested
      ? `<span class="hero-act"><button class="btn primary hero-next">▶ Next: ${lessonById(suggested).title}</button>` +
        zhLine(`下一站：${ISLES[next].zh}`, "zh-sub") + `</span>`
      : "";
    // Enough words due for a review: Pip offers one. It's never required.
    const due = dueWords(REVIEW.size).length;
    const reviewBtn =
      due >= REVIEW.min
        ? `<span class="hero-act"><a class="btn primary hero-review" style="${theme(REVIEW)}" href="#/review">★ ${due} words miss you!</a>` +
          zhLine(`${due} 个词想你了，去复习吧！`, "zh-sub") + `</span>`
        : "";
    // Pip's house stands behind him; its mailbox flag is up while a letter waits for a reply.
    const letters = unanswered();
    const home = `
        <a class="hero-home${letters ? " has-mail" : ""}" href="#/house" aria-label="Pip's House${letters ? ": a new letter!" : ""}">
          <span class="hero-home-art" aria-hidden="true">${ART["_home-hero"]}</span>${letters ? `<span class="hero-home-badge" aria-hidden="true">✉</span>` : ""}
          <span class="hero-home-plate"><b>Pip's House</b>${zhLine("Pip 的小屋", "zh-sub")}${letters ? `<span class="isle-new">✉ New letter!</span>` : ""}</span>
        </a>`;
    app.innerHTML = `
      <section class="map-hero">
        <span class="hero-stage">${home}<span class="hero-pip" aria-hidden="true">${next >= 0 ? ART._pip : ART._pip_cheer}</span></span>
        <div class="hero-bubble">
          <h1>Let's learn English!</h1>
          <p>Hi, I'm Pip! Which island shall we visit?</p>
          ${zhLine("你好，我是 Pip！今天去哪个岛？", "zh-sub")}
          ${levelLine}
          ${nextBtn || reviewBtn ? `<div class="hero-actions">${nextBtn}${reviewBtn}</div>` : ""}
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
      Store.setBoat(k);
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
    app.querySelector(".hero-next")?.addEventListener("click", () => go(next));
  }

  LE.views.world = world;
  // For the router: true once, right after Pip sails into an island (so the island plays its welcome).
  LE.views.takeArrival = () => {
    const a = arriving;
    arriving = false;
    return a;
  };
})();
