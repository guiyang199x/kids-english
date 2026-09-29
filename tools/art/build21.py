"""Sea animals, vegetables and bugs. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66.

(fish, whale, jellyfish and turtle are already drawn for the alphabet in build1 / build5.)
Run `python3 build21.py` to preview all three sets in work/sets_preview.html.
"""
import math
from common import INK, fmt, smooth_path
from build1 import shadow
from build4 import union, circ
from build5 import eyes, cheeks, smile, mirror, dstroke

SHINE = 'fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" opacity=".6"'


def ell(cx, cy, rx, ry, fill, rot=0, cls="k-o", extra=""):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{t} {extra}/>'


def face(x, y, s=1.0, cheek=True):
    """Eyes, smile and cheeks around (x, y)."""
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        + eyes(9, 0, 4.5)
        + (cheeks(15, 8, 5, 3) if cheek else "")
        + smile(8, 5, 4)
        + "</g>"
    )


# ================================================================ sea animals
def octopus():
    body = "#b784e6"
    legs = ""
    for x, s in ((-26, -1), (-15, -1), (-5, -1), (5, 1), (15, 1), (26, 1)):
        legs += dstroke(f"M{x} -4C{x} 22 {x + s * 16} 28 {x + s * 16} 42Q{x + s * 16} 52 {x + s * 6} 50", body, 9)
    spots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d9b8f5"/>' for x, y, r in ((-18, -34, 5), (16, -38, 4), (24, -24, 3)))
    return (
        shadow(58, 46)
        + legs
        + ell(0, -16, 36, 32, body)
        + spots
        + face(0, -12, 1.1)
    )


def shark():
    grey, belly = "#7fa6c9", "#eef5fb"
    return (
        shadow(46, 60)
        + f'<path class="k-o" d="M-12 -22L4 -52L20 -18Z" fill="{grey}"/>'
        + f'<path class="k-o" d="M-66 4C-52 -26 12 -32 40 -12L68 -36L60 2L70 30L40 14C10 30 -46 30 -66 4Z" fill="{grey}"/>'
        + f'<path d="M-62 10C-40 26 10 24 36 14C8 18 -38 18 -62 10Z" fill="{belly}"/>'
        + f'<path class="k-o" d="M-16 14L-6 36L8 16Z" fill="{grey}" stroke-width="2.5"/>'
        + f'<path d="M-24 -8Q-20 0 -24 8M-16 -9Q-12 0 -16 9M-8 -9Q-4 0 -8 9" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + f'<circle cx="-42" cy="-6" r="5" fill="{INK}"/><circle cx="-40.5" cy="-8" r="2" fill="#fff"/>'
        + f'<path d="M-60 8Q-52 15 -42 10" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + '<path d="M-44 -20Q-30 -26 -14 -26" ' + SHINE + "/>"
    )


def dolphin():
    blue, belly = "#6fb7e9", "#dff1fc"
    return (
        f'<path d="M-66 50Q-50 40 -34 50T-2 50T30 50T62 50" fill="none" stroke="#8ec5ff" stroke-width="5" stroke-linecap="round"/>'
        + '<g transform="rotate(-12)">'
        + f'<path class="k-o" d="M-4 -26L10 -50L22 -22Z" fill="{blue}"/>'
        + f'<path class="k-o" d="M-68 8Q-72 0 -58 -4C-40 -32 12 -40 40 -16C50 -8 56 4 58 12L74 2L68 26L50 30L54 16C44 4 20 -2 -10 8C-30 16 -52 18 -68 8Z" fill="{blue}"/>'
        + f'<path d="M-64 8C-50 14 -30 12 -12 6C-30 6 -48 6 -64 8Z" fill="{belly}"/>'
        + f'<path class="k-o" d="M-12 6L-20 28L2 10Z" fill="{blue}" stroke-width="2.5"/>'
        + f'<circle cx="-40" cy="-12" r="5" fill="{INK}"/><circle cx="-38.5" cy="-14" r="2" fill="#fff"/>'
        + f'<path d="M-62 2Q-54 8 -46 4" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + '<path d="M-30 -24Q-14 -32 4 -30" ' + SHINE + "/>"
        + "</g>"
    )


