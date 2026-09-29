"""Toys. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66.

(ball, kite and yo-yo are already drawn in build1 / build5.)
Run `python3 build18.py` to preview them next to those in work/toys_preview.html.
"""
import math
from common import INK, fmt
from build1 import shadow
from build5 import eyes, cheeks, smile, mirror, star, dstroke

GLASS = "#cdeeff"
WOOD, WOOD_DARK = "#c98a4b", "#a86c34"
SHINE = 'fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" opacity=".6"'


# ---------------------------------------------------------------- teddy bear
def teddy_bear():
    fur, light = "#c98a4b", "#f3c89a"
    ear = f'<circle class="k-o" cx="-24" cy="-48" r="11" fill="{fur}"/><circle cx="-24" cy="-48" r="5.5" fill="{light}"/>'
    arm = f'<ellipse class="k-o" cx="-33" cy="16" rx="11" ry="18" fill="{fur}" transform="rotate(28 -33 16)"/>'
    leg = (
        f'<ellipse class="k-o" cx="-20" cy="46" rx="15" ry="11" fill="{fur}"/>'
        f'<ellipse cx="-22" cy="47" rx="7" ry="6" fill="{light}"/>'
    )
    return (
        shadow(58, 42)
        + mirror(leg)
        + f'<ellipse class="k-o" cx="0" cy="22" rx="30" ry="27" fill="{fur}"/>'
        + f'<ellipse cx="0" cy="26" rx="17" ry="15" fill="{light}"/>'
        + mirror(arm)
        + mirror(ear)
        + f'<circle class="k-o" cx="0" cy="-24" r="28" fill="{fur}"/>'
        + f'<ellipse class="k-o" cx="0" cy="-13" rx="13" ry="10" fill="{light}" stroke-width="2.5"/>'
        + f'<ellipse cx="0" cy="-17" rx="5" ry="3.5" fill="{INK}"/>'
        + f'<path d="M0 -14V-9M-5 -7Q0 -4 5 -7" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + eyes(11, -30, 4.5)
        # bow tie
        + f'<path class="k-o" d="M0 4L-15 -4V12ZM0 4L15 -4V12Z" fill="#ef5b56" stroke-width="2.5"/>'
        + f'<circle cx="0" cy="4" r="4" fill="#ef5b56" stroke="{INK}" stroke-width="2.5"/>'
    )


# ---------------------------------------------------------------- doll
def doll():
    skin, hair, dress = "#ffd2b0", "#ef8a3a", "#b784e6"
    pigtail = (
        f'<circle class="k-o" cx="-31" cy="-24" r="11" fill="{hair}"/>'
        f'<path class="k-o" d="M-36 -34L-44 -39V-29ZM-36 -34L-28 -39V-29Z" fill="#ff7d93" stroke-width="2.2"/>'
    )
    arm = f'<path d="M-18 4Q-30 16 -34 30" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>' \
          f'<path d="M-18 4Q-30 16 -34 30" fill="none" stroke="{skin}" stroke-width="6" stroke-linecap="round"/>'
    leg = (
        f'<rect class="k-o" x="-15" y="34" width="10" height="18" fill="#fff" stroke-width="2.5"/>'
        f'<path d="M-15 40H-5M-15 46H-5" stroke="#ef5b56" stroke-width="3"/>'
        f'<path class="k-o" d="M-18 52H-3Q-2 60 -8 60H-18Q-22 56 -18 52Z" fill="{INK}" stroke-width="2"/>'
    )
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#fff"/>' for x, y in ((-10, 14), (8, 10), (0, 24), (-16, 28), (14, 26)))
    return (
        shadow(60, 30)
        + mirror(arm)
        + mirror(leg)
        + f'<path class="k-o" d="M-12 -4H12L26 38Q0 44 -26 38Z" fill="{dress}"/>'
        + dots
        + f'<path class="k-o" d="M-12 -4Q0 6 12 -4L8 -8H-8Z" fill="#fff" stroke-width="2.2"/>'
        + mirror(pigtail)
        + f'<circle class="k-o" cx="0" cy="-26" r="23" fill="{skin}"/>'
        + f'<path class="k-o" d="M-24 -26C-28 -60 28 -60 24 -26C16 -38 8 -40 0 -33C-8 -40 -16 -38 -24 -26Z" fill="{hair}"/>'
        # button eyes and a stitched smile
        + f'<circle cx="-9" cy="-24" r="4.5" fill="{INK}"/><circle cx="9" cy="-24" r="4.5" fill="{INK}"/>'
        + '<path d="M-10.5 -25.5H-7.5M10.5 -25.5H7.5" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>'
        + cheeks(15, -16, 4.5, 3)
        + f'<path d="M-7 -14Q0 -8 7 -14" fill="none" stroke="#c0392b" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="3 2.5"/>'
    )


