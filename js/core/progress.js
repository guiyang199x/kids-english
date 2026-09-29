// What the child has done: best scores, words said, letters written, and the stars each stop shows.
(function () {
  const { buildable, lessonById, mainGame, ROUNDS, spellable } = LE.lesson;

  const bestScore = Store.best;

  const said = Store.said;
  const markSaid = (lessonId, word) => said.add(lessonId + ":" + word);
  const saidCount = (lesson) => lesson.items.filter((it) => said.has(lesson.id + ":" + it.word)).length;
  const written = Store.written;
  const markWritten = (ch) => written.add(ch);

  // 0 to 3 stars for a stop: how much of the best game scores (for Write: of the 52 letters) is done.
  // The picture dictionary has no score, so it gets none (null).
  function stopStars(id) {
    const l = lessonById(id);
    let done;
    if (l) {
      const keys = [mainGame(l).key];
      if (spellable(l).length >= 3) keys.push("spell-" + l.id);
      if (buildable(l).length >= 3) keys.push("build-" + l.id);
      // Moves (act) can't go wrong, so they'd hand out free stars.
      if (l.pipSays && l.pipSays.type !== "act") keys.push("do-" + l.id);
      done = keys.reduce((sum, k) => sum + bestScore(k), 0) / (keys.length * ROUNDS);
    } else if (id === "write") done = written.size / 52;
    else return null;
    return done >= 0.9 ? 3 : done >= 0.5 ? 2 : done > 0 ? 1 : 0;
  }

  LE.progress = { bestScore, said, markSaid, saidCount, written, markWritten, stopStars };
})();
