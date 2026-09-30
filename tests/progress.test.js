// Run with: node --test
// Loads the real lessons and islands with srs.js, store.js, core/ and views/map.js, with a fake localStorage.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["content/data.js", "content/islands.js", "content/visits.js", "srs.js", "store.js", "core/lesson.js", "core/progress.js",
  "core/ui.js", "views/map.js"];
const src = (f) => fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8");
// Objects made inside the fake page have that page's prototypes, so compare plain copies.
const plain = (v) => JSON.parse(JSON.stringify(v));

// A fresh page load. `words` is the saved review schedule to start from; `settings` e.g. { level: "2" }.
function load(words, settings = {}) {
  const data = new Map([["le-version", "2"]]);
  if (words) data.set("le-words", JSON.stringify(words));
  for (const [k, v] of Object.entries(settings)) data.set("le-" + k, v);
  const localStorage = {
    getItem: (k) => (data.has(k) ? data.get(k) : null),
    setItem: (k, v) => data.set(k, String(v)),
    removeItem: (k) => data.delete(k),
  };
  // Just enough page for ui.js and map.js to load: no pictures, and the world map's far islands (4 and 5).
  const document = { getElementById: () => ({}) };
  const WORLD = { wide: { farDocks: { 4: [0, 0], 5: [0, 0] } } };
  const ctx = vm.createContext({ localStorage, document, WORLD, ART: {} });
  ctx.window = ctx; // as in a browser, window.X is also the global X
  for (const f of FILES) vm.runInContext(src(f), ctx, { filename: f });
  return ctx;
}
// Gives a lesson 0-3 stars by saving the same best score in each of its games (5 of 5 = 3 stars).
const SCORE_FOR = [0, 1, 3, 5];
function starLesson(page, id, stars) {
  const l = page.LE.lesson.lessonById(id);
  for (const key of [page.LE.lesson.mainGame(l).key, "spell-" + id, "build-" + id, "do-" + id])
    page.Store.saveBest(key, SCORE_FOR[stars]);
  assert.equal(page.LE.progress.stopStars(id), stars, id);
}
// The lessons that count at level n (not seasonal ones, like the Ghost Ship's Halloween).
const idsAt = (page, n) => page.LESSONS.filter((l) => l.level === n && !page.LE.lesson.seasonal(l)).map((l) => l.id);
const keysOf = (due) => plain(due.map(({ lesson, it }) => lesson.id + ":" + it.word));

test("recordAnswer files the answer under lessonId:word", () => {
  const page = load();
  const { lessonById } = page.LE.lesson;
  const animals = lessonById("animals");
  const cat = animals.items.find((it) => it.word === "cat");
  page.LE.progress.recordAnswer(animals, cat, "miss");
  assert.deepEqual(plain(page.Store.words.get("animals:cat")), { box: 0, due: page.SRS.today(), right: 0, wrong: 1 });
});

test("dueWords gives the lesson and card for each due word, shakiest first", () => {
  const today = load().SRS.today();
  const due = load({
    "colors:red": { box: 2, due: today, right: 2, wrong: 0 },
    "animals:cat": { box: 0, due: today, right: 0, wrong: 1 },
    "fruits:banana": { box: 1, due: today + 1, right: 1, wrong: 0 }, // not due yet
  }).LE.progress.dueWords();
  assert.deepEqual(keysOf(due), ["animals:cat", "colors:red"]);
  assert.equal(due[0].lesson.title, "Animals");
  assert.equal(due[0].it.zh, "猫");
});

test("dueWords asks a word only once, even if it's due in several lessons", () => {
  const page = load();
  const today = page.SRS.today();
  const due = load({
    "alphabet:cat": { box: 1, due: today, right: 1, wrong: 0 },
    "animals:cat": { box: 0, due: today, right: 0, wrong: 2 },
    "phonics:cat": { box: 0, due: today, right: 0, wrong: 1 },
  }).LE.progress.dueWords();
  assert.deepEqual(keysOf(due), ["animals:cat"]); // the shakiest one
});

