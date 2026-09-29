"""Jobs and things in my room. Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
import math
from common import INK, fmt
from build1 import shadow
from build4 import cloud
from build5 import dstroke, star
from build8 import person, glasses

# A few skin tones so the jobs show different people.
SKINS = ["#ffd2b0", "#e8b48a", "#c68a5e", "#8d5a3b"]
GLASS = "#cdeeff"
WOOD, WOOD_DARK = "#c98a4b", "#a86c34"
S = 0.88  # people with hats are drawn a little smaller so the hat fits


def short_hair(fill):
    return f'<path class="k-o" d="M-31 -16C-34 -46 -14 -54 2 -52C22 -52 34 -42 31 -16C26 -28 16 -34 4 -32C-8 -38 -22 -32 -31 -16Z" fill="{fill}"/>'


def long_hair_back(fill):
    return f'<path class="k-o" d="M-36 -14C-40 -54 40 -54 36 -14C38 8 42 26 38 36H-38C-42 26 -38 8 -36 -14Z" fill="{fill}"/>'


def bangs(fill):
    return f'<path class="k-o" d="M-32 -12C-34 -46 32 -52 32 -10C24 -28 6 -34 -6 -26C-14 -22 -24 -18 -32 -12Z" fill="{fill}"/>'


def lapels(fill):
    return (
        f'<path class="k-o" d="M-14 23L-4 60H-30Q-40 40 -30 26Z" fill="{fill}" stroke-width="2.5"/>'
        f'<path class="k-o" d="M14 23L4 60H30Q40 40 30 26Z" fill="{fill}" stroke-width="2.5"/>'
    )


def cap(top, band, badge):
    """Peaked cap sitting on the head (head top at y -44)."""
    return (
        f'<path class="k-o" d="M-34 -36C-40 -58 -20 -70 0 -70C20 -70 40 -58 34 -36Z" fill="{top}"/>'
        f'<rect class="k-o" x="-33" y="-42" width="66" height="10" rx="3" fill="{band}"/>'
        f'<path class="k-o" d="M-30 -32Q0 -22 30 -32L34 -28Q0 -14 -34 -28Z" fill="{INK}" stroke-width="2"/>'
        + badge
    )


# ================================================================ jobs
def doctor():
    steth = (
        f'<path d="M-16 24Q-20 44 -6 48Q6 50 8 38" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        f'<path d="M16 24Q20 36 14 42" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        f'<circle cx="8" cy="40" r="6" fill="#c9c2cc" stroke="{INK}" stroke-width="2.5"/>'
    )
    return person("#fff", front=short_hair("#3b2a20"), extra=lapels("#fff") + '<path d="M-10 26L0 38L10 26" fill="#8ec5ff"/>' + steth, skin=SKINS[1])


def nurse():
    hat = (
        '<path class="k-o" d="M-24 -40L-20 -62H20L24 -40Q0 -34 -24 -40Z" fill="#fff"/>'
        '<path d="M-4 -58H4V-54H8V-46H4V-42H-4V-46H-8V-54H-4Z" fill="#ef4f5a"/>'
    )
    return person("#8ec5ff", back=long_hair_back("#4a3226"), front=bangs("#4a3226"),
                  extra='<path d="M-14 23L0 40L14 23" fill="none" stroke="#fff" stroke-width="3"/>' + hat, s=S, skin=SKINS[0])


def teacher():
    book = (
        '<path class="k-o" d="M-34 40L0 34L34 40V64H-34Z" fill="#ef5b56"/>'
        '<path class="k-o" d="M-30 38L-2 33V60L-30 62Z" fill="#fff" stroke-width="2"/>'
        '<path class="k-o" d="M30 38L2 33V60L30 62Z" fill="#fff" stroke-width="2"/>'
        '<path d="M-24 42L-8 40M-24 48L-8 46M24 42L8 40M24 48L8 46" stroke="#c9c2cc" stroke-width="2" stroke-linecap="round"/>'
    )
    bun = '<circle class="k-o" cx="0" cy="-50" r="11" fill="#7a4a2a"/>'
    front = '<path class="k-o" d="M-33 -10C-38 -46 38 -46 33 -10C28 -26 16 -32 0 -30C-16 -32 -28 -26 -33 -10Z" fill="#7a4a2a"/>'
    return person("#5cc36a", back=bun, front=front, extra=glasses() + book, skin=SKINS[2])


def cook():
    hat = (
        '<rect class="k-o" x="-28" y="-50" width="56" height="14" rx="3" fill="#fff"/>'
        '<path class="k-o" d="M-26 -50C-42 -52 -42 -72 -26 -70C-22 -82 -6 -82 0 -74C6 -82 22 -82 26 -70C42 -72 42 -52 26 -50Z" fill="#fff"/>'
        '<path d="M-10 -52V-64M10 -52V-64" stroke="#dde3ea" stroke-width="3" stroke-linecap="round"/>'
    )
    scarf = '<path class="k-o" d="M-14 22Q0 32 14 22L10 34Q0 38 -10 34Z" fill="#ef5b56" stroke-width="2.5"/>'
    buttons = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{INK}"/>' for x in (-12, 12) for y in (44, 54))
    return person("#fff", front=short_hair("#3b2a20"), extra=hat + scarf + buttons, s=S, skin=SKINS[3])


def farmer():
    straw = "#f2c96b"
    hat = (
        f'<ellipse class="k-o" cx="0" cy="-38" rx="50" ry="10" fill="{straw}"/>'
        f'<path class="k-o" d="M-26 -38C-26 -64 26 -64 26 -38Z" fill="{straw}"/>'
        '<path d="M-25 -44H25" stroke="#ef5b56" stroke-width="6"/>'
    )
    shirt = "#ef5b56"
    checks = "".join(f'<path d="M{x} 26V60" stroke="#c9403b" stroke-width="3"/>' for x in (-40, -28, 28, 40))
    overalls = (
        '<path class="k-o" d="M-22 40H22V62H-22Z" fill="#4a9be8"/>'
        '<path class="k-o" d="M-22 42L-18 24H-10L-12 42ZM22 42L18 24H10L12 42Z" fill="#4a9be8" stroke-width="2.5"/>'
        '<circle cx="-15" cy="40" r="3" fill="#ffd23f" stroke="#3f3345" stroke-width="1.5"/><circle cx="15" cy="40" r="3" fill="#ffd23f" stroke="#3f3345" stroke-width="1.5"/>'
    )
    straw_bit = f'<path d="M6 -2L22 6" stroke="#e8b520" stroke-width="3" stroke-linecap="round"/>'
    return person(shirt, front=short_hair("#a8704a"), extra=checks + overalls + hat + straw_bit, s=S, skin=SKINS[1])


def pilot():
    wings = (
        '<path d="M8 36H34M12 40H30" stroke="#ffc93c" stroke-width="3" stroke-linecap="round"/>'
        '<circle cx="21" cy="37" r="3.5" fill="#ffc93c" stroke="#3f3345" stroke-width="1.5"/>'
    )
    tie = f'<path class="k-o" d="M-5 24H5L7 50L0 58L-7 50Z" fill="#2f4a7a" stroke-width="2"/>'
    jacket = lapels("#2f4a7a")
    badge = '<path class="k-o" d="M-12 -52H12M-8 -56L0 -50L8 -56" fill="none" stroke="#ffc93c" stroke-width="3"/>'
    return person("#fff", front=short_hair("#2a1d16"), extra=jacket + tie + wings + cap("#fff", "#2f4a7a", badge), s=S, skin=SKINS[2])


def police():
    badge_cap = star(0, -54, 8, "#ffc93c", 1.5)
    chest = star(24, 40, 8, "#ffc93c", 1.5)
    pockets = '<path d="M-38 36H-18M18 48H36" stroke="#1f3561" stroke-width="3" stroke-linecap="round"/>'
    return person("#2f5aa8", back=long_hair_back("#3b2a20"), front=bangs("#3b2a20"),
                  extra=pockets + chest + cap("#2f5aa8", "#1f3561", badge_cap), s=S, skin=SKINS[3])


def firefighter():
    helmet = (
        '<path class="k-o" d="M-44 -30Q-40 -34 -32 -34C-34 -62 -16 -72 0 -72C16 -72 34 -62 32 -34C40 -34 44 -30 44 -26Q0 -18 -44 -26Z" fill="#ef4f5a"/>'
        '<path d="M0 -70V-38" stroke="#c9403b" stroke-width="4" stroke-linecap="round"/>'
        '<path class="k-o" d="M-12 -62H12V-44Q0 -38 -12 -44Z" fill="#ffc93c"/>'
        '<path d="M-5 -55L0 -50L5 -55" fill="none" stroke="#ef4f5a" stroke-width="2.5" stroke-linecap="round"/>'
    )
    stripes = '<path d="M-50 46H50M-47 38H-24M24 38H47" stroke="#ffd23f" stroke-width="5"/><path d="M-50 50H50" stroke="#c9c2cc" stroke-width="2"/>'
    coat_close = f'<path d="M0 26V62" stroke="{INK}" stroke-width="2.5"/>'
    return person("#e0a24a", front=short_hair("#4a3226"), extra=stripes + coat_close + helmet, s=S, skin=SKINS[0])


JOBS = [
    ("doctor", doctor), ("nurse", nurse), ("teacher", teacher), ("cook", cook),
    ("farmer", farmer), ("pilot", pilot), ("police officer", police), ("firefighter", firefighter),
]


# ================================================================ my room
def bed():
    return (
        shadow(52, 66)
        + f'<rect class="k-o" x="-68" y="-44" width="16" height="92" rx="6" fill="{WOOD}"/>'
        + f'<rect class="k-o" x="54" y="-10" width="14" height="58" rx="5" fill="{WOOD}"/>'
        + f'<rect class="k-o" x="-54" y="6" width="110" height="28" rx="4" fill="{WOOD_DARK}"/>'
        + '<rect class="k-o" x="-54" y="-6" width="110" height="16" rx="6" fill="#fff"/>'
        + '<ellipse class="k-o" cx="-32" cy="-14" rx="18" ry="11" fill="#fff"/>'
        + '<path class="k-o" d="M-12 -12Q20 -18 56 -12V22H-12Z" fill="#4a9be8"/>'
        + "".join(star(x, y, 5, "#ffd23f", 1.2) for x, y in ((8, 0), (30, 10), (44, -4)))
        + '<path d="M-12 -2V22" stroke="#2f7cc6" stroke-width="3"/>'
    )


def chair():
    return (
        shadow(58, 44)
        + f'<rect class="k-o" x="-34" y="10" width="9" height="46" rx="3" fill="{WOOD_DARK}"/><rect class="k-o" x="25" y="10" width="9" height="46" rx="3" fill="{WOOD_DARK}"/>'
        + f'<rect class="k-o" x="-32" y="-62" width="9" height="70" rx="3" fill="{WOOD}"/><rect class="k-o" x="23" y="-62" width="9" height="70" rx="3" fill="{WOOD}"/>'
        + f'<rect class="k-o" x="-32" y="-62" width="64" height="16" rx="6" fill="{WOOD}"/>'
        + f'<path d="M-12 -46V-6M0 -46V-6M12 -46V-6" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<rect class="k-o" x="-40" y="-6" width="80" height="16" rx="5" fill="{WOOD}"/>'
        + '<rect class="k-o" x="-34" y="-14" width="68" height="12" rx="6" fill="#ef5b56"/>'
    )


def table():
    return (
        shadow(58, 64)
        + "".join(f'<rect class="k-o" x="{x}" y="0" width="10" height="56" rx="3" fill="{WOOD_DARK}"/>' for x in (-54, 44))
        + "".join(f'<rect class="k-o" x="{x}" y="-4" width="8" height="44" rx="3" fill="{WOOD_DARK}"/>' for x in (-38, 30))
        + f'<path class="k-o" d="M-62 -14L-46 -28H46L62 -14Z" fill="#e0a86a"/>'
        + f'<rect class="k-o" x="-64" y="-14" width="128" height="12" rx="3" fill="{WOOD}"/>'
        + '<path class="k-o" d="M-10 -28Q-14 -40 -8 -48H8Q14 -40 10 -28Z" fill="#9fd8f5"/>'
        + dstroke("M0 -48V-58", "#5cc36a", 3)
        + '<circle class="k-o" cx="0" cy="-62" r="6" fill="#f78fb3" stroke-width="2"/><circle cx="0" cy="-62" r="2.5" fill="#ffd23f"/>'
        + '<path class="k-o" d="M24 -28H40V-40H24Z" fill="#fff" stroke-width="2.5"/><path d="M40 -36Q46 -34 40 -30" fill="none" stroke="#3f3345" stroke-width="2.5"/>'
    )


def sofa():
    return (
        shadow(52, 66)
        + f'<rect x="-56" y="36" width="8" height="12" rx="2" fill="{WOOD_DARK}" stroke="{INK}" stroke-width="2"/><rect x="48" y="36" width="8" height="12" rx="2" fill="{WOOD_DARK}" stroke="{INK}" stroke-width="2"/>'
        + '<rect class="k-o" x="-56" y="-34" width="112" height="46" rx="14" fill="#4fc1b9"/>'
        + '<path d="M0 -30V10" stroke="#35a39b" stroke-width="3" stroke-linecap="round"/>'
        + '<rect class="k-o" x="-54" y="4" width="54" height="22" rx="8" fill="#6fd3cb"/><rect class="k-o" x="0" y="4" width="54" height="22" rx="8" fill="#6fd3cb"/>'
        + '<rect class="k-o" x="-70" y="-14" width="22" height="54" rx="10" fill="#4fc1b9"/><rect class="k-o" x="48" y="-14" width="22" height="54" rx="10" fill="#4fc1b9"/>'
        + '<rect class="k-o" x="-42" y="-20" width="26" height="24" rx="6" fill="#ffd23f" transform="rotate(-12 -29 -8)"/>'
    )


def lamp():
    rays = "".join(
        f'<path d="M{fmt(30 * math.cos(a))} {fmt(-6 + 30 * math.sin(a))}L{fmt(40 * math.cos(a))} {fmt(-6 + 40 * math.sin(a))}" stroke="#ffc93c" stroke-width="4" stroke-linecap="round"/>'
        for a in (math.radians(d) for d in (140, 160, 20, 40))
    )
    return (
        shadow(58, 40)
        + '<ellipse cx="0" cy="-6" rx="36" ry="10" fill="#fff3b0" opacity=".9"/>'
        + rays
        + dstroke("M0 -8V48", "#8b5a3c", 5)
        + '<ellipse class="k-o" cx="0" cy="50" rx="30" ry="8" fill="#8b5a3c"/>'
        + '<path class="k-o" d="M-24 -58H24L40 -10H-40Z" fill="#ffc93c"/>'
        + '<path d="M-36 -18H36" stroke="#e8b520" stroke-width="4"/>'
        + '<path d="M-14 -50L-24 -22" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    )


def clock():
    ticks = ""
    for k in range(12):
        a = math.radians(k * 30 - 90)
        r1 = 36 if k % 3 else 32
        ticks += f'<path d="M{fmt(r1 * math.cos(a))} {fmt(r1 * math.sin(a))}L{fmt(41 * math.cos(a))} {fmt(41 * math.sin(a))}" stroke="{INK}" stroke-width="{3 if k % 3 == 0 else 2}" stroke-linecap="round"/>'
    nums = "".join(
        f'<text class="k-f" x="{x}" y="{y}" font-size="13" text-anchor="middle" fill="{INK}">{n}</text>'
        for n, x, y in (("12", 0, -18), ("3", 24, 5), ("6", 0, 29), ("9", -24, 5))
    )
    return (
        shadow(60, 36)
        + '<circle class="k-o" cx="0" cy="0" r="52" fill="#ef5b56"/>'
        + '<circle class="k-o" cx="0" cy="0" r="44" fill="#fff"/>'
        + ticks + nums
        + f'<path d="M0 0L18 8M0 0V-28" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        + f'<path d="M0 0L-20 22" stroke="#ef5b56" stroke-width="2" stroke-linecap="round"/>'
        + f'<circle cx="0" cy="0" r="4" fill="{INK}"/>'
    )


def door():
    return (
        '<rect x="-70" y="54" width="140" height="6" rx="3" fill="#e8dccb"/>'
        + '<rect class="k-o" x="-40" y="-66" width="80" height="122" rx="4" fill="#e8dccb"/>'
        + f'<rect class="k-o" x="-32" y="-58" width="64" height="112" rx="3" fill="{WOOD}"/>'
        + "".join(f'<rect x="{x}" y="{y}" width="22" height="{h}" rx="3" fill="none" stroke="{WOOD_DARK}" stroke-width="3"/>' for x in (-24, 2) for y, h in ((-50, 42), (0, 46)))
        + '<circle class="k-o" cx="22" cy="0" r="5" fill="#ffc93c" stroke-width="2"/>'
        + '<rect class="k-o" x="-52" y="50" width="104" height="10" rx="4" fill="#5cc36a" stroke-width="2.5"/>'
    )


def window():
    return (
        '<rect class="k-o" x="-50" y="-54" width="100" height="96" rx="6" fill="#fff"/>'
        + '<rect x="-42" y="-46" width="84" height="80" fill="#8ec5ff"/>'
        + '<circle cx="22" cy="-26" r="10" fill="#ffd23f"/>'
        + cloud(-10, -8, 0.4)
        + '<path d="M-42 34Q-20 22 0 30T42 26V34H-42Z" fill="#5cc36a"/>'
        + f'<path d="M0 -46V34M-42 -6H42" stroke="#fff" stroke-width="6"/>'
        + f'<rect x="-42" y="-46" width="84" height="80" fill="none" stroke="{INK}" stroke-width="2.5"/>'
        + '<path class="k-o" d="M-60 -60H-34Q-38 -10 -30 44H-60Z" fill="#f78fb3"/>'
        + '<path class="k-o" d="M60 -60H34Q38 -10 30 44H60Z" fill="#f78fb3"/>'
        + '<rect class="k-o" x="-66" y="-66" width="132" height="10" rx="5" fill="#a86c34"/>'
        + '<rect class="k-o" x="-58" y="42" width="116" height="10" rx="3" fill="#fff"/>'
    )


ROOM = [
    ("bed", bed), ("chair", chair), ("table", table), ("sofa", sofa),
    ("lamp", lamp), ("clock", clock), ("door", door), ("window", window),
]
