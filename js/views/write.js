// Write: trace a letter on the pad (js/writer.js), capital and small.
(function () {
  const { lessonById } = LE.lesson;
  const { app, bounce, celebrate, pic, praise, theme, zhLine } = LE.ui;
  const { markWritten, written } = LE.progress;

  let activeWriter = null;
  function write(index) {
    const lesson = lessonById("alphabet");
    const it = lesson.items[index];
    const upper = it.letter[0];
    const lower = it.letter[1];
    const prev = (index + 25) % 26;
    const next = (index + 1) % 26;
    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/alphabet">← ABC</a></nav>
      <section class="write" style="${theme(lesson)}">
        <div class="write-head">
          <a class="btn round" href="#/write/${prev}" aria-label="Previous letter">‹</a>
          <div class="case-tabs" role="group" aria-label="Choose a letter">
            <button class="case" data-c="${upper}">${upper}<span class="case-star">★</span></button>
            <button class="case" data-c="${lower}">${lower}<span class="case-star">★</span></button>
          </div>
          <a class="btn round" href="#/write/${next}" aria-label="Next letter">›</a>
        </div>
        <div class="write-body">
          <div class="pad-wrap"><canvas class="pad" aria-label="Writing pad. Trace the letter with your finger or mouse."></canvas></div>
          <aside class="write-word">
            <span class="card-art">${pic(it)}</span>
            <span class="word">${it.word}</span>
            ${zhLine(it.zh)}
          </aside>
        </div>
        <p class="write-msg" aria-live="polite"></p>
        <div class="tile-actions">
          <button class="btn primary show">✎ Show me</button>
          <button class="btn hear">▶ Hear it</button>
          <button class="btn clear">Clear</button>
          <button class="btn primary check">Done</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const msg = $(".write-msg");
    const writer = (activeWriter = Writer.mount($(".pad"), { color: lesson.color }));
    let ch = upper;
    const cases = [...app.querySelectorAll(".case")];
    const refreshTabs = () =>
      cases.forEach((b) => {
        b.classList.toggle("on", b.dataset.c === ch);
        b.classList.toggle("done", written.has(b.dataset.c));
        b.setAttribute("aria-pressed", b.dataset.c === ch);
      });
    const choose = (c) => {
      ch = c;
      writer.setChar(c);
      refreshTabs();
      setTip();
    };
    const setTip = () => {
      msg.className = "write-msg";
      msg.innerHTML =
        "Start at the green dot 1. Follow the numbers." + zhLine("从绿色的 1 号点开始，按数字顺序描。", "zh-sub");
    };
    const showMe = () => {
      const n = writer.strokeCount();
      msg.className = "write-msg";
      msg.innerHTML = `Watch! ${letterName(ch)} has ${n} stroke${n > 1 ? "s" : ""}.` + zhLine(`看好了！这个字母有 ${n} 笔。`, "zh-sub");
      Speech.say(`Watch. ${letterName(ch)}.`);
      writer.playDemo().then((finished) => {
        if (!finished || activeWriter !== writer) return;
        msg.innerHTML = "Now you try!" + zhLine("现在轮到你了！", "zh-sub");
        Speech.say("Now you try!");
      });
    };
    const letterName = (c) => (c === upper ? "Big " + upper : "Small " + lower);
    cases.forEach((b) =>
      b.addEventListener("click", () => {
        choose(b.dataset.c);
        if (written.has(ch)) Speech.say(letterName(ch));
        else showMe();
      })
    );
    $(".show").addEventListener("click", showMe);
    $(".hear").addEventListener("click", () => Speech.say([letterName(ch), it.sentence], { gap: 300 }));
    $(".clear").addEventListener("click", () => writer.clear());
    $(".check").addEventListener("click", () => {
      const r = writer.check();
      if (r.empty) {
        msg.className = "write-msg retry";
        msg.innerHTML = "Draw on the letter first!" + zhLine("先在字母上描一描！", "zh-sub");
        return;
      }
      if (r.pass) {
        markWritten(ch);
        refreshTabs();
        msg.className = "write-msg good";
        msg.innerHTML = r.orderOk
          ? "★ " + praise() + zhLine("写得真好！", "zh-sub")
          : "★ Good! Next time, start at dot 1 and follow the numbers." +
            zhLine("写得不错！下次从 1 号点开始，按数字顺序写。", "zh-sub");
        bounce($(".pad-wrap"), "pop");
        celebrate($(".pad-wrap"));
        const other = ch === upper ? lower : upper;
        Speech.say([praise(), letterName(ch)], { gap: 250 }).then(() => {
          if (activeWriter !== writer) return;
          if (!written.has(other)) {
            choose(other);
            showMe();
          }
        });
      } else {
        msg.className = "write-msg retry";
        const hint =
          r.coverage < 0.72
            ? ["Keep going! Cover the whole gray letter.", "继续描，把整个灰色字母都描满。"]
            : ["Try to stay inside the gray letter.", "尽量描在灰色字母里面。"];
        msg.innerHTML = hint[0] + zhLine(hint[1], "zh-sub");
        Speech.say(hint[0]);
      }
    });
    choose(written.has(upper) && !written.has(lower) ? lower : upper);
    if (written.has(ch)) Speech.say(letterName(ch));
    else requestAnimationFrame(showMe);
  }

  LE.views.write = write;
  // For the router: leaving the page stops the pad.
  LE.views.stopWriting = () => {
    if (activeWriter) {
      activeWriter.destroy();
      activeWriter = null;
    }
  };
})();
