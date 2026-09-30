"""The island maps: the world map (six theme islands on a sea, with a horizon) and the inside of each island.

Every island is drawn in three layers so the eye goes to the stops first:
  ground (pale, no outlines except the coast) -> road (soft edges) -> stops (full color, drawn by js/views/island.js on top).
Things that move have a class (see "islands" in style.css); they are wrapped in a group of their own,
because a CSS animation replaces an element's transform attribute.

WORLD (exported next to ART) tells the map pages (js/views/) where things are: island middles, where the boat moors,
where each island's stops sit on its road. Change a road here and its stop positions together.
"""
import json
import math

from common import INK, fmt, smooth_path
from build4 import union, circ, house
from build15 import barn, seagull, sandcastle, crab, shell
import build14

SEA, SHALLOW, SAND = "#8fd3f4", "#bfe9fb", "#f8e6bf"
# Colors of things far away: pale and a little blue, like real distance (lighter = farther).
HAZE_SAND, HAZE_HILL, HAZE_MARK = "#d3e3ec", "#b8d0de", "#a6c3d5"


# ---------------------------------------------------------------- shapes
def blob(cx, cy, rx, ry, seed, n=14, wob=0.12):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + wob * math.sin(3 * a + seed) + wob * 0.6 * math.sin(5 * a + seed * 2.3)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return smooth_path(pts, closed=True)


