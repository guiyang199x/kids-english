import math
from common import INK, fmt, svg_wrap
from build1 import beach_ball

SX, SY, SW, SH = 20, 12, 640, 440


def union(shapes, fill, sw=3):
    """shapes: list of (tag, attrs) -> outlined union via stroke pass + fill pass."""
    a = "".join(f"<{t} {at}/>" for t, at in shapes)
    return f'<g fill="{INK}" stroke="{INK}" stroke-width="{2 * sw}">{a}</g><g fill="{fill}">{a}</g>'


def circ(x, y, r):
    return ("circle", f'cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}"')


def rrect(x, y, w, h, rx):
    return ("rect", f'x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="{fmt(rx)}"')


def cloud(cx, cy, s):
    return union(
        [
            rrect(cx - 46 * s, cy, 92 * s, 24 * s, 12 * s),
            circ(cx - 26 * s, cy + 4 * s, 18 * s),
            circ(cx + 2 * s, cy - 6 * s, 25 * s),
            circ(cx + 28 * s, cy + 5 * s, 17 * s),
        ],
        "#fff",
    )


def sun(cx, cy):
    rays = []
    for k in range(10):
        a = math.radians(k * 36 + 18)
        rays.append(
            f"M{fmt(cx + 43 * math.cos(a))} {fmt(cy + 43 * math.sin(a))}L{fmt(cx + 54 * math.cos(a))} {fmt(cy + 54 * math.sin(a))}"
        )
    return (
        f'<path d="{"".join(rays)}" stroke="#ffb31a" stroke-width="6" stroke-linecap="round"/>'
        f'<circle class="k-o" cx="{cx}" cy="{cy}" r="34" fill="#ffd23f"/>'
        f'<path d="M{cx - 16} {cy - 2}q5 -7 10 0M{cx + 6} {cy - 2}q5 -7 10 0M{cx - 10} {cy + 9}q10 10 20 0" '
        f'fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        f'<ellipse cx="{cx - 20}" cy="{cy + 7}" rx="5.5" ry="3.5" fill="#ff7d4d" opacity=".45"/>'
        f'<ellipse cx="{cx + 20}" cy="{cy + 7}" rx="5.5" ry="3.5" fill="#ff7d4d" opacity=".45"/>'
    )


def bird(x, y):
    return (
        f'<g transform="translate({x} {y})">'
        f'<path class="k-o" d="M-13 -2L-28 -11L-25 5Z" fill="#3d8bd9" stroke-width="2.5"/>'
        f'<ellipse class="k-o" cx="0" cy="0" rx="16" ry="12" fill="#5aa9ee" stroke-width="2.5"/>'
        f'<ellipse cx="4" cy="5" rx="9" ry="5.5" fill="#d9eeff"/>'
        f'<path d="M14 -3L24 0.5L14 4.5Z" fill="#ffb13b" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="M-7 -4C-8 -22 6 -28 11 -21C8 -13 3 -7 -7 -4Z" fill="#3d8bd9" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<circle cx="8" cy="-4" r="2.3" fill="{INK}"/>'
        "</g>"
    )


def tree(x, ground):
    canopy = [circ(x - 34, 186, 38), circ(x + 32, 182, 40), circ(x, 146, 44), circ(x, 200, 40), circ(x - 20, 158, 34), circ(x + 22, 154, 34)]
    apples = [(x - 36, 180), (x + 34, 170), (x - 4, 214), (x + 36, 204), (x - 16, 138), (x + 14, 160)]
    return (
        f'<path class="k-o" d="M{x - 11} {ground}L{x - 8} 200L{x + 8} 200L{x + 11} {ground}Z" fill="#a8703f"/>'
        + union(canopy, "#5dbb63")
        + f'<path d="M{x - 52} 170q8 -10 18 -8M{x + 18} 128q10 -6 18 2M{x + 44} 196q6 8 2 16" fill="none" stroke="#8fd68a" stroke-width="3.5" stroke-linecap="round"/>'
        + "".join(
            f'<circle cx="{ax}" cy="{ay}" r="6.5" fill="#ef5b56" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{ax - 2}" cy="{ay - 2}" r="1.6" fill="#fff" opacity=".8"/>'
            for ax, ay in apples
        )
    )


