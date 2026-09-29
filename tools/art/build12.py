"""Action words: a full-body kid posed by joint points, plus a few props.
Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
from common import INK, fmt
from build1 import shadow, ball
from build5 import dstroke, eyes, cheeks, smile
from build8 import eye_whites, luminance

SKINS = ["#ffd2b0", "#e8b48a", "#c68a5e", "#8d5a3b"]
HEAD_R = 19


def pts(p):
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in p)


def limb(p, color, w):
    return dstroke(pts(p), color, w)


def hand(x, y, skin):
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="5.5" fill="{skin}" stroke="{INK}" stroke-width="2.5"/>'


def shoe(x, y, d, color):
    """d = 1 points the toe right, -1 left."""
    return f'<path class="k-o" d="M{fmt(x - 6 * d)} {fmt(y + 4)}Q{fmt(x - 7 * d)} {fmt(y - 5)} {fmt(x + 1 * d)} {fmt(y - 5)}Q{fmt(x + 10 * d)} {fmt(y - 3)} {fmt(x + 10 * d)} {fmt(y + 4)}Z" fill="{color}" stroke-width="2.5"/>'


def arm(p, shirt, skin):
    """Shoulder -> elbow -> hand, with a short sleeve."""
    (sx, sy), (ex, ey) = p[0], p[1]
    sleeve = [(sx, sy), (sx + (ex - sx) * 0.55, sy + (ey - sy) * 0.55)]
    return limb(p, skin, 8) + dstroke(pts(sleeve), shirt, 11) + hand(*p[-1], skin)


def leg(p, pants, shoes, d):
    return limb(p, pants, 11) + shoe(*p[-1], d, shoes)


# ---------------------------------------------------------------- faces and hair
def face(mouth="smile", look="open", skin=SKINS[0]):
    whites = eye_whites(7, -1, 3.2) if (luminance(skin) + 0.05) / (luminance(INK) + 0.05) < 3 else ""
    if look == "down":
        e = f'<path d="M-10 0Q-7 3 -4 0M4 0Q7 3 10 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    elif look == "shut":
        e = f'<path d="M-10 0Q-7 -3 -4 0M4 0Q7 -3 10 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    else:
        e = whites + eyes(7, -1, 3.2)
    if mouth == "open":
        m = f'<ellipse cx="0" cy="9" rx="4" ry="5" fill="#c9403b" stroke="{INK}" stroke-width="2"/>'
    elif mouth == "eat":
        m = f'<ellipse cx="0" cy="9" rx="5" ry="4" fill="#c9403b" stroke="{INK}" stroke-width="2"/>'
    else:
        m = smile(7, 5, 4.5)
    return e + cheeks(12, 6, 4, 2.5) + m


def hair_short(c):
    return (
        f'<path class="k-o" d="M-19 -2C-22 -22 -8 -26 2 -25C16 -25 23 -15 19 -2C15 -12 7 -15 -1 -13C-8 -16 -15 -11 -19 -2Z" fill="{c}"/>',
        "",
    )


def hair_pigtails(c):
    back = (
        f'<circle class="k-o" cx="-22" cy="-6" r="8" fill="{c}"/><circle class="k-o" cx="22" cy="-6" r="8" fill="{c}"/>'
        f'<circle cx="-16" cy="-11" r="2.6" fill="#ef5b56"/><circle cx="16" cy="-11" r="2.6" fill="#ef5b56"/>'
    )
    front = f'<path class="k-o" d="M-19 -1C-21 -24 21 -27 19 -1C14 -12 5 -15 -3 -11C-9 -9 -15 -6 -19 -1Z" fill="{c}"/>'
    return (front, back)


BOY = dict(hair=hair_short("#4a3226"), shirt="#4a9be8", pants="#3f5f9e", shoes="#ef5b56", skin=SKINS[0])
GIRL = dict(hair=hair_pigtails("#7a4a2a"), shirt="#f78fb3", pants="#6a44c2", shoes="#ffd23f", skin=SKINS[2])
BOY2 = dict(hair=hair_short("#2a1d16"), shirt="#5cc36a", pants="#3f5f9e", shoes="#4a9be8", skin=SKINS[3])
GIRL2 = dict(hair=hair_pigtails("#e0a24a"), shirt="#ffc93c", pants="#e0784a", shoes="#6a44c2", skin=SKINS[1])


def kid(k, head, neck, hip, arms, legs, tilt=0, mouth="smile", look="open", facing=1, props_back="", props_mid="", props_front=""):
    """arms/legs are (back, front) point lists; props_mid is drawn between the body and the front arm,
    props_front on top of everything."""
    front_hair, back_hair = k["hair"]
    hx, hy = head
    head_g = (
        f'<g transform="translate({fmt(hx)} {fmt(hy)}) rotate({tilt})">{back_hair}'
        f'<circle class="k-o" cx="0" cy="0" r="{HEAD_R}" fill="{k["skin"]}"/>'
        f"{face(mouth, look, k['skin'])}{front_hair}</g>"
    )
    return (
        props_back
        + arm(arms[0], k["shirt"], k["skin"])
        + leg(legs[0], k["pants"], k["shoes"], facing)
        + leg(legs[1], k["pants"], k["shoes"], facing)
        + dstroke(pts([neck, hip]), k["shirt"], 24)
        + head_g
        + props_mid
        + arm(arms[1], k["shirt"], k["skin"])
        + props_front
    )


# ---------------------------------------------------------------- props
def lines(segs, color=INK, w=3):
    return "".join(f'<path d="{pts(s)}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" fill="none" opacity=".45"/>' for s in segs)


def note(x, y, s=1.0, color="#6a44c2"):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M4 -14V4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M4 -14Q12 -12 13 -5" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        f'<ellipse cx="0" cy="4" rx="5.5" ry="4.2" fill="{color}" stroke="{INK}" stroke-width="2" transform="rotate(-20 0 4)"/></g>'
    )


def water_top(y, x0=-82, x1=82, amp=4, n=6):
    step = (x1 - x0) / n
    d = f"M{x0} {y}"
    for i in range(n):
        a = x0 + i * step
        d += f"Q{fmt(a + step / 4)} {y - amp} {fmt(a + step / 2)} {y}Q{fmt(a + step * 3 / 4)} {y + amp} {fmt(a + step)} {y}"
    return d


# ---------------------------------------------------------------- actions
def run():
    return (
        shadow(60, 34)
        + lines([[(-70, -20), (-48, -20)], [(-76, -4), (-52, -4)], [(-70, 12), (-50, 12)]])
        + kid(
            BOY, head=(6, -38), neck=(2, -18), hip=(-8, 12), tilt=8,
            arms=([(0, -14), (-16, -4), (-26, -16)], [(4, -14), (18, -2), (30, -12)]),
            legs=([(-8, 12), (-26, 28), (-40, 42)], [(-8, 12), (14, 22), (8, 50)]),
        )
    )


def jump():
    return (
        shadow(60, 26)
        + lines([[(-12, 46), (-12, 56)], [(0, 48), (0, 58)], [(12, 46), (12, 56)]])
        + kid(
            GIRL, head=(0, -36), neck=(0, -16), hip=(0, 10),
            arms=([(-4, -12), (-20, -26), (-30, -44)], [(4, -12), (20, -26), (30, -44)]),
            legs=([(-4, 10), (-18, 22), (-12, 36)], [(4, 10), (18, 22), (12, 36)]),
        )
    )


def swim():
    pool = f"{water_top(12, -76, 76)}V50Q76 58 68 58H-68Q-76 58 -76 50Z"
    water = (
        f'<path class="k-o" d="{pool}" fill="#8ed1f5" opacity=".92"/>'
        f'<path d="{water_top(30, -56, 56, 3, 4)}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
        f'<path d="{water_top(44, -30, 62, 3, 4)}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
    )
    splash = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#4a9be8" stroke-width="2"/>'
        for x, y, r in ((58, 4, 4), (66, -2, 3), (52, -4, 2.5), (-30, -44, 3), (-38, -38, 2.5))
    )
    body = kid(
        BOY2, head=(-30, -6), neck=(-8, 8), hip=(32, 14), tilt=-10,
        arms=([(-6, 8), (-18, 18), (-32, 22)], [(-2, 6), (2, -24), (-16, -38)]),
        legs=([(32, 14), (46, 14), (60, 10)], [(32, 14), (46, 18), (60, 20)]),
    )
    return body + water + splash


def dance():
    return (
        shadow(60, 28)
        + note(-50, -40, 1.1) + note(46, -48, 0.9, "#ef5b56") + note(54, 0, 0.8, "#2fa39a")
        + kid(
            GIRL2, head=(-4, -38), neck=(0, -18), hip=(4, 10), tilt=-12,
            arms=([(-2, -14), (-20, -18), (-30, -36)], [(2, -14), (18, -6), (10, 4)]),
            legs=([(4, 10), (-4, 30), (-8, 52)], [(4, 10), (24, 18), (20, 38)]),
        )
    )


def sing():
    mic = (
        f'<path d="M11 -22L12 -8" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<path d="M11 -22L12 -8" stroke="#555a66" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="11" cy="-24" r="6" fill="#c9c2cc" stroke="{INK}" stroke-width="2.5"/>'
    )
    return (
        shadow(60, 28)
        + note(34, -44, 1.1) + note(52, -18, 0.9, "#ef5b56") + note(-40, -40, 0.8, "#2fa39a")
        + kid(
            GIRL, head=(0, -34), neck=(0, -14), hip=(0, 14), mouth="open", look="shut",
            arms=([(-4, -10), (-20, 2), (-30, -10)], [(4, -10), (20, 2), (12, -10)]),
            legs=([(-4, 14), (-8, 32), (-10, 52)], [(4, 14), (8, 32), (10, 52)]),
            props_mid=mic,
        )
    )


def read():
    book = (
        '<path class="k-o" d="M-26 -2L0 2L26 -2V24L0 28L-26 24Z" fill="#ef5b56"/>'
        '<path class="k-o" d="M-23 -3L-1 0V24L-23 21Z" fill="#fff" stroke-width="2"/>'
        '<path class="k-o" d="M23 -3L1 0V24L23 21Z" fill="#fff" stroke-width="2"/>'
        '<path d="M-19 4L-5 6M-19 10L-5 12M-19 16L-9 17M19 4L5 6M19 10L5 12M19 16L9 17" stroke="#c9c2cc" stroke-width="2" stroke-linecap="round"/>'
    )
    return (
        shadow(60, 30)
        + kid(
            BOY, head=(0, -38), neck=(0, -18), hip=(0, 12), look="down", tilt=4,
            arms=([(-4, -14), (-24, 0), (-28, 8)], [(4, -14), (24, 0), (28, 8)]),
            legs=([(-4, 12), (-8, 32), (-10, 52)], [(4, 12), (8, 32), (10, 52)]),
            props_front=f'<g transform="translate(0 -4)">{book}</g>',
        )
    )


def draw():
    easel = (
        f'<path d="M24 60L40 -40M72 60L56 -40M48 -44V60" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        f'<path d="M24 60L40 -40M72 60L56 -40M48 -44V60" stroke="#c98a4b" stroke-width="3" stroke-linecap="round"/>'
        '<rect class="k-o" x="22" y="-46" width="54" height="56" rx="3" fill="#fff"/>'
        f'<rect x="22" y="8" width="54" height="6" rx="2" fill="#c98a4b" stroke="{INK}" stroke-width="2.5"/>'
        '<circle cx="36" cy="-32" r="7" fill="#ffd23f"/>'
        '<path d="M34 -4V-16L48 -26L62 -16V-4Z" fill="none" stroke="#ef5b56" stroke-width="3" stroke-linejoin="round"/>'
        '<path d="M44 -4V-12H52V-4" fill="none" stroke="#4a9be8" stroke-width="3" stroke-linejoin="round"/>'
        '<path d="M26 2H72" stroke="#5cc36a" stroke-width="3" stroke-linecap="round"/>'
    )
    crayon = (
        f'<g transform="translate(20 -18) rotate(-40)">'
        f'<rect x="-3.5" y="-2" width="7" height="18" rx="1.5" fill="#6a44c2" stroke="{INK}" stroke-width="2"/>'
        f'<path d="M-3.5 -2L0 -9L3.5 -2Z" fill="#6a44c2" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/></g>'
    )
    return (
        shadow(60, 60)
        + easel
        + kid(
            GIRL2, head=(-34, -36), neck=(-32, -16), hip=(-34, 14), tilt=6,
            arms=([(-34, -12), (-50, 2), (-44, 14)], [(-28, -12), (-6, -14), (14, -16)]),
            legs=([(-36, 14), (-40, 32), (-42, 52)], [(-32, 14), (-28, 32), (-26, 52)]),
            props_mid=crayon,
        )
    )


def kick():
    b = f'<g transform="translate(52 -8) scale(.3)">{ball()}</g>'
    return (
        shadow(60, 44)
        + lines([[(20, -16), (32, -12)], [(18, -4), (32, -4)], [(20, 8), (32, 4)]])
        + b
        + kid(
            BOY2, head=(-18, -38), neck=(-18, -18), hip=(-16, 12), tilt=-6,
            arms=([(-20, -14), (-38, -4), (-48, -16)], [(-14, -14), (2, -18), (12, -30)]),
            legs=([(-18, 12), (-20, 32), (-22, 52)], [(-14, 12), (4, 26), (22, 18)]),
        )
    )


ACTIONS = [
    ("run", run), ("jump", jump), ("swim", swim), ("dance", dance),
    ("sing", sing), ("read", read), ("draw", draw), ("kick", kick),
]
