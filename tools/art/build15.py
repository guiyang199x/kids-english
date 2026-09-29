"""More picture-dictionary scenes: a kitchen, a beach and a classroom.
Same frame as the sunny day (build4): a 640x440 picture at (20, 12) with tappable word labels.
Each scene is (parts, labels); labels are (word, pill x, pill y, point the leader line at)."""
import math
from common import INK, fmt
from build4 import cloud, sun, pill
from build5 import dstroke, star

SX, SY, SW, SH = 20, 12, 640, 440
WOOD, WOOD_DARK = "#e0a86a", "#c98a4b"


def ko(tag, **a):
    """<tag class="k-o" ...> with keyword attributes (fill, d, x, ...)."""
    attrs = " ".join(f'{k.replace("_", "-")}="{fmt(v) if isinstance(v, float) else v}"' for k, v in a.items())
    return f'<{tag} class="k-o" {attrs}/>'


def steam(x, y, n=3, gap=12):
    return "".join(
        f'<path d="M{x + i * gap} {y}q-6 -8 0 -16q6 -8 0 -16" fill="none" stroke="#c9c2cc" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
        for i in range(n)
    )


# ================================================================ kitchen
def fridge(x0=36, y0=78, x1=146, y1=374):
    return (
        ko("rect", x=x0, y=y0, width=x1 - x0, height=y1 - y0, rx=14, fill="#eaf6ff")
        + f'<path d="M{x0} {y0 + 100}H{x1}" stroke="{INK}" stroke-width="3"/>'
        + ko("rect", x=x1 - 22, y=y0 + 30, width=9, height=44, rx=4, fill="#b8c6d6")
        + ko("rect", x=x1 - 22, y=y0 + 124, width=9, height=70, rx=4, fill="#b8c6d6")
        # a drawing held on with a magnet
        + ko("rect", x=x0 + 18, y=y0 + 150, width=46, height=54, rx=2, fill="#fff", stroke_width=2)
        + f'<path d="M{x0 + 26} {y0 + 190}V{y0 + 176}L{x0 + 41} {y0 + 164}L{x0 + 56} {y0 + 176}V{y0 + 190}Z" fill="none" stroke="#ef5b56" stroke-width="2.5" stroke-linejoin="round"/>'
        + f'<circle cx="{x0 + 41}" cy="{y0 + 150}" r="5" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="{x0 + 28}" cy="{y0 + 40}" r="6" fill="#5cc36a" stroke="{INK}" stroke-width="2"/>'
        + f'<circle cx="{x0 + 46}" cy="{y0 + 54}" r="6" fill="#f78fb3" stroke="{INK}" stroke-width="2"/>'
    )


def kitchen_window(x0=214, y0=48, x1=346, y1=180):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return (
        ko("rect", x=x0 - 6, y=y0 - 6, width=x1 - x0 + 12, height=y1 - y0 + 12, rx=8, fill="#fff")
        + f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#cdeeff" stroke="{INK}" stroke-width="2.5"/>'
        + cloud(mx - 20, y0 + 40, 0.45)
        + f'<path d="M{mx} {y0}V{y1}M{x0} {my}H{x1}" stroke="#fff" stroke-width="7"/>'
        + f'<path d="M{mx} {y0}V{y1}M{x0} {my}H{x1}" stroke="{INK}" stroke-width="2" opacity=".35"/>'
        + ko("rect", x=x0 - 14, y=y1 + 4, width=x1 - x0 + 28, height=10, rx=4, fill="#fff")
        + f'<path class="k-o" d="M{x1 - 34} {y1 + 4}C{x1 - 36} {y1 - 8} {x1 - 20} {y1 - 12} {x1 - 18} {y1 + 4}Z" fill="#e0784a"/>'
        + dstroke(f"M{x1 - 26} {y1 - 8}Q{x1 - 30} {y1 - 24} {x1 - 20} {y1 - 30}", "#5cc36a", 3)
    )


def counter(top=276):
    doors = "".join(
        ko("rect", x=x + 6, y=top + 24, width=78, height=66, rx=6, fill="#f2c58e", stroke_width=2.5)
        + f'<circle cx="{x + 72}" cy="{top + 40}" r="4" fill="{INK}"/>'
        for x in (150, 240, 330, 560)
    )
    return (
        ko("rect", x=150, y=top + 14, width=520, height=84, fill=WOOD)
        + doors
        + ko("rect", x=144, y=top, width=530, height=16, rx=4, fill="#f7f3ee")
    )


def sink(cx=280, top=276):
    return (
        f'<rect x="{cx - 46}" y="{top + 3}" width="92" height="9" rx="4" fill="#9aa3b2" stroke="{INK}" stroke-width="2"/>'
        + dstroke(f"M{cx + 16} {top}V{top - 36}Q{cx + 16} {top - 46} {cx + 4} {top - 46}Q{cx - 8} {top - 46} {cx - 8} {top - 34}", "#c9d3df", 6)
        + ko("rect", x=cx + 22, y=top - 12, width=12, height=10, rx=3, fill="#c9d3df", stroke_width=2)
        + "".join(f'<circle cx="{cx - 8}" cy="{top - 24 + i * 8}" r="2" fill="#4a9be8"/>' for i in range(3))
    )