def starfish():
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        r = 58 if k % 2 == 0 else 27
        pts.append((r * math.cos(a), 6 + r * math.sin(a)))
    dots = "".join(
        f'<circle cx="{fmt(38 * math.cos(math.radians(-90 + k * 72)))}" cy="{fmt(6 + 38 * math.sin(math.radians(-90 + k * 72)))}" r="3.5" fill="#ffd28a"/>'
        for k in range(5)
    )
    return (
        shadow(58, 44)
        + f'<path class="k-o" d="{smooth_path(pts, closed=True)}" fill="#ff9a3c"/>'
        + dots
        + face(0, 4, 1.05)
    )


def seahorse():
    body = "#ffc93c"
    outline = [(6, -58), (22, -50), (42, -46), (42, -37), (22, -35), (14, -24), (22, -2), (15, 20), (0, 28),
               (-14, 16), (-18, -8), (-12, -30), (-10, -48)]
    return (
        shadow(60, 30)
        + f'<path class="k-o" d="M-17 -18Q-32 -12 -30 4Q-24 -2 -18 2Z" fill="#ff9a3c" stroke-width="2.5"/>'
        + dstroke("M3 22C10 44 -2 60 -16 54C-28 48 -20 34 -10 40", body, 11)
        + f'<path class="k-o" d="{smooth_path(outline, closed=True)}" fill="{body}"/>'
        + f'<path d="M-2 -14Q6 -12 10 -16M-4 -2Q6 0 12 -4M-4 10Q4 12 8 8" fill="none" stroke="#e0a800" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<path class="k-o" d="M-6 -56L-4 -66L4 -58L10 -66L12 -54" fill="#ff9a3c" stroke-width="2.2"/>'
        + f'<circle cx="8" cy="-44" r="4.5" fill="{INK}"/><circle cx="9.5" cy="-45.5" r="1.8" fill="#fff"/>'
        + f'<ellipse cx="18" cy="-34" rx="4" ry="2.5" fill="#ff7d93" opacity=".5"/>'
    )


def penguin():
    dark, orange = "#4a4a6a", "#ff9a3c"
    wing = ell(-36, 8, 10, 26, dark, 18)
    foot = ell(-14, 54, 13, 6, orange, 0, "k-o", 'stroke-width="2.5"')
    return (
        shadow(58, 40)
        + mirror(foot)
        + mirror(wing)
        + ell(0, 4, 36, 52, dark)
        + f'<path d="M0 -30C24 -44 28 -16 24 0C28 30 16 50 0 50C-16 50 -28 30 -24 0C-28 -16 -24 -44 0 -30Z" fill="#fff"/>'
        + eyes(10, -22, 4.5)
        + cheeks(18, -12, 5, 3)
        + f'<path class="k-o" d="M-8 -14L8 -14L0 -4Z" fill="{orange}" stroke-width="2.2"/>'
    )


SEA = [("octopus", octopus), ("shark", shark), ("dolphin", dolphin), ("starfish", starfish),
       ("seahorse", seahorse), ("penguin", penguin)]


# ================================================================ vegetables
def leaf(x, y, rot, length=26, fill="#5cc36a"):
    return (f'<path class="k-o" d="M0 0C-8 -{length * .4} -6 -{length * .8} 0 -{length}C6 -{length * .8} 8 -{length * .4} 0 0Z" '
            f'fill="{fill}" stroke-width="2.5" transform="translate({x} {y}) rotate({rot})"/>')


def carrot():
    return (
        shadow(58, 30)
        + '<g transform="rotate(-24 0 10)">'
        + leaf(0, -32, -30, 28) + leaf(0, -32, 0, 34) + leaf(0, -32, 30, 28)
        + '<path class="k-o" d="M-20 -30Q0 -42 20 -30Q16 12 3 58Q0 62 -3 58Q-16 12 -20 -30Z" fill="#ff8a2b"/>'
        + f'<path d="M-15 -8H-7M8 6H15M-12 22H-5M5 36H10" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + '<path d="M-12 -24Q-12 -6 -9 8" ' + SHINE + "/>"
        + "</g>"
    )


