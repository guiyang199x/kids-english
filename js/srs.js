// Spaced review: when each word should come back, from how the child answered it (Leitner boxes).
// Pure functions only (no page, no storage), so tests can run them in Node. Store.words keeps the entries.
//
// An entry is { box, due, right, wrong }:
//   box   0-5, one step up for each right answer on a due day, back to 0 for a wrong one
//   due   the day (see today()) it should be reviewed; after a pass from box b it's 2^b days away (1, 2, 4 ... 32)
//   right / wrong   how often it was answered each way, for reports
(function () {
  const MAX_BOX = 5;
  const MASTERED = 4; // box 4 means it was remembered after gaps of 1, 2 and 4 days
  const DAY = 86400000;

  // Days since 1970 by the local calendar, so a new day starts at the child's midnight, not UTC's.
  const today = (now = Date.now()) => {
    const t = +now;
    return Math.floor((t - new Date(t).getTimezoneOffset() * 60000) / DAY);
  };

  const num = (v, def) => (Number.isFinite(v) ? v : def);
  // Saved entries come from localStorage, so anything missing or broken falls back to a new word.
  const clean = (e, day) => {
    e = e && typeof e === "object" ? e : {};
    return {
      box: Math.min(MAX_BOX, Math.max(0, Math.floor(num(e.box, 0)))),
      due: num(e.due, day),
      right: num(e.right, 0),
      wrong: num(e.wrong, 0),
    };
  };

  // "pass": right first time. Moves up a box only if the word was due, so replaying a lesson can't
  //         rush a word to mastered in one afternoon.
  // "miss": wrong. Back to box 0 and due again today.
  // "soft": got there with a slip or a hint (spelling, sentence building). Knowing a word but not
  //         its spelling isn't forgetting it, so this never moves it down; a new word starts at box 0.
  function grade(entry, outcome, day) {
    const e = clean(entry, day);
    if (outcome === "pass") {
      e.right++;
      if (e.due <= day) {
        e.due = day + 2 ** e.box;
        e.box = Math.min(MAX_BOX, e.box + 1);
      }
    } else if (outcome === "miss") {
      e.wrong++;
      e.box = 0;
      e.due = day;
    } else if (outcome !== "soft") {
      throw new Error("Unknown outcome: " + outcome);
    }
    return e;
  }

  // Keys of the words due by `day`, the shakiest first: lowest box, then longest overdue, then most missed.
  function due(entries, day, limit = Infinity) {
    return Object.keys(entries || {})
      .map((key) => ({ key, e: clean(entries[key], day) }))
      .filter(({ e }) => e.due <= day)
      .sort((a, b) => a.e.box - b.e.box || a.e.due - b.e.due || b.e.wrong - a.e.wrong || (a.key < b.key ? -1 : 1))
      .slice(0, limit)
      .map(({ key }) => key);
  }

  const level = (entry) => (!entry ? "new" : clean(entry, 0).box >= MASTERED ? "mastered" : "learning");

  const SRS = { MAX_BOX, MASTERED, today, grade, due, level };
  if (typeof module === "object" && module.exports) module.exports = SRS;
  else window.SRS = SRS;
})();
