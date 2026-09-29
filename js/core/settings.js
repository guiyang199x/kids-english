// The header controls: voice, speed and the Chinese switch.
(function () {
  const { showZh } = LE.ui;

  for (const id of ["accent", "speed"]) {
    const el = document.getElementById(id);
    el.value = Store.setting(id);
    el.addEventListener("change", () => {
      Store.setSetting(id, el.value);
      Speech.say("Hello!");
    });
  }
  const zhToggle = document.getElementById("zh");
  zhToggle.checked = showZh();
  zhToggle.addEventListener("change", () => {
    Store.setSetting("zh", zhToggle.checked ? "1" : "0");
    document.querySelectorAll(".zh, .zh-sub").forEach((el) => (el.hidden = !zhToggle.checked));
  });
  // The voice panel closes on a tap outside it or on Escape.
  const more = document.querySelector(".more");
  document.addEventListener("click", (e) => {
    if (more.open && !more.contains(e.target)) more.open = false;
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && more.open) {
      more.open = false;
      more.querySelector("summary").focus();
    }
  });
  if (!Speech.supported) document.getElementById("no-speech").hidden = false;
})();