def house():
    return (
        '<path class="k-o" d="M462 178H480V214H462Z" fill="#c9403b"/>'
        + union([circ(476, 160, 6), circ(486, 146, 8), circ(500, 128, 10)], "#fff", 2)
        + '<rect class="k-o" x="372" y="224" width="120" height="96" fill="#ffe1a8"/>'
        + '<path class="k-o" d="M356 232L432 170L508 232Z" fill="#ef5b56"/>'
        + '<path d="M388 219L432 183L476 219" fill="none" stroke="#d8453f" stroke-width="3" stroke-linecap="round"/>'
        + '<path class="k-o" d="M419 320V284A13 13 0 0 1 445 284V320Z" fill="#4a9be8"/>'
        + f'<circle cx="439" cy="302" r="2.5" fill="{INK}"/>'
        + "".join(
            f'<rect class="k-o" x="{wx}" y="248" width="28" height="28" rx="3" fill="#cdeeff"/>'
            f'<path d="M{wx + 14} 248V276M{wx} 262H{wx + 28}" stroke="{INK}" stroke-width="2.5"/>'
            for wx in (382, 454)
        )
    )


def flower(x, y, petal, h=34):
    pts = []
    for k in range(5):
        a = math.radians(k * 72 - 90)
        pts.append(circ(x + 9 * math.cos(a), y + 9 * math.sin(a), 7.5))
    return (
        f'<path d="M{x} {y}V{y + h}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M{x} {y}V{y + h}" stroke="#3f9e4d" stroke-width="2.5" stroke-linecap="round"/>'
        f'<path class="k-o" d="M{x} {y + h - 8}C{x + 4} {y + h - 20} {x + 16} {y + h - 22} {x + 18} {y + h - 18}C{x + 14} {y + h - 10} {x + 6} {y + h - 6} {x} {y + h - 8}Z" fill="#5cc36a" stroke-width="2"/>'
        + union(pts, petal, 2)
        + f'<circle cx="{x}" cy="{y}" r="5.5" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
    )


def butterfly(x, y):
    up = "M1 -2C6 -22 30 -28 29 -11C28 -2 14 2 1 0Z"
    lo = "M1 2C13 1 23 7 19 17C15 25 4 18 1 4Z"
    wing = (
        f'<path class="k-o" d="{up}" fill="#b58cff" stroke-width="2.5"/>'
        f'<path class="k-o" d="{lo}" fill="#f78fb3" stroke-width="2.5"/>'
        '<circle cx="18" cy="-12" r="4" fill="#fff" opacity=".75"/>'
        '<circle cx="12" cy="11" r="2.8" fill="#fff" opacity=".75"/>'
    )
    return (
        f'<g transform="translate({x} {y}) rotate(-10)">'
        f'<path d="M-1 -15Q-4 -24 -10 -27M1 -15Q4 -24 10 -27" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="-10" cy="-27" r="2.2" fill="{INK}"/><circle cx="10" cy="-27" r="2.2" fill="{INK}"/>'
        f'{wing}<g transform="scale(-1 1)">{wing}</g>'
        f'<ellipse cx="0" cy="1" rx="3.5" ry="13" fill="{INK}"/><circle cx="0" cy="-13" r="4" fill="{INK}"/>'
        "</g>"
    )


DOG_EAR = '<path class="k-o" d="M-24 -42C-42 -50 -62 -40 -66 -16C-69 4 -62 22 -52 24C-42 26 -38 14 -36 -2C-34 -18 -30 -32 -24 -42Z" fill="#b5774a"/>'


def dog(x, y, s):
    tan = "#f2cf98"
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M26 64C44 60 52 44 50 28" fill="none" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>'
        f'<path d="M26 64C44 60 52 44 50 28" fill="none" stroke="#b5774a" stroke-width="11" stroke-linecap="round"/>'
        f'<path class="k-o" d="M-30 40C-40 60 -40 86 -30 92H30C40 86 40 60 30 40Z" fill="{tan}"/>'
        f'<ellipse cx="0" cy="58" rx="13" ry="16" fill="#fff4e2"/>'
        f'<rect class="k-o" x="-17" y="60" width="13" height="34" rx="6.5" fill="{tan}"/>'
        f'<rect class="k-o" x="4" y="60" width="13" height="34" rx="6.5" fill="{tan}"/>'
        f'<path class="k-o" d="M-44 -2C-44 -32 -24 -44 0 -44C24 -44 44 -32 44 -2C44 30 26 50 0 50C-26 50 -44 30 -44 -2Z" fill="{tan}"/>'
        f'<path d="M8 -20C18 -26 32 -22 34 -10C36 2 26 8 16 6C6 4 2 -12 8 -20Z" fill="#dca565"/>'
        f'{DOG_EAR}<g transform="scale(-1 1)">{DOG_EAR}</g>'
        f'<ellipse cx="0" cy="25" rx="22" ry="17" fill="#fff4e2"/>'
        f'<circle cx="-17" cy="-6" r="6.5" fill="{INK}"/><circle cx="17" cy="-6" r="6.5" fill="{INK}"/>'
        f'<circle cx="-15" cy="-8.5" r="2.3" fill="#fff"/><circle cx="19" cy="-8.5" r="2.3" fill="#fff"/>'
        f'<path d="M-5 29C-6 39 6 39 5 29Z" fill="#ff7c93" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="M0 20L0 26M0 26C-3 31 -11 31 -13 26M0 26C3 31 11 31 13 26" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        f'<ellipse cx="0" cy="15" rx="9" ry="6.5" fill="{INK}"/>'
        f'<ellipse cx="-3" cy="13" rx="3" ry="1.6" fill="#fff" opacity=".8"/>'
        "</g>"
    )


