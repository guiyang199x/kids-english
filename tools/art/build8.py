"""Body parts, family and weather. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
import math
from common import INK, fmt
from build1 import shadow
from build4 import sun as _sun, union, circ, rrect
from build5 import dstroke, eyes, cheeks, smile

SKIN = "#ffd2b0"
SKIN_DARK = "#f0b48e"
SHINE = 'fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".75"'


# ================================================================ body
def eye():
    lashes = "".join(
        f'<path d="M{fmt(40 * math.cos(a))} {fmt(-6 - 26 * math.sin(a))}L{fmt(50 * math.cos(a))} {fmt(-10 - 36 * math.sin(a))}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        for a in (math.radians(d) for d in (40, 65, 90, 115, 140))
    )
    return (
        '<g transform="translate(0 8)">'
        + '<path d="M-40 -52Q0 -68 40 -52" fill="none" stroke="#7a4a2a" stroke-width="7" stroke-linecap="round"/>'
        + lashes
        + '<path class="k-o" d="M-60 0C-38 -36 38 -36 60 0C38 36 -38 36 -60 0Z" fill="#fff"/>'
        + '<circle cx="0" cy="0" r="22" fill="#5fa3e6"/><circle cx="0" cy="0" r="22" fill="none" stroke="#2f7cc6" stroke-width="3"/>'
        + f'<circle cx="0" cy="0" r="10" fill="{INK}"/>'
        + '<circle cx="-7" cy="-7" r="5" fill="#fff"/><circle cx="7" cy="7" r="2.5" fill="#fff"/>'
        + '<path class="k-o" d="M-60 0C-38 -36 38 -36 60 0C38 36 -38 36 -60 0Z" fill="none"/>'
        + "</g>"
    )


def ear():
    outer = "M-18 -44C-4 -62 40 -56 40 -16C40 10 22 16 18 34C14 52 -10 56 -18 42C-24 30 -30 -26 -18 -44Z"
    waves = "".join(
        f'<path d="M{50 + 9 * k} {-22 - 7 * k}Q{58 + 12 * k} -4 {50 + 9 * k} {14 + 7 * k}" fill="none" stroke="#9b74e8" stroke-width="4" stroke-linecap="round"/>'
        for k in range(3)
    )
    return (
        '<g transform="translate(-14 2)">'
        + shadow(54, 26)
        + f'<path class="k-o" d="{outer}" fill="{SKIN}"/>'
        + f'<path d="M-6 -28C4 -42 28 -38 28 -14C28 2 14 6 10 18C6 28 0 30 -4 24" fill="none" stroke="{SKIN_DARK}" stroke-width="6" stroke-linecap="round"/>'
        + f'<path d="M-6 -28C4 -42 28 -38 28 -14C28 2 14 6 10 18" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<path d="M2 -10C8 -16 16 -12 14 -4" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + waves
        + "</g>"
    )


def nose():
    d = "M0 -48C12 -48 12 -10 28 6C42 22 32 42 14 38C8 46 -8 46 -14 38C-32 42 -42 22 -28 6C-12 -10 -12 -48 0 -48Z"
    return (
        shadow(52, 34)
        + f'<path class="k-o" d="{d}" fill="{SKIN}"/>'
        + f'<ellipse cx="-11" cy="30" rx="5" ry="3.5" fill="{INK}" transform="rotate(20 -11 30)"/>'
        + f'<ellipse cx="11" cy="30" rx="5" ry="3.5" fill="{INK}" transform="rotate(-20 11 30)"/>'
        + '<path d="M-6 -30C-8 -16 -12 -4 -18 4" ' + SHINE + "/>"
        + '<ellipse cx="-30" cy="22" rx="7" ry="4" fill="#ff7d93" opacity=".4"/><ellipse cx="30" cy="22" rx="7" ry="4" fill="#ff7d93" opacity=".4"/>'
    )


def mouth():
    lips = "M-58 -10Q0 -26 58 -10Q44 48 0 48Q-44 48 -58 -10Z"
    inner = "M-46 -6Q0 -16 46 -6Q34 36 0 36Q-34 36 -46 -6Z"
    return (
        shadow(56, 40)
        + f'<path class="k-o" d="{lips}" fill="#ef6b7a"/>'
        + f'<path d="{inner}" fill="#8a3446" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        + f'<path d="M-40 -5Q0 -14 40 -5L38 6Q0 -2 -38 6Z" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        + f'<path d="M-24 34C-22 14 22 14 24 34Q0 40 -24 34Z" fill="#ff8fa3" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        + '<path d="M0 22V32" stroke="#e0607a" stroke-width="2" stroke-linecap="round"/>'
        + '<path d="M-44 -16Q-20 -22 -8 -20" ' + SHINE + "/>"
    )


def hand():
    parts = [
        rrect(-30, -8, 60, 58, 22),
        rrect(-30, -52, 14, 56, 7),
        rrect(-13, -60, 14, 64, 7),
        rrect(4, -56, 14, 60, 7),
        rrect(21, -42, 13, 48, 6.5),
        ("rect", 'x="-40" y="2" width="15" height="42" rx="7.5" transform="rotate(-35 -32 42)"'),
    ]
    return (
        shadow(58, 34)
        + union(parts, SKIN)
        + f'<path d="M-10 20Q0 28 12 20" fill="none" stroke="{SKIN_DARK}" stroke-width="3" stroke-linecap="round"/>'
        + "".join(f'<path d="M{x} {y}h6" stroke="{SKIN_DARK}" stroke-width="2.5" stroke-linecap="round"/>' for x, y in ((-26, -20), (-9, -26), (8, -22), (24, -12)))
    )


def foot():
    parts = [
        ("path", 'd="M-4 -30C22 -34 34 -16 30 6C26 28 30 50 8 54C-14 58 -22 40 -24 22C-26 2 -30 -26 -4 -30Z"'),
        circ(-14, -42, 12), circ(5, -48, 8.5), circ(18, -43, 7.5), circ(28, -34, 6.5), circ(35, -23, 5.5),
    ]
    return (
        '<g transform="translate(-4 4)">'
        + shadow(56, 30)
        + union(parts, SKIN)
        + f'<path d="M-20 -46A6 6 0 0 1 -12 -52" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
        + f'<path d="M-14 22Q-6 30 4 26" fill="none" stroke="{SKIN_DARK}" stroke-width="3" stroke-linecap="round"/>'
        + "</g>"
    )


def tooth():
    d = "M-36 -40C-20 -52 -8 -40 0 -40C8 -40 20 -52 36 -40C52 -26 40 0 36 20C32 40 30 52 20 52C8 52 10 24 0 24C-10 24 -8 52 -20 52C-30 52 -32 40 -36 20C-40 0 -52 -26 -36 -40Z"
    sparkle = lambda x, y, r: f'<path d="M{x} {y - r}Q{x} {y} {x + r} {y}Q{x} {y} {x} {y + r}Q{x} {y} {x - r} {y}Q{x} {y} {x} {y - r}Z" fill="#ffd23f" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
    return (
        shadow(58, 34)
        + f'<path class="k-o" d="{d}" fill="#fff"/>'
        + '<path d="M-30 -30C-36 -20 -34 -6 -30 4" fill="none" stroke="#dbe9f5" stroke-width="6" stroke-linecap="round"/>'
        + eyes(12, -12, 5) + cheeks(24, -2, 6, 3.5) + smile(0, 7, 6)
        + sparkle(52, -40, 10) + sparkle(-54, 20, 7) + sparkle(56, 20, 6)
    )


# ---------------------------------------------------------------- people
def luminance(hex_color):
    """Relative luminance (WCAG) of a #rrggbb color."""
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def eye_whites(x, y, r):
    """White rings behind the pupils, so dark eyes still stand out on dark skin."""
    return "".join(f'<circle cx="{cx}" cy="{y}" r="{fmt(r + 2.5)}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>' for cx in (-x, x))


