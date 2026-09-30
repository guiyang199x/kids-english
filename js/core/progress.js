// What the child has done: best scores, words said, letters written, and the stars each stop shows.
(function () {
  const { buildable, LEVELS, lessonById, mainGame, ROUNDS, seasonal, spellable } = LE.lesson;

  const bestScore = Store.best;

  const said = Store.said;
  const markSaid = (lessonId, word) => said.add(lessonId + ":" + word);
  const saidCount = (lesson) => lesson.items.filter((it) => said.has(lesson.id + ":" + it.word)).length;
  const written = Store.written;
  const markWritten = (ch) => written.add(ch);

  // An answer that shows whether the child knows one word goes into its review schedule (js/srs.js):
  // "pass" right first time, "miss" wrong first time, "soft" got there with a slip or a hint.
  const recordAnswer = (lesson, it, outcome) => Store.words.record(lesson.id + ":" + it.word, outcome);

  // How hard to make a question about one word: "easy" while it's new or was just missed (box 0), "hard" once
  // it's mastered, "normal" in between. The games use it for the number of choices, extra tiles and help.
  const boxOf = (lesson, it) => (Store.words.get(lesson.id + ":" + it.word) || { box: 0 }).box;
  function tier(lesson, it) {
    const box = boxOf(lesson, it);
    return box === 0 ? "easy" : box >= SRS.MASTERED ? "hard" : "normal";
  }
  // n of a lesson's items for one game, the least known first (ties at random), in a random order.
  function pickRounds(lesson, items, n) {
    const { shuffle } = LE.ui;
    return shuffle(shuffle(items).sort((a, b) => boxOf(lesson, a) - boxOf(lesson, b)).slice(0, n));
  }

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

  // 0 to 3 stars for a stop: how much of the best game scores (for Write: of the 52 letters) is done. A picture
  // dictionary's come from its Find it game. Yes or No doesn't count: it came later, and counting it would take
  // stars away from lessons already played.
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
    else if (id.startsWith("scene-")) done = bestScore("find-" + id.slice(6)) / ROUNDS;
    else return null;
    return done >= 0.9 ? 3 : done >= 0.5 ? 2 : done > 0 ? 1 : 0;
  }

  // The child's level: where the grown-ups chose to start (the "Start at" setting), or higher once 70% of
  // the lessons at a level have 2 stars or more. `done` / `total` are those lessons at the child's level.
  // Seasonal lessons (the Ghost Ship's) don't count: they aren't there all year.
  const LEVEL_UP = 0.7;
  function childLevel() {
    const at = (n) => window.LESSONS.filter((l) => (l.level || 1) === n && !seasonal(l));
    const done = (n) => at(n).filter((l) => stopStars(l.id) >= 2).length;
    let n = 1;
    while (n < LEVELS.length && done(n) >= LEVEL_UP * at(n).length) n++;
    n = Math.max(n, Math.min(LEVELS.length, Number(Store.setting("level")) || 1));
    return { n, done: done(n), total: at(n).length };
  }

  LE.progress = { bestScore, said, markSaid, saidCount, written, markWritten, stopStars, recordAnswer, REVIEW, dueWords,
    childLevel, tier, pickRounds };
})();
