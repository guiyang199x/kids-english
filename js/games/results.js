// The results screen every game ends on. It also saves the best score.
(function () {
  const { app, celebrate } = LE.ui;

  function results(box, { score, total, key, lesson, again, note }) {
    Store.saveBest(key, score);
    const msg = score === total ? "Perfect!" : score >= 3 ? "Great work!" : "Good try!";
    // Stars pop in one at a time, the earned ones first.
    const bigStars = Array.from({ length: total }, (_, k) => `<i class="${k < score ? "" : "dim"}" style="--i:${k}">★</i>`).join("");
    app.querySelector(".buddy")?.remove();
    box.innerHTML = `
      <div class="done">
        <span class="done-pip" aria-hidden="true">${score >= 3 ? ART._pip_cheer : ART._pip}</span>
        <h1>${msg}</h1>
        <p class="big-stars"><span class="stars" aria-label="${score} of ${total} stars">${bigStars}</span></p>
        <p>${note}</p>
        <div class="tile-actions">
          <a class="btn" href="#/learn/${lesson.id}">Learn again</a>
          <button class="btn primary again">Play again</button>
        </div>
      </div>`;
    box.querySelector(".again").addEventListener("click", again);
    if (score) celebrate(box.querySelector(".big-stars"), 20 + score * 8);
    Speech.say(msg);
  }

  LE.games.results = results;
})();
