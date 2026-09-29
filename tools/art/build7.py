"""Fruits and food. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
import math
from common import INK, fmt, smooth_path
from build1 import shadow
from build5 import dstroke

SHINE = 'fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".75"'


def leaf(x, y, rot, s=1.0, fill="#6cc070"):
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        f'<path class="k-o" d="M0 0C8 -14 28 -16 38 -8C28 4 12 8 0 0Z" fill="{fill}"/>'
        '<path d="M5 -2Q20 -8 31 -8" fill="none" stroke="#4a9a4f" stroke-width="2" stroke-linecap="round"/>'
        "</g>"
    )


def stem(d="M0 -36C0 -44 2 -50 6 -54"):
    return dstroke(d, "#8b5a3c", 4)


def bitten(R, bx, by, br):
    """Circle of radius R at the origin with a round bite at (bx, by) of radius br."""
    d = math.hypot(bx, by)
    a = (R ** 2 - br ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(R ** 2 - a ** 2)
    ux, uy = bx / d, by / d
    px, py = a * ux, a * uy
    p1 = (px - h * uy, py + h * ux)
    p2 = (px + h * uy, py - h * ux)
    return (
        f"M{fmt(p1[0])} {fmt(p1[1])}A{R} {R} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}"
        f"A{br} {br} 0 0 0 {fmt(p1[0])} {fmt(p1[1])}Z"
    )


# ================================================================ fruits
def banana():
    body = "M-56 -22C-44 34 36 42 58 -30C40 8 -28 12 -56 -22Z"
    return (
        shadow(46, 44)
        + f'<path class="k-o" d="{body}" fill="#ffd23f"/>'
        + '<path d="M-44 -2C-20 22 24 24 46 -6" fill="none" stroke="#e8b520" stroke-width="3" stroke-linecap="round"/>'
        + '<path d="M-38 6C-22 22 0 26 18 22" ' + SHINE + "/>"
        + f'<path class="k-o" d="M54 -24L58 -44L68 -42L62 -22Z" fill="#8b5a3c"/>'
        + f'<circle cx="-55" cy="-21" r="4" fill="{INK}"/>'
    )


def orange_fruit():
    dots = "".join(
        f'<circle cx="{fmt(r * math.cos(a))}" cy="{fmt(6 + r * math.sin(a))}" r="1.6" fill="#e07b1f"/>'
        for r, n in ((18, 6), (32, 10)) for a in (math.radians(k * 360 / n + r) for k in range(n))
    )
    return (
        shadow(54, 38)
        + '<circle class="k-o" cx="0" cy="6" r="46" fill="#ff9a3c"/>'
        + dots
        + '<path d="M-30 -14A34 34 0 0 1 -10 -30" ' + SHINE + "/>"
        + stem("M0 -38C0 -44 1 -48 3 -52")
        + leaf(3, -44, -20)
    )


def strawberry():
    body = "M0 52C-28 42 -48 8 -46 -14C-44 -32 -22 -36 0 -32C22 -36 44 -32 46 -14C48 8 28 42 0 52Z"
    seeds = ""
    for row, (y, xs) in enumerate([(-14, (-30, -12, 8, 26)), (4, (-22, -3, 16, 32)), (22, (-14, 6, 22)), (38, (-4, 10))]):
        for x in xs:
            seeds += f'<ellipse cx="{x}" cy="{y}" rx="2.4" ry="3.6" fill="#ffe27a" stroke="{INK}" stroke-width="1"/>'
    pts = []
    for k in range(10):
        a = math.radians(180 + k * 20)
        r = 34 if k % 2 == 0 else 18
        pts.append(f"{fmt(r * math.cos(a))} {fmt(-32 + r * math.sin(a) * .55 + (8 if k % 2 == 0 else 0))}")
    sepals = f'<path class="k-o" d="M{"L".join(pts)}Z" fill="#5cc36a"/>'
    return (
        shadow(56, 32)
        + f'<path class="k-o" d="{body}" fill="#ef4f5a"/>'
        + '<path d="M-34 -8C-34 8 -26 22 -18 30" ' + SHINE + "/>"
        + seeds
        + sepals
        + stem("M0 -38C0 -46 2 -52 6 -56")
    )


def watermelon():
    seeds = "".join(
        f'<path d="M{x} {y - 4}C{x - 3} {y} {x - 3} {y + 4} {x} {y + 5}C{x + 3} {y + 4} {x + 3} {y} {x} {y - 4}Z" fill="{INK}"/>'
        for x, y in ((-30, -8), (-12, 2), (8, 0), (26, -8), (-18, 18), (2, 22), (18, 14))
    )
    return (
        '<g transform="translate(0 -14)">'
        + shadow(66, 56)
        + '<path class="k-o" d="M-64 -10A64 64 0 0 0 64 -10Z" fill="#3f9e4d"/>'
        + '<path d="M-57 -10A57 57 0 0 0 57 -10Z" fill="#c8f0a8"/>'
        + f'<path d="M-51 -10A51 51 0 0 0 51 -10Z" fill="#ff5f6d" stroke="{INK}" stroke-width="1.5"/>'
        + f'<path class="k-o" d="M-64 -10H64" fill="none"/>'
        + seeds
        + "</g>"
    )


def pear():
    body = "M0 -40C12 -40 14 -24 20 -8C40 10 42 50 0 52C-42 50 -40 10 -20 -8C-14 -24 -12 -40 0 -40Z"
    return (
        shadow(56, 34)
        + f'<path class="k-o" d="{body}" fill="#b8d94a"/>'
        + '<path d="M22 0C36 16 36 44 6 50C30 36 32 16 22 0Z" fill="#9bbf35"/>'
        + f'<path class="k-o" d="{body}" fill="none"/>'
        + '<path d="M-26 12C-30 22 -28 32 -22 38" ' + SHINE + "/>"
        + stem("M0 -38C0 -46 2 -52 6 -56")
        + leaf(4, -46, -30, .8)
    )


def lemon():
    body = "M-58 2C-52 -6 -48 -34 0 -34C48 -34 52 -6 58 2C52 10 48 38 0 38C-48 38 -52 10 -58 2Z"
    return (
        '<g transform="translate(0 6)">'
        + shadow(48, 44)
        + f'<path class="k-o" d="{body}" fill="#ffe14d"/>'
        + '<path d="M-36 -12C-28 -22 -16 -26 -4 -26" ' + SHINE + "/>"
        + leaf(-2, -32, -40, .9)
        + "</g>"
    )


FRUITS = [
    ("banana", banana), ("orange-fruit", orange_fruit), ("strawberry", strawberry),
    ("watermelon", watermelon), ("pear", pear), ("lemon", lemon),
]


# ================================================================ food
def bread():
    crust = "M-44 52V-8C-62 -12 -64 -48 -32 -52C-16 -62 16 -62 32 -52C64 -48 62 -12 44 -8V52Z"
    return (
        shadow(56, 44)
        + f'<path class="k-o" d="{crust}" fill="#d08a45"/>'
        + f'<path d="{crust}" fill="#f7deaa" transform="translate(0 5) scale(.8)"/>'
        + '<path d="M-22 -18Q-18 -22 -14 -18M6 -30Q10 -34 14 -30M16 8Q20 4 24 8M-18 22Q-14 18 -10 22" fill="none" stroke="#e0bd7c" stroke-width="2.5" stroke-linecap="round"/>'
    )


def egg():
    pts = []
    radii = [54, 46, 52, 44, 50, 42, 52, 46, 50, 44]
    for k, r in enumerate(radii):
        a = math.radians(k * 36)
        pts.append((r * math.cos(a), 4 + r * 0.82 * math.sin(a)))
    white = smooth_path(pts, closed=True)
    return (
        shadow(52, 48)
        + f'<path class="k-o" d="{white}" fill="#fff"/>'
        + '<circle class="k-o" cx="4" cy="2" r="22" fill="#ffc93c"/>'
        + '<path d="M-8 -6A14 14 0 0 1 2 -14" ' + SHINE + "/>"
    )


def milk():
    return (
        shadow(56, 36)
        + '<path class="k-o" d="M12 -18L34 -30V42L12 54Z" fill="#cfdcea"/>'
        + '<path class="k-o" d="M-10 -44L12 -56L34 -30L12 -18Z" fill="#b8cbe0"/>'
        + '<path class="k-o" d="M-14 -48L8 -60L12 -56L-10 -44Z" fill="#fff"/>'
        + '<path class="k-o" d="M-32 -18L-10 -44L12 -18Z" fill="#fff"/>'
        + '<rect class="k-o" x="-32" y="-18" width="44" height="72" fill="#fff"/>'
        + '<path d="M-30.5 30Q-20 22 -10 30T10.5 30V52.5H-30.5Z" fill="#4a9be8"/>'
        + '<path d="M13.5 29L32.5 19V41L13.5 52Z" fill="#2f7cc6"/>'
        + f'<text class="k-f" x="-10" y="12" font-size="15" text-anchor="middle" fill="#2268b0">MILK</text>'
        + f'<rect class="k-o" x="-32" y="-18" width="44" height="72" fill="none"/>'
    )


def bowl(fill, band):
    return (
        '<rect class="k-o" x="-20" y="42" width="40" height="10" rx="3" fill="{f}"/>'.format(f=fill)
        + f'<path class="k-o" d="M-56 -4H56C56 30 30 46 0 46C-30 46 -56 30 -56 -4Z" fill="{fill}"/>'
        + f'<path d="M-48 18Q-36 12 -24 18T0 18T24 18T48 18" fill="none" stroke="{band}" stroke-width="4" stroke-linecap="round"/>'
    )


def rice():
    grains = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="4.5" ry="2.4" transform="rotate({r} {x} {y})" fill="none" stroke="#c9c2b4" stroke-width="1.5"/>'
        for x, y, r in ((-30, -12, 20), (-14, -22, -15), (4, -26, 30), (20, -18, -25), (34, -10, 10), (-4, -12, 0), (14, -6, 40), (-22, -4, -30))
    )
    return (
        shadow(56, 34)
        + '<path class="k-o" d="M-52 -4C-48 -40 48 -40 52 -4Z" fill="#fff"/>'
        + grains
        + bowl("#4a9be8", "#fff")
    )


def noodles():
    strands = "".join(
        dstroke(f"M{x} -30C{x - 8} -22 {x + 8} -14 {x} -2", "#ffd66b", 3.5) for x in (-6, 2, 10)
    )
    return (
        shadow(56, 34)
        + '<ellipse class="k-o" cx="0" cy="-4" rx="54" ry="10" fill="#ffcf7a"/>'
        + dstroke("M-40 -4Q-30 -10 -20 -4T0 -4", "#ffd66b", 3.5)
        + dstroke("M16 -6Q26 -12 36 -6", "#ffd66b", 3.5)
        + strands
        + '<circle class="k-o" cx="30" cy="-6" r="7" fill="#fff" stroke-width="2"/><circle cx="30" cy="-6" r="3" fill="#ff9a3c"/>'
        + '<path class="k-o" d="M-34 -8L-22 -12L-18 -4Z" fill="#6cc070" stroke-width="2"/>'
        + bowl("#ef5b56", "#ffd23f")
        + dstroke("M-10 -30L60 -64", "#b5774a", 4)
        + dstroke("M-4 -26L66 -54", "#b5774a", 4)
    )


def cake():
    icing = "M-50 -14C-50 -24 50 -24 50 -14V2C50 10 42 10 42 2V-2C42 10 30 12 30 0C30 12 16 14 16 0V-2C16 8 4 8 4 -2C4 12 -12 14 -12 0C-12 8 -24 8 -24 -2C-24 12 -38 10 -38 0C-38 8 -50 8 -50 0Z"
    return (
        '<g transform="translate(0 6) scale(.94)">'
        + '<ellipse class="k-o" cx="0" cy="48" rx="64" ry="10" fill="#fff"/>'
        + '<rect class="k-o" x="-50" y="-16" width="100" height="62" rx="6" fill="#f5c58c"/>'
        + '<path d="M-48 24H48" stroke="#ef7fa4" stroke-width="6"/>'
        + f'<path class="k-o" d="{icing}" fill="#f78fb3"/>'
        + '<rect class="k-o" x="-5" y="-50" width="10" height="30" rx="2" fill="#9fd8f5"/>'
        + '<path d="M-5 -42L5 -46M-5 -32L5 -36" stroke="#fff" stroke-width="2.5"/>'
        + dstroke("M0 -50V-56", INK, 0.5)
        + '<path class="k-o" d="M0 -72C6 -64 8 -60 0 -56C-8 -60 -6 -64 0 -72Z" fill="#ffb31a" stroke-width="2"/>'
        + '<circle class="k-o" cx="-30" cy="-20" r="6" fill="#ef4f5a" stroke-width="2"/>'
        + '<circle class="k-o" cx="30" cy="-20" r="6" fill="#ef4f5a" stroke-width="2"/>'
        + "</g>"
    )


def pizza():
    cheese = "M-50 -38L0 54L50 -38Z"
    peps = "".join(
        f'<circle class="k-o" cx="{x}" cy="{y}" r="{r}" fill="#e0483f" stroke-width="2"/><circle cx="{x - 2}" cy="{y - 2}" r="1.6" fill="#fff" opacity=".6"/>'
        for x, y, r in ((-18, -16, 9), (16, -18, 8), (0, 14, 8), (-2, -28, 5))
    )
    return (
        shadow(58, 20)
        + f'<path class="k-o" d="{cheese}" fill="#ffd66b"/>'
        + '<path d="M-38 -16L-26 -16L-30 0Z" fill="#ffc23a"/>'
        + peps
        + '<path d="M-10 -2L-4 -6M10 -2L14 4M-24 -30L-20 -34" stroke="#3f9e4d" stroke-width="3" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-56 -36Q0 -60 56 -36Q60 -26 50 -24Q0 -44 -50 -24Q-60 -26 -56 -36Z" fill="#d08a45"/>'
    )


def cookie():
    chips = "".join(
        f'<path d="M{x - 4} {y}Q{x} {y - 6} {x + 4} {y}Q{x} {y + 5} {x - 4} {y}Z" fill="#5a3522"/>'
        for x, y in ((-20, -18), (6, -24), (-28, 8), (-6, 2), (16, 10), (-12, 28), (12, 32), (30, -6))
    )
    return (
        shadow(56, 38)
        + f'<path class="k-o" d="{bitten(48, 40, -34, 18)}" fill="#d9a066"/>'
        + '<path d="M-36 -8A38 38 0 0 1 -16 -34" fill="none" stroke="#f0c48c" stroke-width="5" stroke-linecap="round"/>'
        + chips
    )


FOOD = [
    ("bread", bread), ("egg", egg), ("milk", milk), ("rice", rice),
    ("noodles", noodles), ("cake", cake), ("pizza", pizza), ("cookie", cookie),
]