# ---------------------------------------------------------------- robot
def robot():
    body, face, dark = "#4a9be8", "#c9d6e6", "#2f6fb4"
    arm = (
        f'<path d="M-32 6Q-46 10 -48 26" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
        f'<path d="M-32 6Q-46 10 -48 26" fill="none" stroke="{face}" stroke-width="5" stroke-linecap="round"/>'
        f'<path class="k-o" d="M-56 30A9 9 0 1 1 -40 30" fill="none" stroke-width="4"/>'
    )
    leg = (
        f'<rect class="k-o" x="-19" y="40" width="12" height="10" fill="{face}" stroke-width="2.5"/>'
        f'<rect class="k-o" x="-24" y="49" width="22" height="9" rx="4" fill="{dark}" stroke-width="2.5"/>'
    )
    ear = f'<rect class="k-o" x="-34" y="-40" width="8" height="16" rx="2" fill="#ef5b56" stroke-width="2.5"/>'
    return (
        shadow(60, 40)
        + mirror(leg)
        + mirror(arm)
        + f'<rect class="k-o" x="-32" y="-6" width="64" height="48" rx="9" fill="{body}"/>'
        + f'<rect class="k-o" x="-20" y="2" width="40" height="28" rx="5" fill="{face}" stroke-width="2.5"/>'
        + f'<circle cx="-10" cy="10" r="4" fill="#ef5b56" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="0" cy="10" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="10" cy="10" r="4" fill="#5cc36a" stroke="{INK}" stroke-width="2"/>'
        + f'<path d="M-12 22H12" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="3 3"/>'
        + f'<rect class="k-o" x="-8" y="-12" width="16" height="8" fill="{face}" stroke-width="2.5"/>'
        + f'<path d="M0 -50V-58" stroke="{INK}" stroke-width="3"/>'
        + f'<circle cx="0" cy="-60" r="5" fill="#ef5b56" stroke="{INK}" stroke-width="2.5"/>'
        + mirror(ear)
        + f'<rect class="k-o" x="-28" y="-50" width="56" height="40" rx="10" fill="{face}"/>'
        + f'<circle cx="-11" cy="-34" r="8" fill="#ffd23f" stroke="{INK}" stroke-width="2.5"/>'
        + f'<circle cx="11" cy="-34" r="8" fill="#ffd23f" stroke="{INK}" stroke-width="2.5"/>'
        + f'<circle cx="-10" cy="-34" r="3.5" fill="{INK}"/><circle cx="12" cy="-34" r="3.5" fill="{INK}"/>'
        + f'<rect x="-10" y="-23" width="20" height="6" rx="3" fill="{INK}"/>'
        + '<path d="M-5 -23V-17M0 -23V-17M5 -23V-17" stroke="#fff" stroke-width="1.5"/>'
        + '<path d="M-22 -44H-6" ' + SHINE + "/>"
    )


# ---------------------------------------------------------------- blocks
def block(x, y, s, face, top, side, letter):
    d = 10
    return (
        f'<path class="k-o" d="M{x} {y}L{x + d} {y - d}H{x + s + d}L{x + s} {y}Z" fill="{top}" stroke-width="2.5"/>'
        f'<path class="k-o" d="M{x + s} {y}L{x + s + d} {y - d}V{y + s - d}L{x + s} {y + s}Z" fill="{side}" stroke-width="2.5"/>'
        f'<rect class="k-o" x="{x}" y="{y}" width="{s}" height="{s}" rx="3" fill="{face}"/>'
        f'<rect x="{x + 5}" y="{y + 5}" width="{s - 10}" height="{s - 10}" rx="3" fill="none" stroke="#fff" stroke-width="2.5" opacity=".7"/>'
        f'<text class="k-f" x="{x + s / 2}" y="{y + s / 2 + 11}" font-size="31" font-weight="800" text-anchor="middle" '
        f'fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{letter}</text>'
    )


def blocks():
    s = 44
    return (
        shadow(58, 62)
        + block(-54, 10, s, "#ef5b56", "#ff8a80", "#c9403b", "A")
        + block(2, 10, s, "#4a9be8", "#8ec5ff", "#2f6fb4", "C")
        + block(-26, -36, s, "#ffc93c", "#ffe08a", "#e0a800", "B")
    )