def tomato():
    calyx = "".join(leaf(0, -34, a, 18, "#4fae5a") for a in (-110, -55, 0, 55, 110))
    return (
        shadow(58, 46)
        + ell(0, 10, 50, 44, "#ef4f4a")
        + '<path d="M-34 -8Q-30 -22 -16 -28" ' + SHINE + "/>"
        + calyx
        + f'<path d="M0 -34Q0 -46 6 -52" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
        + '<path d="M0 -34Q0 -46 6 -52" fill="none" stroke="#4fae5a" stroke-width="3.5" stroke-linecap="round"/>'
    )


def potato():
    pts = [(-56, -4), (-44, -30), (-10, -38), (24, -34), (54, -16), (58, 12), (36, 34), (0, 38), (-34, 32), (-54, 18)]
    spots = "".join(f'<path d="M{x - 3} {y}Q{x} {y + 3} {x + 3} {y}" fill="none" stroke="#a86c34" stroke-width="2.5" stroke-linecap="round"/>'
                    for x, y in ((-30, -14), (4, -20), (30, 4), (-12, 16), (-40, 10), (22, 22)))
    return (
        shadow(50, 54)
        + f'<path class="k-o" d="{smooth_path(pts, closed=True)}" fill="#dcaa62"/>'
        + spots
        + '<path d="M-40 -18Q-26 -30 -8 -30" ' + SHINE + "/>"
    )


def corn():
    kernels = ""
    for row in range(9):
        y = -42 + row * 10
        half = 17 * math.sqrt(max(0, 1 - (y / 50) ** 2))
        for x in (-10, 0, 10):
            if abs(x) + 4 < half:
                kernels += f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" rx="3" fill="#ffe27a" stroke="#e0a800" stroke-width="1.5"/>'
    husk = lambda s: (f'<path class="k-o" d="M0 50C{s * -34} 40 {s * -40} 0 {s * -30} -24C{s * -24} 0 {s * -16} 24 0 50Z" '
                      f'fill="#7fcf6f" stroke-width="2.5"/>')
    return (
        shadow(60, 38)
        + '<g transform="rotate(18)">'
        + ell(0, -2, 22, 52, "#ffc93c")
        + kernels
        + husk(1) + husk(-1)
        + f'<path class="k-o" d="M0 50C-10 40 -8 20 0 10C8 20 10 40 0 50Z" fill="#5cc36a" stroke-width="2.5"/>'
        + "</g>"
    )


def broccoli():
    heads = [circ(-28, -18, 20), circ(0, -32, 24), circ(28, -18, 20), circ(-14, -4, 18), circ(14, -4, 18)]
    bumps = "".join(f'<path d="M{x - 5} {y}Q{x} {y - 5} {x + 5} {y}" fill="none" stroke="#2f8a3e" stroke-width="2.5" stroke-linecap="round"/>'
                    for x, y in ((-30, -22), (-4, -38), (22, -26), (4, -16), (-18, -4), (30, -10), (8, -2)))
    return (
        shadow(58, 34)
        + '<path class="k-o" d="M-12 2L-10 54H10L12 2Z" fill="#a8d86a"/>'
        + f'<path d="M-2 16L-16 4M2 26L14 10" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        + '<path d="M-2 16L-16 4M2 26L14 10" stroke="#a8d86a" stroke-width="3" stroke-linecap="round"/>'
        + union(heads, "#4caf50")
        + bumps
    )


def onion():
    return (
        shadow(58, 36)
        + f'<path d="M-6 50Q-10 58 -14 60M0 52V62M6 50Q10 58 14 60" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + '<path class="k-o" d="M0 -36C30 -20 46 10 36 34C28 52 -28 52 -36 34C-46 10 -30 -20 0 -36Z" fill="#b84a7a"/>'
        + '<path d="M0 -30C-16 -10 -18 24 -8 46M0 -30C16 -10 18 24 8 46M-2 -30C-30 -4 -34 26 -24 42" fill="none" stroke="#d985ae" stroke-width="2.5" stroke-linecap="round"/>'
        + '<path class="k-o" d="M-6 -34Q-4 -50 -12 -60Q2 -54 4 -34Z" fill="#7fcf6f" stroke-width="2.5"/>'
        + '<path d="M-28 10Q-28 -6 -18 -18" ' + SHINE + "/>"
    )


