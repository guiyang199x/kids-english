"""Halloween: the Ghost Ship that visits the world map in October, the Halloween words, and a night scene for its story.

ghost_ship() - the ship, centered on its waterline, about 150 wide. Things on it that move have classes of their own
               (bob, ghost-float, lantern); build16 puts it on the world map as <g class="visit-g">.
HALLOWEEN    - the lesson's new pictures (ghost, witch, candy, monster, mask, broom), each centered on (0, 0) within
               about x -80..80, y -66..66 like the other word pictures. Bat, pumpkin, spider and moon are already drawn.
night()      - the story's background: a night sea under the moon with the Ghost Ship, and sand in front.

Run `python3 build24.py` to preview everything in work/halloween_preview.html.
"""
from common import INK
from build1 import shadow
from build5 import eyes, cheeks, smile, mirror, dstroke

HULL, HULL_DARK, SAIL, GLOW = "#5b4a86", "#443566", "#efeaf8", "#ffd23f"
ORANGE, ORANGE_DARK = "#ff9a3c", "#e0761b"


# ---------------------------------------------------------------- the words
def ghost(s=1.0, cls=""):
    """A friendly little ghost: a white blob with a wavy hem, waving."""
    c = f' class="{cls}"' if cls else ""
    body = ("M0 -52C26 -52 38 -32 38 -6V38Q31 30 25 38T12 38T0 38T-12 38T-25 38Q-31 30 -38 38V-6C-38 -32 -26 -52 0 -52Z")
    return (
        f'<g{c} transform="scale({s})">'
        + f'<ellipse cx="0" cy="58" rx="30" ry="5" fill="{INK}" opacity=".12"/>'
        + f'<path class="k-o" d="M36 0C48 -6 52 -16 50 -24" fill="none" stroke-width="9"/><path d="M36 0C48 -6 52 -16 50 -24" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
        + f'<path class="k-o" d="{body}" fill="#fff"/>'
        + '<path d="M-26 -20Q-26 -38 -12 -44" fill="none" stroke="#e6e1f2" stroke-width="5" stroke-linecap="round"/>'
        + eyes(12, -16, 5.5)
        + f'<ellipse cx="0" cy="2" rx="6" ry="8" fill="{INK}"/><ellipse cx="0" cy="5" rx="3.5" ry="4" fill="#ff7d93"/>'
        + cheeks(22, -2, 6, 3.5)
        + "</g>"
    )


def witch():
    """A smiling little witch: a big purple hat with a buckle, a round face and a cape."""
    skin, hair, purple, purple_dark = "#ffd8b8", "#ef7b3a", "#8150c4", "#5f3a99"
    return (
        shadow(62, 44)
        + f'<path class="k-o" d="M-44 64Q-40 30 -20 22H20Q40 30 44 64Z" fill="{purple}"/>'
        + f'<path class="k-o" d="M-8 24L0 36L8 24Z" fill="{GLOW}" stroke-width="2"/>'
        + f'<path class="k-o" d="M-34 6Q-44 30 -30 44Q-26 24 -22 14ZM34 6Q44 30 30 44Q26 24 22 14Z" fill="{hair}"/>'
        + f'<circle class="k-o" cx="0" cy="6" r="26" fill="{skin}"/>'
        + eyes(10, 6, 4) + smile(16, 7, 5) + cheeks(17, 14, 5, 3)
        # the hat: brim, cone with a bent tip, band and buckle
        + f'<ellipse class="k-o" cx="0" cy="-16" rx="46" ry="10" fill="{purple_dark}"/>'
        + f'<path class="k-o" d="M-26 -18L-6 -60Q2 -72 14 -64L28 -56Q16 -58 12 -50L26 -18Z" fill="{purple}"/>'
        + f'<path d="M-24 -26H24" stroke="{ORANGE}" stroke-width="8"/>'
        + f'<rect class="k-o" x="-7" y="-32" width="14" height="12" rx="2" fill="none" stroke="{GLOW}" stroke-width="3"/>'
        + f'<path d="M-26 -22L26 -22" stroke="{INK}" stroke-width="0"/>'
    )


