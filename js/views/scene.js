// The picture dictionary: a scene with labels to tap.
(function () {
  const { app, theme, zhLine } = LE.ui;
  const { backToIsle } = LE.map;

  function scene(s) {
    app.innerHTML = `
      ${backToIsle("scene-" + s.id)}
      <section class="lesson-head" style="${theme(s)}">
        <div><h1>${s.title}</h1><p>${s.subtitle}.</p></div>
      </section>
      <div class="scene">${ART[s.art]}</div>
      <p class="caption" aria-live="polite">&nbsp;</p>`;
    const caption = app.querySelector(".caption");
    const activate = (tag) => {
      app.querySelectorAll(".tag.on").forEach((t) => t.classList.remove("on"));
      tag.classList.add("on");
      const w = tag.dataset.word;
      caption.innerHTML = s.sentences[w] + zhLine(s.sentencesZh[w], "zh caption-zh");
      Speech.say([w, s.sentences[w]], { gap: 350 });
    };
    app.querySelectorAll(".tag").forEach((tag) => {
      tag.addEventListener("click", () => activate(tag));
      tag.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          activate(tag);
        }
      });
    });
  }

  LE.views.scene = scene;
})();
