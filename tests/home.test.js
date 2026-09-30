// Run with: node --test
// Pip's house (js/core/home.js): letters coming to the mailbox one day at a time, and the sticker book.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["content/data.js", "content/islands.js", "content/visits.js", "content/letters.js", "srs.js", "store.js", "core/lesson.js",
  "core/home.js"];
const src = (f) => fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8");

// A fresh page load with a fake localStorage holding `saved` (keys without the "le-" prefix).
function load(saved = {}) {
  const data = new Map([["le-version", "2"]]);
  for (const [k, v] of Object.entries(saved)) data.set("le-" + k, JSON.stringify(v));
  const localStorage = {
    getItem: (k) => (data.has(k) ? data.get(k) : null),
    setItem: (k, v) => data.set(k, String(v)),
    removeItem: (k) => data.delete(k),
  };
  const ctx = vm.createContext({ localStorage });
  ctx.window = ctx;
  for (const f of FILES) vm.runInContext(src(f), ctx, { filename: f });
  return ctx;
}
const ids = (got) => Array.from(got, (m) => m.letter.id); // an array of this realm, for deepEqual
const DAY = 20000;

test("the first letter is there from the start, waiting for a reply", () => {
  const page = load();
  const { mailbox, unanswered, mailNext } = page.LE.home;
  assert.deepEqual(ids(mailbox(DAY)), [page.LETTERS[0].id]);
  assert.equal(unanswered(DAY), 1);
  assert.equal(mailNext(DAY), "reply");
});

test("the next letter comes the day after a reply, not the same day", () => {
  const page = load();
  const { mailbox, unanswered, mailNext, letterById } = page.LE.home;
  const [first, second, third] = page.LETTERS;
  page.Store.mail.send(first.id, first.reply.choices[0].word, DAY);
  assert.deepEqual(ids(mailbox(DAY)), [first.id]);
  assert.equal(unanswered(DAY), 0);
  assert.equal(mailNext(DAY), "tomorrow");
  assert.equal(letterById(second.id, DAY), null, "can't open a letter that hasn't come");

  assert.deepEqual(ids(mailbox(DAY + 1)), [first.id, second.id]);
  assert.equal(letterById(second.id, DAY + 1).id, second.id);
  assert.equal(unanswered(DAY + 1), 1);
  // Waiting days without replying doesn't bring more letters.
  assert.deepEqual(ids(mailbox(DAY + 9)), [first.id, second.id]);
  assert.ok(!ids(mailbox(DAY + 9)).includes(third.id));
});

test("replies are saved and still there after a reload", () => {
  const page = load();
  const first = page.LETTERS[0];
  page.Store.mail.send(first.id, "apple", DAY);
  const mail = JSON.parse(page.localStorage.getItem("le-mail"));
  const again = load({ mail });
  assert.deepEqual(JSON.parse(JSON.stringify(again.Store.mail.get(first.id))), { day: DAY, reply: "apple" });
});

test("once every letter is answered, there's nothing more to come", () => {
  const mail = {};
  const page = load();
  page.LETTERS.forEach((l, k) => (mail[l.id] = { day: DAY + k, reply: l.reply.choices[0].word }));
  const done = load({ mail });
  const day = DAY + page.LETTERS.length;
  assert.equal(done.LE.home.mailbox(day).length, page.LETTERS.length);
  assert.equal(done.LE.home.mailNext(day), "done");
  assert.equal(done.LE.home.unanswered(day), 0);
});

test("a sticker is found once the word is answered or said, and shiny once mastered", () => {
  const page = load({
    said: ["animals:lion"],
    words: {
      "animals:cat": { box: 1, due: DAY, right: 1, wrong: 0 },
      "animals:dog": { box: 0, due: DAY, right: 0, wrong: 1 },
      "animals:fox": { box: 4, due: DAY + 8, right: 4, wrong: 0 },
    },
  });
  const { sticker, albumPage } = page.LE.home;
  const animals = page.LE.lesson.lessonById("animals");
  const kind = (w) => sticker(animals, animals.items.find((it) => it.word === w));
  assert.equal(kind("cat"), "found");
  assert.equal(kind("dog"), "found", "a missed word has still been met");
  assert.equal(kind("lion"), "found");
  assert.equal(kind("fox"), "shiny");
  assert.equal(kind("pig"), "none");
  assert.deepEqual(JSON.parse(JSON.stringify(albumPage(animals))), { found: 4, shiny: 1, total: animals.items.length });
});

test("the sticker book has a page for every lesson, in island order", () => {
  const page = load();
  const { albumLessons, albumTotals } = page.LE.home;
  const pages = albumLessons().map((l) => l.id);
  assert.equal(new Set(pages).size, page.LESSONS.length);
  const firstStops = page.ISLANDS[0].stops.filter((id) => page.LESSONS.some((l) => l.id === id));
  assert.deepEqual(pages.slice(0, firstStops.length), firstStops);
  assert.equal(albumTotals().total, page.LESSONS.reduce((n, l) => n + l.items.length, 0));
  assert.equal(albumTotals().found, 0);
});
