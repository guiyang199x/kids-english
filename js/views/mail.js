// Pip's mailbox (#/mail) and one letter (#/mail/<id>). A letter is read out with each sentence lit up, like a story
// page; then there's a question about it (three pictures), and the child writes back by picking a picture for the
// gap in the reply ("I like ___!"). Sending the reply is what brings the next letter, the day after.
(function () {
  const { lessonById, storyLink, storySentences } = LE.lesson;
  const { app, celebrate, esc, pic, praise, sentenceHtml, shuffle, theme, zhLine } = LE.ui;
  const { mailbox, mailNext } = LE.home;

  const MAIL = { color: "#c94c48", tint: "#ffe8e6" };
  const itemOf = (lessonId, word) => lessonById(lessonId).items.find((it) => it.word === word);
  // The reply with its gap filled by a choice, in English and in Chinese.
  const replyText = (reply, c) => reply.text.replace("___", c.text || c.word);
  const replyZh = (reply, c) => reply.zh.replace("___", c.zh || itemOf(reply.lesson, c.word).zh);
  const choiceOf = (reply, word) => reply.choices.find((c) => c.word === word);

  // What comes next, under the letters: a gull bringing one tomorrow, or all of them read.
  function nextNote(next) {
    if (next === "tomorrow")
      return `<p class="mail-note"><span aria-hidden="true">🕊️</span> A new letter comes tomorrow!${zhLine("明天会有新的信哦！")}</p>`;
    if (next === "done")
      return `<p class="mail-note"><span aria-hidden="true">🎉</span> You answered every letter. Well done!${zhLine("所有的信你都回复啦，真棒！")}</p>`;
    return "";
  }

  function list() {
    const got = mailbox().reverse(); // newest first
    const envelope = ({ letter, sent }) => {
      const reply = sent && choiceOf(letter.reply, sent.reply);
      return `
        <a class="envelope${sent ? "" : " new"}" href="#/mail/${letter.id}" style="${theme(letter)}">
          <span class="envelope-stamp" aria-hidden="true">${ART[letter.art]}</span>
          <span class="envelope-text">
            <b>From ${esc(letter.from)}</b>
            ${sent ? `<span class="envelope-sent">✓ ${esc(reply ? replyText(letter.reply, reply) : "Sent")}</span>` : `<span class="envelope-new">New!</span>`}
          </span>
        </a>`;
    };
    app.innerHTML = `
      <nav class="crumbs"><a href="#/house">← Pip's House</a></nav>
      <section class="mail" style="${theme(MAIL)}">
        <h1 class="mail-title">Mailbox${zhLine("信箱", "zh-sub")}</h1>
        <p class="mail-how">Pip's friends write to you. Read, answer and write back!${zhLine("Pip 的朋友们给你写信啦。读一读，答一答，再回一封信吧！")}</p>
        <div class="envelopes">${got.map(envelope).join("")}</div>
        ${nextNote(mailNext())}
      </section>`;
    const fresh = got.find((m) => !m.sent);
    if (fresh) Speech.say(`A letter from ${fresh.letter.from}!`);
  }

  function letterPage(letter) {
    const sent = mailbox().find((m) => m.letter.id === letter.id).sent;
    const { ask, reply } = letter;
    let run = 0; // goes up with every reading, so an older one stops lighting words

    app.innerHTML = `
      <nav class="crumbs"><a href="#/mail">← Mailbox</a></nav>
      <section class="mail-letter" style="${theme(letter)}">
        <div class="letter-paper">
          <span class="letter-stamp" aria-hidden="true">${ART[letter.art]}</span>
          <div class="letter-lines">
            ${letter.lines.map((l) => `<p class="letter-line"><span class="story-text">${sentenceHtml(storySentences(letter, l.text))}</span>${zhLine(l.zh)}</p>`).join("")}
          </div>
          <div class="story-word" aria-live="polite"></div>
          <div class="story-nav">
            <button class="btn primary letter-read">🔊 Read</button>
            <button class="btn letter-slow">🐢 Word by word</button>
          </div>
        </div>
        <div class="letter-step letter-ask"${sent ? " hidden" : ""}>
          <h2><span class="step-num" aria-hidden="true">1</span> ${esc(ask.text)}${zhLine(ask.zh, "zh-sub")}</h2>
          <div class="options">${shuffle(ask.choices)
            .map((w) => `<button class="option" data-word="${esc(w)}">${pic(itemOf(ask.lesson, w))}<span class="option-word">${esc(w)}</span></button>`)
            .join("")}</div>
        </div>
        <div class="letter-step letter-reply" hidden>
          <h2><span class="step-num" aria-hidden="true">2</span> Write back to ${esc(letter.from)}!${zhLine(`给 ${letter.from} 回信吧！`, "zh-sub")}</h2>
          <div class="postcard">
            <p class="postcard-text">Dear ${esc(letter.from)}, <span class="reply-line"></span></p>
            ${zhLine(reply.zh.replace("___", "……"), "zh reply-zh")}
          </div>
          <div class="reply-choices">${reply.choices
            .map((c) => `<button class="reply-choice" data-word="${esc(c.word)}">${pic(itemOf(reply.lesson, c.word))}<span>${esc(c.text || c.word)}</span></button>`)
            .join("")}</div>
          <button class="btn primary letter-send" disabled>✉️ Send</button>
        </div>
        <div class="letter-step letter-done" hidden></div>
      </section>`;

    const $ = (sel) => app.querySelector(sel);
    const page = $(".mail-letter");
    const here = () => page.isConnected; // false once the child has left this letter
    const box = $(".letter-paper");
    const unlight = () => box.querySelectorAll(".on").forEach((el) => el.classList.remove("on"));

    // ---------- reading ----------
    function read(slow) {
      const my = ++run;
      unlight();
      const parts = [...box.querySelectorAll(slow ? ".w" : ".sent")];
      const light = (k) => {
        if (my !== run) return;
        unlight();
        if (parts[k]) parts[k].classList.add("on");
      };
      return Speech.say(
        parts.map((el) => el.textContent.trim()),
        { gap: slow ? 250 : 450, rateScale: slow ? 0.9 : 1, onPart: light }
      ).then(() => light(-1));
    }
    function showCard(link) {
      const card = box.querySelector(".story-word");
      card.innerHTML = link
        ? `<span class="story-word-pic">${pic(link.it)}</span><span><b>${esc(link.it.word)}</b>${zhLine(link.it.zh)}</span>`
        : "";
      card.classList.toggle("shown", !!link);
    }
    $(".letter-read").addEventListener("click", () => read(false));
    $(".letter-slow").addEventListener("click", () => read(true));
    box.querySelectorAll(".w").forEach((b) =>
      b.addEventListener("click", () => {
        run++;
        unlight();
        b.classList.add("on");
        showCard(storyLink(letter, b.textContent));
        Speech.say(b.textContent);
      })
    );

    // ---------- the question ----------
    let asked = false;
    app.querySelectorAll(".letter-ask .option").forEach((b) =>
      b.addEventListener("click", () => {
        if (asked) return;
        run++;
        if (b.dataset.word !== ask.answer) {
          b.classList.remove("wrong");
          void b.offsetWidth;
          b.classList.add("wrong");
          Speech.say([b.dataset.word, "Try again! Read the letter."], { gap: 250 });
          return;
        }
        asked = true;
        b.classList.add("right");
        celebrate(b);
        Speech.say([praise(), b.dataset.word], { gap: 250 });
        setTimeout(openReply, 1100);
      })
    );

    // ---------- writing back ----------
    let chosen = null;
    function fill(c) {
      $(".reply-line").innerHTML = c ? esc(replyText(reply, c)) : esc(reply.text).replace("___", '<span class="gap">&nbsp;</span>');
      const zh = $(".reply-zh");
      zh.textContent = c ? replyZh(reply, c) : reply.zh.replace("___", "……");
    }
    function openReply() {
      if (!here()) return;
      const step = $(".letter-reply");
      step.hidden = false;
      fill(null);
      step.scrollIntoView({ behavior: "smooth", block: "center" });
      Speech.say(`Write back to ${letter.from}!`);
    }
    app.querySelectorAll(".reply-choice").forEach((b) =>
      b.addEventListener("click", () => {
        chosen = choiceOf(reply, b.dataset.word);
        app.querySelectorAll(".reply-choice").forEach((x) => x.classList.toggle("on", x === b));
        fill(chosen);
        $(".letter-send").disabled = false;
        Speech.say(replyText(reply, chosen));
      })
    );
    $(".letter-send").addEventListener("click", () => {
      if (!chosen) return;
      Store.mail.send(letter.id, chosen.word, SRS.today());
      const card = $(".postcard");
      card.classList.add("flying");
      app.querySelectorAll(".reply-choice, .letter-send").forEach((x) => (x.disabled = true));
      Speech.say([`Your letter is on its way to ${letter.from}!`], { gap: 300 });
      setTimeout(() => here() && done(true), 900);
    });

    // ---------- sent ----------
    function done(justNow) {
      const choice = choiceOf(reply, (Store.mail.get(letter.id) || {}).reply);
      $(".letter-reply").hidden = true;
      const step = $(".letter-done");
      step.hidden = false;
      step.innerHTML = `
        <span class="done-pip" aria-hidden="true">${ART._pip_cheer}</span>
        <h2>${justNow ? "Sent!" : "You wrote back:"}${zhLine(justNow ? "寄出去啦！" : "你的回信：", "zh-sub")}</h2>
        ${choice ? `<p class="postcard-text sent-text">${esc(replyText(reply, choice))}</p>${zhLine(replyZh(reply, choice))}` : ""}
        ${justNow ? nextNote(mailNext()) : ""}
        <div class="story-nav"><a class="btn" href="#/mail">✉️ Mailbox</a><a class="btn primary" href="#/house">🏠 Pip's House</a></div>`;
      if (justNow) {
        celebrate(step.querySelector("h2"));
        step.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }

    if (sent) done(false);
    else read(false);
  }

  LE.views.mail = (letter) => (letter ? letterPage(letter) : list());
})();