def sblob(cx, cy, rx, ry, seed, p=3.0, n=24, wob=0.03):
    """A rounded-square blob (a superellipse with a little wobble): more room inside than an ellipse."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        r = (abs(c) ** p + abs(s) ** p) ** (-1 / p) * (1 + wob * math.sin(3 * a + seed))
        pts.append((cx + rx * r * c, cy + ry * r * s))
    return smooth_path(pts, closed=True)


def at(x, y, s, inner, cls=None, delay=None):
    """Place `inner` at (x, y), scaled by s; with `cls`, inside an animated group of its own."""
    if cls:
        d = f' style="animation-delay:{delay}s"' if delay is not None else ""
        inner = f'<g class="{cls}"{d}>{inner}</g>'
    return f'<g transform="translate({fmt(x)} {fmt(y)}) scale({s})">{inner}</g>'


def waves(pts, near=None):
    """Little white waves. With `near` (a function of y giving 0 at the horizon to 1 at the bottom, see depth()),
    far ones are smaller and fainter."""
    out = ""
    for i, (x, y) in enumerate(pts):
        wave = (f'<path class="wave" style="animation-delay:-{i * 0.7:.1f}s" d="M0 0q7 -6 14 0t14 0" fill="none" '
                f'stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
        t = near(y) if near else 1
        size = DEPTH[0] + DEPTH[1] * t if near else 1
        out += f'<g transform="translate({x} {y}) scale({size:.2f})" opacity="{.45 + .55 * t:.2f}">{wave}</g>'
    return out


# ---------------------------------------------------------------- depth
# On the world map, things far off (up near the horizon) are drawn smaller and paler than near ones (down at the
# bottom), the way real distance looks. DEPTH is the size at the horizon and how much it grows down to the bottom
# edge; world.js scales Pip's boat the same way as it sails (WORLD.<layout>.depth).
DEPTH = (0.62, 0.6)


def depth(HZ, H):
    """How near a point at height y is: 0 at the horizon, 1 at the bottom edge."""
    return lambda y: max(0.0, min(1.0, (y - HZ) / (H - HZ)))


def haze(t):
    """A CSS filter that washes a far thing out a little: less color and contrast, a bit lighter."""
    f = 1 - t
    return f"saturate({1 - .4 * f:.2f}) contrast({1 - .22 * f:.2f}) brightness({1 + .1 * f:.2f})"


# ---------------------------------------------------------------- small things
def block(x, y, s, letter, col, dark, delay=0, still=False):
    """A letter block, drawn a little from above (front face, top and side). Now and then it hops, unless `still`."""
    w = 40
    return at(x, y, s,
        f'<path class="k-o" d="M0 0L10 -10H{w + 10}L{w} 0Z" fill="#fff"/>'
        f'<path class="k-o" d="M{w} 0L{w + 10} -10V{w - 10}L{w} {w}Z" fill="{dark}"/>'
        f'<rect class="k-o" x="0" y="0" width="{w}" height="{w}" rx="4" fill="{col}"/>'
        f'<text x="{w / 2}" y="{w / 2 + 1}" text-anchor="middle" dominant-baseline="central" font-size="28" '
        f'font-weight="900" fill="#fff" stroke="{INK}" stroke-width="1.5" paint-order="stroke" '
        f'font-family="Nunito, sans-serif">{letter}</text>', cls=None if still else "hop", delay=delay)


def rainbow(x, y, s):
    cols = ["#ef5b56", "#ffb13b", "#ffd23f", "#6cc070", "#4a9be8", "#8150c4"]
    arcs = "".join(
        f'<path d="M{-70 + i * 9} 0A{70 - i * 9} {70 - i * 9} 0 0 1 {70 - i * 9} 0" fill="none" stroke="{c}" stroke-width="9"/>'
        for i, c in enumerate(cols)
    )
    return at(x, y, s,
        f'<g class="shimmer"><path d="M-74 0A74 74 0 0 1 74 0H20A20 20 0 0 0 -20 0Z" fill="none" stroke="{INK}" stroke-width="3"/>{arcs}</g>'
        + '<g class="puff">' + union([circ(-70, 2, 14), circ(-56, 6, 12), circ(-84, 6, 10)], "#fff", 2.5) + "</g>"
        + '<g class="puff" style="animation-delay:-1.5s">' + union([circ(70, 2, 14), circ(56, 6, 12), circ(84, 6, 10)], "#fff", 2.5) + "</g>")


def shape_rocks(x, y, s, still=False):
    hop = (lambda d, el: el) if still else (lambda d, el: f'<g class="hop" style="animation-delay:{d}s">{el}</g>')
    return at(x, y, s,
        hop(-1, f'<path class="k-o" d="M-40 10L-26 -14L-12 10Z" fill="#ffd23f"/>')
        + hop(-2.3, f'<circle class="k-o" cx="8" cy="0" r="11" fill="#4a9be8"/>')
        + hop(-3.1, f'<rect class="k-o" x="26" y="-10" width="20" height="20" rx="3" fill="#ef5b56"/>'))


def crayon(x, y, s, col, rot=0):
    return at(x, y, s,
        f'<g transform="rotate({rot})"><rect class="k-o" x="-9" y="-50" width="18" height="50" rx="2" fill="{col}"/>'
        f'<path class="k-o" d="M-9 -50L0 -68L9 -50Z" fill="#f6dca5"/><path d="M-3 -62L0 -68L3 -62Z" fill="{col}"/>'
        f'<path d="M-9 -40H9M-9 -12H9" stroke="{INK}" stroke-width="2" opacity=".5"/></g>')


def building(x, base, w, h, col, win="#cdeeff", lit=True):
    rows = int((h - 20) // 22)
    cls = ' class="win"' if lit else ""
    wins = "".join(
        f'<rect{cls} style="animation-delay:-{(r * 7 + c * 3) % 9}s" x="{x + 8 + c * 16}" y="{base - h + 12 + r * 22}" '
        f'width="10" height="12" rx="2" fill="{win}" stroke="{INK}" stroke-width="1.8"/>'
        for r in range(rows) for c in range(int((w - 8) // 16))
    )
    return f'<rect class="k-o" x="{x}" y="{base - h}" width="{w}" height="{h}" rx="4" fill="{col}"/>' + wins


def traffic_light(x, y, s):
    return at(x, y, s,
        f'<rect class="k-o" x="-7" y="-50" width="14" height="36" rx="5" fill="{INK}"/>'
        f'<path d="M0 -14V0" stroke="{INK}" stroke-width="4"/>'
        '<circle class="tl" cx="0" cy="-42" r="4" fill="#ef5b56"/>'
        '<circle class="tl" style="animation-delay:-2s" cx="0" cy="-32" r="4" fill="#ffd23f"/>'
        '<circle class="tl" style="animation-delay:-4s" cx="0" cy="-22" r="4" fill="#6cc070"/>')


def city(x, y, s):
    return at(x, y, s,
        building(-70, 0, 42, 70, "#f2a65a") + building(-26, 0, 48, 104, "#7fb3e8") + building(24, 0, 42, 82, "#d98bb6")
        + traffic_light(79, 0, 1))


def palm(x, y, s, still=False):
    leaves = "".join(
        f'<path class="k-o" d="M0 -60C{dx * 0.4} {-74 + dy * 0.3} {dx * 0.8} {-70 + dy * 0.6} {dx} {-56 + dy}C{dx * 0.6} {-62 + dy * 0.5} {dx * 0.3} {-62} 0 -60Z" fill="#5dbb63" stroke-width="2.5"/>'
        for dx, dy in ((-46, 6), (46, 6), (-34, -18), (34, -18), (0, -26))
    )
    return at(x, y, s,
        f'<path class="k-o" d="M-6 0C-2 -20 -4 -40 -2 -60H4C4 -40 6 -20 6 0Z" fill="#c98a4b"/>{leaves}'
        '<circle cx="-4" cy="-56" r="5" fill="#8b5a3c" stroke="#3f3345" stroke-width="2"/><circle cx="5" cy="-54" r="5" fill="#8b5a3c" stroke="#3f3345" stroke-width="2"/>',
        cls=None if still else "sway")


def lighthouse(x, y, s):
    return at(x, y, s,
        f'<path d="M14 -80L60 -98M14 -76L60 -64" class="beam" stroke="#ffd23f" stroke-width="5" stroke-linecap="round"/>'
        f'<path class="k-o" d="M-16 0L-11 -70H11L16 0Z" fill="#fff"/>'
        f'<path d="M-14 -20H14M-12.5 -44H12.5" stroke="#ef5b56" stroke-width="10"/>'
        f'<path d="M-16 0L-11 -70H11L16 0Z" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<rect class="k-o" x="-12" y="-86" width="24" height="16" rx="3" fill="#ffd23f"/>'
        f'<path class="k-o" d="M-15 -86L0 -100L15 -86Z" fill="#ef5b56"/>')


def smoke(x, y):
    return "".join(
        f'<circle class="smoke" style="animation-delay:-{d}s" cx="{fmt(x)}" cy="{fmt(y)}" r="5" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
        for d in (0, 1.4)
    )


def goal_flag(x, y, s, cloth="#ffd23f"):
    flag = build14.START_FLAG.replace("#ef5b56", cloth).replace('<path class="k-o" d="M0 -30C10', '<path class="k-o cloth" d="M0 -30C10')
    return at(x, y, s, flag)


def bunting(x0, x1, y, sag=22):
    cols = ["#ef5b56", "#ffd23f", "#4a9be8", "#6cc070", "#d65b9a", "#ffb13b"]
    n = int((x1 - x0) // 18)
    mid = (x0 + x1) / 2
    flags = "".join(
        f'<path d="M{x0 + 6 + k * 18:.0f} {y + sag * (1 - ((x0 + 6 + k * 18 - mid) / ((x1 - x0) / 2)) ** 2):.1f}l7 15l7 -15Z" '
        f'fill="{cols[k % 6]}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        for k in range(n)
    )
    return f'<g opacity=".9"><path d="M{x0} {y}Q{mid} {y + 2 * sag} {x1} {y}" fill="none" stroke="{INK}" stroke-width="2"/>{flags}</g>'


# ---------------------------------------------------------------- world map
# (id, rx, ry, seed, grass); names and lessons are in js/content/islands.js (ISLANDS)
ISLANDS = [
    ("abc", 130, 92, 1.0, "#c9ecac"),
    ("num", 120, 84, 2.1, "#dcefa4"),
    ("town", 132, 96, 3.3, "#c4e9c9"),
    ("nature", 140, 100, 4.2, "#b7e4b0"),
    ("city", 128, 94, 5.5, "#d2ebb4"),
    ("beach", 112, 82, 0.4, "#f9e7bf"),
]
FAR = (3, 4, 5)  # these start far off on the horizon, until a child first sails to them


def island(cx, cy, rx, ry, seed, grass):
    return (
        f'<path d="{blob(cx, cy + 6, rx * 1.12, ry * 1.14, seed)}" fill="{SHALLOW}"/>'
        f'<path class="k-o" d="{blob(cx, cy, rx, ry, seed)}" fill="#f6dca5"/>'
        f'<path d="{blob(cx, cy - 4, rx * 0.84, ry * 0.8, seed)}" fill="{grass}" stroke="{INK}" stroke-width="2" stroke-opacity=".25"/>'
    )


def landmark(iid, cx, cy):
    """Each island's landmark on the world map, placed relative to the island's middle."""
    if iid == "abc":
        return (block(cx - 52, cy - 40, 1.0, "A", "#ef5b56", "#c94c48", -0.5) + block(cx - 4, cy - 40, 1.0, "B", "#4a9be8", "#3a79b5", -2)
                + block(cx - 28, cy - 86, 1.0, "C", "#6cc070", "#4f8127", -3.2)
                + at(cx - 90, cy + 15, .8, build14.TREE, "sway") + at(cx + 72, cy + 20, .7, build14.FLOWERS, "sway", -1))
    if iid == "num":
        return rainbow(cx, cy + 18, 0.95) + shape_rocks(cx - 30, cy + 46, 0.8)
    if iid == "town":
        return (at(cx - 221, cy - 124, .42, house()) + at(cx - 116, cy - 101, .36, house())
                + smoke(cx - 11, cy - 72) + smoke(cx + 64, cy - 57)
                + at(cx + 50, cy + 30, .6, build14.BUSH) + at(cx - 60, cy + 20, .6, build14.FLOWERS, "sway"))
    if iid == "nature":
        return (at(cx - 50, cy + 20, .5, barn(-94, 94, 0)) + at(cx + 60, cy - 10, .85, build14.TREE, "sway")
                + at(cx + 100, cy + 30, .7, build14.PINE, "sway", -1.2) + at(cx + 20, cy + 50, .6, build14.POND))
    if iid == "city":
        return city(cx, cy + 20, 0.95)
    return palm(cx - 30, cy + 20, 0.9) + lighthouse(cx + 50, cy + 20, 0.75)


def far_isle(i, iid, x, hz, s):
    """An island nobody has visited yet, seen from far off: a side-view silhouette standing on the horizon."""
    if iid == "nature":
        mark = ('<path d="M-44 -28V-52L-30 -64L-16 -52V-28Z"/><circle cx="14" cy="-56" r="15"/>'
                '<rect x="11" y="-44" width="6" height="18"/><path d="M40 -26L51 -70L62 -26Z"/>')
    elif iid == "city":
        mark = ('<rect x="-46" y="-72" width="26" height="46" rx="3"/><rect x="-16" y="-98" width="30" height="72" rx="3"/>'
                '<rect x="18" y="-62" width="26" height="36" rx="3"/>')
        mark += "".join(f'<rect x="{wx}" y="{wy}" width="6" height="8" rx="1" fill="{HAZE_SAND}"/>'
                        for wx, wy in ((-40, -62), (-30, -62), (-40, -48), (-9, -88), (3, -88), (-9, -72), (3, -72), (-9, -56), (24, -52), (34, -52)))
    else:  # beach
        mark = (f'<path d="M-30 -26C-28 -44 -31 -58 -27 -72" fill="none" stroke="{HAZE_MARK}" stroke-width="6" stroke-linecap="round"/>'
                '<path d="M-27 -72C-40 -80 -54 -76 -60 -66C-48 -70 -38 -70 -27 -72ZM-27 -72C-16 -82 0 -80 6 -70C-6 -74 -16 -74 -27 -72Z'
                'M-27 -72C-30 -86 -22 -94 -12 -96C-20 -88 -24 -80 -27 -72Z"/>'
                '<path d="M20 -26L25 -82H39L44 -26Z"/><rect x="23" y="-94" width="18" height="12" rx="2"/><path d="M21 -94L32 -106L43 -94Z"/>'
                '<circle class="far-lamp" cx="32" cy="-88" r="4" fill="#fff6c0"/>')
    inner = (
        f'<path d="M-92 0C-72 -12 72 -12 92 0Z" fill="{HAZE_SAND}"/>'
        f'<path d="M-74 -5C-62 -40 -22 -46 0 -30C22 -52 62 -42 76 -5Z" fill="{HAZE_HILL}"/>'
        f'<g fill="{HAZE_MARK}">{mark}</g>'
        '<path d="M-78 7H78" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".55"/>'
    )
    mist = (f'<path class="mist" d="M{x - 120 * s:.0f} {hz - 18}h{70 * s:.0f}M{x + 40 * s:.0f} {hz - 34}h{90 * s:.0f}" '
            'stroke="#fff" stroke-width="5" stroke-linecap="round"/>')
    return f'<g class="far" data-i="{i}"><g transform="translate({x} {hz}) scale({s})">{inner}</g>{mist}</g>'


def boat_with_pip(s=0.9):
    pip = f'<g transform="translate(0 -44) scale(.42)">{build14.pip("wave", extra=build14.WAVE_LINES)}</g>'
    return (
        f'<g class="bob"><g transform="scale({s})">'
        f'<path d="M4 -44V-118" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M4 -44V-118" stroke="#c98a4b" stroke-width="3"/>'
        f'<path class="k-o" d="M8 -114L52 -60H8Z" fill="#fff"/>'
        f'<path class="k-o" d="M4 -118L22 -112L4 -106Z" fill="#ffd23f" stroke-width="2"/>'
        + pip
        + f'<path class="k-o" d="M-50 -14H56L42 8H-38Z" fill="#ef5b56"/>'
        + '<path d="M-40 -4H46" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
        + "</g></g>"
        + '<path class="wake" d="M-66 12q10 -6 20 0t20 0M40 12q10 -6 20 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    )


def gulls(specs, W):
    """Seagulls flying across, left to right, each on its own loop."""
    return "".join(
        f'<g class="gull-fly" style="--dist:{W + 140}px;--dur:{dur}s;animation-delay:-{delay}s"><g class="glide">'
        f'<g class="flap">{seagull(-70, y, sc)}</g></g></g>'
        for y, sc, dur, delay in specs
    )


def compass(x, y):
    return at(x, y, 1,
        f'<circle class="k-o" r="30" fill="#fff6d9"/>'
        f'<g class="needle"><path class="k-o" d="M0 -26L7 0L0 26L-7 0Z" fill="#fff" stroke-width="2.5"/>'
        f'<path d="M0 -26L7 0H-7Z" fill="#ef5b56" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/></g>'
        f'<text y="-36" text-anchor="middle" font-size="16" font-weight="900" fill="{INK}" font-family="Nunito, sans-serif">N</text>')


def soft_cloud(x, y, s):
    return (f'<g opacity=".85" fill="#fff"><ellipse cx="{x}" cy="{y}" rx="{46 * s}" ry="{14 * s}"/>'
            f'<circle cx="{x - 14 * s}" cy="{y - 8 * s}" r="{16 * s}"/><circle cx="{x + 12 * s}" cy="{y - 12 * s}" r="{20 * s}"/></g>')


# Two arrangements of the same islands: wide screens get a landscape sea, phones a tall one.
# HZ is the horizon; far islands stand on it at x = far[index]. visit is where a visitor like the Ghost Ship (build24)
# floats in its season: its waterline middle and its size.
LAYOUTS = {
    "wide": dict(W=1000, H=940, HZ=190, far_s=.95, far={3: 820, 4: 520, 5: 200}, far_label_gap=58,
                 pos=[(180, 370), (500, 330), (830, 400), (820, 720), (500, 650), (180, 720)],
                 visit=(660, 560, .9), gulls=[(90, .55, 30, 5), (560, .6, 34, 17)], compass=(940, 250), clouds=[(360, 52, .7), (690, 78, .55)],
                 waves=[(90, 540), (330, 480), (660, 510), (380, 820), (640, 830), (940, 560), (60, 250), (700, 240), (950, 860), (330, 230)]),
    "tall": dict(W=700, H=1490, HZ=260, far_s=.8, far={3: 560, 4: 145, 5: 355}, far_label_gap=112,
                 pos=[(190, 410), (510, 570), (190, 760), (510, 930), (190, 1100), (500, 1230)],
                 visit=(575, 395, .9), gulls=[(40, .5, 20, 2), (990, .6, 26, 12)], compass=(52, 305), clouds=[],
                 waves=[(40, 570), (600, 740), (40, 930), (620, 1100), (60, 1300), (330, 880), (360, 490), (300, 300)]),
}


def dock(cx, cy, rx, W):
    """Where the boat moors: on the sea side of the island, towards the middle of the map."""
    return (cx + rx + 34, cy + 22) if cx < W / 2 else (cx - rx - 34, cy + 22)


def world(name):
    """The whole world map for one layout, and where things are on it (for js/views/world.js).
    Every island is drawn both near (class isle-g) and, for the FAR ones, as a silhouette on the horizon;
    world.js shows one or the other depending on whether the child has been there."""
    L = LAYOUTS[name]
    W, H, HZ, pos, far = L["W"], L["H"], L["HZ"], L["pos"], L["far"]
    body = (f'<defs><linearGradient id="sky-{name}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe6ff"/>'
            f'<stop offset="1" stop-color="#eef9ff"/></linearGradient>'
            # the sea: pale at the horizon, deeper blue nearer the bottom
            f'<linearGradient id="sea-{name}" gradientUnits="userSpaceOnUse" x1="0" y1="{HZ}" x2="0" y2="{H}">'
            f'<stop offset="0" stop-color="#dcf3fd"/><stop offset="{320 / (H - HZ):.2f}" stop-color="{SEA}"/>'
            f'<stop offset="1" stop-color="#6dc3ec"/></linearGradient></defs>')
    near = depth(HZ, H)
    size = lambda y: DEPTH[0] + DEPTH[1] * near(y)
    body += f'<rect x="0" y="0" width="{W}" height="{H}" rx="40" fill="url(#sky-{name})"/>'
    body += "".join(soft_cloud(x, y, sc) for x, y, sc in L["clouds"])
    body += (f'<path d="M0 {HZ}H{W}V{H - 40}A40 40 0 0 1 {W - 40} {H}H40A40 40 0 0 1 0 {H - 40}Z" fill="url(#sea-{name})"/>'
             f'<path d="M0 {HZ}H{W}" stroke="#fff" stroke-width="3" opacity=".8"/>')
    for k in FAR:
        body += far_isle(k, ISLANDS[k][0], far[k], HZ, L["far_s"])
    body += waves(L["waves"], near)
    for k, (a, b) in enumerate(zip(pos, pos[1:])):
        body += (f'<path class="route seg" data-a="{k}" data-b="{k + 1}" '
                 f'd="M{a[0]} {a[1]}Q{(a[0] + b[0]) / 2 + (40 if k % 2 else -40)} {(a[1] + b[1]) / 2 + 30} {b[0]} {b[1]}" '
                 'fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round"/>')
    for k, ((iid, rx, ry, seed, grass), (cx, cy)) in enumerate(zip(ISLANDS, pos)):
        glide = f' style="--fx:{far[k] - cx}px;--fy:{HZ - 40 - cy}px"' if k in far else ""
        # scaled and hazed for its distance, in an inner group (the outer one moves with CSS)
        s = size(cy)
        body += (f'<g class="isle-g" data-i="{k}"{glide}><g transform="translate({cx} {cy}) scale({s:.3f}) translate({-cx} {-cy})" '
                 f'style="filter:{haze(near(cy))}">' + island(cx, cy, rx, ry, seed, grass) + landmark(iid, cx, cy) + "</g></g>")
    # the Ghost Ship, hidden unless it's visiting (world.js shows it in October)
    from build24 import ghost_ship  # build24 draws with this file's neighbours, so it's imported here
    vx, vy, vs = L["visit"]
    vs *= size(vy)
    body += f'<g class="visit-g" data-visit="halloween">{at(vx, vy, vs, ghost_ship())}</g>'
    body += gulls(L["gulls"], W)
    body += f'<g class="boat"><g class="boat-flip">{boat_with_pip()}</g></g>'
    body += compass(*L["compass"])
    svg = f'<svg class="world-art" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>'
    data = {
        "W": W, "H": H,
        "pos": pos,
        "docks": [dock(cx, cy, isl[1] * size(cy), W) for isl, (cx, cy) in zip(ISLANDS, pos)],
        "farDocks": {k: (x, HZ + 24) for k, x in far.items()},
        # name plates, in percent of the map: under each island, and above each far silhouette
        "labels": [(round(cx / W * 100, 1), round((cy + isl[2] * size(cy) + 8) / H * 100, 1)) for isl, (cx, cy) in zip(ISLANDS, pos)],
        # for the boat: the horizon, the bottom edge and DEPTH, so it's scaled like the islands where it sails
        "depth": [HZ, H, *DEPTH],
        # the visitor: where it floats and where the boat moors next to it
        "visit": {"pos": (vx, vy - 50 * vs), "dock": (round(vx - 150 * vs), round(vy + 6))},
        "farLabels": {k: (round(x / W * 100, 1), round((HZ - 100 * L["far_s"] - L["far_label_gap"]) / H * 100, 1)) for k, x in far.items()},
    }
    return svg, data


# ---------------------------------------------------------------- inside the islands
# Each island is a 700 x 980 picture (Nature Island is taller, see NATURE_H): sea, the island, a road from the dock at the bottom to a goal at the top,
# and the stops along the road (in order). ROAD_STYLES: edge, fill, dash color, dash pattern, dash width.
IW, IH = 700, 980
ROAD_STYLES = {
    "sand": ("#dcb67c", "#f8e7c0", "#fff", "2 18", 5),
    "trail": ("#c7a169", "#eed8ab", "#fffaf0", "2 22", 5),
    "street": ("#b9b2c6", "#e7e3ee", "#fff", "18 16", 4),
    "boardwalk": ("#b98a55", "#e8c592", "#c99a66", "3 11", 34),
}


def road(d, kind):
    edge, fill, dash, pattern, dw = ROAD_STYLES[kind]
    return (f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path class="road-line" d="{d}" fill="none" stroke="{dash}" stroke-width="{dw}" stroke-dasharray="{pattern}" stroke-linecap="{"butt" if dw > 10 else "round"}"/>')


def ground(seed, grass, p=3.0, sand=SAND, h=IH):
    """Sea, shallows, sand and grass. Only the coast has an outline. A taller island (h) stretches downward."""
    e = (h - IH) / 2
    return (f'<rect x="0" y="0" width="{IW}" height="{h}" rx="40" fill="{SEA}"/>'
            + waves([(60, 70), (610, 110), (40, 930 + 2 * e), (620, 900 + 2 * e)])
            + f'<path d="{sblob(350, 510 + e, 318, 448 + e, seed, p)}" fill="{SHALLOW}"/>'
            f'<path class="k-o" d="{sblob(350, 500 + e, 300, 430 + e, seed, p)}" fill="{sand}"/>'
            f'<path d="{sblob(350, 488 + e, 262, 392 + e, seed, p)}" fill="{grass}"/>')


def pier(h=IH):
    """The dock at the bottom, with the boat Pip came in."""
    if h != IH:
        return f'<g transform="translate(0 {h - IH})">{pier()}</g>'
    return (f'<rect x="324" y="872" width="52" height="92" rx="4" fill="#d9a066" stroke="#b07a45" stroke-width="3"/>'
            + "".join(f'<path d="M324 {y}H376" stroke="#b07a45" stroke-width="2"/>' for y in (892, 912, 932))
            + at(436, 948, .7, '<path class="k-o" d="M-50 -14H56L42 8H-38Z" fill="#ef5b56"/>', "bob"))


def quiet(inner):
    """Scenery: a little faded, so it stays behind the stops."""
    return f'<g class="quiet">{inner}</g>'


def rounded(points, r=46):
    """A path through `points` with straight lines and rounded corners (for city streets)."""
    d = f"M{points[0][0]} {points[0][1]}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(points, points[1:], points[2:]):
        l1, l2 = math.hypot(x1 - x0, y1 - y0), math.hypot(x2 - x1, y2 - y1)
        k1, k2 = min(r, l1 / 2) / l1, min(r, l2 / 2) / l2
        d += f"L{x1 - (x1 - x0) * k1:.0f} {y1 - (y1 - y0) * k1:.0f}Q{x1} {y1} {x1 + (x2 - x1) * k2:.0f} {y1 + (y2 - y1) * k2:.0f}"
    return d + f"L{points[-1][0]} {points[-1][1]}"


def isle_abc():
    """ABC Island: the road zigzags up a hill to a flag on top."""
    d = ("M350 905C350 850 220 830 220 760C220 690 480 680 480 600C480 520 230 525 230 440"
         "C230 360 470 370 470 290C470 225 350 235 350 175")
    body = ground(1.7, "#d6efbf")
    body += f'<path d="{sblob(350, 215, 200, 130, .6, p=2.4)}" fill="#c6e8ab"/><path d="{sblob(350, 196, 122, 78, .6, p=2.2)}" fill="#b6df9a"/>'
    body += '<path d="M268 178Q300 150 340 146" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".5"/>'
    body += pier()
    body += quiet(
        block(452, 792, .8, "A", "#ef5b56", "#c94c48", still=True) + block(490, 792, .8, "b", "#4a9be8", "#3a79b5", still=True)
        + block(471, 755, .8, "C", "#6cc070", "#4f8127", still=True)
        + crayon(118, 640, .9, "#ffd23f")
        + at(165, 636, .8, f'<rect class="k-o" x="-28" y="-8" width="56" height="13" rx="3" fill="#4a9be8"/>'
                           f'<rect class="k-o" x="-24" y="-21" width="50" height="13" rx="3" fill="#ef5b56"/>')
        + at(585, 430, .75, build14.TREE) + at(620, 480, .6, build14.TREE)
        + at(128, 300, .7, build14.MUSHROOM) + at(172, 318, .6, build14.FLOWERS))
    body += road(d, "sand")
    body += bunting(290, 410, 142, 11) + goal_flag(352, 140, 1.25)
    return body, d, [(220, 760), (480, 600), (355, 520), (230, 440), (470, 290)]


def isle_num():
    """Rainbow Island: a big S over a stream to the rainbow at the top."""
    d = ("M350 905C350 850 210 840 210 770C210 700 480 720 480 650C480 580 380 580 360 530"
         "C340 480 230 480 230 410C230 340 470 360 470 290C470 240 350 250 350 215")
    body = ground(2.1, "#e5f3c4", p=2.6)
    stream = "M92 552C200 512 300 568 400 530S560 504 612 522"
    body += f'<path d="{stream}" fill="none" stroke="#bfe6f7" stroke-width="34" stroke-linecap="round"/>'
    body += f'<path d="M150 540q10 -6 20 0M470 520q10 -6 20 0M560 512q10 -6 20 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    body += pier()
    body += quiet(
        shape_rocks(150, 650, 1.1, still=True)
        + crayon(560, 470, .95, "#ef5b56", -8) + crayon(592, 478, .95, "#4a9be8", 6) + crayon(622, 470, .9, "#ffd23f", 12)
        + block(470, 800, .8, "1", "#ef5b56", "#c94c48", still=True) + block(508, 800, .8, "2", "#4a9be8", "#3a79b5", still=True)
        + block(546, 800, .8, "3", "#6cc070", "#4f8127", still=True)
        + at(128, 300, .6, build14.FLOWERS) + at(590, 300, .7, build14.BUSH))
    body += road(d, "sand")
    # the bridge over the stream: two rails
    body += f'<path d="M330 548L312 520M392 540L410 512" stroke="#b07a45" stroke-width="7" stroke-linecap="round"/>'
    body += rainbow(350, 210, 1.55)
    return body, d, [(210, 770), (480, 650), (360, 530), (230, 410), (470, 290)]


def small_house(x, y, s, smoky=False):
    """build4's house, centered on (x, y) and scaled by s; with `smoky`, smoke from the chimney."""
    x0, y0 = x - 432 * s, y - 224 * s
    return at(x0, y0, s, house()) + (smoke(x0 + 471 * s, y0 + 168 * s) if smoky else "")


