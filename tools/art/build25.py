"""More Pre A1 Starters words: pictures for six lessons that fill gaps in the Cambridge wordlist.

FARM      - chicken, duck, goat, donkey, mouse (cow, horse and sheep come from the farm scene in build15)
HOUSE     - the rooms: bedroom, bathroom, kitchen, living room, dining room, garden
SPORTS    - football, basketball, tennis, baseball, hockey, guitar, piano, skateboard
OPPOSITES - big, small, long, short, old, new, clean, dirty: each shows the pair, with the word's half in full color
DAY       - morning, afternoon, evening, night (the sky at each time), breakfast, lunch, dinner
HELLO     - hello, goodbye, please, thank you, sorry, yes, no

Each drawing is centered on (0, 0) within about x -80..80, y -66..66, like the other word pictures.
Run `python3 build25.py` to preview them all in work/more_words_preview.html.
"""
import math

from common import INK
from build1 import shadow
from build4 import cloud
from build5 import eyes, cheeks, smile, mirror, dstroke, star
from build10 import bed, sofa, table, lamp, chair
from build15 import cow as farm_cow, horse as farm_horse, sheep as farm_sheep, fence
import build14


def ell(cx, cy, rx, ry, fill, rot=0, cls="k-o", extra=""):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    c = f' class="{cls}"' if cls else ""
    return f'<ellipse{c} cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{t} {extra}/>'


def at(x, y, s, inner):
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>'


# ================================================================ farm
def chicken():
    body = "M-30 10C-34 -14 -16 -30 4 -26C8 -44 30 -46 34 -28C36 -18 30 -10 30 -4C44 -10 50 4 42 16C34 36 -18 40 -30 10Z"
    return (
        shadow(52, 40)
        + dstroke("M-4 34V50M-4 50L-12 54M-4 50L4 54", "#f2a33a", 3.5) + dstroke("M12 34V50M12 50L4 54M12 50L20 54", "#f2a33a", 3.5)
        + f'<path class="k-o" d="{body}" fill="#fff"/>'
        + f'<path class="k-o" d="M8 -40C4 -52 14 -54 16 -46C18 -56 28 -54 26 -44C32 -48 36 -40 30 -36Z" fill="#ef5b56" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M34 -26L46 -22L34 -18Z" fill="#ffc93c" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M32 -16Q36 -8 30 -6Q26 -10 30 -16Z" fill="#ef5b56" stroke-width="2"/>'
        + f'<circle cx="24" cy="-30" r="3.5" fill="{INK}"/><circle cx="25" cy="-31.5" r="1.2" fill="#fff"/>'
        + f'<path d="M-14 0Q0 14 16 4" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-30 6C-44 -2 -46 -16 -38 -22C-36 -12 -32 -6 -26 -2Z" fill="#fff" stroke-width="2.5"/>'
        + '<ellipse cx="18" cy="-18" rx="5" ry="3" fill="#ff7d93" opacity=".45"/>'
    )


def duck():
    body = "M-40 8C-44 -8 -30 -16 -10 -12C-8 -36 24 -44 34 -24C40 -12 30 -2 22 2C40 2 46 20 30 32C10 44 -34 38 -40 8Z"
    return (
        shadow(50, 44)
        + f'<path class="k-o" d="{body}" fill="#ffd23f"/>'
        + f'<path class="k-o" d="M32 -22Q50 -24 54 -16Q46 -10 32 -12Z" fill="#ff9a3c" stroke-width="2.5"/>'
        + f'<circle cx="20" cy="-24" r="3.5" fill="{INK}"/><circle cx="21" cy="-25.5" r="1.2" fill="#fff"/>'
        + f'<path class="k-o" d="M-24 6C-10 2 6 6 12 16C-2 22 -18 18 -24 6Z" fill="#f2b92c" stroke-width="2.5"/>'
        + '<ellipse cx="14" cy="-12" rx="5" ry="3" fill="#ff7d93" opacity=".45"/>'
        + f'<path d="M-50 44q8 -5 16 0t16 0M20 46q8 -5 16 0" fill="none" stroke="#8fd3f4" stroke-width="3" stroke-linecap="round"/>'
    )


def goat():
    fur, inner = "#f4efe6", "#e2d6c4"
    horn = f'<path class="k-o" d="M-12 -34C-18 -54 -32 -60 -38 -52C-30 -50 -24 -44 -20 -30Z" fill="#c9b79a" stroke-width="2.5"/>'
    ear = f'<path class="k-o" d="M-26 -18C-44 -24 -56 -18 -58 -10C-48 -8 -36 -8 -26 -10Z" fill="{fur}" stroke-width="2.5"/>'
    return (
        shadow(60, 36)
        + mirror(horn) + mirror(ear)
        + f'<path class="k-o" d="M-28 -24C-28 -44 28 -44 28 -24L22 18C20 32 -20 32 -22 18Z" fill="{fur}"/>'
        + ell(0, 18, 16, 11, inner, cls="k-o", extra='stroke-width="2"')
        + f'<path class="k-o" d="M-8 30Q0 52 8 30Z" fill="{fur}" stroke-width="2.5"/>'
        + f'<ellipse cx="-12" cy="-10" rx="6" ry="4" fill="{INK}"/><ellipse cx="12" cy="-10" rx="6" ry="4" fill="{INK}"/>'
        + '<path d="M-15 -10H-9M9 -10H15" stroke="#fff" stroke-width="1.8"/>'
        + f'<ellipse cx="-5" cy="16" rx="2" ry="3" fill="{INK}"/><ellipse cx="5" cy="16" rx="2" ry="3" fill="{INK}"/>'
        + cheeks(18, 2, 4.5, 3)
    )


