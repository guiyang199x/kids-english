// Listen game: hear a word (or sentence), tap its picture.
(function () {
  const { ROUNDS } = LE.lesson;
  const { app, bounce, celebrate, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { results } = LE.games;

  function play(lesson) {
    const rounds = shuffle(lesson.items).slice(0, ROUNDS);
    const nOptions = lesson.items.length >= 6 ? 4 : 3;
    let round = 0;
    let score = 0;
    let firstTry = true;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <button class="btn primary listen">▶ Listen again</button>
        <div class="options"></div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const prompt = () =>
      lesson.askSentence ? Speech.say(rounds[round].sentence) : Speech.say(["Tap", rounds[round].word], { gap: 60 });
    $(".listen").addEventListener("click", prompt);

    function showRound() {
      const target = rounds[round];
      const others = shuffle(lesson.items.filter((x) => x !== target)).slice(0, nOptions - 1);
      const opts = shuffle([target, ...others]);
      firstTry = true;
      locked = false;
      $(".progress").innerHTML = progress("Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".options").innerHTML = opts
        .map((o) => `<button class="option" data-word="${o.word}" aria-label="${o.word}">${pic(o)}</button>`)
        .join("");
      $(".options").querySelectorAll(".option").forEach((b) => b.addEventListener("click", () => choose(b)));
      prompt();
    }

    function choose(btn) {
      if (locked) return;
      const target = rounds[round];
      if (btn.dataset.word === target.word) {
        locked = true;
        if (firstTry) score++;
        btn.classList.add("right");
        btn.insertAdjacentHTML("beforeend", `<span class="option-word">${target.word}${zhLine(target.zh)}</span>`);
        celebrate(btn);
        $(".score").innerHTML = stars(score, rounds.length);
        Speech.say([praise(), target.sentence], { gap: 250 }).then(() => {
          round++;
          round < rounds.length ? showRound() : finish();
        });
      } else {
        firstTry = false;
        bounce(btn, "wrong");
        if (lesson.askSentence) {
          const picked = lesson.items.find((x) => x.word === btn.dataset.word);
          Speech.say([picked.sentence, "Try again.", target.sentence], { gap: 250 });
        } else {
          Speech.say(["That is " + btn.dataset.word + ".", "Try again. Tap " + target.word + "."], { gap: 200 });
        }
      }
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: lesson.id,
        lesson,
        again: () => play(lesson),
        note: `You got ${score} of ${rounds.length} on the first try.`,
      });

    showRound();
  }

  LE.games.play = play;
})();
