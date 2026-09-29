"""Numbers 1-10 and shapes. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
import math
from common import INK, fmt
from build1 import shadow
from build5 import eyes, cheeks, smile

# ---------------------------------------------------------------- numbers
NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
BALLS = ["#ef5b56", "#ffc93c", "#4a9be8", "#5cc36a", "#9b74e8", "#f78fb3", "#ff9a3c"]


def ball(x, y, r, fill):
    return (
        f'<circle class="k-o" cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{fill}"/>'
        f'<circle cx="{fmt(x - r * .35)}" cy="{fmt(y - r * .38)}" r="{fmt(r * .26)}" fill="#fff" opacity=".7"/>'
    )


def number(n):
    """The numeral on top, n balls to count underneath (one row up to 5, then two rows)."""
    color = BALLS[(n - 1) % len(BALLS)]
    g = (
        f'<text class="k-f" x="0" y="-4" font-size="62" text-anchor="middle" fill="{color}" '
        f'stroke="{INK}" stroke-width="7" stroke-linejoin="round" paint-order="stroke">{n}</text>'
    )
    rows = [n] if n <= 5 else [math.ceil(n / 2), n // 2]
    r, gap = 10, 25
    y0 = 26 if len(rows) == 1 else 18
    k = 0
    for ri, cnt in enumerate(rows):
        for i in range(cnt):
            x = (i - (cnt - 1) / 2) * gap
            g += ball(x, y0 + ri * 24, r, BALLS[k % len(BALLS)])
            k += 1
    return g


# ---------------------------------------------------------------- shapes
def face(y=0, s=1.0):
    q = lambda v: round(v, 1)
    return eyes(q(11 * s), q(y - 4 * s), q(4.5 * s)) + cheeks(q(20 * s), q(y + 5 * s), q(5.5 * s), q(3.5 * s)) + smile(q(y + 6 * s), q(6 * s), q(5 * s))


def shine(d):
    return f'<path d="{d}" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>'


def star_path(r, inner=0.48, pts=5):
    out = []
    for k in range(pts * 2):
        a = math.radians(-90 + k * 180 / pts)
        rr = r if k % 2 == 0 else r * inner
        out.append(f"{fmt(rr * math.cos(a))} {fmt(rr * math.sin(a))}")
    return "M" + "L".join(out) + "Z"


def circle():
    return shadow(54, 34) + '<circle class="k-o" cx="0" cy="0" r="46" fill="#ef5b56"/>' + shine("M-34 -12A36 36 0 0 1 -14 -33") + face(4)


def square():
    return shadow(54, 38) + '<rect class="k-o" x="-44" y="-44" width="88" height="88" rx="8" fill="#4a9be8"/>' + shine("M-34 -14V-32H-16") + face(4)


def triangle():
    return (
        shadow(52, 44)
        + '<path class="k-o" d="M0 -54L54 46H-54Z" fill="#ffc93c" stroke-linejoin="round"/>'
        + shine("M-8 -30L-26 4")
        + face(18, 0.9)
    )


def rectangle():
    return shadow(46, 56) + '<rect class="k-o" x="-66" y="-36" width="132" height="72" rx="8" fill="#5cc36a"/>' + shine("M-56 -8V-26H-36") + face(2)


def oval():
    return shadow(56, 30) + '<ellipse class="k-o" cx="0" cy="0" rx="36" ry="52" fill="#9b74e8"/>' + shine("M-26 -16A30 44 0 0 1 -10 -42") + face(4)


def star():
    return shadow(54, 36) + f'<path class="k-o" d="{star_path(58)}" fill="#ffd23f" transform="translate(0 4)"/>' + face(10, 0.85)


def heart():
    d = "M0 50C-22 34 -52 12 -52 -16C-52 -36 -38 -48 -24 -48C-12 -48 -4 -40 0 -32C4 -40 12 -48 24 -48C38 -48 52 -36 52 -16C52 12 22 34 0 50Z"
    return shadow(56, 30) + f'<path class="k-o" d="{d}" fill="#f78fb3"/>' + shine("M-40 -16C-40 -28 -34 -36 -26 -38") + face(0)


def diamond():
    return shadow(56, 28) + '<path class="k-o" d="M0 -56L44 0L0 56L-44 0Z" fill="#ff9a3c"/>' + shine("M-8 -38L-26 -14") + face(2)


SHAPES = [
    ("circle", circle), ("square", square), ("triangle", triangle), ("rectangle", rectangle),
    ("oval", oval), ("star", star), ("heart", heart), ("diamond", diamond),
]
