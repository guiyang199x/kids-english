"""The big map on the home page: one tall map, read from top to bottom, in three regions by level (Sunny Meadow,
the Forest, Snowy Mountains & the Cove). A road winds through them past every place; js/views/world.js walks Pip
along it (the path with class "bigroad") and opens a place when he gets there.

PLACES must list the places in the same order as js/content/islands.js (tests/islands.test.js checks).
WORLD.bigmap tells world.js where things are: each place's landmark, its name plate and the region signs, in the
map's units and in % of it, and where the Ghost Ship floats in its season.

Run `python3 build27.py` to preview it in work/bigmap_preview.html.
"""
import math

from common import INK, smooth_path
import build14
from build16 import at, blob, landmark, mountain, snow_pine, snowman, weather_station, mushroom_house, tree_house
from build24 import ghost_ship

W, H = 800, 3000
# the regions, top to bottom: (id, top, bottom, ground, patches); names and levels are in js/content/islands.js
REGIONS = [
    ("meadow", 170, 1450, "#d4efb4", "#c3e6a0"),
    ("forest", 1450, 2220, "#a9d98e", "#93cc78"),
    ("snow", 2220, H, "#eef5fa", "#dde9f2"),
]
# the places: (id, x, y) where its landmark stands, in the order the road passes them
PLACES = [
    ("abc", 230, 330), ("school", 570, 490), ("num", 230, 660), ("town", 570, 830), ("home", 230, 1000),
    ("farm", 570, 1170), ("city", 230, 1340),
    ("mushroom", 570, 1620), ("treehouse", 230, 1820), ("nature", 570, 2020),
    ("station", 230, 2400), ("beach", 570, 2640),
]
START = (400, 180)  # where the road begins, under the title
VISIT = (380, 2860, .75)  # the Ghost Ship, out on the water of the cove


def ground(k, top, bottom, col, dark):
    """A region's ground, with a wavy top edge where it meets the one above."""
    edge = smooth_path([(W * i / 8, top + (14 * math.sin(i * 1.3 + k) if k else 0)) for i in range(9)])
    patches = "".join(f'<path d="{blob(x, y, rx, ry, k + x / 100, n=10, wob=.15)}" fill="{dark}"/>'
                      for x, y, rx, ry in ((110, top + 190, 90, 40), (660, top + 360, 110, 44), (150, top + 560, 80, 36),
                                           (680, top + 700, 90, 40), (120, top + 980, 90, 40)) if y < bottom - 60)
    return f'<path d="{edge}L{W} {bottom}H0Z" fill="{col}"/>' + patches