def person(shirt, back="", front="", extra="", s=1.0, skin=SKIN, head_r=30, eye_r=4.5):
    """A smiling bust: shoulders at the bottom (y 60), head above."""
    hy = -14
    # Ink eyes on dark skin fall below ~3:1 contrast, so add eye whites there.
    whites = eye_whites(11, hy - 2, eye_r) if (luminance(skin) + 0.05) / (luminance(INK) + 0.05) < 3 else ""
    body = (
        back
        + f'<path class="k-o" d="M-52 62C-52 32 -32 22 0 22C32 22 52 32 52 62Z" fill="{shirt}"/>'
        + f'<rect class="k-o" x="-9" y="{hy + head_r - 8}" width="18" height="{30 - head_r + 18}" fill="{skin}"/>'
        + f'<circle class="k-o" cx="-{head_r}" cy="{hy + 2}" r="7" fill="{skin}"/><circle class="k-o" cx="{head_r}" cy="{hy + 2}" r="7" fill="{skin}"/>'
        + f'<circle class="k-o" cx="0" cy="{hy}" r="{head_r}" fill="{skin}"/>'
        + whites
        + eyes(11, hy - 2, eye_r)
        + cheeks(19, hy + 8, 5.5, 3.5)
        + smile(hy + 10, 7, 6)
        + front
        + extra
    )
    return f'<g transform="translate(0 {fmt(62 * (1 - s) - 4)}) scale({s})">{body}</g>'