def candy():
    """A wrapped sweet with twisted ends, and a swirly lollipop behind it."""
    stripes = "".join(f'<path d="M{x} -14Q{x + 6} 0 {x} 14" fill="none" stroke="#fff" stroke-width="5"/>' for x in (-12, 0, 12))
    swirl = '<path d="M34 -30m-14 0a14 14 0 1 1 28 0a10 10 0 1 1 -20 0a6 6 0 1 1 12 0" fill="none" stroke="#fff" stroke-width="4"/>'
    return (
        shadow(46, 58)
        + dstroke("M34 -16V40", "#fff", 4)
        + f'<circle class="k-o" cx="34" cy="-30" r="22" fill="#6cc070"/>' + swirl
        + f'<path class="k-o" d="M-26 0L-52 -18L-48 0L-52 18Z" fill="{ORANGE}"/>'
        + f'<path class="k-o" d="M26 0L52 -18L48 0L52 18Z" fill="{ORANGE}"/>'
        + f'<ellipse class="k-o" cx="0" cy="0" rx="28" ry="20" fill="#8150c4"/>' + stripes
        + f'<ellipse cx="0" cy="0" rx="28" ry="20" fill="none" stroke="{INK}" stroke-width="3"/>'
        + '<path d="M-16 -10Q-8 -16 2 -15" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
    )


def monster():
    """A round green monster with one big eye, two little horns and a toothy grin."""
    green, green_dark = "#7ccf5a", "#5aa83b"
    return (
        shadow(60, 44)
        + mirror(f'<path class="k-o" d="M-22 -44L-30 -64L-12 -50Z" fill="{GLOW}"/>')
        + mirror(f'<path class="k-o" d="M-44 10Q-62 4 -64 -12" fill="none" stroke-width="10"/><path d="M-44 10Q-62 4 -64 -12" fill="none" stroke="{green}" stroke-width="5" stroke-linecap="round"/>')
        + mirror(f'<rect class="k-o" x="-26" y="40" width="16" height="18" rx="7" fill="{green_dark}"/>')
        + f'<path class="k-o" d="M0 -52C32 -52 46 -26 46 4C46 34 26 48 0 48C-26 48 -46 34 -46 4C-46 -26 -32 -52 0 -52Z" fill="{green}"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{green_dark}"/>' for x, y, r in ((-30, -8, 4), (32, 18, 5), (-22, 30, 3)))
        + f'<circle class="k-o" cx="0" cy="-16" r="18" fill="#fff"/><circle cx="2" cy="-14" r="9" fill="{INK}"/><circle cx="5" cy="-18" r="3" fill="#fff"/>'
        + f'<path class="k-o" d="M-20 12Q0 34 20 12Z" fill="#8a2d3b" stroke-width="2.5"/>'
        + mirror('<path d="M-12 14L-9 21L-6 15" fill="#fff" stroke="#3f3345" stroke-width="1.5" stroke-linejoin="round"/>')
        + cheeks(30, 6, 5, 3)
    )


def mask():
    """A party eye mask on a stick: purple, with sparkles."""
    shape = "M-58 -14C-40 -34 -12 -26 0 -14C12 -26 40 -34 58 -14C62 4 48 24 26 22C12 20 6 12 0 8C-6 12 -12 20 -26 22C-48 24 -62 4 -58 -14Z"
    sparkle = lambda x, y, r: (f'<path d="M{x} {y - r}Q{x} {y} {x + r} {y}Q{x} {y} {x} {y + r}Q{x} {y} {x - r} {y}Q{x} {y} {x} {y - r}Z" '
                               f'fill="{GLOW}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    return (
        shadow(52, 40)
        + dstroke("M44 18L60 60", "#c98a4b", 5)
        + f'<path class="k-o" d="{shape}" fill="#8150c4"/>'
        + mirror(f'<path class="k-o" d="M-44 -8C-36 -18 -20 -18 -14 -6C-20 6 -38 6 -44 -8Z" fill="#fbf6ee" stroke-width="2.5"/>')
        + f'<path d="M-50 -20C-38 -30 -20 -26 -12 -18" fill="none" stroke="#b58cf0" stroke-width="3" stroke-linecap="round"/>'
        + sparkle(-58, -34, 8) + sparkle(56, -36, 6) + sparkle(0, -30, 5)
    )


def broom():
    """A witch's broom, lying on the slant: a long handle and a tied bundle of straw."""
    straws = "".join(f'<path d="M{-30 + k * 5} {18 + (k % 3)}L{-64 + k * 7} {50 + (k % 2) * 6}" stroke="#c9922f" stroke-width="2"/>' for k in range(7))
    return (
        shadow(56, 60)
        + dstroke("M62 -52L-12 8", "#b5774a", 6)
        + f'<path class="k-o" d="M-8 4C-20 10 -40 20 -66 50C-50 60 -30 60 -10 56C-6 40 -2 24 4 12Z" fill="#f2c14e"/>'
        + straws
        + f'<path class="k-o" d="M-14 0L4 16L-2 22L-20 6Z" fill="{ORANGE}" stroke-width="2.5"/>'
    )