def pumpkin():
    o = "#ff9a3c"
    return (
        shadow(58, 60)
        + f'<path d="M8 -38C22 -54 44 -44 36 -32C32 -26 24 -32 30 -38" fill="none" stroke="#4fae5a" stroke-width="3" stroke-linecap="round"/>'
        + ell(-28, 10, 30, 40, o) + ell(28, 10, 30, 40, o)
        + ell(0, 10, 28, 44, "#ffab55")
        + f'<path class="k-o" d="M-6 -30L-8 -50Q0 -54 6 -50L6 -30Z" fill="#8a5a3c" stroke-width="2.5"/>'
        + leaf(-8, -36, -70, 26)
        + '<path d="M-44 -6Q-42 -20 -32 -26" ' + SHINE + "/>"
    )


def peas():
    pea = "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="#7fcf6f" stroke="{INK}" stroke-width="2.5"/>'
                  f'<circle cx="{x - 4}" cy="{y - 4}" r="3" fill="#fff" opacity=".6"/>'
                  for x, y in ((-36, 2), (-12, -4), (12, -6), (36, -4)))
    return (
        shadow(40, 62)
        + '<path class="k-o" d="M-64 6C-44 -30 44 -34 66 -10C44 26 -40 34 -64 6Z" fill="#4fae5a"/>'
        + '<path d="M-56 4C-36 -18 36 -22 58 -10C36 4 -34 12 -56 4Z" fill="#2f8a3e"/>'
        + pea
        + '<path class="k-o" d="M-64 6C-40 34 44 26 66 -10C40 16 -38 22 -64 6Z" fill="#6fcf62"/>'
        + f'<path d="M66 -10Q74 -18 72 -28" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        + '<path d="M66 -10Q74 -18 72 -28" fill="none" stroke="#4fae5a" stroke-width="3" stroke-linecap="round"/>'
    )


VEGETABLES = [("carrot", carrot), ("tomato", tomato), ("potato", potato), ("corn", corn),
              ("broccoli", broccoli), ("onion", onion), ("pumpkin", pumpkin), ("peas", peas)]


# ================================================================ bugs
def antennae(x, y, spread=10, h=18, dot="#3f3345"):
    return (
        f'<path d="M{x - 4} {y}Q{x - spread} {y - h * .6} {x - spread - 4} {y - h}M{x + 4} {y}Q{x + spread} {y - h * .6} {x + spread + 4} {y - h}" '
        f'fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        f'<circle cx="{x - spread - 4}" cy="{y - h}" r="3.5" fill="{dot}"/><circle cx="{x + spread + 4}" cy="{y - h}" r="3.5" fill="{dot}"/>'
    )


def bee():
    stripes = ""
    for x in (-4, 14):
        h = 27 * math.sqrt(max(0, 1 - ((x - 6) / 36) ** 2)) - 1.5
        stripes += f'<path d="M{x} {fmt(6 - h)}V{fmt(6 + h)}" stroke="{INK}" stroke-width="9"/>'
    return (
        shadow(52, 40)
        + ell(-4, -28, 16, 22, "#e3f4ff", -20, "k-o", 'stroke-width="2.5" opacity=".95"')
        + ell(18, -28, 14, 20, "#e3f4ff", 20, "k-o", 'stroke-width="2.5" opacity=".95"')
        + f'<path class="k-o" d="M40 0L56 6L40 12Z" fill="{INK}"/>'
        + ell(6, 6, 36, 27, "#ffc93c")
        + stripes
        + antennae(-36, -18, 6, 18)
        + '<circle class="k-o" cx="-36" cy="-2" r="20" fill="#ffc93c"/>'
        + face(-36, -4, .9)
    )


def ant():
    red = "#c9503a"
    legs = ""
    for x, d in ((-16, -10), (-8, 0), (0, 10)):
        legs += f'<path d="M{x} 4L{x + d - 6} 22L{x + d - 10} 36" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    return (
        shadow(40, 56)
        + legs
        + ell(26, 2, 26, 20, red)
        + ell(-8, 2, 12, 10, red)
        + antennae(-38, -18, 6, 20)
        + f'<circle class="k-o" cx="-38" cy="-4" r="17" fill="{red}"/>'
        + f'<circle cx="-44" cy="-8" r="4" fill="{INK}"/><circle cx="-32" cy="-8" r="4" fill="{INK}"/>'
        + '<circle cx="-43" cy="-9.5" r="1.5" fill="#fff"/><circle cx="-31" cy="-9.5" r="1.5" fill="#fff"/>'
        + f'<path d="M-43 2Q-38 6 -33 2" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + '<path d="M12 -10Q24 -16 36 -12" ' + SHINE + "/>"
    )


