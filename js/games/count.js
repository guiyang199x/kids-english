// Count game: count the pictures, tap the number.
(function () {
  const { NUMBERS, ROUNDS, ZH_NUMBERS } = LE.lesson;
  const { app, bounce, celebrate, many, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { results } = LE.games;

  function countGame(lesson) {
    const things = shuffle(window.COUNT_THINGS).slice(0, ROUNDS);
    const counts = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).slice(0, ROUNDS);
    let round = 0;
    let score = 0;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz countgame" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <div class="count-pic"></div>
        <p class="count-msg" aria-live="polite"></p>
        <div class="num-options"></div>
        <button class="btn listen">▶ Listen again</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);

    function showRound() {
      const thing = things[round];
      const n = counts[round];
      const name = (k) => (k === 1 ? thing.word : thing.plural);
      const near = shuffle([n - 2, n - 1, n + 1, n + 2].filter((k) => k >= 1 && k <= 10));
      const opts = shuffle([n, ...near.slice(0, 2)]);
      let tapped = 0;
      let firstTry = true;
      let locked = false;
      const msg = $(".count-msg");
      const setMsg = (cls, html) => {
        msg.className = "count-msg " + cls;
        msg.innerHTML = html;
      };

      $(".progress").innerHTML = progress("Question", round, ROUNDS);
      $(".score").innerHTML = stars(score, ROUNDS);
      $(".count-pic").innerHTML = many(thing.word, n, 320, 150);
      setMsg("", `How many ${thing.plural}? Tap each one to count.` + zhLine("有几个？点一点，数一数。", "zh-sub"));
      $(".num-options").innerHTML = opts
        .map((k) => `<button class="num" data-n="${k}" aria-label="${NUMBERS[k - 1]}">${k}</button>`)
        .join("");

      // Tapping a picture counts it out loud and puts a number on it.
      const svg = $(".count-pic svg");
      const clearCount = () => {
        tapped = 0;
        svg.querySelectorAll(".count-badge").forEach((b) => b.remove());
        svg.querySelectorAll(".thing").forEach((t) => t.classList.remove("counted"));
      };
      svg.querySelectorAll(".thing").forEach((t) =>
        t.addEventListener("click", () => {
          if (locked || t.classList.contains("counted")) return;
          tapped++;
          t.classList.add("counted");
          const { x, y, r } = t.dataset;
          t.insertAdjacentHTML(
            "afterend",
            `<g class="count-badge"><circle cx="${x - r * 1.2}" cy="${+y + r * 1.2}" r="${r}"/>` +
              `<text x="${x - r * 1.2}" y="${+y + r * 1.2}" font-size="${r * 1.3}" text-anchor="middle" dominant-baseline="central">${tapped}</text></g>`
          );
          Speech.say(NUMBERS[tapped - 1], { rateScale: 1.1 });
        })
      );

      app.querySelectorAll(".num").forEach((b) =>
        b.addEventListener("click", () => {
          if (locked) return;
          const k = Number(b.dataset.n);
          if (k === n) {
            locked = true;
            if (firstTry) score++;
            b.classList.add("right");
            $(".score").innerHTML = stars(score, ROUNDS);
            const phrase = `${NUMBERS[n - 1]} ${name(n)}`;
            setMsg("good", `★ ${n} ${name(n)}` + zhLine(ZH_NUMBERS[n - 1] + thing.unit + thing.zh, "zh-sub"));
            bounce($(".count-pic"), "pop");
            celebrate(b);
            Speech.say([phrase[0].toUpperCase() + phrase.slice(1) + "!", praise()], { gap: 250 }).then(() => {
              round++;
              round < ROUNDS ? showRound() : finish();
            });
          } else {
            firstTry = false;
            bounce(b, "wrong");
            clearCount();
            setMsg("retry", "Let's count again! Tap each one." + zhLine("我们再数一遍！一个一个点。", "zh-sub"));
            Speech.say([NUMBERS[k - 1] + "?", "Let's count again."], { gap: 200 });
          }
        })
      );
      $(".listen").onclick = () => Speech.say(`How many ${thing.plural}?`);
      Speech.say(`How many ${thing.plural}?`);
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: ROUNDS,
        key: "count-" + lesson.id,
        lesson,
        again: () => countGame(lesson),
        note: `You counted ${score} of ${ROUNDS} right on the first try.`,
      });

    showRound();
  }

  LE.games.countGame = countGame;
})();
