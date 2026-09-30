"""Each place's own map (the page a place on the big map opens, #/island/<id>), and the landmarks the big map
(build27.py) puts at each place. Places were islands once, so the code still calls them that.

Every place is drawn in three layers so the eye goes to the stops first:
  ground (pale, no outlines except the coast) -> road (soft edges) -> stops (full color, drawn by js/views/island.js on top).
Things that move have a class (see "islands" in style.css); they are wrapped in a group of their own,
because a CSS animation replaces an element's transform attribute.

WORLD.isles (exported next to ART) says where each place's stops sit on its road. Change a road here and its stop
positions together. A place in a region of land has that land around it (AROUND); the Cove is by the sea.
"""
import json
import math

from common import INK, fmt, smooth_path
from build4 import union, circ, house
from build15 import barn, hay, fence, tractor, slide, swing_set, seagull, sandcastle, crab, shell
import build14

SEA, SHALLOW, SAND = "#8fd3f4", "#bfe9fb", "#f8e6bf"


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


def waves(pts):
    return "".join(
        f'<path class="wave" style="animation-delay:-{i * 0.7:.1f}s" d="M{x} {y}q7 -6 14 0t14 0" fill="none" '
        f'stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
        for i, (x, y) in enumerate(pts)
    )


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


# ---------------------------------------------------------------- landmarks (for the big map, build27.py)
# (id, rx, ry, seed, grass); names and lessons are in js/content/islands.js (ISLANDS)
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
        return (at(cx - 40, cy + 10, 1.0, build14.TREE, "sway") + at(cx + 50, cy - 6, .85, build14.PINE, "sway", -1.2)
                + at(cx + 20, cy + 50, .6, build14.POND) + at(cx - 86, cy + 36, .6, build14.MUSHROOM)
                + at(cx + 92, cy + 34, .6, build14.FLOWERS, "sway", -.6))
    if iid == "home":
        from build23 import cottage  # build23 draws with this file's shapes, so it's imported here
        return (at(cx - 6, cy + 30, .95, cottage()) + smoke(cx + 14, cy - 64)
                + at(cx - 72, cy + 30, .6, build14.TREE, "sway") + at(cx + 70, cy + 40, .6, build14.FLOWERS, "sway", -1))
    if iid == "school":
        return school_house(cx, cy + 26, .72) + at(cx + 84, cy + 36, .55, build14.TREE, "sway") + at(cx - 86, cy + 38, .55, build14.FLOWERS, "sway")
    if iid == "farm":
        return (at(cx - 30, cy + 26, .5, barn(-94, 94, 0)) + at(cx + 70, cy + 30, .42, hay(0, 0, 30))
                + at(cx + 60, cy + 58, .5, fence(-60, 60, -40)) + at(cx - 86, cy + 40, .55, build14.BUSH))
    if iid == "city":
        return city(cx, cy + 20, 0.95)
    return palm(cx - 30, cy + 20, 0.9) + lighthouse(cx + 50, cy + 20, 0.75)


def school_house(x, y, s):
    """A little school standing on (x, y): red roof, a clock in the gable, a bell tower and a flag."""
    wins = "".join(f'<rect class="k-o" x="{wx}" y="-46" width="18" height="18" rx="3" fill="#cdeeff" stroke-width="2.5"/>' for wx in (-62, -38, 20, 44))
    return at(x, y, s,
        f'<rect class="k-o" x="-72" y="-60" width="144" height="60" rx="4" fill="#f3d9a6"/>' + wins
        + f'<path class="k-o" d="M-80 -58L0 -100L80 -58Z" fill="#ef5b56"/>'
        + f'<circle class="k-o" cx="0" cy="-74" r="12" fill="#fff" stroke-width="2.5"/><path d="M0 -74V-82M0 -74L6 -71" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<rect class="k-o" x="-12" y="-122" width="24" height="24" fill="#f3d9a6" stroke-width="2.5"/><path class="k-o" d="M-16 -122L0 -136L16 -122Z" fill="#ef5b56" stroke-width="2.5"/>'
        + f'<circle cx="0" cy="-110" r="5" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<path class="k-o" d="M-14 0V-34A14 14 0 0 1 14 -34V0Z" fill="#4a9be8"/>'
        + f'<path d="M0 -136V-160" stroke="{INK}" stroke-width="3"/><path class="k-o cloth" d="M0 -160L22 -154L0 -148Z" fill="#ffd23f" stroke-width="2"/>')