# ---------------------------------------------------------------- drum
def drum():
    rx, ry, top, bot = 46, 14, -18, 30
    rim = lambda y: f'M{-rx} {y}A{rx} {ry} 0 0 0 {rx} {y}V{y + 8}A{rx} {ry} 0 0 1 {-rx} {y + 8}Z'
    arc_y = lambda x, y: y + ry * math.sqrt(max(0, 1 - (x / rx) ** 2))
    xs = [-38, -19, 0, 19, 38]
    zig = "M" + "L".join(
        f"{fmt(x)} {fmt(arc_y(x, top + 8) if i % 2 == 0 else arc_y(x, bot))}" for i, x in enumerate(xs)
    )
    stick = lambda a, b: dstroke(f"M{a[0]} {a[1]}L{b[0]} {b[1]}", WOOD, 5) + f'<circle cx="{b[0]}" cy="{b[1]}" r="6" fill="#fff4e0" stroke="{INK}" stroke-width="2.5"/>'
    return (
        shadow(48, 54)
        + f'<path class="k-o" d="M{-rx} {top}V{bot + 8}A{rx} {ry} 0 0 0 {rx} {bot + 8}V{top}Z" fill="#ef5b56"/>'
        + f'<path d="{zig}" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
        + f'<path class="k-o" d="{rim(top)}" fill="#ffd23f" stroke-width="2.5"/>'
        + f'<path class="k-o" d="{rim(bot)}" fill="#ffd23f" stroke-width="2.5"/>'
        + f'<ellipse class="k-o" cx="0" cy="{top}" rx="{rx}" ry="{ry}" fill="#fff4e0"/>'
        + f'<path d="M-38 6V22" {SHINE}/>'
        + stick((-50, -58), (8, -22))
        + stick((52, -52), (-10, -18))
    )


# ---------------------------------------------------------------- balloon
BALLOON = "M0 -27C16 -27 22 -12 22 -2C22 14 10 25 0 27C-10 25 -22 14 -22 -2C-22 -12 -16 -27 0 -27Z"


def one_balloon(x, y, rot, color):
    return (
        f'<g transform="translate({x} {y}) rotate({rot})">'
        f'<path class="k-o" d="M-4 32L0 26L4 32Z" fill="{color}" stroke-width="2.2"/>'
        f'<path class="k-o" d="{BALLOON}" fill="{color}"/>'
        f'<path d="M-12 -12Q-10 -20 -3 -22" {SHINE}/>'
        "</g>"
    )


def balloon():
    # each string starts at its balloon's knot (32 below the middle, turned with the balloon)
    knots = [(-28 + 32 * math.sin(math.radians(14)), -26 + 32 * math.cos(math.radians(14))), (0, -4),
             (28 - 32 * math.sin(math.radians(14)), -26 + 32 * math.cos(math.radians(14)))]
    strings = "".join(
        f'<path d="M{fmt(x)} {fmt(y)}Q{fmt(x * .2 - 4)} {fmt(y + 28)} 0 50" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        for x, y in knots
    )
    return (
        strings
        + one_balloon(0, -36, 0, "#ef5b56")
        + one_balloon(-28, -26, -14, "#4a9be8")
        + one_balloon(28, -26, 14, "#ffc93c")
        + f'<path class="k-o" d="M0 50L-11 44V58ZM0 50L11 44V58Z" fill="#5cc36a" stroke-width="2.2"/>'
        + f'<circle cx="0" cy="50" r="3.5" fill="#5cc36a" stroke="{INK}" stroke-width="2.2"/>'
    )


# ---------------------------------------------------------------- puzzle
def piece_path(x, y, s, edges):
    """A jigsaw piece: square at (x, y) of side s; edges (top, right, bottom, left) are 1 tab out, -1 slot in, 0 flat."""
    corners = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
    normals = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    out = [f"M{fmt(x)} {fmt(y)}"]
    for i, t in enumerate(edges):
        (ax, ay), (bx, by) = corners[i], corners[(i + 1) % 4]
        nx, ny = normals[i]
        at = lambda f, h=0: (ax + (bx - ax) * f + nx * h * t, ay + (by - ay) * f + ny * h * t)
        if t:
            p1, c1, c2, p2 = at(.36), at(.12, 17), at(.88, 17), at(.64)
            out.append(f"L{fmt(p1[0])} {fmt(p1[1])}C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}")
        out.append(f"L{fmt(bx)} {fmt(by)}")
    return "".join(out) + "Z"