def fruit_bowl(cx=190, top=276):
    return (
        ko("path", d=f"M{cx - 10} {top - 22}C{cx - 22} {top - 50} {cx + 6} {top - 58} {cx + 14} {top - 42}C{cx + 4} {top - 46} {cx - 6} {top - 40} {cx - 4} {top - 22}Z", fill="#ffd23f")
        + ko("circle", cx=cx - 16, cy=top - 26, r=12, fill="#ef5b56")
        + ko("circle", cx=cx + 14, cy=top - 26, r=12, fill="#ff9a3c")
        + ko("path", d=f"M{cx - 34} {top - 22}H{cx + 34}C{cx + 32} {top - 2} {cx + 18} {top} {cx} {top}C{cx - 18} {top} {cx - 32} {top - 2} {cx - 34} {top - 22}Z", fill="#4fc1b9")
        + f'<path d="M{cx - 26} {top - 14}H{cx + 26}" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    )


def utensil_jar(cx=372, top=276):
    spoon = dstroke(f"M{cx - 4} {top - 30}L{cx - 14} {top - 60}", "#c9d3df", 4) + ko("ellipse", cx=cx - 17, cy=top - 68, rx=7, ry=10, fill="#c9d3df", transform=f"rotate(-18 {cx - 17} {top - 68})", stroke_width=2.5)
    fork = (
        dstroke(f"M{cx + 4} {top - 30}L{cx + 12} {top - 58}", "#c9d3df", 4)
        + f'<path d="M{cx + 6} {top - 58}L{cx + 10} {top - 74}M{cx + 12} {top - 58}L{cx + 15} {top - 74}M{cx + 17} {top - 58}L{cx + 20} {top - 73}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M{cx + 6} {top - 58}L{cx + 10} {top - 74}M{cx + 12} {top - 58}L{cx + 15} {top - 74}M{cx + 17} {top - 58}L{cx + 20} {top - 73}" stroke="#c9d3df" stroke-width="2" stroke-linecap="round"/>'
        + ko("path", d=f"M{cx + 4} {top - 56}H{cx + 20}L{cx + 18} {top - 50}H{cx + 6}Z", fill="#c9d3df", stroke_width=2)
    )
    return spoon + fork + ko("rect", x=cx - 16, y=top - 36, width=32, height=36, rx=6, fill="#ffd23f") + f'<path d="M{cx - 10} {top - 22}H{cx + 10}" stroke="#e8b520" stroke-width="3"/>'


def stove(x0=420, x1=540, top=276):
    knobs = "".join(ko("circle", cx=x0 + 22 + i * 25, cy=top + 26, r=5, fill="#3f4450", stroke_width=2) for i in range(4))
    return (
        ko("rect", x=x0, y=top + 14, width=x1 - x0, height=84, fill="#dfe3ea")
        + ko("rect", x=x0 - 2, y=top, width=x1 - x0 + 4, height=16, rx=4, fill="#3f4450")
        + knobs
        + ko("rect", x=x0 + 16, y=top + 40, width=x1 - x0 - 32, height=46, rx=6, fill="#3f4450")
        + f'<path d="M{x0 + 26} {top + 50}L{x0 + 44} {top + 50}" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".4"/>'
        + ko("rect", x=x0 + 30, y=top + 34, width=x1 - x0 - 60, height=6, rx=3, fill="#b8c6d6", stroke_width=2)
    )


def pot(cx=452, top=276):
    return (
        steam(cx - 14, top - 38)
        + ko("rect", x=cx - 38, y=top - 28, width=10, height=8, rx=3, fill="#c9403b", stroke_width=2)
        + ko("rect", x=cx + 28, y=top - 28, width=10, height=8, rx=3, fill="#c9403b", stroke_width=2)
        + ko("path", d=f"M{cx - 30} {top - 32}H{cx + 30}V{top - 6}Q{cx + 30} {top} {cx + 24} {top}H{cx - 24}Q{cx - 30} {top} {cx - 30} {top - 6}Z", fill="#ef5b56")
        + ko("path", d=f"M{cx - 33} {top - 32}Q{cx} {top - 46} {cx + 33} {top - 32}Z", fill="#f07b76")
        + ko("circle", cx=cx, cy=top - 42, r=5, fill="#3f4450", stroke_width=2)
    )


def kettle(cx=512, top=276):
    return (
        dstroke(f"M{cx - 14} {top - 38}Q{cx} {top - 64} {cx + 14} {top - 38}", "#3f4450", 4)
        + ko("path", d=f"M{cx + 16} {top - 18}L{cx + 34} {top - 34}L{cx + 36} {top - 28}L{cx + 22} {top - 8}Z", fill="#4a9be8", stroke_width=2.5)
        + ko("path", d=f"M{cx - 24} {top}C{cx - 26} {top - 26} {cx - 14} {top - 40} {cx} {top - 40}C{cx + 14} {top - 40} {cx + 26} {top - 26} {cx + 24} {top}Z", fill="#4a9be8")
        + ko("circle", cx=cx, cy=top - 42, r=5, fill="#3f4450", stroke_width=2)
        + f'<path d="M{cx - 14} {top - 24}Q{cx - 12} {top - 32} {cx - 4} {top - 34}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    )


def shelf_with_plates(x0=420, x1=640, y=178):
    plates = "".join(
        ko("circle", cx=cx, cy=y - 22, r=21, fill="#fff")
        + f'<circle cx="{cx}" cy="{y - 22}" r="13" fill="none" stroke="#ef5b56" stroke-width="2" stroke-dasharray="4 3"/>'
        for cx in (462, 504, 546)
    )
    return (
        plates
        + ko("rect", x=x0, y=y, width=x1 - x0 + 30, height=10, rx=3, fill=WOOD)
        + "".join(ko("path", d=f"M{x} {y + 10}V{y + 26}L{x + 14} {y + 10}Z", fill=WOOD_DARK, stroke_width=2) for x in (434, 600))
        + ko("rect", x=580, y=y - 30, width=18, height=30, rx=3, fill="#fff", stroke_width=2.5)
        + ko("rect", x=602, y=y - 38, width=20, height=38, rx=3, fill="#ffd23f", stroke_width=2.5)
    )


def cup(cx=604, top=276):
    return (
        steam(cx - 8, top - 36, 2, 14)
        + dstroke(f"M{cx + 15} {top - 24}C{cx + 28} {top - 24} {cx + 28} {top - 8} {cx + 15} {top - 8}", "#f78fb3", 4)
        + ko("path", d=f"M{cx - 16} {top - 32}H{cx + 16}V{top - 6}Q{cx + 16} {top} {cx + 10} {top}H{cx - 10}Q{cx - 16} {top} {cx - 16} {top - 6}Z", fill="#f78fb3")
        + '<path d="M{0} {1}c-3 -4 -8 -1 -4 3l4 4l4 -4c4 -4 -1 -7 -4 -3z" fill="#fff"/>'.format(cx, top - 20)
    )


def kitchen():
    tiles = "".join(f'<path d="M150 {y}H660" stroke="#f1d9b2" stroke-width="2"/>' for y in range(200, 276, 19))
    tiles += "".join(f'<path d="M{x} 200V276" stroke="#f1d9b2" stroke-width="2"/>' for x in range(170, 660, 38))
    floor = "".join(f'<path d="M{x} 374L{x - 30 + (x - 340) * 0.3:.0f} 452" stroke="#d9b07c" stroke-width="2"/>' for x in range(60, 660, 60))
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#fff1d6"/>',
        '<rect x="150" y="196" width="510" height="80" fill="#fdf6ea"/>',
        tiles,
        '<rect x="20" y="374" width="640" height="78" fill="#efcf9f"/>',
        floor,
        f'<path d="M20 374H660" stroke="{INK}" stroke-width="3"/>',
        kitchen_window(),
        shelf_with_plates(),
        fridge(),
        counter(),
        stove(),
        sink(),
        fruit_bowl(),
        utensil_jar(),
        pot(),
        kettle(),
        cup(),
    ]
    labels = [
        ("fridge", 91, 50, (91, 100)),
        ("bowl", 192, 206, (192, 244)),
        ("sink", 262, 214, (262, 282)),
        ("spoon", 372, 184, (355, 206)),
        ("pot", 432, 206, (446, 240)),
        ("kettle", 560, 212, (524, 244)),
        ("plate", 504, 104, (504, 134)),
        ("cup", 628, 226, (606, 250)),
        ("stove", 480, 410, (480, 344)),
    ]
    return parts, labels


# ================================================================ beach
def seagull(x, y, s=1.0):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        + ko("path", d="M-4 0C-14 -16 -30 -18 -42 -10C-30 -10 -18 -4 -10 6Z", fill="#dfe3ea")
        + ko("path", d="M4 0C14 -18 32 -22 44 -14C32 -12 20 -4 12 6Z", fill="#dfe3ea")
        + ko("ellipse", cx=0, cy=4, rx=16, ry=9, fill="#fff")
        + ko("circle", cx=-14, cy=-2, r=7, fill="#fff")
        + ko("path", d="M-20 -2L-30 1L-20 3Z", fill="#ffc93c", stroke_width=2)
        + f'<circle cx="-15" cy="-4" r="1.8" fill="{INK}"/></g>'
    )


