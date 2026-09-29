// What the child has done: best scores, words said, letters written, and the stars each stop shows.
(function () {
  const { buildable, LEVELS, lessonById, mainGame, ROUNDS, spellable } = LE.lesson;

  const bestScore = Store.best;

  const said = Store.said;
  const markSaid = (lessonId, word) => said.add(lessonId + ":" + word);
  const saidCount = (lesson) => lesson.items.filter((it) => said.has(lesson.id + ":" + it.word)).length;
  const written = Store.written;
  const markWritten = (ch) => written.add(ch);

  // An answer that shows whether the child knows one word goes into its review schedule (js/srs.js):
  // "pass" right first time, "miss" wrong first time, "soft" got there with a slip or a hint.
  const recordAnswer = (lesson, it, outcome) => Store.words.record(lesson.id + ":" + it.word, outcome);

  // Review: up to `size` words a go, offered on the map once `min` are due. It has its own color.
  const REVIEW = { size: 8, min: 3, color: "#8150c4", tint: "#f0e8fb" };
  // Today's due words as { lesson, it }, shakiest first. Words no longer in a lesson are skipped, and a
  // word in several lessons ("cat" is in three) comes once, so a review never asks the same thing twice.
  function dueWords(limit = Infinity) {
    const out = [];
    const words = new Set();
    for (const key of SRS.due(Store.words.all(), SRS.today())) {
      const cut = key.indexOf(":");
      const lesson = lessonById(key.slice(0, cut));
      const it = lesson && lesson.items.find((x) => x.word === key.slice(cut + 1));
      if (!it || words.has(it.word)) continue;
      words.add(it.word);
      out.push({ lesson, it });
      if (out.length >= limit) break;
    }
    return out;
  }

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

  // The child's level: where the grown-ups chose to start (the "Start at" setting), or higher once 70% of
  // the lessons at a level have 2 stars or more. `done` / `total` are those lessons at the child's level.
  const LEVEL_UP = 0.7;
  function childLevel() {
    const at = (n) => window.LESSONS.filter((l) => (l.level || 1) === n);
    const done = (n) => at(n).filter((l) => stopStars(l.id) >= 2).length;
    let n = 1;
    while (n < LEVELS.length && done(n) >= LEVEL_UP * at(n).length) n++;
    n = Math.max(n, Math.min(LEVELS.length, Number(Store.setting("level")) || 1));
    return { n, done: done(n), total: at(n).length };
  }

  LE.progress = { bestScore, said, markSaid, saidCount, written, markWritten, stopStars, recordAnswer, REVIEW, dueWords,
    childLevel };
})();
