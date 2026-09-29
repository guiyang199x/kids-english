// Pip says: touch, drag, color or move along with what Pip asks.
(function () {
  const { ROUNDS } = LE.lesson;
  const { app, bounce, celebrate, praise, progress, shuffle, stars, theme, tween, zhLine } = LE.ui;
  const { results } = LE.games;

  // Pip asks and the child does it on the picture: touches a part of Pip ("Touch Pip's nose.", type "tap"), drags
  // the cat somewhere ("Put the cat under the table.", type "drag") or colors a thing with a crayon ("Color the ball
  // blue.", type "paint"). The zones are drawn in tools/art/build17.py and build19.py. Doing the wrong thing reads
  // out what the child did ("The cat is on the table."); after two misses the right zone (and crayon) glows.
  // The cat can also be tapped, then tapped where it should go, for fingers that can't drag yet.
  // Type "act" is for the body: Pip says a move and does it (build20.py), the child does it too and taps "I did it!".
  const svgPoint = (svg, e) => new DOMPoint(e.clientX, e.clientY).matrixTransform(svg.getScreenCTM().inverse());

  function pipSays(lesson) {
    const game = lesson.pipSays;
    const colorZh = (c) => lesson.items.find((it) => it.word === c).zh;
    // Coloring: what the page says when `thing` is colored `c`, and the asks (each thing once, each color once).
    const painted = (thing, c) => ({ is: `The ${thing.zone} is ${c}.`, isZh: `${thing.zh}是${colorZh(c)}的。` });
    const colors = game.paint ? shuffle(Object.keys(game.paint)) : [];
    const rounds =
      game.type === "paint"
        ? shuffle(game.things)
            .slice(0, ROUNDS)
            .map((th, i) => ({
              zone: th.zone,
              color: colors[i],
              say: `Color the ${th.zone} ${colors[i]}.`,
              zh: `把${th.zh}涂成${colorZh(colors[i])}。`,
              ...painted(th, colors[i]),
            }))
        : shuffle(game.tasks).slice(0, ROUNDS);
    let round = 0;
    let score = 0;
    let misses = 0;
    let locked = false;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/learn/${lesson.id}">← ${lesson.title}</a></nav>
      <section class="quiz pipsays pipsays-${game.type}" style="${theme(lesson)}">
        <div class="quiz-top">
          <span class="progress" aria-live="polite"></span>
          <span class="score"></span>
        </div>
        <p class="do-ask" aria-live="polite"><span class="do-say"></span><span class="do-note"></span></p>
        <div class="do-pic">${ART[game.art]}</div>
        ${game.paint ? `<div class="crayons">${Object.keys(game.paint)
          .map((c) => `<button class="crayon" data-color="${c}" aria-label="${c}" aria-pressed="false">${ART[c]}</button>`)
          .join("")}</div>` : ""}
        ${game.type === "act" ? `<button class="btn primary did" disabled>I did it!</button>` : ""}
        <button class="btn listen">▶ Listen again</button>
      </section>`;
    const $ = (sel) => app.querySelector(sel);
    const svg = $(".do-pic svg");
    // Pip acts out what was touched (blinks, wiggles his ears...), or giggles; one at a time.
    const react = (cls) => {
      svg.classList.remove(...[...svg.classList].filter((c) => c.startsWith("react-") || c === "tickle"));
      bounce(svg, cls);
    };
    const task = () => rounds[round];
    const taskFor = (zone) => game.tasks.find((t) => t.zone === zone);
    const note = (cls, text, zh) => {
      const el = $(".do-note");
      el.className = "do-note " + cls;
      el.innerHTML = text ? text + zhLine(zh, "zh-sub") : "";
    };
    $(".listen").addEventListener("click", () => Speech.say(task().say));
    let startRound = () => Speech.say(task().say);

    function showRound() {
      misses = 0;
      locked = false;
      app.querySelectorAll(".pipsays .hint").forEach((el) => el.classList.remove("hint"));
      $(".progress").innerHTML = progress(game.type === "act" ? "Move" : "Question", round, rounds.length);
      $(".score").innerHTML = stars(score, rounds.length);
      $(".do-say").innerHTML = task().say + zhLine(task().zh, "zh-sub");
      note("", "");
      startRound();
    }

    // `ok`: the child did what Pip asked. `did` says what they did ({is, isZh}); `el` is where the confetti comes from.
    function answer(ok, did, el) {
      const t = task();
      if (ok) {
        locked = true;
        if (!misses) score++;
        $(".score").innerHTML = stars(score, rounds.length);
        note("good", "★ " + t.is, t.isZh);
        app.querySelectorAll(".pipsays .hint").forEach((z) => z.classList.remove("hint"));
        celebrate(el);
        if (game.type === "tap") react("react-" + t.zone);
        Speech.say([praise(), t.is], { gap: 250 }).then(() => {
          if (!svg.isConnected) return;
          round++;
          round < rounds.length ? showRound() : finish();
        });
      } else {
        misses++;
        note("retry", did.is + " Try again!", did.isZh + "再试一次！");
        if (misses >= 2)
          app.querySelectorAll(`.pipsays [data-zone="${t.zone}"], .crayon[data-color="${t.color}"]`).forEach((z) => z.classList.add("hint"));
        Speech.say([did.is, "Try again.", t.say], { gap: 250 });
      }
    }

    // ----- tap: touch a part of Pip -----
    if (game.type === "tap") {
      const spots = [...svg.querySelectorAll(".do-spot")];
      svg.addEventListener("click", (e) => {
        if (locked) return;
        const p = svgPoint(svg, e);
        // The nearest part, measured in part sizes, so the small nose is as easy to hit as a big ear.
        let hit = null;
        let best = 1.8;
        for (const s of spots) {
          const d = Math.hypot(p.x - s.getAttribute("cx"), p.y - s.getAttribute("cy")) / s.getAttribute("r");
          if (d < best) [hit, best] = [s, d];
        }
        if (!hit) {
          react("tickle");
          return Speech.say("Hee hee! That tickles!");
        }
        const zone = hit.dataset.zone;
        const ring = zone === task().zone ? "on" : "miss";
        const same = spots.filter((s) => s.dataset.zone === zone);
        same.forEach((s) => bounce(s, ring));
        setTimeout(() => same.forEach((s) => s.classList.remove(ring)), 1200);
        answer(zone === task().zone, taskFor(zone), hit);
      });
    }

    // ----- drag: move the cat around the room -----
    if (game.type === "drag") {
      const cat = svg.querySelector(".do-thing");
      const layer = svg.querySelector(".do-drag");
      const zones = [...svg.querySelectorAll(".do-zone")];
      const slotPos = (slot) => ({ x: +slot.dataset.x, y: +slot.dataset.y, s: +slot.dataset.s });
      let slot = cat.parentNode;
      let pos = slotPos(slot);
      const place = () => cat.setAttribute("transform", `translate(${pos.x.toFixed(1)} ${pos.y.toFixed(1)}) scale(${pos.s.toFixed(3)})`);
      const glide = (to, done) => {
        const from = { ...pos };
        tween(280, (t) => {
          pos = { x: from.x + (to.x - from.x) * t, y: from.y + (to.y - from.y) * t, s: from.s + (to.s - from.s) * t };
          place();
        }, done);
      };
      // The zone under a point, or the nearest one if the point is just outside.
      const inZone = (z, p, pad = 0) => {
        const [x, y, w, h] = ["x", "y", "width", "height"].map((a) => +z.getAttribute(a));
        return p.x >= x - pad && p.x <= x + w + pad && p.y >= y - pad && p.y <= y + h + pad;
      };
      const zoneAt = (p) => zones.find((z) => inZone(z, p)) || zones.find((z) => inZone(z, p, 24));

      let drag = null; // {off, start, moved} while a finger is on the cat
      let carrying = false; // the cat was tapped and waits for a tap where it should go
      let busy = false; // the cat is gliding to its place
      const pickUp = () => {
        layer.appendChild(cat);
        cat.classList.add("lifted");
      };
      function drop(p) {
        carrying = false;
        cat.classList.remove("lifted", "carry");
        const z = zoneAt(p);
        busy = true;
        if (!z) {
          // dropped nowhere in particular: back where it was
          return glide(slotPos(slot), () => {
            slot.appendChild(cat);
            busy = false;
            Speech.say(task().say);
          });
        }
        const to = svg.querySelector(`.do-slot[data-slot="${z.dataset.slot}"]`);
        glide(slotPos(to), () => {
          to.appendChild(cat);
          slot = to;
          busy = false;
          answer(z.dataset.zone === task().zone, taskFor(z.dataset.zone), cat);
        });
      }

      svg.addEventListener("pointerdown", (e) => {
        if (locked || busy || e.button > 0) return;
        const p = svgPoint(svg, e);
        const onCat = e.target.closest(".do-thing");
        if (!onCat) {
          if (carrying) drop(p);
          return;
        }
        e.preventDefault();
        svg.setPointerCapture(e.pointerId);
        if (!carrying) pickUp();
        drag = { off: { x: pos.x - p.x, y: pos.y - p.y }, start: p, moved: false };
      });
      svg.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const p = svgPoint(svg, e);
        if (!drag.moved && Math.hypot(p.x - drag.start.x, p.y - drag.start.y) < 8) return;
        drag.moved = true;
        cat.classList.remove("carry");
        pos = { ...pos, x: p.x + drag.off.x, y: p.y + drag.off.y };
        place();
      });
      const release = () => {
        if (!drag) return;
        const { moved } = drag;
        drag = null;
        if (moved) return drop(pos);
        // a tap on the cat picks it up (or puts it back down)
        if (carrying) {
          carrying = false;
          cat.classList.remove("lifted", "carry");
          slot.appendChild(cat);
        } else {
          carrying = true;
          cat.classList.add("carry");
          Speech.say("Where does the cat go? Tap there.");
        }
      };
      svg.addEventListener("pointerup", release);
      svg.addEventListener("pointercancel", () => {
        if (!drag) return;
        drag = null;
        drop({ x: -999, y: -999 });
      });
    }

    // ----- paint: pick a crayon, then tap the thing to color -----
    if (game.type === "paint") {
      let crayon = null;
      app.querySelectorAll(".crayon").forEach((b) =>
        b.addEventListener("click", () => {
          app.querySelectorAll(".crayon").forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
          crayon = b.dataset.color;
          bounce(b);
          Speech.say(crayon);
        })
      );
      svg.querySelectorAll(".do-paint").forEach((g) =>
        g.addEventListener("click", () => {
          if (locked) return;
          if (!crayon) {
            bounce($(".crayons"));
            note("retry", "Pick a crayon first!", "先选一支蜡笔！");
            return Speech.say("Pick a crayon first.");
          }
          // Whatever the child does gets colored, right or not.
          g.querySelectorAll(".pf").forEach((el) => (el.style.fill = game.paint[crayon]));
          const thing = game.things.find((th) => th.zone === g.dataset.zone);
          answer(thing.zone === task().zone && crayon === task().color, painted(thing, crayon), g);
        })
      );
    }

    // ----- act: Pip says a move and does it; the child does it too -----
    if (game.type === "act") {
      const did = $(".did");
      startRound = () => {
        const t = task();
        svg.querySelectorAll(".act-prop").forEach((p) => (p.style.display = p.dataset.move === t.zone ? "" : "none"));
        svg.setAttribute("class", "act-" + t.zone);
        did.disabled = true;
        // Pip starts moving on "Go!" and keeps going until the child says they did it.
        Speech.say([t.say, "Ready? Go!"], { gap: 300 }).then(() => {
          if (!svg.isConnected || task() !== t || locked) return;
          svg.classList.add("moving");
          did.disabled = false;
        });
      };
      did.addEventListener("click", () => {
        if (locked) return;
        did.disabled = true;
        svg.classList.remove("moving");
        answer(true, task(), did);
      });
    }

    const finish = () =>
      results($(".quiz"), {
        score,
        total: rounds.length,
        key: "do-" + lesson.id,
        lesson,
        again: () => pipSays(lesson),
        note:
          game.type === "act"
            ? `You did ${score} moves with Pip!`
            : `You did ${score} of ${rounds.length} right on the first try.`,
      });

    showRound();
  }

  LE.games.pipSays = pipSays;
})();
