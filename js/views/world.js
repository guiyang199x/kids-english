// Home: Pip and his house at the top, then the big map (ART._bigmap, tools/art/build27.py): one tall map in three
// regions by level, with a road past every place. Tap a place and Pip walks there along the road, the page
// scrolling with him; then the map zooms in and the place opens.
(function () {
  const { app, reduceMotion, theme, tween, zhLine } = LE.ui;
  const { lessonById, LEVELS, levelOf, seasonal, visitNow } = LE.lesson;
  const { childLevel, dueWords, REVIEW, stopStars } = LE.progress;
  const { isleOf, ISLES, nextStop, starsText } = LE.map;
  const { unanswered } = LE.home;

  let arriving = false; // true while Pip walks into a place, so its page plays the welcome

  // How much of each level is done: lessons with 2 stars or more, of all the lessons at that level.
  function levelDone(n) {
    const at = window.LESSONS.filter((l) => levelOf(l).n === n && !seasonal(l));
    return { done: at.filter((l) => stopStars(l.id) >= 2).length, total: at.length };
  }

  function world() {
    const visit = visitNow();
    const B = window.WORLD.bigmap;
    // What Pip suggests next, and at which place.
    const suggested = nextStop();
    const next = suggested ? ISLES.indexOf(isleOf(suggested)) : -1;
    // Pip waits at the place he last went to, or at the one with the next thing to play.
    let at = Store.boat();
    if (!(at >= 0 && at < ISLES.length)) at = next >= 0 ? next : 0;

    // The child's level, and Pip's suggestion: a button that walks there.
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
    // The visitor: Pip points it out, and the button walks down to it.
    const visitBtn = visit
      ? `<span class="hero-act"><button class="btn primary hero-visit" style="${theme(visit)}">👻 The ${visit.title} is here!</button>` +
        zhLine(`${visit.zh}来啦！`, "zh-sub") + `</span>`
      : "";
    // Pip's house stands behind him; its mailbox flag is up while a letter waits for a reply.
    const letters = unanswered();
    const home = `
        <a class="hero-home${letters ? " has-mail" : ""}" href="#/house" aria-label="Pip's House${letters ? ": a new letter!" : ""}">
          <span class="hero-home-art" aria-hidden="true">${ART["_home-hero"]}</span>${letters ? `<span class="hero-home-badge" aria-hidden="true">✉</span>` : ""}
          <span class="hero-home-plate"><b>Pip's House</b>${zhLine("Pip 的小屋", "zh-sub")}${letters ? `<span class="isle-new">✉ New letter!</span>` : ""}</span>
        </a>`;
    // The map's region signs (with how much of their level is done) and a name plate under each place.
    const signs = window.REGIONS.map((r, k) => {
      const lvl = LEVELS[r.level - 1];
      const d = levelDone(r.level);
      return `
        <div class="region-sign" style="left:${B.signs[k][0]}%;top:${B.signs[k][1]}%">
          <span>${lvl.icon} Level ${lvl.n} · ${d.done}/${d.total}</span><b>${r.title}</b>${zhLine(r.zh, "zh-sub")}
        </div>`;
    }).join("");
    const plates = ISLES.map((isle, k) => `
        <button class="isle-label place-label" data-i="${k}" style="left:${B.labels[k][0]}%;top:${B.labels[k][1]}%">
          <b>${isle.title}</b>${zhLine(isle.zh, "zh-sub")}<span class="isle-stars">${starsText(isle)}</span>
        </button>`).join("");

    app.innerHTML = `
      <section class="map-hero">
        <span class="hero-stage">${home}<span class="hero-pip" aria-hidden="true">${next >= 0 ? ART._pip : ART._pip_cheer}</span></span>
        <div class="hero-bubble">
          <h1>Let's learn English!</h1>
          <p>Hi, I'm Pip! Where shall we go today?</p>
          ${zhLine("你好，我是 Pip！今天去哪儿？", "zh-sub")}
          ${levelLine}
          ${nextBtn || reviewBtn || visitBtn ? `<div class="hero-actions">${nextBtn}${reviewBtn}${visitBtn}</div>` : ""}
        </div>
      </section>
      <div class="bigmap${visit ? " visit-" + visit.id : ""}">${ART._bigmap}${signs}${plates}</div>`;

    const map = app.querySelector(".bigmap");
    const svg = map.querySelector("svg");
    const road = svg.querySelector(".bigroad");
    const pip = svg.querySelector(".bigpip");
    const total = road.getTotalLength();
    // How far along the road each place is: the nearest point to its landmark.
    const along = B.places.map(([x, y]) => {
      let best = 0;
      let bestD = Infinity;
      for (let L = 0; L <= total; L += 6) {
        const p = road.getPointAtLength(L);
        const d = Math.hypot(p.x - x, p.y - y);
        if (d < bestD) [best, bestD] = [L, d];
      }
      return best;
    });
    let now = along[at];
    const put = (L) => {
      const p = road.getPointAtLength(L);
      pip.setAttribute("transform", `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`);
      return p;
    };
    put(now);
    // Where a point of the map is on the page, to keep Pip in sight while he walks.
    const pageY = (y) => map.getBoundingClientRect().top + window.scrollY + (y / B.H) * map.offsetHeight;
    const follow = (y) => window.scrollTo(0, Math.max(0, pageY(y) - innerHeight / 2));

    // Into a place (or aboard the visitor): the map zooms towards it, then its page opens.
    function enter(k, toShip) {
      Store.setBoat(k);
      const [x, y] = toShip ? B.visit.pos : B.places[k];
      map.style.transformOrigin = `${(x / B.W) * 100}% ${(y / B.H) * 100}%`;
      map.classList.add("zoom");
      setTimeout(() => {
        arriving = !toShip;
        location.hash = toShip ? "#/ship" : "#/island/" + ISLES[k].id;
      }, reduceMotion() ? 0 : 650);
    }
    let busy = false;
    function go(k, toShip = false) {
      if (busy) return;
      busy = true;
      const from = now;
      const to = along[k];
      now = to;
      const flip = pip.querySelector(".bigpip-flip");
      pip.classList.add("walking");
      tween(
        Math.min(3200, Math.max(700, Math.abs(to - from) * 1.6)),
        (t) => {
          const p0 = road.getPointAtLength(from + (to - from) * Math.max(0, t - 0.01));
          const p = put(from + (to - from) * t);
          flip.classList.toggle("left", p.x < p0.x);
          follow(p.y);
        },
        () => {
          pip.classList.remove("walking");
          setTimeout(() => enter(k, toShip), 200);
        }
      );
    }
    map.querySelectorAll(".place-g, .place-label").forEach((el) => el.addEventListener("click", () => go(+el.dataset.i)));
    app.querySelector(".hero-next")?.addEventListener("click", () => go(next));
    if (visit) {
      const ship = () => go(B.visit.at, true);
      map.querySelector(".visit-g").addEventListener("click", ship);
      app.querySelector(".hero-visit").addEventListener("click", ship);
    }
  }

  LE.views.world = world;
  // For the router: true once, right after Pip walks into a place (so the place plays its welcome).
  LE.views.takeArrival = () => {
    const a = arriving;
    arriving = false;
    return a;
  };
})();
