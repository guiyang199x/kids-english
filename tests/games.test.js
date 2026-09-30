// Run with: node --test
// Checks what the Yes or No and Find it games need from the lessons and the scenes.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["art.js", "content/data.js", "core/lesson.js"];
const ctx = vm.createContext({});
ctx.window = ctx;
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8"), ctx, { filename: f });
const { ART, LESSONS, SCENES } = ctx;
const { yesnoable } = ctx.LE.lesson;

test("Find it: every word in a scene has a label that knows where its thing is", () => {
  for (const s of SCENES) {
    for (const w of Object.keys(s.sentences)) {
      const m = ART[s.art].match(new RegExp(`data-word="${w}" data-tx="(\\d+(?:\\.\\d+)?)" data-ty="(\\d+(?:\\.\\d+)?)"`));
      assert.ok(m, `${s.id}: "${w}" has no label with a target point`);
    }
  }
});

test("Yes or No is on most lessons, and each one's sentences are all different", () => {
  const on = LESSONS.filter(yesnoable);
  assert.ok(on.length >= LESSONS.length - 3, `only ${on.length} of ${LESSONS.length} lessons have Yes or No`);
  for (const l of on) assert.equal(new Set(l.items.map((it) => it.sentence)).size, l.items.length, l.id);
});
