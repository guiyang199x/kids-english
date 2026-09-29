// Spell game: tap the letter tiles in order.
(function () {
  const { ROUNDS, spellable } = LE.lesson;
  const { app, bounce, celebrate, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { recordAnswer } = LE.progress;
  const { results } = LE.games;

  function spellGame(lesson) {
    const pool = spellable(lesson);
    const rounds = shuffle(pool).slice(0, Math.min(ROUNDS, pool.length));
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz spellgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="slots" aria-live="polite"></div>
        <div class="letter-tiles"></div>
        <div class="tile-actions">
          <button class="btn hear">▶ Hear the word</button>
          <button class="btn hint">Hint</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const letters = it.word.split("");
      const abc = "abcdefghijklmnopqrstuvwxyz".split("").filter((c) => !letters.includes(c));
      const tiles = shuffle([...letters, ...shuffle(abc).slice(0, 2)]);
      let pos = 0;
      let perfect = true;
      let locked = false;

      $(".progress").innerHTML = progress("Word", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".slots").innerHTML = letters.map(() => `<span class="slot"></span>`).join("");
      $(".letter-tiles").innerHTML = tiles
        .map((c) => `<button class="ltile" data-c="${c}" aria-label="letter ${c}">${c}</button>`)
        .join("");
      const slots = [...app.querySelectorAll(".slot")];
      slots[0].classList.add("next");

      app.querySelectorAll(".ltile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.disabled) return;
          if (t.dataset.c === letters[pos]) {
            t.disabled = true;
            t.classList.add("used");
            slots[pos].textContent = letters[pos];
            slots[pos].classList.remove("next");
            slots[pos].classList.add("filled");
            pos++;
            if (pos < letters.length) {
              slots[pos].classList.add("next");
              Speech.say(t.dataset.c, { rateScale: 1.1 });
            } else {
              locked = true;
              if (perfect) score++;
              recordAnswer(lesson, it, perfect ? "pass" : "soft");
              $(".score").innerHTML = stars(score, rounds.length);
              bounce($(".slots"), "pop");
              celebrate($(".slots"));
              Speech.say([it.word, praise()], { gap: 250 }).then(() => {
                round++;
                round < rounds.length ? showRound() : finish();
              });
            }
          } else {
            perfect = false;
            bounce(t, "wrong");
            Speech.say(t.dataset.c);
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.word);
      $(".hint").onclick = () => {
        if (locked) return;
        perfect = false;
        const tile = [...app.querySelectorAll(".ltile:not(.used)")].find((x) => x.dataset.c === letters[pos]);
        if (tile) bounce(tile, "glow");
        Speech.say(letters[pos]);
      };
      Speech.say(["Spell", it.word], { gap: 80 });
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "spell-" + lesson.id,
        lesson,
        again: () => spellGame(lesson),
        note: `You spelled ${score} of ${rounds.length} with no mistakes.`,
      });

    showRound();
  }

  LE.games.spellGame = spellGame;
})();