# ---------------------------------------------------------------- inside the islands
# Each island is a 700 x 980 picture (Nature Island is taller, see NATURE_H): sea, the island, a road from the dock at the bottom to a goal at the top,
# and the stops along the road (in order). ROAD_STYLES: edge, fill, dash color, dash pattern, dash width.
IW, IH = 700, 980
ROAD_STYLES = {
    "sand": ("#dcb67c", "#f8e7c0", "#fff", "2 18", 5),
    "trail": ("#c7a169", "#eed8ab", "#fffaf0", "2 22", 5),
    "street": ("#b9b2c6", "#e7e3ee", "#fff", "18 16", 4),
    "boardwalk": ("#b98a55", "#e8c592", "#c99a66", "3 11", 34),
    "snow": ("#9fb3c8", "#dde7f1", "#fff", "2 18", 5),
}


def road(d, kind):
    edge, fill, dash, pattern, dw = ROAD_STYLES[kind]
    return (f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path class="road-line" d="{d}" fill="none" stroke="{dash}" stroke-width="{dw}" stroke-dasharray="{pattern}" stroke-linecap="{"butt" if dw > 10 else "round"}"/>')


# The ground around each place, by the region it's in on the big map: (around, edge). None is the sea.
MEADOW, FOREST, SNOW = ("#b9dd98", "#cbe7ae"), ("#82c06b", "#9ccf84"), ("#d3e2ee", "#e8f0f6")
AROUND = {"abc": MEADOW, "school": MEADOW, "num": MEADOW, "town": MEADOW, "home": MEADOW, "farm": MEADOW, "city": MEADOW,
          "mushroom": FOREST, "treehouse": FOREST, "nature": FOREST, "station": SNOW, "beach": None}
_around = None  # the ground of the place being drawn; isle() sets it


def ground(seed, grass, p=3.0, sand=SAND, h=IH):
    """The place's ground: its region's land around it (or the sea, with shallows), a rim, and grass in the middle.
    Only the edge has an outline. A taller place (h) stretches downward."""
    e = (h - IH) / 2
    if _around:
        around, edge = _around
        return (f'<rect x="0" y="0" width="{IW}" height="{h}" rx="40" fill="{around}"/>'
                + "".join(f'<path d="M{x} {y}l4 -10l4 10M{x + 10} {y}l3 -8l3 8" fill="none" stroke="{edge}" stroke-width="3" stroke-linecap="round"/>'
                          for x, y in ((50, 80), (620, 120), (40, 940 + 2 * e), (630, 910 + 2 * e), (60, 500 + e), (640, 520 + e)))
                + f'<path class="k-o" d="{sblob(350, 500 + e, 300, 430 + e, seed, p)}" fill="{edge}" stroke-opacity=".35"/>'
                f'<path d="{sblob(350, 488 + e, 262, 392 + e, seed, p)}" fill="{grass}"/>')
    return (f'<rect x="0" y="0" width="{IW}" height="{h}" rx="40" fill="{SEA}"/>'
            + waves([(60, 70), (610, 110), (40, 930 + 2 * e), (620, 900 + 2 * e)])
            + f'<path d="{sblob(350, 510 + e, 318, 448 + e, seed, p)}" fill="{SHALLOW}"/>'
            f'<path class="k-o" d="{sblob(350, 500 + e, 300, 430 + e, seed, p)}" fill="{sand}"/>'
            f'<path d="{sblob(350, 488 + e, 262, 392 + e, seed, p)}" fill="{grass}"/>')


def pier(h=IH):
    """Where Pip comes in, at the bottom: a gate on land, or the dock with the boat by the sea."""
    if h != IH:
        return f'<g transform="translate(0 {h - IH})">{pier()}</g>'
    if _around:
        return (f'<path d="M318 960V900M382 960V900" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M318 960V900M382 960V900" stroke="#c98a4b" stroke-width="5" stroke-linecap="round"/>'
                f'<rect class="k-o" x="306" y="884" width="88" height="24" rx="6" fill="#ffd23f" stroke-width="2.5"/>'
                f'<path d="M322 896H378" stroke="#e8b520" stroke-width="3" stroke-linecap="round"/>')
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
    return body, d, [(220, 760), (355, 520), (470, 290)]


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
    # the stops spaced evenly along the ring (by length, not angle: the ring is taller than it is wide)
    around = [(cx + rx * math.cos(math.radians(a / 10)), cy + ry * math.sin(math.radians(a / 10))) for a in range(1300, 4251)]
    run = [0.0]
    for (x0, y0), (x1, y1) in zip(around, around[1:]):
        run.append(run[-1] + math.hypot(x1 - x0, y1 - y0))
    at_len = lambda L: around[min(range(len(run)), key=lambda i: abs(run[i] - L))]
    n = 5
    stops = [tuple(round(v) for v in at_len(run[-1] * (k + .5) / n)) for k in range(n)]
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


NATURE_H = IH


def isle_nature():
    """Nature Island: a forest trail winding up to a big tree."""
    h = NATURE_H
    # the stops sit on the trail's bends, alternating right and left
    bends = [(230, 780), (470, 640), (230, 510), (450, 380), (260, 262)]
    d = f"M350 {h - 75}C350 {h - 130} 230 {h - 120} {bends[0][0]} {bends[0][1]}"
    for (x0, y0), (x1, y1) in zip(bends, bends[1:]):
        d += f"C{x0} {y0 - 60} {x1} {y1 + 60} {x1} {y1}"
    d += "C260 200 380 190 420 180"
    y = lambda v: round(180 + (v - 180) * (h - 75 - 180) / (905 - 180))  # scenery spread over the taller island
    body = ground(4.2, "#cfeab6", p=2.6, h=h)
    body += f'<ellipse cx="578" cy="{y(486)}" rx="52" ry="34" fill="#a9dcf2"/><path d="M556 {y(486) - 2}q8 -5 16 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    body += pier(h)
    body += quiet(
        at(112, y(600), .7, build14.PINE) + at(600, y(700), .75, build14.PINE) + at(630, y(740), .6, build14.PINE) + at(615, y(300), .7, build14.PINE)
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
    return body, d, [(170, 800), (350, 640), (530, 640), (170, 480), (530, 320), (366, 200)]


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
    return body, d, [(304, 808), (262, 660), (324, 539), (427, 368)]


def isle_home():
    """Home Island: a garden path up to a cottage like Pip's, past a vegetable patch and a washing line."""
    from build23 import cottage, mailbox
    d = ("M350 905C350 850 220 840 220 770C220 700 470 710 470 640C470 570 240 580 240 510"
         "C240 440 460 450 460 380C460 320 260 340 260 290C260 240 330 235 350 222")
    body = ground(6.3, "#dcefcb", p=2.8)
    body += f'<path d="{sblob(350, 200, 170, 100, .9, p=2.4)}" fill="#cde8b4"/>'
    body += pier()
    # a vegetable patch, a washing line, trees and flowers
    patch = "".join(f'<path d="M{x} 842q6 -14 12 0" fill="#6cc070" stroke="{INK}" stroke-width="1.5"/>' for x in range(470, 580, 18))
    line = (f'<path d="M110 560V480M240 560V480" stroke="#b07a45" stroke-width="5" stroke-linecap="round"/><path d="M110 488Q175 504 240 488" fill="none" stroke="{INK}" stroke-width="1.5"/>'
            + "".join(f'<rect x="{x}" y="494" width="18" height="22" rx="3" fill="{c}" stroke="{INK}" stroke-width="1.5"/>' for x, c in ((130, "#ef5b56"), (160, "#4a9be8"), (190, "#ffd23f"))))
    body += quiet(
        f'<rect x="460" y="826" width="130" height="30" rx="8" fill="#b98a55"/>' + patch + line
        + at(590, 520, .7, build14.TREE) + at(120, 330, .7, build14.TREE) + at(600, 300, .6, build14.FLOWERS)
        + at(110, 760, .6, build14.BUSH) + at(590, 700, .6, build14.FLOWERS))
    body += road(d, "sand")
    body += at(350, 222, 1.7, cottage()) + smoke(378, 58) + at(430, 226, 1.2, mailbox())
    return body, d, [(220, 770), (470, 640), (355, 575), (240, 510), (460, 380), (260, 292)]


def isle_school():
    """School Island: through the playground to the school, past a slide, a swing and a football goal."""
    d = ("M350 905C350 850 220 840 220 770C220 700 470 700 470 630C470 560 240 570 240 500"
         "C240 430 460 440 460 370C460 320 330 330 330 290")
    body = ground(8.2, "#dcefcb", p=2.9)
    body += f'<rect x="120" y="150" width="460" height="120" rx="30" fill="#e8dcc0"/>'
    body += pier()
    goal = (f'<path d="M0 0V-40H70V0" fill="none" stroke="#fff" stroke-width="7"/><path d="M0 0V-40H70V0" fill="none" stroke="{INK}" stroke-width="2"/>'
            + "".join(f'<path d="M{x} -40V0" stroke="#fff" stroke-width="1.5" opacity=".8"/>' for x in range(10, 70, 10)))
    body += quiet(
        at(110, 700, .6, slide(-60, 0)) + at(560, 560, .55, swing_set(-60, 60, -80, 0))
        + at(520, 830, 1, goal) + at(600, 420, .6, build14.TREE) + at(110, 430, .6, build14.TREE)
        + at(120, 840, .6, build14.FLOWERS) + at(580, 700, .6, build14.BUSH))
    body += road(d, "sand")
    body += school_house(350, 262, 1.5)
    return body, d, [(220, 770), (470, 630), (240, 500), (460, 370), (330, 290)]


def mushroom_house(x, y, s, cap="#ef5b56"):
    """A little house with a mushroom for a roof, standing on (x, y)."""
    return at(x, y, s,
        f'<rect class="k-o" x="-18" y="-30" width="36" height="30" rx="8" fill="#fff3dc"/>'
        f'<path class="k-o" d="M-8 0V-14A8 8 0 0 1 8 -14V0Z" fill="#c98a4b" stroke-width="2.5"/>'
        f'<path class="k-o" d="M-40 -26C-40 -60 40 -60 40 -26Z" fill="{cap}"/>'
        + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>' for cx, cy, r in ((-20, -40, 6), (4, -48, 5), (22, -36, 6))))


def tree_house(x, y, s):
    """A red-roofed house up in a big round tree, with a ladder, standing on (x, y)."""
    return at(x, y, s,
        f'<rect class="k-o" x="-10" y="-40" width="20" height="40" fill="#94592f"/>'
        f'<circle class="k-o" cx="0" cy="-86" r="46" fill="#5aa84a"/><circle cx="-22" cy="-96" r="14" fill="#6fbf5c"/>'
        f'<rect class="k-o" x="-30" y="-78" width="60" height="36" rx="3" fill="#c98a4b"/>'
        f'<path class="k-o" d="M-36 -76L0 -100L36 -76Z" fill="#ef5b56"/>'
        f'<rect class="k-o" x="-8" y="-68" width="16" height="16" rx="2" fill="#ffe89a" stroke-width="2"/>'
        + "".join(f'<path d="M22 {yy}H34" stroke="#94592f" stroke-width="3"/>' for yy in (-36, -26, -16, -6))
        + '<path d="M22 -42V0M34 -42V0" stroke="#94592f" stroke-width="3"/>')


def mountain(x, y, w, h, snow=True):
    """A mountain standing on y, with a snowy top."""
    cap = (f'<path d="M{x - w * .18:.0f} {y - h * .66:.0f}L{x} {y - h}L{x + w * .18:.0f} {y - h * .66:.0f}L{x + w * .08:.0f} {y - h * .6:.0f}'
           f'L{x} {y - h * .68:.0f}L{x - w * .08:.0f} {y - h * .58:.0f}Z" fill="#fff"/>') if snow else ""
    return f'<path class="k-o" d="M{x - w / 2} {y}L{x} {y - h}L{x + w / 2} {y}Z" fill="#b9c8dc"/>' + cap


def snow_pine(x, y, s):
    return at(x, y, s, build14.PINE + '<path d="M-10 -34L0 -46L10 -34Z M-14 -14L0 -26L14 -14Z" fill="#fff" opacity=".9"/>')


def snowman(x, y, s):
    return at(x, y, s,
        f'<circle class="k-o" cx="0" cy="-16" r="18" fill="#fff"/><circle class="k-o" cx="0" cy="-46" r="13" fill="#fff"/>'
        f'<circle cx="-4" cy="-49" r="2" fill="{INK}"/><circle cx="4" cy="-49" r="2" fill="{INK}"/><path d="M0 -45L10 -43L0 -41Z" fill="#ff9a3c"/>'
        f'<path class="k-o" d="M-12 -58H12L8 -70H-8Z" fill="{INK}" stroke-width="2"/><path d="M-12 -36H12" stroke="#ef5b56" stroke-width="5"/>')


def weather_station(x, y, s):
    """A little white hut with a blue roof, a weather vane and a sun on the door, standing on (x, y)."""
    return at(x, y, s,
        f'<rect class="k-o" x="-34" y="-44" width="68" height="44" rx="4" fill="#fff"/><path class="k-o" d="M-40 -42L0 -66L40 -42Z" fill="#4a9be8"/>'
        f'<path d="M0 -66V-100" stroke="{INK}" stroke-width="3"/>'
        f'<g class="needle"><path class="k-o" d="M0 -100L22 -94L0 -88Z" fill="#ef5b56" stroke-width="2"/></g>'
        f'<circle class="k-o" cx="0" cy="-24" r="10" fill="#ffd23f" stroke-width="2.5"/>')


def isle_mushroom():
    """Mushroom Village: a forest path between mushroom houses, up to the biggest one."""
    d = ("M350 905C350 850 230 830 230 760C230 690 470 670 470 600C470 520 240 520 240 440"
         "C240 370 460 380 460 300C460 250 360 250 350 240")
    body = ground(9.1, "#a6d58c", p=2.8)
    body += pier()
    body += quiet(
        mushroom_house(560, 820, .9, "#8150c4") + mushroom_house(120, 640, .8, "#ffb13b") + mushroom_house(590, 470, .8)
        + mushroom_house(130, 330, .7, "#4a9be8") + at(600, 660, .7, build14.PINE) + at(110, 820, .7, build14.PINE)
        + at(600, 300, .6, build14.MUSHROOM) + at(150, 480, .6, build14.FLOWERS))
    body += road(d, "trail")
    body += mushroom_house(350, 230, 2.0) + goal_flag(440, 222, .9)
    return body, d, [(230, 760), (470, 600), (240, 440), (460, 300)]


def isle_treehouse():
    """Tree House: a trail through tall trees to a house up in the biggest one."""
    d = ("M350 905C350 850 470 830 470 760C470 690 230 680 230 610C230 540 460 540 460 470"
         "C460 400 250 400 250 340C250 300 330 300 350 290")
    body = ground(3.7, "#9ed085", p=2.6)
    body += pier()
    body += quiet(
        at(120, 820, .8, build14.TREE) + at(590, 640, .8, build14.PINE) + at(110, 520, .8, build14.PINE)
        + at(600, 400, .7, build14.TREE) + at(130, 300, .7, build14.TREE) + at(580, 820, .6, build14.MUSHROOM)
        + at(140, 700, .6, build14.FLOWERS))
    body += road(d, "trail")
    body += tree_house(350, 300, 1.6)
    return body, d, [(470, 760), (230, 610), (460, 470), (250, 340)]


def isle_station():
    """Weather Station: a snowy path up the mountain to the weather hut, past pines and a snowman."""
    d = ("M350 905C350 850 230 830 230 760C230 690 470 680 470 610C470 540 240 540 240 470"
         "C240 400 450 400 450 330C450 290 370 290 350 280")
    body = ground(5.9, "#f4f8fb", p=2.8)
    body += mountain(200, 250, 300, 170) + mountain(520, 260, 340, 200)
    body += pier()
    body += quiet(
        snow_pine(120, 820, .8) + snow_pine(590, 700, .8) + snow_pine(110, 560, .7) + snow_pine(600, 460, .7)
        + snowman(570, 850, .9) + at(130, 380, .6, build14.ROCK))
    body += road(d, "snow")
    body += weather_station(350, 280, 1.6) + snowman(450, 290, .8)
    return body, d, [(230, 760), (470, 610), (240, 470), (450, 330)]


def isle_farm():
    """Farm Island: a farm track between the fields, up to the barn."""
    d = ("M350 905C350 840 230 830 230 760C230 690 470 670 470 600C470 520 240 520 240 440"
         "C240 370 460 380 460 300C460 250 360 250 350 230")
    body = ground(7.1, "#e6f0bf", p=3.0)
    # fields in stripes, a pond with a duck, hay, a fence and a tractor
    rows = "".join(f'<path d="M80 {y}Q160 {y - 8} 240 {y}" fill="none" stroke="#b9d77a" stroke-width="10" stroke-linecap="round"/>' for y in range(610, 700, 22))
    rows += "".join(f'<path d="M470 {y}Q540 {y - 8} 610 {y}" fill="none" stroke="#e8c96a" stroke-width="10" stroke-linecap="round"/>' for y in range(420, 510, 22))
    body += pier()
    body += quiet(
        rows
        + f'<ellipse cx="560" cy="780" rx="60" ry="32" fill="#a9dcf2"/>'
        + at(120, 440, .5, hay(0, 0, 30)) + at(160, 452, .4, hay(0, 0, 30))
        + at(110, 300, .5, fence(-60, 60, 0)) + at(580, 300, .6, build14.TREE)
        + at(130, 820, .45, tractor(0, 0)) + at(600, 640, .6, build14.BUSH))
    body += road(d, "trail")
    body += at(350, 210, .9, barn(-94, 94, 0)) + goal_flag(452, 214, .9)
    return body, d, [(230, 760), (470, 600), (240, 440), (460, 300)]


ISLES = {"abc": isle_abc, "school": isle_school, "num": isle_num, "town": isle_town, "home": isle_home, "farm": isle_farm,
         "city": isle_city, "mushroom": isle_mushroom, "treehouse": isle_treehouse, "nature": isle_nature,
         "station": isle_station, "beach": isle_beach}


def isle(iid):
    global _around
    _around = AROUND.get(iid)
    body, d, stops, *rest = ISLES[iid]()
    _around = None
    h = rest[0] if rest else IH
    svg = f'<svg class="isle-art" viewBox="0 0 {IW} {h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>'
    return svg, {"W": IW, "H": h, "stops": stops}


def export():
    """(art, data): the pictures for ART, and WORLD for the map pages."""
    art, data = {}, {"isles": {}}
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
            f'</body></html>')
    open(os.path.join(here, "../../work/islands_preview.html"), "w").write(html)
    print("wrote work/islands_preview.html")