def isle_town():
    """My Town: a ring road around the town square, with a fountain in the middle."""
    cx, cy, rx, ry = 350, 470, 215, 290
    ring = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(90, 451, 15)]
    d = "M350 905C350 850 350 800 " + f"{ring[0][0]:.0f} {ring[0][1]:.0f}" + smooth_path(ring, start_cmd=False)
    # nine stops spaced evenly along the ring (by length, not angle: the ring is taller than it is wide)
    around = [(cx + rx * math.cos(math.radians(a / 10)), cy + ry * math.sin(math.radians(a / 10))) for a in range(1300, 4251)]
    run = [0.0]
    for (x0, y0), (x1, y1) in zip(around, around[1:]):
        run.append(run[-1] + math.hypot(x1 - x0, y1 - y0))
    at_len = lambda L: around[min(range(len(run)), key=lambda i: abs(run[i] - L))]
    stops = [tuple(round(v) for v in at_len(run[-1] * k / 8)) for k in range(9)]
    body = ground(3.3, "#d8eecd", p=3.2)
    body += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx - 40}" ry="{ry - 40}" fill="#cbe7bd"/>'
    body += pier()
    body += quiet(
        small_house(cx - 80, cy - 60, .36, smoky=True) + small_house(cx + 60, cy + 120, .32)
        + at(cx - 50, cy - 170, .7, build14.TREE) + at(cx + 90, cy - 140, .6, build14.BUSH)
        + at(120, 170, .7, build14.TREE) + at(600, 820, .7, build14.FLOWERS) + at(110, 820, .6, build14.BUSH)
        + at(600, 150, .6, build14.FLOWERS))
    body += road(d, "sand")
    # the fountain in the square is the goal
    body += at(cx, cy + 10, 1,
        f'<ellipse class="k-o" cx="0" cy="0" rx="62" ry="26" fill="#bfe6f7"/>'
        f'<ellipse cx="0" cy="-3" rx="44" ry="16" fill="#8fd3f4"/>'
        f'<path class="k-o" d="M-10 -4V-40H10V-4Z" fill="#fff"/><ellipse class="k-o" cx="0" cy="-40" rx="22" ry="8" fill="#bfe6f7"/>'
        + "".join(f'<path class="spray" style="animation-delay:-{k * .4}s" d="M0 -44q{dx} -26 {dx * 2} 0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
                  for k, dx in enumerate((-14, 14, -6, 6))))
    body += goal_flag(cx + 70, cy + 4, .9)
    return body, d, stops


