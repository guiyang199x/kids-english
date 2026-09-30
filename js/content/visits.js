// Visitors that come to the world map for a season: a ship with its own lesson and stories, drawn on the map by
// tools/art/build16.py (`visit` in each layout) and build24.py. `from` and `to` are [month, day], both included,
// every year. The lesson is on no island and doesn't count toward the child's level; the stories name the visit
// in their `visit` instead of an island.
window.VISITS = [
  {
    id: "halloween",
    title: "Ghost Ship",
    zh: "幽灵船",
    from: [10, 1],
    to: [11, 7],
    hello: "It's here for Halloween, and sails away after November 7.",
    helloZh: "万圣节限定！11 月 7 日之后就开走啦。",
    lesson: "halloween",
    art: "_ghost-ship",
    color: "#6b4fa0",
    tint: "#efe9fa",
  },
];