def donkey():
    fur, muzzle, dark = "#a79cb0", "#e7e0ea", "#6e627a"
    ear = f'<path class="k-o" d="M-16 -30C-24 -60 -18 -70 -8 -66C-4 -54 -4 -40 -6 -30Z" fill="{fur}"/><path d="M-13 -36C-17 -54 -14 -62 -9 -60" fill="none" stroke="#ff9fb0" stroke-width="4" stroke-linecap="round"/>'
    return (
        shadow(62, 36)
        + mirror(ear)
        + f'<path class="k-o" d="M-26 -26C-26 -44 26 -44 26 -26L24 10H-24Z" fill="{fur}"/>'
        + f'<path d="M-8 -40C-4 -50 4 -50 8 -40C4 -44 -4 -44 -8 -40Z" fill="{dark}"/>'
        + ell(0, 24, 26, 22, muzzle)
        + eyes(13, -14, 4.8)
        + f'<ellipse cx="-9" cy="22" rx="3" ry="4" fill="{dark}"/><ellipse cx="9" cy="22" rx="3" ry="4" fill="{dark}"/>'
        + smile(34, 8, 4)
        + cheeks(22, -2, 5, 3)
    )


def mouse():
    grey, pink = "#b7b1c4", "#ffb3c6"
    ear = ell(-26, -22, 20, 20, grey) + ell(-26, -22, 12, 12, pink, cls="")
    return (
        shadow(52, 38)
        + dstroke("M30 30C54 40 62 20 50 12", "#b7b1c4", 4)
        + mirror(ear)
        + f'<path class="k-o" d="M-30 8C-30 -18 30 -18 30 8C30 30 12 42 0 50C-12 42 -30 30 -30 8Z" fill="{grey}"/>'
        + eyes(11, 4, 4.5)
        + f'<circle class="k-o" cx="0" cy="44" r="5" fill="{pink}" stroke-width="2"/>'
        + mirror(f'<path d="M-8 36L-30 32M-8 40L-30 42" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
        + cheeks(16, 20, 5, 3)
    )


FARM = [
    ("chicken", chicken), ("duck", duck), ("goat", goat), ("donkey", donkey), ("mouse", mouse),
    ("cow", lambda: at(4, 4, .95, farm_cow(14, 54))), ("horse", lambda: at(0, 4, .95, farm_horse(20, 58))),
    ("sheep", lambda: at(10, 0, 1.25, farm_sheep(22, 42))),
]


# ================================================================ my house: the rooms
def room(wall, floor, inner, window=True):
    """A room seen from the front: wall, floor, a skirting board and (unless told not to) a little window."""
    win = (f'<rect class="k-o" x="36" y="-50" width="30" height="26" rx="3" fill="#bfe6ff" stroke-width="2.5"/>'
           f'<path d="M51 -50V-24M36 -37H66" stroke="{INK}" stroke-width="2"/>') if window else ""
    return (
        '<clipPath id="none"></clipPath>'
        f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="{wall}"/>'
        f'<path d="M-74 22H74V38A14 14 0 0 1 60 52H-60A14 14 0 0 1 -74 38Z" fill="{floor}"/>'
        f'<path d="M-74 22H74" stroke="#fff" stroke-width="4"/>'
        + win + inner
        + f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="none" stroke="{INK}" stroke-width="3"/>'
    )


def bedroom():
    return room("#e7ddff", "#d9b38a", at(-6, 10, .62, bed()) + at(-52, -10, .34, lamp()))


def bathroom():
    bubbles = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                      for x, y, r in ((-30, -2, 8), (-16, -8, 10), (0, -4, 7), (14, -10, 9), (26, -2, 6), (-6, -18, 5)))
    return room("#d8f1fb", "#bfe0ea",
                f'<rect x="-74" y="-60" width="148" height="82" fill="url(#tiles)" opacity=".0"/>'
                + dstroke("M42 -6V-36Q42 -44 34 -44H28", "#c9ced6", 4)
                + bubbles
                + f'<path class="k-o" d="M-50 0H52V18C52 32 40 38 28 38H-26C-38 38 -50 32 -50 18Z" fill="#fff"/>'
                + f'<path d="M-44 8H46" stroke="#8fd3f4" stroke-width="4" stroke-linecap="round"/>'
                + f'<rect class="k-o" x="-40" y="36" width="8" height="10" rx="2" fill="#c9ced6" stroke-width="2"/><rect class="k-o" x="32" y="36" width="8" height="10" rx="2" fill="#c9ced6" stroke-width="2"/>'
                + f'<path class="k-o" d="M-34 -8C-38 -18 -26 -22 -22 -14C-18 -18 -14 -14 -16 -10C-20 -4 -30 -2 -34 -8Z" fill="#ffd23f" stroke-width="2"/>',
                window=False)


