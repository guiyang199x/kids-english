// Run with: node --test
// Checks the Pip TV shows in js/content/shows.js against the real lessons and pictures.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["art.js", "content/data.js", "content/shows.js", "core/lesson.js"];
const ctx = vm.createContext({});
ctx.window = ctx;
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8"), ctx, { filename: f });
const { ART, LESSONS, SCENES, SHOWS } = ctx;
const { storySentences } = ctx.LE.lesson;

// The little words a show may use without a lesson teaching them: the stories' list, plus what people say when
// they talk ("Nice to meet you", "Can I help you?") and the sounds in the chants. Keep it short.
const LITTLE = new Set(
  `a an the and but or is are am was it its this that these i you he she we they me my your his her our
  to in on at of with for from up down here there not no yes very too so now then oh
  go come look see say hello hi bye bye-bye thank thanks please can like have has do does want let's
  big small little pip what how many old name nice meet help play fun again count friend favorite color
  can't what's it's meow woof roar hoot yum wow fly`.split(/\s+/)
);
const TAUGHT = new Set([
  ...LESSONS.flatMap((l) => l.items.flatMap((it) => it.word.toLowerCase().split(/\s+/))),
  ...SCENES.flatMap((s) => Object.keys(s.sentences)),
]);
const known = (show, w) => {
  const names = show.talk.cast.map((c) => c.name.toLowerCase());
  return names.includes(w) || [w, w.replace(/s$/, ""), w.replace(/es$/, "")].some((f) => TAUGHT.has(f) || LITTLE.has(f));
};
const lines = (show) => [...show.chant.lines, ...show.talk.lines];

test("show ids are unique and each show has what the player needs", () => {
  assert.equal(new Set(SHOWS.map((s) => s.id)).size, SHOWS.length);
  for (const s of SHOWS) {
    for (const key of ["title", "zh", "color", "tint"]) assert.ok(s[key], `${s.id}: ${key}`);
    assert.ok(s.chant.title && s.chant.zh && s.chant.bpm >= 60 && s.chant.bpm <= 140, `${s.id}: chant title, zh, bpm`);
    assert.ok(s.chant.lines.length >= 2 && s.chant.lines.length <= 8, `${s.id}: 2 to 8 chant lines`);
    assert.ok(s.talk.title && s.talk.zh, `${s.id}: talk title and zh`);
    assert.equal(s.talk.cast.length, 2, `${s.id}: two in the cast`);
    assert.equal(s.talk.cast[0].name, "Pip", `${s.id}: Pip is the first of the cast`);
    for (const c of s.talk.cast) assert.ok(ART[c.art] && c.pitch > 0, `${s.id}: ${c.name} needs a picture and a pitch`);
    assert.ok(s.talk.lines.some((l) => l.who === 1), `${s.id}: the friend says something (it's the child's part later)`);
    for (const l of lines(s)) {
      assert.ok(l.text && l.zh, `${s.id}: a line needs text and zh`);
      if (l.pic) assert.ok(ART[l.pic], `${s.id}: no picture "${l.pic}"`);
    }
    for (const l of s.talk.lines) assert.ok([0, 1].includes(l.who), `${s.id}: who is 0 (Pip) or 1`);
  }
});

test("every word in a show is taught by a lesson or is a little word", () => {
  for (const s of SHOWS) {
    const words = lines(s).flatMap((l) => storySentences(s, l.text).flat().filter((x) => x.word).map((x) => x.word.toLowerCase()));
    const unknown = [...new Set(words.filter((w) => !known(s, w)))];
    assert.deepEqual(unknown, [], `${s.id} uses words no lesson teaches: ${unknown.join(", ")}`);
  }
});
