// The places on the big map, in the order the road passes them, and the stops at each in order along its own road.
// The map is in three regions, one per level (REGIONS); each place is in one region and holds that level's lessons.
// Keep a place to six stops at most: a new lesson that doesn't fit goes on a new place.
// "write" is the tracing pad; "scene-<id>" are the picture dictionaries (window.SCENES).
// The big map and each place's own map (with where its stops sit) are drawn in tools/art/build16.py (window.WORLD).
// Places are called "islands" in the code (ISLANDS, #/island/<id>), from when the home page was a sea of islands.
// A lesson that isn't listed here goes on the last place, below its map.
window.REGIONS = [
  { id: "meadow", level: 1, title: "Sunny Meadow", zh: "阳光草原" },
  { id: "forest", level: 2, title: "The Forest", zh: "森林" },
  { id: "snow", level: 3, title: "Snowy Mountains", zh: "雪山和海湾" },
];

window.ISLANDS = [
  { id: "abc", region: "meadow", title: "ABC Corner", zh: "字母角", stops: ["alphabet", "hello", "write"] },
  { id: "school", region: "meadow", title: "School", zh: "学校", stops: ["school", "people", "snacks", "scene-classroom"] },
  { id: "num", region: "meadow", title: "Rainbow Hill", zh: "彩虹山", stops: ["numbers", "colors", "scene-sunny"] },
  { id: "town", region: "meadow", title: "My Town", zh: "小镇", stops: ["body", "family", "clothes", "sports"] },
  { id: "home", region: "meadow", title: "Home", zh: "家", stops: ["house", "room", "food", "scene-kitchen"] },
  { id: "farm", region: "meadow", title: "The Farm", zh: "农场", stops: ["farm", "fruits", "animals", "scene-farm"] },
  { id: "city", region: "meadow", title: "The City", zh: "城市", stops: ["vehicles", "zoo", "toys", "scene-market"] },
  { id: "mushroom", region: "forest", title: "Mushroom Village", zh: "蘑菇村", stops: ["feelings", "actions", "day"] },
  { id: "treehouse", region: "forest", title: "Tree House", zh: "树屋", stops: ["phonics", "opposites", "howmany"] },
  { id: "nature", region: "forest", title: "Forest Glade", zh: "林中空地", stops: ["where", "athome", "scene-park"] },
  { id: "station", region: "snow", title: "Weather Station", zh: "气象站", stops: ["weather", "shapes", "jobs"] },
  { id: "beach", region: "snow", title: "The Cove", zh: "海湾", stops: ["sea", "bugs", "vegetables", "scene-beach"] },
];
