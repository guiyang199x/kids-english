// The islands in the order Pip sails them, and the stops on each in order along its road. Keep an island to six
// stops at most: a new lesson that doesn't fit goes on a new island.
// "write" is the tracing pad; "scene-<id>" are the picture dictionaries (window.SCENES).
// Each island's picture and where its stops sit are drawn in tools/art/build16.py (window.WORLD).
// A lesson that isn't listed here goes on the last island, below the map if the road has no room for it.
window.ISLANDS = [
  { id: "abc", title: "ABC Island", zh: "字母岛", stops: ["alphabet", "phonics", "hello"] },
  { id: "school", title: "School Island", zh: "学校岛", stops: ["school", "people", "snacks", "write", "scene-classroom"] },
  { id: "num", title: "Rainbow Island", zh: "数字彩虹岛", stops: ["numbers", "howmany", "opposites", "shapes", "colors"] },
  { id: "town", title: "My Town", zh: "我的小镇", stops: ["feelings", "body", "actions", "family", "clothes"] },
  { id: "home", title: "Home Island", zh: "家园岛", stops: ["house", "room", "day", "food", "athome", "scene-kitchen"] },
  { id: "nature", title: "Nature Island", zh: "自然岛", stops: ["animals", "bugs", "weather", "scene-sunny", "scene-park"] },
  { id: "farm", title: "Farm Island", zh: "农场岛", stops: ["farm", "fruits", "vegetables", "scene-farm"] },
  { id: "city", title: "City Island", zh: "城市岛", stops: ["vehicles", "zoo", "jobs", "sports", "where", "scene-market"] },
  { id: "beach", title: "Beach Island", zh: "海滩岛", stops: ["scene-beach", "sea", "toys"] },
];
