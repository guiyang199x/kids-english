"""Pip says, coloring: a page of things to color ("Color the ball blue.").

Each thing is a <g class="do-paint" data-zone="..."> in a cell of a 3 x 2 grid. Its parts with class "pf" start
white and take the crayon color (js/games/pipsays.js sets their fill); a transparent <rect class="paint-hit"> fills the cell so a
tap anywhere near the thing counts. Everything else (lines, windows, wheels) keeps its own color.

Run `python3 build19.py` to write work/paint_preview.html: the page blank, and every thing colored.
"""
from common import INK

W, H = 680, 360
WHITE = "#fff"


def _pf(tag, attrs, extra_cls=""):
    return f'<{tag} class="k-o pf{extra_cls}" {attrs} fill="{WHITE}"/>'


def ball():
    return (
        _pf("circle", 'cx="0" cy="0" r="50"')
        + f'<path d="M-48 -12Q0 12 48 -12M-12 -48Q14 0 -12 48" fill="none" stroke="{INK}" stroke-width="3"/>'
        + '<path d="M-30 -30Q-22 -38 -12 -40" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    )


def balloon():
    return (
        f'<path d="M0 36C-8 46 8 52 0 62S-6 74 2 80" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + _pf("path", 'd="M-7 42L0 32L7 42Z"')
        + _pf("path", 'd="M0 34C-26 34 -42 10 -42 -16C-42 -44 -22 -62 0 -62C22 -62 42 -44 42 -16C42 10 26 34 0 34Z"')
        + '<path d="M-24 -30Q-22 -44 -10 -50" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".8"/>'
    )


def car():
    wheel = lambda x: (
        f'<circle cx="{x}" cy="24" r="15" fill="{INK}"/><circle cx="{x}" cy="24" r="6" fill="#c9c2d3"/>'
    )
    return (
        _pf("path", 'd="M-72 22V2Q-72 -10 -60 -12L-40 -14L-26 -40H22L40 -14L62 -10Q74 -8 74 4V22Z"')
        + f'<path class="k-o" d="M-34 -14L-24 -32H-4V-14Z" fill="#d9f0ff" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M4 -14V-32H18L30 -14Z" fill="#d9f0ff" stroke-width="2.5"/>'
        + f'<circle cx="66" cy="0" r="5" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + wheel(-42)
        + wheel(44)
    )


def tshirt():
    return (
        _pf("path", 'd="M-22 -50Q0 -38 22 -50L62 -30L48 -2L34 -10V52H-34V-10L-48 -2L-62 -30Z"')
        + f'<path d="M-22 -50Q0 -26 22 -50" fill="none" stroke="{INK}" stroke-width="3"/>'
        + f'<path d="M-34 -10L-40 -22M34 -10L40 -22" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def fish():
    return (
        _pf("path", 'd="M36 0L72 -30V30Z"')
        + _pf("path", 'd="M-66 0C-50 -34 -10 -44 22 -30C34 -24 42 -10 44 0C42 10 34 24 22 30C-10 44 -50 34 -66 0Z"')
        + _pf("path", 'd="M-16 -36Q0 -54 18 -32Z"')
        + f'<path d="M0 -20Q10 0 0 20" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<circle cx="-40" cy="-6" r="8" fill="#fff" stroke="{INK}" stroke-width="2.5"/><circle cx="-41" cy="-6" r="4" fill="{INK}"/>'
        + f'<path d="M-58 8Q-52 12 -48 8" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def kite():
    bow = lambda x, y: _pf("path", f'd="M{x} {y}L{x - 11} {y - 7}V{y + 7}ZM{x} {y}L{x + 11} {y - 7}V{y + 7}Z"', "")
    return (
        f'<path d="M0 52C-10 60 12 66 2 74S-14 82 -6 88" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + _pf("path", 'd="M0 -62L40 -10L0 52L-40 -10Z"')
        + f'<path d="M0 -62V52M-40 -10H40" fill="none" stroke="{INK}" stroke-width="2.5"/>'
        + bow(1, 64)
        + bow(-7, 84)
    )


# (zone, drawing, scale); the cells run left to right, top to bottom
THINGS = [("ball", ball, 1), ("balloon", balloon, 1), ("car", car, 1), ("T-shirt", tshirt, 1), ("fish", fish, 1), ("kite", kite, 0.9)]
CW, CH = W / 3, H / 2


def page():
    out = f'<rect width="{W}" height="{H}" fill="#fffdf7"/>'
    for i, (zone, draw, s) in enumerate(THINGS):
        cx, cy = CW * (i % 3) + CW / 2, CH * (i // 3) + CH / 2
        out += (
            f'<g class="do-paint" data-zone="{zone}" transform="translate({cx:.1f} {cy:.1f})">'
            f'<rect class="paint-hit" x="{-CW / 2 + 8:.1f}" y="{-CH / 2 + 8:.1f}" width="{CW - 16:.1f}" height="{CH - 16:.1f}" rx="20" fill="transparent"/>'
            f'<g transform="scale({s})">{draw()}</g></g>'
        )
    return out


VB = f"0 0 {W} {H}"


def export():
    return {
        "_do-paint": f'<svg viewBox="{VB}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="A ball, a balloon, a car, a T-shirt, a fish and a kite to color">{page()}</svg>'
    }


if __name__ == "__main__":
    import os, re
    from build2 import COLORS

    css = f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
    cols = [c[1] for c in COLORS]
    painted = page()
    for i, (zone, *_) in enumerate(THINGS):
        start = painted.index(f'data-zone="{zone}"')
        end = painted.index('<g class="do-paint"', start) if i < len(THINGS) - 1 else len(painted)
        part = re.sub(r'(class="k-o pf[^"]*"[^>]*?)fill="#fff"', rf'\1fill="{cols[i]}"', painted[start:end])
        painted = painted[:start] + part + painted[end:]
    html = (
        f"<html><head><style>{css}body{{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:12px}}"
        f"figure{{margin:0;border:1px solid #ccc}}</style></head><body>"
        f'<figure><svg viewBox="{VB}" width="680">{page()}</svg><figcaption>blank</figcaption></figure>'
        f'<figure><svg viewBox="{VB}" width="680">{painted}</svg><figcaption>colored</figcaption></figure></body></html>'
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../work/paint_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
