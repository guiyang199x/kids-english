// Everything the site saves lives in localStorage under "le-" keys, and this is the only file that touches it.
// If storage is blocked or full (some private modes throw), values are kept in memory for this visit instead.
(function () {
  const PREFIX = "le-";
  // Bump when a saved format changes, and add a step to migrate() that converts the old data.
  const VERSION = 2;
  const DEFAULTS = { accent: "en-US", speed: "0.7", zh: "0" };

  let ls = null;
  try {
    ls = window.localStorage;
    ls.setItem(PREFIX + "probe", "1");
    ls.removeItem(PREFIX + "probe");
  } catch (e) {
    ls = null;
  }
  // Every write lands here too, so a value that couldn't be stored still holds until the page closes.
  const memory = new Map();

  function read(name) {
    if (memory.has(name)) return memory.get(name);
    if (!ls) return null;
    try {
      return ls.getItem(PREFIX + name);
    } catch (e) {
      return null;
    }
  }
  function write(name, value) {
    memory.set(name, String(value));
    if (!ls) return;
    try {
      ls.setItem(PREFIX + name, String(value));
    } catch (e) {}
  }

  // A saved JSON value, or `fallback` if it's missing, broken or not the right shape.
  function readJSON(name, isValid, fallback) {
    try {
      const value = JSON.parse(read(name));
      if (isValid(value)) return value;
    } catch (e) {}
    return fallback;
  }
  const isMap = (v) => !!v && typeof v === "object" && !Array.isArray(v);

  // A set of strings saved as a JSON array (words said, letters written, islands visited).
  function savedSet(name) {
    const set = new Set(readJSON(name, Array.isArray, []));
    return {
      has: (v) => set.has(v),
      add(v) {
        if (set.has(v)) return;
        set.add(v);
        write(name, JSON.stringify([...set]));
      },
      get size() {
        return set.size;
      },
    };
  }

  // The review schedule, { "lessonId:word": entry } for every word answered in a game (see js/srs.js).
  function wordLog() {
    const words = readJSON("words", isMap, {});
    return {
      get: (key) => words[key],
      all: () => ({ ...words }),
      // outcome: "pass", "miss" or "soft". Returns the word's new entry.
      record(key, outcome) {
        words[key] = SRS.grade(words[key], outcome, SRS.today());
        write("words", JSON.stringify(words));
        return words[key];
      },
    };
  }

  function migrate(from) {
    // Version 1 is the format the site already used before this file existed.
    // Version 2 adds "words". Words the child has already said right start in box 1, due today,
    // so the first review has something in it for a child who has been playing a while.
    if (from < 2) {
      const words = readJSON("words", isMap, {});
      const day = SRS.today();
      const said = readJSON("said", Array.isArray, []).filter((key) => !words[key]);
      said.forEach((key) => (words[key] = { box: 1, due: day, right: 1, wrong: 0 }));
      if (said.length) write("words", JSON.stringify(words));
    }
    if (from < VERSION) write("version", VERSION);
  }
  migrate(Number(read("version") || 0));

  window.Store = {
    // Settings: "accent" (en-US / en-GB), "speed" (0.7 / 0.9), "zh" ("1" shows the Chinese).
    setting: (name) => read(name) ?? DEFAULTS[name],
    setSetting: write,
    // Best score (0-5) for one game, e.g. "animals", "spell-animals", "do-body".
    best: (key) => Number(read("best-" + key) || 0),
    saveBest(key, score) {
      if (score > window.Store.best(key)) write("best-" + key, score);
    },
    // Which island Pip's boat is moored at.
    boat: () => Number(read("boat")),
    setBoat: (k) => write("boat", k),
    said: savedSet("said"), // "lessonId:word" for every word the child said right
    written: savedSet("written"), // letters traced, "A" and "a" separately
    isles: savedSet("isles"), // far islands sailed to
    words: wordLog(), // when each word comes back for review
  };
})();
