"""Word families (phonics): the CVC words that didn't have a picture yet.
Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
from common import INK
from build1 import shadow
from build5 import dstroke, eyes, cheeks, smile, mirror
from build12 import kid, BOY

def face(y=0):
    """Small cute face centered at (0, y)."""
    return eyes(9, y - 2, 4) + cheeks(15, y + 6, 4.5, 3) + smile(y + 6, 5, 4)


# ---------------------------------------------------------------- -at
def bat():
    wing = (
        '<path class="k-o" d="M-12 -8C-26 -26 -52 -34 -74 -24C-68 -16 -66 -8 -68 2'
        'C-60 -2 -52 0 -48 8C-42 2 -34 2 -28 10C-24 4 -18 2 -12 6Z" fill="#6a5a8a"/>'
        '<path d="M-20 -8L-44 -22M-26 2L-58 -14" stroke="#4d4166" stroke-width="2.5" stroke-linecap="round"/>'
    )
    return (
        shadow(56, 30)
        + mirror(wing)
        + mirror('<path class="k-o" d="M-18 -26L-22 -46L-6 -34Z" fill="#7d6c9e"/>')
        + '<ellipse class="k-o" cx="0" cy="4" rx="20" ry="30" fill="#7d6c9e"/>'
        + '<ellipse cx="0" cy="14" rx="11" ry="14" fill="#b3a6cc"/>'
        + face(-10)
        + '<path d="M-3 -4L-2 0L-1 -3.5M1 -3.5L2 0L3 -4" fill="#fff" stroke="#fff" stroke-width="1"/>'
        + mirror(f'<path d="M-8 32L-10 40" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    )


def mat():
    stripes = "".join(
        f'<path d="M{-58 + i * 4} {4 + i * 7}H{58 - i * 4}" stroke="{c}" stroke-width="5"/>'
        for i, c in enumerate(["#ef5b56", "#ffd23f", "#4a9be8", "#5cc36a"])
    )
    fringe = "".join(f'<path d="M{x} 44V52" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>' for x in range(-66, 70, 8))
    fringe += "".join(f'<path d="M{x} -12V-19" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>' for x in range(-46, 50, 8))
    return (
        shadow(52, 70)
        + fringe
        + '<path class="k-o" d="M-50 -12H50L70 44H-70Z" fill="#f2c58e"/>'
        + stripes.replace("M-58 4H58", "M-53 2H53")
        + '<path d="M-44 -4H44L60 36H-60Z" fill="none" stroke="#c98a4b" stroke-width="2.5" stroke-dasharray="6 5"/>'
    )


# ---------------------------------------------------------------- -an
def fan():
    blade = '<path class="k-o" d="M0 0C-6 -10 -8 -24 0 -30C8 -24 6 -10 0 0Z" fill="#8ed1f5" stroke-width="2.5"/>'
    blades = "".join(f'<g transform="translate(0 -18) rotate({a})">{blade}</g>' for a in (0, 120, 240))
    cage = '<path d="M0 -54V18M-36 -18H36" stroke="#9aa3b2" stroke-width="1.5"/>'
    return (
        shadow(58, 40)
        + '<path class="k-o" d="M-8 18H8L10 48H-10Z" fill="#dfe3ea"/>'
        + '<ellipse class="k-o" cx="0" cy="52" rx="34" ry="8" fill="#4a9be8"/>'
        + '<circle class="k-o" cx="0" cy="-18" r="38" fill="#fff"/>'
        + blades
        + cage
        + '<circle cx="0" cy="-18" r="24" fill="none" stroke="#9aa3b2" stroke-width="1.5"/>'
        + '<circle class="k-o" cx="0" cy="-18" r="7" fill="#4a9be8" stroke-width="2.5"/>'
        + '<circle class="k-o" cx="0" cy="-18" r="38" fill="none"/>'
        + '<path d="M50 -40Q58 -30 50 -20M60 -46Q72 -30 60 -14" fill="none" stroke="#8ed1f5" stroke-width="3" stroke-linecap="round"/>'
    )


def pan():
    return (
        shadow(40, 52)
        + dstroke("M34 6L76 -14", "#3f3345", 8)
        + '<path d="M72 -12L78 -15" stroke="#ef5b56" stroke-width="7" stroke-linecap="round"/>'
        + '<path class="k-o" d="M-62 6C-62 30 -40 38 -14 38C12 38 34 30 34 6Z" fill="#555a66"/>'
        + '<ellipse class="k-o" cx="-14" cy="6" rx="48" ry="16" fill="#6f7584"/>'
        + '<ellipse cx="-14" cy="8" rx="38" ry="11" fill="#3f4450"/>'
        + '<path d="M-40 4Q-30 0 -20 0" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".5" fill="none"/>'
    )


# ---------------------------------------------------------------- -en
def hen():
    return (
        shadow(58, 36)
        + "".join(f'<path d="M{x} 38V54M{x} 54L{x - 8} 58M{x} 54L{x + 6} 58" stroke="{INK}" stroke-width="3" stroke-linecap="round" fill="none"/>' for x in (-8, 14))
        + '<path class="k-o" d="M30 -6C38 -30 50 -40 58 -34C60 -22 56 -10 50 0Z" fill="#d9772b"/>'
        + '<path class="k-o" d="M-24 -40C-8 -44 0 -30 0 -14C14 -16 40 -14 48 6C54 30 30 42 6 42C-22 42 -36 26 -36 4C-36 -12 -40 -36 -24 -40Z" fill="#fff"/>'
        + '<path class="k-o" d="M0 8C12 4 28 10 30 22C18 28 6 24 0 8Z" fill="#f2e6d8" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-30 -44C-32 -52 -24 -56 -20 -50C-18 -58 -8 -56 -10 -48C-4 -50 0 -44 -6 -40H-26Z" fill="#ef4f5a" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-36 -28L-48 -24L-36 -20Z" fill="#ffc93c" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-36 -18C-40 -12 -34 -8 -32 -14Z" fill="#ef4f5a" stroke-width="2"/>'
        + f'<circle cx="-24" cy="-30" r="3.5" fill="{INK}"/><circle cx="-23" cy="-31.5" r="1.2" fill="#fff"/>'
        + '<ellipse cx="-18" cy="-20" rx="4" ry="2.5" fill="#ff7d93" opacity=".45"/>'
    )


def pen():
    return (
        shadow(58, 44)
        + '<path d="M-60 46C-44 30 -30 52 -14 40C0 30 10 50 24 40" fill="none" stroke="#2268b0" stroke-width="3.5" stroke-linecap="round"/>'
        + '<g transform="rotate(-40)">'
        + '<path class="k-o" d="M-8 -54H8V26H-8Z" fill="#4a9be8"/>'
        + '<path class="k-o" d="M-8 26H8L4 40H-4Z" fill="#dfe3ea"/>'
        + f'<path d="M-4 40L0 50L4 40Z" fill="{INK}"/>'
        + '<path class="k-o" d="M-9 -60H9V-30H-9Z" fill="#2268b0"/>'
        + '<path class="k-o" d="M9 -56H14V-20Q14 -16 11 -16" fill="none" stroke-width="2.5"/>'
        + '<path d="M-3 -24V20" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".5"/>'
        + "</g>"
    )


# ---------------------------------------------------------------- -ig
def wig():
    back = [(-30, -28), (-14, -40), (0, -44), (14, -40), (30, -28), (-36, -10), (36, -10), (-38, 8), (38, 8), (-34, 24), (34, 24)]
    bangs = [(-20, -24), (-7, -28), (7, -28), (20, -24)]
    curl = lambda x, y, r: f'<circle class="k-o" cx="{x}" cy="{y}" r="{r}" fill="#f78fb3"/>'
    shine = lambda x, y: f'<path d="M{x - 5} {y - 3}Q{x} {y - 8} {x + 5} {y - 3}" fill="none" stroke="#ffc4d9" stroke-width="2.5" stroke-linecap="round"/>'
    return (
        shadow(58, 34)
        + '<ellipse class="k-o" cx="0" cy="54" rx="28" ry="6" fill="#c98a4b"/>'
        + '<rect class="k-o" x="-5" y="28" width="10" height="26" fill="#c98a4b"/>'
        + "".join(curl(x, y, 14) for x, y in back)
        + '<ellipse class="k-o" cx="0" cy="4" rx="22" ry="26" fill="#e8e1d6"/>'
        + "".join(curl(x, y, 10) for x, y in bangs)
        + "".join(shine(x, y) for x, y in back[:5] + bangs)
    )


def dig():
    dirt = '<path class="k-o" d="M10 60C14 36 30 28 44 30C60 30 74 42 78 60Z" fill="#a8704a"/>'
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#7a4a2a"/>' for x, y in ((30, 44), (46, 38), (58, 48), (40, 54), (66, 54)))
    flying = "".join(f'<circle class="k-o" cx="{x}" cy="{y}" r="{r}" fill="#a8704a" stroke-width="2"/>' for x, y, r in ((54, 6, 4), (64, 14, 3), (46, 16, 3)))
    shovel = (
        dstroke("M-4 -24L30 34", "#c98a4b", 5)
        + '<path class="k-o" d="M24 30L40 26L44 44Q38 52 30 48Z" fill="#9aa3b2" stroke-width="2.5"/>'
    )
    body = kid(
        BOY, head=(-34, -36), neck=(-32, -16), hip=(-30, 14), tilt=8,
        arms=([(-32, -12), (-18, -18), (-4, -24)], [(-28, -12), (-6, 2), (14, 10)]),
        legs=([(-32, 14), (-40, 32), (-46, 52)], [(-28, 14), (-18, 32), (-14, 52)]),
        props_mid=shovel,
    )
    return shadow(60, 64) + dirt + dots + flying + body


# ---------------------------------------------------------------- -og
def log():
    rings = "".join(f'<ellipse cx="44" cy="10" rx="{rx}" ry="{ry}" fill="none" stroke="#c98a4b" stroke-width="2"/>' for rx, ry in ((12, 18), (6, 10)))
    bark = "".join(f'<path d="M{x} {y}H{x + w}" stroke="#7a4a2a" stroke-width="2.5" stroke-linecap="round"/>' for x, y, w in ((-50, -4, 30), (-20, 12, 36), (-56, 26, 24), (-6, -10, 22)))
    return (
        shadow(44, 66)
        + '<path class="k-o" d="M-60 -18H44V38H-60C-72 38 -76 24 -76 10C-76 -4 -72 -18 -60 -18Z" fill="#a8704a"/>'
        + bark
        + '<ellipse class="k-o" cx="44" cy="10" rx="18" ry="28" fill="#f2c58e"/>'
        + rings
        + dstroke("M-20 -18C-20 -30 -14 -36 -8 -40", "#5cc36a", 3)
        + '<path class="k-o" d="M-8 -40C0 -50 12 -48 14 -42C6 -36 -2 -36 -8 -40Z" fill="#6cc070" stroke-width="2.5"/>'
    )


def frog():
    eye = '<circle class="k-o" cx="-22" cy="-32" r="15" fill="#6cc070"/><circle cx="-22" cy="-32" r="9" fill="#fff"/>' \
          f'<circle cx="-20" cy="-31" r="5.5" fill="{INK}"/><circle cx="-18" cy="-33" r="2" fill="#fff"/>'
    return (
        shadow(56, 50)
        + mirror('<path class="k-o" d="M-30 28C-54 26 -62 44 -50 52H-20Z" fill="#4fa64f"/>')
        + '<path class="k-o" d="M-46 6C-46 -26 46 -26 46 6C46 40 24 52 0 52C-24 52 -46 40 -46 6Z" fill="#6cc070"/>'
        + '<ellipse cx="0" cy="30" rx="26" ry="18" fill="#c8ecb4"/>'
        + mirror(eye)
        + mirror('<path class="k-o" d="M-20 38L-26 54H-10Z" fill="#4fa64f" stroke-width="2.5"/>')
        + f'<path d="M-24 4Q0 22 24 4" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + cheeks(30, 6, 6, 4)
    )


# ---------------------------------------------------------------- -un
def bun():
    seeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="1.8" fill="#fff5dc" stroke="{INK}" stroke-width="1" transform="rotate({r} {x} {y})"/>' for x, y, r in ((-24, -22, -20), (-6, -32, 10), (14, -30, 30), (30, -16, -30), (-36, -8, 20), (2, -20, -10)))
    return (
        shadow(50, 58)
        + '<path class="k-o" d="M-56 24C-60 -66 60 -66 56 24C56 38 -56 38 -56 24Z" fill="#e0a24a"/>'
        + '<path d="M-42 4C-40 -20 -22 -34 -4 -36" fill="none" stroke="#f7d08a" stroke-width="7" stroke-linecap="round"/>'
        + '<path d="M-54 22C-30 32 30 32 54 22" fill="none" stroke="#c98a4b" stroke-width="3" stroke-linecap="round"/>'
        + seeds
        + face(4)
    )


WORDS = [
    ("bat", bat), ("mat", mat), ("fan", fan), ("pan", pan), ("hen", hen), ("pen", pen),
    ("wig", wig), ("dig", dig), ("log", log), ("frog", frog), ("bun", bun),
]
