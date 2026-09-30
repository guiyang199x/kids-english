// Pip's house (#/house): his room, with the sticker book on the desk, Pip TV, letters at the door and a shelf of stories.
// The room is ART["_home-room"] (tools/art/build23.py); WORLD.home.spots says where each thing's name plate sits.
(function () {
  const { app, bookHtml, bounce, zhLine } = LE.ui;
  const { albumTotals, unanswered } = LE.home;
  const { visitNow } = LE.lesson;
  // Pip's storybooks: every island's, and a visitor's only while it's here.
  const books = () => {
    const visit = visitNow();
    return (window.STORIES || []).filter((s) => !s.visit || (visit && visit.id === s.visit));
  };

  // The things in the room, left to right.
  const PLACES = {
    books: { href: "#books", title: "Storybooks", zh: "绘本" },
    stickers: { href: "#/stickers", title: "Sticker Book", zh: "我的图鉴" },
    tv: { href: "#/tv", title: "Pip TV", zh: "Pip 电视台" },
    mail: { href: "#/mail", title: "Mailbox", zh: "信箱" },
  };

  function house() {
    const spots = window.WORLD.home.spots;
    const waiting = unanswered();
    const t = albumTotals();
    const extra = {
      stickers: `<span class="home-count">★ ${t.found}/${t.total}</span>`,
      mail: waiting ? `<span class="home-new">✉ New!</span>` : "",
      books: `<span class="home-count">📖 ${books().length}</span>`,
      tv: `<span class="home-count">📺 ${window.SHOWS.filter((s) => Store.shows.has(s.id)).length}/${window.SHOWS.length}</span>`,
    };
    const plate = (go) => {
      const p = PLACES[go];
      const [x, y] = spots[go];
      return `<a class="home-plate" data-go="${go}" href="${p.href}" style="left:${x}%;top:${y}%"><b>${p.title}</b>${zhLine(p.zh, "zh-sub")}${extra[go]}</a>`;
    };
    app.innerHTML = `
      <nav class="crumbs"><a href="#/">← World map</a></nav>
      <section class="home">
        <h1 class="home-title">Pip's House${zhLine("Pip 的小屋", "zh-sub")}</h1>
        <div class="home-room-wrap${waiting ? " has-mail" : ""}">
          ${ART["_home-room"]}
          ${Object.keys(PLACES).map(plate).join("")}
        </div>
      </section>
      <section class="isle-stories" id="books">
        <h2>📖 Pip's Storybooks${zhLine("Pip 的绘本", "zh-sub")}</h2>
        <div class="shelf">${books().map(bookHtml).join("")}</div>
      </section>`;

    const room = app.querySelector(".home-room-wrap");
    const shelf = app.querySelector("#books");
    // The storybooks are on this page, under the room: the shelf scrolls there instead of changing the address.
    function go(to) {
      if (to !== "books") return (location.hash = PLACES[to].href);
      Speech.say("Let's read a story!");
      shelf.scrollIntoView({ behavior: "smooth", block: "start" });
      bounce(shelf.querySelector(".shelf"));
    }
    room.querySelectorAll(".home-spot").forEach((g) => {
      g.addEventListener("click", () => go(g.dataset.go));
      g.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          go(g.dataset.go);
        }
      });
    });
    room.querySelector('.home-plate[data-go="books"]').addEventListener("click", (e) => {
      e.preventDefault();
      go("books");
    });
    // Pip says hello, and points out a letter that's waiting.
    Speech.say(waiting ? ["Welcome to my house!", "Look! A letter for you!"] : "Welcome to my house!", { gap: 300 });
  }

  LE.views.house = house;
})();