def cove():
    """The sea at the bottom of the map, with a sandy shore, waves and a lighthouse."""
    shore = "M-10 2760C140 2700 320 2740 460 2720S700 2690 810 2730V3010H-10Z"
    return (f'<path d="{shore}" fill="#f6dca5"/>'
            f'<path d="M-10 2800C150 2750 330 2790 470 2770S700 2740 810 2780V3010H-10Z" fill="#8fd3f4"/>'
            + "".join(f'<path class="wave" style="animation-delay:-{k * .6}s" d="M{x} {y}q7 -6 14 0t14 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                      for k, (x, y) in enumerate(((80, 2860), (230, 2920), (560, 2850), (690, 2930), (420, 2960), (130, 2960))))
            + at(700, 2760, .8, '<path class="k-o" d="M-16 0L-11 -70H11L16 0Z" fill="#fff"/><path d="M-14 -20H14M-12.5 -44H12.5" stroke="#ef5b56" stroke-width="10"/>'
                                '<path d="M-16 0L-11 -70H11L16 0Z" fill="none" stroke="#3f3345" stroke-width="3" stroke-linejoin="round"/>'
                                '<rect class="k-o" x="-12" y="-86" width="24" height="16" rx="3" fill="#ffd23f"/><path class="k-o" d="M-15 -86L0 -100L15 -86Z" fill="#ef5b56"/>'))


def scenery():
    out = ""
    # the meadow: a stream across, flowers, bushes and a few trees
    out += '<path d="M0 580C200 540 300 620 420 580S640 520 800 560" fill="none" stroke="#bfe6f7" stroke-width="30" stroke-linecap="round"/>'
    out += '<path d="M0 1100C180 1070 320 1130 460 1100S660 1060 800 1090" fill="none" stroke="#bfe6f7" stroke-width="26" stroke-linecap="round"/>'
    for k, (x, y) in enumerate(((80, 440), (720, 660), (90, 840), (700, 1010), (400, 1260), (730, 1400), (400, 400), (400, 910), (740, 300))):
        out += at(x, y, .7, build14.FLOWERS if k % 3 else build14.BUSH)
    for x, y in ((60, 1200), (740, 360), (60, 720), (740, 960)):
        out += at(x, y, .7, build14.TREE)
    # the forest: trees everywhere, and mushrooms
    for k, (x, y) in enumerate(((60, 1520), (140, 1580), (720, 1500), (760, 1760), (60, 1700), (380, 1540), (400, 1740),
                                (60, 1940), (720, 1920), (380, 1940), (120, 2120), (720, 2160), (400, 2160), (260, 2190))):
        out += at(x, y, .8 + (k % 3) * .1, build14.PINE if k % 2 else build14.TREE)
    for x, y in ((300, 1660), (480, 1880), (180, 2040)):
        out += at(x, y, .6, build14.MUSHROOM)
    # the mountains, snowy pines, a snowman, and the cove
    out += mountain(170, 2340, 300, 160) + mountain(640, 2360, 360, 190) + mountain(420, 2320, 240, 120)
    for x, y in ((60, 2520), (740, 2460), (400, 2540), (730, 2580), (70, 2700)):
        out += snow_pine(x, y, .8)
    out += snowman(420, 2450, .8)
    out += cove()
    return out


def place_art(iid, x, y):
    if iid in ("abc", "school", "num", "town", "home", "farm", "city"):
        return landmark(iid, x, y - 20)
    if iid == "mushroom":
        return mushroom_house(x - 40, y + 10, 1.1) + mushroom_house(x + 40, y, .9, "#8150c4") + mushroom_house(x, y + 30, .7, "#ffb13b")
    if iid == "treehouse":
        return tree_house(x, y + 30, 1.1)
    if iid == "nature":
        return (at(x - 50, y + 10, .9, build14.POND) + at(x + 50, y, .9, build14.FLOWERS) + at(x, y - 10, 1, build14.TREE, "sway")
                + at(x + 70, y + 30, .7, build14.MUSHROOM))
    if iid == "station":
        return weather_station(x, y + 30, 1.1) + snowman(x + 70, y + 36, .9)
    if iid == "beach":
        return landmark("beach", x, y - 10)
    return ""


def beside(x, y):
    """Where the road passes a place: beside its landmark, on the side of the middle of the map."""
    return (x + 110 if x < W / 2 else x - 110, y + 46)


def road_path():
    return smooth_path([START] + [beside(x, y) for _i, x, y in PLACES] + [(400, 2740)])


def bigmap():
    d = road_path()
    body = f'<rect width="{W}" height="{H}" fill="#bfe6ff"/>'
    body += "".join(ground(k, top, bottom, col, dark) for k, (_r, top, bottom, col, dark) in enumerate(REGIONS))
    body += scenery()
    body += (f'<path d="{d}" fill="none" stroke="#dcb67c" stroke-width="46" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="{d}" fill="none" stroke="#f8e7c0" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path class="route bigroad" d="{d}" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="2 18" stroke-linecap="round"/>')
    for k, (iid, x, y) in enumerate(PLACES):
        body += f'<g class="place-g" data-i="{k}">{place_art(iid, x, y)}</g>'
    vx, vy, vs = VISIT
    body += f'<g class="visit-g" data-visit="halloween">{at(vx, vy, vs, ghost_ship())}</g>'
    # Pip, who walks along the road (world.js moves the outer group; the inner one bobs)
    body += f'<g class="bigpip"><g class="bigpip-flip"><g class="pip-bob">{at(0, -58, .62, build14.pip("wave", extra=build14.WAVE_LINES))}</g></g></g>'
    svg = f'<svg class="bigmap-art" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{body}</svg>'
    pct = lambda v, of: round(v / of * 100, 2)
    data = {
        "W": W, "H": H,
        "places": [(x, y) for _i, x, y in PLACES],
        "ids": [i for i, _x, _y in PLACES],
        "labels": [(pct(x, W), pct(y + 62, H)) for _i, x, y in PLACES],
        # each region's sign, on the other side from its first place
        # (the first region's goes in the sky above the map, in the middle)
        "signs": [(50, pct(28, H)) if k == 0 else (pct(W - first_x(top), W), pct(top + 110, H))
                  for k, (_r, top, _b, _c, _d) in enumerate(REGIONS)],
        "regions": [r for r, *_ in REGIONS],
        "visit": {"pos": (vx, vy - 60), "at": len(PLACES) - 1},
    }
    return svg, data


def first_x(top):
    """The x of the first place below `top` (a region's first place)."""
    return next(x for _i, x, y in PLACES if y > top)


def export():
    svg, data = bigmap()
    return {"_bigmap": svg}, data


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    svg, data = bigmap()
    plates = "".join(f'<div class="plate" style="left:{x}%;top:{y}%">{i}</div>' for i, (x, y) in zip(data["ids"], data["labels"]))
    html = ("<!doctype html><meta charset=utf-8><title>Big map preview</title><link rel=stylesheet href=../css/style.css>"
            "<style>body{padding:20px}.big{position:relative;max-width:760px;margin:0 auto}.big svg{width:100%;display:block}"
            ".plate{position:absolute;transform:translateX(-50%);background:#fff;border:2px solid #3f3345;border-radius:10px;padding:0 8px;font-weight:800}</style>"
            f'<div class=big>{svg}{plates}</div>')
    open(os.path.join(here, "../../work/bigmap_preview.html"), "w").write(html)
    print("wrote work/bigmap_preview.html")