HALLOWEEN = [("ghost", lambda: ghost()), ("witch", witch), ("candy", candy), ("monster", monster), ("mask", mask), ("broom", broom)]


# ---------------------------------------------------------------- the ship
def jack(x, y, s=1.0):
    """A jack-o'-lantern, glowing."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 -14V-20" stroke="#5aa83b" stroke-width="4" stroke-linecap="round"/>'
            f'<ellipse class="k-o" cx="0" cy="0" rx="16" ry="13" fill="{ORANGE}" stroke-width="2.5"/>'
            f'<path d="M-6 -12Q-8 0 -6 12M6 -12Q8 0 6 12" fill="none" stroke="{ORANGE_DARK}" stroke-width="2"/>'
            f'<path d="M-9 -4L-5 -8L-2 -3ZM9 -4L5 -8L2 -3ZM-8 4Q0 10 8 4Q0 7 -8 4Z" fill="{GLOW}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/></g>')


def ghost_ship():
    """The Ghost Ship on its waterline (y=0): a purple hull with glowing portholes, two masts of patched sails (the
    big one has a friendly ghost face), an orange flag, a jack-o'-lantern at the bow and a little ghost floating above."""
    big_sail = "M-34 -118Q-6 -124 22 -118Q28 -84 22 -44L13 -38L4 -44L-6 -38L-15 -44L-24 -38L-34 -44Q-40 -84 -34 -118Z"
    small_sail = "M34 -92Q50 -96 64 -92Q68 -70 64 -46L57 -40L49 -46L41 -40L34 -46Q30 -70 34 -92Z"
    return (
        '<g class="bob">'
        # masts, sails and the flag
        + dstroke("M-6 -20V-136", "#6b4a2e", 5) + dstroke("M48 -20V-104", "#6b4a2e", 4)
        + f'<path class="k-o" d="{big_sail}" fill="{SAIL}"/>'
        + f'<path class="k-o" d="{small_sail}" fill="{SAIL}"/>'
        + f'<rect x="-22" y="-70" width="12" height="10" rx="2" fill="#d9d1ee" stroke="{INK}" stroke-width="1.5"/>'
        + f'<ellipse cx="-16" cy="-92" rx="4.5" ry="6" fill="{INK}"/><ellipse cx="4" cy="-92" rx="4.5" ry="6" fill="{INK}"/>'
        + f'<ellipse cx="-6" cy="-76" rx="5" ry="6.5" fill="{INK}"/>'
        + f'<path class="k-o cloth" d="M-6 -136L20 -130L-6 -122Z" fill="{ORANGE}" stroke-width="2"/>'
        # the hull: raised at the stern (left), with a rail and glowing portholes
        + f'<path class="k-o" d="M-76 -44L-58 -44L-52 -24H70L78 -30L64 4Q0 14 -58 4Z" fill="{HULL}"/>'
        + f'<path d="M-62 -6Q0 4 62 -6" fill="none" stroke="{HULL_DARK}" stroke-width="4"/>'
        + f'<path d="M-52 -24H70" stroke="{INK}" stroke-width="3"/>'
        + "".join(f'<path d="M{x} -24V-32" stroke="{INK}" stroke-width="2.5"/>' for x in (-40, -20, 0, 20, 40, 60))
        + f'<path d="M-50 -32H72" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + "".join(f'<circle class="lantern" style="animation-delay:-{k * .5}s" cx="{x}" cy="-12" r="5.5" fill="{GLOW}" stroke="{INK}" stroke-width="2.5"/>'
                  for k, x in enumerate((-34, -8, 18, 44)))
        # a lantern hanging at the stern, and the jack-o'-lantern at the bow
        + f'<path d="M-70 -44V-52" stroke="{INK}" stroke-width="2.5"/><rect class="lantern" x="-75" y="-62" width="10" height="12" rx="3" fill="{GLOW}" stroke="{INK}" stroke-width="2"/>'
        + jack(62, -42, .9)
        + "</g>"
        # the ghost that floats above the deck (in a group of its own, so it can drift)
        + f'<g transform="translate(-66 -80)"><g class="ghost-float">{ghost(.42)}</g></g>'
        + '<path class="wake" d="M-86 12q10 -6 20 0t20 0M52 14q10 -6 20 0t20 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
    )


