// Run with: node --test
const test = require("node:test");
const assert = require("node:assert/strict");
const SRS = require("../js/srs.js");

const D = 20000; // any day number

test("a new word answered right goes to box 1, due tomorrow", () => {
  assert.deepEqual(SRS.grade(undefined, "pass", D), { box: 1, due: D + 1, right: 1, wrong: 0 });
});

test("a new word answered wrong stays in box 0, due today", () => {
  assert.deepEqual(SRS.grade(undefined, "miss", D), { box: 0, due: D, right: 0, wrong: 1 });
});

test("each pass on a due day doubles the gap: 1, 2, 4, 8, 16, then 32 days", () => {
  let e;
  let day = D;
  const gaps = [];
  for (let i = 0; i < 7; i++) {
    e = SRS.grade(e, "pass", day);
    gaps.push(e.due - day);
    day = e.due;
  }
  assert.deepEqual(gaps, [1, 2, 4, 8, 16, 32, 32]);
  assert.equal(e.box, SRS.MAX_BOX);
});

test("passing a word before it's due counts the answer but doesn't move it up", () => {
  const e = { box: 2, due: D + 3, right: 4, wrong: 0 };
  assert.deepEqual(SRS.grade(e, "pass", D), { box: 2, due: D + 3, right: 5, wrong: 0 });
});

test("replaying a lesson all afternoon can't rush a word to mastered", () => {
  let e;
  for (let i = 0; i < 10; i++) e = SRS.grade(e, "pass", D);
  assert.equal(e.box, 1);
  assert.equal(SRS.level(e), "learning");
});

test("an overdue word passed late gets its gap from today, not from when it was due", () => {
  const e = SRS.grade({ box: 2, due: D - 10, right: 2, wrong: 0 }, "pass", D);
  assert.deepEqual(e, { box: 3, due: D + 4, right: 3, wrong: 0 });
});

test("a miss sends even a mastered word back to box 0, due today", () => {
  const e = SRS.grade({ box: 5, due: D + 20, right: 9, wrong: 0 }, "miss", D);
  assert.deepEqual(e, { box: 0, due: D, right: 9, wrong: 1 });
});

test("a soft answer never moves a word or changes its date", () => {
  const e = { box: 3, due: D, right: 3, wrong: 1 };
  assert.deepEqual(SRS.grade(e, "soft", D), e);
  assert.deepEqual(SRS.grade(undefined, "soft", D), { box: 0, due: D, right: 0, wrong: 0 });
});

test("grade doesn't change the entry it's given", () => {
  const e = { box: 1, due: D, right: 1, wrong: 0 };
  SRS.grade(e, "pass", D);
  SRS.grade(e, "miss", D);
  assert.deepEqual(e, { box: 1, due: D, right: 1, wrong: 0 });
});

test("an unknown outcome is an error, not a silent no-op", () => {
  assert.throws(() => SRS.grade(undefined, "right", D), /Unknown outcome/);
});

test("broken saved entries are treated as a new word", () => {
  assert.deepEqual(SRS.grade("junk", "pass", D), { box: 1, due: D + 1, right: 1, wrong: 0 });
  assert.deepEqual(SRS.grade({ box: "x", due: null }, "pass", D), { box: 1, due: D + 1, right: 1, wrong: 0 });
  assert.deepEqual(SRS.grade({ box: 99, due: D }, "pass", D).box, SRS.MAX_BOX);
  assert.deepEqual(SRS.grade({ box: -3, due: D }, "pass", D).box, 1);
});

test("due lists only words due by today, shakiest first", () => {
  const entries = {
    "a:later": { box: 0, due: D + 1, right: 0, wrong: 3 },
    "a:box2": { box: 2, due: D - 5, right: 2, wrong: 0 },
    "a:box0-new": { box: 0, due: D, right: 0, wrong: 1 },
    "a:box0-old": { box: 0, due: D - 2, right: 0, wrong: 1 },
    "a:box0-missed-more": { box: 0, due: D, right: 0, wrong: 4 },
    "a:box1": { box: 1, due: D, right: 1, wrong: 0 },
  };
  assert.deepEqual(SRS.due(entries, D), ["a:box0-old", "a:box0-missed-more", "a:box0-new", "a:box1", "a:box2"]);
});

test("due stops at the limit and copes with nothing saved", () => {
  const entries = {};
  for (let i = 0; i < 20; i++) entries["a:w" + String(i).padStart(2, "0")] = { box: 1, due: D, right: 1, wrong: 0 };
  assert.equal(SRS.due(entries, D, 8).length, 8);
  assert.deepEqual(SRS.due({}, D, 8), []);
  assert.deepEqual(SRS.due(undefined, D), []);
});

test("level: new, learning, then mastered from box 4", () => {
  assert.equal(SRS.level(undefined), "new");
  assert.equal(SRS.level({ box: 0 }), "learning");
  assert.equal(SRS.level({ box: 3 }), "learning");
  assert.equal(SRS.level({ box: 4 }), "mastered");
  assert.equal(SRS.level({ box: 5 }), "mastered");
});

test("today follows the local calendar: a new day starts at local midnight", () => {
  const lateNight = new Date(2026, 8, 29, 23, 59);
  const earlyMorning = new Date(2026, 8, 30, 0, 1);
  const morning = new Date(2026, 8, 29, 0, 1);
  assert.equal(SRS.today(earlyMorning) - SRS.today(lateNight), 1);
  assert.equal(SRS.today(lateNight), SRS.today(morning));
  assert.ok(Number.isInteger(SRS.today()));
});