def sailboat(cx=486, y=184):
    return (
        dstroke(f"M{cx} {y - 4}V{y - 78}", "#a8704a", 3)
        + ko("path", d=f"M{cx + 4} {y - 74}L{cx + 44} {y - 12}H{cx + 4}Z", fill="#fff")
        + ko("path", d=f"M{cx - 4} {y - 62}L{cx - 32} {y - 12}H{cx - 4}Z", fill="#ef5b56")
        + ko("path", d=f"M{cx - 46} {y - 8}H{cx + 50}L{cx + 36} {y + 10}H{cx - 34}Z", fill="#4a9be8")
        + ko("path", d=f"M{cx} {y - 78}L{cx + 16} {y - 72}L{cx} {y - 66}Z", fill="#ffd23f", stroke_width=2)
    )


def big_wave(x0=40):
    return (
        ko("path", d=f"M{x0} 300C{x0 + 20} 260 {x0 + 60} 226 {x0 + 110} 230C{x0 + 150} 234 {x0 + 162} 262 {x0 + 146} 280"
           f"C{x0 + 134} 262 {x0 + 112} 262 {x0 + 104} 276C{x0 + 124} 280 {x0 + 150} 296 {x0 + 180} 300Z", fill="#3a9fd8")
        + f'<path d="M{x0 + 60} 244C{x0 + 90} 228 {x0 + 136} 232 {x0 + 146} 262" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
        + "".join(f'<circle cx="{x0 + x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>' for x, y, r in ((150, 250, 5), (162, 238, 3.5), (140, 234, 3)))
    )


def sandcastle(cx=200, base=384):
    tower = lambda x, w, top: (
        ko("rect", x=x, y=top, width=w, height=base - top, fill="#e8c07a")
        + "".join(ko("rect", x=x + i * (w / 3), y=top - 8, width=w / 3 - 2, height=10, fill="#e8c07a", stroke_width=2.5) for i in (0, 2))
    )
    return (
        tower(cx - 62, 30, 314) + tower(cx + 32, 30, 314)
        + ko("rect", x=cx - 44, y=334, width=88, height=base - 334, fill="#f0cf8c")
        + tower(cx - 18, 36, 290)
        + dstroke(f"M{cx} 282V250", "#a8704a", 2.5)
        + ko("path", d=f"M{cx + 2} 250L{cx + 22} 257L{cx + 2} 264Z", fill="#ef5b56", stroke_width=2)
        + ko("path", d=f"M{cx - 10} {base}V{base - 26}Q{cx} {base - 38} {cx + 10} {base - 26}V{base}Z", fill="#a8704a", stroke_width=2.5)
        + "".join(ko("path", d=f"M{x - 5} {y}V{y - 8}Q{x} {y - 14} {x + 5} {y - 8}V{y}Z", fill="#a8704a", stroke_width=2) for x, y in ((cx - 47, 344), (cx + 47, 344), (cx, 314)))
    )


def bucket(cx=316, base=412):
    return (
        dstroke(f"M{cx + 30} {base - 6}L{cx + 52} {base - 64}", "#a8704a", 3)
        + ko("path", d=f"M{cx + 46} {base - 60}L{cx + 64} {base - 82}L{cx + 70} {base - 60}L{cx + 56} {base - 52}Z", fill="#ffd23f", stroke_width=2.5)
        + f'<path d="M{cx - 24} {base - 42}Q{cx} {base - 76} {cx + 24} {base - 42}" fill="none" stroke="{INK}" stroke-width="3"/>'
        + ko("path", d=f"M{cx - 26} {base - 42}H{cx + 26}L{cx + 20} {base}H{cx - 20}Z", fill="#ef5b56")
        + f'<path d="M{cx - 25} {base - 34}H{cx + 25}" stroke="#c9403b" stroke-width="4"/>'
    )


def crab(cx=462, cy=398):
    legs = "".join(
        f'<path d="M{cx + d * 18} {cy + 2 + i * 6}l{d * 14} {4 + i * 3}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        for d in (-1, 1) for i in range(3)
    )
    claw = lambda d: (
        dstroke(f"M{cx + d * 20} {cy - 6}L{cx + d * 32} {cy - 22}", "#ef4f5a", 4)
        + ko("path", d=f"M{cx + d * 30} {cy - 20}C{cx + d * 26} {cy - 40} {cx + d * 44} {cy - 44} {cx + d * 44} {cy - 30}L{cx + d * 36} {cy - 30}Z", fill="#ef4f5a", stroke_width=2.5)
    )
    eye = lambda d: dstroke(f"M{cx + d * 8} {cy - 12}V{cy - 24}", "#ef4f5a", 3) + f'<circle cx="{cx + d * 8}" cy="{cy - 26}" r="5" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="{cx + d * 8}" cy="{cy - 26}" r="2.2" fill="{INK}"/>'
    return (
        legs + claw(-1) + claw(1) + eye(-1) + eye(1)
        + ko("ellipse", cx=cx, cy=cy, rx=26, ry=16, fill="#ef4f5a")
        + f'<path d="M{cx - 6} {cy + 4}Q{cx} {cy + 9} {cx + 6} {cy + 4}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
        + f'<ellipse cx="{cx - 16}" cy="{cy + 2}" rx="4" ry="2.5" fill="#ff9aa8"/><ellipse cx="{cx + 16}" cy="{cy + 2}" rx="4" ry="2.5" fill="#ff9aa8"/>'
    )


def shell(cx=584, base=424):
    ridges = "".join(f'<path d="M{cx} {base}L{cx + 26 * math.cos(math.radians(a)):.1f} {base - 26 * math.sin(math.radians(a)):.1f}" stroke="#e46a95" stroke-width="2"/>' for a in (35, 62, 90, 118, 145))
    return (
        ko("path", d=f"M{cx - 8} {base + 2}H{cx + 8}L{cx + 6} {base + 8}H{cx - 6}Z", fill="#f78fb3", stroke_width=2)
        + ko("path", d=f"M{cx} {base}L{cx - 30} {base - 14}C{cx - 30} {base - 34} {cx - 16} {base - 42} {cx} {base - 42}C{cx + 16} {base - 42} {cx + 30} {base - 34} {cx + 30} {base - 14}Z", fill="#ffb3cc")
        + ridges
    )


def beach():
    foam = "M20 296" + "".join(f"q{12} -10 {24} 0" for _ in range(27))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#dcbf85"/>' for x, y in ((80, 340), (120, 420), (260, 430), (400, 350), (520, 440), (640, 380), (380, 420), (60, 400)))
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#cdeeff"/>',
        sun(604, 70),
        cloud(150, 60, 0.8),
        cloud(430, 50, 0.6),
        seagull(290, 96),
        seagull(356, 124, 0.6),
        '<rect x="20" y="168" width="640" height="140" fill="#58b7e8"/>',
        '<path d="M20 168H660" stroke="#3a9fd8" stroke-width="3"/>',
        "".join(f'<path d="M{x} {y}q10 -6 20 0" fill="none" stroke="#bfe6fb" stroke-width="3" stroke-linecap="round"/>' for x, y in ((250, 210), (330, 244), (560, 226), (620, 270), (420, 276))),
        sailboat(),
        big_wave(),
        '<path d="M20 300C200 290 460 292 660 296V452H20Z" fill="#f5dfb3"/>',
        f'<path d="{foam}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>',
        dots,
        sandcastle(),
        bucket(),
        crab(),
        shell(),
    ]
    labels = [
        ("seagull", 212, 84, (262, 96)),
        ("boat", 570, 140, (520, 150)),
        ("sea", 390, 214, None),
        ("wave", 122, 204, (130, 240)),
        ("sand", 610, 340, None),
        ("sandcastle", 330, 320, (240, 330)),
        ("bucket", 400, 386, (340, 392)),
        ("crab", 462, 330, (462, 352)),
        ("shell", 584, 440, (584, 424)),
    ]
    return parts, labels


