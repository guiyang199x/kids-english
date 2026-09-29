// Rules about lessons that don't touch the page: lookups, which games a lesson has, phonics parts.
(function () {
  window.LE = { views: {}, games: {} };

  const ROUNDS = 5;
  const lessonById = (id) => window.LESSONS.find((l) => l.id === id);
  const sceneById = (id) => window.SCENES.find((s) => s.id === id);
  // The lesson's main game: most lessons use the listen game, "How many?" uses the count game.
  const mainGame = (l) =>
    l.game === "count"
      ? { view: "count", label: "Count", key: "count-" + l.id }
      : l.game === "blend"
      ? { view: "blend", label: "Blend", key: "blend-" + l.id }
      : { view: "play", label: "Listen", key: l.id };
  // Phonics: "bat" = onset "b" + family (rime) "at", and how to say each part on its own.
  const onsetOf = (it) => it.word.slice(0, it.word.length - it.family.length);
  const onsetSound = (o) => window.ONSET_SOUNDS[o] || o;
  const rimeSound = (lesson, rime) => (lesson.families.find((f) => f.rime === rime) || { sound: rime }).sound;
  const NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];
  const ZH_NUMBERS = ["一", "两", "三", "四", "五", "六", "七", "八", "九", "十"];
  const spellable = (lesson) => lesson.items.filter((it) => /^[a-z]+$/.test(it.word) && it.word.length <= 7);

  // A sentence split into word tiles. A multi-word item ("next to", "in front of") stays one tile,
  // except counting items, where the number and the noun are separate so the plural matters.
  function sentenceTiles(it) {
    const text = it.sentence.replace(/[.!?]$/, "");
    let words = text.split(" ");
    const key = it.word.toLowerCase().split(" ");
    if (key.length > 1 && !it.count) {
      const at = words.findIndex((_, k) => key.every((w, j) => (words[k + j] || "").toLowerCase() === w));
      if (at >= 0) words = [...words.slice(0, at), words.slice(at, at + key.length).join(" "), ...words.slice(at + key.length)];
    }
    return { words, end: it.sentence.slice(text.length) };
  }
  // One short sentence (3 to 6 tiles), no commas and no second sentence.
  const buildable = (lesson) =>
    lesson.items.filter((it) => {
      if (!it.sentence || /[.!?,;:]/.test(it.sentence.slice(0, -1))) return false;
      const n = sentenceTiles(it).words.length;
      return n >= 3 && n <= 6;
    });

  // How easily two words get mixed up, for the hardest listening questions: a rhyme (cat / hat) most,
  // then the same first letter, then about the same length.
  function likeness(a, b) {
    [a, b] = [a.toLowerCase(), b.toLowerCase()];
    let end = 0;
    while (end < Math.min(a.length, b.length) && a[a.length - 1 - end] === b[b.length - 1 - end]) end++;
    return (end >= 2 ? 2 : 0) + (a[0] === b[0] ? 1 : 0) + (Math.abs(a.length - b.length) <= 1 ? 0.5 : 0);
  }

  // The levels a lesson can have (its `level` in data.js). They only guide what Pip suggests; nothing is locked.
  const LEVELS = [
    { n: 1, icon: "🌱", title: "Words", zh: "认词" },
    { n: 2, icon: "🌿", title: "Sentences & sounds", zh: "句型和拼读" },
    { n: 3, icon: "🌳", title: "More words", zh: "进阶词汇" },
  ];
  const levelOf = (l) => LEVELS[(l.level || 1) - 1];

  LE.lesson = { ROUNDS, LEVELS, levelOf, likeness, lessonById, sceneById, mainGame, onsetOf, onsetSound, rimeSound, NUMBERS, ZH_NUMBERS,
    spellable, sentenceTiles, buildable };
})();
