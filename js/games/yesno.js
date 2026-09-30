// Yes or No (#/yesno/<lessonId>): a picture and a sentence. Is it right? About half the time the sentence is the
// card's own ("The cat says meow." under the cat); otherwise it's another card's, and the answer is No. It's the
// "look and read" question from the Cambridge Starters test. The sentence is read out too, and can be heard again.
(function () {
  const { ROUNDS } = LE.lesson;
  const { pickRounds, recordAnswer } = LE.progress;
  const { app, bounce, celebrate, esc, pic, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { results } = LE.games;

  function yesno(lesson) {
    const picks = pickRounds(lesson, lesson.items, ROUNDS);
    // Two of each for sure, the last one either way, all in a random order.
    const answers = shuffle([true, true, false, false, Math.random() < 0.5]).slice(0, picks.length);
    const rounds = picks.map((it, k) => {
      const other = shuffle(lesson.items.filter((x) => x !== it))[0];
      return { it, yes: answers[k], shown: answers[k] ? it : other };
    });
    let round = 0;
    let score = 0;
    let firstTry = true;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${esc(lesson.title)}</a></nav>
      <section class="quiz yesno" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <p class="yesno-ask">Is it right?${zhLine("说得对吗？", "zh-sub")}</p>
        <div class="yesno-card">
          <span class="yesno-pic"></span>
          <p class="yesno-text"><span class="yesno-sentence"></span> <button class="mini yesno-hear" aria-label="Hear it again">🔊</button></p>
          <p class="yesno-note" aria-live="polite"></p>
        </div>
        <div class="yesno-buttons">
          <button class="yesno-btn yes" data-yes="1"><span aria-hidden="true">✓</span> Yes</button>
          <button class="yesno-btn no" data-yes="0"><span aria-hidden="true">✗</span> No</button>
        </div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const say = () => Speech.say(rounds[round].shown.sentence);
    $(".yesno-hear").addEventListener("click", say);

    function showRound() {
      const r = rounds[round];
      firstTry = true;
      locked = false;
      $(".progress").innerHTML = progress("Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".yesno-pic").innerHTML = pic(r.it);
      $(".yesno-sentence").textContent = r.shown.sentence;
      $(".yesno-note").innerHTML = "";
      app.querySelectorAll(".yesno-btn").forEach((b) => b.classList.remove("right", "wrong"));
      say();
    }

    function answer(btn) {
      if (locked) return;
      const r = rounds[round];
      const ok = (btn.dataset.yes === "1") === r.yes;
      // Reading the sentence right says the child knows the word in the picture; a slip isn't forgetting it.
      if (firstTry) recordAnswer(lesson, r.it, ok ? "pass" : "soft");
      if (!ok) {
        firstTry = false;
        bounce(btn, "wrong");
        $(".score").innerHTML = stars(score, rounds.length);
        Speech.say(["Look again!", r.shown.sentence], { gap: 250 });
        return;
      }
      locked = true;
      if (firstTry) score++;
      btn.classList.add("right");
      celebrate(btn);
      $(".score").innerHTML = stars(score, rounds.length);
      // For a No, show what the picture really is.
      $(".yesno-note").innerHTML = r.yes
        ? `✓ ${esc(r.it.sentence)}${zhLine(r.it.sentenceZh || r.it.zh, "zh-sub")}`
        : `<b>${esc(r.it.word)}</b>: ${esc(r.it.sentence)}${zhLine(r.it.sentenceZh || r.it.zh, "zh-sub")}`;
      Speech.say(r.yes ? [praise(), "Yes!"] : [praise(), "No.", r.it.sentence], { gap: 250 }).then(() => {
        round++;
        if (round < rounds.length) showRound();
        else
          results($(".quiz"), {
            score,
            total: rounds.length,
            key: "yesno-" + lesson.id,
            lesson,
            again: () => yesno(lesson),
            note: `You got ${score} of ${rounds.length} right on the first try.`,
          });
      });
    }
    app.querySelectorAll(".yesno-btn").forEach((b) => b.addEventListener("click", () => answer(b)));
    showRound();
  }

  LE.games.yesno = yesno;
})();
