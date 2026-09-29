// A picture story (js/content/stories.js), one page at a time. Each page is read out with the sentence being
// spoken lit up; "Word by word" reads it one word at a time for a child pointing along. A tapped word is said,
// and a word a lesson teaches also shows its picture card. Tapping a sprite in the picture says it and moves it.
(function () {
  const { storyLink, storySentences } = LE.lesson;
  const { app, bounce, celebrate, esc, pic, progress, storyPic, theme, viewBox, zhLine } = LE.ui;
  const { ISLES } = LE.map;

  // The page's picture, no taller than --pic-h: the width that makes comes from the picture's shape.
  function picture(page) {
    const [, , W, H] = viewBox(ART[page.bg]);
    return storyPic(page, `style="max-width:calc(var(--pic-h) * ${(W / H).toFixed(3)})"`);
  }

  // One span per sentence, one button per word. The punctuation right after a word stays on its line ("beach.").
  function textHtml(sentences) {
    const word = (p, stuck) =>
      `<span class="wp"><button class="w${p.link ? " link" : ""}">${esc(p.word)}</button>${esc(stuck)}</span>`;
    return sentences
      .map((parts) => {
        // Text before the first word (a quote mark, say), then each word with the text after it.
        let html = esc(parts[0].text || "");
        parts.forEach((p, k) => {
          if (!p.word) return;
          const after = (parts[k + 1] && parts[k + 1].text) || "";
          const stuck = after.match(/^\S*/)[0];
          html += word(p, stuck) + esc(after.slice(stuck.length));
        });
        return `<span class="sent">${html}</span>`;
      })
      .join("");
  }

  function story(st) {
    const isle = ISLES.find((i) => i.id === st.island);
    const home = isle ? { href: "#/island/" + isle.id, title: isle.title } : { href: "#/", title: "World map" };
    const total = st.pages.length;
    let at = 0;
    let run = 0; // goes up with every reading, so an older one stops lighting words

    app.innerHTML = `
      <nav class="crumbs"><a href="${home.href}">← ${home.title}</a></nav>
      <section class="story" style="${theme(st)}">
        <header class="story-top">
          <h1>${esc(st.title)}${zhLine(st.zh, "zh-sub")}</h1>
          <span class="progress" aria-live="polite"></span>
        </header>
        <div class="story-page"></div>
      </section>`;
    const box = app.querySelector(".story-page");
    const dots = app.querySelector(".story-top .progress");

    const unlight = () => box.querySelectorAll(".on").forEach((el) => el.classList.remove("on"));
    // Reads the page: sentence by sentence, or word by word (`slow`), lighting each part as it's spoken.
    function read(slow) {
      const my = ++run;
      unlight();
      const parts = [...box.querySelectorAll(slow ? ".w" : ".sent")];
      const light = (k) => {
        if (my !== run) return;
        unlight();
        if (parts[k]) parts[k].classList.add("on");
      };
      Speech.say(
        parts.map((el) => el.textContent.trim()),
        { gap: slow ? 250 : 450, rateScale: slow ? 0.9 : 1, onPart: light }
      ).then(() => light(-1));
    }
    // The picture card for a word a lesson teaches, under the text.
    function showCard(link) {
      const card = box.querySelector(".story-word");
      card.innerHTML = link
        ? `<span class="story-word-pic">${pic(link.it)}</span><span><b>${esc(link.it.word)}</b>${zhLine(link.it.zh)}</span>`
        : "";
      card.classList.toggle("shown", !!link);
    }

    function showPage(i) {
      at = i;
      run++;
      Speech.stop();
      const page = st.pages[i];
      dots.innerHTML = progress("Page", i, total);
      box.innerHTML = `
        <div class="story-pic">${picture(page)}</div>
        <p class="story-text">${textHtml(storySentences(st, page.text))}</p>
        ${zhLine(page.zh, "zh story-zh")}
        <div class="story-word" aria-live="polite"></div>
        <div class="story-nav">
          <button class="btn story-prev" aria-label="Previous page"${i ? "" : " disabled"}>◀</button>
          <button class="btn primary story-read">🔊 Read</button>
          <button class="btn story-slow">🐢 Word by word</button>
          <button class="btn primary story-next" aria-label="${i === total - 1 ? "The end" : "Next page"}">${i === total - 1 ? "The End ▶" : "▶"}</button>
        </div>
        <label class="story-auto"><input type="checkbox"${Store.setting("autoread") === "1" ? " checked" : ""}> Read each page out</label>`;
      const $ = (sel) => box.querySelector(sel);
      $(".story-prev").addEventListener("click", () => go(-1));
      $(".story-next").addEventListener("click", () => go(1));
      $(".story-read").addEventListener("click", () => read(false));
      $(".story-slow").addEventListener("click", () => read(true));
      $(".story-auto input").addEventListener("change", (e) => Store.setSetting("autoread", e.target.checked ? "1" : "0"));

      box.querySelectorAll(".w").forEach((b) =>
        b.addEventListener("click", () => {
          run++;
          unlight();
          b.classList.add("on");
          showCard(storyLink(st, b.textContent));
          Speech.say(b.textContent);
        })
      );
      box.querySelectorAll(".sprite.tap").forEach((g) => {
        const s = page.sprites[g.dataset.i];
        const act = () => {
          run++;
          unlight();
          if (s.anim) bounce(g.querySelector(".sprite-move"), "move-" + s.anim);
          showCard(storyLink(st, s.word));
          Speech.say(s.word);
        };
        g.addEventListener("click", act);
        g.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            act();
          }
        });
      });
      if (Store.setting("autoread") === "1") read(false);
    }

    function theEnd() {
      at = total;
      run++;
      dots.innerHTML = progress("Page", total, total);
      box.innerHTML = `
        <div class="story-end">
          <span class="story-end-pip" aria-hidden="true">${ART._pip_cheer}</span>
          <h2>The End</h2>
          ${zhLine("讲完啦！", "zh-sub")}
          <div class="story-nav">
            <button class="btn story-again">↺ Read again</button>
            <a class="btn primary" href="${home.href}">${home.title}</a>
          </div>
        </div>`;
      box.querySelector(".story-again").addEventListener("click", () => showPage(0));
      celebrate(box.querySelector("h2"));
      Speech.say(["The end!", "Great reading!"], { gap: 300 });
    }

    function go(d) {
      const i = at + d;
      if (i < 0) return;
      if (i >= total) theEnd();
      else showPage(i);
    }

    // Arrow keys and a swipe across the page turn it too.
    const onKey = (e) => {
      if (!box.isConnected) return document.removeEventListener("keydown", onKey);
      if (at >= total || e.target.closest?.("input:not([type=checkbox]), select, textarea")) return;
      if (e.key === "ArrowRight") go(1);
      else if (e.key === "ArrowLeft") go(-1);
    };
    document.addEventListener("keydown", onKey);
    let downX = null;
    box.addEventListener("pointerdown", (e) => (downX = e.clientX));
    box.addEventListener("pointerup", (e) => {
      const dx = downX === null ? 0 : e.clientX - downX;
      downX = null;
      if (at < total && Math.abs(dx) > 60) go(dx < 0 ? 1 : -1);
    });

    showPage(0);
  }

  LE.views.story = story;
})();