# ================================================================ classroom
def board(x0=164, y0=44, x1=476, y1=190):
    return (
        ko("rect", x=x0 - 10, y=y0 - 10, width=x1 - x0 + 20, height=y1 - y0 + 20, rx=6, fill=WOOD)
        + ko("rect", x=x0, y=y0, width=x1 - x0, height=y1 - y0, rx=2, fill="#3f7d5c")
        + f'<text class="k-f" x="{x0 + 30}" y="{y0 + 62}" font-size="44" fill="#fff" opacity=".9">ABC</text>'
        + f'<text class="k-f" x="{x0 + 40}" y="{y0 + 118}" font-size="34" fill="#ffe08a" opacity=".9">1 2 3</text>'
        + f'<circle cx="{x1 - 70}" cy="{y0 + 56}" r="22" fill="none" stroke="#fff" stroke-width="3" opacity=".85"/>'
        + f'<path d="M{x1 - 110} {y0 + 118}L{x1 - 70} {y0 + 88}L{x1 - 30} {y0 + 118}Z" fill="none" stroke="#f78fb3" stroke-width="3" stroke-linejoin="round" opacity=".9"/>'
        + ko("rect", x=x0 - 4, y=y1 + 6, width=x1 - x0 + 8, height=8, rx=3, fill=WOOD_DARK, stroke_width=2)
        + f'<rect x="{x0 + 40}" y="{y1 + 1}" width="18" height="6" rx="2" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
    )


def wall_clock(cx=566, cy=96, r=34):
    ticks = "".join(
        f'<circle cx="{cx + (r - 8) * math.cos(math.radians(a)):.1f}" cy="{cy + (r - 8) * math.sin(math.radians(a)):.1f}" r="2.2" fill="{INK}"/>'
        for a in range(0, 360, 30)
    )
    return (
        ko("circle", cx=cx, cy=cy, r=r + 6, fill="#ef5b56")
        + ko("circle", cx=cx, cy=cy, r=r, fill="#fff", stroke_width=2)
        + ticks
        + f'<path d="M{cx} {cy}V{cy - 22}M{cx} {cy}L{cx - 14} {cy}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        + f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{INK}"/>'
    )


def cabinet_with_globe(x0=566, top=300):
    land = (
        f'<path d="M{x0 + 34} {top - 70}C{x0 + 44} {top - 80} {x0 + 58} {top - 76} {x0 + 54} {top - 64}C{x0 + 50} {top - 54} {x0 + 40} {top - 58} {x0 + 34} {top - 70}Z" fill="#5cc36a"/>'
        f'<path d="M{x0 + 60} {top - 50}C{x0 + 72} {top - 56} {x0 + 76} {top - 42} {x0 + 68} {top - 36}C{x0 + 62} {top - 34} {x0 + 58} {top - 42} {x0 + 60} {top - 50}Z" fill="#5cc36a"/>'
    )
    gx, gy = x0 + 52, top - 60
    return (
        ko("rect", x=x0, y=top, width=110, height=104, fill=WOOD)
        + ko("rect", x=x0 + 10, y=top + 14, width=90, height=34, rx=4, fill="#f2c58e", stroke_width=2.5)
        + ko("rect", x=x0 + 10, y=top + 58, width=90, height=34, rx=4, fill="#f2c58e", stroke_width=2.5)
        + ko("path", d=f"M{gx - 22} {top}H{gx + 22}L{gx + 14} {top - 10}H{gx - 14}Z", fill=WOOD_DARK, stroke_width=2.5)
        + dstroke(f"M{gx} {top - 10}V{top - 22}", WOOD_DARK, 4)
        + ko("circle", cx=gx, cy=gy, r=32, fill="#4a9be8")
        + land
        + f'<circle cx="{gx}" cy="{gy}" r="32" fill="none" stroke="{INK}" stroke-width="3"/>'
        + f'<path d="M{gx - 38} {gy + 14}A40 40 0 0 0 {gx + 18} {gy + 36}" fill="none" stroke="{WOOD_DARK}" stroke-width="5" stroke-linecap="round"/>'
    )


def desk(x0=110, x1=372, top=302):
    return (
        ko("rect", x=x0 + 12, y=top + 14, width=12, height=92, rx=3, fill=WOOD_DARK)
        + ko("rect", x=x1 - 24, y=top + 14, width=12, height=92, rx=3, fill=WOOD_DARK)
        + ko("rect", x=x0 + 24, y=top + 16, width=100, height=30, rx=3, fill="#f2c58e", stroke_width=2.5)
        + f'<circle cx="{x0 + 74}" cy="{top + 31}" r="3.5" fill="{INK}"/>'
        + ko("rect", x=x0, y=top, width=x1 - x0, height=16, rx=4, fill=WOOD)
    )


def open_book(cx=162, base=302):
    return (
        ko("path", d=f"M{cx - 34} {base}L{cx - 32} {base - 22}L{cx} {base - 18}L{cx + 32} {base - 22}L{cx + 34} {base}Z", fill="#4a9be8")
        + ko("path", d=f"M{cx - 30} {base - 4}L{cx - 28} {base - 24}Q{cx - 12} {base - 28} {cx} {base - 20}V{base - 2}Q{cx - 14} {base - 8} {cx - 30} {base - 4}Z", fill="#fff", stroke_width=2)
        + ko("path", d=f"M{cx + 30} {base - 4}L{cx + 28} {base - 24}Q{cx + 12} {base - 28} {cx} {base - 20}V{base - 2}Q{cx + 14} {base - 8} {cx + 30} {base - 4}Z", fill="#fff", stroke_width=2)
        + f'<path d="M{cx - 22} {base - 18}l14 1M{cx - 22} {base - 12}l14 1M{cx + 8} {base - 17}l14 -1M{cx + 8} {base - 11}l14 -1" stroke="#c9c2cc" stroke-width="2" stroke-linecap="round"/>'
    )


def pencil(cx=236, base=302):
    return (
        f'<g transform="translate({cx} {base - 7}) rotate(-6)">'
        + ko("path", d="M-34 -6H26V6H-34Z", fill="#ffc93c")
        + ko("path", d="M26 -6L40 0L26 6Z", fill="#f2c58e", stroke_width=2.5)
        + f'<path d="M36 -2L40 0L36 2Z" fill="{INK}"/>'
        + ko("rect", x=-44, y=-6, width=10, height=12, rx=3, fill="#f78fb3", stroke_width=2.5)
        + '<path d="M-30 0H22" stroke="#e8a900" stroke-width="2"/></g>'
    )


def ruler(x0=290, base=302):
    ticks = "".join(f'<path d="M{x0 + 6 + i * 6} {base - 12}v{4 if i % 2 else 7}" stroke="{INK}" stroke-width="1.5"/>' for i in range(10))
    return ko("rect", x=x0, y=base - 12, width=70, height=12, rx=2, fill="#8ed1f5", stroke_width=2.5) + ticks


