// Starts the site: picks the page for the address (#/learn/animals ...) and shows it.
(function () {
  const { buildable, lessonById, sceneById, spellable, storyById, visitNow } = LE.lesson;
  const { app, BUDDY } = LE.ui;
  const { ISLES } = LE.map;
  const { letterById } = LE.home;
  const { house, island, learn, mail, scene, ship, stickers, stopWriting, story, takeArrival, tv, world, write } = LE.views;
  const { blendGame, buildGame, countGame, pipSays, play, review, spellGame } = LE.games;

  const showById = (id) => (window.SHOWS || []).find((s) => s.id === id);

  function route() {
    Speech.stop();
    stopWriting();
    const welcome = takeArrival();
    const [, view, id] = location.hash.replace(/^#/, "").split("/");
    const lesson = id && lessonById(id);
    if (view === "learn" && lesson) learn(lesson);
    else if (view === "play" && lesson) play(lesson);
    else if (view === "spell" && lesson && spellable(lesson).length >= 3) spellGame(lesson);
    else if (view === "build" && lesson && buildable(lesson).length >= 3) buildGame(lesson);
    else if (view === "count" && lesson && lesson.game === "count") countGame(lesson);
    else if (view === "blend" && lesson && lesson.game === "blend") blendGame(lesson);
    else if (view === "do" && lesson && lesson.pipSays) pipSays(lesson);
    else if (view === "review") review();
    else if (view === "write" && /^\d+$/.test(id) && Number(id) < 26) write(Number(id));
    else if (view === "scene" && sceneById(id || "sunny")) scene(sceneById(id || "sunny"));
    else if (view === "story" && storyById(id)) story(storyById(id));
    else if (view === "house") house();
    else if (view === "tv" && (!id || showById(id))) tv(id && showById(id));
    else if (view === "ship" && visitNow()) ship(visitNow());
    else if (view === "stickers" && (!id || lesson)) stickers(lesson);
    else if (view === "mail" && (!id || letterById(id))) mail(id && letterById(id));
    else if (view === "island" && ISLES.some((i) => i.id === id)) island(ISLES.find((i) => i.id === id), welcome);
    else world();
    if (app.querySelector(".quiz:not(.pipsays-tap):not(.pipsays-act):not(.no-buddy), .write")) app.insertAdjacentHTML("beforeend", BUDDY());
    window.scrollTo(0, 0);
    app.focus({ preventScroll: true });
  }
  window.addEventListener("hashchange", route);
  route();
})();
