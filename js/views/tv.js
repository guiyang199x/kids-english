// Pip TV (#/tv, and #/tv/<id> for one show; the shows are in js/content/shows.js). A show plays by itself in three
// parts: a chant to a drum beat (Pip says a line, the child says it back), a talk between Pip and a friend, and the
// same talk again with the child saying the friend's lines. Pause, skip to the next part or play a line again with the
// buttons under the screen. The drum, the jingle and the claps are made with Web Audio, so there are no sound files.
(function () {
  const { app, celebrate, esc, theme, zhLine } = LE.ui;

  // ---------- sounds ----------
  let ctx = null;
  function audio() {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    if (!ctx) ctx = new AC();
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }
  // A note: `freq` Hz from `at` for `dur` seconds, sliding to `to` if given.
  function note(freq, at, dur, { type = "triangle", vol = 0.12, to } = {}) {
    const a = audio();
    if (!a) return;
    const o = a.createOscillator();
    const g = a.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, at);
    if (to) o.frequency.exponentialRampToValueAtTime(to, at + dur);
    g.gain.setValueAtTime(vol, at);
    g.gain.exponentialRampToValueAtTime(0.001, at + dur);
    o.connect(g).connect(a.destination);
    o.start(at);
    o.stop(at + dur + 0.02);
  }
  // A short burst of noise, filtered: the tick of the beat, or a clap.
  function noise(at, dur, freq, vol) {
    const a = audio();
    if (!a) return;
    const buf = a.createBuffer(1, Math.ceil(a.sampleRate * dur), a.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
    const src = a.createBufferSource();
    const f = a.createBiquadFilter();
    const g = a.createGain();
    src.buffer = buf;
    f.type = "bandpass";
    f.frequency.value = freq;
    g.gain.value = vol;
    src.connect(f).connect(g).connect(a.destination);
    src.start(at);
  }
  const now = () => (audio() ? ctx.currentTime : 0);
  const jingle = () => [523, 659, 784, 1047].forEach((f, i) => note(f, now() + i * 0.12, 0.25, { vol: 0.1 }));
  const clap = () => noise(now(), 0.12, 1500, 0.5);

  // The drum beat under a chant: a soft kick on beats 1 and 3, a tick on 2 and 4. `onBeat(n)` lights the beat dots.
  const beat = {
    timer: 0,
    bpm: 0,
    start(bpm, onBeat, alive) {
      if (this.timer && this.bpm === bpm) return;
      this.stop();
      this.bpm = bpm;
      let n = 0;
      const tick = () => {
        if (!alive()) return this.stop();
        const t = now();
        if (n % 2 === 0) note(140, t, 0.16, { type: "sine", vol: 0.28, to: 45 });
        else noise(t, 0.05, 6000, 0.12);
        onBeat(n % 4);
        n++;
      };
      tick();
      this.timer = setInterval(tick, 60000 / bpm);
    },
    stop() {
      clearInterval(this.timer);
      this.timer = 0;
      this.bpm = 0;
    },
  };

  // ---------- the guide: every show ----------
  function guide() {
    const channel = (s) => `
      <a class="channel${Store.shows.has(s.id) ? " seen" : ""}" href="#/tv/${s.id}" style="${theme(s)}">
        <span class="channel-screen" aria-hidden="true">${ART[s.talk.cast[1].art]}</span>
        <b>${esc(s.title)}</b>${zhLine(s.zh, "zh-sub")}
        <span class="channel-parts">🎵 ${esc(s.chant.title)}</span>
        <span class="channel-parts">💬 ${esc(s.talk.title)}</span>
        ${Store.shows.has(s.id) ? `<span class="channel-seen">✓ Watched</span>` : ""}
      </a>`;
    app.innerHTML = `
      <nav class="crumbs"><a href="#/house">← Pip's House</a></nav>
      <section class="tv-guide">
        <h1>📺 Pip TV${zhLine("Pip 电视台", "zh-sub")}</h1>
        <p class="tv-how">Sing, listen and talk with Pip and his friends!${zhLine("和 Pip 还有他的朋友们一起唱歌、听对话、说英语！")}</p>
        <div class="channels">${window.SHOWS.map(channel).join("")}</div>
      </section>`;
  }

  // ---------- one show ----------
  function show(s) {
    const cast = s.talk.cast;
    const friend = cast[1];
    // How long the child gets to say a line back: longer for more words, and longer again at the slow speed.
    const turnMs = (text) => (1400 + text.split(/\s+/).length * 480) / Number(Store.setting("speed")) * 0.9;

    app.innerHTML = `
      <nav class="crumbs"><a href="#/tv">← Pip TV</a></nav>
      <section class="tv-show" style="${theme(s)}">
        <div class="tv-set">
          <div class="tv-screen" aria-live="polite"></div>
          <div class="tv-bar">
            <span class="tv-parts" aria-hidden="true"><i data-part="chant">🎵</i><i data-part="talk">💬</i><i data-part="role">🎭</i></span>
            <span class="tv-buttons">
              <button class="tv-btn tv-again" aria-label="Again">↺</button>
              <button class="tv-btn tv-pause" aria-label="Pause">⏸</button>
              <button class="tv-btn tv-skip" aria-label="Next part">⏭</button>
            </span>
          </div>
        </div>
      </section>`;
    const screen = app.querySelector(".tv-screen");
    const bar = app.querySelector(".tv-bar");
    const pic = (key) => (key && ART[key] ? `<span class="tv-pic">${ART[key]}</span>` : "");

    // ---------- the steps of the show, in order ----------
    let run = 0; // goes up whenever the show jumps, so an older step stops
    const wait = (ms, alive) =>
      new Promise((done) => {
        const until = Date.now() + ms;
        const check = () => (!alive() || Date.now() >= until ? done() : setTimeout(check, 100));
        check();
      });
    const card = (part, icon, title, zh, say) => ({
      part,
      async play(alive) {
        screen.innerHTML = `<div class="tv-card"><span class="tv-card-icon" aria-hidden="true">${icon}</span><h2>${title}</h2>${zhLine(zh, "zh-sub")}</div>`;
        jingle();
        await Speech.say(say, { gap: 250 });
        await wait(500, alive);
      },
    });
    const chantLine = (line, k) => ({
      part: "chant",
      beat: true,
      async play(alive) {
        screen.innerHTML = `
          <div class="tv-chant">
            <p class="tv-sub">🎵 ${esc(s.chant.title)} <span class="tv-beat" aria-hidden="true"><i></i><i></i><i></i><i></i></span></p>
            <div class="tv-chant-main">
              <span class="tv-dancer" aria-hidden="true" style="--beat:${(60 / s.chant.bpm).toFixed(3)}s">${ART._pip}</span>
              ${pic(line.pic)}
            </div>
            <p class="tv-line">${esc(line.text)}</p>${zhLine(line.zh)}
            <p class="tv-turn"></p>
            <button class="tv-clap">👏 Clap!</button>
            <span class="tv-count" aria-hidden="true">${k + 1} / ${s.chant.lines.length}</span>
          </div>`;
        screen.querySelector(".tv-clap").addEventListener("click", (e) => {
          clap();
          const b = e.currentTarget;
          b.classList.remove("pop");
          void b.offsetWidth;
          b.classList.add("pop");
        });
        const turn = screen.querySelector(".tv-turn");
        const text = screen.querySelector(".tv-line");
        turn.textContent = "Listen to Pip…";
        await Speech.say(line.text, { rateScale: 0.95 });
        if (!alive()) return;
        turn.innerHTML = `🎤 Your turn!${zhLine("轮到你说啦！", "zh-sub")}`;
        text.classList.add("yours");
        await wait(turnMs(line.text), alive);
      },
    });
    // A line of the talk. In the child's part (`yours`), the friend's lines aren't spoken: the child says them.
    const talkLine = (line, yours) => ({
      part: yours ? "role" : "talk",
      async play(alive) {
        const mine = yours && line.who === 1;
        const actor = (c, k) => `
          <div class="tv-actor${line.who === k ? " speaking" : ""}${k ? " right" : ""}">
            ${line.who === k ? `<p class="tv-bubble${mine ? " yours" : ""}">${mine ? `<span class="tv-turn-tag">🎤 Your turn!</span>` : ""}<b>${esc(line.text)}</b>${zhLine(line.zh, "zh-sub")}</p>` : ""}
            <span class="tv-actor-art" aria-hidden="true">${ART[c.art]}</span>
            <span class="tv-name">${esc(k && yours ? "You" : c.name)}</span>
          </div>`;
        screen.innerHTML = `
          <div class="tv-talk">
            <p class="tv-sub">${yours ? "🎭" : "💬"} ${esc(s.talk.title)}</p>
            <div class="tv-stage">${actor(cast[0], 0)}${pic(line.pic) || '<span class="tv-pic"></span>'}${actor(friend, 1)}</div>
            ${mine ? `<button class="tv-hear">🔊 Hear it</button>` : ""}
          </div>`;
        if (mine) {
          screen.querySelector(".tv-hear").addEventListener("click", () => Speech.say(line.text, { pitch: friend.pitch }));
          await wait(turnMs(line.text), alive);
        } else {
          await Speech.say(line.text, { pitch: cast[line.who].pitch });
          await wait(450, alive);
        }
      },
    });
    const theEnd = {
      part: "end",
      async play() {
        Store.shows.add(s.id);
        screen.innerHTML = `
          <div class="tv-card tv-end">
            <span class="tv-end-pip" aria-hidden="true">${ART._pip_cheer}</span>
            <h2>Well done!</h2>${zhLine("你真棒！", "zh-sub")}
            <div class="tv-end-btns"><button class="btn tv-replay">↺ Watch again</button><a class="btn primary" href="#/tv">📺 More shows</a></div>
          </div>`;
        screen.querySelector(".tv-replay").addEventListener("click", () => go(0));
        jingle();
        celebrate(screen.querySelector("h2"));
        await Speech.say(["Well done!", "See you next time!"], { gap: 300 });
      },
    };
    const steps = [
      card("chant", "🎵", "Sing along!", "跟着唱！", ["Let's sing!", "Listen, and say it after me."]),
      ...s.chant.lines.map(chantLine),
      card("talk", "💬", esc(s.talk.title), s.talk.zh, ["Talk time!", "Listen to Pip and " + friend.name + "."]),
      ...s.talk.lines.map((l) => talkLine(l, false)),
      card("role", "🎭", `Your turn! You are ${esc(friend.name)}.`, `轮到你了！你来当 ${friend.name}。`, [`Now it's your turn.`, `You are ${friend.name}!`]),
      ...s.talk.lines.map((l) => talkLine(l, true)),
      theEnd,
    ];

    // ---------- playing ----------
    let at = 0;
    let paused = true;
    const alive = (my) => () => my === run && !paused && screen.isConnected;
    function showBar() {
      const part = (steps[at] || {}).part;
      bar.querySelectorAll(".tv-parts i").forEach((i) => i.classList.toggle("on", i.dataset.part === part));
      const p = bar.querySelector(".tv-pause");
      p.textContent = paused ? "▶" : "⏸";
      p.setAttribute("aria-label", paused ? "Play" : "Pause");
    }
    async function go(i) {
      const my = ++run;
      at = i;
      paused = false;
      Speech.stop();
      const ok = alive(my);
      while (at < steps.length && ok()) {
        showBar();
        const lights = () => screen.querySelectorAll(".tv-beat i");
        if (steps[at].beat) beat.start(s.chant.bpm, (n) => lights().forEach((d, k) => d.classList.toggle("on", k === n)), ok);
        else beat.stop();
        await steps[at].play(ok);
        if (!ok()) return;
        at++;
      }
      beat.stop();
    }
    function pause() {
      run++;
      paused = true;
      Speech.stop();
      beat.stop();
      showBar();
    }
    bar.querySelector(".tv-pause").addEventListener("click", () => (paused ? go(at) : pause()));
    bar.querySelector(".tv-again").addEventListener("click", () => go(at));
    bar.querySelector(".tv-skip").addEventListener("click", () => {
      const part = steps[at].part;
      const next = steps.findIndex((st, k) => k > at && st.part !== part);
      go(next < 0 ? steps.length - 1 : next);
    });

    // The title card waits for a tap: browsers only play sound after the child has done something on the page.
    screen.innerHTML = `
      <div class="tv-card tv-title">
        <span class="tv-logo">📺 Pip TV</span>
        <span class="tv-title-art" aria-hidden="true">${ART._pip}${ART[friend.art]}</span>
        <h2>${esc(s.title)}</h2>${zhLine(s.zh, "zh-sub")}
        <button class="btn primary tv-start">▶ Watch</button>
      </div>`;
    screen.querySelector(".tv-start").addEventListener("click", () => go(0));
    showBar();
  }

  LE.views.tv = (s) => (s ? show(s) : guide());
})();
