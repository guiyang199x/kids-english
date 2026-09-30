// Aboard a seasonal visitor (#/ship): the Ghost Ship in October, with its lesson (the same card a map stop opens)
// and its stories. The router only opens it in season (LE.lesson.visitNow); otherwise the map shows instead.
(function () {
  const { app, bookHtml, esc, theme, zhLine } = LE.ui;
  const { stopInfo } = LE.map;

  function ship(visit) {
    const stories = (window.STORIES || []).filter((s) => s.visit === visit.id);
    app.innerHTML = `
      <nav class="crumbs"><a href="#/">← World map</a></nav>
      <section class="ship" style="${theme(visit)}">
        <div class="ship-head">
          <span class="ship-art" aria-hidden="true">${ART[visit.art]}</span>
          <div>
            <h1>The ${esc(visit.title)}${zhLine(visit.zh, "zh-sub")}</h1>
            <p class="ship-hello">${esc(visit.hello)}${zhLine(visit.helloZh)}</p>
          </div>
        </div>
        <div class="ship-deck">
          <div class="ship-lesson">${stopInfo(visit.lesson).card}</div>
          ${stories.length ? `<div class="ship-books"><h2>📖 Stories${zhLine("绘本", "zh-sub")}</h2><div class="shelf">${stories.map(bookHtml).join("")}</div></div>` : ""}
        </div>
      </section>`;
    Speech.say([`Welcome aboard the ${visit.title}!`, "Boo!"], { gap: 300 });
  }

  LE.views.ship = ship;
})();
