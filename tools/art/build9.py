"""Vehicles and clothes. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
from common import INK, fmt
from build1 import shadow
from build4 import union, circ
from build5 import dstroke

GLASS = "#cdeeff"
SHINE = 'fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"'


def wheel(x, y=20, r=13):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x}" cy="{y}" r="{fmt(r * .42)}" fill="#c9c2cc"/>'


def light(x, y, fill="#ffd23f"):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>'


# ================================================================ vehicles
def car():
    body = "M-62 20V4Q-62 -8 -50 -10L-34 -12L-20 -34Q-16 -38 -10 -38H18Q24 -38 28 -32L40 -12L54 -10Q64 -8 64 4V20Z"
    return (
        shadow(34, 60)
        + f'<path class="k-o" d="{body}" fill="#ef5b56"/>'
        + f'<path class="k-o" d="M-26 -14L-15 -31H0V-14Z" fill="{GLASS}" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M6 -31H18Q21 -31 23 -28L32 -14H6Z" fill="{GLASS}" stroke-width="2.5"/>'
        + f'<path d="M3 -10V16M10 -4H15" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        + '<path d="M-54 -2H52" ' + SHINE + "/>"
        + light(58, 0) + light(-58, 2, "#ef4f5a")
        + wheel(-36) + wheel(38)
    )


def bus():
    windows = "".join(
        f'<rect class="k-o" x="{x}" y="-32" width="20" height="18" rx="3" fill="{GLASS}" stroke-width="2.5"/>' for x in (-58, -32, -6, 20)
    )
    return (
        shadow(36, 64)
        + '<rect class="k-o" x="-66" y="-42" width="132" height="64" rx="10" fill="#ffc93c"/>'
        + '<rect x="-64.5" y="0" width="129" height="7" fill="#ef5b56"/>'
        + windows
        + f'<path class="k-o" d="M46 -32H58Q62 -32 62 -28V-6H46Z" fill="{GLASS}" stroke-width="2.5"/>'
        + f'<path d="M48 -2V20" stroke="{INK}" stroke-width="2"/>'
        + light(60, 12) + light(-62, 12, "#ef4f5a")
        + wheel(-40, 22) + wheel(40, 22)
    )


def truck():
    return (
        shadow(36, 64)
        + f'<rect x="-64" y="12" width="126" height="9" rx="2" fill="{INK}"/>'
        + '<rect class="k-o" x="-66" y="-46" width="82" height="58" rx="4" fill="#ff9a3c"/>'
        + '<path d="M-56 -36V2M-40 -36V2M-24 -36V2M-8 -36V2" stroke="#e07b1f" stroke-width="3" stroke-linecap="round"/>'
        + '<path class="k-o" d="M22 14V-24Q22 -30 28 -30H44Q50 -30 54 -22L62 -6Q64 -2 64 4V14Z" fill="#4a9be8"/>'
        + f'<path class="k-o" d="M29 -24H43Q46 -24 48 -20L54 -8H29Z" fill="{GLASS}" stroke-width="2.5"/>'
        + light(60, 6)
        + wheel(-46, 22, 12) + wheel(-20, 22, 12) + wheel(44, 22, 12)
    )


def train():
    smoke = union([circ(34, -52, 8), circ(46, -58, 7), circ(56, -62, 5)], "#f2f2f5", 2.5)
    return (
        shadow(40, 64)
        + smoke
        + '<path class="k-o" d="M17 -20L13 -44H33L29 -20Z" fill="#3f3345"/>'
        + '<rect class="k-o" x="-30" y="-22" width="72" height="36" rx="8" fill="#5cc36a"/>'
        + '<path d="M-10 -20V12M14 -20V12" stroke="#3f9e4d" stroke-width="4"/>'
        + '<rect class="k-o" x="-62" y="-42" width="36" height="56" rx="4" fill="#ef5b56"/>'
        + '<rect class="k-o" x="-67" y="-50" width="46" height="9" rx="3" fill="#3f3345"/>'
        + f'<rect class="k-o" x="-54" y="-34" width="20" height="16" rx="3" fill="{GLASS}" stroke-width="2.5"/>'
        + '<path class="k-o" d="M42 -2L56 20H42Z" fill="#ffd23f"/>'
        + light(46, -12)
        + f'<rect x="-64" y="12" width="106" height="7" rx="2" fill="{INK}"/>'
        + wheel(-44, 22, 15) + wheel(-4, 26, 11) + wheel(24, 26, 11)
    )


def plane():
    body = "M-62 -12Q-58 -16 -44 -16H38Q60 -16 66 -2Q62 12 40 12H-44Q-56 12 -62 -12Z"
    portholes = "".join(f'<circle cx="{x}" cy="-4" r="4" fill="{GLASS}" stroke="{INK}" stroke-width="2"/>' for x in range(-30, 31, 12))
    return (
        '<g transform="translate(-2 6)">'
        + '<path class="k-o" d="M-4 -16L-22 -40H-10L14 -16Z" fill="#2f7cc6"/>'
        + '<path class="k-o" d="M-58 -14L-66 -44H-54L-36 -16Z" fill="#ef5b56"/>'
        + f'<path class="k-o" d="{body}" fill="#fff"/>'
        + '<path d="M-56 4Q-50 8 -44 8H44Q54 8 60 4" fill="none" stroke="#4a9be8" stroke-width="5"/>'
        + f'<path class="k-o" d="{body}" fill="none"/>'
        + portholes
        + f'<path class="k-o" d="M44 -12H52Q58 -10 60 -4H44Z" fill="{GLASS}" stroke-width="2"/>'
        + '<path class="k-o" d="M-8 2L-30 38H-16L16 2Z" fill="#4a9be8"/>'
        + "</g>"
    )


def boat():
    waves = "M-70 40Q-60 32 -50 40T-30 40T-10 40T10 40T30 40T50 40T70 40V50H-70Z"
    return (
        dstroke("M0 12V-60", "#8b5a3c", 4)
        + '<path class="k-o" d="M5 -56L5 4H52Z" fill="#fff"/>'
        + '<path d="M12 -38L12 -4H38" fill="none" stroke="#4a9be8" stroke-width="4" stroke-linecap="round"/>'
        + '<path class="k-o" d="M-5 -46L-5 4H-40Z" fill="#ffd23f"/>'
        + '<path class="k-o" d="M0 -60L-18 -54L0 -48Z" fill="#ef5b56" stroke-width="2"/>'
        + '<path class="k-o" d="M-62 10H62L46 38H-46Z" fill="#ef5b56"/>'
        + '<path d="M-56 18H56" stroke="#fff" stroke-width="4" opacity=".85"/>'
        + "".join(f'<circle cx="{x}" cy="28" r="4" fill="{GLASS}" stroke="{INK}" stroke-width="2"/>' for x in (-24, 0, 24))
        + f'<path d="{waves}" fill="#8ec5ff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    )


def bike():
    def bwheel(x):
        spokes = "".join(f'<path d="M{x} 18l{fmt(22 * c)} {fmt(22 * s)}" stroke="#c9c2cc" stroke-width="1.5"/>'
                         for c, s in ((1, 0), (0, 1), (.707, .707), (.707, -.707)))
        spokes += "".join(f'<path d="M{x} 18l{fmt(-22 * c)} {fmt(-22 * s)}" stroke="#c9c2cc" stroke-width="1.5"/>'
                          for c, s in ((1, 0), (0, 1), (.707, .707), (.707, -.707)))
        return spokes + f'<circle cx="{x}" cy="18" r="24" fill="none" stroke="{INK}" stroke-width="6"/><circle cx="{x}" cy="18" r="4" fill="{INK}"/>'
    frame = "M-38 18L-12 -16L22 -18L-2 18Z M-38 18H-2M22 -18L38 18"
    return (
        shadow(46, 64)
        + bwheel(-38) + bwheel(38)
        + dstroke(frame, "#ef5b56", 5)
        + dstroke("M-12 -16L-15 -24M22 -18L20 -30L30 -32", INK, 1.5)
        + f'<path d="M-24 -28Q-14 -32 -6 -26Q-14 -22 -24 -24Z" fill="{INK}"/>'
        + f'<circle cx="-2" cy="18" r="7" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        + f'<path d="M-2 18L6 30M2 30H10" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    )


VEHICLES = [
    ("car", car), ("bus", bus), ("truck", truck), ("train", train),
    ("plane", plane), ("boat", boat), ("bike", bike),
]


# ================================================================ clothes
def shirt():
    body = "M-24 -46L-50 -34L-66 -2L-46 8L-36 -10V50H36V-10L46 8L66 -2L50 -34L24 -46Q0 -36 -24 -46Z"
    return (
        shadow(56, 44)
        + f'<path class="k-o" d="{body}" fill="#5aa9ee"/>'
        + '<path d="M-44 -6L-58 -12M44 -6L58 -12" stroke="#2f7cc6" stroke-width="3" stroke-linecap="round"/>'
        + f'<path d="M0 -34V50" stroke="{INK}" stroke-width="2"/>'
        + "".join(f'<circle cx="5" cy="{y}" r="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/>' for y in (-20, 0, 20, 38))
        + '<path class="k-o" d="M-24 -46L-2 -32L-14 -20Z" fill="#fff" stroke-width="2.5"/>'
        + '<path class="k-o" d="M24 -46L2 -32L14 -20Z" fill="#fff" stroke-width="2.5"/>'
        + '<rect class="k-o" x="14" y="-6" width="14" height="14" rx="2" fill="#4a9be8" stroke-width="2"/>'
    )


def dress():
    skirt = "M-22 -8L-58 48Q0 58 58 48L22 -8Z"
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#fff" opacity=".85"/>' for x, y in ((-20, 12), (6, 20), (28, 34), (-36, 38), (-10, 40), (18, 8), (40, 44)))
    return (
        shadow(58, 50)
        + '<ellipse class="k-o" cx="-30" cy="-38" rx="12" ry="9" transform="rotate(-25 -30 -38)" fill="#f78fb3"/>'
        + '<ellipse class="k-o" cx="30" cy="-38" rx="12" ry="9" transform="rotate(25 30 -38)" fill="#f78fb3"/>'
        + f'<path class="k-o" d="{skirt}" fill="#f78fb3"/>'
        + dots
        + '<path class="k-o" d="M-22 -8L-24 -50Q0 -38 24 -50L22 -8Z" fill="#f78fb3"/>'
        + '<path d="M-14 -44Q0 -34 14 -44" fill="none" stroke="#e06b95" stroke-width="3" stroke-linecap="round"/>'
        + '<rect class="k-o" x="-25" y="-12" width="50" height="9" rx="3" fill="#9b74e8" stroke-width="2.5"/>'
        + '<path class="k-o" d="M0 -8l-12 -7v14Zm0 0l12 -7v14Z" fill="#9b74e8" stroke-width="2"/>'
    )


def skirt():
    body = "M-34 -26H34L62 38Q0 52 -62 38Z"
    return (
        shadow(52, 56)
        + f'<path class="k-o" d="{body}" fill="#9b74e8"/>'
        + '<path d="M-20 -26L-34 44M0 -26V48M20 -26L34 44" stroke="#7a52cc" stroke-width="3" stroke-linecap="round"/>'
        + '<path d="M-50 30Q0 42 50 30" fill="none" stroke="#ffd23f" stroke-width="4" stroke-linecap="round"/>'
        + '<rect class="k-o" x="-37" y="-40" width="74" height="15" rx="4" fill="#7a52cc"/>'
        + '<path d="M-26 -18L-36 10" ' + SHINE + "/>"
    )


def jeans():
    legs = "M-40 -44H40L46 56H10L0 -6L-10 56H-46Z"
    return (
        '<g transform="translate(0 2)">'
        + shadow(58, 50)
        + f'<path class="k-o" d="{legs}" fill="#3d7cc9"/>'
        + '<path d="M-38 -26Q-24 -24 -20 -40M38 -26Q24 -24 20 -40" fill="none" stroke="#ffc93c" stroke-width="2.5" stroke-dasharray="4 3"/>'
        + '<path d="M0 -44V-12" stroke="#2a5f9e" stroke-width="3"/>'
        + '<path d="M-44 46H-11M11 46H45" stroke="#2a5f9e" stroke-width="4"/>'
        + '<rect class="k-o" x="-42" y="-58" width="84" height="14" rx="3" fill="#2f6fb0"/>'
        + '<circle cx="0" cy="-51" r="3.5" fill="#ffc93c" stroke="#3f3345" stroke-width="1.5"/>'
        + "".join(f'<rect x="{x}" y="-60" width="5" height="18" rx="2" fill="#2f6fb0" stroke="{INK}" stroke-width="2"/>' for x in (-30, 25))
        + "</g>"
    )


def shoe(fill, dark):
    upper = "M-40 12V-18Q-40 -26 -32 -26H-14Q-8 -26 -4 -18Q8 -6 26 -4Q40 -2 40 10V12Z"
    return (
        f'<path class="k-o" d="{upper}" fill="{fill}"/>'
        f'<path d="M-4 -18Q8 -6 26 -4" fill="none" stroke="{dark}" stroke-width="3"/>'
        + "".join(f'<path d="M{x} {y}l7 -6" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' for x, y in ((-6, -12), (2, -6), (10, -2)))
        + f'<path class="k-o" d="M-42 12H42Q42 22 34 22H-34Q-42 22 -42 12Z" fill="#fff"/>'
        + f'<circle cx="-28" cy="-6" r="5" fill="#fff" opacity=".8"/>'
    )


def shoes():
    return (
        shadow(46, 60)
        + f'<g transform="translate(-14 -18) scale(.94)">{shoe("#e0483f", "#b93a33")}</g>'
        + f'<g transform="translate(14 18)">{shoe("#ef5b56", "#c9403b")}</g>'
    )


def sock(fill, stripe):
    body = "M-14 -52H14V10Q14 30 -4 36L-28 44Q-46 48 -48 34Q-50 22 -36 16L-14 8Z"
    return (
        f'<path class="k-o" d="{body}" fill="{fill}"/>'
        f'<path d="M-14 -28H14M-14 -18H14" stroke="{stripe}" stroke-width="5"/>'
        f'<path d="M-40 18Q-50 28 -44 40Q-38 46 -30 42L-26 26Z" fill="{stripe}"/>'
        f'<path class="k-o" d="{body}" fill="none"/>'
        f'<rect class="k-o" x="-16" y="-58" width="32" height="12" rx="4" fill="#fff"/>'
    )


def socks():
    return (
        shadow(56, 54)
        + f'<g transform="translate(-10 2)">{sock("#5cc36a", "#ffd23f")}</g>'
        + f'<g transform="translate(36 8)">{sock("#5cc36a", "#ffd23f")}</g>'
    )


def coat():
    body = "M-24 -52L-52 -38L-62 44H-44L-40 -6V54H40V-6L44 44H62L52 -38L24 -52Q0 -42 -24 -52Z"
    return (
        shadow(58, 50)
        + f'<path class="k-o" d="{body}" fill="#e0783c"/>'
        + f'<path d="M0 -40V54" stroke="{INK}" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-24 -52L-2 -40L-10 -10L-20 -30Z" fill="#c9602a" stroke-width="2.5"/>'
        + '<path class="k-o" d="M24 -52L2 -40L10 -10L20 -30Z" fill="#c9602a" stroke-width="2.5"/>'
        + "".join(f'<rect x="-10" y="{y}" width="20" height="5" rx="2.5" fill="#ffe0b8" stroke="{INK}" stroke-width="1.5"/>' for y in (2, 20, 38))
        + '<path class="k-o" d="M-34 18H-16V34H-34Z" fill="#c9602a" stroke-width="2"/><path class="k-o" d="M16 18H34V34H16Z" fill="#c9602a" stroke-width="2"/>'
        + '<path d="M-60 32H-46M60 32H46" stroke="#ffe0b8" stroke-width="4"/>'
    )


CLOTHES = [
    ("shirt", shirt), ("dress", dress), ("skirt", skirt), ("jeans", jeans),
    ("shoes", shoes), ("socks", socks), ("coat", coat),
]