def kitchen():
    return room("#fff1d6", "#c9d6a8",
                # the stove with a pot on it, and a fridge
                f'<rect class="k-o" x="-60" y="-44" width="40" height="84" rx="6" fill="#dfe8f2"/><path d="M-60 -10H-20" stroke="{INK}" stroke-width="2.5"/>'
                + f'<path d="M-26 -34V-20M-26 -2V14" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                + f'<rect class="k-o" x="-10" y="0" width="64" height="40" rx="4" fill="#ef9a5a"/>'
                + f'<rect class="k-o" x="0" y="12" width="44" height="22" rx="3" fill="#3f3345" stroke-width="2"/>'
                + f'<rect class="k-o" x="-12" y="-6" width="68" height="8" rx="2" fill="#fff" stroke-width="2.5"/>'
                + f'<path class="k-o" d="M4 -6V-24H40V-6Z" fill="#8a9bb0"/><rect class="k-o" x="0" y="-28" width="44" height="6" rx="2" fill="#a9b7c8" stroke-width="2"/>'
                + "".join(f'<path d="M{x} -34q-5 -6 0 -12t0 -12" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".9"/>' for x in (14, 28)),
                window=False)


def living_room():
    tv = (f'<rect class="k-o" x="24" y="-44" width="44" height="32" rx="5" fill="#3f3345"/><rect x="29" y="-39" width="34" height="22" rx="3" fill="#8fd3f4"/>'
          f'<path d="M40 -12L36 -4M52 -12L56 -4" stroke="{INK}" stroke-width="2.5"/>')
    return room("#ffe6d6", "#c99a6a", tv + at(-16, 12, .7, sofa()) + at(52, 20, .4, build14.BUSH), window=False)


def dining_room():
    return room("#e3f4dd", "#d4a878",
                at(-50, 16, .5, chair()) + f'<g transform="translate(50 16) scale(-.5 .5)">{chair()}</g>' + at(0, 12, .62, table())
                + f'<path class="k-o" d="M-10 -34H10L6 -24H-6Z" fill="#ffd23f" stroke-width="2"/><path d="M0 -34V-42" stroke="{INK}" stroke-width="2"/><circle cx="0" cy="-44" r="3" fill="#ffd23f"/>',
                window=False)


def garden():
    flowers = "".join(build14._flower(x, 30, c, h) for x, c, h in ((-48, "#ff9ab5", 26), (-30, "#fff", 18), (30, "#b58cf0", 22), (50, "#ffd23f", 16)))
    return (
        f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="#cdeeff"/>'
        + f'<circle cx="46" cy="-36" r="12" fill="#ffd23f" stroke="{INK}" stroke-width="2.5"/>'
        + f'<path d="M-74 14Q0 0 74 14V38A14 14 0 0 1 60 52H-60A14 14 0 0 1 -74 38Z" fill="#8fd16a"/>'
        + at(-4, -22, .5, fence(-160, 160, 0))
        + at(-40, 6, .75, build14.TREE)
        + at(0, 12, 1, flowers)
        + f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="none" stroke="{INK}" stroke-width="3"/>'
    )


HOUSE = [("bedroom", bedroom), ("bathroom", bathroom), ("kitchen", kitchen), ("living room", living_room),
         ("dining room", dining_room), ("garden", garden)]


