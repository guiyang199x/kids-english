// Build game: put the words of a sentence in order.
(function () {
  const { buildable, ROUNDS, sentenceTiles } = LE.lesson;
  const { app, bounce, celebrate, esc, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { recordAnswer } = LE.progress;
  const { results } = LE.games;

  function buildGame(lesson) {
    const pool = buildable(lesson);
    const rounds = shuffle(pool).slice(0, Math.min(ROUNDS, pool.length));
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz buildgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="spell-pic"></div>
        <div class="wslots" aria-live="polite"></div>
        <div class="word-tiles"></div>
        <div class="tile-actions">
          <button class="btn hear">▶ Hear it</button>
          <button class="btn hint">Hint</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const it = rounds[round];
      const { words, end } = sentenceTiles(it);
      // One extra tile, so the picture decides which word fits: another card's word,
      // or for counting items the other form of the noun ("car" next to "cars").
      const lower = words.map((w) => w.toLowerCase());
      const other = shuffle(lesson.items).find((x) => x !== it && !lower.includes(x.word.toLowerCase()));
      const plural = it.count && (window.COUNT_THINGS.find((t) => t.word === it.thing) || {}).plural;
      const extra = it.count ? (it.count === 1 ? plural : it.thing) : other && other.word;
      const tiles = shuffle(extra ? [...words, extra] : words);
      let pos = 0;
      let perfect = true;
      let locked = false;

      $(".progress").innerHTML = progress("Sentence", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".spell-pic").innerHTML = pic(it) + zhLine(it.zh);
      $(".wslots").innerHTML = words.map(() => `<span class="wslot"></span>`).join("") + `<span class="wend">${end}</span>`;
      $(".word-tiles").innerHTML = tiles.map((w) => `<button class="wtile">${esc(w)}</button>`).join("");
      const slots = [...app.querySelectorAll(".wslot")];
      slots[0].classList.add("next");

      app.querySelectorAll(".wtile").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.disabled) return;
          if (t.textContent === words[pos]) {
            t.disabled = true;
            t.classList.add("used");
            slots[pos].textContent = words[pos];
            slots[pos].classList.remove("next");
            slots[pos].classList.add("filled");
            pos++;
            if (pos < words.length) {
              slots[pos].classList.add("next");
              Speech.say(t.textContent);
            } else {
              locked = true;
              if (perfect) score++;
              recordAnswer(lesson, it, perfect ? "pass" : "soft");
              $(".score").innerHTML = stars(score, rounds.length);
              bounce($(".wslots"), "pop");
              celebrate($(".wslots"));
              app.querySelectorAll(".wtile:not(.used)").forEach((x) => x.classList.add("leftover"));
              if (it.sentenceZh) $(".wslots").insertAdjacentHTML("beforeend", zhLine(it.sentenceZh, "zh-sub"));
              Speech.say([it.sentence, praise()], { gap: 300 }).then(() => {
                round++;
                round < rounds.length ? showRound() : finish();
              });
            }
          } else {
            perfect = false;
            bounce(t, "wrong");
            Speech.say(t.textContent);
          }
        })
      );
      $(".hear").onclick = () => Speech.say(it.sentence);
      $(".hint").onclick = () => {
        if (locked) return;
        perfect = false;
        const tile = [...app.querySelectorAll(".wtile:not(.used)")].find((x) => x.textContent === words[pos]);
        if (tile) bounce(tile, "glow");
        Speech.say(words[pos]);
      };
      Speech.say(it.sentence);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "build-" + lesson.id,
        lesson,
        again: () => buildGame(lesson),
        note: `You built ${score} of ${rounds.length} sentences with no mistakes.`,
      });

    showRound();
  }

  LE.games.buildGame = buildGame;
})();