def school_chair(x0=402, seat=344):
    c = "#4a9be8"
    return (
        ko("rect", x=x0 + 4, y=seat - 86, width=9, height=148, rx=3, fill="#9aa3b2")
        + ko("rect", x=x0 + 56, y=seat, width=9, height=62, rx=3, fill="#9aa3b2")
        + ko("rect", x=x0, y=seat - 90, width=64, height=40, rx=10, fill=c)
        + ko("rect", x=x0 + 26, y=seat + 12, width=9, height=50, rx=3, fill="#9aa3b2")
        + ko("rect", x=x0 - 4, y=seat - 8, width=74, height=16, rx=6, fill=c)
    )


def backpack(cx=520, base=414):
    return (
        dstroke(f"M{cx - 16} {base - 70}Q{cx} {base - 90} {cx + 16} {base - 70}", "#c9403b", 5)
        + ko("rect", x=cx - 30, y=base - 72, width=60, height=72, rx=16, fill="#ef5b56")
        + ko("path", d=f"M{cx - 30} {base - 50}Q{cx - 30} {base - 72} {cx - 14} {base - 72}H{cx + 14}Q{cx + 30} {base - 72} {cx + 30} {base - 50}V{base - 40}H{cx - 30}Z", fill="#f07b76", stroke_width=2.5)
        + ko("rect", x=cx - 18, y=base - 28, width=36, height=20, rx=6, fill="#f07b76", stroke_width=2.5)
        + f'<circle cx="{cx}" cy="{base - 42}" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
    )


def classroom():
    planks = "".join(f'<path d="M20 {y}H660" stroke="#c99a62" stroke-width="2"/>' for y in (366, 392, 422))
    alphabet = "".join(
        ko("rect", x=40 + i * 22, y=30, width=18, height=22, rx=3, fill=c, stroke_width=2)
        + f'<text class="k-f" x="{49 + i * 22}" y="47" font-size="14" fill="#fff" text-anchor="middle">{ch}</text>'
        for i, (ch, c) in enumerate(zip("ABCDE", ["#ef5b56", "#ff9a3c", "#e6a700", "#5cc36a", "#4a9be8"]))
    )
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#e6f4e4"/>',
        '<rect x="20" y="340" width="640" height="112" fill="#e0b884"/>',
        planks,
        f'<path d="M20 340H660" stroke="{INK}" stroke-width="3"/>',
        alphabet,
        star(78, 100, 14, "#ffd23f", 2.5) + star(112, 130, 10, "#f78fb3", 2) + star(66, 150, 9, "#8ed1f5", 2),
        board(),
        wall_clock(),
        cabinet_with_globe(),
        desk(),
        open_book(),
        pencil(),
        ruler(),
        school_chair(),
        backpack(),
    ]
    labels = [
        ("board", 320, 226, (320, 196)),
        ("clock", 610, 152, (586, 118)),
        ("globe", 540, 214, (600, 236)),
        ("desk", 248, 380, (248, 318)),
        ("book", 110, 250, (150, 286)),
        ("pencil", 214, 256, (228, 294)),
        ("ruler", 330, 262, (324, 290)),
        ("chair", 434, 226, (434, 258)),
        ("bag", 520, 436, (520, 404)),
    ]
    return parts, labels



# ================================================================ farm
def barn(x0=396, x1=584, base=292):
    cx, w = (x0 + x1) / 2, x1 - x0
    wall = base - 110
    return (
        ko("path", d=f"M{x0 - 10} {wall + 4}L{cx} {wall - 64}L{x1 + 10} {wall + 4}Z", fill="#8a3a3a")
        + ko("rect", x=x0, y=wall, width=w, height=base - wall, fill="#d9534f")
        + "".join(f'<path d="M{x} {wall + 6}V{base}" stroke="#b8403c" stroke-width="2"/>' for x in range(int(x0) + 16, int(x1), 16))
        + ko("path", d=f"M{cx - 16} {wall - 34}H{cx + 16}V{wall - 6}H{cx - 16}Z", fill="#fff")
        + ko("rect", x=cx - 34, y=base - 70, width=68, height=70, fill="#fff")
        + f'<path d="M{cx - 34} {base - 70}L{cx + 34} {base}M{cx + 34} {base - 70}L{cx - 34} {base}M{cx} {base - 70}V{base}" stroke="{INK}" stroke-width="3"/>'
        + ko("rect", x=cx - 30, y=base - 66, width=60, height=62, fill="none", stroke_width=2)
    )


def hay(cx=622, base=298, r=30):
    return (
        ko("ellipse", cx=cx, cy=base - r, rx=r + 6, ry=r, fill="#f2c96b")
        + f'<path d="M{cx - 14} {base - r - 8}q14 -10 26 2q6 14 -8 20q-14 4 -18 -8q0 -8 8 -8" fill="none" stroke="#c9953a" stroke-width="3" stroke-linecap="round"/>'
        + "".join(f'<path d="M{cx + dx} {base - 4}l{sx} -8" stroke="#c9953a" stroke-width="2" stroke-linecap="round"/>' for dx, sx in ((-24, -3), (-8, 2), (10, -2), (26, 3)))
    )


def fence(x0=20, x1=380, y=300):
    posts = "".join(ko("path", d=f"M{x - 6} {y + 44}V{y - 6}L{x} {y - 14}L{x + 6} {y - 6}V{y + 44}Z", fill="#fff", stroke_width=2.5) for x in range(x0 + 20, x1, 44))
    rails = "".join(ko("rect", x=x0, y=y + dy, width=x1 - x0, height=8, rx=2, fill="#fff", stroke_width=2.5) for dy in (4, 24))
    return rails + posts


def horse(cx=300, base=300):
    legs = "".join(ko("rect", x=cx + dx, y=base - 34, width=9, height=40, rx=3, fill="#a8704a", stroke_width=2.5) for dx in (-40, -26, 18, 32))
    return (
        legs
        + ko("ellipse", cx=cx, cy=base - 44, rx=50, ry=24, fill="#b5774a")
        + dstroke(f"M{cx + 48} {base - 50}Q{cx + 66} {base - 44} {cx + 62} {base - 18}", "#5a3a26", 6)
        + ko("path", d=f"M{cx - 30} {base - 56}L{cx - 44} {base - 100}L{cx - 22} {base - 104}L{cx - 10} {base - 60}Z", fill="#b5774a")
        + ko("path", d=f"M{cx - 44} {base - 100}C{cx - 70} {base - 102} {cx - 80} {base - 90} {cx - 76} {base - 80}C{cx - 70} {base - 74} {cx - 56} {base - 80} {cx - 44} {base - 84}Z", fill="#b5774a")
        + ko("path", d=f"M{cx - 30} {base - 112}L{cx - 26} {base - 124}L{cx - 20} {base - 110}Z", fill="#b5774a", stroke_width=2.5)
        + f'<path d="M{cx - 20} {base - 110}Q{cx - 8} {base - 90} {cx - 8} {base - 64}" fill="none" stroke="#5a3a26" stroke-width="7" stroke-linecap="round"/>'
        + f'<circle cx="{cx - 50}" cy="{base - 94}" r="3" fill="{INK}"/><circle cx="{cx - 70}" cy="{base - 84}" r="2" fill="{INK}"/>'
    )