NATURE_H = 1290


def isle_nature():
    """Nature Island: a forest trail winding up to a big tree. It is taller than the others, to fit 9 stops."""
    h = NATURE_H
    # the stops sit on the trail's bends, alternating right and left
    bends = [(230, 1107), (470, 1000), (230, 893), (430, 786), (220, 679), (450, 572), (240, 465), (440, 358), (260, 251)]
    d = f"M350 {h - 75}C350 {h - 130} 230 {h - 120} 230 1107"
    for (x0, y0), (x1, y1) in zip(bends, bends[1:]):
        d += f"C{x0} {y0 - 60} {x1} {y1 + 60} {x1} {y1}"
    d += "C260 200 380 190 420 180"
    y = lambda v: round(180 + (v - 180) * (h - 75 - 180) / (905 - 180))  # scenery spread over the taller island
    body = ground(4.2, "#cfeab6", p=2.6, h=h)
    body += f'<ellipse cx="578" cy="{y(486)}" rx="52" ry="34" fill="#a9dcf2"/><path d="M556 {y(486) - 2}q8 -5 16 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    body += pier(h)
    body += quiet(
        at(118, y(600), .42, barn(-94, 94, 0))
        + at(600, y(700), .75, build14.PINE) + at(630, y(740), .6, build14.PINE) + at(615, y(300), .7, build14.PINE)
        + at(115, y(340), .7, build14.TREE) + at(110, y(800), .65, build14.TREE) + at(570, y(830), .7, build14.FLOWERS)
        + at(590, y(380), .6, build14.MUSHROOM) + at(600, y(512), .5, build14.ROCK))
    body += road(d, "trail")
    body += at(470, 172, 1.7, build14.TREE, "sway")
    return body, d, bends, h


