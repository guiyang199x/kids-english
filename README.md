# Little English

A website for children learning English, with picture cards, spoken pronunciation and listening games. It's plain HTML, CSS and JavaScript, so there's nothing to install and no build step.

## Run it

Open `index.html` in Chrome, Edge or Safari. To serve it locally instead:

```bash
python3 -m http.server 5173
```

Then visit http://localhost:5173.

## Tests

The tests use Node's built-in test runner (Node 18 or newer), so there's still nothing to install:

```bash
node --test
```

## Features

- **Island map:** the home page is a sea with six theme islands: ABC Island, Rainbow Island (numbers, shapes, colors), My Town, Nature Island, City Island and Beach Island. Tap an island and Pip sails there in a little boat, then the map zooms into it. Islands a child hasn't visited yet stand far off on the horizon, pale and small; the first time Pip sails to one, it glides closer and takes its place on the map. Nothing is locked.
- **Inside an island:** each island has its own map (a road up a hill, a ring road around a town square, city streets, a boardwalk...) with one stop per lesson. A stop shows up to 3 stars from its best game scores, and the island adds them up. Pip walks from the dock to the stop he suggests (see "Levels"), or else the next one without stars; tap any stop and Pip walks there, then its card opens with Learn and the games.
- **Harder as a word gets known:** each game picks the words a child knows least first (new and missed ones, then the rest by their review box), and makes each question fit the word. A word that's new or was just missed is easy: 3 pictures in the listening game, its first letter already in place and no extra letters in Spell, no extra tile in Build. While it's being learned: 4 pictures, 2 extra letters, 1 extra tile. Once it's mastered: the other pictures are the words most like it (hat and bat for cat), 4 extra letters, 2 extra tiles.
- **Levels:** every lesson has a level, checked against the Cambridge Young Learners wordlists: 🌱 1 everyday words (ABC, colors, numbers, animals...), 🌿 2 the same kind of words in sentences and sounds (Where is it?, How many?, I can…, Feelings, Word Families), 🌳 3 harder words, mostly from the next Cambridge list, Movers (weather, jobs, sea animals, shapes, bugs, vegetables). A child starts at level 1 and moves up once 70% of the lessons at their level have 2 stars. Pip's bubble on the home map shows the level and how many of its lessons are done, and a "Next" button sails to the lesson he suggests: the first one in island order at the child's level or below with no stars yet, then one there with only 1 star, then the next level up. Each stop shows its level; one above the child's level has an orange ring and its card says "Challenge!". Nothing is locked. Grown-ups can pick a higher starting level in the settings ("Start at").
- **Pip:** the panda mascot waves on the home page and the lesson pages, sits in the corner of the games and cheers at each right answer, and shows up on the results screen.
- **Lessons:** ABC (A–Z), colors, feelings, animals, numbers (1–20; from 11 the picture is a row of ten and the ones under it), shapes, fruits, food, my body, family, weather, vehicles, clothes, jobs, things in my room, toys, sea animals, vegetables, bugs, **How many?** (one apple, two apples) **Where is it?** (in, on, under, next to, behind, in front of) **I can…** (run, jump, swim, dance, sing, read, draw, kick) and **Word Families** (phonics: -at, -an, -en, -ig, -og, -un), each shown as picture cards. In "I can…" each card also shows its sentence ("I can jump high."), and the picture acts out the word when tapped. In "How many?" the plural ending is underlined.
- **Pronunciation:** tap a card to hear the word and a short sentence. "Spell it" reads the word one letter at a time and highlights each letter as it's spoken.
- **Say it:** tap the microphone and say the word. The site listens and gives a star when it hears the word correctly. This needs Chrome or Edge, internet access, and the site opened from `http://localhost` (see "Run it"), not by double-clicking the file. In other browsers it records the child instead and plays it back after the teacher's voice so they can compare by ear.
- **Chinese hints (中文):** a switch in the header shows the Chinese meaning under each word and sentence.
- **Spell game:** see the picture, hear the word, and tap letter tiles in the right order. Two extra letters make it a little harder, and "Hint" makes the next letter glow.
- **Write:** trace each letter, capital and small, on four-line handwriting paper with a finger or mouse. Green numbered dots and arrows show where each stroke starts and which way it goes, and "Show me" animates the strokes in order (it plays automatically the first time). "Done" checks that the letter is covered and the strokes stay on it, then gives a star. If the strokes were in the wrong order, the child still gets the star, plus a gentle tip to start at dot 1.
- **Listening game:** hear a word, then tap the matching picture. In "Where is it?" it reads the whole sentence ("The cat is under the table.") instead. There are 5 rounds, and each correct first try earns a star. The best score for each lesson is saved in the browser.
- **Word Families (phonics):** cards are grouped by ending, with the first sound colored (**b**at). "Sound it" says the first sound, the ending and the word (buh… at… bat); tapping a family heading like "-at" chants the family. In the **Blend game** the ending is already there (_at) and the child picks the first sound; every choice makes a real word, so a wrong pick is read out ("That says hat. Find bat.").
- **Build game (句型搭积木):** see the picture, hear the sentence, and tap the word tiles in order to build it ("I can jump high."). One extra tile is another card's word, so the child has to look at the picture; in "How many?" the extra tile is the other form of the noun ("car" / "cars"). Phrases like "next to" stay one tile. It appears on every lesson with at least 3 short sentences (3–6 tiles, one sentence, no commas).
- **Count game:** in "How many?", count the pictures and tap the right number (1–10). Tapping each picture counts it out loud and puts a number on it; a wrong answer clears the numbers so the child can count again.
- **Pip says (动手做):** Pip gives an instruction and the child does it on the picture. In "My Body" they touch Pip ("Touch Pip's nose."), and he blinks, wiggles his ears or hops; tapping anywhere else tickles him. In "Where is it?" they drag the cat around a room ("Put the cat under the table."). Small children can also tap the cat and then tap where it goes. In "Colors" they pick a crayon and color a thing on a coloring page ("Color the ball blue."); tapping a crayon says its color. Doing the wrong thing reads out what the child did ("The cat is on the table. Try again."); after two misses the right place (and crayon) glows. There are 5 rounds, with a star for each first try. In "I can…" the child moves with Pip: he says a move ("Jump high!", "Swim like a fish!"), says "Ready? Go!" and acts it out until the child taps "I did it!". This one can't go wrong, so it doesn't count toward the island's stars.
- **Review (复习):** every game answer about a word is remembered, and each word comes back after a growing gap: the next day, then 2, 4, 8, 16 and 32 days, as long as the child keeps getting it right the first time. A word missed the first time is due again the same day. When at least 3 words are due, Pip offers "3 words miss you!" on the home map. The review is the listening game with up to 8 words from any lessons; a word missed there comes back once at the end. The results show which words got stronger and each word's level (5 dots). It's never required, and it doesn't change the islands' stars. Spelling and sentence building only move a word up, never down: getting a letter wrong isn't forgetting the word. "Say it" counts when it hears the word, but not when it doesn't, since speech recognition is often unsure.
- **Picture dictionary:** seven scenes (a sunny day, the park, the farm, the kitchen, the supermarket, the classroom, the beach), each with 9 labels to tap. A tap reads the word and a sentence, with the Chinese underneath. They have their own area on the home map, "Places to Explore".
- **Settings:** choose an American or British voice, a slow or normal speaking speed, and the level to start at.

