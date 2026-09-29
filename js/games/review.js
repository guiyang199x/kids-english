// Review: today's due words from every lesson, in the listen game. A word missed the first time comes
// back once at the end. There's no best score; the results show which words got stronger.
(function () {
  const { dueWords, recordAnswer, REVIEW } = LE.progress;
  const { app, celebrate, pic, shuffle, theme, zhLine } = LE.ui;
  const { listenQuiz } = LE.games;

  const box = ({ lesson, it }) => (Store.words.get(lesson.id + ":" + it.word) || { box: 0 }).box;
  // A word's box as five dots, filled up to its box (4 and up is mastered).
  const levelDots = (n) =>
    `<span class="rw-level" aria-label="level ${n} of ${SRS.MAX_BOX}">${Array.from({ length: SRS.MAX_BOX }, (_, k) =>
      `<i class="${k < n ? "on" : ""}"></i>`
    ).join("")}</span>`;
  const page = (inner) => `
      <nav class="crumbs"><a href="#/">← Map</a></nav>
      <section class="quiz no-buddy" style="${theme(REVIEW)}">${inner}</section>`;

  function review() {
    const rounds = shuffle(dueWords(REVIEW.size));
    if (!rounds.length) {
      app.innerHTML = page(`
        <div class="done">
          <span class="done-pip" aria-hidden="true">${ART._pip_cheer}</span>
          <h1>All done!</h1>
          <p>No words to review today. Come back tomorrow!</p>
          ${zhLine("今天没有要复习的词，明天再来吧！", "zh-sub")}
          <div class="tile-actions"><a class="btn primary" href="#/">Back to the map</a></div>
        </div>`);
      return;
    }
    const before = rounds.map(box);
    listenQuiz({
      rounds,
      back: `<a href="#/">← Map</a>`,
      retry: true,
      onFirst: ({ lesson, it }, ok) => recordAnswer(lesson, it, ok ? "pass" : "miss"),
      onDone: (quiz) => done(quiz, rounds, before),
    });
  }

  function done(quiz, rounds, before) {
    const after = rounds.map(box);
    const up = rounds.filter((_, k) => after[k] > before[k]).length;
    const msg = up === rounds.length ? "Perfect!" : up * 2 >= rounds.length ? "Great work!" : "Good try!";
    const note = up
      ? `${up} ${up === 1 ? "word" : "words"} got stronger!` + zhLine(`${up} 个词记得更牢了！`, "zh-sub")
      : "These words will come back soon." + zhLine("这些词很快会再来找你。", "zh-sub");
    const more = dueWords(1).length > 0;
    app.querySelector(".buddy")?.remove();
    quiz.style.cssText = theme(REVIEW);
    quiz.innerHTML = `
      <div class="done">
        <span class="done-pip" aria-hidden="true">${up ? ART._pip_cheer : ART._pip}</span>
        <h1>${msg}</h1>
        <p>${note}</p>
        <ul class="review-words">${rounds
          .map(
            ({ it }, k) => `
          <li class="${after[k] > before[k] ? "up" : ""}">
            <span class="rw-pic" aria-hidden="true">${pic(it)}</span>
            <b>${it.word}</b>${zhLine(it.zh)}
            ${levelDots(after[k])}${after[k] > before[k] ? '<span class="rw-up" aria-label="stronger">↑</span>' : ""}
          </li>`
          )
          .join("")}
        </ul>
        <div class="tile-actions">
          <a class="btn${more ? "" : " primary"}" href="#/">Back to the map</a>
          ${more ? `<button class="btn primary again">More words</button>` : ""}
        </div>
      </div>`;
    quiz.querySelector(".again")?.addEventListener("click", review);
    if (up) celebrate(quiz.querySelector("h1"), 20 + up * 6);
    Speech.say(msg);
  }

  LE.games.review = review;
})();
