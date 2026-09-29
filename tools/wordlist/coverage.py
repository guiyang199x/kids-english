"""How the lessons line up with the Cambridge Young Learners wordlists (Pre A1 Starters, A1 Movers, A2 Flyers).

The wordlists belong to Cambridge, so they aren't kept in this project. Download the combined one yourself:
https://www.cambridgeenglish.org/Images/wordlists-pre-a1-starters-a1-movers-and-a2-flyers.pdf
and save it as work/cambridge-yle-wordlists.pdf (work/ isn't committed). Then, from the project root:

    python3 tools/wordlist/coverage.py

It writes work/wordlist-report.md: for each lesson and scene, which of its words are Starters, Movers, Flyers
or on none of the lists; and the Starters words no lesson teaches yet, by part of speech.
Needs macOS (the PDF is read with PDFKit, see pdftext.swift) and Node (to read js/content/data.js).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "work" / "cambridge-yle-wordlists.pdf"
TXT = ROOT / "work" / "cambridge-yle-wordlists.txt"
REPORT = ROOT / "work" / "wordlist-report.md"

LEVELS = ["starters", "movers", "flyers"]
HEADINGS = {"Pre A1 Starters A–Z wordlist": "starters", "A1 Movers A–Z wordlist": "movers", "A2 Flyers A–Z wordlist": "flyers"}
POS = {"n", "v", "adj", "adv", "prep", "pron", "det", "conj", "excl", "dis", "int", "poss"}
POS_NAMES = {"n": "nouns", "v": "verbs", "adj": "adjectives", "adv": "adverbs", "prep": "prepositions",
             "pron": "pronouns", "det": "determiners", "conj": "conjunctions", "excl": "exclamations",
             "dis": "discourse markers", "int": "question words", "poss": "possessives"}
NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
           "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def pdf_text():
    if not TXT.exists() or TXT.stat().st_mtime < PDF.stat().st_mtime:
        out = subprocess.run(["swift", str(Path(__file__).with_name("pdftext.swift")), str(PDF)],
                             check=True, capture_output=True, text=True).stdout
        TXT.write_text(out)
    return TXT.read_text()


def pages(text):
    return [p.splitlines() for p in re.split(r"^=== PAGE \d+ ===$", text, flags=re.M)[1:]]


def forms(head):
    """'child/children' -> both; 'colour (US color)' -> both; 'sweet(s)' -> sweet, sweets."""
    out = []
    # "teddy (bear)": the word in brackets is optional ("keyboard (computer)" gets a useless extra form)
    m = re.fullmatch(r"([a-z ]+) \(([a-z]+)\)", head.strip())
    optional = [m.group(1) + " " + m.group(2)] if m else []
    variants = re.findall(r"\((?:US|UK) ((?:[^()]|\([^()]*\))+)\)", head)
    head = re.sub(r"\((?:[^()]|\([^()]*\))*\)", " ", head)
    for part in [head] + variants:
        for f in part.split("/"):
            f = " ".join(f.split()).lower()
            m = re.fullmatch(r"(.*)\(s\)", f)
            out += [m.group(1), m.group(1) + "s"] if m else [f]
    return [f for f in out + optional if f]


def entries(line):
    """One line of an A–Z list -> [(head, [pos...])]. A line can hold two entries ('zebra n zoo n')."""
    line = re.sub(r"\((?:[^()]|\([^()]*\))*\)", lambda m: m.group(0).replace(" ", " "), line)
    line = re.sub(r"\bof (place|time)( \+ (place|time))?", "", line)
    out, head, tags = [], [], []
    for tok in line.split():
        if tok in POS and head:
            tags.append(tok)
        elif tok == "+" and tags:
            continue
        else:
            if tags:
                out.append((" ".join(head), tags))
                head, tags = [], []
            head.append(tok.replace(" ", " "))
    if head and tags:
        out.append((" ".join(head), tags))
    return out


def wordlists():
    """{form: (level, pos, head)}: every spelling of a word points at its headword (its first form),
    so child/children or colour/color count as one word. The lowest level wins. Names are left out."""
    words, names = {}, set()
    for lines in pages(pdf_text()):
        level = next((HEADINGS[l.strip()] for l in lines if l.strip() in HEADINGS), None)
        if not level:
            continue
        # an entry that wrapped onto the next line: its POS tag ("bat (as sports equipment)" / "n"),
        # or the end of a note in brackets ("take off (i.e. get" / "undressed) v")
        joined = []
        for l in lines:
            l = l.strip()
            prev = joined[-1] if joined else ""
            if prev.count("(") > prev.count(")") or (
                l.split() and l.split()[0] in POS and prev not in ("", "Grammatical key") and not set(prev.split()) & POS
            ):
                joined[-1] += " " + l
            else:
                joined.append(l)
        in_names = False
        for l in joined:
            if l in HEADINGS or re.fullmatch(r"\d+|[A-Z]", l) or l == "Grammatical key":
                continue
            if l in ("Names",):
                in_names = True
                continue
            if l in ("Letters & numbers", "Numbers") or l.startswith("Candidates will"):
                continue
            if in_names:
                names.update(forms(l))
                continue
            for head, tags in entries(l):
                if len(head) > 1 and all(t in POS for t in tags):
                    fs = forms(head)
                    for f in fs:
                        if f not in words or LEVELS.index(level) < LEVELS.index(words[f][0]):
                            words[f] = (level, tags[0], fs[0])
    # Numbers are stated, not listed: Starters 1-20.
    for n in NUMBERS:
        words.setdefault(n, ("starters", "n", n))
    for n in names:
        words.pop(n, None)
    return words


def lessons():
    js = ("global.window = {}; require(process.argv[1]);"
          "console.log(JSON.stringify({ lessons: window.LESSONS, scenes: window.SCENES }))")
    data = json.loads(subprocess.run(["node", "-e", js, str(ROOT / "js/content/data.js")],
                                     check=True, capture_output=True, text=True).stdout)
    groups, sentences = [], []
    for l in data["lessons"]:
        sentences += [it.get("sentence", "") for it in l["items"]]
        words = []
        for it in l["items"]:
            # "two apples" is a number and a thing; the lesson teaches both
            words += [NUMBERS[it["count"] - 1], it["thing"]] if it.get("count") else [it["word"]]
        groups.append((l["id"], l["title"], words))
    for s in data["scenes"]:
        groups.append(("scene-" + s["id"], s["title"], list(s["sentences"])))  # keyed by the label words
        sentences += list(s["sentences"].values())
    return groups, " ".join(sentences)


# The lists are in UK English and give some US spellings, but not these.
US_WORDS = {"mom": "mum"}


def look_up(word, lists):
    """The list entry for one of our words, trying plain, singular and the hyphen-less spellings."""
    w = word.lower().strip()
    w = US_WORDS.get(w, w)
    tries = [w, w.replace("-", " "), w.replace("-", "")]
    for t in list(tries):
        if t.endswith("ies"):
            tries.append(t[:-3] + "y")
        if t.endswith("es"):
            tries.append(t[:-2])
        if t.endswith("s"):
            tries.append(t[:-1])
    return next((lists[t] for t in tries if t in lists), None)


def main():
    if not PDF.exists():
        sys.exit(f"Save the wordlist PDF as {PDF.relative_to(ROOT)} first (see the top of this file).")
    lists = wordlists()
    groups, sentences = lessons()
    heard = set()  # headwords a child hears in some sentence, though no card teaches them
    words = re.findall(r"[a-z’'-]+", sentences.lower().replace("’", "'"))
    for n in (3, 2, 1):
        for k in range(len(words) - n + 1):
            hit = look_up(" ".join(words[k:k + n]).replace("'", "’"), lists)
            if hit:
                heard.add(hit[2])
    taught = set()  # headwords some lesson or scene teaches
    rows, detail = [], []
    for gid, title, words in groups:
        by = {k: [] for k in LEVELS + ["none"]}
        for w in dict.fromkeys(words):
            hit = look_up(w, lists)
            by[hit[0] if hit else "none"].append(w)
            if hit:
                taught.add(hit[2])
        n = len(dict.fromkeys(words))
        rows.append(f"| {gid} | {n} | " + " | ".join(str(len(by[k])) for k in LEVELS + ["none"]) +
                    f" | {round(100 * len(by['starters']) / n)}% |")
        detail.append(f"### {title} (`{gid}`)\n\n" + "\n".join(
            f"- **{k.capitalize()}:** {', '.join(by[k])}" for k in LEVELS + ["none"] if by[k]))

    starters = {head: pos for level, pos, head in lists.values() if level == "starters"}
    covered = [h for h in starters if h in taught]
    missing = {}
    for head, pos in sorted(starters.items()):
        if head not in taught:
            missing.setdefault(pos, []).append(head + ("*" if head in heard else ""))

    out = [
        "# Lessons vs. the Cambridge Young Learners wordlists",
        "",
        f"Made by `tools/wordlist/coverage.py` from `{PDF.name}`. Not committed: the lists belong to Cambridge.",
        "",
        f"Starters words taught somewhere: **{len(covered)} of {len(starters)}** "
        f"({round(100 * len(covered) / len(starters))}%). Plurals, US/UK spellings and a/b forms count as the same word.",
        "",
        "## Each lesson",
        "",
        "| lesson | words | Starters | Movers | Flyers | on no list | Starters share |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
        *detail,
        "",
        "## Starters words no lesson teaches yet",
        "",
        f"Marked * if a child still hears it in some sentence ({sum(w.endswith('*') for ws in missing.values() for w in ws)} of "
        f"{sum(map(len, missing.values()))}).",
        "",
        *[f"- **{POS_NAMES.get(p, p)} ({len(ws)}):** {', '.join(ws)}" for p, ws in sorted(missing.items(), key=lambda kv: -len(kv[1]))],
        "",
    ]
    REPORT.write_text("\n\n".join(out).replace("\n\n\n\n", "\n\n").replace("|\n\n|", "|\n|"))
    print(f"Wrote {REPORT.relative_to(ROOT)}: {len(covered)} of {len(starters)} Starters words taught.")


if __name__ == "__main__":
    main()
