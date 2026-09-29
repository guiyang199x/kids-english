"""Pip the panda (the site's mascot) and the scenery for the home page map."""
from common import INK

PINK = "#ff7d93"
RED = "#ef5b56"
LEAF = "#6cc070"


def _arm(x, y, rot):
    return f'<ellipse cx="{x}" cy="{y}" rx="11" ry="17" fill="{INK}" transform="rotate({rot} {x} {y})"/>'


# (behind the head, in front of the head): a paw on the chin has to cover the face.
ARMS = {
    "down": (_arm(-37, 38, 22) + _arm(37, 38, -22), ""),
    "wave": (_arm(-37, 38, 22) + _arm(45, 2, 32), ""),
    "up": (_arm(-45, 2, -32) + _arm(45, 2, 32), ""),
    "chin": (_arm(-37, 38, 22), _arm(20, 14, -42)),
}


def _eyes(look=(0, 0), happy=False):
    patches = (
        f'<ellipse cx="-18" cy="-28" rx="11.5" ry="14.5" fill="{INK}" transform="rotate(32 -18 -28)"/>'
        f'<ellipse cx="18" cy="-28" rx="11.5" ry="14.5" fill="{INK}" transform="rotate(-32 18 -28)"/>'
    )
    if happy:
        return patches + (
            '<path d="M-24 -26Q-17 -35 -10 -26M10 -26Q17 -35 24 -26" fill="none" stroke="#fff" '
            'stroke-width="3.5" stroke-linecap="round"/>'
        )
    dx, dy = look
    out = patches
    for ex in (-16, 16):
        out += (
            f'<circle cx="{ex}" cy="-28" r="7" fill="#fff"/>'
            f'<circle cx="{ex + dx}" cy="{-27 + dy}" r="4.6" fill="{INK}"/>'
            f'<circle cx="{ex + dx - 1.5}" cy="{-29.5 + dy}" r="1.7" fill="#fff"/>'
        )
    return out


def _mouth(open_=False):
    if open_:
        return (
            f'<path d="M-9 -4Q0 12 9 -4Z" fill="{INK}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M-4.5 3.5Q0 0 4.5 3.5Q0 6 -4.5 3.5Z" fill="{PINK}"/>'
        )
    return (
        f'<path d="M0 -7V-4M0 -4C-2 1 -8 1 -9 -3M0 -4C2 1 8 1 9 -3" fill="none" stroke="{INK}" '
        'stroke-width="2.5" stroke-linecap="round"/>'
    )


def pip(arms="down", look=(0, 0), happy=False, extra="", parts=False):
    # parts=True wraps the ears, eyes, nose, mouth, arms and feet in <g class="pp-..."> so each can move on its own.
    g = (lambda cls, s: f'<g class="pp-{cls}">{s}</g>') if parts else (lambda cls, s: s)
    return (
        f'<ellipse cx="0" cy="86" rx="42" ry="7" fill="{INK}" opacity=".12"/>'
        # legs
        + g(
            "feet",
            f'<ellipse cx="-20" cy="74" rx="15" ry="12" fill="{INK}"/>'
            f'<ellipse cx="20" cy="74" rx="15" ry="12" fill="{INK}"/>'
            f'<ellipse cx="-20" cy="77" rx="6" ry="4" fill="{PINK}" opacity=".7"/>'
            f'<ellipse cx="20" cy="77" rx="6" ry="4" fill="{PINK}" opacity=".7"/>',
        )
        # body
        + '<ellipse class="k-o" cx="0" cy="40" rx="37" ry="36" fill="#fff"/>'
        '<ellipse cx="0" cy="48" rx="21" ry="20" fill="#f7f2ea"/>'
        + g("arms", ARMS[arms][0])
        # scarf
        + f'<path class="k-o" d="M18 12L30 34L20 36L12 16Z" fill="{RED}" stroke-width="2.5"/>'
        f'<path class="k-o" d="M-30 4C-14 14 14 14 30 4L29 13C14 23 -14 23 -29 13Z" fill="{RED}" stroke-width="2.5"/>'
        # ears
        + g("ears", f'<circle cx="-35" cy="-60" r="14" fill="{INK}"/><circle cx="35" cy="-60" r="14" fill="{INK}"/>')
        # head
        + '<ellipse class="k-o" cx="0" cy="-26" rx="48" ry="40" fill="#fff"/>'
        # sprout
        f'<path d="M2 -65C2 -72 4 -76 8 -80" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M2 -65C2 -72 4 -76 8 -80" fill="none" stroke="#4a9a4f" stroke-width="2" stroke-linecap="round"/>'
        f'<path class="k-o" d="M7 -79C12 -91 26 -94 32 -89C27 -80 16 -76 7 -79Z" fill="{LEAF}" stroke-width="2.5"/>'
        f'<path class="k-o" d="M5 -76C-2 -86 -14 -86 -18 -80C-12 -73 -2 -72 5 -76Z" fill="{LEAF}" stroke-width="2.5"/>'
        + g("eyes", _eyes(look, happy))
        + f'<ellipse cx="-33" cy="-10" rx="7.5" ry="4.5" fill="{PINK}" opacity=".5"/>'
        f'<ellipse cx="33" cy="-10" rx="7.5" ry="4.5" fill="{PINK}" opacity=".5"/>'
        + g("nose", f'<path d="M-6 -15Q0 -19 6 -15Q4 -9 0 -9Q-4 -9 -6 -15Z" fill="{INK}"/>')
        + g("mouth", _mouth(open_=happy))
        + ARMS[arms][1]
        + extra
    )


