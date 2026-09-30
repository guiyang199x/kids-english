// Picture stories: a few short pages each, told with words the lessons teach.
// A page's picture is put together from ART: `bg` is the background, and each sprite is one more picture on top.
// A sprite's x and y are where its middle sits and w is its width, all in % of the background; tapping a sprite
// with a `word` says it, and `anim` is the move it makes (the "I can…" moves: swim, jump, dance...).
// Words in `text` that a lesson teaches can be tapped for their picture; `links` picks the lesson when a word is
// in more than one with different meanings ("orange" the color, not the fruit).
// A story belongs to an `island`, or to a seasonal `visit` (js/content/visits.js) such as the Ghost Ship.
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
  {
    id: "pip-ghost-ship",
    visit: "halloween",
    level: 1,
    title: "Pip and the Ghost Ship",
    zh: "Pip 和幽灵船",
    color: "#6b4fa0",
    tint: "#efe9fa",
    cover: "ghost",
    links: { bat: "halloween", spider: "halloween", moon: "halloween", happy: "feelings" },
    pages: [
      {
        bg: "_scene-ghost",
        sprites: [{ art: "_pip_think", x: 20, y: 74, w: 20 }],
        text: "Look at the moon. What is that?",
        zh: "看，月亮。那是什么？",
      },
      {
        bg: "_scene-ghost",
        sprites: [
          { art: "_pip_think", x: 20, y: 74, w: 20 },
          { art: "ghost", x: 42, y: 44, w: 18, word: "ghost", anim: "jump" },
        ],
        text: "It is a big boat. A ghost says boo!",
        zh: "是一艘大船。一个小幽灵说：“嘣！”",
      },
      {
        bg: "_scene-ghost",
        sprites: [
          { art: "_pip_think", x: 18, y: 74, w: 20, word: "scared", anim: "read" },
          { art: "ghost", x: 38, y: 66, w: 18, word: "happy", anim: "dance" },
        ],
        text: "Pip is scared. But the ghost is happy.",
        zh: "Pip 害怕了。可是小幽灵很开心。",
      },
      {
        bg: "_scene-ghost",
        sprites: [
          { art: "_pip_cheer", x: 18, y: 72, w: 20 },
          { art: "bat", x: 38, y: 36, w: 16, word: "bat", anim: "dance" },
          { art: "spider", x: 44, y: 80, w: 14, word: "spider", anim: "dance" },
        ],
        text: "A bat and a spider dance.",
        zh: "一只蝙蝠和一只蜘蛛在跳舞。",
      },
      {
        bg: "_scene-ghost",
        sprites: [
          { art: "_pip_cheer", x: 22, y: 71, w: 22, word: "happy", anim: "jump" },
          { art: "ghost", x: 44, y: 66, w: 16, word: "ghost" },
          { art: "candy", x: 34, y: 86, w: 12, word: "candy", anim: "dance" },
        ],
        text: "The ghost has candy for Pip. Happy Halloween!",
        zh: "小幽灵给 Pip 带来了糖果。万圣节快乐！",
      },
    ],
  },
];
