"""Zoo animals (the Pre A1 Starters ones the other lessons don't have). Each drawing is centered on (0,0),
roughly within x -80..80, y -66..66. The furry ones are faces, like the lion in build5.

Run `python3 build22.py` to preview them next to the lion, zebra and elephant in work/zoo_preview.html.
"""
from common import INK
from build1 import shadow
from build4 import union, circ
from build5 import eyes, cheeks, smile, mirror, dstroke

SHINE = 'fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" opacity=".6"'


def ell(cx, cy, rx, ry, fill, rot=0, cls="k-o", extra=""):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    c = f' class="{cls}"' if cls else ""
    return f'<ellipse{c} cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{t} {extra}/>'


def nose_mouth(y, fill="#5a3a2a", w=6):
    """A little triangle nose and a w-shaped mouth under it, as on the lion."""
    return (
        f'<path d="M{-w} {y}L{w} {y}L0 {y + 6}Z" fill="{fill}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="M0 {y + 6}C0 {y + 12} -6 {y + 14} -9 {y + 10}M0 {y + 6}C0 {y + 12} 6 {y + 14} 9 {y + 10}" '
        f'fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def monkey():
    fur, face = "#9a6a44", "#f3d3a8"
    ear = ell(-38, -2, 14, 15, fur) + ell(-38, -2, 8, 9, face, cls="")
    mask = union([circ(-12, -8, 17), circ(12, -8, 17), ("ellipse", 'cx="0" cy="14" rx="27" ry="20"')], face, sw=1.5)
    return (
        shadow(60, 42)
        + mirror(ear)
        + '<circle class="k-o" cx="0" cy="0" r="38" fill="' + fur + '"/>'
        + f'<path d="M-6 -38Q0 -50 8 -38" fill="{fur}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        + mask
        + eyes(11, -9, 4.8)
        + f'<ellipse cx="-4" cy="8" rx="2.2" ry="3" fill="{INK}"/><ellipse cx="4" cy="8" rx="2.2" ry="3" fill="{INK}"/>'
        + smile(18, 10, 7)
        + cheeks(22, 12, 5, 3)
    )


def giraffe():
    yellow, spot, dark = "#ffc93c", "#d98e3a", "#8b5a3c"
    neck = f'<path class="k-o" d="M-22 66L-12 -8L14 -8L20 66Z" fill="{yellow}"/>'
    spots = "".join(
        f'<path d="{d}" fill="{spot}"/>'
        for d in ("M-12 44L-2 38L4 48L-4 58L-14 56Z", "M4 18L14 14L16 28L6 32Z", "M-10 8L-2 4L0 16L-10 20Z",
                  "M8 50L16 46L18 60L8 62Z")
    )
    horn = f'<path d="M-6 -44L-8 -58" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>' \
           f'<path d="M-6 -44L-8 -58" stroke="{dark}" stroke-width="3" stroke-linecap="round"/>' \
           f'<circle class="k-o" cx="-8" cy="-60" r="5" fill="{dark}" stroke-width="2.5"/>'
    return (
        shadow(64, 30)
        + neck
        + spots
        + horn
        + f'<g transform="translate(16 0)">{horn}</g>'
        + ell(-24, -36, 11, 6, yellow, -25)
        + ell(26, -36, 11, 6, yellow, 25)
        + ell(0, -28, 26, 22, yellow)
        + ell(0, -6, 20, 14, "#ffe6a3")
        + f'<circle cx="-18" cy="-34" r="5" fill="{spot}"/><circle cx="18" cy="-38" r="4" fill="{spot}"/>'
        + eyes(11, -30, 4.5)
        + f'<ellipse cx="-6" cy="-6" rx="2.2" ry="3" fill="{INK}"/><ellipse cx="6" cy="-6" rx="2.2" ry="3" fill="{INK}"/>'
        + smile(1, 8, 5)
        + cheeks(19, -20, 5, 3)
    )


def tiger():
    orange, white, stripe = "#ff9a3c", "#fff4e6", INK
    ear = ell(-28, -28, 12, 12, orange) + ell(-28, -28, 6, 6, "#ffd1a8", cls="")
    stripes = (
        f'<path d="M-8 -36L-4 -26M0 -38V-26M8 -36L4 -26" fill="none" stroke="{stripe}" stroke-width="3.5" stroke-linecap="round"/>'
        + mirror(f'<path d="M-36 -6H-26M-37 4H-27" fill="none" stroke="{stripe}" stroke-width="3.5" stroke-linecap="round"/>')
    )
    return (
        shadow(60, 44)
        + mirror(ear)
        + '<circle class="k-o" cx="0" cy="0" r="38" fill="' + orange + '"/>'
        + mirror(ell(-10, 14, 14, 11, white, cls=""))
        + ell(0, 22, 9, 7, white, cls="")
        + stripes
        + eyes(13, -8, 5.2)
        + nose_mouth(9, "#f07a8a")
        + cheeks(24, 6, 5, 3)
    )


def hippo():
    grey, snout, pink = "#a79cc9", "#c7bde6", "#ff9fb0"
    eye_bump = ell(-18, -40, 12, 11, grey)
    ear = ell(-34, -34, 7, 5, grey, -30) + ell(-34, -34, 3.5, 2.5, pink, -30, cls="")
    return (
        shadow(62, 48)
        + mirror(ear)
        + mirror(eye_bump)
        + ell(0, -12, 40, 28, grey)
        + ell(0, 22, 46, 30, snout)
        + f'<circle cx="-18" cy="-42" r="5" fill="{INK}"/><circle cx="18" cy="-42" r="5" fill="{INK}"/>'
        + '<circle cx="-16.2" cy="-44" r="1.9" fill="#fff"/><circle cx="19.8" cy="-44" r="1.9" fill="#fff"/>'
        + mirror(ell(-14, 10, 4, 6, "#7f73a3", cls=""))
        + f'<path d="M-24 32Q0 44 24 32" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + mirror(f'<rect x="-14" y="35" width="7" height="8" rx="2" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
        + cheeks(32, 16, 6, 3.5)
    )


def bear_face(fur, inner, muzzle, nose):
    ear = ell(-30, -30, 14, 14, fur) + ell(-30, -30, 7, 7, inner, cls="")
    return (
        mirror(ear)
        + '<circle class="k-o" cx="0" cy="0" r="38" fill="' + fur + '"/>'
        + ell(0, 14, 19, 14, muzzle, cls="k-o", extra='stroke-width="2"')
        + eyes(14, -8, 5)
        + f'<ellipse cx="0" cy="7" rx="7" ry="5" fill="{nose}"/><ellipse cx="-2" cy="5.5" rx="2.2" ry="1.3" fill="#fff" opacity=".6"/>'
        + f'<path d="M0 12V16M0 16C-2 22 -8 22 -9 18M0 16C2 22 8 22 9 18" fill="none" stroke="{INK}" stroke-width="2.3" stroke-linecap="round"/>'
        + cheeks(25, 6, 5, 3)
    )


def bear():
    return shadow(60, 42) + bear_face("#a0693f", "#d9a877", "#e8c49a", INK)


def polar_bear():
    # the same face in white, sitting on a floe of ice so it doesn't read as a brown bear drawn pale
    ice = f'<path class="k-o" d="M-60 46L-44 32H46L62 44L54 60H-52Z" fill="#dff1fc"/>' \
          f'<path d="M-40 40H-16M20 40H36" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
    return ice + f'<g transform="translate(0 -6)">{bear_face("#fbfaf6", "#e3dde4", "#fff", INK)}</g>'


def crocodile():
    green, belly, dark = "#6cc070", "#c9e9a8", "#4f8a3a"
    body = ("M-74 6C-74 -6 -60 -10 -44 -10L-30 -14C-24 -26 -12 -26 -8 -14C10 -18 34 -16 50 -8"
            "C62 -2 70 -8 78 -20C80 -4 70 10 52 12C30 18 0 18 -20 14L-44 14C-60 14 -74 14 -74 6Z")
    ridges = "".join(f'<path class="k-o" d="M{x} {y}l5 -9l5 9" fill="{dark}" stroke-width="2.2"/>'
                     for x, y in ((0, -16), (14, -16), (28, -14), (42, -10)))
    legs = "".join(f'<path class="k-o" d="M{x} 12l-4 18h14l-2 -18" fill="{green}" stroke-width="2.5"/>' for x in (-24, 26))
    teeth = "".join(f'<path d="M{x} 6l3 5l3 -5" fill="#fff" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
                    for x in (-68, -60, -52, -44))
    return (
        shadow(46, 64)
        + legs
        + ridges
        + f'<path class="k-o" d="{body}" fill="{green}"/>'
        + f'<path d="M-44 12C-20 16 20 16 48 10C20 12 -20 12 -44 12Z" fill="{belly}"/>'
        + f'<path d="M-72 4H-40" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + teeth
        + f'<circle cx="-70" cy="-3" r="1.8" fill="{INK}"/>'
        + f'<circle cx="-19" cy="-20" r="5" fill="{INK}"/><circle cx="-17.5" cy="-22" r="2" fill="#fff"/>'
        + ell(-28, -4, 5, 3, "#ff7d93", cls="", extra='opacity=".45"')
        + f'<path d="M-4 -8Q12 -12 30 -8" {SHINE}/>'
    )


def snake():
    body, spot = "#9bd35a", "#5e9a2e"
    coil = "M-50 48C-60 30 -30 22 0 26C34 30 58 36 48 50C38 62 -40 62 -50 48Z"
    neck = "M10 28C30 20 30 0 14 -12C2 -20 -4 -30 4 -40"
    spots = "".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{spot}"/>' for x, y in ((-30, 34), (-6, 30), (22, 36), (-36, 52), (2, 56), (30, 52)))
    return (
        shadow(60, 58)
        + f'<path class="k-o" d="{coil}" fill="{body}"/>'
        + f'<path d="M-40 44C-20 36 20 38 40 46" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" opacity=".5"/>'
        + spots
        + dstroke(neck, body, 16)
        + f'<path d="M26 -4L30 4M16 14L22 20" stroke="{spot}" stroke-width="3" stroke-linecap="round"/>'
        + f'<path d="M6 -58L10 -66M6 -58L2 -66M6 -58V-50" stroke="#ef5b56" stroke-width="2.5" stroke-linecap="round"/>'
        + ell(4, -42, 17, 13, body)
        + eyes(7, -46, 4)
        + f'<g transform="translate(4 0)">{smile(-38, 6, 4)}</g>'
        + cheeks(12, -40, 4, 2.5).replace('cx="-12"', 'cx="-8"').replace('cx="12"', 'cx="16"')
    )


def lizard():
    green, light = "#4fc1a5", "#a8e6d4"
    tail = "M30 8C54 12 70 0 64 -16C60 -28 44 -26 46 -14C48 -6 56 -8 56 -14"
    legs = "".join(
        f'<path d="M{x} {y0}L{x + dx} {y0 + 16}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M{x} {y0}L{x + dx} {y0 + 16}" stroke="{green}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M{x + dx - 5} {y0 + 18}h10" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        for x, dx, y0 in ((-30, -8, 8), (-18, 6, 10), (10, -6, 10), (22, 8, 8))
    )
    return (
        shadow(40, 56)
        + legs
        + dstroke(tail, green, 12)
        + ell(-2, 2, 36, 14, green)
        + f'<path d="M-24 -2Q-2 -8 22 -2" fill="none" stroke="{light}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 9"/>'
        + ell(-44, -6, 20, 14, green, -10)
        + f'<circle cx="-48" cy="-12" r="4.5" fill="{INK}"/><circle cx="-46.5" cy="-13.8" r="1.8" fill="#fff"/>'
        + f'<path d="M-62 -2Q-54 4 -44 0" fill="none" stroke="{INK}" stroke-width="2.3" stroke-linecap="round"/>'
        + ell(-38, -2, 4, 2.5, "#ff7d93", cls="", extra='opacity=".45"')
    )


ZOO = [("monkey", monkey), ("giraffe", giraffe), ("tiger", tiger), ("hippo", hippo), ("crocodile", crocodile),
       ("snake", snake), ("bear", bear), ("polar bear", polar_bear), ("lizard", lizard)]


if __name__ == "__main__":
    import os, build5

    here = os.path.dirname(os.path.abspath(__file__))
    by_word = {w: fn for _L, w, fn in build5.ITEMS}
    old = [("lion", by_word["lion"]), ("zebra", by_word["zebra"])]
    cell = lambda w, fn, was=False: (
        f'<figure><svg viewBox="-82 -68 164 136" xmlns="http://www.w3.org/2000/svg">{fn()}</svg>'
        f"<figcaption>{w}{' <small>(old)</small>' if was else ''}</figcaption></figure>"
    )
    html = (
        "<!doctype html><meta charset=utf-8><title>Zoo preview</title><style>"
        ":root{--ink:#3f3345;--font-sans:Nunito,-apple-system,sans-serif}"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:var(--font-sans);color:var(--ink)}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        ".grid{display:grid;grid-template-columns:repeat(4,180px);gap:14px}"
        "figure{margin:0;background:#fff;border:3px solid var(--ink);border-radius:18px;box-shadow:0 5px 0 var(--ink);padding:8px}"
        "figcaption{text-align:center;font-weight:800;font-size:18px}small{color:#8a7f90;font-weight:600}"
        "</style><div class=grid>"
        + "".join(cell(w, fn) for w, fn in ZOO)
        + "".join(cell(w, fn, True) for w, fn in old)
        + "</div>"
    )
    out = os.path.join(here, "../../work/zoo_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
