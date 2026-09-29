"""Pip says: the pictures for the "do it" games.

ROOM  - a room with a table and an open box, where the child drags the cat ("Put the cat under the table.").
        Each <rect class="do-zone"> is where a drop counts as that place (data-zone), and data-slot names the
        <g class="do-slot"> that says where the cat then sits (data-x, data-y, data-s) and how deep in the
        picture it is drawn (behind the box is drawn before the box, and so on).
PIP_BODY - Pip, big, with his parts in groups (see build14.pip(parts=True)) and a <circle class="do-spot"> on
        each part the child can touch ("Touch Pip's nose.").

Run `python3 build17.py` to write work/do_preview.html with every zone outlined and the cat in each slot.
"""
from common import INK
from build1 import CAT
from build11 import open_box_front
from build14 import pip, PIP_VB

W, H = 680, 420
WOOD, WOOD_DARK = "#b5774a", "#94592f"
CAT_HOME = (72, 346, 0.6)

# where the cat sits: slot -> (x, y, scale), the middle of the cat
SLOTS = {
    "home": CAT_HOME,
    "on": (215, 176, 0.62),
    "under": (215, 298, 0.62),
    "in": (495, 222, 0.62),
    "behind": (530, 221, 0.52),
    "next-left": (386, 300, 0.62),
    "next-right": (630, 300, 0.62),
    "front": (495, 362, 0.7),
}
# drop areas: (zone, slot, x, y, w, h). A drop is tested against them in this order.
ZONES = [
    ("on-table", "on", 95, 80, 240, 142),
    ("under-table", "under", 105, 236, 220, 112),
    ("in-box", "in", 425, 226, 158, 116),
    ("behind-box", "behind", 425, 110, 158, 116),
    ("next-to-box", "next-left", 335, 214, 90, 136),
    ("next-to-box", "next-right", 583, 196, 97, 160),
    ("in-front-of-box", "front", 400, 342, 200, 78),
]


def _slot(name):
    x, y, s = SLOTS[name]
    return f'<g class="do-slot" data-slot="{name}" data-x="{x}" data-y="{y}" data-s="{s}"></g>'


def _room_back():
    planks = "".join(f'<path d="M0 {y}H{W}" stroke="#d9b07a" stroke-width="2"/>' for y in (250, 310, 375))
    return (
        f'<rect width="{W}" height="200" fill="#fdf1dc"/>'
        f'<rect y="200" width="{W}" height="{H - 200}" fill="#f0cfa0"/>'
        + planks
        + f'<rect y="192" width="{W}" height="12" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        # window
        + f'<rect class="k-o" x="40" y="28" width="118" height="92" rx="8" fill="#bfe6fb"/>'
        + f'<path d="M99 28V120M40 74H158" stroke="{INK}" stroke-width="3"/>'
        + '<path d="M52 44Q58 38 66 40" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
        # clock
        + f'<circle class="k-o" cx="610" cy="66" r="30" fill="#fff"/>'
        + f'<path d="M610 66V46M610 66L624 74" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        + f'<circle cx="610" cy="66" r="3.5" fill="{INK}"/>'
        # the cat's bed
        + f'<ellipse cx="72" cy="392" rx="62" ry="20" fill="{INK}" opacity=".12"/>'
        + f'<ellipse class="k-o" cx="72" cy="382" rx="60" ry="22" fill="#8fd0f5"/>'
        + '<ellipse cx="72" cy="378" rx="42" ry="12" fill="#c3e8fb"/>'
    )


def _table():
    legs = lambda xs, y, h, w: "".join(
        f'<rect class="k-o" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{WOOD_DARK}"/>' for x in xs
    )
    return (
        f'<ellipse cx="215" cy="342" rx="118" ry="8" fill="{INK}" opacity=".12"/>'
        + legs((140, 278), 230, 84, 12)
        + legs((110, 304), 236, 106, 16)
        + f'<path class="k-o" d="M105 222L132 198H298L325 222Z" fill="{WOOD}"/>'
        + f'<rect class="k-o" x="100" y="220" width="230" height="18" rx="4" fill="{WOOD_DARK}"/>'
    )