Pronunciation uses the browser's built-in speech (Web Speech API), so voices vary between devices.

## Project layout

There's no build step, so the files are plain `<script>`s. `index.html` loads them in order, and each one only uses what's loaded above it. The page code shares its parts through one object, `window.LE`: each file takes what it needs at the top (`const { theme, stars } = LE.ui;`) and adds what it offers at the bottom.

- `index.html`: the page shell and the list of scripts
- `css/style.css`: all styles

Content (plain data, no page code):

- `js/content/data.js`: lesson content (words, sentences, colors). Add lessons here, each with a `level` (1–3, see "Levels"; `tools/wordlist/coverage.py` shows which Cambridge list its words are on). Pictures are looked up by word; if a word already has a different picture (like the fruit "orange" vs. the crayon), give the item an `art` key. Set `showSentence: true` on a lesson to print each sentence (and its `sentenceZh`) on the cards; give an item `move` to animate its picture on tap. Counting items use `count` and `thing` instead, and the picture is drawn as that many copies of `thing`. `COUNT_THINGS` lists what the count game can ask about. Phonics items have a `family` (their ending); the lesson's `families` and `ONSET_SOUNDS` hold how each ending and first sound is spelled for the speech engine (e.g. "buh" for b), since engines read single letters by name. A lesson with `pipSays` gets the Pip says game: its `art` is the picture, and each task names the `zone` to touch or drop the cat on, what Pip asks (`say`), and what's read out when that zone is picked (`is`), each with Chinese. For coloring (`type: "paint"`) the asks are made up from `things` and the lesson's crayons instead, and `paint` holds each crayon's color.
- `js/content/islands.js`: `ISLANDS` says which lessons are on which island, in order along its road. A lesson that isn't listed goes on the last island; if its road has no room for it, it shows up under "More on this island".
- `js/art.js`: the illustrations as inline SVG. This file is generated; don't edit it by hand.

Helpers that work on their own and know nothing about the pages:

