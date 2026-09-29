from common import INK, fmt, svg_wrap

MOUTH = "#8a3446"
S = f'stroke="{INK}" stroke-linecap="round" stroke-linejoin="round" fill="none"'


def face(fill):
    return f'<circle class="k-o" cx="0" cy="0" r="46" fill="{fill}"/>'


def cheeks(y=8, x=30):
    return (
        f'<ellipse cx="{-x}" cy="{y}" rx="7" ry="4.5" fill="#ff6f86" opacity=".4"/>'
        f'<ellipse cx="{x}" cy="{y}" rx="7" ry="4.5" fill="#ff6f86" opacity=".4"/>'
    )


def dot_eyes(y=-6, rx=5, ry=6.5, x=18):
    return (
        f'<ellipse cx="{-x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK}"/>'
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{INK}"/>'
        f'<circle cx="{-x + 2}" cy="{y - 2.5}" r="1.8" fill="#fff"/>'
        f'<circle cx="{x + 2}" cy="{y - 2.5}" r="1.8" fill="#fff"/>'
    )


def big_eyes(y=-8, r=8.5, pr=4, x=17):
    return (
        f'<circle cx="{-x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        f'<circle cx="{-x}" cy="{y + 1}" r="{pr}" fill="{INK}"/>'
        f'<circle cx="{x}" cy="{y + 1}" r="{pr}" fill="{INK}"/>'
    )


HAPPY = (
    face("#ffd23f")
    + cheeks(9, 31)
    + f'<path d="M-26 -6Q-19 -17 -12 -6M12 -6Q19 -17 26 -6" {S} stroke-width="3.5"/>'
    + f'<path d="M-22 7Q0 37 22 7Z" fill="{MOUTH}"/>'
    + '<ellipse cx="0" cy="18" rx="8" ry="4" fill="#ff7c93"/>'
    + f'<path d="M-22 7Q0 37 22 7Z" {S} stroke-width="3"/>'
)

SAD = (
    face("#8ec5ff")
    + f'<path d="M-29 -17Q-20 -20 -11 -26M29 -17Q20 -20 11 -26" {S} stroke-width="3"/>'
    + dot_eyes(-5)
    + f'<path d="M-13 25Q0 13 13 25" {S} stroke-width="3.5"/>'
    + f'<path d="M-19 5C-21 9 -25 13 -25 16.5A6 6 0 0 0 -13 16.5C-13 13 -17 9 -19 5Z" fill="#e3f3ff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
)

ANGRY = (
    face("#ff8a73")
    + f'<path d="M-29 -23L-10 -14M29 -23L10 -14" {S} stroke-width="4"/>'
    + dot_eyes(-4, 5, 5.5, 17)
    + f'<rect x="-16" y="13" width="32" height="13" rx="5" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    + f'<path d="M-15 19.5H15M-8 13V26M0 13V26M8 13V26" {S} stroke-width="2"/>'
)

SURPRISED = (
    face("#ffb45e")
    + cheeks(10, 32)
    + f'<path d="M-27 -26Q-18 -34 -9 -27M27 -26Q18 -34 9 -27" {S} stroke-width="3"/>'
    + big_eyes(-8, 8.5, 4.2, 17)
    + '<circle cx="-15.5" cy="-9" r="1.6" fill="#fff"/><circle cx="18.5" cy="-9" r="1.6" fill="#fff"/>'
    + f'<ellipse cx="0" cy="21" rx="8" ry="10" fill="{MOUTH}" stroke="{INK}" stroke-width="3"/>'
)

SLEEPY = (
    face("#c9b8ff")
    + cheeks(10, 31)
    + f'<path d="M-25 -5A7 6 0 0 0 -11 -5Z" fill="{INK}"/><path d="M11 -5A7 6 0 0 0 25 -5Z" fill="{INK}"/>'
    + f'<path d="M-28 -5H-8M8 -5H28" {S} stroke-width="3"/>'
    + f'<ellipse cx="0" cy="21" rx="6" ry="7.5" fill="{MOUTH}" stroke="{INK}" stroke-width="3"/>'
    + '<text class="k-f" x="40" y="-36" font-size="16" fill="#6a44c2">z</text>'
    + '<text class="k-f" x="52" y="-50" font-size="22" fill="#6a44c2">Z</text>'
)

SCARED = (
    face("#a8e4a0")
    + f'<path d="M-28 -22Q-20 -25 -11 -31M28 -22Q20 -25 11 -31" {S} stroke-width="3"/>'
    + big_eyes(-7, 8, 2.6, 17)
    + f'<path d="M-16 21l4 -4l4 4l4 -4l4 4l4 -4l4 4l4 -4l4 4" {S} stroke-width="3"/>'
    + f'<path d="M33 -34C31 -30 28 -27 28 -24A5 5 0 0 0 38 -24C38 -27 35 -30 33 -34Z" fill="#cdeaff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    + f'<path d="M-55 -9Q-59 0 -55 9M-63 -14Q-69 0 -63 14M55 -9Q59 0 55 9M63 -14Q69 0 63 14" {S} stroke-width="2.5"/>'
)

CARDS = [
    ("happy", HAPPY, "#fff6d1", "#f3dc8a"),
    ("sad", SAD, "#e3f0ff", "#bcd8f7"),
    ("angry", ANGRY, "#ffe5e0", "#f7c3b8"),
    ("surprised", SURPRISED, "#ffeedd", "#f5d0a2"),
    ("sleepy", SLEEPY, "#efe9ff", "#d6c8fa"),
    ("scared", SCARED, "#e5f6e2", "#bfe3b8"),
]

W, H, GAP = 184, 200, 24
X0 = [40, 248, 456]
Y0 = [20, 20 + H + GAP]


def card(i, spec):
    word, art, bg, border = spec
    x = X0[i % 3]
    y = Y0[i // 3]
    cx = x + W / 2
    return (
        f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="20" fill="{bg}" stroke="{border}" stroke-width="2"/>'
        f'<g transform="translate({fmt(cx)} {y + 88})">{art}</g>'
        f'<text class="k-f" x="{fmt(cx)}" y="{y + 174}" font-size="24" fill="{INK}" text-anchor="middle">{word}</text>'
    )


svg = svg_wrap(
    Y0[1] + H + 20,
    "Feelings faces",
    "Six cartoon faces labeled happy, sad, angry, surprised, sleepy and scared.",
    "".join(card(i, c) for i, c in enumerate(CARDS)),
)
open("feelings.svg", "w").write(svg)
print(len(svg), "bytes")
