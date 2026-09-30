// Shared by the world map and the island pages: the islands with their stops, the card a stop opens.
(function () {
  const { buildable, lessonById, levelOf, mainGame, ROUNDS, sceneById, seasonal, spellable, yesnoable } = LE.lesson;
  const { app, cover, MIC, PENCIL, stars, theme, zhLine } = LE.ui;
  const { bestScore, childLevel, saidCount, stopStars, written } = LE.progress;

  // A lesson above the child's level. It's open like any other; the map just marks it as a challenge.
  const aboveLevel = (id) => {
    const l = lessonById(id);
    return !!l && levelOf(l).n > childLevel().n;
  };

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
        <p class="tile-level">${levelOf(l).icon} Level ${levelOf(l).n}${aboveLevel(id) ? " · Challenge!" : ""}${zhLine(
          `第 ${levelOf(l).n} 级：${levelOf(l).zh}${aboveLevel(id) ? "（挑战）" : ""}`,
          "zh-sub"
        )}</p>
        <a class="btn primary learn" href="#/learn/${l.id}">Learn</a>
        <div class="games">
          ${game(`#/${g.view}/${l.id}`, g.label, bestScore(g.key))}
          ${spellable(l).length >= 3 ? game(`#/spell/${l.id}`, "Spell", bestScore("spell-" + l.id)) : ""}
          ${buildable(l).length >= 3 ? game(`#/build/${l.id}`, "Build", bestScore("build-" + l.id)) : ""}
          ${l.pipSays ? game(`#/do/${l.id}`, "Pip says", bestScore("do-" + l.id)) : ""}
          ${yesnoable(l) ? game(`#/yesno/${l.id}`, "Yes/No", bestScore("yesno-" + l.id)) : ""}
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
        <div class="games">${game(`#/find/${s.id}`, "Find it", bestScore("find-" + s.id))}</div>
      </article>`,
      };
    return null;
  }

  // The islands with their stops; anything nobody listed joins the last island (but not a seasonal lesson: that comes
  // with its visitor).
  const ISLES = (() => {
    const all = [...window.LESSONS.filter((l) => !seasonal(l)).map((l) => l.id), "write", ...window.SCENES.map((s) => "scene-" + s.id)];
    const listed = new Set(window.ISLANDS.flatMap((i) => i.stops));
    const extra = all.filter((id) => !listed.has(id));
    return window.ISLANDS.map((isle, k) => ({
      ...isle,
      stops: [...isle.stops, ...(k === window.ISLANDS.length - 1 ? extra : [])].filter((id) => all.includes(id)),
    }));
  })();
  const isleOf = (stopId) => ISLES.find((i) => i.stops.includes(stopId));
  const backToIsle = (stopId) => {
    const isle = isleOf(stopId);
    const visit = (window.VISITS || []).find((v) => v.lesson === stopId);
    if (isle) return `<nav class="crumbs"><a href="#/island/${isle.id}">← ${isle.title}</a></nav>`;
    if (visit) return `<nav class="crumbs"><a href="#/ship">← ${visit.title}</a></nav>`;
    return `<nav class="crumbs"><a href="#/">← World map</a></nav>`;
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

  // What Pip suggests next, in island order: a lesson at or below the child's level with no stars yet, then one
  // there with only 1 star, then any lesson with no stars (the next level up). null once everything has stars.
  function nextStop() {
    const n = childLevel().n;
    const lessons = ISLES.flatMap((i) => i.stops).map(lessonById).filter(Boolean);
    const fits = (l) => levelOf(l).n <= n;
    const l =
      lessons.find((l) => fits(l) && stopStars(l.id) === 0) ||
      lessons.find((l) => fits(l) && stopStars(l.id) < 2) ||
      lessons.find((l) => stopStars(l.id) === 0);
    return l ? l.id : null;
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

  LE.map = { aboveLevel, nextStop, stopInfo, ISLES, isleOf, backToIsle, isleStars, starsText, openCard, dialogHtml,
    wireDialog };
})();
