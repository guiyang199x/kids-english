// Run with: node --test
// Loads js/srs.js and js/store.js the way the page does, with a fake localStorage.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

// Objects made inside the fake page have that page's prototypes, so compare plain copies.
const plain = (v) => JSON.parse(JSON.stringify(v));
const src = (f) => fs.readFileSync(path.join(__dirname, "..", "js", f), "utf8");

function fakeStorage(initial = {}) {
  const data = new Map(Object.entries(initial));
  return {
    data,
    getItem: (k) => (data.has(k) ? data.get(k) : null),
    setItem: (k, v) => data.set(k, String(v)),
    removeItem: (k) => data.delete(k),
  };
}

// A fresh page load over the given storage.
function load(storage) {
  const window = { localStorage: storage };
  const ctx = vm.createContext({ window });
  vm.runInContext(src("srs.js"), ctx);
  ctx.SRS = window.SRS; // store.js uses the global, as it does in the browser
  vm.runInContext(src("store.js"), ctx);
  return window;
}

test("record saves a word's entry and it's still there after a reload", () => {
  const storage = fakeStorage();
  const { Store, SRS } = load(storage);
  const e = Store.words.record("animals:cat", "pass");
  assert.equal(e.box, 1);
  assert.equal(e.due, SRS.today() + 1);

  const again = load(storage).Store;
  assert.equal(again.words.get("animals:cat").box, 1);
  assert.deepEqual(plain(Object.keys(again.words.all())), ["animals:cat"]);
});

test("a miss after a pass puts the word back to box 0, due today", () => {
  const { Store, SRS } = load(fakeStorage());
  Store.words.record("fruits:orange", "pass");
  const e = Store.words.record("fruits:orange", "miss");
  assert.equal(e.box, 0);
  assert.equal(e.due, SRS.today());
  assert.equal(e.right, 1);
  assert.equal(e.wrong, 1);
});

test("all() is a copy, so changing it doesn't change what's saved", () => {
  const { Store } = load(fakeStorage());
  Store.words.record("animals:cat", "pass");
  delete Store.words.all()["animals:cat"];
  assert.ok(Store.words.get("animals:cat"));
});

test("upgrading from version 1 puts words already said right into today's review", () => {
  const storage = fakeStorage({
    "le-version": "1",
    "le-said": JSON.stringify(["animals:cat", "colors:red"]),
  });
  const { Store, SRS } = load(storage);
  assert.equal(storage.getItem("le-version"), "2");
  assert.deepEqual(plain(Store.words.get("animals:cat")), { box: 1, due: SRS.today(), right: 1, wrong: 0 });
  assert.deepEqual(plain(SRS.due(Store.words.all(), SRS.today()).sort()), ["animals:cat", "colors:red"]);
});

test("the upgrade runs once and keeps words that already have a schedule", () => {
  const kept = { box: 3, due: 1, right: 5, wrong: 0 };
  const storage = fakeStorage({
    "le-version": "1",
    "le-said": JSON.stringify(["animals:cat"]),
    "le-words": JSON.stringify({ "animals:cat": kept }),
  });
  load(storage);
  assert.deepEqual(JSON.parse(storage.getItem("le-words"))["animals:cat"], kept);

  // Already on version 2: a word said later isn't seeded again by another load.
  storage.setItem("le-said", JSON.stringify(["animals:cat", "animals:dog"]));
  const { Store } = load(storage);
  assert.equal(Store.words.get("animals:dog"), undefined);
});

test("a first visit writes no word list", () => {
  const storage = fakeStorage();
  load(storage);
  assert.equal(storage.getItem("le-words"), null);
  assert.equal(storage.getItem("le-version"), "2");
});

test("a broken saved word list starts empty instead of breaking the page", () => {
  for (const junk of ["{not json", "[1,2]", "null", "42"]) {
    const { Store } = load(fakeStorage({ "le-version": "2", "le-words": junk }));
    assert.deepEqual(plain(Store.words.all()), {});
    assert.equal(Store.words.record("animals:cat", "pass").box, 1);
  }
});

test("when storage is blocked, words are kept in memory for the visit", () => {
  const blocked = {
    getItem() {
      throw new Error("blocked");
    },
    setItem() {
      throw new Error("blocked");
    },
    removeItem() {},
  };
  const { Store } = load(blocked);
  Store.words.record("animals:cat", "pass");
  assert.equal(Store.words.get("animals:cat").box, 1);
});
