// Run with: node --test
// Checks the letters in js/content/letters.js against the real lessons and pictures.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["art.js", "content/data.js", "content/letters.js", "core/lesson.js"];
const ctx = vm.createContext({});
ctx.window = ctx;
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8"), ctx, { filename: f });
const { ART, LESSONS, SCENES, LETTERS } = ctx;
const { lessonById, storySentences } = ctx.LE.lesson;

// The little words a letter may use without a lesson teaching them: the stories' list (tests/stories.test.js),
// plus what letters say ("Dear", "Love") and ask ("What do you like?"). Keep it short: a new content word
// belongs in a lesson first.
const LITTLE = new Set(
  `a an the and but or is are am was it its this that these i you he she we they me my your his her our
  to in on at of with for from up down here there not no yes very too so now then oh
  go come look see say hello hi bye bye-bye thank thanks please can like have has do does want let's
  big little pip
  dear love what who how many when be live play new today favorite color family zoo toy weather lunch school
  friend animal by fast hoot buzz roar yum`.split(/\s+/)
);
const TAUGHT = new Set([
  ...LESSONS.flatMap((l) => l.items.flatMap((it) => it.word.toLowerCase().split(/\s+/))),
  ...SCENES.flatMap((s) => Object.keys(s.sentences)),
]);
const NAMES = new Set(LETTERS.map((l) => l.from.toLowerCase()));
const known = (w) => {
  w = w.replace(/'s$/, "");
  return NAMES.has(w) || [w, w.replace(/s$/, ""), w.replace(/es$/, ""), w.replace(/ies$/, "y")].some((f) => TAUGHT.has(f) || LITTLE.has(f));
};
const textsOf = (l) => [...l.lines.map((x) => x.text), l.ask.text, ...l.reply.choices.map((c) => l.reply.text.replace("___", c.text || c.word))];
const words = (l) =>
  textsOf(l).flatMap((t) => storySentences(l, t).flat().filter((x) => x.word).map((x) => x.word.toLowerCase()));
const itemIn = (lessonId, word) => lessonById(lessonId) && lessonById(lessonId).items.find((it) => it.word === word);

test("letter ids are unique and each letter has what the page needs", () => {
  assert.equal(new Set(LETTERS.map((l) => l.id)).size, LETTERS.length);
  for (const l of LETTERS) {
    for (const key of ["from", "art", "color", "tint"]) assert.ok(l[key], `${l.id}: ${key}`);
    assert.ok(ART[l.art], `${l.id}: no picture "${l.art}"`);
    assert.ok(l.lines.length >= 3 && l.lines.length <= 7, `${l.id}: 3 to 7 lines`);
    for (const line of l.lines) assert.ok(line.text && line.zh, `${l.id}: a line needs text and zh`);
    assert.match(l.lines[l.lines.length - 1].text, new RegExp(l.from + "$"), `${l.id}: the last line is signed`);
  }
});

test("every word in a letter is taught by a lesson or is a little word", () => {
  for (const l of LETTERS) {
    const unknown = [...new Set(words(l).filter((w) => !known(w)))];
    assert.deepEqual(unknown, [], `${l.id} uses words no lesson teaches: ${unknown.join(", ")}`);
  }
});

test("each question has three pictures from its lesson, and the answer is one of them", () => {
  for (const { id, ask } of LETTERS) {
    assert.ok(ask.text && ask.zh, `${id}: ask needs text and zh`);
    assert.equal(ask.choices.length, 3, `${id}: three choices`);
    assert.ok(ask.choices.includes(ask.answer), `${id}: the answer is a choice`);
    for (const w of ask.choices) assert.ok(itemIn(ask.lesson, w), `${id}: "${w}" is not in ${ask.lesson}`);
  }
});

test("each reply has a gap and at least four pictures from its lesson", () => {
  for (const { id, reply } of LETTERS) {
    assert.ok(reply.text.includes("___") && reply.zh.includes("___"), `${id}: the reply needs a gap in text and zh`);
    assert.ok(reply.choices.length >= 4 && reply.choices.length <= 6, `${id}: 4 to 6 choices`);
    for (const c of reply.choices) assert.ok(itemIn(reply.lesson, c.word), `${id}: "${c.word}" is not in ${reply.lesson}`);
  }
});

test("words a letter links to a lesson are in that lesson", () => {
  for (const l of LETTERS)
    for (const [w, lessonId] of Object.entries(l.links || {})) assert.ok(itemIn(lessonId, w), `${l.id}: "${w}" is not in ${lessonId}`);
});
