// Shared by the world map and the island pages: the islands with their stops, the card a stop opens.
(function () {
  const { buildable, lessonById, mainGame, ROUNDS, sceneById, spellable } = LE.lesson;
  const { app, cover, MIC, PENCIL, stars, theme } = LE.ui;
  const { bestScore, saidCount, stopStars, written } = LE.progress;

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
  const seen = Store.isles;
  const markSeen = (id) => seen.add(id);
  const FAR = Object.keys(window.WORLD.wide.farDocks).map(Number);
  const isNear = (k) => !FAR.includes(k) || seen.has(ISLES[k].id) || ISLES[k].stops.some((id) => stopStars(id) > 0);

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

  LE.map = { stopInfo, ISLES, isleOf, backToIsle, isleStars, starsText, markSeen, FAR, isNear, openCard, dialogHtml,
    wireDialog };
})();