def cow(cx=150, base=392):
    legs = "".join(ko("rect", x=cx + dx, y=base - 30, width=10, height=30, rx=3, fill="#fff", stroke_width=2.5) for dx in (-44, -28, 18, 34))
    spots = "".join(f'<path d="{d}" fill="{INK}"/>' for d in (
        f"M{cx - 20} {base - 62}c10 -4 20 2 16 12c-4 8 -18 6 -20 -2z", f"M{cx + 18} {base - 50}c8 -6 20 0 16 10c-6 6 -18 4 -16 -10z"))
    return (
        legs
        + dstroke(f"M{cx + 50} {base - 58}Q{cx + 64} {base - 44} {cx + 58} {base - 30}", "#fff", 3)
        + ko("rect", x=cx - 52, y=base - 76, width=104, height=50, rx=24, fill="#fff")
        + spots
        + ko("ellipse", cx=cx - 12, cy=base - 24, rx=10, ry=6, fill="#ffb3c6", stroke_width=2)
        + ko("path", d=f"M{cx - 78} {base - 94}l-14 -6l10 12z", fill="#fff", stroke_width=2)
        + ko("path", d=f"M{cx - 48} {base - 94}l14 -6l-10 12z", fill="#fff", stroke_width=2)
        + ko("ellipse", cx=cx - 63, cy=base - 76, rx=20, ry=22, fill="#fff")
        + ko("ellipse", cx=cx - 63, cy=base - 62, rx=16, ry=10, fill="#ffb3c6", stroke_width=2.5)
        + f'<circle cx="{cx - 69}" cy="{base - 62}" r="2" fill="{INK}"/><circle cx="{cx - 57}" cy="{base - 62}" r="2" fill="{INK}"/>'
        + f'<circle cx="{cx - 71}" cy="{base - 82}" r="3" fill="{INK}"/><circle cx="{cx - 55}" cy="{base - 82}" r="3" fill="{INK}"/>'
        + ko("path", d=f"M{cx - 74} {base - 96}q-6 -12 0 -12M{cx - 52} {base - 96}q6 -12 0 -12", fill="none", stroke_width=3)
    )


def sheep(cx=330, base=410):
    puffs = "".join(ko("circle", cx=cx + dx, cy=base - 34 + dy, r=15, fill="#fff") for dx, dy in ((-22, 0), (-8, -10), (8, -10), (22, 0), (10, 8), (-10, 8)))
    return (
        "".join(ko("rect", x=cx + dx, y=base - 20, width=8, height=20, rx=3, fill="#3f3345", stroke_width=2) for dx in (-22, -8, 6, 18))
        + puffs
        + ko("ellipse", cx=cx - 38, cy=base - 40, rx=13, ry=16, fill="#5a4a5e")
        + ko("ellipse", cx=cx - 52, cy=base - 44, rx=8, ry=4, fill="#5a4a5e", stroke_width=2)
        + ko("circle", cx=cx - 36, cy=base - 56, r=9, fill="#fff", stroke_width=2.5)
        + f'<circle cx="{cx - 42}" cy="{base - 42}" r="2.2" fill="#fff"/><circle cx="{cx - 33}" cy="{base - 42}" r="2.2" fill="#fff"/>'
    )


def farm_pig(cx=452, base=414):
    return (
        "".join(ko("rect", x=cx + dx, y=base - 22, width=9, height=22, rx=3, fill="#f5a3b5", stroke_width=2.5) for dx in (-28, -14, 8, 20))
        + dstroke(f"M{cx + 36} {base - 40}c8 -2 10 -10 4 -12c-6 -2 -6 6 0 6", "#f5a3b5", 2.5)
        + ko("ellipse", cx=cx, cy=base - 36, rx=38, ry=24, fill="#ffc2cf")
        + ko("path", d=f"M{cx - 36} {base - 60}l-6 -14l14 8z", fill="#f5a3b5", stroke_width=2.5)
        + ko("circle", cx=cx - 34, cy=base - 42, r=20, fill="#ffc2cf")
        + ko("ellipse", cx=cx - 48, cy=base - 38, rx=9, ry=7, fill="#f5a3b5", stroke_width=2.5)
        + f'<circle cx="{cx - 51}" cy="{base - 38}" r="1.8" fill="{INK}"/><circle cx="{cx - 45}" cy="{base - 38}" r="1.8" fill="{INK}"/>'
        + f'<circle cx="{cx - 36}" cy="{base - 50}" r="2.8" fill="{INK}"/>'
    )


def tractor(cx=566, base=424):
    wheel = lambda x, r: ko("circle", cx=x, cy=base - r, r=r, fill=INK) + f'<circle cx="{x}" cy="{base - r}" r="{r * 0.45:.1f}" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
    return (
        ko("rect", x=cx - 4, y=base - 96, width=56, height=54, rx=6, fill="#5cc36a")
        + ko("rect", x=cx + 6, y=base - 88, width=36, height=26, rx=3, fill="#cdeeff", stroke_width=2.5)
        + ko("path", d=f"M{cx - 66} {base - 60}H{cx + 4}V{base - 26}H{cx - 66}Z", fill="#5cc36a")
        + dstroke(f"M{cx - 52} {base - 60}V{base - 82}", "#9aa3b2", 5)
        + wheel(cx + 32, 38) + wheel(cx - 48, 22)
    )


def farm():
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#cdeeff"/>',
        sun(96, 70),
        cloud(250, 60, 0.8),
        cloud(560, 50, 0.6),
        '<path d="M20 230C140 180 260 196 360 214C460 232 560 196 660 206V452H20Z" fill="#a5dc8e"/>',
        '<path d="M20 272C200 256 460 262 660 268V452H20Z" fill="#8fd16f"/>',
        barn(),
        hay(),
        horse(),
        fence(),
        '<path d="M470 452C480 380 500 320 490 292H530C540 330 560 390 580 452Z" fill="#e8cf9a"/>',
        cow(),
        f'<g transform="translate(236 402) scale(.42)">' + __import__("build13").hen() + '</g>',
        sheep(),
        farm_pig(),
        tractor(),
    ]
    labels = [
        ("barn", 490, 92, (490, 118)),
        ("hay", 622, 224, (622, 246)),
        ("horse", 214, 176, (252, 196)),
        ("fence", 80, 272, (80, 300)),
        ("cow", 112, 424, (120, 380)),
        ("hen", 236, 342, (236, 372)),
        ("sheep", 330, 330, (330, 358)),
        ("pig", 440, 350, (440, 376)),
        ("tractor", 540, 300, (556, 330)),
    ]
    return parts, labels


# ================================================================ park
def slide(x0=56, base=330):
    return (
        ko("rect", x=x0, y=base - 120, width=8, height=120, fill="#9aa3b2", stroke_width=2.5)
        + ko("rect", x=x0 + 30, y=base - 120, width=8, height=120, fill="#9aa3b2", stroke_width=2.5)
        + "".join(f'<path d="M{x0 + 8} {base - 100 + i * 22}H{x0 + 30}" stroke="{INK}" stroke-width="4"/>' for i in range(5))
        + ko("rect", x=x0 - 4, y=base - 128, width=50, height=12, rx=3, fill="#ffd23f")
        + ko("path", d=f"M{x0 + 40} {base - 124}C{x0 + 90} {base - 110} {x0 + 110} {base - 20} {x0 + 150} {base - 12}L{x0 + 150} {base}C{x0 + 104} {base - 8} {x0 + 84} {base - 100} {x0 + 40} {base - 108}Z", fill="#ef5b56")
    )