test("dueWords skips words and lessons that are gone", () => {
  const page = load();
  const today = page.SRS.today();
  const due = load({
    "animals:unicorn": { box: 0, due: today, right: 0, wrong: 1 },
    "dragons:cat": { box: 0, due: today, right: 0, wrong: 1 },
    "animals:dog": { box: 0, due: today, right: 0, wrong: 1 },
  }).LE.progress.dueWords();
  assert.deepEqual(keysOf(due), ["animals:dog"]);
});

test("dueWords stops at the limit, after skipping", () => {
  const page = load();
  const today = page.SRS.today();
  const words = { "animals:unicorn": { box: 0, due: today - 9, right: 0, wrong: 1 } };
  for (const w of ["cat", "dog", "pig", "lion", "owl"]) words["animals:" + w] = { box: 1, due: today, right: 1, wrong: 0 };
  const due = load(words).LE.progress.dueWords(3);
  assert.deepEqual(keysOf(due), ["animals:cat", "animals:dog", "animals:lion"]);
});

test("every word in every lesson can be filed and found again", () => {
  const page = load();
  const { recordAnswer, dueWords } = page.LE.progress;
  for (const lesson of page.LESSONS) for (const it of lesson.items) recordAnswer(lesson, it, "miss");
  const words = new Set(page.LESSONS.flatMap((l) => l.items.map((it) => it.word)));
  assert.equal(dueWords().length, words.size);
});

test("every lesson has a level from 1 to 3, and every level has lessons", () => {
  const page = load();
  for (const l of page.LESSONS) assert.ok([1, 2, 3].includes(l.level), l.id);
  for (const n of [1, 2, 3]) assert.ok(idsAt(page, n).length > 0, "level " + n);
});

test("a new child is at level 1, with none of its lessons done", () => {
  const page = load();
  assert.deepEqual(plain(page.LE.progress.childLevel()), { n: 1, done: 0, total: idsAt(page, 1).length });
});

test("a seasonal lesson is on no island and doesn't count toward the level", () => {
  const page = load();
  assert.ok(page.LE.lesson.seasonal(page.LE.lesson.lessonById("halloween")));
  assert.ok(!page.LE.map.ISLES.some((i) => i.stops.includes("halloween")));
  assert.ok(!idsAt(page, 1).includes("halloween"));
});

test("a visitor comes only in its season", () => {
  const { visitNow } = load().LE.lesson;
  assert.equal(visitNow(new Date(2026, 8, 30)), null);
  assert.equal(visitNow(new Date(2026, 9, 1)).id, "halloween");
  assert.equal(visitNow(new Date(2026, 10, 7)).id, "halloween");
  assert.equal(visitNow(new Date(2026, 10, 8)), null);
});

test("level 2 comes once 70% of the level-1 lessons have 2 stars or more", () => {
  const page = load();
  const one = idsAt(page, 1);
  const needed = Math.ceil(0.7 * one.length);
  one.slice(0, needed - 1).forEach((id) => starLesson(page, id, 2));
  starLesson(page, one[needed - 1], 1); // 1 star doesn't count
  assert.equal(page.LE.progress.childLevel().n, 1);
  starLesson(page, one[needed - 1], 2);
  assert.equal(page.LE.progress.childLevel().n, 2);
  assert.equal(page.LE.progress.childLevel().done, 0);
});

test("the Start at setting raises the level, and progress can still go past it", () => {
  const page = load(undefined, { level: "2" });
  assert.equal(page.LE.progress.childLevel().n, 2);
  const two = idsAt(page, 2);
  two.forEach((id) => starLesson(page, id, 3));
  assert.equal(page.LE.progress.childLevel().n, 2, "level 1 isn't done, but the child started at 2");
  idsAt(page, 1).forEach((id) => starLesson(page, id, 3));
  assert.equal(page.LE.progress.childLevel().n, 3);
  assert.equal(load(undefined, { level: "junk" }).LE.progress.childLevel().n, 1);
});

test("Pip suggests the first level-1 lesson in island order, skipping harder ones", () => {
  const page = load();
  const { nextStop } = page.LE.map;
  assert.equal(nextStop(), "alphabet");
  starLesson(page, "alphabet", 1);
  // Word Families (level 2) is next on ABC Island, but Pip goes on to Rainbow Island's numbers.
  assert.equal(nextStop(), "numbers");
});

