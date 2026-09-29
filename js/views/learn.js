// A lesson's picture cards: hear it, spell it or sound it out, and "Say it" speaking practice.
(function () {
  const { buildable, mainGame, onsetOf, onsetSound, rimeSound, spellable } = LE.lesson;
  const { app, bounce, celebrate, esc, MIC, pic, praise, theme, zhLine } = LE.ui;
  const { markSaid, said } = LE.progress;
  const { backToIsle } = LE.map;

  function learn(lesson) {
    const sayLabel = Speech.canListen || Speech.canRecord ? "Say it" : "";
    const cardHtml = (it, i) => `
      <div class="card ${said.has(lesson.id + ":" + it.word) ? "said" : ""}" style="${theme(lesson)}" data-i="${i}">
        <span class="said-badge" title="You said it!" aria-hidden="true">★</span>
        <button class="card-main" aria-label="Hear ${it.word}">
          ${it.letter ? `<span class="letter">${it.letter}</span>` : ""}
          <span class="card-art">${pic(it)}</span>
          <span class="word" ${it.text ? `style="color:${it.text}"` : ""}>${wordLetters(it)}</span>
          ${zhLine(it.zh)}
          ${lesson.showSentence ? `<span class="card-sentence">${it.sentence}${zhLine(it.sentenceZh, "zh-sub")}</span>` : ""}
        </button>
        <div class="card-actions">
          <button class="mini spell">${it.family ? "Sound it" : "Spell it"}</button>
          ${sayLabel ? `<button class="mini say">${MIC}<span>${sayLabel}</span></button>` : ""}
          ${it.letter ? `<a class="mini" href="#/write/${i}">Write</a>` : ""}
        </div>
        <p class="say-msg" aria-live="polite"></p>
      </div>`;
    const cards = lesson.families
      ? lesson.families
          .map(
            (f) =>
              `<button class="family-head" style="${theme(lesson)}" data-rime="${f.rime}" aria-label="Hear the ${f.rime} family">-${f.rime}</button>` +
              lesson.items.map((it, i) => (it.family === f.rime ? cardHtml(it, i) : "")).join("")
          )
          .join("")
      : lesson.items.map(cardHtml).join("");
    const spellBtn = spellable(lesson).length >= 3 ? `<a class="btn primary" href="#/spell/${lesson.id}">Spell game</a>` : "";
    const buildBtn = buildable(lesson).length >= 3 ? `<a class="btn primary" href="#/build/${lesson.id}">Build a sentence</a>` : "";
    const doBtn = lesson.pipSays ? `<a class="btn primary" href="#/do/${lesson.id}">Pip says</a>` : "";
    const g = mainGame(lesson);
    const tip = lesson.tip ? `<p class="tip">${lesson.tip}${zhLine(lesson.tipZh, "zh-sub")}</p>` : "";
    app.innerHTML = `
      ${backToIsle(lesson.id)}
      <section class="lesson-head" style="${theme(lesson)}">
        <div class="head-main">
          <span class="head-pip" aria-hidden="true">${ART._pip}</span>
          <div><h1>${lesson.title}</h1><p>Tap a card to hear it. Tap “Say it” and say the word.</p>${tip}</div>
        </div>
        <div class="tile-actions"><a class="btn primary" href="#/${g.view}/${lesson.id}">${g.label} game</a>${spellBtn}${buildBtn}${doBtn}</div>
      </section>
      <div class="cards">${cards}</div>`;

    app.querySelectorAll(".card").forEach((card) => {
      const it = lesson.items[card.dataset.i];
      const main = card.querySelector(".card-main");
      main.addEventListener("click", () => {
        bounce(main);
        if (it.move) bounce(main.querySelector(".card-art"), "move-" + it.move);
        Speech.say([it.word, it.sentence], { gap: 350 });
      });
      card.querySelector(".spell").addEventListener("click", () => (it.family ? soundOut(card, it, lesson) : spellOut(card, it)));
      const sayBtn = card.querySelector(".say");
      if (sayBtn) sayBtn.addEventListener("click", () => sayIt(card, sayBtn, it, lesson));
    });
    // Tapping a family heading chants the family: "at: cat, hat, bat, mat".
    app.querySelectorAll(".family-head").forEach((h) =>
      h.addEventListener("click", () => {
        bounce(h);
        const rime = h.dataset.rime;
        Speech.say([rimeSound(lesson, rime), ...lesson.items.filter((it) => it.family === rime).map((it) => it.word)], { gap: 300 });
      })
    );
  }

  // One span per letter (for "Spell it"). In "two apples" the plural ending is marked so it can be highlighted,
  // and in phonics words the first sound ("b" in "bat").
  function wordLetters(it) {
    const at = it.count > 1 ? it.word.lastIndexOf(it.thing) : -1;
    const ending = at >= 0 ? at + it.thing.length : it.word.length;
    const onset = it.family ? onsetOf(it).length : 0;
    return it.word
      .split("")
      .map((c, k) =>
        /[a-z]/i.test(c)
          ? `<span class="l${k >= ending ? " plural" : ""}${k < onset ? " onset" : ""}">${c}</span>`
          : c === " "
          ? "&nbsp;"
          : c
      )
      .join("");
  }

  // "Sound it": the first sound, then the family ending, then the whole word (buh… at… bat).
  function soundOut(card, it, lesson) {
    const letters = [...card.querySelectorAll(".word .l")];
    const n = onsetOf(it).length;
    const show = (from, to) => letters.forEach((s, k) => s.classList.toggle("on", k >= from && k < to));
    Speech.say([onsetSound(onsetOf(it)), rimeSound(lesson, it.family), it.word], {
      gap: 350,
      onPart: (k) => (k === 0 ? show(0, n) : k === 1 ? show(n, letters.length) : show(0, letters.length)),
    }).then(() => setTimeout(() => show(0, 0), 400));
  }

  function spellOut(card, it) {
    const letters = [...card.querySelectorAll(".word .l")];
    const clear = () => letters.forEach((s) => s.classList.remove("on"));
    Speech.say([...letters.map((s) => s.textContent), it.word], {
      gap: 180,
      onPart: (k) => {
        clear();
        if (k < letters.length) letters[k].classList.add("on");
        else letters.forEach((s) => s.classList.add("on"));
      },
    }).then(() => setTimeout(clear, 400));
  }

  let busy = false;
  async function sayIt(card, btn, it, lesson) {
    if (busy) return;
    busy = true;
    const msg = card.querySelector(".say-msg");
    const label = btn.querySelector("span");
    const setState = (state, text) => {
      btn.classList.toggle("listening", state === "listening");
      label.textContent = state === "listening" ? "Listening…" : "Say it";
      msg.className = "say-msg " + (state === "good" ? "good" : state === "retry" ? "retry" : "");
      msg.innerHTML = text || "";
    };
    try {
      if (Speech.canListen) {
        await Speech.say(it.word);
        setState("listening", "Now you say it!" + zhLine("现在你来说！", "zh-sub"));
        const r = await Speech.listen();
        if (r.heard && Speech.matches(r.heard, it)) {
          setState("good", "★ " + praise());
          card.classList.add("said");
          bounce(card, "pop");
          celebrate(card.querySelector(".card-art"), 18);
          markSaid(lesson.id, it.word);
          await Speech.say([praise(), it.word], { gap: 200 });
        } else if (r.heard) {
          setState("retry", `I heard “${esc(r.heard[0])}”. Try again!` + zhLine("再试一次！", "zh-sub"));
          await Speech.say(["Try again.", it.word], { gap: 250 });
        } else if (r.error === "not-allowed" || r.error === "service-not-allowed") {
          setState("retry", "Please allow the microphone." + zhLine("请允许使用麦克风。", "zh-sub"));
        } else if (r.error === "network") {
          setState("retry", "Speech check needs the internet." + zhLine("跟读检查需要联网。", "zh-sub"));
        } else {
          setState("retry", "I didn't hear you. Try again!" + zhLine("没听到，再试一次！", "zh-sub"));
        }
      } else {
        // No recognition (e.g. Safari/Firefox): record, then compare by ear.
        await Speech.say(it.word);
        setState("listening", "Now you say it!");
        const url = await Speech.record(2500);
        setState("", "Listen: first the teacher, then you.");
        await Speech.say(it.word);
        await new Promise((res) => {
          const a = new Audio(url);
          a.onended = a.onerror = res;
          a.play().catch(res);
        });
        setState("", "Do they sound the same?" + zhLine("听起来一样吗？", "zh-sub"));
      }
    } catch (err) {
      setState("retry", "Please allow the microphone." + zhLine("请允许使用麦克风。", "zh-sub"));
    } finally {
      busy = false;
    }
  }

  LE.views.learn = learn;
})();
