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

  // Yes or No: a lesson where every card has a sentence of its own, so a sentence under another card's picture is
  // plainly wrong ("The cat says meow." under the dog). Counting cards are left out: their sentences only differ
  // by the number, which the Count game already asks about.
  const yesnoable = (lesson) =>
    !lesson.game && lesson.items.length >= 3 && lesson.items.every((it) => it.sentence) &&
    new Set(lesson.items.map((it) => it.sentence)).size === lesson.items.length;

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

  // ---------- stories (js/content/stories.js) ----------
  const storyById = (id) => (window.STORIES || []).find((s) => s.id === id);
  // The lesson card a word in a story stands for, as { lesson, it }, or null. Plurals and verbs with -s find
  // their word too ("apples", "swims"). The story's `links` picks the lesson when a word is in several.
  function storyLink(story, word) {
    const w = word.toLowerCase();
    const forms = [w, w.replace(/s$/, ""), w.replace(/es$/, "")];
    const pinned = story.links && lessonById(story.links[w]);
    for (const lesson of pinned ? [pinned] : window.LESSONS)
      for (const f of forms) {
        const it = lesson.items.find((x) => !x.count && x.word.toLowerCase() === f);
        if (it) return { lesson, it };
      }
    return null;
  }
  // A page's text as sentences, each a list of pieces: words ({ word, link }) and what's between them ({ text }).
  // "Bye-bye" and "Pip's" stay one word.
  function storySentences(story, text) {
    // split() with one capture group puts the words at the odd places.
    return text.match(/[^.!?]+[.!?]*\s*/g).map((s) =>
      s
        .split(/([A-Za-z]+(?:[-'][A-Za-z]+)*)/)
        .map((part, k) => (k % 2 ? { word: part, link: storyLink(story, part) } : { text: part }))
        .filter((p) => p.word || p.text)
    );
  }

  // ---------- seasonal visitors (js/content/visits.js) ----------
  // The visitor whose season `date` falls in (from and to are [month, day], both included, every year), or null.
  function visitNow(date = new Date()) {
    const md = (m, d) => m * 100 + d;
    const now = md(date.getMonth() + 1, date.getDate());
    return (
      (window.VISITS || []).find((v) => {
        const [a, b] = [md(...v.from), md(...v.to)];
        return a <= b ? now >= a && now <= b : now >= a || now <= b; // a season may run over New Year
      }) || null
    );
  }
  // A lesson that only comes with a visitor: it's on no island and doesn't count toward the child's level.
  const seasonal = (l) => (window.VISITS || []).some((v) => v.lesson === l.id);

  LE.lesson = { ROUNDS, visitNow, seasonal, yesnoable, LEVELS, levelOf, likeness, lessonById, sceneById, mainGame, onsetOf, onsetSound, rimeSound, NUMBERS, ZH_NUMBERS,
    spellable, sentenceTiles, buildable, storyById, storyLink, storySentences };
})();
