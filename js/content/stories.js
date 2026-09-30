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
    id: "hello-monkey",
    island: "abc",
    level: 1,
    title: "Hello, Monkey!",
    zh: "你好，小猴子！",
    color: "#e2556f",
    tint: "#fde7ec",
    cover: "_pip",
    pages: [
      {
        bg: "_scene-classroom",
        sprites: [{ art: "_pip", x: 30, y: 70, w: 20 }],
        text: "Hello! It is morning.",
        zh: "你好！现在是早上。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "_pip_think", x: 28, y: 70, w: 20 },
          { art: "monkey", x: 64, y: 72, w: 20, word: "monkey", anim: "jump" },
        ],
        text: "Look! A monkey says hello.",
        zh: "看！一只小猴子在打招呼。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "_pip", x: 28, y: 70, w: 20 },
          { art: "monkey", x: 64, y: 72, w: 20, word: "monkey" },
          { art: "kite", x: 46, y: 42, w: 14, word: "kite", anim: "dance" },
        ],
        text: "Hi! I have a kite.",
        zh: "嗨！我有一只风筝。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "_pip_think", x: 32, y: 70, w: 20, word: "read", anim: "read" },
          { art: "monkey", x: 58, y: 72, w: 20, word: "read", anim: "read" },
        ],
        text: "Pip and the monkey read the book.",
        zh: "Pip 和小猴子一起看书。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "_pip", x: 30, y: 70, w: 20, word: "goodbye", anim: "jump" },
          { art: "monkey", x: 66, y: 72, w: 20, word: "goodbye", anim: "jump" },
        ],
        text: "Goodbye! Thank you!",
        zh: "再见！谢谢你！",
      },
    ],
  },
  {
    id: "at-school",
    island: "school",
    level: 1,
    title: "At School",
    zh: "在学校",
    color: "#3a79b5",
    tint: "#e3eefa",
    cover: "crayon",
    links: { paint: "school" },
    pages: [
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "boy", x: 34, y: 72, w: 20, word: "boy", anim: "jump" },
          { art: "girl", x: 64, y: 72, w: 20, word: "girl", anim: "jump" },
        ],
        text: "Look! A boy and a girl.",
        zh: "看！一个男孩和一个女孩。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "boy", x: 34, y: 72, w: 20, word: "boy" },
          { art: "crayon", x: 58, y: 70, w: 18, word: "crayon", anim: "draw" },
        ],
        text: "The boy has a crayon.",
        zh: "男孩有一支蜡笔。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "girl", x: 36, y: 72, w: 20, word: "girl" },
          { art: "paint", x: 62, y: 72, w: 18, word: "paint", anim: "dance" },
        ],
        text: "The girl can paint.",
        zh: "女孩会画画。",
      },
      {
        bg: "_scene-classroom",
        sprites: [
          { art: "burger", x: 40, y: 70, w: 16, word: "burger", anim: "jump" },
          { art: "chips", x: 62, y: 70, w: 14, word: "chips", anim: "jump" },
        ],
        text: "They have burgers and chips for lunch.",
        zh: "他们午饭吃汉堡和薯条。",
      },
      {
        bg: "_scene-classroom",
        sprites: [{ art: "friend", x: 50, y: 72, w: 26, word: "friend", anim: "dance" }],
        text: "They are friends. They are happy!",
        zh: "他们是好朋友。他们很开心！",
      },
    ],
  },
  {
    id: "count-colors",
    island: "num",
    level: 1,
    title: "One, Two, Three Colors",
    zh: "一二三，颜色多",
    color: "#4a9be8",
    tint: "#e3f0ff",
    cover: "red",
    pages: [
      {
        bg: "_scene",
        sprites: [{ art: "red", x: 50, y: 70, w: 16, word: "red", anim: "jump" }],
        text: "One red crayon.",
        zh: "一支红色的蜡笔。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "blue", x: 40, y: 70, w: 16, word: "blue", anim: "jump" },
          { art: "blue", x: 60, y: 70, w: 16, word: "blue", anim: "jump" },
        ],
        text: "Two blue crayons.",
        zh: "两支蓝色的蜡笔。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "yellow", x: 32, y: 70, w: 16, word: "yellow", anim: "jump" },
          { art: "yellow", x: 50, y: 70, w: 16, word: "yellow", anim: "jump" },
          { art: "yellow", x: 68, y: 70, w: 16, word: "yellow", anim: "jump" },
        ],
        text: "Three yellow crayons.",
        zh: "三支黄色的蜡笔。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip", x: 36, y: 72, w: 20, word: "draw", anim: "draw" },
          { art: "sun", x: 62, y: 50, w: 18, word: "sun", anim: "dance" },
        ],
        text: "Pip can draw a sun.",
        zh: "Pip 会画太阳。",
      },
      {
        bg: "_scene",
        sprites: [{ art: "_pip_cheer", x: 50, y: 72, w: 22, word: "happy", anim: "jump" }],
        text: "Red, blue, yellow. One, two, three!",
        zh: "红、蓝、黄。一、二、三！",
      },
    ],
  },
  {
    id: "pip-can-dance",
    island: "mushroom",
    level: 2,
    title: "Pip Can Dance",
    zh: "Pip 会跳舞",
    color: "#2f8fd8",
    tint: "#e2f1ff",
    cover: "dance",
    pages: [
      {
        bg: "_scene-park",
        sprites: [{ art: "_pip_think", x: 40, y: 72, w: 20, word: "sleepy", anim: "read" }],
        text: "It is morning. Pip is sleepy.",
        zh: "早上了。Pip 还很困。",
      },
      {
        bg: "_scene-park",
        sprites: [{ art: "_pip", x: 36, y: 72, w: 20, word: "run", anim: "run" }],
        text: "Pip can run!",
        zh: "Pip 会跑！",
      },
      {
        bg: "_scene-park",
        sprites: [{ art: "_pip_cheer", x: 50, y: 70, w: 22, word: "dance", anim: "dance" }],
        text: "He can jump and dance.",
        zh: "他会跳，还会跳舞。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip", x: 30, y: 72, w: 20 },
          { art: "duck", x: 20, y: 84, w: 12, word: "duck", anim: "swim" },
        ],
        text: "Look! The duck can swim.",
        zh: "看！鸭子会游泳。",
      },
      {
        bg: "_scene-park",
        sprites: [{ art: "_pip_cheer", x: 50, y: 70, w: 22, word: "happy", anim: "jump" }],
        text: "In the afternoon, Pip is happy!",
        zh: "到了下午，Pip 很开心！",
      },
    ],
  },
  {
    id: "where-cat",
    island: "nature",
    level: 2,
    title: "Where Is the Cat?",
    zh: "小猫在哪里？",
    color: "#2f9a8f",
    tint: "#e1f5f2",
    cover: "cat",
    links: { cat: "animals", table: "room" },
    pages: [
      {
        bg: "_scene-kitchen",
        sprites: [{ art: "_pip_think", x: 50, y: 70, w: 20 }],
        text: "Where is the cat?",
        zh: "小猫在哪里？",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip_think", x: 30, y: 70, w: 18 },
          { art: "rug", x: 62, y: 84, w: 28, word: "rug" },
        ],
        text: "Is it on the rug? No!",
        zh: "在地毯上吗？不在！",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip_think", x: 30, y: 70, w: 18 },
          { art: "cupboard", x: 62, y: 66, w: 20, word: "cupboard" },
        ],
        text: "Is it in the cupboard? No!",
        zh: "在橱柜里吗？不在！",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip_think", x: 30, y: 70, w: 18 },
          { art: "table", x: 62, y: 76, w: 26, word: "table" },
        ],
        text: "Is it under the table? No!",
        zh: "在桌子下面吗？不在！",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip_cheer", x: 28, y: 70, w: 18, word: "happy", anim: "jump" },
          { art: "mirror", x: 58, y: 66, w: 18, word: "mirror" },
          { art: "cat", x: 74, y: 80, w: 16, word: "cat", anim: "jump" },
        ],
        text: "Here it is! The cat is next to the mirror.",
        zh: "在这儿！小猫在镜子旁边。",
      },
    ],
  },
  {
    id: "big-small",
    island: "treehouse",
    level: 2,
    title: "Big and Small",
    zh: "大和小",
    color: "#c96a1b",
    tint: "#fdeede",
    cover: "ball",
    links: { ball: "toys" },
    pages: [
      {
        bg: "_scene",
        sprites: [
          { art: "_pip", x: 30, y: 72, w: 20 },
          { art: "ball", x: 48, y: 86, w: 14, word: "big", anim: "jump" },
        ],
        text: "Pip has a big ball.",
        zh: "Pip 有一个大球。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "dog", x: 66, y: 80, w: 20, word: "dog", anim: "run" },
          { art: "ball", x: 52, y: 88, w: 6, word: "small", anim: "jump" },
        ],
        text: "The dog has a small ball.",
        zh: "小狗有一个小球。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_cheer", x: 30, y: 72, w: 20 },
          { art: "dog", x: 66, y: 80, w: 20, word: "dog", anim: "jump" },
        ],
        text: "One, two, three. Let's play!",
        zh: "一、二、三。我们来玩吧！",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_think", x: 30, y: 72, w: 20 },
          { art: "_shirt-dirty", x: 58, y: 80, w: 18, word: "dirty" },
        ],
        text: "Oh no! My shirt is dirty.",
        zh: "哎呀！我的衣服脏了。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_cheer", x: 30, y: 72, w: 20, word: "happy", anim: "jump" },
          { art: "_shirt-clean", x: 58, y: 80, w: 18, word: "clean" },
        ],
        text: "Now it is clean. Pip is happy.",
        zh: "现在干净了。Pip 很开心。",
      },
    ],
  },
  {
    id: "pip-day",
    island: "home",
    level: 2,
    title: "Pip's Day",
    zh: "Pip 的一天",
    color: "#e0703a",
    tint: "#fff0e6",
    cover: "morning",
    pages: [
      {
        bg: "_scene-kitchen",
        sprites: [{ art: "_pip", x: 50, y: 70, w: 20 }],
        text: "It is morning. Pip has breakfast.",
        zh: "现在是早上。Pip 在吃早饭。",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip_think", x: 50, y: 70, w: 20 },
          { art: "egg", x: 30, y: 58, w: 11, word: "egg", anim: "jump" },
          { art: "milk", x: 70, y: 58, w: 11, word: "milk", anim: "jump" },
        ],
        text: "An egg and milk for Pip.",
        zh: "给 Pip 一个鸡蛋和一杯牛奶。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_cheer", x: 34, y: 72, w: 20, word: "play", anim: "jump" },
          { art: "kite", x: 62, y: 40, w: 16, word: "kite", anim: "dance" },
        ],
        text: "In the afternoon, Pip can play.",
        zh: "下午，Pip 可以去玩。",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "_pip", x: 40, y: 70, w: 20 },
          { art: "mom", x: 66, y: 66, w: 20, word: "mom" },
        ],
        text: "In the evening, Pip has dinner with Mom.",
        zh: "傍晚，Pip 和妈妈一起吃晚饭。",
      },
      {
        bg: "_scene-kitchen",
        sprites: [
          { art: "bed", x: 50, y: 76, w: 34, word: "bed" },
          { art: "_pip_think", x: 50, y: 62, w: 16, word: "sleepy", anim: "read" },
        ],
        text: "At night, Pip is in bed. He is sleepy.",
        zh: "晚上，Pip 躺在床上。他困了。",
      },
    ],
  },
  {
    id: "cold-day",
    island: "town",
    level: 1,
    title: "A Cold Day",
    zh: "冷冷的一天",
    color: "#4a7fd0",
    tint: "#e6effc",
    cover: "coat",
    links: { hat: "clothes", cold: "weather" },
    pages: [
      {
        bg: "_scene",
        sprites: [{ art: "_pip_think", x: 34, y: 72, w: 20, word: "sad", anim: "read" }],
        text: "It is cold. Pip is sad.",
        zh: "天好冷。Pip 不开心。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_think", x: 30, y: 72, w: 20 },
          { art: "mom", x: 62, y: 70, w: 20, word: "mom" },
          { art: "coat", x: 46, y: 50, w: 14, word: "coat", anim: "dance" },
        ],
        text: "Mom has a coat for Pip.",
        zh: "妈妈给 Pip 拿来一件外套。",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip", x: 34, y: 72, w: 20 },
          { art: "hat", x: 56, y: 60, w: 14, word: "hat", anim: "jump" },
        ],
        text: "And a red hat, too!",
        zh: "还有一顶红帽子！",
      },
      {
        bg: "_scene",
        sprites: [
          { art: "_pip_cheer", x: 34, y: 72, w: 20, word: "run", anim: "run" },
          { art: "dog", x: 62, y: 80, w: 18, word: "dog", anim: "run" },
        ],
        text: "Now Pip can run and jump.",
        zh: "现在 Pip 可以跑跑跳跳了。",
      },
      {
        bg: "_scene",
        sprites: [{ art: "_pip_cheer", x: 40, y: 72, w: 22, word: "happy", anim: "jump" }],
        text: "Pip is not cold. He is happy!",
        zh: "Pip 不冷了。他很开心！",
      },
    ],
  },
  {
    id: "rainy-day",
    island: "station",
    level: 1,
    title: "Rain in the Park",
    zh: "公园里下雨了",
    color: "#3f8fd0",
    tint: "#e4f1fb",
    cover: "rainy",
    links: { duck: "farm" },
    pages: [
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip", x: 28, y: 72, w: 20 },
          { art: "butterfly", x: 56, y: 40, w: 14, word: "butterfly", anim: "dance" },
        ],
        text: "It is sunny. Pip sees a butterfly.",
        zh: "天气晴朗。Pip 看见一只蝴蝶。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip_think", x: 28, y: 72, w: 20 },
          { art: "cloudy", x: 60, y: 30, w: 20, word: "cloudy" },
        ],
        text: "Oh! It is cloudy.",
        zh: "哦！天阴了。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "rainy", x: 50, y: 28, w: 22, word: "rainy" },
          { art: "duck", x: 62, y: 80, w: 14, word: "duck", anim: "swim" },
        ],
        text: "Now it is rainy. The duck is happy.",
        zh: "现在下雨了。鸭子很开心。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip", x: 36, y: 74, w: 20 },
          { art: "umbrella", x: 36, y: 44, w: 20, word: "umbrella" },
        ],
        text: "Pip has a big umbrella.",
        zh: "Pip 撑着一把大伞。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip_cheer", x: 30, y: 72, w: 20 },
          { art: "snail", x: 56, y: 86, w: 12, word: "snail", anim: "run" },
          { art: "frog", x: 72, y: 82, w: 14, word: "frog", anim: "jump" },
        ],
        text: "Look! A snail and a frog.",
        zh: "看！一只蜗牛和一只青蛙。",
      },
    ],
  },
  {
    id: "farm-friends",
    island: "farm",
    level: 1,
    title: "Farm Friends",
    zh: "农场朋友",
    color: "#6f9a2e",
    tint: "#eef7df",
    cover: "cow",
    links: { cow: "farm", horse: "farm", sheep: "farm", duck: "farm" },
    pages: [
      {
        bg: "_scene-farm",
        sprites: [{ art: "_pip", x: 74, y: 70, w: 18 }],
        text: "Pip can see a cow and a horse.",
        zh: "Pip 看见了一头奶牛和一匹马。",
      },
      {
        bg: "_scene-farm",
        sprites: [
          { art: "_pip_cheer", x: 74, y: 70, w: 18 },
          { art: "duck", x: 40, y: 86, w: 14, word: "duck", anim: "swim" },
        ],
        text: "The duck can swim.",
        zh: "鸭子会游泳。",
      },
      {
        bg: "_scene-farm",
        sprites: [
          { art: "goat", x: 36, y: 80, w: 16, word: "goat", anim: "jump" },
          { art: "donkey", x: 60, y: 78, w: 16, word: "donkey", anim: "dance" },
        ],
        text: "Look at the goat and the donkey.",
        zh: "看那只山羊和那头驴。",
      },
      {
        bg: "_scene-farm",
        sprites: [
          { art: "_pip_think", x: 70, y: 70, w: 18 },
          { art: "mouse", x: 44, y: 88, w: 9, word: "mouse", anim: "run" },
        ],
        text: "Oh! A little mouse. It is small.",
        zh: "哦！一只小老鼠。它很小。",
      },
      {
        bg: "_scene-farm",
        sprites: [{ art: "_pip", x: 72, y: 70, w: 20, word: "goodbye", anim: "jump" }],
        text: "Goodbye, cow! Goodbye, sheep!",
        zh: "再见，奶牛！再见，绵羊！",
      },
    ],
  },
  {
    id: "pip-can-play",
    island: "city",
    level: 1,
    title: "We Can Play",
    zh: "我们会玩",
    color: "#1f8a70",
    tint: "#e1f5ef",
    cover: "football",
    pages: [
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip", x: 30, y: 72, w: 20 },
          { art: "football", x: 48, y: 86, w: 10, word: "football", anim: "jump" },
        ],
        text: "Pip has a football.",
        zh: "Pip 有一个足球。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip_cheer", x: 30, y: 72, w: 20, word: "kick", anim: "kick" },
          { art: "football", x: 58, y: 70, w: 10, word: "football", anim: "kick" },
        ],
        text: "He can kick the ball.",
        zh: "他会踢球。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "monkey", x: 40, y: 76, w: 18, word: "monkey", anim: "sing" },
          { art: "guitar", x: 58, y: 78, w: 14, word: "guitar", anim: "dance" },
        ],
        text: "The monkey can play the guitar.",
        zh: "小猴子会弹吉他。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "rabbit", x: 44, y: 74, w: 18, word: "rabbit", anim: "jump" },
          { art: "skateboard", x: 44, y: 88, w: 20, word: "skateboard", anim: "run" },
        ],
        text: "The rabbit has a skateboard.",
        zh: "小兔子有一块滑板。",
      },
      {
        bg: "_scene-park",
        sprites: [
          { art: "_pip_cheer", x: 30, y: 72, w: 20, word: "happy", anim: "jump" },
          { art: "monkey", x: 54, y: 76, w: 16, word: "monkey", anim: "dance" },
          { art: "rabbit", x: 72, y: 76, w: 16, word: "rabbit", anim: "jump" },
        ],
        text: "We can play! We are happy.",
        zh: "我们会玩！我们很开心。",
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
