// Listen game: hear a word (or sentence), tap its picture.
(function () {
  const { likeness, ROUNDS } = LE.lesson;
  const { pickRounds, recordAnswer, tier } = LE.progress;
  const { app, bounce, celebrate, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { results } = LE.games;

  // The game itself. Rounds are { lesson, it }, so a review can mix lessons: each round takes its colors,
  // its question and the other pictures from its own lesson. onFirst(round, ok) hears each round's first
  // answer. With `retry`, a round missed the first time comes back once at the end.
  // onDone(box, score, total) shows the results in `box`.
  function listenQuiz({ rounds, back, onFirst, retry, onDone }) {
    rounds = rounds.slice();
    let round = 0;
    let score = 0;
    let firstTry = true;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs">${back}</nav>
      <section class="quiz">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <button class="btn primary listen">▶ Listen again</button>
        <div class="options"></div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const prompt = () => {
      const { lesson, it } = rounds[round];
      return lesson.askSentence ? Speech.say(it.sentence) : Speech.say(["Tap", it.word], { gap: 60 });
    };
    $(".listen").addEventListener("click", prompt);

    function showRound() {
      const { lesson, it: target } = rounds[round];
      // 3 pictures for a word that's new or was just missed, 4 once it's known (if the lesson has 6 or more),
      // and for a mastered word the other pictures are the words most like it (hat and bat for cat).
      const level = tier(lesson, target);
      const nOptions = lesson.items.length >= 6 && level !== "easy" ? 4 : 3;
      let others = shuffle(lesson.items.filter((x) => x !== target));
      if (level === "hard") others.sort((x, y) => likeness(y.word, target.word) - likeness(x.word, target.word));
      others = others.slice(0, nOptions - 1);
      const opts = shuffle([target, ...others]);
      firstTry = true;
      locked = false;
      $(".quiz").style.cssText = theme(lesson);
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
      const { lesson, it: target } = rounds[round];
      const ok = btn.dataset.word === target.word;
      if (firstTry) {
        onFirst(rounds[round], ok);
        if (!ok && retry && !rounds[round].again) rounds.push({ ...rounds[round], again: true });
      }
      if (ok) {
        locked = true;
        if (firstTry) score++;
        btn.classList.add("right");
        btn.insertAdjacentHTML("beforeend", `<span class="option-word">${target.word}${zhLine(target.zh)}</span>`);
        celebrate(btn);
        $(".score").innerHTML = stars(score, rounds.length);
        Speech.say([praise(), target.sentence], { gap: 250 }).then(() => {
          round++;
          round < rounds.length ? showRound() : onDone($(".quiz"), score, rounds.length);
        });
      } else {
        firstTry = false;
        bounce(btn, "wrong");
        // A missed round coming back adds a dot.
        $(".progress").innerHTML = progress("Question", round, rounds.length);
        $(".score").innerHTML = stars(score, rounds.length);
        if (lesson.askSentence) {
          const picked = lesson.items.find((x) => x.word === btn.dataset.word);
          Speech.say([picked.sentence, "Try again.", target.sentence], { gap: 250 });
        } else {
          Speech.say(["That is " + btn.dataset.word + ".", "Try again. Tap " + target.word + "."], { gap: 200 });
        }
      }
    }

    showRound();
  }

  function play(lesson) {
    listenQuiz({
      rounds: pickRounds(lesson, lesson.items, ROUNDS).map((it) => ({ lesson, it })),
      back: `<a href="#/learn/${lesson.id}">← ${lesson.title}</a>`,
      onFirst: ({ it }, ok) => recordAnswer(lesson, it, ok ? "pass" : "miss"),
      onDone: (box, score, total) =>
        results(box, {
          score,
          total,
          key: lesson.id,
          lesson,
          again: () => play(lesson),
          note: `You got ${score} of ${total} on the first try.`,
        }),
    });
  }

  LE.games.listenQuiz = listenQuiz;
  LE.games.play = play;
})();