def small_ball(x, y, r):
    parts = beach_ball(r=r, cx=x, cy=y, tilt=55, rho=22, offset=-20)
    parts = [p.replace('stroke-width="2"', 'stroke-width="1.5"') for p in parts]
    return (
        f'<ellipse cx="{x}" cy="{y + r}" rx="{r}" ry="3.5" fill="{INK}" opacity=".15"/>'
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' + "".join(parts) + f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    )


def tufts(pts):
    return "".join(
        f'<path d="M{x - 6} {y}l2 -8M{x} {y}v-11M{x + 6} {y}l-2 -8" fill="none" stroke="#4fa94f" stroke-width="2.5" stroke-linecap="round"/>'
        for x, y in pts
    )


def pill(text, cx, cy, to=None):
    w = round(len(text) * 8.6 + 24)
    out = ""
    if to:
        out += f'<path d="M{fmt(cx)} {fmt(cy)}L{fmt(to[0])} {fmt(to[1])}" stroke="{INK}" stroke-width="1.5"/>'
        out += f'<circle cx="{fmt(to[0])}" cy="{fmt(to[1])}" r="3" fill="{INK}"/>'
    out += (
        f'<rect x="{fmt(cx - w / 2)}" y="{fmt(cy - 13)}" width="{w}" height="26" rx="13" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
        f'<text class="k-f" x="{fmt(cx)}" y="{fmt(cy + 5)}" font-size="15" fill="{INK}" text-anchor="middle">{text}</text>'
    )
    return out


scene = [
    f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#cdeeff"/>',
    sun(584, 82),
    cloud(160, 58, 1.0),
    cloud(372, 70, 0.7),
    bird(286, 128),
    '<path d="M20 252C140 202 260 212 360 240C460 268 560 222 660 232V452H20Z" fill="#a5dc8e"/>',
    tree(106, 316),
    '<path d="M20 318C160 296 300 304 420 314C520 322 600 306 660 300V452H20Z" fill="#7ccb6b"/>',
    '<path d="M421 318C418 356 392 398 352 452H458C462 400 452 356 443 318Z" fill="#f5dfb3"/>',
    house(),
    tufts([(60, 350), (300, 334), (520, 342), (250, 440), (620, 330), (80, 432)]),
    flower(170, 372, "#f78fb3"),
    flower(206, 390, "#b58cff", 30),
    flower(140, 400, "#ff9a3c", 30),
    butterfly(272, 360),
    dog(538, 366, 0.6),
    small_ball(618, 420, 14),
]

labels = [
    pill("sun", 584, 160),
    pill("cloud", 262, 60, (207, 66)),
    pill("bird", 330, 170, (296, 140)),
    pill("tree", 62, 282, (93, 266)),
    pill("house", 560, 268, (494, 268)),
    pill("flower", 88, 378, (130, 376)),
    pill("butterfly", 300, 414, (280, 374)),
    pill("dog", 468, 398, (514, 392)),
    pill("ball", 618, 370, (618, 403)),
]

body = (
    f'<defs><clipPath id="k-scene"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="24"/></clipPath></defs>'
    + f'<g clip-path="url(#k-scene)">{"".join(scene)}</g>'
    + f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="24" fill="none" stroke="{INK}" stroke-width="3"/>'
    + "".join(labels)
)

svg = svg_wrap(
    SY + SH + 12,
    "Picture dictionary: a sunny day",
    "A sunny outdoor scene with labeled words: sun, cloud, bird, tree, house, flower, butterfly, dog and ball.",
    body,
)
open("scene.svg", "w").write(svg)
print(len(svg), "bytes")
