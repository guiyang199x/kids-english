// Run with: node --test
// Checks js/content/islands.js against the island maps drawn in js/art.js (window.WORLD).
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const FILES = ["art.js", "content/data.js", "content/islands.js", "content/visits.js"];
const ctx = vm.createContext({});
ctx.window = ctx;
for (const f of FILES) vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8"), ctx, { filename: f });
const { ISLANDS, WORLD, LESSONS, SCENES, VISITS } = ctx;

test("no island has more than six stops, and each island's road has a place for every one", () => {
  for (const isle of ISLANDS) {
    assert.ok(isle.stops.length <= 6, `${isle.id} has ${isle.stops.length} stops: put the rest on a new island`);
    assert.ok(WORLD.isles[isle.id], `${isle.id} has no map in tools/art/build16.py`);
    assert.ok(WORLD.isles[isle.id].stops.length >= isle.stops.length, `${isle.id}: its road has room for fewer stops`);
  }
});

test("every lesson and picture dictionary is on exactly one island (seasonal lessons on none)", () => {
  const seasonal = new Set(VISITS.map((v) => v.lesson));
  const all = [...LESSONS.filter((l) => !seasonal.has(l.id)).map((l) => l.id), "write", ...SCENES.map((s) => "scene-" + s.id)];
  const listed = ISLANDS.flatMap((i) => i.stops);
  assert.deepEqual([...listed].sort(), [...all].sort());
});

test("both world maps place every island", () => {
  for (const name of ["wide", "tall"]) {
    assert.equal(WORLD[name].pos.length, ISLANDS.length, `${name}: one position per island`);
    assert.equal(WORLD[name].labels.length, ISLANDS.length, `${name}: one name plate per island`);
  }
});
