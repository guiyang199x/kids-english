// Everything the site saves lives in localStorage under "le-" keys, and this is the only file that touches it.
// If storage is blocked or full (some private modes throw), values are kept in memory for this visit instead.
(function () {
  const PREFIX = "le-";
  // Bump when a saved format changes, and add a step to migrate() that converts the old data.
  const VERSION = 1;
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

  // A set of strings saved as a JSON array (words said, letters written, islands visited).
  function savedSet(name) {
    let items;
    try {
      items = JSON.parse(read(name) || "[]");
    } catch (e) {
      items = [];
    }
    const set = new Set(Array.isArray(items) ? items : []);
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

  function migrate(from) {
    // Nothing to convert yet: version 1 is the format the site already used before this file existed.
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
  };
})();