def ladybug():
    spots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>' for x, y, r in
                    ((-20, -6, 7), (20, -6, 7), (-26, 22, 6), (26, 22, 6), (-10, 36, 5), (10, 36, 5)))
    leg = f'<path d="M-40 0L-54 -6M-42 18L-56 20M-36 34L-48 44" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    return (
        shadow(58, 44)
        + mirror(leg)
        + antennae(0, -40, 8, 16)
        + f'<circle class="k-o" cx="0" cy="-30" r="20" fill="{INK}"/>'
        + '<circle class="k-o" cx="0" cy="12" r="42" fill="#ef4f4a"/>'
        + f'<path d="M0 -28V52" stroke="{INK}" stroke-width="3"/>'
        + spots
        + '<path d="M-30 -8Q-24 -22 -12 -26" ' + SHINE + "/>"
        + '<circle cx="-8" cy="-34" r="4.5" fill="#fff"/><circle cx="8" cy="-34" r="4.5" fill="#fff"/>'
        + f'<circle cx="-7" cy="-34" r="2.2" fill="{INK}"/><circle cx="9" cy="-34" r="2.2" fill="{INK}"/>'
    )


def butterfly():
    wings = (
        ell(-28, -18, 26, 30, "#ff7d93", -25) + ell(-22, 22, 18, 20, "#b784e6", 20)
        + '<circle cx="-30" cy="-22" r="8" fill="#ffd23f"/><circle cx="-22" cy="24" r="6" fill="#fff" opacity=".8"/>'
    )
    return (
        shadow(58, 34)
        + mirror(wings)
        + ell(0, 6, 8, 34, "#5b4a6b")
        + antennae(0, -26, 8, 20)
        + f'<circle class="k-o" cx="0" cy="-28" r="11" fill="#5b4a6b"/>'
        + '<circle cx="-4" cy="-29" r="2.5" fill="#fff"/><circle cx="4" cy="-29" r="2.5" fill="#fff"/>'
    )


def spider():
    dark = "#5b4a6b"
    leg = ""
    for y0, ky, kx in ((-6, -24, -40), (2, -12, -48), (10, 8, -48), (16, 26, -40)):
        leg += dstroke(f"M-12 {y0}Q{kx + 8} {ky - 12} {kx} {ky}L{kx - 8} {ky + 16}", dark, 4)
    return (
        f'<path d="M0 -66V-24" stroke="{INK}" stroke-width="2"/>'
        + shadow(58, 36)
        + mirror(leg)
        + f'<circle class="k-o" cx="0" cy="4" r="28" fill="{dark}"/>'
        + '<circle cx="-10" cy="-2" r="8" fill="#fff"/><circle cx="10" cy="-2" r="8" fill="#fff"/>'
        + f'<circle cx="-9" cy="-1" r="4" fill="{INK}"/><circle cx="11" cy="-1" r="4" fill="{INK}"/>'
        + cheeks(17, 12, 5, 3)
        + '<path d="M-7 14Q0 20 7 14" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
    )


def snail():
    spiral = "M14 -8C14 -16 26 -16 26 -6C26 6 8 8 4 -4C0 -18 20 -30 32 -18C44 -6 36 16 16 20"
    return (
        shadow(52, 60)
        + '<path class="k-o" d="M58 34Q68 44 54 46H-40C-56 46 -62 36 -60 20C-58 4 -52 -8 -44 -10C-34 -12 -30 -2 -30 8C-28 24 -18 30 0 30Z" fill="#f3d7a6"/>'
        + antennae(-45, -10, 4, 20, "#f3d7a6")
        + f'<circle class="k-o" cx="14" cy="-2" r="34" fill="#f2a65a"/>'
        + f'<path d="{spiral}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + '<path d="M-10 -22Q0 -34 14 -34" ' + SHINE + "/>"
        + f'<circle cx="-50" cy="6" r="3.5" fill="{INK}"/><circle cx="-40" cy="6" r="3.5" fill="{INK}"/>'
        + '<ellipse cx="-52" cy="15" rx="4" ry="2.5" fill="#ff7d93" opacity=".5"/>'
        + f'<path d="M-50 16Q-45 20 -40 16" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
    )