def isle_city():
    """City Island: streets with square corners up to the skyline."""
    pts = [(350, 905), (350, 800), (170, 800), (170, 640), (530, 640), (530, 480), (170, 480), (170, 320), (530, 320), (530, 200), (250, 200)]
    d = rounded(pts)
    body = ground(5.5, "#e2ecd4", p=4.0)
    # blocks between the streets: pale buildings, windows unlit
    blocks = ""
    for x, base, w, h, col in ((240, 760, 60, 70, "#f5dcc0"), (380, 760, 60, 60, "#dbe8f5"),
                               (220, 600, 60, 62, "#efd6e6"), (330, 600, 60, 76, "#f5e7c0"),
                               (270, 440, 60, 74, "#dbe8f5"), (400, 440, 60, 60, "#e6f0d5")):
        blocks += building(x, base, w, h, col, win="#eef6ff", lit=False)
    body += quiet(blocks + traffic_light(600, 690, .9) + traffic_light(96, 530, .9)
                  + at(600, 440, .6, build14.TREE) + at(100, 700, .6, build14.TREE) + at(600, 820, .6, build14.BUSH))
    body += pier()
    body += road(d, "street")
    body += city(222, 165, 1.0)
    return body, d, [(170, 800), (350, 640), (530, 640), (350, 480), (170, 480), (530, 320), (366, 200)]