- `js/store.js`: everything saved in the browser (settings, best scores, words said, letters written, islands visited, where the boat is, and each word's review schedule). It's the only file that uses `localStorage`; keys start with `le-`. If storage is blocked, progress lasts until the page closes.
- `js/srs.js`: when each word comes back for review (Leitner boxes 0–5). A right first answer on a word that's due moves it up a box and doubles the wait (1, 2, 4 … 32 days); a wrong one sends it back to box 0, due today. Box 4 and up counts as mastered. `Store.words.record("animals:cat", "pass" | "miss" | "soft")` saves an answer.
- `js/speech.js`: text-to-speech helper
- `js/strokes.js`: stroke order for all 52 letters (ball-and-stick, Zaner-Bloser style). Edit here to change how a letter is taught.
- `js/writer.js`: the tracing pad (lined paper, guide letter, stroke demo, scoring)

Shared by the pages (`js/core/`):

- `lesson.js` (`LE.lesson`): rules about lessons that don't touch the page: looking up a lesson or scene, which games a lesson has (`mainGame`, `spellable`, `buildable`), how a sentence splits into word tiles, phonics parts. `ROUNDS` (5) is the number of questions per game. `LEVELS` names the three levels (icon, title, Chinese) and `levelOf(lesson)` gives a lesson's. `likeness(a, b)` scores how easily two words get mixed up.
- `ui.js` (`LE.ui`): pictures (`pic`, and `many` for counting), stars and progress dots, the Chinese lines (`zhLine`), Pip's cheer and the confetti, and `theme`: each lesson's button and text shades are worked out from its `color` so they stay readable.
- `progress.js` (`LE.progress`): best scores, words said, letters written, and how many stars (0–3) each stop shows. `recordAnswer(lesson, item, outcome)` is how the games report an answer about a word; `dueWords()` is today's review (one card per word, skipping words no longer in a lesson), and `REVIEW` holds its size, when the map offers it, and its color. `childLevel()` is the child's level and how many of its lessons are done. `tier(lesson, item)` says how hard to make a question about a word ("easy", "normal", "hard"), and `pickRounds` picks a game's words, least known first.
- `settings.js`: the voice, speed and Chinese controls in the header.

Pages (`js/views/`, each adds its page to `LE.views`):

- `map.js` (`LE.map`): shared by the two map pages: the islands with their stops, which far islands have come closer, the card a stop opens, what Pip suggests next (`nextStop`) and which stops are above the child's level (`aboveLevel`)
- `world.js`: the home map and Pip's boat
- `island.js`: inside an island, with Pip walking along the road
- `learn.js`: a lesson's picture cards, "Spell it" / "Sound it" and "Say it"
- `scene.js`: the picture dictionary
- `write.js`: the letter tracing page (uses `js/writer.js`)

Games (`js/games/`, each adds its game to `LE.games`): `listen.js`, `spell.js`, `build.js`, `blend.js`, `count.js` and `pipsays.js` (all four kinds of Pip says). `results.js` is the screen they all end on, and it saves the best score. `listen.js` also exports `listenQuiz`, the game without a fixed lesson, which `review.js` uses for the review (`#/review`) with its own results screen.

- `js/main.js`: the router. It picks the page from the address (`#/learn/animals`, `#/spell/animals`, `#/island/city` ...) and shows it.
- `tests/`: tests for `srs.js`, `store.js`, and the review and level parts of `core/progress.js` and `views/map.js` (against the real lessons and islands), run with `node --test`.
- `tools/wordlist/`: `python3 tools/wordlist/coverage.py` compares the lessons and scenes with the Cambridge Young Learners wordlists (Pre A1 Starters, A1 Movers, A2 Flyers) and writes `work/wordlist-report.md`: which level each lesson's words are, and which Starters words no lesson teaches yet. The wordlists belong to Cambridge and aren't in the project; download the combined PDF first (the link is at the top of `coverage.py`) and save it as `work/cambridge-yle-wordlists.pdf`. Needs macOS and Node.
- `tools/art/`: Python scripts that draw the illustrations. `build14.py` draws Pip (three poses) and small scenery (trees, flowers...); `build16.py` draws the world map (a landscape one and a tall one for phones) and the inside of each island, with the road and where each stop sits on it (exported as `window.WORLD`). To give an island more stops, add a spot along its road there; Nature Island is drawn taller than the others (`NATURE_H`) to fit its 8 stops. Run `python3 build16.py` to preview every island with numbered stops in `work/islands_preview.html`; `build15.py` draws the kitchen, beach, classroom, farm, park and supermarket scenes (their words and sentences are in `SCENES` in `js/content/data.js`); the sky and hills behind the pages are in `style.css`. `build21.py` draws sea animals, vegetables and bugs (`python3 build21.py` previews all three in `work/sets_preview.html`). `build18.py` draws the toys (`python3 build18.py` previews them in `work/toys_preview.html`). `build17.py` draws the Pip says pictures: the room with its drop zones and the places the cat sits, and a big Pip whose parts can be touched (`python3 build17.py` previews them in `work/do_preview.html`); `build19.py` draws the coloring page (preview: `work/paint_preview.html`); `build20.py` draws Pip with a prop for each "I can…" move (preview: `work/act_preview.html`). Run `python3 export_js.py` from that folder to rebuild `js/art.js`.
