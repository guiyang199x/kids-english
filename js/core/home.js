// Pip's house, without the page: which letters have come to the mailbox, and the stickers in the sticker book.
(function () {
  const { lessonById } = LE.lesson;

  // ---------- the mailbox (js/content/letters.js) ----------
  // The letters that have come, in order, as { letter, sent }: `sent` is the saved reply ({ day, reply }), or
  // undefined while the letter waits for one. The first letter is there from the start; each next one comes the
  // day after the one before it was answered, so there's something new to find on another day.
  function mailbox(day = SRS.today()) {
    const out = [];
    for (const letter of window.LETTERS) {
      const prev = out[out.length - 1];
      if (prev && !(prev.sent && prev.sent.day < day)) break;
      out.push({ letter, sent: Store.mail.get(letter.id) });
    }
    return out;
  }
  // A letter that has come, by id (null for one still on its way: it can't be opened yet).
  const letterById = (id, day) => (mailbox(day).find((m) => m.letter.id === id) || { letter: null }).letter;
  // How many letters wait for a reply (0 or 1: the next one only comes once this one is answered).
  const unanswered = (day) => mailbox(day).filter((m) => !m.sent).length;
  // What happens next: "reply" (a letter waits), "tomorrow" (answered today; the next comes tomorrow) or
  // "done" (every letter has come and been answered).
  function mailNext(day) {
    const got = mailbox(day);
    if (got.some((m) => !m.sent)) return "reply";
    return got.length < window.LETTERS.length ? "tomorrow" : "done";
  }

  // ---------- the sticker book ----------
  // A word's sticker: "none" until the child has answered it in a game or said it, "found" after that, and "shiny"
  // once it's mastered in the review schedule (box 4: remembered after gaps of 1, 2 and 4 days).
  function sticker(lesson, it) {
    const key = lesson.id + ":" + it.word;
    const entry = Store.words.get(key);
    if (SRS.level(entry) === "mastered") return "shiny";
    return entry || Store.said.has(key) ? "found" : "none";
  }
  // The book's pages: every lesson, in the order of the islands, then any that no island lists.
  const albumLessons = () =>
    [...new Set([...window.ISLANDS.flatMap((i) => i.stops), ...window.LESSONS.map((l) => l.id)])].map(lessonById).filter(Boolean);
  // How many stickers a page (a lesson) has: { found, shiny, total }. Shiny ones count as found too.
  function albumPage(lesson) {
    const kinds = lesson.items.map((it) => sticker(lesson, it));
    return { found: kinds.filter((k) => k !== "none").length, shiny: kinds.filter((k) => k === "shiny").length, total: kinds.length };
  }
  // The same, added up over the whole book.
  function albumTotals() {
    return albumLessons()
      .map(albumPage)
      .reduce((a, p) => ({ found: a.found + p.found, shiny: a.shiny + p.shiny, total: a.total + p.total }), { found: 0, shiny: 0, total: 0 });
  }

  LE.home = { mailbox, letterById, unanswered, mailNext, sticker, albumLessons, albumPage, albumTotals };
})();
