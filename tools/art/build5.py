"""Alphabet G-Z illustrations. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
import math
from common import INK, fmt, svg_wrap
from build1 import shadow
from build4 import sun as _sun, union, circ


def dstroke(d, color, w=4.5):
    """A line with an ink outline."""
    return (
        f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 5}" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def eyes(x, y, r=5.5):
    return (
        f'<circle cx="{-x}" cy="{y}" r="{r}" fill="{INK}"/><circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>'
        f'<circle cx="{fmt(-x + r * .35)}" cy="{fmt(y - r * .4)}" r="{fmt(r * .38)}" fill="#fff"/>'
        f'<circle cx="{fmt(x + r * .35)}" cy="{fmt(y - r * .4)}" r="{fmt(r * .38)}" fill="#fff"/>'
    )


def cheeks(x, y, rx=6.5, ry=4):
    return (
        f'<ellipse cx="{-x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ff7d93" opacity=".45"/>'
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ff7d93" opacity=".45"/>'
    )


def smile(y, w=7, d=5, sw=2.5):
    return f'<path d="M{-w} {y}Q0 {y + d} {w} {y}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round"/>'


def mirror(s):
    return s + f'<g transform="scale(-1 1)">{s}</g>'


def star(cx, cy, r, fill="#ffd23f", sw=2):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        pts.append(f"{fmt(cx + rr * math.cos(a))} {fmt(cy + rr * math.sin(a))}")
    return f'<path d="M{"L".join(pts)}Z" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'


# ---------------------------------------------------------------- G grapes
def grapes():
    g = shadow(58, 34)
    g += dstroke("M2 -40C2 -50 6 -56 12 -60", "#8b5a3c")
    g += '<path class="k-o" d="M4 -44C-8 -60 -30 -60 -38 -50C-26 -40 -10 -38 4 -44Z" fill="#6cc070"/>'
    order = [(-8, [-40, 40]), (-30, [-28, 0, 28]), (-6, [-14, 14]), (18, [-26, 0, 26]), (40, [-12, 12])]
    for y, xs in order:
        for x in xs:
            if abs(x) == 40:
                continue
            g += f'<circle class="k-o" cx="{x}" cy="{y}" r="15" fill="#9b74e8"/>'
            g += f'<circle cx="{x - 5}" cy="{y - 5}" r="3.5" fill="#fff" opacity=".6"/>'
    return g


# ---------------------------------------------------------------- H hat
def hat():
    crown = "M-34 22L-30 -26Q0 -38 30 -26L34 22Z"
    return (
        shadow(40, 56)
        + f'<ellipse class="k-o" cx="0" cy="22" rx="60" ry="13" fill="#4a9be8"/>'
        + f'<path d="{crown}" fill="#5aa9ee"/>'
        + '<path d="M-32.4 2H32.4L33.3 15H-33.3Z" fill="#ef5b56"/>'
        + f'<path class="k-o" d="{crown}" fill="none"/>'
        + '<path d="M-20 -24Q-22 -8 -22 -2" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".5"/>'
        + "".join(
            f'<circle cx="{fmt(18 + 6 * math.cos(math.radians(a)))}" cy="{fmt(8 + 6 * math.sin(math.radians(a)))}" r="4.5" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
            for a in range(0, 360, 72)
        )
        + f'<circle cx="18" cy="8" r="3.5" fill="#ffd23f" stroke="{INK}" stroke-width="1.5"/>'
    )


# ---------------------------------------------------------------- I ice cream
def ice_cream():
    return (
        '<g transform="translate(0 4)">'
        + '<path class="k-o" d="M-24 0L0 58L24 0Z" fill="#f3c27a"/>'
        + '<path d="M-16 8L6 40M0 8L10 28M16 8L-6 40M0 8L-10 28" stroke="#d99a45" stroke-width="2.5" stroke-linecap="round"/>'
        + '<ellipse class="k-o" cx="0" cy="-32" rx="22" ry="19" fill="#8fe0c0"/>'
        + '<path class="k-o" d="M-30 2C-34 -20 -16 -28 0 -28C16 -28 34 -20 30 2Q24 8 18 3Q12 10 6 4Q0 10 -6 4Q-12 10 -18 3Q-24 8 -30 2Z" fill="#f99bb8"/>'
        + '<path d="M-20 -18Q-14 -24 -6 -24" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
        + dstroke("M4 -52Q6 -60 12 -62", "#6cc070", 2.5)
        + f'<circle class="k-o" cx="4" cy="-50" r="7" fill="#ef5b56" stroke-width="2.5"/>'
        + '<circle cx="2" cy="-52" r="2" fill="#fff" opacity=".8"/>'
        + "</g>"
    )


# ---------------------------------------------------------------- J jellyfish
def jellyfish():
    col = "#f7a8d0"
    t = ""
    for x in (-24, -8, 8, 24):
        t += dstroke(f"M{x} 4q-7 10 0 20t0 20", col, 4)
    return (
        t
        + f'<path class="k-o" d="M-38 4C-38 -30 -20 -44 0 -44C20 -44 38 -30 38 4Q28 12 19 4Q9.5 12 0 4Q-9.5 12 -19 4Q-28 12 -38 4Z" fill="{col}"/>'
        + '<path d="M-24 -26Q-18 -34 -8 -36" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
        + eyes(12, -14, 5)
        + cheeks(22, -6, 5.5, 3.5)
        + smile(-6, 5, 4)
        + f'<circle cx="-54" cy="-30" r="5" fill="#fff" fill-opacity=".7" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="52" cy="-42" r="3.5" fill="#fff" fill-opacity=".7" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="58" cy="-24" r="5.5" fill="#fff" fill-opacity=".7" stroke="{INK}" stroke-width="2"/>'
    )


# ---------------------------------------------------------------- K kite
def kite():
    T, R, B, L, C = (0, -58), (34, -18), (0, 34), (-34, -18), (0, -18)
    tri = lambda a, b, col: f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}L{C[0]} {C[1]}Z" fill="{col}"/>'
    bow = lambda x, y, col: (
        f'<path d="M{x - 7} {y - 5}L{x} {y}L{x - 7} {y + 5}ZM{x + 7} {y - 5}L{x} {y}L{x + 7} {y + 5}Z" '
        f'fill="{col}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    )
    return (
        '<g transform="translate(4 -5) rotate(-14)">'
        + f'<path d="M0 34C-10 40 6 46 -4 52C-12 58 -2 62 -10 66" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        + bow(-1, 44, "#4a9be8")
        + bow(-6, 58, "#5cc36a")
        + tri(T, L, "#ef5b56")
        + tri(T, R, "#ffd23f")
        + tri(B, L, "#ffd23f")
        + tri(B, R, "#ef5b56")
        + f'<path d="M0 -58V34M-34 -18H34" stroke="{INK}" stroke-width="2"/>'
        + f'<path class="k-o" d="M{T[0]} {T[1]}L{R[0]} {R[1]}L{B[0]} {B[1]}L{L[0]} {L[1]}Z" fill="none"/>'
        + "</g>"
    )


# ---------------------------------------------------------------- L lion
def lion():
    mane = [circ(40 * math.cos(math.radians(a)), 2 + 40 * math.sin(math.radians(a)), 17) for a in range(0, 360, 30)]
    ear = '<circle class="k-o" cx="-26" cy="-24" r="11" fill="#ffc94a"/><circle cx="-26" cy="-24" r="5.5" fill="#f5a05a"/>'
    return (
        shadow(60, 44)
        + union(mane, "#e0892b")
        + mirror(ear)
        + '<circle class="k-o" cx="0" cy="4" r="34" fill="#ffc94a"/>'
        + '<ellipse cx="0" cy="17" rx="16" ry="11" fill="#fff1d6"/>'
        + eyes(13, -4, 5.5)
        + cheeks(22, 8)
        + f'<path d="M-6 10L6 10L0 16Z" fill="#8b5a3c" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        + f'<path d="M0 16C0 22 -6 24 -9 20M0 16C0 22 6 24 9 20" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    )


# ---------------------------------------------------------------- M moon
def moon():
    R1, (cx2, cy2), R2 = 44, (24, -14), 38
    d = math.hypot(cx2, cy2)
    a = (R1 ** 2 - R2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(R1 ** 2 - a ** 2)
    ux, uy = cx2 / d, cy2 / d
    px, py = a * ux, a * uy
    p1 = (px - h * uy, py + h * ux)
    p2 = (px + h * uy, py - h * ux)
    path = (
        f"M{fmt(p1[0])} {fmt(p1[1])}A{R1} {R1} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}"
        f"A{R2} {R2} 0 0 0 {fmt(p1[0])} {fmt(p1[1])}Z"
    )
    return (
        '<g transform="translate(-8 4)">'
        + f'<path class="k-o" d="{path}" fill="#ffd23f"/>'
        + f'<path d="M-30 -6q5 -6 10 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<path d="M-26 12q6 6 12 1" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + '<ellipse cx="-32" cy="6" rx="5" ry="3.5" fill="#ff7d93" opacity=".45"/>'
        + "</g>"
        + star(42, -30, 13)
        + star(58, 6, 8)
        + star(56, 36, 9)
    )


# ---------------------------------------------------------------- N nest
def nest():
    egg = lambda x, y, r: (
        f'<ellipse class="k-o" cx="{x}" cy="{y}" rx="14" ry="18" fill="#9fd8f5" transform="rotate({r} {x} {y})"/>'
        f'<circle cx="{x - 4}" cy="{y - 6}" r="2" fill="#5aa9d6"/><circle cx="{x + 4}" cy="{y - 1}" r="1.6" fill="#5aa9d6"/>'
    )
    return (
        shadow(40, 52)
        + egg(-22, -12, -14)
        + egg(22, -12, 14)
        + egg(0, -20, 0)
        + '<path class="k-o" d="M-58 -6Q-52 34 0 36Q52 34 58 -6Q30 6 0 4Q-30 6 -58 -6Z" fill="#b07a4f"/>'
        + '<path d="M-48 6Q-20 16 10 12M-40 20Q-10 28 26 20M-18 30Q10 32 38 24M20 10Q40 10 52 2M-54 -2Q-40 6 -26 8" fill="none" stroke="#7d5232" stroke-width="2.5" stroke-linecap="round"/>'
    )


# ---------------------------------------------------------------- O owl
def owl():
    tuft = '<path class="k-o" d="M-34 -28L-40 -56L-14 -42Z" fill="#8b5a3c"/>'
    wing = '<ellipse class="k-o" cx="-40" cy="10" rx="11" ry="24" fill="#87532f" transform="rotate(12 -40 10)"/>'
    feet = '<ellipse class="k-o" cx="-12" cy="54" rx="7" ry="4.5" fill="#ffb13b" stroke-width="2.5"/>'
    eye = (
        f'<circle cx="-16" cy="-16" r="15" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        f'<circle cx="-15" cy="-15" r="7.5" fill="{INK}"/><circle cx="-12.5" cy="-18" r="2.5" fill="#fff"/>'
    )
    return (
        shadow(58, 36)
        + mirror(tuft)
        + mirror(feet)
        + '<path class="k-o" d="M0 -46C30 -46 42 -20 42 10C42 38 24 52 0 52C-24 52 -42 38 -42 10C-42 -20 -30 -46 0 -46Z" fill="#a8704a"/>'
        + '<ellipse cx="0" cy="24" rx="24" ry="24" fill="#f2d7b0"/>'
        + '<path d="M-10 16l4 4l4 -4M2 16l4 4l4 -4M-16 30l4 4l4 -4M-4 30l4 4l4 -4M8 30l4 4l4 -4" fill="none" stroke="#c9a077" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        + mirror(wing)
        + mirror(eye)
        + f'<path d="M-6 -4L6 -4L0 6Z" fill="#ffb13b" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    )


# ---------------------------------------------------------------- P pig
def pig():
    ear = '<path class="k-o" d="M-38 -18L-40 -50Q-38 -54 -34 -52L-12 -34Z" fill="#f7a1bd"/>'
    return (
        shadow(52, 42)
        + mirror(ear)
        + '<ellipse class="k-o" cx="0" cy="4" rx="48" ry="40" fill="#fbbfd2"/>'
        + eyes(20, -10, 5.5)
        + cheeks(32, 8, 7, 4.5)
        + '<ellipse class="k-o" cx="0" cy="12" rx="19" ry="13" fill="#f58fb0"/>'
        + f'<ellipse cx="-7" cy="12" rx="3" ry="4.5" fill="{INK}"/><ellipse cx="7" cy="12" rx="3" ry="4.5" fill="{INK}"/>'
        + smile(32, 8, 6)
    )


# ---------------------------------------------------------------- Q queen
def queen():
    return (
        '<path class="k-o" d="M-44 40C-50 -6 -34 -36 0 -36C34 -36 50 -6 44 40Q0 54 -44 40Z" fill="#a0602f"/>'
        + '<circle class="k-o" cx="0" cy="6" r="33" fill="#ffd9b8"/>'
        + '<path class="k-o" d="M-32 -2C-30 -22 -14 -28 0 -28C14 -28 30 -22 32 -2C22 -10 12 -16 0 -16C-12 -16 -22 -10 -32 -2Z" fill="#a0602f"/>'
        + '<path class="k-o" d="M-30 -24L-32 -54L-15 -38L0 -60L15 -38L32 -54L30 -24Q0 -32 -30 -24Z" fill="#ffd23f"/>'
        + f'<circle cx="0" cy="-36" r="4.5" fill="#ef5b56" stroke="{INK}" stroke-width="1.5"/>'
        + f'<circle cx="-17" cy="-31" r="3" fill="#4a9be8" stroke="{INK}" stroke-width="1.5"/>'
        + f'<circle cx="17" cy="-31" r="3" fill="#4a9be8" stroke="{INK}" stroke-width="1.5"/>'
        + eyes(12, 6, 4.5)
        + cheeks(20, 16, 6, 3.5)
        + f'<path d="M-8 21Q0 29 8 21" fill="#e25563" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    )


# ---------------------------------------------------------------- R rabbit
def rabbit():
    ear = (
        '<ellipse class="k-o" cx="-16" cy="-34" rx="11" ry="27" fill="#f1ece9" transform="rotate(-10 -16 -34)"/>'
        '<ellipse cx="-16" cy="-32" rx="5" ry="18" fill="#f9b6c8" transform="rotate(-10 -16 -32)"/>'
    )
    return (
        shadow(52, 38)
        + mirror(ear)
        + '<ellipse class="k-o" cx="0" cy="14" rx="40" ry="34" fill="#f1ece9"/>'
        + eyes(15, 6, 5)
        + cheeks(25, 18, 6, 4)
        + f'<path d="M-4.5 18L4.5 18L0 23Z" fill="#f47c96" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        + f'<path d="M-4 30H4V36H-4Z" fill="#fff" stroke="{INK}" stroke-width="1.8"/><path d="M0 30V36" stroke="{INK}" stroke-width="1.5"/>'
        + f'<path d="M0 23V28M0 28C-2 31 -7 31 -8 28M0 28C2 31 7 31 8 28" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + f'<path d="M-18 24L-44 20M-18 28L-44 32M18 24L44 20M18 28L44 32" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
    )


# ---------------------------------------------------------------- S sun
def sun():
    return _sun(0, 0)


# ---------------------------------------------------------------- T turtle
def turtle():
    leg = lambda x: f'<rect class="k-o" x="{x}" y="8" width="18" height="20" rx="8" fill="#9bd97f"/>'
    return (
        '<g transform="translate(-8 6)">'
        + shadow(34, 56)
        + '<path class="k-o" d="M-48 6L-60 10L-48 14Z" fill="#9bd97f" stroke-width="2.5"/>'
        + leg(-32) + leg(16)
        + '<circle class="k-o" cx="58" cy="-6" r="15" fill="#9bd97f"/>'
        + f'<circle cx="62" cy="-10" r="3.8" fill="{INK}"/><circle cx="63.3" cy="-11.5" r="1.4" fill="#fff"/>'
        + f'<path d="M58 -1Q63 3 68 -1" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
        + '<ellipse cx="52" cy="-2" rx="4" ry="2.5" fill="#ff7d93" opacity=".45"/>'
        + '<path class="k-o" d="M-44 10C-44 -30 44 -30 44 10Z" fill="#5cc36a"/>'
        + '<path d="M-12 -16L0 -22L12 -16L12 -4L0 2L-12 -4Z" fill="#3f9e4d"/>'
        + '<path d="M-34 -2L-24 -10L-18 -2L-22 6L-34 6Z" fill="#3f9e4d"/><path d="M34 -2L24 -10L18 -2L22 6L34 6Z" fill="#3f9e4d"/>'
        + '<path class="k-o" d="M-50 6H50Q54 6 54 10Q54 16 48 16H-48Q-54 16 -54 10Q-54 6 -50 6Z" fill="#f2c14e"/>'
        + "</g>"
    )


# ---------------------------------------------------------------- U umbrella
def umbrella():
    canopy = "M-56 0C-56 -34 -30 -50 0 -50C30 -50 56 -34 56 0Q46.7 -8 37.3 0Q28 -8 18.7 0Q9.3 -8 0 0Q-9.3 -8 -18.7 0Q-28 -8 -37.3 0Q-46.7 -8 -56 0Z"
    drop = lambda x, y: f'<path d="M{x} {y - 8}C{x - 2} {y - 4} {x - 5} {y} {x - 5} {y + 2}A5 5 0 0 0 {x + 5} {y + 2}C{x + 5} {y} {x + 2} {y - 4} {x} {y - 8}Z" fill="#9fd8f5" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    return (
        '<g transform="translate(0 4)">'
        + dstroke("M0 0V42Q0 54 -10 54Q-19 54 -19 45", "#8b5a3c", 4)
        + f'<path d="{canopy}" fill="#ef5b56"/>'
        + '<path d="M0 -50Q-12 -26 -18.7 0Q-9.3 -8 0 0Q9.3 -8 18.7 0Q12 -26 0 -50Z" fill="#ffd23f"/>'
        + '<path d="M-38 -38Q-50 -20 -56 0Q-46.7 -8 -37.3 0Q-40 -22 -38 -38Z" fill="#ffd23f"/>'
        + '<path d="M38 -38Q50 -20 56 0Q46.7 -8 37.3 0Q40 -22 38 -38Z" fill="#ffd23f"/>'
        + f'<path d="M0 -50Q-12 -26 -18.7 0M0 -50Q12 -26 18.7 0M-5 -50Q-30 -30 -37.3 0M5 -50Q30 -30 37.3 0" fill="none" stroke="{INK}" stroke-width="2"/>'
        + f'<path class="k-o" d="{canopy}" fill="none"/>'
        + f'<circle class="k-o" cx="0" cy="-53" r="4" fill="#ef5b56" stroke-width="2.5"/>'
        + drop(-58, 30) + drop(56, 22) + drop(40, 44)
        + "</g>"
    )


# ---------------------------------------------------------------- V van
def van():
    wheel = lambda x: (
        f'<circle cx="{x}" cy="22" r="13" fill="{INK}"/><circle cx="{x}" cy="22" r="5.5" fill="#c9c2cc"/>'
    )
    return (
        shadow(36, 60)
        + '<path class="k-o" d="M-60 22V-16Q-60 -32 -44 -32H28Q38 -32 44 -22L56 -4Q62 2 62 10V22Z" fill="#4fc1b9"/>'
        + '<rect x="-58.5" y="2" width="119" height="6" fill="#fff" opacity=".85"/>'
        + f'<rect class="k-o" x="-50" y="-24" width="28" height="18" rx="4" fill="#cdeeff" stroke-width="2.5"/>'
        + f'<rect class="k-o" x="-14" y="-24" width="28" height="18" rx="4" fill="#cdeeff" stroke-width="2.5"/>'
        + f'<path class="k-o" d="M22 -24H32Q35 -24 37 -21L46 -6H22Z" fill="#cdeeff" stroke-width="2.5"/>'
        + f'<path d="M4 -2V20" stroke="{INK}" stroke-width="2"/><path d="M8 12H13" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<circle cx="57" cy="8" r="3.5" fill="#ffd23f" stroke="{INK}" stroke-width="1.8"/>'
        + wheel(-34) + wheel(34)
    )


# ---------------------------------------------------------------- W whale
def whale():
    body = "M-56 14C-56 -18 -30 -32 0 -32C24 -32 42 -20 46 2C50 20 44 34 18 36C-8 38 -56 38 -56 14Z"
    return (
        shadow(46, 50)
        + '<path class="k-o" d="M40 12C52 10 58 0 58 -10C54 -18 46 -22 44 -30C52 -30 60 -26 63 -19C66 -26 72 -30 80 -30C76 -22 68 -16 66 -10C66 6 54 20 40 24Z" fill="#4a9be8"/>'
        + f'<path class="k-o" d="{body}" fill="#5aa9ee"/>'
        + '<path d="M-50 20C-40 30 -10 34 18 32C34 31 42 26 44 18C30 24 -20 26 -50 20Z" fill="#d9eeff"/>'
        + f'<path class="k-o" d="{body}" fill="none"/>'
        + '<path class="k-o" d="M-10 16C-4 24 6 26 12 22C8 16 0 12 -10 16Z" fill="#4a9be8" stroke-width="2.5"/>'
        + f'<circle cx="-30" cy="-4" r="5" fill="{INK}"/><circle cx="-28.2" cy="-6" r="1.9" fill="#fff"/>'
        + f'<path d="M-50 8Q-44 14 -36 10" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + '<ellipse cx="-20" cy="6" rx="5.5" ry="3.5" fill="#ff7d93" opacity=".45"/>'
        + dstroke("M-8 -32C-8 -44 -14 -50 -22 -50M-8 -32C-8 -44 -2 -52 6 -50", "#9fd8f5", 4)
        + f'<circle cx="-26" cy="-56" r="3.5" fill="#9fd8f5" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="10" cy="-57" r="3.5" fill="#9fd8f5" stroke="{INK}" stroke-width="2"/>'
    )


# ---------------------------------------------------------------- X fox
def fox():
    ear = (
        '<path class="k-o" d="M-44 -16L-42 -58L-12 -30Z" fill="#ff8c3a"/>'
        '<path d="M-38 -24L-37 -46L-22 -31Z" fill="#5b3a2e"/>'
    )
    face = "M-48 -14C-40 -30 -20 -34 0 -34C20 -34 40 -30 48 -14C40 10 16 36 0 42C-16 36 -40 10 -48 -14Z"
    return (
        shadow(52, 34)
        + mirror(ear)
        + f'<path d="{face}" fill="#ff8c3a"/>'
        + mirror('<path d="M-48 -14C-36 -8 -18 6 -2 40C-16 36 -40 10 -48 -14Z" fill="#fff"/>')
        + f'<path class="k-o" d="{face}" fill="none"/>'
        + eyes(17, -10, 5.5)
        + cheeks(24, 6, 5.5, 3.5)
        + f'<ellipse cx="0" cy="34" rx="7" ry="5" fill="{INK}"/><ellipse cx="-2" cy="32.5" rx="2.2" ry="1.3" fill="#fff" opacity=".8"/>'
    )


# ---------------------------------------------------------------- Y yo-yo
def yoyo():
    return (
        '<g transform="translate(0 10)">'
        + shadow(50, 34)
        + f'<path d="M0 0C6 -24 -6 -40 0 -62" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<ellipse cx="0" cy="-68" rx="6" ry="4" fill="none" stroke="{INK}" stroke-width="2.5"/>'
        + '<circle class="k-o" cx="0" cy="0" r="40" fill="#ef5b56"/>'
        + f'<circle cx="0" cy="0" r="27" fill="#ff8a80" stroke="{INK}" stroke-width="2"/>'
        + '<path d="M-26 -18A32 32 0 0 1 -6 -32" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" opacity=".6"/>'
        + f'<circle cx="0" cy="0" r="8" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        + f'<path d="M-52 -14Q-56 0 -52 14M-60 -8Q-62 0 -60 8M52 -14Q56 0 52 14M60 -8Q62 0 60 8" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + "</g>"
    )


# ---------------------------------------------------------------- Z zebra
def zebra():
    ear = (
        '<ellipse class="k-o" cx="-26" cy="-46" rx="9" ry="17" fill="#fff" transform="rotate(-28 -26 -46)"/>'
        '<ellipse cx="-26" cy="-45" rx="4" ry="10" fill="#c9c2cc" transform="rotate(-28 -26 -45)"/>'
    )
    head = "M-28 -34C-28 -52 28 -52 28 -34C30 -10 30 8 26 22C22 42 -22 42 -26 22C-30 8 -30 -10 -28 -34Z"
    stripes = (
        "M-28 -32Q-20 -28 -13 -34M-29 -18Q-24 -15 -20 -18M-28 12Q-23 15 -19 11"
        "M28 -32Q20 -28 13 -34M29 -18Q24 -15 20 -18M28 12Q23 15 19 11"
        "M-6 -46Q0 -38 6 -46M-5 -34Q0 -28 5 -34"
    )
    return (
        shadow(52, 34)
        + f'<path d="M-10 -44L-8 -60L-2 -50L2 -62L8 -50L12 -60L12 -42Z" fill="{INK}"/>'
        + mirror(ear)
        + f'<path class="k-o" d="{head}" fill="#fff"/>'
        + f'<path d="{stripes}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        + '<ellipse class="k-o" cx="0" cy="26" rx="25" ry="16" fill="#6d6275"/>'
        + f'<ellipse cx="-9" cy="24" rx="3" ry="4.5" fill="{INK}"/><ellipse cx="9" cy="24" rx="3" ry="4.5" fill="{INK}"/>'
        + '<path d="M-8 34Q0 38 8 34" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>'
        + eyes(15, -4, 5)
        + cheeks(22, 8, 5, 3.5)
    )


ITEMS = [
    ("G", "grapes", grapes), ("H", "hat", hat), ("I", "ice cream", ice_cream), ("J", "jellyfish", jellyfish),
    ("K", "kite", kite), ("L", "lion", lion), ("M", "moon", moon), ("N", "nest", nest), ("O", "owl", owl),
    ("P", "pig", pig), ("Q", "queen", queen), ("R", "rabbit", rabbit), ("S", "sun", sun), ("T", "turtle", turtle),
    ("U", "umbrella", umbrella), ("V", "van", van), ("W", "whale", whale), ("X", "fox", fox), ("Y", "yo-yo", yoyo),
    ("Z", "zebra", zebra),
]

if __name__ == "__main__":
    cells = ""
    for i, (L, w, fn) in enumerate(ITEMS):
        x, y = 90 + (i % 4) * 166, 90 + (i // 4) * 170
        cells += (
            f'<rect x="{x - 82}" y="{y - 72}" width="164" height="160" rx="16" fill="#f4f1ea"/>'
            f'<g transform="translate({x} {y})">{fn()}</g>'
            f'<text class="k-f" x="{x}" y="{y + 82}" font-size="15" fill="{INK}" text-anchor="middle">{L} {w}</text>'
        )
    open("g_to_z.svg", "w").write(svg_wrap(20 + 5 * 170 + 10, "G-Z", "test", cells))
    print("ok")
