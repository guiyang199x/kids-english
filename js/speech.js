(function () {
  const synth = window.speechSynthesis;
  const supported = !!synth && "SpeechSynthesisUtterance" in window;
  const PREFERRED = ["Samantha", "Google US English", "Daniel", "Google UK English Female", "Karen", "Moira"];
  let voices = [];

  function loadVoices() {
    voices = supported ? synth.getVoices() : [];
  }
  if (supported) {
    loadVoices();
    synth.addEventListener("voiceschanged", loadVoices);
  }

  function pickVoice(lang) {
    const matching = voices.filter((v) => v.lang.replace("_", "-").startsWith(lang));
    const pool = matching.length ? matching : voices.filter((v) => v.lang.startsWith("en"));
    for (const name of PREFERRED) {
      const v = pool.find((x) => x.name.includes(name));
      if (v) return v;
    }
    return pool.find((v) => v.localService) || pool[0] || null;
  }

  // Speaks a list of phrases in order. Resolves when finished or cancelled.
  // opts: gap (ms between phrases), rateScale, pitch, onPart(i) as each phrase starts.
  function say(phrases, opts = {}) {
    if (!supported) return Promise.resolve();
    const list = Array.isArray(phrases) ? phrases : [phrases];
    const lang = Store.setting("accent");
    const rate = Number(Store.setting("speed")) * (opts.rateScale || 1);
    const voice = pickVoice(lang);
    synth.cancel();
    return new Promise((resolve) => {
      let i = 0;
      const next = () => {
        if (i >= list.length) return resolve();
        const u = new SpeechSynthesisUtterance(list[i]);
        u.lang = lang;
        u.rate = rate;
        u.pitch = opts.pitch || 1.1; // a character in a Pip TV show can have a voice of its own
        if (voice) u.voice = voice;
        const idx = i++;
        let settled = false;
        // Some browsers never fire onend (stuck or muted audio); move on after a generous estimate.
        const guard = setTimeout(() => {
          if (settled) return;
          settled = true;
          synth.cancel();
          next();
        }, 1500 + (list[idx].length * 120) / rate);
        const settle = (fn) => () => {
          if (settled) return;
          settled = true;
          clearTimeout(guard);
          fn();
        };
        u.onstart = () => opts.onPart && opts.onPart(idx);
        u.onend = settle(() => setTimeout(next, opts.gap || 120));
        u.onerror = settle(resolve);
        synth.speak(u);
      };
      next();
    });
  }

  // ---------- listening (speech recognition) ----------
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const canListen = !!Recognition;
  const canRecord = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);

  // Resolves { heard: [transcripts...] } or { error: "no-speech" | "not-allowed" | ... }
  function listen() {
    if (!canListen) return Promise.resolve({ error: "unsupported" });
    if (supported) synth.cancel();
    return new Promise((resolve) => {
      const rec = new Recognition();
      rec.lang = Store.setting("accent");
      rec.interimResults = false;
      rec.maxAlternatives = 5;
      let done = false;
      const finish = (r) => {
        if (done) return;
        done = true;
        clearTimeout(timer);
        resolve(r);
      };
      const timer = setTimeout(() => rec.stop(), 6000);
      rec.onresult = (e) => finish({ heard: [...e.results[0]].map((a) => a.transcript) });
      rec.onerror = (e) => finish({ error: e.error });
      rec.onend = () => finish({ error: "no-speech" });
      try {
        rec.start();
      } catch (err) {
        finish({ error: "start-failed" });
      }
    });
  }

  function normalize(s) {
    return s.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  }

  // True when any transcript contains the target word (or an accepted variant) as whole words.
  function matches(heard, item) {
    const targets = [item.word, ...(item.accept || [])].map(normalize);
    return heard.some((h) => {
      const text = " " + normalize(h) + " ";
      return targets.some((t) => text.includes(" " + t + " ") || text.includes(" " + t + "s "));
    });
  }

  // Fallback for browsers without recognition: record a short clip and return its URL.
  async function record(ms = 2500) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    const chunks = [];
    rec.ondataavailable = (e) => chunks.push(e.data);
    const stopped = new Promise((r) => (rec.onstop = r));
    rec.start();
    await new Promise((r) => setTimeout(r, ms));
    rec.stop();
    await stopped;
    stream.getTracks().forEach((t) => t.stop());
    return URL.createObjectURL(new Blob(chunks, { type: rec.mimeType }));
  }

  window.Speech = {
    supported,
    say,
    stop: () => supported && synth.cancel(),
    canListen,
    canRecord,
    listen,
    matches,
    record,
  };
})();