WAVE_LINES = (
    f'<path d="M60 -22q6 4 6 12M66 -32q9 6 9 20" fill="none" stroke="{INK}" stroke-width="2.5" '
    'stroke-linecap="round" opacity=".55"/>'
)
SPARKLES = "".join(
    f'<path d="M{x} {y - s}Q{x} {y} {x + s} {y}Q{x} {y} {x} {y + s}Q{x} {y} {x - s} {y}Q{x} {y} {x} {y - s}Z" '
    f'fill="#ffd23f" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    for x, y, s in ((-60, -62, 9), (62, -48, 7), (-64, 18, 6))
)
THINK_DOTS = (
    f'<circle cx="46" cy="-58" r="3" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    f'<circle cx="54" cy="-70" r="4.5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    f'<circle cx="64" cy="-84" r="6" fill="#fff" stroke="{INK}" stroke-width="2"/>'
)

PIP_VB = "-80 -98 160 192"
PIP = {
    "_pip": pip("wave", extra=WAVE_LINES),
    "_pip_cheer": pip("up", happy=True, extra=SPARKLES),
    "_pip_think": pip("chin", look=(2, -2), extra=THINK_DOTS),
}


# ---------- scenery for the island maps (build16), each drawn around 0,0 standing on y=32 ----------
def _shadow(rx=24, y=33):
    return f'<ellipse cx="0" cy="{y}" rx="{rx}" ry="5" fill="{INK}" opacity=".12"/>'


TREE = (
    _shadow(22)
    + f'<path class="k-o" d="M-5 32L-4 8H4L5 32Z" fill="#b5774a"/>'
    + '<path class="k-o" d="M0 -34C14 -34 24 -24 24 -12C30 -8 30 6 22 10C18 16 8 18 0 16C-8 18 -18 16 -22 10C-30 6 -30 -8 -24 -12C-24 -24 -14 -34 0 -34Z" fill="#6cc070"/>'
    + '<path d="M-14 -18C-12 -24 -6 -27 0 -27" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".55"/>'
    + '<circle cx="-10" cy="0" r="3.5" fill="#ef5b56" stroke="#3f3345" stroke-width="1.8"/>'
    + '<circle cx="9" cy="-12" r="3.5" fill="#ef5b56" stroke="#3f3345" stroke-width="1.8"/>'
    + '<circle cx="12" cy="6" r="3.5" fill="#ef5b56" stroke="#3f3345" stroke-width="1.8"/>'
)
PINE = (
    _shadow(18)
    + '<path class="k-o" d="M-4 32V20H4V32Z" fill="#b5774a"/>'
    + '<path class="k-o" d="M0 -38L14 -14H8L20 4H11L24 22H-24L-11 4H-20L-8 -14H-14Z" fill="#3fa37a"/>'
    + '<path d="M-5 -22L-11 -12M-8 -2L-15 8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".45"/>'
)
BUSH = (
    _shadow(26)
    + '<path class="k-o" d="M-26 32C-34 32 -34 16 -24 14C-26 2 -12 -4 -6 4C-2 -8 16 -8 16 4C26 0 34 12 26 20C34 26 30 32 24 32Z" fill="#7fca6a"/>'
    + '<circle cx="-12" cy="18" r="3" fill="#ffd23f" stroke="#3f3345" stroke-width="1.6"/>'
    + '<circle cx="10" cy="12" r="3" fill="#fff" stroke="#3f3345" stroke-width="1.6"/>'
)


