// Pip TV: short shows on the TV in Pip's house (#/tv). Each one plays by itself, in three parts:
//   chant - a rhyme to a drum beat (`bpm`). Pip says a line, then it's the child's turn to say it back. A line can
//           show a picture (`pic`, any ART key).
//   talk  - Pip and a friend talk; each of the `cast` has a picture (`art`) and a voice (`pitch`). A line can show a
//           picture between them (`pic`).
//   then the same talk again, with the child saying the friend's lines.
// All the chants are written for this site. tests/shows.test.js checks the words against the lessons, like the stories.
window.SHOWS = [
  {
    id: "hello",
    title: "Hello, Hello!",
    zh: "你好，你好！",
    color: "#e0784a",
    tint: "#ffece2",
    chant: {
      title: "The Hello Chant",
      zh: "打招呼歌",
      bpm: 100,
      lines: [
        { text: "Hello, hello, how are you?", zh: "你好，你好，你好吗？", pic: "_pip" },
        { text: "I am happy, thank you!", zh: "我很开心，谢谢你！", pic: "happy" },
        { text: "Hello, hello, one, two, three.", zh: "你好，你好，一二三。", pic: "three" },
        { text: "Let's play, you and me!", zh: "我们一起玩吧，你和我！", pic: "ball" },
      ],
    },
    talk: {
      title: "Meet Momo",
      zh: "认识 Momo",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Momo", art: "monkey", pitch: 1.45 },
      ],
      lines: [
        { who: 0, text: "Hello! I am Pip.", zh: "你好！我是 Pip。" },
        { who: 1, text: "Hi, Pip! My name is Momo.", zh: "嗨，Pip！我叫 Momo。" },
        { who: 0, text: "How old are you, Momo?", zh: "Momo，你几岁了？" },
        { who: 1, text: "I am six. How old are you?", zh: "我六岁。你几岁？", pic: "six" },
        { who: 0, text: "I am seven.", zh: "我七岁。", pic: "seven" },
        { who: 1, text: "Nice to meet you, Pip!", zh: "很高兴认识你，Pip！" },
        { who: 0, text: "Nice to meet you, too!", zh: "我也很高兴认识你！" },
      ],
    },
  },
  {
    id: "colors",
    title: "I See Red",
    zh: "我看见红色",
    color: "#8150c4",
    tint: "#f0e8fb",
    chant: {
      title: "Red, Red, I See Red",
      zh: "颜色歌",
      bpm: 96,
      lines: [
        { text: "Red, red, I see red.", zh: "红色，红色，我看见红色。", pic: "red" },
        { text: "A red apple on my bed.", zh: "我的床上有个红苹果。", pic: "apple" },
        { text: "Blue, blue, I see blue.", zh: "蓝色，蓝色，我看见蓝色。", pic: "blue" },
        { text: "A blue fish swims to you.", zh: "一条蓝色的鱼游向你。", pic: "fish" },
      ],
    },
    talk: {
      title: "What Color Is It?",
      zh: "它是什么颜色？",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Ollie", art: "owl", pitch: 0.9 },
      ],
      lines: [
        { who: 1, text: "Pip, look at my kite!", zh: "Pip，看我的风筝！", pic: "kite" },
        { who: 0, text: "Wow! What color is it?", zh: "哇！它是什么颜色的？" },
        { who: 1, text: "It is yellow and green.", zh: "它是黄色和绿色的。" },
        { who: 0, text: "I like yellow!", zh: "我喜欢黄色！", pic: "yellow" },
        { who: 1, text: "What is your favorite color?", zh: "你最喜欢什么颜色？" },
        { who: 0, text: "My favorite color is red.", zh: "我最喜欢红色。", pic: "red" },
      ],
    },
  },
  {
    id: "zoo",
    title: "At the Zoo",
    zh: "在动物园",
    color: "#c9822f",
    tint: "#fbefdc",
    chant: {
      title: "Animal Sounds",
      zh: "动物叫声歌",
      bpm: 104,
      lines: [
        { text: "The cat says meow, meow, meow.", zh: "小猫喵喵喵。", pic: "cat" },
        { text: "The dog says woof, woof, woof.", zh: "小狗汪汪汪。", pic: "dog" },
        { text: "The lion says roar, roar, roar!", zh: "狮子嗷呜嗷呜！", pic: "lion" },
        { text: "The owl says hoot, hoot, hoot.", zh: "猫头鹰咕咕咕。", pic: "owl" },
      ],
    },
    talk: {
      title: "What's This?",
      zh: "这是什么？",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Gigi", art: "giraffe", pitch: 1.3 },
      ],
      lines: [
        { who: 0, text: "Gigi, what's this?", zh: "Gigi，这是什么？" },
        { who: 1, text: "It's a monkey!", zh: "是一只猴子！", pic: "monkey" },
        { who: 0, text: "Is it big?", zh: "它大吗？" },
        { who: 1, text: "No. It is small.", zh: "不大，它很小。" },
        { who: 0, text: "What's that?", zh: "那是什么？" },
        { who: 1, text: "It's an elephant. It is very big!", zh: "是一头大象。它非常大！", pic: "elephant" },
      ],
    },
  },
  {
    id: "ican",
    title: "I Can Jump",
    zh: "我会跳",
    color: "#2f8fd8",
    tint: "#e2f1ff",
    chant: {
      title: "Jump, Jump, I Can Jump",
      zh: "我会做歌",
      bpm: 112,
      lines: [
        { text: "Jump, jump, I can jump.", zh: "跳呀跳，我会跳。", pic: "jump" },
        { text: "Run, run, I can run.", zh: "跑呀跑，我会跑。", pic: "run" },
        { text: "Swim, swim, I can swim.", zh: "游呀游，我会游泳。", pic: "swim" },
        { text: "Dance, dance, it is fun!", zh: "跳舞跳舞，真好玩！", pic: "dance" },
      ],
    },
    talk: {
      title: "Can You Fly?",
      zh: "你会飞吗？",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Penny", art: "penguin", pitch: 1.35 },
      ],
      lines: [
        { who: 0, text: "Penny, can you swim?", zh: "Penny，你会游泳吗？", pic: "swim" },
        { who: 1, text: "Yes, I can!", zh: "是的，我会！" },
        { who: 0, text: "Can you fly?", zh: "你会飞吗？" },
        { who: 1, text: "No, I can't. Can you fly, Pip?", zh: "不，我不会。Pip，你会飞吗？" },
        { who: 0, text: "No! But I can dance!", zh: "不会！但是我会跳舞！", pic: "dance" },
      ],
    },
  },
  {
    id: "shop",
    title: "At the Shop",
    zh: "在商店",
    color: "#5e9a2e",
    tint: "#ecf6e2",
    chant: {
      title: "Yummy Fruit",
      zh: "水果歌",
      bpm: 100,
      lines: [
        { text: "Apples, apples, one, two, three.", zh: "苹果，苹果，一二三。", pic: "apple" },
        { text: "Bananas for you and me.", zh: "香蕉给你也给我。", pic: "banana" },
        { text: "Grapes, grapes, purple and green.", zh: "葡萄，葡萄，紫色和绿色。", pic: "grapes" },
        { text: "I like bananas, yum, yum, yum!", zh: "我喜欢香蕉，好吃好吃！", pic: "banana" },
      ],
    },
    talk: {
      title: "Can I Have an Apple?",
      zh: "我可以要一个苹果吗？",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Ben", art: "bear", pitch: 0.8 },
      ],
      lines: [
        { who: 1, text: "Hello, Pip! Can I help you?", zh: "你好，Pip！要买点什么？" },
        { who: 0, text: "Can I have an apple, please?", zh: "我可以要一个苹果吗？", pic: "apple" },
        { who: 1, text: "Here you are.", zh: "给你。" },
        { who: 0, text: "Thank you! And two bananas, please.", zh: "谢谢！再要两根香蕉。", pic: "banana" },
        { who: 1, text: "Here you are. Bye-bye, Pip!", zh: "给你。再见，Pip！" },
        { who: 0, text: "Bye-bye, Ben!", zh: "再见，Ben！" },
      ],
    },
  },
  {
    id: "count",
    title: "Count With Me",
    zh: "一起数数",
    color: "#d65b9a",
    tint: "#fde8f2",
    chant: {
      title: "One, Two, Three, Four, Five",
      zh: "数数歌",
      bpm: 108,
      lines: [
        { text: "One, two, three, four, five.", zh: "一、二、三、四、五。", pic: "five" },
        { text: "Five little fish, swim, swim, swim!", zh: "五条小鱼，游呀游！", pic: "fish" },
        { text: "Six, seven, eight, nine, ten.", zh: "六、七、八、九、十。", pic: "ten" },
        { text: "Let's count again, my friend!", zh: "朋友，我们再数一遍！", pic: "_pip_cheer" },
      ],
    },
    talk: {
      title: "How Many?",
      zh: "有几个？",
      cast: [
        { name: "Pip", art: "_pip", pitch: 1.1 },
        { name: "Rosie", art: "rabbit", pitch: 1.5 },
      ],
      lines: [
        { who: 0, text: "Rosie, how many carrots?", zh: "Rosie，有几根胡萝卜？", pic: "carrot" },
        { who: 1, text: "One, two, three. Three carrots!", zh: "一、二、三。三根胡萝卜！", pic: "three" },
        { who: 0, text: "How many for me?", zh: "有几根给我？" },
        { who: 1, text: "One for you, and two for me!", zh: "一根给你，两根给我！" },
        { who: 0, text: "Thank you, Rosie!", zh: "谢谢你，Rosie！" },
      ],
    },
  },
];
