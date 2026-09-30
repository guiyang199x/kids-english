// The sticker book (#/stickers, and #/stickers/<lessonId> for one page): a page for every lesson, a sticker for every
// word. A sticker is a gray shape until the child meets the word in a game (or says it), then its picture; it turns
// shiny once the word is mastered in the review (see LE.home.sticker).
(function () {
  const { mainGame } = LE.lesson;
  const { app, bounce, celebrate, cover, esc, pic, theme, zhLine } = LE.ui;
  const { albumLessons, albumPage, albumTotals, sticker } = LE.home;

  const BOOK = { color: "#8150c4", tint: "#f0e8fb" };
  const bar = ({ found, total }) =>
    `<span class="album-bar" aria-hidden="true"><i style="width:${Math.round((found / total) * 100)}%"></i></span>`;

  // The cover: how many stickers there are, and a page for each lesson.
  function index() {
    const t = albumTotals();
    const page = (l) => {
      const p = albumPage(l);
      return `
        <a class="album-page${p.found === p.total ? " full" : ""}" href="#/stickers/${l.id}" style="${theme(l)}"
           aria-label="${esc(l.title)}: ${p.found} of ${p.total} stickers${p.shiny ? `, ${p.shiny} shiny` : ""}">
          <span class="album-cover" aria-hidden="true">${cover(l)}</span>
          <b>${esc(l.title)}</b>
          ${bar(p)}
          <span class="album-num">${p.found}/${p.total}${p.shiny ? ` <span class="album-shiny">✨${p.shiny}</span>` : ""}</span>
        </a>`;
    };
    app.innerHTML = `
      <nav class="crumbs"><a href="#/house">← Pip's House</a></nav>
      <section class="album" style="${theme(BOOK)}">
        <header class="album-head">
          <h1>My Sticker Book${zhLine("我的图鉴", "zh-sub")}</h1>
          <p class="album-total"><span>★ ${t.found}/${t.total} stickers</span>${t.shiny ? `<span>✨ ${t.shiny} shiny</span>` : ""}</p>
        </header>
        <p class="album-how">Play the games to find stickers. A word you still know days later turns shiny!
          ${zhLine("玩游戏收集贴纸。过了好几天还记得的词，会变成闪亮贴纸！")}</p>
        <div class="album-pages">${albumLessons().map(page).join("")}</div>
      </section>`;
  }

  // One page: a sticker for each of the lesson's words.
  function page(lesson) {
    const all = albumLessons();
    const k = all.indexOf(lesson);
    const [prev, next] = [all[k - 1], all[k + 1]];
    const p = albumPage(lesson);
    const g = mainGame(lesson);
    const slot = (it, i) => {
      const kind = sticker(lesson, it);
      const name = kind === "none" ? "?" : esc(it.word);
      return `
        <button class="sticker ${kind}" data-i="${i}" aria-label="${kind === "none" ? "A sticker still to find" : esc(it.word) + (kind === "shiny" ? ", shiny" : "")}">
          <span class="sticker-pic" aria-hidden="true">${pic(it)}</span>
          <b aria-hidden="true">${name}</b>
          ${kind === "none" ? "" : zhLine(it.zh, "zh-sub")}
          ${kind === "shiny" ? `<span class="sticker-star" aria-hidden="true">★</span>` : ""}
        </button>`;
    };
    app.innerHTML = `
      <nav class="crumbs"><a href="#/stickers">← Sticker Book</a></nav>
      <section class="album" style="${theme(lesson)}">
        <header class="album-head">
          <h1>${esc(lesson.title)}</h1>
          <p class="album-total"><span>★ ${p.found}/${p.total}</span>${p.shiny ? `<span>✨ ${p.shiny}</span>` : ""}</p>
        </header>
        <p class="album-msg" aria-live="polite"></p>
        <div class="stickers">${lesson.items.map(slot).join("")}</div>
        <nav class="album-turn">
          ${prev ? `<a class="btn" href="#/stickers/${prev.id}" aria-label="Previous page: ${esc(prev.title)}">◀ ${esc(prev.title)}</a>` : "<span></span>"}
          ${next ? `<a class="btn" href="#/stickers/${next.id}" aria-label="Next page: ${esc(next.title)}">${esc(next.title)} ▶</a>` : "<span></span>"}
        </nav>
      </section>`;

    const msg = app.querySelector(".album-msg");
    app.querySelectorAll(".sticker").forEach((b) =>
      b.addEventListener("click", () => {
        const it = lesson.items[b.dataset.i];
        const kind = sticker(lesson, it);
        bounce(b);
        if (kind === "none") {
          // Still hiding: the games are where it's found.
          msg.innerHTML =
            `This sticker is still hiding! <a class="btn primary" href="#/${g.view}/${lesson.id}">▶ ${g.label}</a> ` +
            `<a class="btn" href="#/learn/${lesson.id}">Learn</a>` + zhLine("这张贴纸还藏着呢！去玩游戏找到它吧。");
          Speech.say("It's hiding! Let's play and find it!");
          return;
        }
        msg.innerHTML = `<b>${esc(it.word)}</b>${kind === "shiny" ? " ✨ You know it well!" : ""}` + zhLine(it.zh);
        if (kind === "shiny") celebrate(b, 14);
        Speech.say(it.sentence ? [it.word, it.sentence] : it.word, { gap: 300 });
      })
    );
  }

  LE.views.stickers = (lesson) => (lesson ? page(lesson) : index());
})();
