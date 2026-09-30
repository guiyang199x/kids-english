"""Even more Pre A1 Starters words.

CRAYONS - black, white and grey crayons for the Colors lesson (drawn like build2's)
BODY    - head, face, hair, arm, leg (more of My Body)
CLOTHES - jacket, shorts, trousers, T-shirt, boots, glasses, watch, baseball cap (more of Clothes)
SCHOOL  - eraser, crayon, computer, bookcase, board game, paint, poster, keyboard
PEOPLE  - boy, girl, man, woman, friend
SNACKS  - burger, chips, sausage, chocolate, lemonade, pie, pineapple, mango
HOME    - mirror, phone, radio, camera, television, armchair, rug, cupboard

Each drawing is centered on (0, 0) within about x -80..80, y -66..66, like the other word pictures.
Run `python3 build26.py` to preview them all in work/even_more_words_preview.html.
"""
import math

from common import INK
from build1 import shadow
from build2 import crayon as crayon_body
from build5 import eyes, cheeks, smile, mirror, dstroke, star
from build8 import person, glasses as glasses_on, SKIN, SKIN_DARK


def at(x, y, s, inner, rot=0):
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x} {y}){r} scale({s})">{inner}</g>'


def ell(cx, cy, rx, ry, fill, cls="k-o", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<ellipse{c} cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


# ================================================================ crayons
def crayon_pic(main, dark):
    return f'<g transform="rotate(40) translate(0 71)">{crayon_body(main, dark, 112)}</g>'


CRAYONS = [
    ("black", lambda: crayon_pic("#4a4250", "#2e2833")),
    ("white", lambda: crayon_pic("#fbf8f2", "#dcd6ca")),
    ("grey", lambda: crayon_pic("#a9a4ae", "#86818c")),
]


# ================================================================ my body: more parts
def kid_head(hair="#5a3a26", extra=""):
    return (
        f'<circle class="k-o" cx="-34" cy="6" r="8" fill="{SKIN}"/><circle class="k-o" cx="34" cy="6" r="8" fill="{SKIN}"/>'
        f'<circle class="k-o" cx="0" cy="0" r="36" fill="{SKIN}"/>'
        f'<path class="k-o" d="M-36 -2C-40 -44 40 -44 36 -2C28 -20 12 -26 0 -22C-12 -28 -28 -20 -36 -2Z" fill="{hair}"/>'
        + eyes(13, 2, 5) + cheeks(22, 12, 6, 3.5) + smile(14, 8, 6) + extra
    )


def pointer(x0, y0, x1, y1):
    """A yellow arrow pointing at the part the word names."""
    a = math.atan2(y1 - y0, x1 - x0)
    hx, hy = x1 - 10 * math.cos(a), y1 - 10 * math.sin(a)
    px, py = -math.sin(a) * 7, math.cos(a) * 7
    return (dstroke(f"M{x0} {y0}L{hx:.1f} {hy:.1f}", "#ffd23f", 5)
            + f'<path class="k-o" d="M{x1} {y1}L{hx + px:.1f} {hy + py:.1f}L{hx - px:.1f} {hy - py:.1f}Z" fill="#ffd23f" stroke-width="2.5"/>')


def head():
    return shadow(56, 40) + at(-6, 4, 1.2, kid_head()) + pointer(70, -48, 44, -30)


def face():
    ring = '<ellipse cx="0" cy="8" rx="31" ry="27" fill="#fff6c0" opacity=".55"/>'
    frame = '<ellipse cx="0" cy="8" rx="34" ry="30" fill="none" stroke="#ffb31a" stroke-width="4" stroke-dasharray="7 5"/>'
    return shadow(56, 40) + at(-4, 2, 1.25, kid_head(extra=ring + eyes(13, 2, 5) + smile(14, 8, 6) + cheeks(22, 12, 6, 3.5) + frame))


def hair():
    locks = "M-40 10C-50 -40 -20 -56 0 -54C24 -56 52 -40 40 10C36 -8 30 -22 20 -26C8 -18 -12 -18 -26 -26C-34 -18 -38 -6 -40 10Z"
    return (shadow(58, 40) + at(0, 10, 1.15,
            f'<circle class="k-o" cx="0" cy="0" r="34" fill="{SKIN}"/>' + eyes(12, 4, 4.5) + smile(15, 7, 5)
            + f'<path class="k-o" d="{locks}" fill="#e2862f"/>'
            + '<path d="M-24 -40Q-8 -48 10 -44" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"/>')
            + pointer(66, -58, 38, -44))


def arm():
    """An arm bent up to show its muscle, in a short sleeve."""
    return (
        shadow(56, 56)
        + f'<path class="k-o" d="M4 22L20 -34L42 -28L28 28Z" fill="{SKIN}"/>'
        + f'<circle class="k-o" cx="33" cy="-42" r="16" fill="{SKIN}"/>'
        + f'<path d="M26 -52Q32 -56 38 -52" fill="none" stroke="{SKIN_DARK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-46 2C-26 -22 0 -16 14 -2L24 30H-46Z" fill="{SKIN}"/>'
        + f'<path d="M-24 -6Q-10 -14 2 -6" fill="none" stroke="{SKIN_DARK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<rect class="k-o" x="-70" y="-6" width="32" height="40" rx="10" fill="#4a9be8"/>'
        + star(48, -66, 7) + star(64, -44, 5)
    )


def leg():
    return (
        shadow(58, 40)
        + f'<path class="k-o" d="M-16 -64H16V20C16 34 20 40 30 44C44 48 48 58 40 60H-12C-18 60 -18 48 -16 40Z" fill="{SKIN}"/>'
        + f'<path class="k-o" d="M-20 -66H20V-34H-20Z" fill="#4a9be8"/>'
        + f'<path class="k-o" d="M-16 40C-18 50 -14 60 -8 60H40C48 58 46 48 34 44L22 40Z" fill="#ef5b56"/>'
        + f'<path d="M-6 0Q2 6 8 0" fill="none" stroke="{SKIN_DARK}" stroke-width="3" stroke-linecap="round"/>'
    )


BODY = [("head", head), ("face", face), ("hair", hair), ("arm", arm), ("leg", leg)]


# ================================================================ clothes
def jacket():
    body = "M-24 -52L-54 -40L-64 42H-46L-42 -4V52H42V-4L46 42H64L54 -40L24 -52Q0 -42 -24 -52Z"
    return (
        shadow(58, 50)
        + f'<path class="k-o" d="{body}" fill="#5cc36a"/>'
        + f'<path d="M0 -44V52" stroke="{INK}" stroke-width="2.5"/><path d="M4 -40V50" stroke="#c9ced6" stroke-width="3" stroke-dasharray="4 3"/>'
        + f'<path class="k-o" d="M-24 -52Q0 -30 24 -52Q0 -64 -24 -52Z" fill="#3f9e4d" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-34 14H-14V32H-34ZM14 14H34V32H14Z" fill="#3f9e4d" stroke-width="2"/>'
        + f'<path d="M-62 34H-46M62 34H46" stroke="#fff" stroke-width="4"/>'
    )


def shorts():
    return (
        shadow(46, 52)
        + f'<path class="k-o" d="M-44 -32H44L50 30H10L0 -2L-10 30H-50Z" fill="#ff9a3c"/>'
        + f'<path class="k-o" d="M-44 -40H44V-28H-44Z" fill="#e07b1f" stroke-width="2.5"/>'
        + f'<path d="M-6 -34Q0 -24 6 -34" fill="none" stroke="#fff" stroke-width="2.5"/>'
        + f'<path d="M-46 22H-12M12 22H46" stroke="#fff" stroke-width="4"/>'
    )


def trousers():
    return (
        shadow(62, 44)
        + f'<path class="k-o" d="M-34 -60H34L40 58H10L0 -16L-10 58H-40Z" fill="#6a5acd"/>'
        + f'<path class="k-o" d="M-34 -64H34V-52H-34Z" fill="#5446b0" stroke-width="2.5"/>'
        + f'<path d="M-18 -52V-40M18 -52V-40" stroke="{INK}" stroke-width="2"/><path d="M-26 -8L-20 52M26 -8L20 52" stroke="#8578e0" stroke-width="3"/>'
    )


def t_shirt():
    body = "M-22 -46L-52 -32L-40 -8L-30 -14V48H30V-14L40 -8L52 -32L22 -46Q0 -30 -22 -46Z"
    return (
        shadow(56, 44)
        + f'<path class="k-o" d="{body}" fill="#ef5b56"/>'
        + star(0, 6, 16, "#ffd23f", 2.5)
        + f'<path d="M-44 -18L-34 -22M44 -18L34 -22" stroke="#c9403b" stroke-width="3"/>'
    )


def boots():
    boot = lambda col, dark: (
        f'<path class="k-o" d="M-18 -44H12V14C12 18 16 20 22 22C34 26 38 34 34 40H-18Z" fill="{col}"/>'
        f'<path class="k-o" d="M-20 -48H14V-36H-20Z" fill="{dark}" stroke-width="2.5"/>'
        f'<path d="M-18 34H34" stroke="{dark}" stroke-width="6"/>')
    return shadow(48, 60) + at(-24, -6, .9, boot("#ffd23f", "#e8b520")) + at(16, 8, 1, boot("#ffd23f", "#e8b520"))


def glasses():
    return (
        shadow(40, 50)
        + f'<path d="M-66 -10L-50 -14M66 -10L50 -14" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        + f'<circle class="k-o" cx="-26" cy="0" r="22" fill="#cdeeff" fill-opacity=".6" stroke-width="5"/>'
        + f'<circle class="k-o" cx="26" cy="0" r="22" fill="#cdeeff" fill-opacity=".6" stroke-width="5"/>'
        + f'<path d="M-4 -4Q0 -10 4 -4" fill="none" stroke="{INK}" stroke-width="4"/>'
        + '<path d="M-36 -10Q-30 -16 -22 -16M16 -10Q22 -16 30 -16" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
    )


def watch():
    ticks = "".join(f'<path d="M{16 * math.cos(math.radians(a)):.1f} {16 * math.sin(math.radians(a)):.1f}L{20 * math.cos(math.radians(a)):.1f} {20 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="2"/>' for a in range(0, 360, 90))
    return (
        shadow(56, 30)
        + f'<rect class="k-o" x="-12" y="-62" width="24" height="124" rx="10" fill="#ef9a5a"/>'
        + "".join(f'<circle cx="0" cy="{y}" r="2.5" fill="{INK}"/>' for y in (36, 46))
        + f'<circle class="k-o" cx="0" cy="0" r="30" fill="#c9ced6"/><circle class="k-o" cx="0" cy="0" r="24" fill="#fff" stroke-width="2.5"/>'
        + ticks + f'<path d="M0 0V-14M0 0L10 6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><circle cx="0" cy="0" r="2.5" fill="{INK}"/>'
    )


def baseball_cap():
    return (
        shadow(40, 60)
        + f'<path class="k-o" d="M-8 18C20 12 56 16 70 26C56 36 18 32 -8 30Z" fill="#2f7cc6"/>'
        + f'<path class="k-o" d="M-52 22C-56 -20 -30 -40 0 -40C30 -40 50 -20 46 22Z" fill="#4a9be8"/>'
        + f'<path d="M0 -40V22M-26 -34C-34 -16 -34 4 -30 22M26 -34C34 -16 34 4 30 22" fill="none" stroke="#2f7cc6" stroke-width="2.5"/>'
        + f'<circle class="k-o" cx="0" cy="-42" r="5" fill="#2f7cc6" stroke-width="2"/>'
        + star(-2, -4, 10, "#ffd23f", 2)
    )


CLOTHES = [("jacket", jacket), ("shorts", shorts), ("trousers", trousers), ("T-shirt", t_shirt), ("boots", boots),
           ("glasses", glasses), ("watch", watch), ("baseball cap", baseball_cap)]


# ================================================================ school things
def eraser():
    return (
        shadow(40, 56)
        + at(0, 0, 1, f'<path class="k-o" d="M-48 -10L10 -28L50 4L-8 22Z" fill="#f78fb3"/>'
                      f'<path class="k-o" d="M-48 -10V6L-8 38V22Z" fill="#e06b95"/><path class="k-o" d="M-8 22V38L50 20V4Z" fill="#d05a86"/>'
                      f'<path class="k-o" d="M-28 -16L30 -34L50 -18L-8 0Z" fill="#4a9be8" stroke-width="2.5"/>')
        + '<path d="M-30 -6L6 -18" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    )


def crayon():
    return (
        shadow(48, 56)
        + at(-20, 10, .62, crayon_body("#ef5b56", "#c9403b", 112), -50)
        + at(8, 22, .62, crayon_body("#4a9be8", "#2f7cc6", 112), -38)
        + at(34, 30, .62, crayon_body("#ffd23f", "#e8b520", 112), -24)
    )


def computer():
    return (
        shadow(56, 58)
        + f'<rect class="k-o" x="-56" y="-52" width="112" height="76" rx="8" fill="#5a4d63"/>'
        + f'<rect x="-48" y="-44" width="96" height="60" rx="4" fill="#8fd3f4"/>'
        + f'<path d="M-40 -34H6M-40 -22H20M-40 -10H-4" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
        + f'<circle cx="28" cy="-4" r="10" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<path class="k-o" d="M-12 24L-18 40H18L12 24Z" fill="#c9ced6"/>'
        + f'<rect class="k-o" x="-34" y="40" width="68" height="8" rx="3" fill="#c9ced6"/>'
    )


def bookcase():
    cols = ["#ef5b56", "#4a9be8", "#ffd23f", "#6cc070", "#d65b9a", "#ffb13b"]
    books = ""
    for row, base in enumerate((-8, 40)):
        x = -44
        for k in range(6):
            w = 10 + (k * 3 + row) % 6
            h = 34 - (k * 5 + row * 3) % 12
            books += f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="2" fill="{cols[(k + row) % 6]}" stroke="{INK}" stroke-width="2"/>'
            x += w + 2
    return (
        shadow(58, 60)
        + f'<rect class="k-o" x="-54" y="-58" width="108" height="112" rx="6" fill="#c98a4b"/>'
        + f'<rect x="-46" y="-50" width="92" height="96" rx="3" fill="#94592f"/>'
        + books
        + f'<rect class="k-o" x="-50" y="-10" width="100" height="7" rx="2" fill="#c98a4b" stroke-width="2"/>'
    )


def board_game():
    squares = "".join(f'<rect x="{-44 + (k % 5) * 18}" y="{-30 + (k // 5) * 18}" width="18" height="18" fill="{["#ef5b56", "#fff", "#4a9be8", "#fff", "#ffd23f"][(k + k // 5) % 5]}" stroke="{INK}" stroke-width="1.5"/>' for k in range(20))
    return (
        shadow(52, 60)
        + f'<rect class="k-o" x="-54" y="-40" width="108" height="92" rx="8" fill="#6cc070"/>'
        + squares
        + f'<path class="k-o" d="M40 30L54 22L68 30V46L54 54L40 46Z" fill="#fff" stroke-width="2.5"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{INK}"/>' for x, y in ((50, 32), (58, 40), (50, 46)))
        + f'<path class="k-o" d="M-30 38C-36 38 -38 30 -30 26C-34 18 -22 14 -22 24C-18 28 -22 38 -30 38Z" fill="#ef5b56" stroke-width="2"/>'
    )


def paint():
    blobs = "".join(f'<circle class="k-o" cx="{x}" cy="{y}" r="11" fill="{c}" stroke-width="2"/>'
                    for x, y, c in ((-40, -10, "#ef5b56"), (-16, -22, "#ffd23f"), (12, -22, "#6cc070"), (34, -6, "#4a9be8")))
    return (
        shadow(52, 60)
        + f'<path class="k-o" d="M-60 8C-66 -30 -30 -44 6 -42C44 -40 66 -24 62 2C58 20 36 16 30 26C24 38 38 46 22 50C-10 58 -54 42 -60 8Z" fill="#f3e2c4"/>'
        + f'<ellipse cx="12" cy="18" rx="10" ry="8" fill="#fbf6ee" stroke="{INK}" stroke-width="2.5"/>'
        + blobs
        + at(40, 40, 1, dstroke("M0 0L30 -34", "#c98a4b", 5) + f'<path class="k-o" d="M26 -30L34 -44L42 -36Z" fill="#8150c4" stroke-width="2"/>')
    )


def poster():
    return (
        shadow(58, 46)
        + f'<rect class="k-o" x="-44" y="-58" width="88" height="112" rx="4" fill="#fff"/>'
        + f'<rect x="-36" y="-50" width="72" height="56" rx="3" fill="#bfe6ff"/>'
        + f'<circle cx="18" cy="-34" r="9" fill="#ffd23f"/><path d="M-36 6L-12 -22L6 -4L18 -16L36 6Z" fill="#6cc070"/>'
        + f'<path d="M-30 20H30M-30 32H16M-30 44H24" stroke="#c9ced6" stroke-width="5" stroke-linecap="round"/>'
        + "".join(f'<circle cx="{x}" cy="-54" r="4" fill="#ef5b56" stroke="{INK}" stroke-width="1.5"/>' for x in (-36, 36))
    )


def keyboard():
    keys = "".join(f'<rect x="{-58 + c * 13 + (r % 2) * 5}" y="{-18 + r * 13}" width="10" height="10" rx="2" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                   for r in range(3) for c in range(9 - r % 2))
    return (
        shadow(40, 66)
        + f'<rect class="k-o" x="-66" y="-28" width="132" height="62" rx="8" fill="#c9ced6"/>'
        + keys
        + f'<rect x="-30" y="21" width="60" height="9" rx="2" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    )


SCHOOL = [("eraser", eraser), ("crayon", crayon), ("computer", computer), ("bookcase", bookcase),
          ("board game", board_game), ("paint", paint), ("poster", poster), ("keyboard", keyboard)]


# ================================================================ people
def boy():
    front = '<path class="k-o" d="M-31 -12L-32 -34L-20 -40L-14 -52L0 -44L12 -54L20 -42L32 -36L31 -12C20 -28 -20 -28 -31 -12Z" fill="#5a3a26"/>'
    return person("#4a9be8", front=front, extra='<path d="M-48 44H48" stroke="#fff" stroke-width="6"/>')


def girl():
    hair = "#2f2420"
    back = f'<path class="k-o" d="M-34 -14C-40 -50 40 -50 34 -14L38 30H-38Z" fill="{hair}"/>'
    front = f'<path class="k-o" d="M-32 -10C-34 -46 32 -50 32 -10C28 -26 18 -30 10 -30C4 -24 -8 -24 -14 -30C-20 -28 -28 -22 -32 -10Z" fill="{hair}"/>'
    bow = '<path class="k-o" d="M18 -40l-10 -8v16Zm0 0l10 -8v16Z" fill="#ffd23f" stroke-width="2"/>'
    return person("#d65b9a", back=back, front=front + bow)


def man():
    front = '<path class="k-o" d="M-31 -16C-34 -46 -12 -52 4 -50C24 -50 34 -40 31 -16C26 -30 12 -34 0 -32C-10 -36 -24 -30 -31 -16Z" fill="#2f2420"/>'
    beard = f'<path class="k-o" d="M-28 -2C-28 20 -12 26 0 26C12 26 28 20 28 -2C22 10 12 12 0 12C-12 12 -22 10 -28 -2Z" fill="#2f2420" stroke-width="2"/>'
    tie = f'<path class="k-o" d="M-6 22L0 30L6 22ZM-5 30L0 56L5 30L0 28Z" fill="#ef5b56" stroke-width="2"/>'
    return person("#6cc070", front=front, extra=beard + tie)


def woman():
    hair = "#c9602a"
    back = f'<path class="k-o" d="M-36 -14C-42 -52 42 -52 36 -14C40 10 46 30 40 42H-40C-46 30 -40 10 -36 -14Z" fill="{hair}"/>'
    front = f'<path class="k-o" d="M-32 -12C-34 -46 32 -52 32 -10C22 -20 2 -24 -10 -34C-16 -24 -26 -18 -32 -12Z" fill="{hair}"/>'
    beads = "".join(f'<circle cx="{x}" cy="{24 + (x * x) / 60:.1f}" r="3" fill="#ffd23f" stroke="{INK}" stroke-width="1.5"/>' for x in (-14, -7, 0, 7, 14))
    return person("#ffb13b", back=back, front=front, extra=beads)


def friend():
    return (at(-30, 4, .66, boy()) + at(30, 4, .66, girl())
            + f'<path class="k-o" d="M-2 30C-4 44 4 44 2 30Z" fill="{SKIN}" stroke-width="2"/>'
            + f'<path class="k-o" d="M0 -58C-10 -70 -24 -60 -14 -48L0 -36L14 -48C24 -60 10 -70 0 -58Z" fill="#ff7d93" stroke-width="2.5"/>')


PEOPLE = [("boy", boy), ("girl", girl), ("man", man), ("woman", woman), ("friend", friend)]


# ================================================================ yummy food
def burger():
    return (
        shadow(52, 56)
        + f'<path class="k-o" d="M-52 20H52C52 36 40 44 0 44C-40 44 -52 36 -52 20Z" fill="#e8a94f"/>'
        + f'<path class="k-o" d="M-56 8C-40 16 -30 4 -14 12C2 20 14 4 30 12C44 18 52 8 58 14L54 22H-54Z" fill="#6cc070" stroke-width="2.5"/>'
        + f'<rect class="k-o" x="-54" y="-8" width="108" height="16" rx="8" fill="#8b4a2e"/>'
        + f'<path class="k-o" d="M-50 -10L-30 2L-10 -10L10 2L30 -10L50 2L50 -14H-50Z" fill="#ffd23f" stroke-width="2"/>'
        + f'<path class="k-o" d="M-52 -14C-52 -46 52 -46 52 -14Z" fill="#f2b04a"/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3.5" ry="2" fill="#fff6d9"/>' for x, y in ((-24, -30), (-6, -36), (14, -30), (30, -24), (0, -24)))
    )


def chips():
    fries = "".join(f'<rect x="{x}" y="{-58 + (k % 3) * 6}" width="9" height="60" rx="2" fill="#ffd23f" stroke="{INK}" stroke-width="2" transform="rotate({(k - 3) * 5} {x + 4} 0)"/>'
                    for k, x in enumerate(range(-32, 30, 10)))
    return (
        shadow(58, 44)
        + fries
        + f'<path class="k-o" d="M-40 -10H40L32 56H-32Z" fill="#ef5b56"/>'
        + f'<path class="k-o" d="M-12 18C-12 4 12 4 12 18C12 30 0 34 0 34C0 34 -12 30 -12 18Z" fill="#ffd23f" stroke-width="2"/>'
    )


def sausage():
    return (
        shadow(46, 60)
        + f'<path class="k-o" d="M-58 10C-60 -8 -44 -14 -30 -8C-10 0 10 0 30 -8C44 -14 60 -8 58 10C56 26 40 30 20 26C0 22 -20 22 -40 26C-52 28 -58 22 -58 10Z" fill="#c9602a"/>'
        + '<path d="M-40 0C-20 8 20 8 40 0" fill="none" stroke="#e8894f" stroke-width="5" stroke-linecap="round"/>'
        + f'<path d="M-30 14Q-24 10 -18 14T-6 14T6 14T18 14T30 14" fill="none" stroke="#ffd23f" stroke-width="4" stroke-linecap="round"/>'
        + dstroke("M60 30L30 -10", "#c9ced6", 3)
    )


def chocolate():
    squares = "".join(f'<rect x="{-40 + c * 22}" y="{-40 + r * 22}" width="18" height="18" rx="3" fill="#8b4a2e" stroke="#6b3620" stroke-width="2"/>'
                      for r in range(4) for c in range(4) if not (r == 0 and c == 3))
    return (
        shadow(58, 50)
        + f'<path class="k-o" d="M-48 -48H48V52H-48Z" fill="#6b3620"/>'
        + squares
        + f'<path class="k-o" d="M-52 10H52V56H-52Z" fill="#ef5b56"/><path d="M-52 18H52" stroke="#ffd23f" stroke-width="4"/>'
        + f'<path class="k-o" d="M26 -44L44 -44L44 -26Z" fill="#fbf6ee" stroke-width="2"/>'
    )


def lemonade():
    return (
        shadow(58, 36)
        + dstroke("M10 -60L-2 -20", "#ef5b56", 4)
        + f'<path class="k-o" d="M-30 -40H30L24 54H-24Z" fill="#fff8c9"/>'
        + f'<path d="M-28 -18H28L24 54H-24Z" fill="#fff06a" opacity=".85"/>'
        + f'<path d="M-30 -40H30L24 54H-24Z" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        + "".join(f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="#fff" fill-opacity=".7" stroke="#bfe6ff" stroke-width="2" transform="rotate(15 {x + 6} {y + 6})"/>' for x, y in ((-16, -6), (4, 10)))
        + f'<circle class="k-o" cx="32" cy="-40" r="16" fill="#ffd23f"/><path d="M32 -54V-26M18 -40H46M22 -50L42 -30M42 -50L22 -30" stroke="#fff" stroke-width="2"/>'
    )


def pie():
    return (
        shadow(46, 62)
        + f'<path class="k-o" d="M-62 10H62L52 36H-52Z" fill="#c98a4b"/>'
        + f'<path class="k-o" d="M-62 10C-62 -30 62 -30 62 10Z" fill="#f2c14e"/>'
        + "".join(f'<path d="M{x} -18L{x + 8} 8" stroke="#d9a038" stroke-width="3" stroke-linecap="round"/>' for x in (-30, -10, 10, 30))
        + f'<path d="M-62 10Q-52 2 -42 10T-22 10T-2 10T18 10T38 10T58 10" fill="none" stroke="{INK}" stroke-width="3"/>'
        + f'<path d="M-6 -36q-5 -6 0 -12t0 -12M10 -36q-5 -6 0 -12t0 -12" fill="none" stroke="#c9ced6" stroke-width="3" stroke-linecap="round"/>'
    )


def pineapple():
    leaves = "".join(f'<path class="k-o" d="M0 -26C{dx * .4} -40 {dx} -56 {dx * 1.1} -66C{dx * .6} -56 {dx * .2} -44 0 -26Z" fill="#5cc36a" stroke-width="2.5"/>' for dx in (-22, -8, 8, 22, 0))
    grid = "".join(f'<path d="M{-30 + k * 12} -22L{-10 + k * 12} 56" stroke="#d9901f" stroke-width="2.5"/><path d="M{30 - k * 12} -22L{10 - k * 12} 56" stroke="#d9901f" stroke-width="2.5"/>' for k in range(5))
    return (
        shadow(60, 36)
        + leaves
        + '<clipPath id="k-pine"><ellipse cx="0" cy="18" rx="32" ry="42"/></clipPath>'
        + f'<ellipse cx="0" cy="18" rx="32" ry="42" fill="#ffc93c"/><g clip-path="url(#k-pine)">{grid}</g>'
        + f'<ellipse cx="0" cy="18" rx="32" ry="42" fill="none" stroke="{INK}" stroke-width="3"/>'
    )


def mango():
    return (
        shadow(52, 50)
        + f'<path class="k-o" d="M-44 10C-50 -30 -4 -50 30 -36C58 -24 56 20 30 38C4 56 -38 48 -44 10Z" fill="#ffb13b"/>'
        + f'<path d="M-44 10C-50 -30 -4 -50 30 -36C8 -30 -20 -12 -20 20C-20 36 -8 46 0 50C-24 50 -40 36 -44 10Z" fill="#ef7b3c" opacity=".6"/>'
        + f'<path class="k-o" d="M28 -36C34 -48 44 -54 52 -54C50 -44 42 -36 28 -36Z" fill="#5cc36a" stroke-width="2.5"/>'
        + '<path d="M-26 -14Q-16 -26 0 -28" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
    )


SNACKS = [("burger", burger), ("chips", chips), ("sausage", sausage), ("chocolate", chocolate), ("lemonade", lemonade),
          ("pie", pie), ("pineapple", pineapple), ("mango", mango)]


# ================================================================ things at home
def mirror():
    return (
        shadow(60, 40)
        + f'<ellipse class="k-o" cx="0" cy="-6" rx="42" ry="54" fill="#c98a4b"/>'
        + f'<ellipse class="k-o" cx="0" cy="-6" rx="32" ry="44" fill="#d8f1fb" stroke-width="2.5"/>'
        + '<path d="M-18 -30L6 -44M-20 -12L16 -34" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-10 46H10L14 58H-14Z" fill="#94592f" stroke-width="2.5"/>'
    )


def phone():
    return (
        shadow(60, 34)
        + f'<rect class="k-o" x="-30" y="-58" width="60" height="112" rx="12" fill="#5a4d63"/>'
        + f'<rect x="-24" y="-46" width="48" height="84" rx="4" fill="#8fd3f4"/>'
        + "".join(f'<rect x="{-18 + (k % 3) * 13}" y="{-38 + (k // 3) * 16}" width="10" height="10" rx="3" fill="{c}"/>'
                  for k, c in enumerate(("#ef5b56", "#ffd23f", "#6cc070", "#4a9be8", "#d65b9a", "#ffb13b")))
        + f'<circle cx="0" cy="46" r="4" fill="#c9ced6"/>'
        + f'<path d="M36 -40q10 8 0 18M44 -48q18 16 0 34" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    )


def radio():
    return (
        shadow(52, 60)
        + f'<path d="M34 -30L50 -62" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><circle cx="50" cy="-62" r="4" fill="{INK}"/>'
        + f'<rect class="k-o" x="-60" y="-30" width="120" height="76" rx="12" fill="#ef9a5a"/>'
        + f'<circle class="k-o" cx="-24" cy="8" r="24" fill="#fbf6ee" stroke-width="2.5"/>'
        + "".join(f'<circle cx="{-24 + dx}" cy="{8 + dy}" r="2.5" fill="{INK}"/>' for dx in (-10, 0, 10) for dy in (-10, 0, 10))
        + f'<rect class="k-o" x="10" y="-18" width="40" height="20" rx="3" fill="#ffe89a" stroke-width="2"/><path d="M26 -18V2" stroke="#ef5b56" stroke-width="2.5"/>'
        + f'<circle class="k-o" cx="20" cy="26" r="7" fill="#fff" stroke-width="2"/><circle class="k-o" cx="40" cy="26" r="7" fill="#fff" stroke-width="2"/>'
        + f'<path d="M-58 -46q6 -6 12 0M64 -10q6 -6 12 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity=".5"/>'
    )


def camera():
    return (
        shadow(52, 60)
        + f'<path class="k-o" d="M-24 -34L-16 -46H16L24 -34Z" fill="#5a4d63"/>'
        + f'<rect class="k-o" x="-60" y="-34" width="120" height="80" rx="12" fill="#3f3345"/>'
        + f'<circle class="k-o" cx="0" cy="6" r="30" fill="#c9ced6"/><circle class="k-o" cx="0" cy="6" r="20" fill="#4a9be8" stroke-width="2.5"/>'
        + '<circle cx="-7" cy="-1" r="6" fill="#fff" opacity=".7"/>'
        + f'<rect class="k-o" x="34" y="-26" width="16" height="10" rx="2" fill="#ffd23f" stroke-width="2"/>'
        + f'<rect x="-50" y="-26" width="14" height="8" rx="2" fill="#ef5b56"/>'
    )


def television():
    return (
        shadow(58, 60)
        + f'<path d="M-8 -48L-28 -66M8 -48L28 -66" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        + f'<rect class="k-o" x="-64" y="-48" width="128" height="88" rx="14" fill="#5a4d63"/>'
        + f'<rect x="-54" y="-38" width="90" height="68" rx="8" fill="#8fd3f4"/>'
        + f'<path d="M-54 14Q-30 0 -10 10T36 6V30H-54Z" fill="#6cc070"/><circle cx="14" cy="-18" r="9" fill="#ffd23f"/>'
        + "".join(f'<circle cx="50" cy="{y}" r="5" fill="{c}" stroke="{INK}" stroke-width="2"/>' for y, c in ((-24, "#ffd23f"), (-6, "#ef5b56")))
        + f'<path d="M-40 40L-46 54M40 40L46 54" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    )


def armchair():
    return (
        shadow(54, 60)
        + f'<path d="M-44 44V56M44 44V56" stroke="#94592f" stroke-width="7" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-44 -40C-44 -60 44 -60 44 -40V20H-44Z" fill="#d65b9a"/>'
        + f'<rect class="k-o" x="-46" y="8" width="92" height="36" rx="10" fill="#e67db0"/>'
        + f'<rect class="k-o" x="-64" y="-14" width="26" height="58" rx="12" fill="#d65b9a"/>'
        + f'<rect class="k-o" x="38" y="-14" width="26" height="58" rx="12" fill="#d65b9a"/>'
        + f'<path d="M-20 -40V-2M0 -44V-2M20 -40V-2" stroke="#c24a88" stroke-width="3" stroke-linecap="round"/>'
    )


def rug():
    return (
        shadow(44, 70)
        + f'<ellipse class="k-o" cx="0" cy="10" rx="70" ry="34" fill="#4fc1b9"/>'
        + f'<ellipse cx="0" cy="10" rx="54" ry="24" fill="none" stroke="#ffd23f" stroke-width="5"/>'
        + f'<ellipse cx="0" cy="10" rx="34" ry="14" fill="#ef5b56" stroke="{INK}" stroke-width="2"/>'
        + "".join(f'<path d="M{70 * math.cos(math.radians(a)):.1f} {10 + 34 * math.sin(math.radians(a)):.1f}l{8 * math.cos(math.radians(a)):.1f} {8 * math.sin(math.radians(a)):.1f}" stroke="{INK}" stroke-width="2"/>' for a in range(0, 360, 20))
    )


def cupboard():
    return (
        shadow(60, 52)
        + f'<rect class="k-o" x="-48" y="-60" width="96" height="116" rx="6" fill="#e0a86a"/>'
        + f'<rect class="k-o" x="-40" y="-52" width="38" height="100" rx="3" fill="#c98a4b" stroke-width="2.5"/>'
        + f'<rect class="k-o" x="2" y="-52" width="38" height="100" rx="3" fill="#c98a4b" stroke-width="2.5"/>'
        + f'<circle cx="-8" cy="0" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/><circle cx="8" cy="0" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<path d="M-40 56V62M40 56V62" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    )


HOME = [("mirror", mirror), ("phone", phone), ("radio", radio), ("camera", camera), ("television", television),
        ("armchair", armchair), ("rug", rug), ("cupboard", cupboard)]

ALL = CRAYONS + BODY + CLOTHES + SCHOOL + PEOPLE + SNACKS + HOME


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    groups = (("crayons", CRAYONS), ("body", BODY), ("clothes", CLOTHES), ("school", SCHOOL), ("people", PEOPLE),
              ("snacks", SNACKS), ("home", HOME))
    cell = lambda w, fn: (f'<figure><svg viewBox="-82 -68 164 136" xmlns="http://www.w3.org/2000/svg">{fn()}</svg>'
                          f"<figcaption>{w}</figcaption></figure>")
    html = (
        "<!doctype html><meta charset=utf-8><title>Even more words preview</title><style>"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:Nunito,-apple-system,sans-serif;color:#3f3345}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        ".grid{display:grid;grid-template-columns:repeat(8,150px);gap:10px;margin-bottom:14px}"
        "figure{margin:0;background:#fff;border:3px solid #3f3345;border-radius:16px;padding:6px}"
        "figcaption{text-align:center;font-weight:800}h2{margin:4px 0}"
        "</style>"
        + "".join(f"<h2>{name}</h2><div class=grid>" + "".join(cell(w, fn) for w, fn in items) + "</div>" for name, items in groups)
    )
    out = os.path.join(here, "../../work/even_more_words_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