test("with every level-1 lesson started, Pip suggests one with only 1 star", () => {
  const page = load();
  const weak = ["fruits", "family", "toys", "food"];
  idsAt(page, 1).forEach((id) => starLesson(page, id, weak.includes(id) ? 1 : 2));
  assert.equal(page.LE.progress.childLevel().n, 1); // 8 of 12 isn't 70%
  const first = page.LE.map.ISLES.flatMap((i) => i.stops).find((id) => weak.includes(id));
  assert.equal(page.LE.map.nextStop(), first);
});

test("at level 2, Pip suggests level-2 lessons, starting with the first in island order", () => {
  const page = load(undefined, { level: "2" });
  starLesson(page, "alphabet", 3);
  assert.equal(page.LE.map.nextStop(), "phonics");
});

test("when everything at the child's level is done, Pip suggests the next level up; then nothing", () => {
  const page = load();
  idsAt(page, 1).forEach((id) => starLesson(page, id, 2));
  idsAt(page, 2).forEach((id) => starLesson(page, id, 2));
  // now level 3; with its lessons done too, only the stars are left to collect
  assert.equal(page.LE.progress.childLevel().n, 3);
  assert.equal(page.LE.map.nextStop(), page.LE.map.ISLES.flatMap((i) => i.stops).find((id) => idsAt(page, 3).includes(id)));
  idsAt(page, 3).forEach((id) => starLesson(page, id, 2));
  assert.equal(page.LE.map.nextStop(), null);
});

test("lessons above the child's level are marked as a challenge; Write and the scenes never are", () => {
  const page = load();
  const { aboveLevel } = page.LE.map;
  assert.equal(aboveLevel("weather"), true);
  assert.equal(aboveLevel("phonics"), true);
  assert.equal(aboveLevel("animals"), false);
  assert.equal(aboveLevel("write"), false);
  assert.equal(aboveLevel("scene-farm"), false);
  assert.equal(load(undefined, { level: "3" }).LE.map.aboveLevel("weather"), false);
});

test("tier: easy while a word is new or just missed, normal while learning, hard once mastered", () => {
  const page = load();
  const { lessonById } = page.LE.lesson;
  const { recordAnswer, tier } = page.LE.progress;
  const animals = lessonById("animals");
  const cat = animals.items.find((it) => it.word === "cat");
  assert.equal(tier(animals, cat), "easy");
  recordAnswer(animals, cat, "pass");
  assert.equal(tier(animals, cat), "normal");
  recordAnswer(animals, cat, "miss");
  assert.equal(tier(animals, cat), "easy");
  const today = page.SRS.today();
  const known = load({ "animals:cat": { box: 4, due: today + 8, right: 4, wrong: 0 } });
  assert.equal(known.LE.progress.tier(known.LE.lesson.lessonById("animals"), cat), "hard");
});

test("pickRounds takes the least known words first", () => {
  const today = load().SRS.today();
  const words = {};
  for (const w of ["cat", "dog", "pig", "lion", "owl", "fish", "rabbit", "turtle", "elephant"])
    words["animals:" + w] = { box: 3, due: today + 4, right: 3, wrong: 0 };
  words["animals:turtle"].box = 0; // just missed
  const page = load(words);
  const animals = page.LE.lesson.lessonById("animals");
  for (let k = 0; k < 20; k++) {
    const picked = plain(page.LE.progress.pickRounds(animals, animals.items, 5).map((it) => it.word)).sort();
    // zebra, whale and fox are new (box 0) and turtle was missed: those four always, plus one of the rest
    for (const w of ["fox", "turtle", "whale", "zebra"]) assert.ok(picked.includes(w), w);
    assert.equal(picked.length, 5);
  }
});

test("pickRounds never asks for more than the lesson has", () => {
  const page = load();
  const colors = page.LE.lesson.lessonById("colors");
  assert.equal(page.LE.progress.pickRounds(colors, colors.items.slice(0, 3), 5).length, 3);
});

test("likeness ranks rhymes, then the same first letter, then the same length", () => {
  const { likeness } = load().LE.lesson;
  const rank = (w, others) => [...others].sort((a, b) => likeness(b, w) - likeness(a, w));
  assert.deepEqual(plain(rank("cat", ["dog", "car", "bat", "elephant"])), ["bat", "car", "dog", "elephant"]);
  assert.equal(likeness("Cat", "hat"), likeness("cat", "hat"));
});
