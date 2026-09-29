// Picture stories: a few short pages each, told with words the lessons teach.
// A page's picture is put together from ART: `bg` is the background, and each sprite is one more picture on top.
// A sprite's x and y are where its middle sits and w is its width, all in % of the background; tapping a sprite
// with a `word` says it, and `anim` is the move it makes (the "I can…" moves: swim, jump, dance...).
// Words in `text` that a lesson teaches can be tapped for their picture; `links` picks the lesson when a word is
// in more than one with different meanings ("orange" the color, not the fruit).
// tests/stories.test.js checks that every word is taught somewhere (or is on its short list of little words).
window.STORIES = [
  {
    id: "pip-beach",
    island: "beach",
    level: 2,
    title: "Pip at the Beach",
    zh: "Pip 去海滩",
    color: "#0f8a9e",
    tint: "#e3f6f8",
    cover: "_pip_cheer",
    links: { orange: "colors" },
    pages: [
      {
        bg: "_scene-beach",
        sprites: [{ art: "_pip", x: 57, y: 64, w: 22 }],
        text: "Pip goes to the beach.",
        zh: "Pip 去海滩。",
      },
      {
        bg: "_scene-beach",
        sprites: [{ art: "_pip_think", x: 57, y: 64, w: 22 }],
        text: "The sun is hot. Pip has a red bucket.",
        zh: "太阳很热。Pip 有一个红色的小桶。",
      },
      {
        bg: "_scene-beach",
        sprites: [
          { art: "_pip_think", x: 38, y: 66, w: 20 },
          { art: "starfish", x: 61, y: 86, w: 14, word: "starfish", anim: "dance" },
        ],
        text: "Look! A starfish. It is orange.",
        zh: "看！一只海星。它是橙色的。",
      },
      {
        bg: "_scene-beach",
        sprites: [
          { art: "whale", x: 58, y: 48, w: 40, word: "whale", anim: "swim" },
          { art: "_pip", x: 20, y: 70, w: 20 },
        ],
        text: "A big whale says hello.",
        zh: "一头大鲸鱼说你好。",
      },
      {
        bg: "_scene-beach",
        sprites: [{ art: "_pip_cheer", x: 50, y: 66, w: 26, word: "happy", anim: "jump" }],
        text: "Pip is happy. Bye-bye, beach!",
        zh: "Pip 很开心。再见，海滩！",
      },
    ],
  },
];
