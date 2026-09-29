"""Pip says, moves: Pip acting out the "I can..." words, for the child to copy ("Jump high!").

One picture: Pip with his parts in groups (build14.pip(parts=True)) and a prop for each move in a
<g class="act-prop" data-move="...">. js/games/pipsays.js shows only the current move's prop, and style.css moves Pip and the
prop (.act-<move>.moving). Props that move get their own class (act-waves, act-note...) so CSS can animate them
without touching the transform attributes inside.

Run `python3 build20.py` to write work/act_preview.html with Pip and each prop.
"""
from common import INK
from build1 import ball
from build2 import crayon
from build12 import note
from build14 import pip, _mouth

VB = "-120 -104 240 200"


def prop(move, inner):
    return f'<g class="act-prop" data-move="{move}">{inner}</g>'


def _lines(d, w=4, op=".5"):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'


def _puff(x, y, r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#efe6d6" stroke="{INK}" stroke-width="2"/>'


RUN = prop("run", f'<g class="act-speed">{_lines("M-62 -6H-96M-58 20H-104M-64 46H-92")}</g>'
           + f'<g class="act-dust">{_puff(-48, 84, 7)}{_puff(-62, 80, 5)}{_puff(-72, 86, 4)}</g>')

JUMP = prop("jump", _lines("M-50 70L-64 60M-54 86H-70M50 70L64 60M54 86H70", 3.5, ".55"))

_wave = "M-180 44" + "".join(f"Q{x + 15} 34 {x + 30} 44T{x + 60} 44" for x in range(-180, 180, 60))
SWIM = prop(
    "swim",
    f'<g class="act-waves"><path d="{_wave}V100H-180Z" fill="#8fd0f5" fill-opacity=".9" stroke="{INK}" stroke-width="3"/>'
    f'<path d="{_wave.replace("44", "62")}" transform="translate(30 0)" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/></g>'
    + f'<g class="act-bubbles"><circle cx="-60" cy="20" r="5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    f'<circle cx="-70" cy="4" r="3.5" fill="#fff" stroke="{INK}" stroke-width="2"/></g>',
)


def _notes(spots):
    return "".join(f'<g class="act-note" style="animation-delay:{d}s">{note(x, y, s, c)}</g>' for x, y, s, c, d in spots)


DANCE = prop("dance", _notes([(-82, -52, 1.3, "#d65b9a", 0), (80, -34, 1.2, "#4a9be8", 0.3), (-88, 16, 1, "#5e9a2e", 0.6), (84, 30, 1, "#ffb31a", 0.9)]))

SING = prop(
    "sing",
    f'<g class="act-open-mouth">{_mouth(open_=True)}</g>'
    + _notes([(64, -12, 1.1, "#6a44c2", 0), (82, -44, 1.3, "#d65b9a", 0.4), (98, -76, 1, "#4a9be8", 0.8)]),
)

READ = prop(
    "read",
    '<g class="act-book">'
    f'<path class="k-o" d="M0 18C-16 10 -36 10 -48 16V56C-36 50 -16 50 0 58C16 50 36 50 48 56V16C36 10 16 10 0 18Z" fill="#4a9be8"/>'
    f'<path class="k-o" d="M0 22C-14 14 -32 14 -42 20V52C-32 46 -14 46 0 54C14 46 32 46 42 52V20C32 14 14 14 0 22Z" fill="#fff" stroke-width="2.5"/>'
    f'<path d="M0 22V54" stroke="{INK}" stroke-width="2.5"/>'
    + _lines("M-34 26Q-20 22 -8 28M-34 34Q-20 30 -8 36M-34 42Q-20 38 -8 44M8 28Q20 22 34 26M8 36Q20 30 34 34M8 44Q20 38 34 42", 2, ".45")
    + f'<circle cx="-46" cy="40" r="9" fill="{INK}"/><circle cx="46" cy="40" r="9" fill="{INK}"/></g>',
)

DRAW = prop(
    "draw",
    '<circle class="act-circle" cx="78" cy="-40" r="24" fill="none" stroke="#ef5b56" stroke-width="6" '
    'stroke-linecap="round" stroke-dasharray="151" transform="rotate(-90 78 -40)"/>'
    f'<g class="act-crayon"><g transform="translate(52 28) rotate(35) scale(.42)">{crayon("#ef5b56", "#c9403b", 90)}</g>'
    f'<circle cx="46" cy="32" r="12" fill="{INK}"/></g>',
)

KICK = prop("kick", f'<g class="act-ball"><g transform="translate(58 70) scale(.36)">{ball()}</g></g>')

PROPS = [RUN, JUMP, SWIM, DANCE, SING, READ, DRAW, KICK]
MOVES = ["run", "jump", "swim", "dance", "sing", "read", "draw", "kick"]


def stage():
    # The waves go in front of Pip, the rest too; Pip is drawn first.
    return f'<g class="pp-all">{pip("down", parts=True)}</g>' + "".join(PROPS)


def export():
    return {
        "_do-act": f'<svg viewBox="{VB}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pip showing a move">{stage()}</svg>'
    }


if __name__ == "__main__":
    import os

    css = f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
    cells = ""
    for i, m in enumerate(MOVES):
        cells += f'<figure><svg viewBox="{VB}" width="240"><g class="pp-all">{pip("down", parts=True)}</g>{PROPS[i]}</svg><figcaption>{m}</figcaption></figure>'
    html = f"<html><head><style>{css}body{{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:12px}}figure{{margin:0;border:1px solid #ccc}}</style></head><body>{cells}</body></html>"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../work/act_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
