// Run with: node --test
// Checks js/content/islands.js (the places and regions) against the maps drawn in js/art.js (window.WORLD).
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

test("the big map has every place, in the same order, and every place is in a region", () => {
  const { REGIONS } = ctx;
  assert.deepEqual(Array.from(WORLD.bigmap.ids), Array.from(ISLANDS, (i) => i.id), "tools/art/build27.py lists the places in another order");
  assert.equal(WORLD.bigmap.labels.length, ISLANDS.length);
  assert.deepEqual(Array.from(WORLD.bigmap.regions), Array.from(REGIONS, (r) => r.id));
  for (const isle of ISLANDS) assert.ok(REGIONS.some((r) => r.id === isle.region), `${isle.id}: no region "${isle.region}"`);
});

test("a place only holds lessons of its region's level", () => {
  const { REGIONS } = ctx;
  for (const isle of ISLANDS) {
    const level = REGIONS.find((r) => r.id === isle.region).level;
    for (const id of isle.stops) {
      const l = LESSONS.find((x) => x.id === id);
      if (l) assert.equal(l.level || 1, level, `${isle.id}: ${id} is level ${l.level || 1}, not ${level}`);
    }
  }
});