# ---------------------------------------------------------------- the story's night scene
def night():
    """680 x 464 like the scenes: night sky, moon and stars, a dark sea with the Ghost Ship, sand in front."""
    stars = "".join(f'<path d="M{x} {y - r}L{x + r * .3:.1f} {y - r * .3:.1f}L{x + r} {y}L{x + r * .3:.1f} {y + r * .3:.1f}L{x} {y + r}'
                    f'L{x - r * .3:.1f} {y + r * .3:.1f}L{x - r} {y}L{x - r * .3:.1f} {y - r * .3:.1f}Z" fill="#fff6c0"/>'
                    for x, y, r in ((80, 60, 7), (180, 110, 5), (300, 50, 6), (420, 96, 4), (620, 70, 6), (560, 150, 4), (40, 170, 4), (250, 170, 3)))
    return (
        '<defs><linearGradient id="night-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d2a5c"/>'
        '<stop offset="1" stop-color="#5a4f95"/></linearGradient></defs>'
        '<rect x="20" y="12" width="640" height="440" rx="24" fill="url(#night-sky)"/>' + stars
        + f'<circle cx="500" cy="96" r="54" fill="#fff4c4" opacity=".25"/><circle class="k-o" cx="500" cy="96" r="42" fill="#fff1b8"/>'
        + '<circle cx="486" cy="84" r="8" fill="#f1dd8e"/><circle cx="512" cy="108" r="6" fill="#f1dd8e"/>'
        + '<path d="M20 262H660V452H20Z" fill="#2f5d8a"/>'
        + '<path d="M20 262H660" stroke="#8fb8e0" stroke-width="3" opacity=".6"/>'
        + "".join(f'<path d="M{x} {y}q8 -5 16 0t16 0" fill="none" stroke="#8fb8e0" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
                  for x, y in ((70, 300), (220, 290), (330, 330), (600, 310), (150, 350)))
        + '<path d="M470 272Q500 268 520 274" stroke="#fff1b8" stroke-width="4" stroke-linecap="round" opacity=".5"/>'
        + f'<g transform="translate(440 300) scale(1.25)">{ghost_ship()}</g>'
        + f'<path class="k-o" d="M20 372Q180 350 340 368T660 360V452H20Z" fill="#e8cf9a"/>'
        + '<path d="M60 410q6 -3 12 0M500 420q6 -3 12 0M300 430q6 -3 12 0" stroke="#c9ab6e" stroke-width="3" stroke-linecap="round" fill="none"/>'
        + jack(610, 396, 1.3) + jack(90, 404, 1.0)
    )


def export():
    AV = "-82 -68 164 136"
    art = {w: f'<svg viewBox="{AV}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{fn()}</svg>' for w, fn in HALLOWEEN}
    art["_scene-ghost"] = (f'<svg viewBox="0 0 680 464" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Ghost Ship at night">'
                           f'<defs><clipPath id="k-night"><rect x="20" y="12" width="640" height="440" rx="24"/></clipPath></defs>'
                           f'<g clip-path="url(#k-night)">{night()}</g>'
                           f'<rect x="20" y="12" width="640" height="440" rx="24" fill="none" stroke="{INK}" stroke-width="3"/></svg>')
    art["_ghost-ship"] = f'<svg viewBox="-100 -150 200 170" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{ghost_ship()}</svg>'
    return art


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    art = export()
    cells = "".join(f'<figure>{art[w]}<figcaption>{w}</figcaption></figure>' for w, _ in HALLOWEEN)
    html = (
        "<!doctype html><meta charset=utf-8><title>Halloween preview</title><link rel=stylesheet href=../css/style.css><style>"
        "body{padding:24px}.grid{display:grid;grid-template-columns:repeat(6,160px);gap:12px}"
        "figure{margin:0;background:#fff;border:3px solid #3f3345;border-radius:18px;padding:6px;text-align:center;font-weight:800}"
        ".big{display:flex;gap:20px;margin-top:20px;align-items:center}.big>*{width:420px}.ship{background:#8fd3f4;border-radius:20px;width:260px!important}"
        "</style>"
        f'<div class=grid>{cells}</div><div class=big><div>{art["_scene-ghost"]}</div><div class=ship>{art["_ghost-ship"]}</div></div>'
    )
    out = os.path.join(here, "../../work/halloween_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