def swing_set(x0=236, x1=356, top=196, base=330):
    seat = lambda x, y: (
        f'<path d="M{x - 12} {top + 6}V{y}M{x + 12} {top + 6}V{y}" stroke="{INK}" stroke-width="2.5"/>'
        + ko("rect", x=x - 18, y=y, width=36, height=8, rx=3, fill="#4a9be8", stroke_width=2.5)
    )
    return (
        seat(x0 + 32, base - 44) + seat(x1 - 32, base - 38)
        + dstroke(f"M{x0 - 14} {base}L{x0} {top}L{x0 + 14} {base}", "#ff9a3c", 5)
        + dstroke(f"M{x1 - 14} {base}L{x1} {top}L{x1 + 14} {base}", "#ff9a3c", 5)
        + dstroke(f"M{x0 - 4} {top}H{x1 + 4}", "#ff9a3c", 6)
    )


def seesaw(cx=420, base=404):
    return (
        dstroke(f"M{cx - 70} {base - 36}L{cx + 70} {base - 12}", "#5cc36a", 8)
        + "".join(dstroke(f"M{x} {y}v-14h8", "#3f3345", 2.5) for x, y in ((cx - 60, base - 38), (cx + 56, base - 16)))
        + ko("path", d=f"M{cx - 16} {base}L{cx} {base - 26}L{cx + 16} {base}Z", fill="#ffd23f")
    )


def duck(cx=150, cy=392):
    return (
        ko("path", d=f"M{cx - 22} {cy}C{cx - 24} {cy - 16} {cx + 12} {cy - 18} {cx + 22} {cy - 8}L{cx + 30} {cy - 14}C{cx + 30} {cy - 2} {cx + 22} {cy + 6} {cx} {cy + 6}C{cx - 14} {cy + 6} {cx - 22} {cy + 4} {cx - 22} {cy}Z", fill="#ffd23f")
        + ko("circle", cx=cx - 16, cy=cy - 20, r=11, fill="#ffd23f")
        + ko("path", d=f"M{cx - 26} {cy - 20}L{cx - 38} {cy - 16}L{cx - 26} {cy - 13}Z", fill="#ff9a3c", stroke_width=2)
        + f'<circle cx="{cx - 18}" cy="{cy - 23}" r="2.2" fill="{INK}"/>'
        + f'<path d="M{cx - 2} {cy - 6}q8 4 16 -2" fill="none" stroke="#e8b520" stroke-width="2.5" stroke-linecap="round"/>'
    )


def bench(x0=516, base=424):
    return (
        ko("rect", x=x0 + 8, y=base - 34, width=8, height=34, fill="#5a6070", stroke_width=2)
        + ko("rect", x=x0 + 104, y=base - 34, width=8, height=34, fill="#5a6070", stroke_width=2)
        + ko("rect", x=x0, y=base - 76, width=120, height=12, rx=3, fill=WOOD)
        + ko("rect", x=x0, y=base - 58, width=120, height=12, rx=3, fill=WOOD)
        + ko("rect", x=x0 - 4, y=base - 40, width=128, height=12, rx=3, fill=WOOD)
    )


def balloon(cx, cy, color, to):
    return (
        f'<path d="M{cx} {cy + 22}Q{cx - 6} {(cy + to[1]) / 2} {to[0]} {to[1]}" fill="none" stroke="{INK}" stroke-width="1.5"/>'
        + ko("ellipse", cx=cx, cy=cy, rx=16, ry=20, fill=color)
        + ko("path", d=f"M{cx - 4} {cy + 24}L{cx} {cy + 19}L{cx + 4} {cy + 24}Z", fill=color, stroke_width=2)
        + f'<path d="M{cx - 8} {cy - 8}q2 -6 8 -8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>'
    )


def park():
    import build5, build9
    from build4 import tree
    from build12 import kid, BOY
    kite_art = f'<g transform="translate(520 88) scale(.42) rotate(-10)">{build5.kite()}</g>'
    flyer = kid(
        BOY, head=(470, 262), neck=(470, 282), hip=(470, 312), tilt=-8,
        arms=([(466, 286), (452, 298), (446, 312)], [(474, 286), (488, 270), (500, 252)]),
        legs=([(466, 312), (460, 332), (456, 350)], [(474, 312), (480, 332), (484, 350)]),
    )
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#cdeeff"/>',
        cloud(170, 60, 0.9),
        cloud(380, 44, 0.6),
        '<path d="M20 214C160 196 420 206 660 200V452H20Z" fill="#8fd16f"/>',
        tree(612, 250),
        '<path d="M300 452C330 400 420 370 520 364C590 360 640 350 660 344V380C600 392 520 396 460 410C400 424 380 440 376 452Z" fill="#f2dfb8"/>',
        slide(),
        swing_set(),
        '<ellipse cx="160" cy="400" rx="116" ry="36" fill="#6cc3ee" stroke="#3f3345" stroke-width="3"/>',
        '<path d="M100 394q14 -6 28 0M190 410q14 -6 28 0" stroke="#bfe6fb" stroke-width="3" fill="none" stroke-linecap="round"/>',
        duck(),
        seesaw(),
        f'<path d="M500 250L520 104" stroke="{INK}" stroke-width="1.5"/>',
        kite_art,
        flyer,
        f'<g transform="translate(396 300) scale(.58)">{build9.bike()}</g>',
        bench(),
        balloon(600, 318, "#ef5b56", (596, 358)),
        balloon(628, 330, "#ffd23f", (600, 358)),
    ]
    labels = [
        ("slide", 150, 176, (116, 212)),
        ("swing", 296, 170, (296, 196)),
        ("seesaw", 420, 436, (420, 400)),
        ("pond", 60, 360, (84, 392)),
        ("duck", 210, 350, (160, 376)),
        ("kite", 590, 76, (548, 88)),
        ("bike", 330, 262, (376, 292)),
        ("bench", 560, 440, (560, 404)),
        ("balloon", 600, 262, (604, 298)),
    ]
    return parts, labels