def isle_beach():
    """Beach Island: a boardwalk along the shore to the lighthouse."""
    d = "M350 905C350 820 240 780 250 690C260 600 330 560 350 480C372 392 460 360 500 280"
    body = ground(0.4, "#e3f1c6", p=2.4, sand="#f8e3b4")
    # most of this island is beach: a wide band of sand along the right side
    body += f'<path d="M430 120C560 180 640 360 630 560C620 760 520 880 400 900L380 700C460 560 470 330 430 120Z" fill="#f8e3b4"/>'
    body += pier()
    body += quiet(
        palm(150, 520, .9, still=True) + palm(120, 700, .75, still=True)
        # sandcastle() draws its towers at fixed heights for a base line of 384, so move that base line to y=720
        + at(560, 720 - 384 * .45, .45, sandcastle(0, 384)) + at(520, 810, .55, crab(0, 0)) + at(600, 600, .6, shell(0, 0))
        + at(590, 470, 1, f'<path d="M0 0V-70" stroke="{INK}" stroke-width="4"/><path class="k-o" d="M-48 -64Q0 -104 48 -64Z" fill="#ef5b56"/>'
                          f'<path d="M-16 -84Q0 -64 16 -84" fill="none" stroke="#fff" stroke-width="10"/>')
        + at(150, 300, .6, build14.FLOWERS))
    body += road(d, "boardwalk")
    body += lighthouse(515, 262, 1.5)
    return body, d, [(304, 808), (324, 539), (427, 368)]