def _box_inside():
    """The dark inside of the open box and its back edge (drawn before the cat when it is in the box)."""
    return (
        f'<ellipse cx="505" cy="340" rx="84" ry="7" fill="{INK}" opacity=".12"/>'
        f'<g transform="translate(495 250) scale(1.55)">'
        f'<path class="k-o" d="M-42 0L-30 -12H54L42 0Z" fill="#8a5a2e" stroke-width="2"/></g>'
    )


def _box_front():
    return f'<g transform="translate(495 250) scale(1.55)"><g style="stroke-width:2">{open_box_front(0, 0)}</g></g>'


def _zones(show=False):
    style = 'fill="none"' if not show else 'fill="rgba(255,210,63,.18)" stroke="#e08a00" stroke-width="2" stroke-dasharray="6 5"'
    out = ""
    for zone, slot, x, y, w, h in ZONES:
        out += f'<rect class="do-zone" data-zone="{zone}" data-slot="{slot}" x="{x}" y="{y}" width="{w}" height="{h}" rx="18" {style}/>'
    return out


def cat_g(slot="home"):
    x, y, s = SLOTS[slot]
    return f'<g class="do-thing" transform="translate({x} {y}) scale({s})">{CAT}</g>'


def room(show_zones=False, cat_at="home"):
    """The room in drawing order. The cat starts in its bed; js/games/pipsays.js moves it between the slots."""
    order = [
        _room_back(),
        _slot("behind"),
        _box_inside(),
        _slot("in"),
        _box_front(),
        _table(),
        _slot("under"),
        _slot("on"),
        _slot("next-left"),
        _slot("next-right"),
        _slot("front"),
        _slot("home"),
    ]
    out = "".join(order)
    # put the cat into its slot
    marker = f'data-slot="{cat_at}"'
    i = out.index(marker)
    j = out.index("></g>", i) + 1
    out = out[:j] + cat_g(cat_at) + out[j:]
    return out + _zones(show_zones) + '<g class="do-drag"></g>'


ROOM_VB = f"0 0 {W} {H}"

# Pip's parts the child can touch: (zone, x, y, r). Eyes, ears, hands and feet come in twos.
SPOTS = [
    ("eye", -17, -28, 13), ("eye", 17, -28, 13),
    ("ear", -35, -60, 14), ("ear", 35, -60, 14),
    ("nose", 0, -13, 7), ("mouth", 0, -2, 8),
    ("hand", -37, 38, 14), ("hand", 37, 38, 14),
    ("foot", -20, 74, 13), ("foot", 20, 74, 13),
]


def pip_body(show=False):
    style = 'fill="transparent"' if not show else 'fill="rgba(255,210,63,.3)" stroke="#e08a00" stroke-width="1.5"'
    spots = "".join(
        f'<circle class="do-spot" data-zone="{z}" cx="{x}" cy="{y}" r="{r}" {style}/>' for z, x, y, r in SPOTS
    )
    return f'<g class="pp-all">{pip("down", parts=True)}</g>{spots}'


def export():
    """ART keys for export_js.py."""
    return {
        "_do-room": f'<svg viewBox="{ROOM_VB}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="A room with a table, a box and a cat">{room()}</svg>',
        "_do-pip": f'<svg viewBox="{PIP_VB}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pip the panda">{pip_body()}</svg>',
    }


if __name__ == "__main__":
    import os

    css = f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
    cells = [f'<figure><svg viewBox="{ROOM_VB}" width="680">{room(True)}</svg><figcaption>zones</figcaption></figure>']
    for slot in SLOTS:
        cells.append(f'<figure><svg viewBox="{ROOM_VB}" width="680">{room(False, slot)}</svg><figcaption>{slot}</figcaption></figure>')
    cells.append(f'<figure><svg viewBox="{PIP_VB}" width="320">{pip_body(True)}</svg><figcaption>Pip spots</figcaption></figure>')
    html = f"<html><head><style>{css}body{{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:12px}}figure{{margin:0;border:1px solid #ccc}}</style></head><body>{''.join(cells)}</body></html>"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../work/do_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
