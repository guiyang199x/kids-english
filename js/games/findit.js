// Find it (#/find/<sceneId>): a picture dictionary scene with its labels hidden. Pip says "Find the duck!" and the
// child taps it. Each label keeps the point it points at (data-tx, data-ty, from tools/art/build15.py); a tap
// counts for the nearest of those points, if it's close enough. After two misses the right spot glows.
(function () {
  const { ROUNDS } = LE.lesson;
  const { app, bounce, celebrate, esc, praise, progress, shuffle, stars, theme, zhLine } = LE.ui;
  const { backToIsle } = LE.map;
  const { results } = LE.games;

  const NEAR = 90; // how far from a thing's point (in the picture's units) a tap still counts as that thing

  function findIt(s) {
    const words = Object.keys(s.sentences);
    const rounds = shuffle(words).slice(0, ROUNDS);
    let round = 0;
    let score = 0;
    let misses = 0;
    let locked = false;

    app.innerHTML = `
      ${backToIsle("scene-" + s.id)}
      <section class="quiz find" style="${theme(s)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <p class="find-ask"><span class="find-say"></span><button class="mini find-hear" aria-label="Hear it again">🔊</button></p>
        <div class="find-pic">${ART[s.art]}<p class="find-note" aria-live="polite"></p></div>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const svg = $(".find-pic svg");
    const tags = [...svg.querySelectorAll(".tag")];
    const spot = (w) => tags.find((t) => t.dataset.word === w);
    const target = () => rounds[round];
    const ask = () => Speech.say(`Find the ${target()}!`);
    $(".find-hear").addEventListener("click", ask);

    // A ring on the picture, where a thing is: yellow to show the answer, faint while hinting.
    const NS = "http://www.w3.org/2000/svg";
    function ring(w, cls) {
      const t = spot(w);
      const c = document.createElementNS(NS, "circle");
      c.setAttribute("cx", t.dataset.tx);
      c.setAttribute("cy", t.dataset.ty);
      c.setAttribute("r", "34");
      c.setAttribute("class", "find-ring " + cls);
      svg.appendChild(c);
      return c;
    }
    const clearMarks = () => {
      svg.querySelectorAll(".find-ring").forEach((c) => c.remove());
      tags.forEach((t) => t.classList.remove("shown"));
    };

    function showRound() {
      locked = false;
      misses = 0;
      clearMarks();
      $(".progress").innerHTML = progress("Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".find-say").innerHTML = `Find the <b>${esc(target())}</b>!${zhLine(s.zh && s.zh[target()] ? `找一找：${s.zh[target()]}` : "找一找", "zh-sub")}`;
      $(".find-note").innerHTML = "";
      ask();
    }

    // The thing a tap is on: the nearest point within NEAR, or null.
    function tapped(e) {
      const p = svg.createSVGPoint();
      p.x = e.clientX;
      p.y = e.clientY;
      const at = p.matrixTransform(svg.getScreenCTM().inverse());
      let best = null;
      let bestD = NEAR;
      for (const t of tags) {
        const d = Math.hypot(at.x - t.dataset.tx, at.y - t.dataset.ty);
        if (d < bestD) [best, bestD] = [t.dataset.word, d];
      }
      return best;
    }

    svg.addEventListener("click", (e) => {
      if (locked) return;
      const w = tapped(e);
      const note = $(".find-note");
      if (w === target()) {
        locked = true;
        if (misses === 0) score++;
        clearMarks();
        ring(w, "found");
        spot(w).classList.add("shown");
        $(".score").innerHTML = stars(score, rounds.length);
        note.innerHTML = `${esc(s.sentences[w])}${zhLine(s.sentencesZh[w], "zh-sub")}`;
        celebrate(note);
        Speech.say([praise(), s.sentences[w]], { gap: 250 }).then(() => {
          round++;
          if (round < rounds.length) showRound();
          else
            results($(".quiz"), {
              score,
              total: rounds.length,
              key: "find-" + s.id,
              lesson: s,
              again: () => findIt(s),
              back: { href: "#/scene/" + s.id, label: "Look again" },
              note: `You found ${score} of ${rounds.length} on the first try.`,
            });
        });
        return;
      }
      misses++;
      bounce($(".find-pic"), "wrong");
      if (w) {
        spot(w).classList.add("shown");
        setTimeout(() => spot(w) && w !== target() && spot(w).classList.remove("shown"), 1600);
      }
      Speech.say(w ? [`That's the ${w}.`, `Find the ${target()}!`] : ["Try again!", `Find the ${target()}!`], { gap: 200 });
      note.innerHTML = w ? `That's the <b>${esc(w)}</b>. Try again!` : "Try again!";
      if (misses === 2) ring(target(), "hint");
    });

    showRound();
  }

  LE.games.findIt = findIt;
})();
