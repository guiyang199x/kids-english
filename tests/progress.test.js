// Run with: node --test
// Loads the real lessons with srs.js, store.js and core/progress.js, with a fake localStorage.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["content/data.js", "srs.js", "store.js", "core/lesson.js", "core/progress.js"];
const src = (f) => fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8");
// Objects made inside the fake page have that page's prototypes, so compare plain copies.
const plain = (v) => JSON.parse(JSON.stringify(v));

// A fresh page load. `words` is the saved review schedule to start from.
function load(words) {
  const data = new Map([["le-version", "2"]]);
  if (words) data.set("le-words", JSON.stringify(words));
  const localStorage = {
    getItem: (k) => (data.has(k) ? data.get(k) : null),
    setItem: (k, v) => data.set(k, String(v)),
    removeItem: (k) => data.delete(k),
  };
  const ctx = vm.createContext({ localStorage });
  ctx.window = ctx; // as in a browser, window.X is also the global X
  for (const f of FILES) vm.runInContext(src(f), ctx, { filename: f });
  return ctx;
}
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
