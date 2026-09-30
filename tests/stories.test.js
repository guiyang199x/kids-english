// Run with: node --test
// Checks the stories in js/content/stories.js against the real lessons, islands and pictures.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["art.js", "content/data.js", "content/islands.js", "content/visits.js", "content/stories.js", "core/lesson.js"];
const ctx = vm.createContext({});
ctx.window = ctx;
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8"), ctx, { filename: f });
const { ART, LESSONS, SCENES, ISLANDS, STORIES, VISITS } = ctx;
const { storyLink, storySentences } = ctx.LE.lesson;

// The little words a story may use without a lesson teaching them. Keep this short: a story is there to
// use the lessons' words, so a new content word belongs in a lesson first.
const LITTLE = new Set(
  `a an the and but or is are am was it its this that these i you he she we they me my your his her our
  to in on at of with for from up down here there not no yes very too so now then oh
  go come look see say hello hi bye bye-bye thank thanks please can like have has do does want let's
  big little pip beach what boo halloween play`.split(/\s+/)
);
// Every word a lesson or a picture dictionary teaches, one word at a time ("ice cream" gives "ice" and "cream").
const TAUGHT = new Set([
  ...LESSONS.flatMap((l) => l.items.flatMap((it) => it.word.toLowerCase().split(/\s+/))),
  ...SCENES.flatMap((s) => Object.keys(s.sentences)),
]);
const known = (w) => [w, w.replace(/s$/, ""), w.replace(/es$/, "")].some((f) => TAUGHT.has(f) || LITTLE.has(f));
const words = (story) =>
  story.pages.flatMap((p) => storySentences(story, p.text).flat().filter((x) => x.word).map((x) => x.word.toLowerCase()));

test("story ids are unique and each story has what the page needs", () => {
  assert.equal(new Set(STORIES.map((s) => s.id)).size, STORIES.length);
  for (const s of STORIES) {
    for (const key of ["title", "zh", "color", "tint", "cover"]) assert.ok(s[key], `${s.id}: ${key}`);
    assert.ok(
      s.island ? ISLANDS.some((i) => i.id === s.island) : VISITS.some((v) => v.id === s.visit),
      `${s.id}: no island "${s.island}" or visit "${s.visit}"`
    );
    assert.ok([1, 2, 3].includes(s.level), `${s.id}: level`);
    assert.ok(s.pages.length >= 3 && s.pages.length <= 8, `${s.id}: 3 to 8 pages`);
    for (const p of s.pages) assert.ok(p.text && p.zh, `${s.id}: a page needs text and zh`);
  }
});

test("every word in a story is taught by a lesson or is one of the little words", () => {
  for (const s of STORIES) {
    const unknown = [...new Set(words(s).filter((w) => !known(w)))];
    assert.deepEqual(unknown, [], `${s.id} uses words no lesson teaches`);
  }
});

test("every picture a story uses exists, and sprites sit inside the page", () => {
  for (const s of STORIES) {
    assert.ok(ART[s.cover], `${s.id}: cover ${s.cover}`);
    s.pages.forEach((p, k) => {
      assert.ok(ART[p.bg], `${s.id} page ${k + 1}: bg ${p.bg}`);
      for (const sp of p.sprites || []) {
        assert.ok(ART[sp.art], `${s.id} page ${k + 1}: sprite ${sp.art}`);
        for (const v of ["x", "y", "w"]) assert.ok(sp[v] > 0 && sp[v] <= 100, `${s.id} page ${k + 1}: ${sp.art}.${v}`);
      }
    });
  }
});

test("a story's links point at a lesson that teaches the word", () => {
  for (const s of STORIES)
    for (const [w, id] of Object.entries(s.links || {})) {
      const link = storyLink(s, w);
      assert.ok(link && link.lesson.id === id, `${s.id}: "${w}" isn't in lesson "${id}"`);
    }
});

test("a page's text splits into sentences and words, and joins back the same", () => {
  const s = STORIES.find((x) => x.id === "pip-beach");
  const text = "Look! A starfish. It is orange. Bye-bye, Pip's beach!";
  const sentences = storySentences(s, text);
  assert.equal(sentences.length, 4);
  assert.equal(sentences.flat().map((x) => x.word || x.text).join(""), text);
  const ws = sentences.flat().filter((x) => x.word);
  assert.deepEqual([...ws.map((x) => x.word)], ["Look", "A", "starfish", "It", "is", "orange", "Bye-bye", "Pip's", "beach"]);
  assert.equal(ws.find((x) => x.word === "orange").link.lesson.id, "colors");
  assert.equal(ws.find((x) => x.word === "starfish").link.it.zh, "海星");
  assert.equal(ws.find((x) => x.word === "Look").link, null);
});