# ================================================================ sports and hobbies
def football():
    pent = lambda x, y, r: ("M" + "L".join(f"{x + r * math.cos(math.radians(-90 + k * 72)):.1f} {y + r * math.sin(math.radians(-90 + k * 72)):.1f}" for k in range(5)) + "Z")
    return (
        shadow(56, 44)
        + '<circle class="k-o" cx="0" cy="0" r="46" fill="#fff"/>'
        + f'<path d="{pent(0, 0, 14)}" fill="{INK}"/>'
        + "".join(f'<path d="{pent(34 * math.cos(math.radians(a)), 34 * math.sin(math.radians(a)), 11)}" fill="{INK}"/>' for a in (-90, -18, 54, 126, 198))
        + "".join(f'<path d="M{14 * math.cos(math.radians(a)):.1f} {14 * math.sin(math.radians(a)):.1f}L{24 * math.cos(math.radians(a)):.1f} {24 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="2.5"/>' for a in (-54, 18, 90, 162, 234))
        + '<circle cx="0" cy="0" r="46" fill="none" stroke="#3f3345" stroke-width="3"/>'
        + '<path d="M-30 -24Q-20 -36 -6 -38" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    )


def basketball():
    return (
        shadow(56, 44)
        + '<circle class="k-o" cx="0" cy="0" r="46" fill="#ff9a3c"/>'
        + f'<path d="M-46 0H46M0 -46V46M-32 -33C-12 -14 -12 14 -32 33M32 -33C12 -14 12 14 32 33" fill="none" stroke="{INK}" stroke-width="3"/>'
        + '<path d="M-30 -26Q-20 -36 -8 -38" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    )


def tennis():
    strings = "".join(f'<path d="M{x} -58V-2" stroke="#cfd6de" stroke-width="1.5"/>' for x in range(-38, 1, 8)) + \
              "".join(f'<path d="M-44 {y}H6" stroke="#cfd6de" stroke-width="1.5"/>' for y in range(-54, -5, 8))
    return (
        shadow(58, 50)
        + f'<g transform="rotate(-30 -20 -30)">'
        + dstroke("M-19 2V50", "#3f3345", 6) + dstroke("M-19 22V50", "#ef5b56", 6)
        + '<clipPath id="k-racket"><ellipse cx="-19" cy="-30" rx="24" ry="30"/></clipPath>'
        + f'<ellipse cx="-19" cy="-30" rx="24" ry="30" fill="#fff"/><g clip-path="url(#k-racket)">{strings}</g>'
        + f'<ellipse cx="-19" cy="-30" rx="24" ry="30" fill="none" stroke="{INK}" stroke-width="7"/><ellipse cx="-19" cy="-30" rx="24" ry="30" fill="none" stroke="#4a9be8" stroke-width="3"/>'
        + "</g>"
        + '<circle class="k-o" cx="40" cy="20" r="16" fill="#d8f04a"/>'
        + '<path d="M26 12C34 18 34 28 28 32M54 28C46 22 46 12 52 8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
    )


def baseball():
    return (
        shadow(56, 54)
        + f'<path class="k-o" d="M-62 40L-56 46L30 -38C36 -44 30 -52 22 -48Z" fill="#c98a4b"/>'
        + f'<path d="M-62 40L-56 46" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        + '<circle class="k-o" cx="36" cy="24" r="20" fill="#fff"/>'
        + '<path d="M22 10C30 18 30 30 22 38M50 10C42 18 42 30 50 38" fill="none" stroke="#ef5b56" stroke-width="2.5" stroke-dasharray="3 3"/>'
    )


def hockey():
    return (
        shadow(52, 60)
        + f'<path class="k-o" d="M24 -60L-18 30C-20 36 -26 40 -34 40H-60C-66 40 -68 30 -60 28H-34C-30 28 -28 26 -26 22L14 -62Z" fill="#c98a4b"/>'
        + f'<path d="M-46 28V40M-40 28V40" stroke="#fff" stroke-width="3"/>'
        + ell(36, 36, 22, 8, INK, cls="")
        + f'<rect x="14" y="28" width="44" height="8" fill="{INK}"/>' + ell(36, 28, 22, 8, "#5a4d63", cls="k-o", extra='stroke-width="2"')
    )


def guitar():
    return (
        shadow(60, 34)
        + f'<g transform="rotate(35)">'
        + f'<rect class="k-o" x="-5" y="-66" width="10" height="56" rx="2" fill="#8b5a3c"/>'
        + f'<rect class="k-o" x="-9" y="-76" width="18" height="16" rx="4" fill="#5a3a26"/>'
        + f'<path class="k-o" d="M0 -14C22 -14 26 4 18 12C30 22 26 52 0 52C-26 52 -30 22 -18 12C-26 4 -22 -14 0 -14Z" fill="#ff9a3c"/>'
        + '<circle class="k-o" cx="0" cy="10" r="8" fill="#5a3a26" stroke-width="2.5"/>'
        + f'<rect class="k-o" x="-10" y="30" width="20" height="5" rx="2" fill="#5a3a26" stroke-width="2"/>'
        + "".join(f'<path d="M{x} -72V32" stroke="#f3e6c8" stroke-width="1"/>' for x in (-2.5, 0, 2.5))
        + "</g>"
    )


def piano():
    white = "".join(f'<rect x="{-60 + k * 15}" y="-4" width="15" height="44" fill="#fff" stroke="{INK}" stroke-width="2"/>' for k in range(8))
    black = "".join(f'<rect x="{-60 + k * 15 + 10}" y="-4" width="10" height="26" rx="1.5" fill="{INK}"/>' for k in (0, 1, 3, 4, 5))
    return (
        shadow(56, 66)
        + f'<path class="k-o" d="M-68 -44H68V44H-68Z" fill="#3f3345"/>'
        + f'<rect class="k-o" x="-60" y="-36" width="120" height="24" rx="4" fill="#5a4d63" stroke-width="2"/>'
        + "".join(f'<path d="M{x} -30q6 -4 0 -8" fill="none" stroke="#fff" stroke-width="2"/>' for x in (-40, -20))
        + f'<path d="M24 -30V-18M24 -30L34 -32V-20" fill="none" stroke="#ffd23f" stroke-width="2.5" stroke-linecap="round"/><circle cx="22" cy="-18" r="3" fill="#ffd23f"/><circle cx="32" cy="-20" r="3" fill="#ffd23f"/>'
        + white + black
        + f'<rect x="-68" y="-44" width="136" height="88" rx="4" fill="none" stroke="{INK}" stroke-width="3"/>'
    )


def skateboard():
    wheel = lambda x: f'<circle class="k-o" cx="{x}" cy="24" r="9" fill="#ffd23f"/><circle cx="{x}" cy="24" r="3" fill="{INK}"/>'
    return (
        shadow(40, 60)
        + f'<path d="M-40 10V16M40 10V16" stroke="{INK}" stroke-width="5"/>'
        + wheel(-44) + wheel(-28) + wheel(28) + wheel(44)
        + f'<path class="k-o" d="M-70 -6Q-72 8 -58 10H58Q72 8 70 -6Q66 2 56 2H-56Q-66 2 -70 -6Z" fill="#8150c4"/>'
        + f'<path d="M-40 2L-30 -2M-10 2L0 -2M20 2L30 -2" stroke="#ffd23f" stroke-width="3" stroke-linecap="round"/>'
    )


SPORTS = [("football", football), ("basketball", basketball), ("tennis", tennis), ("baseball", baseball),
          ("hockey", hockey), ("guitar", guitar), ("piano", piano), ("skateboard", skateboard)]


# ================================================================ opposites
# Each shows the pair; the word's half is in full color and the other is pale, so "big" and "small" are the same
# two things with the other one picked out.
def pair(a, b, first):
    """`a` on the left and `b` on the right; `first` picks which one is the word."""
    faded = '<g opacity=".3" style="filter:grayscale(1)">{}</g>'
    return (faded.format(b) + a) if first else (faded.format(a) + b)


def big_small(first):
    return shadow(58, 66) + pair(at(-26, 2, 1.25, build14.TREE.replace('class="sway"', "")),
                                 at(46, 30, .55, build14.TREE), first)


def apple_pic(x, y, s):
    return at(x, y, s, f'<path class="k-o" d="M0 -18C8 -26 30 -26 30 -2C30 18 16 30 8 29C5 28 2 27 0 27C-2 27 -5 28 -8 29C-16 30 -30 18 -30 -2C-30 -26 -8 -26 0 -18Z" fill="#ef5b56"/>'
                         f'<path d="M0 -18C0 -26 4 -32 8 -34" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                         f'<path class="k-o" d="M6 -28C14 -36 24 -32 24 -28C16 -24 10 -24 6 -28Z" fill="#6cc070" stroke-width="2"/>')


def big():
    return shadow(56, 60) + pair(apple_pic(-24, 0, 1.5), apple_pic(46, 28, .6), True)


def small():
    return shadow(56, 60) + pair(apple_pic(-24, 0, 1.5), apple_pic(46, 28, .6), False)


def snake_pic(y, x0, x1, col):
    n = max(2, int((x1 - x0) // 22))
    pts = "".join(f"Q{x0 + (k + .5) * (x1 - x0) / n:.0f} {y + (-10 if k % 2 else 10)} {x0 + (k + 1) * (x1 - x0) / n:.0f} {y}" for k in range(n))
    return (dstroke(f"M{x0} {y}{pts}", col, 10)
            + f'<circle class="k-o" cx="{x1 + 6}" cy="{y}" r="9" fill="{col}" stroke-width="2.5"/><circle cx="{x1 + 9}" cy="{y - 3}" r="2" fill="{INK}"/>'
            + f'<path d="M{x1 + 15} {y + 1}l7 -2m-7 2l7 3" stroke="#ef5b56" stroke-width="2" stroke-linecap="round"/>')


def long_():
    return shadow(56, 66) + pair(snake_pic(-24, -66, 52, "#6cc070"), snake_pic(26, -24, 4, "#6cc070"), True)


def short():
    return shadow(56, 66) + pair(snake_pic(-24, -66, 52, "#6cc070"), snake_pic(26, -24, 4, "#6cc070"), False)


def teddy(x, y, s, worn):
    fur = "#b58a66" if worn else "#d99a5b"
    patch = (f'<rect x="4" y="12" width="12" height="12" fill="#8fd3f4" stroke="{INK}" stroke-width="1.8" transform="rotate(10 10 18)"/>'
             f'<path d="M6 14l8 8M14 14l-8 8" stroke="{INK}" stroke-width="1.2"/>' '<path d="M-20 -30l-4 -6" stroke="#3f3345" stroke-width="2"/>') if worn else ""
    shine = "" if worn else star(24, -28, 7) + star(-26, 20, 5)
    return at(x, y, s,
              mirror(f'<circle class="k-o" cx="-16" cy="-24" r="9" fill="{fur}"/>')
              + f'<ellipse class="k-o" cx="0" cy="16" rx="20" ry="18" fill="{fur}"/>'
              + f'<circle class="k-o" cx="0" cy="-12" r="18" fill="{fur}"/>'
              + ell(0, -6, 8, 6, "#f3d8b8", cls="", extra="")
              + f'<circle cx="-7" cy="-15" r="2.5" fill="{INK}"/><circle cx="7" cy="-15" r="2.5" fill="{INK}"/><circle cx="0" cy="-8" r="2.5" fill="{INK}"/>'
              + patch + shine)


def old():
    return shadow(58, 66) + pair(teddy(-30, 2, 1.25, True), teddy(36, 2, 1.25, False), True)


def new():
    return shadow(58, 66) + pair(teddy(-30, 2, 1.25, True), teddy(36, 2, 1.25, False), False)


def tshirt(x, y, dirty):
    mud = "".join(f'<ellipse cx="{a}" cy="{b}" rx="{r}" ry="{r * .7:.1f}" fill="#8b5a3c"/>' for a, b, r in ((-8, -4, 6), (8, 12, 5), (-4, 20, 3.5), (12, -10, 3))) if dirty else \
        star(-14, -24, 6) + star(20, 22, 5)
    return at(x, y, 1,
              f'<path class="k-o" d="M-12 -30L-34 -20L-28 -4L-20 -8V30H20V-8L28 -4L34 -20L12 -30Q0 -20 -12 -30Z" fill="{"#e9e4d4" if dirty else "#fff"}"/>' + mud)


def clean():
    return shadow(58, 66) + pair(tshirt(-32, 4, False), tshirt(36, 4, True), True)


def dirty():
    return shadow(58, 66) + pair(tshirt(-32, 4, False), tshirt(36, 4, True), False)


# one shirt on its own, for the story "Big and Small" (the word pictures show both)
STORY_BITS = [("_shirt-clean", lambda: shadow(40, 40) + at(0, 0, 1.5, tshirt(0, 4, False))),
              ("_shirt-dirty", lambda: shadow(40, 40) + at(0, 0, 1.5, tshirt(0, 4, True)))]

OPPOSITES = [("big", big), ("small", small), ("long", long_), ("short", short), ("old", old), ("new", new),
             ("clean", clean), ("dirty", dirty)]


# ================================================================ my day
def sky_card(top, bottom, inner, gid):
    return (
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
        f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="url(#{gid})"/>'
        + inner
        + f'<rect x="-74" y="-60" width="148" height="112" rx="14" fill="none" stroke="{INK}" stroke-width="3"/>'
    )


def hills(col, house_lit=False):
    win = "#ffe89a" if house_lit else "#cdeeff"
    return (f'<path d="M-74 22Q-30 4 10 18T74 14V38A14 14 0 0 1 60 52H-60A14 14 0 0 1 -74 38Z" fill="{col}" stroke="{INK}" stroke-width="2" stroke-opacity=".3"/>'
            f'<rect class="k-o" x="-50" y="2" width="30" height="24" fill="#fff3dc" stroke-width="2.5"/><path class="k-o" d="M-54 4L-35 -12L-16 4Z" fill="#ef5b56" stroke-width="2.5"/>'
            f'<rect x="-42" y="10" width="10" height="9" rx="1.5" fill="{win}" stroke="{INK}" stroke-width="1.8"/>')


def sun_at(x, y, r=14, col="#ffd23f", rays=True):
    ray = "".join(f'<path d="M{x + (r + 5) * math.cos(math.radians(a)):.1f} {y + (r + 5) * math.sin(math.radians(a)):.1f}L{x + (r + 11) * math.cos(math.radians(a)):.1f} {y + (r + 11) * math.sin(math.radians(a)):.1f}" stroke="{col}" stroke-width="3.5" stroke-linecap="round"/>' for a in range(0, 360, 45)) if rays else ""
    return ray + f'<circle class="k-o" cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke-width="2.5"/>'


def morning():
    return sky_card("#bfe6ff", "#ffe6c2", sun_at(34, 12, 14) + hills("#9fd784") + at(28, -30, .5, cloud(0, 0, 1) if False else ""), "g-morning")


def afternoon():
    return sky_card("#6cc2f0", "#bfe6ff", sun_at(10, -32, 15) + f'<g transform="translate(-44 -34) scale(.5)">{cloud(0, 0, 1)}</g>' + hills("#8fd16a"), "g-afternoon")


def evening():
    return sky_card("#ff9a6c", "#ffd08a", sun_at(40, 16, 16, "#ff7b3c", rays=False) + hills("#7cb86a", house_lit=True), "g-evening")


def night():
    stars = "".join(star(x, y, r, "#fff6c0", 1.5) for x, y, r in ((-50, -40, 5), (-14, -46, 4), (10, -24, 3.5), (-32, -18, 3)))
    moon = f'<path class="k-o" d="M44 -48A20 20 0 1 0 60 -16A16 16 0 1 1 44 -48Z" fill="#fff1b8" stroke-width="2.5"/>'
    return sky_card("#2d2a5c", "#5a4f95", stars + moon + hills("#3d6b5a", house_lit=True), "g-night")


def breakfast():
    return (
        shadow(56, 66)
        + ell(0, 30, 66, 18, "#fff", extra='stroke-width="2.5"')
        # a bowl of cereal, a glass of milk, and an egg
        + f'<path class="k-o" d="M-54 4H2C2 28 -14 38 -26 38C-38 38 -54 28 -54 4Z" fill="#4a9be8"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#f2b04a" stroke="{INK}" stroke-width="1.5"/>' for x, y in ((-44, 2), (-34, -2), (-24, 1), (-14, -2), (-6, 2)))
        + '<ellipse cx="-26" cy="4" rx="28" ry="5" fill="none" stroke="#3f3345" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M14 -38H40L36 30H18Z" fill="#fff"/><path d="M15 -14H39" stroke="#dfe8f2" stroke-width="3"/>'
        + ell(56, 24, 14, 10, "#fff", extra='stroke-width="2.5"') + f'<circle cx="56" cy="22" r="5" fill="#ffc93c" stroke="{INK}" stroke-width="2"/>'
    )


def lunch():
    return (
        shadow(52, 62)
        # a lunch box with a sandwich and an apple
        + f'<rect class="k-o" x="-60" y="-10" width="120" height="54" rx="10" fill="#6cc070"/>'
        + f'<rect class="k-o" x="-52" y="-4" width="104" height="42" rx="6" fill="#e8f6dc" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M-46 32L-10 -26L26 32Z" fill="#f6dca5"/><path d="M-40 26L-10 -18L20 26" fill="none" stroke="#6cc070" stroke-width="5"/>'
        + f'<path d="M-36 30H16" stroke="#ef5b56" stroke-width="4"/>'
        + f'<circle class="k-o" cx="34" cy="14" r="13" fill="#ef5b56"/><path d="M34 1V-6" stroke="{INK}" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M-60 -10C-60 -30 60 -30 60 -10" fill="none" stroke-width="3"/>'
    )


def dinner():
    return (
        shadow(56, 66)
        + ell(0, 14, 58, 30, "#fff") + ell(0, 14, 44, 22, "#f7f2ea", cls="", extra="")
        # rice, a fish and some peas
        + ell(-16, 10, 18, 12, "#fffdf6", cls="k-o", extra='stroke-width="2"')
        + f'<path class="k-o" d="M4 16C10 6 26 4 34 12L42 6V24L34 18C26 26 10 24 4 16Z" fill="#ff9a6c" stroke-width="2.5"/><circle cx="12" cy="14" r="1.8" fill="{INK}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#6cc070" stroke="{INK}" stroke-width="1.5"/>' for x, y in ((-12, 28), (-4, 30), (-20, 26)))
        + dstroke("M-72 -20V40", "#c9ced6", 3.5) + dstroke("M-78 -20V-4Q-72 2 -66 -4V-20", "#c9ced6", 2.5)
        + dstroke("M70 -20V40", "#c9ced6", 3.5)
        + f'<path d="M-6 -24q-5 -6 0 -12t0 -12M10 -24q-5 -6 0 -12t0 -12" fill="none" stroke="#c9ced6" stroke-width="3" stroke-linecap="round"/>'
    )


DAY = [("morning", morning), ("afternoon", afternoon), ("evening", evening), ("night", night),
       ("breakfast", breakfast), ("lunch", lunch), ("dinner", dinner)]


# ================================================================ hello: words for talking to people
HAND = "#ffd8b8"


def hand(x, y, s=1.0, rot=0):
    """An open hand, palm out and fingers up, standing on (x, y): four fingers, a thumb, and the palm over them."""
    fingers = "".join(f'<rect class="k-o" x="{fx - 4.5}" y="{top}" width="9" height="{-top - 14}" rx="4.5" fill="{HAND}" stroke-width="2.5"/>'
                      for fx, top in ((-12, -50), (-3, -56), (6, -54), (15, -46)))
    thumb = f'<rect class="k-o" x="-5" y="-26" width="9" height="24" rx="4.5" fill="{HAND}" stroke-width="2.5" transform="rotate(-50 0 -2) translate(-18 0)"/>'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">' + fingers + thumb
            + f'<rect class="k-o" x="-17" y="-30" width="37" height="32" rx="12" fill="{HAND}" stroke-width="2.5"/>'
            + f'<path d="M-6 -12Q2 -6 10 -12" fill="none" stroke="#e8b48f" stroke-width="2" stroke-linecap="round"/></g>')


def waves_lines(x, y):
    return f'<path d="M{x} {y}q8 6 8 16M{x + 8} {y - 12}q12 8 12 26" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".6"/>'


def hello():
    return (
        shadow(58, 52)
        + sun_at(-44, -34, 12)
        + f'<path class="k-o" d="M-60 8H-20V56H-60Z" fill="#fff3dc" stroke-width="2.5"/><path class="k-o" d="M-50 56V30A10 10 0 0 1 -30 30V56Z" fill="#c98a4b" stroke-width="2.5"/>'
        + hand(14, 36, 1.3, -12) + waves_lines(44, -30) + waves_lines(-12, -26).replace("M-12", "M-12")
    )


def goodbye():
    return (
        shadow(58, 60)
        + f'<path class="k-o" d="M-66 30H-18L-24 44H-60Z" fill="#ef5b56"/><path d="M-42 30V0" stroke="{INK}" stroke-width="3"/><path class="k-o" d="M-40 2L-22 26H-40Z" fill="#fff" stroke-width="2.5"/>'
        + f'<path d="M-72 50q8 -5 16 0t16 0t16 0" fill="none" stroke="#8fd3f4" stroke-width="3" stroke-linecap="round"/>'
        + hand(22, 40, 1.3, 14) + waves_lines(50, -26)
        + f'<path d="M-12 -40q10 -8 22 -4" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".5"/>'
    )


def please():
    cookie = (f'<circle class="k-o" cx="0" cy="-30" r="20" fill="#e0a86a"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#6b4a2e"/>' for x, y in ((-8, -36), (6, -40), (8, -26), (-6, -22), (-12, -28))))
    palm = (f'<path class="k-o" d="M-44 34C-40 22 -30 16 -16 16H24C32 16 34 26 26 28H4C20 28 40 30 44 22C48 16 58 22 54 30C46 44 26 50 6 50H-30Z" fill="{HAND}"/>')
    bubble = (f'<path class="k-o" d="M36 -58H66Q72 -58 72 -52V-34Q72 -28 66 -28H50L42 -20V-28H36Q30 -28 30 -34V-52Q30 -58 36 -58Z" fill="#fff" stroke-width="2.5"/>'
              f'<path class="k-o" d="M51 -44C44 -50 44 -56 50 -54C51 -54 51 -52 51 -52C51 -52 51 -54 52 -54C58 -56 58 -50 51 -44Z" fill="#ff7d93" stroke-width="1.8"/>')
    return shadow(60, 56) + cookie + palm + bubble


def thank_you():
    return (
        shadow(58, 56)
        + f'<rect class="k-o" x="-40" y="-8" width="80" height="58" rx="6" fill="#ef5b56"/>'
        + f'<rect class="k-o" x="-46" y="-22" width="92" height="18" rx="5" fill="#ff7b76"/>'
        + f'<path d="M-6 -22V50M6 -22V50" stroke="#ffd23f" stroke-width="7"/><path d="M-6 -22V50M6 -22V50" stroke="{INK}" stroke-width="0"/>'
        + f'<path class="k-o" d="M0 -22C-12 -40 -32 -36 -24 -26C-18 -20 -8 -22 0 -22ZM0 -22C12 -40 32 -36 24 -26C18 -20 8 -22 0 -22Z" fill="#ffd23f" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M52 -50C40 -62 30 -52 38 -42L52 -28L66 -42C74 -52 64 -62 52 -50Z" fill="#ff7d93" stroke-width="2.5"/>'
    )


def sorry():
    return (
        shadow(58, 60)
        # a broken cup, and a face saying sorry
        + f'<path class="k-o" d="M-60 20H-34L-30 0L-38 -8L-30 -18H-64L-62 12Z" fill="#8fd3f4"/>'
        + f'<path class="k-o" d="M-24 -18H6L4 20H-20L-24 0L-18 -8Z" fill="#8fd3f4" transform="rotate(14 -8 0)"/>'
        + f'<path class="k-o" d="M8 -10C18 -12 20 4 8 6" fill="none" stroke-width="4" transform="rotate(14 -8 0)"/>'
        + f'<path d="M-66 34q8 6 20 2" fill="none" stroke="#8fd3f4" stroke-width="3" stroke-linecap="round"/>'
        + f'<circle class="k-o" cx="42" cy="-10" r="26" fill="#ffd8b8"/>'
        + f'<path d="M30 -18l6 4M54 -18l-6 4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<circle cx="34" cy="-10" r="3" fill="{INK}"/><circle cx="50" cy="-10" r="3" fill="{INK}"/>'
        + f'<path d="M34 6Q42 0 50 6" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M66 -30C70 -22 70 -18 66 -16C62 -18 62 -22 66 -30Z" fill="#8fd3f4" stroke-width="2"/>'
    )


def yes():
    return (
        shadow(56, 52)
        + f'<circle class="k-o" cx="0" cy="-4" r="46" fill="#6cc070"/>'
        + f'<path d="M-22 -4L-6 12L24 -20" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>'
        + f'<path d="M-22 -4L-6 12L24 -20" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def no():
    return (
        shadow(56, 52)
        + f'<circle class="k-o" cx="0" cy="-4" r="46" fill="#ef5b56"/>'
        + f'<path d="M-18 -22L18 14M18 -22L-18 14" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
        + f'<path d="M-18 -22L18 14M18 -22L-18 14" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>'
    )


HELLO = [("hello", hello), ("goodbye", goodbye), ("please", please), ("thank you", thank_you), ("sorry", sorry),
         ("yes", yes), ("no", no)]

ALL = FARM + HOUSE + SPORTS + OPPOSITES + DAY + HELLO + STORY_BITS


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    groups = (("farm", FARM), ("house", HOUSE), ("sports", SPORTS), ("opposites", OPPOSITES), ("day", DAY), ("hello", HELLO))
    cell = lambda w, fn: (f'<figure><svg viewBox="-82 -68 164 136" xmlns="http://www.w3.org/2000/svg">{fn()}</svg>'
                          f"<figcaption>{w}</figcaption></figure>")
    html = (
        "<!doctype html><meta charset=utf-8><title>More words preview</title><style>"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:Nunito,-apple-system,sans-serif;color:#3f3345}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        ".grid{display:grid;grid-template-columns:repeat(8,150px);gap:10px;margin-bottom:18px}"
        "figure{margin:0;background:#fff;border:3px solid #3f3345;border-radius:16px;padding:6px}"
        "figcaption{text-align:center;font-weight:800}h2{margin:6px 0}"
        "</style>"
        + "".join(f"<h2>{name}</h2><div class=grid>" + "".join(cell(w, fn) for w, fn in items) + "</div>" for name, items in groups)
    )
    out = os.path.join(here, "../../work/more_words_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
