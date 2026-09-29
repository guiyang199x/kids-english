// Blend game (phonics): the ending is there, pick the first sound.
(function () {
  const { onsetOf, onsetSound, rimeSound, ROUNDS } = LE.lesson;
  const { app, bounce, celebrate, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { pickRounds, recordAnswer } = LE.progress;
  const { results } = LE.games;

  function blendGame(lesson) {
    const rounds = pickRounds(lesson, lesson.items, ROUNDS);
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz blendgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="blend-word" aria-live="polite"></div>
        <p class="count-msg"></p>
        <div class="letter-tiles"></div>
        <button class="btn hear">▶ Hear it</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const rime = it.family;
      const family = lesson.items.filter((x) => x.family === rime);
      // Every choice makes a real word in the family, so a wrong pick is a rhyming word to hear.
      const choices = shuffle(family.map(onsetOf));
      let firstTry = true;
      let locked = false;

      $(".progress").innerHTML = progress("Word", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".blend-word").innerHTML = `<span class="slot bslot next"></span><span class="rime">${rime}</span>`;
      const msg = $(".count-msg");
      msg.className = "count-msg";
      msg.innerHTML = "What is the first sound?" + zhLine("第一个音是什么？", "zh-sub");
      $(".letter-tiles").innerHTML = choices
        .map((o) => `<button class="ltile otile" data-o="${o}" aria-label="${o}">${o}</button>`)
        .join("");
      const slot = $(".bslot");

      app.querySelectorAll(".otile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked) return;
          const o = t.dataset.o;
          const made = family.find((x) => onsetOf(x) === o);
          slot.textContent = o;
          if (firstTry) recordAnswer(lesson, it, made === it ? "pass" : "miss");
          if (made === it) {
            locked = true;
            if (firstTry) score++;
            slot.classList.remove("next", "wrongword");
            slot.classList.add("filled");
            t.classList.add("used");
            $(".score").innerHTML = stars(score, rounds.length);
            msg.className = "count-msg good";
            msg.innerHTML = `★ ${o}-${rime}, ${it.word}!`;
            bounce($(".blend-word"), "pop");
            celebrate($(".blend-word"));
            Speech.say([onsetSound(o), rimeSound(lesson, rime), it.word, praise()], { gap: 300 }).then(() => {
              round++;
              round < rounds.length ? showRound() : finish();
            });
          } else {
            firstTry = false;
            locked = true;
            slot.classList.add("wrongword");
            bounce(t, "wrong");
            msg.className = "count-msg retry";
            msg.innerHTML = `That says “${made.word}”. Find “${it.word}”!` + zhLine(`这是 ${made.word}，再找找 ${it.word}！`, "zh-sub");
            Speech.say(["That says " + made.word + ".", "Find " + it.word + "."], { gap: 250 }).then(() => {
              if (rounds[round] !== it) return;
              locked = false;
              slot.textContent = "";
              slot.classList.remove("wrongword");
            });
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.word);
      Speech.say(it.word);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "blend-" + lesson.id,
        lesson,
        again: () => blendGame(lesson),
        note: `You found ${score} of ${rounds.length} first sounds on the first try.`,
      });

    showRound();
  }

  LE.games.blendGame = blendGame;
})();