def glasses(y=-16):
    return (
        f'<circle cx="-11" cy="{y}" r="9" fill="#fff" fill-opacity=".25" stroke="{INK}" stroke-width="2.5"/>'
        f'<circle cx="11" cy="{y}" r="9" fill="#fff" fill-opacity=".25" stroke="{INK}" stroke-width="2.5"/>'
        f'<path d="M-2 {y}H2M-20 {y - 2}L-29 {y - 5}M20 {y - 2}L29 {y - 5}" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def mom():
    hair = "#7a4a2a"
    back = f'<path class="k-o" d="M-36 -14C-40 -54 40 -54 36 -14C38 8 42 26 38 36H-38C-42 26 -38 8 -36 -14Z" fill="{hair}"/>'
    front = f'<path class="k-o" d="M-32 -12C-34 -46 32 -52 32 -10C24 -28 6 -34 -6 -26C-14 -22 -24 -18 -32 -12Z" fill="{hair}"/>'
    extra = '<circle class="k-o" cx="-31" cy="-4" r="3.5" fill="#ffd23f" stroke-width="2"/><circle class="k-o" cx="31" cy="-4" r="3.5" fill="#ffd23f" stroke-width="2"/>'
    return person("#f78fb3", back=back, front=front, extra=extra)


def dad():
    front = '<path class="k-o" d="M-31 -16C-34 -46 -14 -54 2 -52C22 -52 34 -42 31 -16C26 -28 16 -34 4 -32C-8 -38 -22 -32 -31 -16Z" fill="#4a3226"/>'
    brows = f'<path d="M-17 -24H-6M6 -24H17" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    collar = f'<path class="k-o" d="M-12 22L0 36L12 22L6 20L0 28L-6 20Z" fill="#fff" stroke-width="2"/>'
    return person("#4a9be8", front=front + brows, extra=collar)


def grandma():
    hair = "#c9c9d6"
    back = f'<circle class="k-o" cx="0" cy="-48" r="13" fill="{hair}"/>'
    front = f'<path class="k-o" d="M-33 -10C-38 -46 38 -46 33 -10C28 -26 16 -32 0 -30C-16 -32 -28 -26 -33 -10Z" fill="{hair}"/>'
    lines = f'<path d="M-28 -14l-5 -2M28 -14l5 -2" stroke="{INK}" stroke-width="1.5" stroke-linecap="round"/>'
    necklace = "".join(f'<circle cx="{x}" cy="{fmt(24 + (x * x) / 60)}" r="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/>' for x in (-16, -8, 0, 8, 16))
    return person("#9b74e8", back=back, front=front, extra=glasses() + lines + necklace)


def grandpa():
    hair = "#d6d6de"
    sides = f'<path class="k-o" d="M-31 -2C-36 -16 -32 -30 -24 -34C-22 -22 -24 -10 -20 -2Z" fill="{hair}"/><path class="k-o" d="M31 -2C36 -16 32 -30 24 -34C22 -22 24 -10 20 -2Z" fill="{hair}"/>'
    shine = '<path d="M-14 -38A26 26 0 0 1 4 -42" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
    stache = f'<path class="k-o" d="M0 -6C-8 -10 -20 -8 -20 0C-12 0 -6 -2 0 -2C6 -2 12 0 20 0C20 -8 8 -10 0 -6Z" fill="{hair}" stroke-width="2"/>'
    vest = f'<path d="M-12 23L0 60L12 23" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/><circle cx="0" cy="40" r="2.5" fill="{INK}"/><circle cx="0" cy="50" r="2.5" fill="{INK}"/>'
    return person("#a8704a", front=sides + shine, extra=glasses() + stache + vest)


def sister():
    hair = "#b5774a"
    back = "".join(f'<circle class="k-o" cx="{x}" cy="-26" r="13" fill="{hair}"/>' for x in (-38, 38))
    bows = "".join(f'<path class="k-o" d="M{x} -38l-8 -6v12Zm0 0l8 -6v12Z" fill="#ef5b56" stroke-width="2"/>' for x in (-30, 30))
    front = f'<path class="k-o" d="M-32 -12C-34 -46 32 -52 32 -10C26 -24 16 -28 8 -26C0 -32 -10 -24 -16 -26C-22 -24 -28 -18 -32 -12Z" fill="{hair}"/>'
    return person("#ffd23f", back=back, front=front + bows, s=0.84)


def brother():
    front = '<path class="k-o" d="M-31 -12L-32 -34L-22 -38L-18 -52L-6 -44L4 -56L12 -44L26 -48L26 -34L32 -12C22 -28 -22 -28 -31 -12Z" fill="#3b2a20"/>'
    stripe = '<path d="M-48 44H48" stroke="#fff" stroke-width="6"/>'
    return person("#5cc36a", front=front, extra=stripe, s=0.84)


def baby():
    curl = f'<path d="M0 -44C-2 -54 8 -58 12 -52C14 -48 10 -44 6 -46" fill="none" stroke="#b5774a" stroke-width="4" stroke-linecap="round"/>'
    bib = f'<path class="k-o" d="M-18 22C-18 44 18 44 18 22Z" fill="#fff" stroke-width="2.5"/><circle cx="0" cy="32" r="4" fill="#f78fb3"/>'
    return person("#9fd8f5", front=curl, extra=bib, s=0.8, head_r=32, eye_r=5.5)


FAMILY = [
    ("mom", mom), ("dad", dad), ("baby", baby), ("sister", sister),
    ("brother", brother), ("grandma", grandma), ("grandpa", grandpa),
]

BODY = [
    ("eye", eye), ("ear", ear), ("nose", nose), ("mouth", mouth),
    ("hand", hand), ("foot", foot), ("tooth", tooth),
]


# ================================================================ weather
def cloud(cx, cy, s, fill="#fff"):
    return union(
        [
            rrect(cx - 46 * s, cy, 92 * s, 24 * s, 12 * s),
            circ(cx - 26 * s, cy + 4 * s, 18 * s),
            circ(cx + 2 * s, cy - 6 * s, 25 * s),
            circ(cx + 28 * s, cy + 5 * s, 17 * s),
        ],
        fill,
    )


def cloud_face(cx, cy, sleepy=False):
    if sleepy:
        e = f'<path d="M{cx - 14} {cy}q4 3 8 0M{cx + 6} {cy}q4 3 8 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    else:
        e = f'<circle cx="{cx - 10}" cy="{cy}" r="3.5" fill="{INK}"/><circle cx="{cx + 10}" cy="{cy}" r="3.5" fill="{INK}"/>'
    return e + f'<path d="M{cx - 5} {cy + 8}q5 4 10 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'


def drop(x, y, s=1.0):
    return (
        f'<path d="M{x} {y - 9 * s}C{x - 2 * s} {y - 4 * s} {x - 6 * s} {y} {x - 6 * s} {y + 3 * s}A{6 * s} {6 * s} 0 0 0 {x + 6 * s} {y + 3 * s}C{x + 6 * s} {y} {x + 2 * s} {y - 4 * s} {x} {y - 9 * s}Z" '
        f'fill="#5fa3e6" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    )


def flake(x, y, r):
    arms = ""
    for k in range(6):
        a = math.radians(k * 60 + 90)
        ex, ey = x + r * math.cos(a), y + r * math.sin(a)
        arms += f"M{x} {y}L{fmt(ex)} {fmt(ey)}"
        for side in (-1, 1):
            b = a + side * math.radians(40)
            mx, my = x + r * .6 * math.cos(a), y + r * .6 * math.sin(a)
            arms += f"M{fmt(mx)} {fmt(my)}L{fmt(mx + r * .32 * math.cos(b))} {fmt(my + r * .32 * math.sin(b))}"
    return (
        f'<path d="{arms}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="{arms}" stroke="#bfe3ff" stroke-width="3" stroke-linecap="round"/>'
    )


def sunny():
    shades = (
        f'<path d="M-24 -9H24" stroke="{INK}" stroke-width="3"/>'
        f'<path d="M-22 -10H-3V-4C-3 4 -21 4 -22 -4Z" fill="{INK}"/><path d="M3 -10H22V-4C21 4 3 4 3 -4Z" fill="{INK}"/>'
        '<path d="M-18 -7L-12 -7M7 -7L13 -7" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
    )
    return _sun(0, 0) + '<circle cx="0" cy="0" r="30" fill="none"/>' + shades


def cloudy():
    return cloud(20, -34, 0.8, "#eef3fa") + cloud(-8, -2, 1.1) + cloud_face(-6, 8, sleepy=True)


def rainy():
    drops = "".join(drop(x, y) for x, y in ((-34, 18), (-10, 30), (14, 18), (36, 30), (-22, 50), (24, 50)))
    return cloud(0, -28, 1.1, "#c5d3e6") + cloud_face(2, -16) + drops


def snowy():
    return cloud(0, -28, 1.1, "#fff") + cloud_face(2, -16, sleepy=True) + flake(-34, 24, 10) + flake(0, 44, 12) + flake(34, 22, 9)


def windy():
    wind = (
        dstroke("M-66 -24H14C30 -24 34 -46 20 -48C10 -50 6 -40 12 -36", "#8ec5ff", 6)
        + dstroke("M-58 2H40C58 2 62 26 46 28C36 30 32 20 38 16", "#8ec5ff", 6)
        + dstroke("M-66 28H-2C12 28 14 46 2 48C-6 49 -9 42 -5 38", "#8ec5ff", 6)
    )
    leaves = (
        '<g transform="translate(46 -40) rotate(30)"><path class="k-o" d="M0 0C6 -12 22 -14 30 -6C22 4 10 6 0 0Z" fill="#6cc070"/></g>'
        '<g transform="translate(-50 50) rotate(-20)"><path class="k-o" d="M0 0C6 -12 22 -14 30 -6C22 4 10 6 0 0Z" fill="#ff9a3c"/></g>'
    )
    return wind + leaves


def stormy():
    bolt = '<path class="k-o" d="M4 -6L-18 28H-2L-12 58L22 14H6L16 -6Z" fill="#ffd23f"/>'
    return drop(-36, 24) + drop(40, 22) + drop(-28, 48) + drop(34, 46) + bolt + cloud(0, -28, 1.1, "#8f9bb3") + (
        f'<path d="M-14 -22l8 3M16 -22l-8 3" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="-8" cy="-15" r="3.5" fill="{INK}"/><circle cx="10" cy="-15" r="3.5" fill="{INK}"/>'
        f'<path d="M-4 -4q5 -4 10 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def thermometer(level, color):
    top = 36 - level
    ticks = "".join(f'<path d="M12 {y}h7" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>' for y in (-30, -14, 2, 18))
    return (
        '<rect class="k-o" x="-12" y="-52" width="24" height="92" rx="12" fill="#fff"/>'
        + f'<rect x="-5" y="{top}" width="10" height="{40 - top}" rx="5" fill="{color}"/>'
        + f'<circle class="k-o" cx="0" cy="44" r="18" fill="{color}"/>'
        + '<circle cx="-6" cy="38" r="4.5" fill="#fff" opacity=".6"/>'
        + ticks
    )


def hot():
    rays = "".join(
        f'<path d="M{fmt(44 + 20 * math.cos(a))} {fmt(-30 + 20 * math.sin(a))}L{fmt(44 + 27 * math.cos(a))} {fmt(-30 + 27 * math.sin(a))}" stroke="#ffb31a" stroke-width="4.5" stroke-linecap="round"/>'
        for a in (math.radians(k * 45) for k in range(8))
    )
    heat = "".join(f'<path d="M{x} 44q-6 -8 0 -16t0 -16" fill="none" stroke="#ff9a3c" stroke-width="3.5" stroke-linecap="round"/>' for x in (38, 52))
    return '<g transform="translate(-22 0)">' + thermometer(84, "#ef4f5a") + "</g>" + rays + '<circle class="k-o" cx="44" cy="-30" r="15" fill="#ffd23f"/>' + heat


def cold():
    return '<g transform="translate(-22 0)">' + thermometer(18, "#4a9be8") + "</g>" + flake(40, -28, 16) + flake(46, 26, 11)


WEATHER = [
    ("sunny", sunny), ("cloudy", cloudy), ("rainy", rainy), ("snowy", snowy),
    ("windy", windy), ("stormy", stormy), ("hot", hot), ("cold", cold),
]
