// Run with: node --test
// Every script index.html loads must at least parse: a syntax error in one page's file (a name declared twice,
// say) stops that whole file, and the other tests only load some of them.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const root = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const scripts = [...html.matchAll(/<script src="([^"?]+)(?:\?v=\d+)?"/g)].map((m) => m[1]);

test("index.html loads scripts, each one there", () => {
  assert.ok(scripts.length > 20, `only ${scripts.length} scripts found`);
  for (const s of scripts) assert.ok(fs.existsSync(path.join(root, s)), `${s} is missing`);
});

test("every script parses", () => {
  for (const s of scripts) {
    const code = fs.readFileSync(path.join(root, s), "utf8");
    assert.doesNotThrow(() => new vm.Script(code, { filename: s }), `${s} has a syntax error`);
  }
});