# ================================================================ supermarket
def shelf_unit(x0=36, x1=316, top=58, base=332):
    boards = "".join(ko("rect", x=x0, y=y, width=x1 - x0, height=8, fill="#b8c6d6", stroke_width=2.5) for y in (140, 224, base - 8))
    milk = "".join(
        ko("path", d=f"M{x} 138V104L{x + 8} 94H{x + 22}L{x + 30} 104V138Z", fill="#fff")
        + f'<path d="M{x} 104H{x + 30}" stroke="{INK}" stroke-width="2"/>'
        + f'<path d="M{x + 6} 116h18v12h-18z" fill="#4a9be8"/>'
        for x in (52, 88, 124)
    )
    juice = "".join(
        ko("path", d=f"M{x} 138V108Q{x} 100 {x + 6} 98V88H{x + 14}V98Q{x + 20} 100 {x + 20} 108V138Z", fill="#ff9a3c")
        + f'<rect x="{x + 3}" y="{112}" width="14" height="12" fill="#ffd23f"/>'
        for x in (182, 212, 242, 272)
    )
    bread = "".join(
        ko("path", d=f"M{x} 222V204C{x} 188 {x + 44} 188 {x + 44} 204V222Z", fill="#e0a24a")
        + "".join(f'<path d="M{x + dx} 200l6 -6" stroke="#b87a2a" stroke-width="2.5" stroke-linecap="round"/>' for dx in (10, 20, 30))
        for x in (52, 108, 164, 220)
    )
    cheese = "".join(
        ko("path", d=f"M{x} 316V292L{x + 48} 280L{x + 48} 316Z", fill="#ffd23f")
        + "".join(f'<circle cx="{x + cx}" cy="{cy}" r="{r}" fill="#e8b520"/>' for cx, cy, r in ((14, 300, 4), (30, 306, 3), (38, 294, 3)))
        for x in (52, 116, 180, 244)
    )
    return (
        ko("rect", x=x0 - 8, y=top, width=x1 - x0 + 16, height=base - top, rx=4, fill="#dfe6ef")
        + milk + juice + bread + cheese + boards
    )


def carrot_crate(cx=356, base=338):
    carrots = "".join(
        ko("path", d=f"M{cx + dx - 7} {base - 64}L{cx + dx} {base - 20}L{cx + dx + 7} {base - 64}Z", fill="#ff9a3c", stroke_width=2)
        + f'<path d="M{cx + dx} {base - 64}l-6 -12M{cx + dx} {base - 64}l0 -14M{cx + dx} {base - 64}l6 -12" stroke="#4fa64f" stroke-width="3" stroke-linecap="round"/>'
        for dx in (-28, -14, 0, 14, 28)
    )
    return carrots + ko("rect", x=cx - 44, y=base - 30, width=88, height=40, rx=3, fill=WOOD) + "".join(
        f'<path d="M{cx - 44} {y}H{cx + 44}" stroke="{WOOD_DARK}" stroke-width="2.5"/>' for y in (base - 18, base - 6))


def cart(cx=476, base=432):
    grid = "".join(f'<path d="M{x} {base - 92}L{x + 4} {base - 44}" stroke="#9aa3b2" stroke-width="2"/>' for x in range(cx - 44, cx + 40, 14))
    return (
        f'<path d="M{cx - 64} {base - 104}H{cx - 50}L{cx - 38} {base - 40}H{cx + 40}" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        + ko("path", d=f"M{cx - 50} {base - 96}H{cx + 54}L{cx + 42} {base - 44}H{cx - 38}Z", fill="#dfe6ef")
        + grid
        + ko("circle", cx=cx - 28, cy=base - 14, r=10, fill=INK) + ko("circle", cx=cx + 30, cy=base - 14, r=10, fill=INK)
        + f'<path d="M{cx - 34} {base - 40}L{cx - 28} {base - 24}M{cx + 34} {base - 40}L{cx + 30} {base - 24}" stroke="{INK}" stroke-width="3"/>'
        + ko("circle", cx=cx - 10, cy=base - 104, r=14, fill="#ef5b56")
        + ko("path", d=f"M{cx + 6} {base - 96}C{cx + 4} {base - 126} {cx + 34} {base - 128} {cx + 36} {base - 110}Z", fill="#ffd23f")
    )


def market_basket(cx=522, base=252):
    return (
        f'<path d="M{cx - 22} {base - 30}Q{cx} {base - 62} {cx + 22} {base - 30}" fill="none" stroke="{INK}" stroke-width="4"/>'
        + ko("path", d=f"M{cx - 30} {base - 32}H{cx + 30}L{cx + 24} {base}H{cx - 24}Z", fill="#ef5b56")
        + "".join(f'<path d="M{cx - 26 + i * 10} {base - 26}V{base - 6}" stroke="#c9403b" stroke-width="3"/>' for i in range(6))
    )


def checkout(x0=470, top=254):
    from build12 import kid, GIRL2
    cashier = kid(
        GIRL2, head=(606, 176), neck=(606, 196), hip=(606, 230),
        arms=([(602, 200), (588, 214), (578, 240)], [(610, 200), (628, 216), (640, 244)]),
        legs=([(602, 230), (600, 250), (600, 262)], [(610, 230), (612, 250), (612, 262)]),
    )
    return (
        cashier
        + ko("rect", x=x0, y=top, width=200, height=86, fill="#4a9be8")
        + ko("rect", x=x0 - 6, y=top - 8, width=206, height=14, rx=4, fill="#dfe6ef")
        + f'<path d="M{x0 + 6} {top - 1}H{x0 + 110}" stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>'
        + ko("rect", x=x0 + 116, y=top - 40, width=40, height=34, rx=4, fill="#3f4450")
        + ko("rect", x=x0 + 122, y=top - 34, width=28, height=12, rx=2, fill="#8ed1f5", stroke_width=2)
        + ko("rect", x=x0 + 20, y=top + 20, width=70, height=46, rx=6, fill="#6fb2f0", stroke_width=2.5)
    )


def market():
    floor = "".join(
        f'<rect x="{x}" y="{y}" width="40" height="30" fill="#e3e8f0"/>'
        for i, x in enumerate(range(20, 660, 40)) for j, y in enumerate(range(340, 452, 30)) if (i + j) % 2 == 0
    )
    parts = [
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#f4f1ff"/>',
        '<rect x="20" y="340" width="640" height="112" fill="#fff"/>',
        floor,
        f'<path d="M20 340H660" stroke="{INK}" stroke-width="3"/>',
        ko("rect", x=366, y=30, width=148, height=40, rx=10, fill="#ef5b56"),
        f'<text class="k-f" x="440" y="58" font-size="22" fill="#fff" text-anchor="middle">SHOP</text>',
        shelf_unit(),
        carrot_crate(),
        checkout(),
        market_basket(),
        cart(),
    ]
    labels = [
        ("shelf", 176, 40, (176, 58)),
        ("milk", 88, 76, (100, 100)),
        ("juice", 256, 70, (250, 94)),
        ("bread", 150, 170, (140, 196)),
        ("cheese", 212, 258, (206, 290)),
        ("carrots", 356, 222, (356, 262)),
        ("cart", 400, 420, (430, 404)),
        ("basket", 522, 180, (522, 208)),
        ("cashier", 606, 110, (606, 150)),
    ]
    return parts, labels


SCENES = {"kitchen": kitchen, "beach": beach, "classroom": classroom, "farm": farm, "park": park, "market": market}


def scene_svg(name, aria):
    """The whole scene as one SVG: the picture clipped to a rounded frame, then the word labels on top."""
    parts, labels = SCENES[name]()
    clip = f"k-scene-{name}"
    tags = "".join(
        f'<g class="tag" data-word="{w}" tabindex="0" role="button" aria-label="{w}">{pill(w, x, y, to)}</g>' for w, x, y, to in labels
    )
    return (
        f'<svg viewBox="0 0 680 464" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{aria}">'
        f'<defs><clipPath id="{clip}"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="24"/></clipPath></defs>'
        f'<g clip-path="url(#{clip})">{"".join(parts)}</g>'
        f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="24" fill="none" stroke="{INK}" stroke-width="3"/>{tags}</svg>'
    )