ISLES = {"abc": isle_abc, "num": isle_num, "town": isle_town, "nature": isle_nature, "city": isle_city, "beach": isle_beach}


def isle(iid):
    body, d, stops, *rest = ISLES[iid]()
    h = rest[0] if rest else IH
    svg = f'<svg class="isle-art" viewBox="0 0 {IW} {h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>'
    return svg, {"W": IW, "H": h, "stops": stops}


def export():
    """(art, data): the pictures for ART, and WORLD for the map pages."""
    art, data = {}, {"isles": {}}
    for name in LAYOUTS:
        art["_world-" + name], data[name] = world(name)
    for iid in ISLES:
        art["_isle-" + iid], data["isles"][iid] = isle(iid)
    return art, data


if __name__ == "__main__":
    # Preview every island with numbered stop markers: open work/islands_preview.html through the dev server.
    import os
    from common import style
    art, data = export()
    here = os.path.dirname(os.path.abspath(__file__))
    cells = ""
    for iid, info in data["isles"].items():
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="46" fill="#fff" stroke="#3f3345" stroke-width="6" opacity=".9"/>'
                       f'<text x="{x}" y="{y + 12}" text-anchor="middle" font-size="36" font-weight="900">{n + 1}</text>'
                       for n, (x, y) in enumerate(info["stops"]))
        svg = art["_isle-" + iid].replace("</svg>", dots + "</svg>").replace("<svg ", '<svg style="width:340px;height:auto" ', 1)
        cells += f'<div><h3>{iid}</h3>{svg}</div>'
    html = (f'<!doctype html><html><head><link rel="stylesheet" href="../css/style.css"><style>body{{padding:20px}}'
            f'.grid{{display:flex;flex-wrap:wrap;gap:20px}}</style></head><body>{style()}<div class="grid">{cells}</div>'
            f'<div style="max-width:1000px">{art["_world-wide"]}</div></body></html>')
    open(os.path.join(here, "../../work/islands_preview.html"), "w").write(html)
    print("wrote work/islands_preview.html")