def puzzle():
    s, x0, y0 = 42, -52, -40
    piece = lambda gx, gy, edges, color, extra="": (
        f'<path class="k-o" d="{piece_path(x0 + gx * s, y0 + gy * s, s, edges)}" fill="{color}" {extra}/>'
    )
    # the fourth piece has been lifted out, leaving its slot
    lifted = piece(1, 1, (-1, 0, 0, 1), "#5cc36a", 'transform="translate(26 14) rotate(14 11 23)"')
    return (
        shadow(56, 62)
        + piece(1, 1, (-1, 0, 0, 1), "#efe7d6", 'stroke-dasharray="5 4" stroke-width="2.5"')
        + piece(0, 0, (0, 1, -1, 0), "#ef5b56")
        + piece(1, 0, (0, 0, 1, -1), "#ffc93c")
        + piece(0, 1, (1, -1, 0, 0), "#4a9be8")
        + f'<path d="M{x0 + 8} {y0 + 12}Q{x0 + 10} {y0 + 6} {x0 + 18} {y0 + 5}" {SHINE}/>'
        + lifted
        + f'<path d="M66 -4L72 -10M70 8H78" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


# ---------------------------------------------------------------- rocket
def rocket():
    fin = f'<path class="k-o" d="M-18 8Q-36 16 -38 40L-19 32Z" fill="#ef5b56"/>'
    return (
        star(-54, -38, 8) + star(56, -50, 6, "#8ec5ff") + star(-60, 30, 5, "#ff7d93")
        + '<g transform="rotate(16)">'
        + f'<path class="k-o" d="M-10 38Q-14 54 0 64Q14 54 10 38Z" fill="#ff9a3c"/>'
        + '<path d="M-5 38Q-6 50 0 56Q6 50 5 38Z" fill="#ffd23f"/>'
        + mirror(fin)
        + f'<path class="k-o" d="M0 -60C22 -44 24 -10 20 34H-20C-24 -10 -22 -44 0 -60Z" fill="#f4f1ea"/>'
        + f'<path class="k-o" d="M0 -60C12 -52 17 -42 19 -34Q0 -28 -19 -34C-17 -42 -12 -52 0 -60Z" fill="#ef5b56"/>'
        + f'<rect class="k-o" x="-14" y="30" width="28" height="9" rx="3" fill="#8a7f90" stroke-width="2.5"/>'
        + f'<circle cx="0" cy="-6" r="12" fill="#4a9be8" stroke="{INK}" stroke-width="3"/>'
        + f'<circle cx="0" cy="-6" r="7" fill="{GLASS}"/>'
        + '<path d="M-4 -9Q-3 -12 0 -12" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'
        + '<path d="M-14 14V24" ' + SHINE + "/>"
        + "</g>"
    )


TOYS = [
    ("teddy bear", teddy_bear), ("doll", doll), ("robot", robot), ("blocks", blocks),
    ("drum", drum), ("balloon", balloon), ("puzzle", puzzle), ("rocket", rocket),
]


if __name__ == "__main__":
    import os, build1, build5

    here = os.path.dirname(os.path.abspath(__file__))
    old = [("ball", build1.ball), ("kite", build5.kite), ("yo-yo", build5.yoyo)]
    cell = lambda w, fn, tag="": (
        f'<figure><svg viewBox="-82 -68 164 136" xmlns="http://www.w3.org/2000/svg">{fn()}</svg>'
        f"<figcaption>{w}{tag}</figcaption></figure>"
    )
    html = (
        "<!doctype html><meta charset=utf-8><title>Toys preview</title><style>"
        ":root{--ink:#3f3345;--font-sans:Nunito,-apple-system,sans-serif}"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:var(--font-sans);color:var(--ink)}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        ".k-f{font-family:var(--font-sans);font-weight:500}"
        "h2{margin:8px 0 12px}.grid{display:grid;grid-template-columns:repeat(4,200px);gap:16px}"
        "figure{margin:0;background:#fff;border:3px solid var(--ink);border-radius:18px;box-shadow:0 5px 0 var(--ink);padding:10px}"
        "figcaption{text-align:center;font-weight:800;font-size:20px}small{color:#8a7f90;font-weight:600}"
        "</style>"
        "<h2>New toys</h2><div class=grid>" + "".join(cell(w, fn) for w, fn in TOYS) + "</div>"
        "<h2>Already drawn</h2><div class=grid>" + "".join(cell(w, fn, " <small>(old)</small>") for w, fn in old) + "</div>"
    )
    out = os.path.join(here, "../../work/toys_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