def caterpillar():
    segs = [(-52, 18), (-36, 8), (-20, 2), (-4, 6), (12, 14), (28, 12)]
    body = ""
    for i, (x, y) in enumerate(segs):
        body += (f'<path d="M{x - 3} {y + 14}V{y + 22}M{x + 3} {y + 14}V{y + 22}" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
                 f'<circle class="k-o" cx="{x}" cy="{y}" r="15" fill="{"#7fcf6f" if i % 2 else "#5cc36a"}"/>')
    return (
        shadow(44, 62)
        + body
        + antennae(46, -12, 6, 16, "#ef5b56")
        + '<circle class="k-o" cx="46" cy="4" r="20" fill="#9ee07f"/>'
        + face(46, 2, .9)
    )


def dragonfly():
    wing = lambda rot, y: ell(-26, y, 30, 9, "#d9f2ff", rot, "k-o", 'stroke-width="2.2" opacity=".95"')
    return (
        shadow(58, 40)
        + mirror(wing(12, -14) + wing(-14, 2))
        + f'<path d="M-5 -2L-4 54Q0 60 4 54L5 -2Z" fill="#2fa39a" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        + f'<path d="M-4 14H4M-4 26H4M-4 38H4" stroke="{INK}" stroke-width="2"/>'
        + ell(0, -12, 9, 12, "#2fa39a")
        + '<circle class="k-o" cx="-9" cy="-30" r="10" fill="#6ad1c6"/><circle class="k-o" cx="9" cy="-30" r="10" fill="#6ad1c6"/>'
        + f'<circle cx="-9" cy="-30" r="4" fill="{INK}"/><circle cx="9" cy="-30" r="4" fill="{INK}"/>'
        + f'<path d="M-5 -18Q0 -14 5 -18" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
    )


BUGS = [("bee", bee), ("ant", ant), ("ladybug", ladybug), ("butterfly", butterfly),
        ("spider", spider), ("snail", snail), ("caterpillar", caterpillar), ("dragonfly", dragonfly)]


if __name__ == "__main__":
    import os, build1, build5

    here = os.path.dirname(os.path.abspath(__file__))
    by_word = {w: fn for _L, w, fn in build5.ITEMS}
    old_sea = [("fish", lambda: build1.FISH), ("whale", by_word["whale"]), ("jellyfish", by_word["jellyfish"]), ("turtle", by_word["turtle"])]
    cell = lambda w, fn, old=False: (
        f'<figure><svg viewBox="-82 -68 164 136" xmlns="http://www.w3.org/2000/svg">{fn()}</svg>'
        f"<figcaption>{w}{' <small>(old)</small>' if old else ''}</figcaption></figure>"
    )
    section = lambda title, new, old=(): (
        f"<h2>{title}</h2><div class=grid>" + "".join(cell(w, fn) for w, fn in new) + "".join(cell(w, fn, True) for w, fn in old) + "</div>"
    )
    html = (
        "<!doctype html><meta charset=utf-8><title>Sets preview</title><style>"
        ":root{--ink:#3f3345;--font-sans:Nunito,-apple-system,sans-serif}"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:var(--font-sans);color:var(--ink)}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        "h2{margin:8px 0 12px}.grid{display:grid;grid-template-columns:repeat(5,180px);gap:14px;margin-bottom:18px}"
        "figure{margin:0;background:#fff;border:3px solid var(--ink);border-radius:18px;box-shadow:0 5px 0 var(--ink);padding:8px}"
        "figcaption{text-align:center;font-weight:800;font-size:18px}small{color:#8a7f90;font-weight:600}"
        "</style>"
        + section("Sea animals", SEA, old_sea)
        + section("Vegetables", VEGETABLES)
        + section("Bugs", BUGS)
    )
    out = os.path.join(here, "../../work/sets_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