def _flower(x, y, col, h=18):
    petals = "".join(
        f'<circle cx="{x + dx}" cy="{y - h + dy}" r="4.5" fill="{col}" stroke="{INK}" stroke-width="1.8"/>'
        for dx, dy in ((0, -5), (5, -1), (3, 5), (-3, 5), (-5, -1))
    )
    return (
        f'<path d="M{x} {y}V{y - h}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M{x} {y}V{y - h}" stroke="#4a9a4f" stroke-width="1.8" stroke-linecap="round"/>'
        f'<path class="k-o" d="M{x} {y - 6}C{x + 4} {y - 12} {x + 11} {y - 12} {x + 12} {y - 9}C{x + 8} {y - 5} {x + 4} {y - 5} {x} {y - 6}Z" fill="{LEAF}" stroke-width="2"/>'
        + petals
        + f'<circle cx="{x}" cy="{y - h}" r="3.2" fill="#ffd23f" stroke="{INK}" stroke-width="1.6"/>'
    )


FLOWERS = _shadow(24) + _flower(-14, 32, "#ff9ab5") + _flower(4, 32, "#fff", 26) + _flower(18, 32, "#b58cf0", 14)
ROCK = (
    _shadow(24)
    + '<path class="k-o" d="M-24 32C-28 22 -20 8 -8 6C-2 -2 14 0 18 10C28 14 28 28 24 32Z" fill="#c9c2d3"/>'
    + '<path d="M-14 14C-10 10 -4 9 0 10" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" opacity=".7"/>'
)
POND = (
    '<ellipse class="k-o" cx="0" cy="18" rx="36" ry="15" fill="#8fd0f5"/>'
    + '<path d="M-20 16Q-14 12 -8 16M6 22Q12 18 18 22" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    + f'<path class="k-o" d="M14 12A7 5 0 1 1 22 16L16 15Z" fill="{LEAF}" stroke-width="2"/>'
)
MUSHROOM = (
    _shadow(16)
    + '<path class="k-o" d="M-7 32C-8 24 -7 16 -6 12H6C7 16 8 24 7 32Z" fill="#fff4e2"/>'
    + '<path class="k-o" d="M-20 12C-20 -4 -10 -12 0 -12C10 -12 20 -4 20 12Z" fill="#ef5b56"/>'
    + '<circle cx="-8" cy="0" r="3.5" fill="#fff"/><circle cx="7" cy="-4" r="2.8" fill="#fff"/><circle cx="10" cy="6" r="2.5" fill="#fff"/>'
)


def _flag(cloth):
    return (
        _shadow(16)
        + f'<path class="k-o" d="M-14 32C-14 26 -6 24 0 24C6 24 14 26 14 32Z" fill="#b5774a"/>'
        + f'<path d="M-2 28V-34" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        + f'<path d="M-2 28V-34" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        + cloth
        + f'<circle cx="-2" cy="-36" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
    )


START_FLAG = _flag(f'<path class="k-o" d="M0 -30C10 -34 20 -26 32 -30V-6C20 -2 10 -10 0 -6Z" fill="{RED}"/>')
