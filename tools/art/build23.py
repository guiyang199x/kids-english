"""Pip's house: where Pip lives, next to him at the top of the home page, and the room inside it (#/house).

home_hero() - the house at the top of the home page, next to Pip (js/views/world.js). The mailbox flag is in
             <g class="mail-flag">; world.js raises it when a letter has come.
room()     - the room inside: a bookshelf (the stories), the sticker book on a desk, Pip TV on a shelf, and the door
             with the letter slot. Each <g class="home-spot" data-go="..."> is one thing to tap; SPOTS says where its name plate
             sits (in % of the room, for js/views/house.js). The letters in <g class="home-letter"> only show
             while one is waiting (.has-mail on the page).

Run `python3 build23.py` to preview both in work/house_preview.html.
"""
from common import INK
from build1 import shadow
from build16 import at, bunting, smoke
from build14 import pip, WAVE_LINES, FLOWERS

WALL, FLOOR, PLANK = "#fdf1dc", "#f0cfa0", "#d9b07a"
WOOD, WOOD_DARK = "#c98a4b", "#94592f"
ROOF, ROOF_DARK = "#6cc070", "#4f9a4f"


# ---------------------------------------------------------------- on the world map
def bamboo(x, y, h, s=1.0):
    """One bamboo stalk standing on (x, y), with joints and two leaves."""
    joints = "".join(f'<path d="M-4 {-k}H4" stroke="{INK}" stroke-width="2"/>' for k in range(14, h - 6, 14))
    return at(x, y, s,
        f'<rect class="k-o" x="-4" y="{-h}" width="8" height="{h}" rx="3" fill="#8fcf6a" stroke-width="2.5"/>' + joints
        + f'<path class="k-o" d="M3 {-h + 10}C12 {-h + 2} 20 {-h + 4} 24 {-h + 8}C16 {-h + 12} 9 {-h + 12} 3 {-h + 10}Z" fill="{ROOF}" stroke-width="2"/>'
        + f'<path class="k-o" d="M-3 {-h + 22}C-12 {-h + 14} -20 {-h + 16} -24 {-h + 20}C-16 {-h + 24} -9 {-h + 24} -3 {-h + 22}Z" fill="{ROOF}" stroke-width="2"/>')


def cottage():
    """Pip's house standing on y=0: cream walls, a bamboo-green roof, a round door and a warm window."""
    stripes = "".join(f'<path d="M{x} -50L{x * 0.25:.1f} -84" stroke="{ROOF_DARK}" stroke-width="2.5" stroke-linecap="round"/>'
                      for x in (-26, -12, 12, 26))
    return (
        '<ellipse cx="0" cy="2" rx="40" ry="6" fill="#3f3345" opacity=".12"/>'
        f'<rect class="k-o" x="-30" y="-52" width="60" height="52" rx="4" fill="#fff3dc"/>'
        f'<path class="k-o" d="M-42 -46Q-40 -54 -34 -58L-4 -88Q0 -92 4 -88L34 -58Q40 -54 42 -46Z" fill="{ROOF}"/>'
        + stripes
        + f'<path d="M-42 -46Q-40 -54 -34 -58L-4 -88Q0 -92 4 -88L34 -58Q40 -54 42 -46Z" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        # a round attic window with a light on
        + '<circle class="k-o" cx="0" cy="-64" r="7" fill="#ffe89a" stroke-width="2.5"/>'
        # the door and the window
        + f'<path class="k-o" d="M-2 0V-22A10 10 0 0 1 18 -22V0Z" fill="{WOOD}"/><circle cx="14" cy="-11" r="1.8" fill="{INK}"/>'
        + '<rect class="k-o" x="-22" y="-38" width="15" height="15" rx="3" fill="#ffe89a" stroke-width="2.5"/>'
        + f'<path d="M-14.5 -38V-23M-22 -30.5H-7" stroke="{INK}" stroke-width="2"/>'
        # chimney
        + f'<rect class="k-o" x="16" y="-86" width="10" height="18" rx="2" fill="#ef5b56" stroke-width="2.5"/>'
    )


def mailbox(flag_up=True):
    """A red mailbox on a post, standing on y=0. Its flag is a group of its own so it can be raised."""
    flag = (f'<g class="mail-flag"><path d="M10 -30V-44" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<path class="k-o" d="M10 -44H20V-37H10Z" fill="#ffd23f" stroke-width="2"/></g>')
    return (
        f'<path d="M0 0V-22" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><path d="M0 0V-22" stroke="{WOOD}" stroke-width="3"/>'
        f'<path class="k-o" d="M-12 -22V-34A8 8 0 0 1 -4 -42H4A8 8 0 0 1 12 -34V-22Z" fill="#ef5b56" stroke-width="2.5"/>'
        f'<path d="M-6 -30H4" stroke="#b83b37" stroke-width="2.5" stroke-linecap="round"/>'
        + flag
    )


def home_hero():
    """The house for the top of the home page, where Pip stands: the cottage on a patch of grass, bamboo on one
    side and the mailbox on the other, standing on y=0."""
    return (
        '<ellipse cx="0" cy="4" rx="74" ry="9" fill="#9fd784" stroke="#3f3345" stroke-width="2" stroke-opacity=".25"/>'
        + bamboo(-50, 4, 64) + bamboo(-38, 6, 46)
        + at(0, 2, 1, cottage())
        + smoke(21, -96)
        + at(48, 4, 1, mailbox())
        + at(-14, 10, .5, FLOWERS)
    )


# ---------------------------------------------------------------- inside
W, H = 680, 440
TOP = 300  # where the wall meets the floor

# the things to tap: data-go -> (name plate x %, y %)
SPOTS = {"books": (18, 90), "stickers": (43, 90), "tv": (69, 43), "mail": (85, 92)}


def back():
    planks = "".join(f'<path d="M0 {y}H{W}" stroke="{PLANK}" stroke-width="2"/>' for y in (338, 386))
    return (
        f'<rect width="{W}" height="{TOP}" fill="{WALL}"/>'
        f'<rect y="{TOP}" width="{W}" height="{H - TOP}" fill="{FLOOR}"/>' + planks
        + f'<rect y="{TOP - 8}" width="{W}" height="12" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
        + bunting(20, 660, 16, 18)
    )


def sea_window(x0=242, y0=64, w=150, h=118):
    """A round-topped window with the sea outside and a little boat on it."""
    x1, y1, r = x0 + w, y0 + h, w / 2
    frame = f'M{x0} {y1}V{y0 + r}A{r} {r} 0 0 1 {x1} {y0 + r}V{y1}Z'
    sea_y = y0 + h * .62
    return (
        f'<path d="{frame}" fill="#bfe6ff"/>'
        f'<path d="M{x0} {sea_y}H{x1}V{y1}H{x0}Z" fill="#8fd3f4"/>'
        f'<path d="M{x0 + 14} {sea_y + 16}q7 -5 14 0t14 0M{x0 + 90} {sea_y + 28}q7 -5 14 0t14 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="{x1 - 34}" cy="{y0 + 46}" r="13" fill="#ffd23f"/>'
        # a boat far off
        + f'<path d="M{x0 + 40} {sea_y - 1}h30l-5 7h-20Z" fill="#ef5b56"/><path d="M{x0 + 55} {sea_y - 3}V{sea_y - 26}L{x0 + 70} {sea_y - 3}Z" fill="#fff"/>'
        + f'<path d="{frame}" fill="none" stroke="#fff" stroke-width="10"/>'
        + f'<path d="M{x0 + r} {y0}V{y1}M{x0} {y0 + r + 8}H{x1}" stroke="#fff" stroke-width="6"/>'
        + f'<path d="{frame}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        + f'<rect class="k-o" x="{x0 - 10}" y="{y1 - 2}" width="{w + 20}" height="11" rx="4" fill="#fff"/>'
    )


def bookshelf(x0=36, y0=78, x1=210, y1=334):
    """The shelf of storybooks: three shelves of colorful spines, one book leaning and one lying down."""
    shelves = (150, 230)
    cols = ["#ef5b56", "#4a9be8", "#ffd23f", "#6cc070", "#d65b9a", "#ffb13b", "#8150c4", "#4fc1b9"]
    books = ""
    for row, (top, bottom) in enumerate(((y0 + 14, shelves[0]), (shelves[0] + 8, shelves[1]), (shelves[1] + 8, y1 - 14))):
        x, k = x0 + 16, row * 3
        while x < x1 - 30:
            w = 16 + (k * 7) % 9
            h = (bottom - top) - 6 - (k * 5) % 16
            c = cols[k % len(cols)]
            books += (f'<rect class="k-o" x="{x}" y="{bottom - h}" width="{w}" height="{h}" rx="2" fill="{c}" stroke-width="2.5"/>'
                      f'<path d="M{x + 3} {bottom - h + 8}H{x + w - 3}M{x + 3} {bottom - 12}H{x + w - 3}" stroke="#fff" stroke-width="2.5" opacity=".7"/>')
            x += w + 2
            k += 1
    # a book leaning on the last one, top shelf
    books += f'<rect class="k-o" x="{x1 - 34}" y="{shelves[0] - 50}" width="16" height="50" rx="2" fill="#ffb13b" stroke-width="2.5" transform="rotate(14 {x1 - 26} {shelves[0]})"/>'
    return (
        f'<ellipse cx="{(x0 + x1) / 2}" cy="{y1 + 4}" rx="{(x1 - x0) / 2 + 8}" ry="8" fill="{INK}" opacity=".12"/>'
        f'<rect class="k-o" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="6" fill="{WOOD}"/>'
        f'<rect x="{x0 + 10}" y="{y0 + 10}" width="{x1 - x0 - 20}" height="{y1 - y0 - 20}" rx="3" fill="{WOOD_DARK}"/>'
        + books
        + "".join(f'<rect class="k-o" x="{x0 + 6}" y="{y}" width="{x1 - x0 - 12}" height="9" rx="3" fill="{WOOD}" stroke-width="2.5"/>' for y in shelves)
        # a globe on top
        + f'<path d="M{x0 + 40} {y0}V{y0 - 8}" stroke="{INK}" stroke-width="4"/><ellipse class="k-o" cx="{x0 + 40}" cy="{y0 - 4}" rx="14" ry="4" fill="{WOOD_DARK}" stroke-width="2.5"/>'
        + f'<circle class="k-o" cx="{x0 + 40}" cy="{y0 - 26}" r="18" fill="#8fd3f4"/>'
        + f'<path d="M{x0 + 30} {y0 - 36}c6 -2 10 4 6 8s2 8 -2 10M{x0 + 44} {y0 - 20}c4 -4 10 -2 10 4" fill="#6cc070" stroke="#4f9a4f" stroke-width="2"/>'
    )


def sticker_book(cx=300, top=262):
    """An open sticker album on the desk: two pages of round stickers, a gold star on the left page."""
    y = top - 24
    stickers = ""
    for i, (sx, sy, c) in enumerate(((-52, 8, "#ef5b56"), (-30, 4, "#4a9be8"), (26, 4, "#6cc070"), (48, 8, "#ffd23f"),
                                      (-46, 18, "#d65b9a"), (32, 16, "#ffb13b"), (52, 20, "#dcd3c6"))):
        stickers += f'<ellipse cx="{cx + sx}" cy="{y + sy}" rx="8" ry="5" fill="{c}" stroke="{INK}" stroke-width="1.8"/>'
    return (
        f'<g class="home-glow"><path d="M{cx - 76} {top - 2}L{cx - 62} {y - 10}Q{cx - 30} {y - 16} {cx} {y - 8}Q{cx + 30} {y - 16} {cx + 62} {y - 10}L{cx + 76} {top - 2}Q{cx + 38} {top - 8} {cx} {top}Q{cx - 38} {top - 8} {cx - 76} {top - 2}Z" '
        f'fill="#8150c4" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M{cx - 70} {top - 6}L{cx - 58} {y - 6}Q{cx - 28} {y - 12} {cx} {y - 4}V{top - 4}Q{cx - 36} {top - 11} {cx - 70} {top - 6}Z" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<path d="M{cx + 70} {top - 6}L{cx + 58} {y - 6}Q{cx + 28} {y - 12} {cx} {y - 4}V{top - 4}Q{cx + 36} {top - 11} {cx + 70} {top - 6}Z" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        + stickers
        + f'<path d="M{cx - 18} {y - 2}l3 6 6 1 -4 4 1 6 -6 -3 -6 3 1 -6 -4 -4 6 -1Z" fill="#ffd23f" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'
        + "</g>"
    )


def desk(x0=212, x1=388, top=262):
    legs = "".join(f'<rect class="k-o" x="{x}" y="{top + 10}" width="12" height="{360 - top - 10}" rx="3" fill="{WOOD_DARK}"/>' for x in (x0 + 14, x1 - 26))
    return (
        f'<ellipse cx="{(x0 + x1) / 2}" cy="362" rx="{(x1 - x0) / 2}" ry="7" fill="{INK}" opacity=".12"/>'
        + legs
        + f'<rect class="k-o" x="{x0}" y="{top}" width="{x1 - x0}" height="14" rx="4" fill="{WOOD}"/>'
    )


def front_door(x0=528, y0=108, x1=640, y1=372):
    """The front door with a letter slot; a letter sticks out of the slot and one lies on the mat when mail has come."""
    slot_y = 250
    cx = (x0 + x1) / 2
    letter = lambda x, y, rot: (f'<g transform="translate({x} {y}) rotate({rot})">'
                                f'<rect class="k-o" x="-20" y="-13" width="40" height="26" rx="3" fill="#fff" stroke-width="2.5"/>'
                                f'<path d="M-20 -13L0 3L20 -13" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
                                f'<rect x="8" y="-9" width="8" height="9" rx="1" fill="#ef5b56"/></g>')
    return (
        f'<rect x="{x0 - 10}" y="{y0 - 10}" width="{x1 - x0 + 20}" height="{y1 - y0 + 10}" rx="8" fill="#e8dccb" stroke="{INK}" stroke-width="3"/>'
        f'<rect class="k-o" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="4" fill="#4a9be8"/>'
        + "".join(f'<rect x="{x}" y="{y}" width="38" height="{h}" rx="4" fill="none" stroke="#2f7cc6" stroke-width="3.5"/>'
                  for x in (x0 + 12, x1 - 50) for y, h in ((y0 + 14, 110), (y0 + 170, 70)))
        + f'<circle class="k-o" cx="{x1 - 18}" cy="{y0 + 150}" r="6" fill="#ffc93c" stroke-width="2"/>'
        # the letter slot, a letter halfway through it
        + f'<g class="home-letter">{letter(cx, slot_y + 8, -4)}</g>'
        + f'<rect class="k-o" x="{cx - 28}" y="{slot_y}" width="56" height="12" rx="4" fill="#ffc93c" stroke-width="2.5"/>'
        + f'<path d="M{cx - 20} {slot_y + 6}H{cx + 20}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        # the mat, with a letter on it
        + f'<rect class="k-o" x="{x0 - 18}" y="{y1 + 2}" width="{x1 - x0 + 36}" height="16" rx="6" fill="#ef5b56" stroke-width="2.5"/>'
        + f'<g class="home-letter">{letter(cx - 36, y1 + 2, 12)}</g>'
    )


def tv(cx=470, shelf=156):
    """Pip TV: a little retro TV with rabbit-ear antennas, on a shelf on the wall. The screen shows a play button."""
    x0, x1, y0 = cx - 46, cx + 46, shelf - 70
    return (
        f'<path d="M{cx} {y0 + 2}L{cx - 22} {y0 - 26}M{cx} {y0 + 2}L{cx + 20} {y0 - 30}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        + f'<circle cx="{cx - 22}" cy="{y0 - 26}" r="4" fill="#ef5b56" stroke="{INK}" stroke-width="2"/><circle cx="{cx + 20}" cy="{y0 - 30}" r="4" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
        + f'<rect class="k-o" x="{x0}" y="{y0}" width="{x1 - x0}" height="66" rx="14" fill="#ef9a5a"/>'
        + f'<rect class="k-o tv-glass" x="{x0 + 9}" y="{y0 + 9}" width="58" height="48" rx="9" fill="#8fd3f4" stroke-width="2.5"/>'
        + f'<path d="M{x0 + 32} {y0 + 23}V{y0 + 43}L{x0 + 48} {y0 + 33}Z" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
        + f'<path d="M{x0 + 14} {y0 + 18}Q{x0 + 18} {y0 + 13} {x0 + 26} {y0 + 13}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
        + "".join(f'<circle cx="{x1 - 13}" cy="{y0 + y}" r="5" fill="{c}" stroke="{INK}" stroke-width="2"/>' for y, c in ((20, "#ffd23f"), (36, "#6cc070")))
        + "".join(f'<path d="M{x1 - 18} {y0 + y}H{x1 - 8}" stroke="{INK}" stroke-width="2"/>' for y in (48, 53))
        # the shelf
        + f'<rect class="k-o" x="{cx - 60}" y="{shelf - 4}" width="120" height="10" rx="3" fill="{WOOD}"/>'
        + f'<path d="M{cx - 44} {shelf + 6}L{cx - 36} {shelf + 20}M{cx + 44} {shelf + 6}L{cx + 36} {shelf + 20}" stroke="{WOOD_DARK}" stroke-width="5" stroke-linecap="round"/>'
    )


def spot(go, label, inner):
    return f'<g class="home-spot" data-go="{go}" tabindex="0" role="button" aria-label="{label}">{inner}</g>'


def room():
    return (
        back()
        + sea_window()
        + spot("tv", "Pip TV", tv())
        + spot("books", "Storybooks", bookshelf())
        + spot("stickers", "Sticker book", desk() + sticker_book())
        # a potted bamboo by the door
        + f'<path class="k-o" d="M474 368L468 334H504L498 368Z" fill="#ef9a5a"/>'
        + bamboo(478, 336, 90) + bamboo(492, 336, 70)
        + spot("mail", "Mailbox", front_door())
        # the rug, and Pip waving on it
        + f'<ellipse class="k-o" cx="420" cy="398" rx="84" ry="20" fill="#ffd23f"/><ellipse cx="420" cy="398" rx="60" ry="12" fill="none" stroke="#ef9a5a" stroke-width="3" stroke-dasharray="8 6"/>'
        + f'<g class="home-pip">{at(420, 312, .95, pip("wave", extra=WAVE_LINES))}</g>'
    )


def export():
    """ART keys for export_js.py, and WORLD["home"] (where the room's name plates sit)."""
    art = {
        "_home-hero": f'<svg viewBox="-80 -104 160 118" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{home_hero()}</svg>',
        "_home-room": f'<svg class="home-room" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
                      f'aria-label="Pip\'s room: a bookshelf, a sticker book on a desk, a TV and the front door">{room()}</svg>',
    }
    return art, {"spots": SPOTS}


if __name__ == "__main__":
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    art, data = export()
    plates = "".join(f'<span class="plate" style="left:{x}%;top:{y}%">{go}</span>' for go, (x, y) in data["spots"].items())
    html = (
        "<!doctype html><meta charset=utf-8><title>Pip's house preview</title><style>"
        "body{margin:0;padding:24px;background:#fbf6ee;font-family:Nunito,-apple-system,sans-serif;color:#3f3345}"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        ".map{width:240px;margin-bottom:20px}.map svg{width:100%}"
        ".room{position:relative;width:900px}.room svg{width:100%;display:block;border:3px solid #3f3345;border-radius:20px}"
        ".plate{position:absolute;transform:translate(-50%,-50%);background:#fff;border:2px solid #3f3345;border-radius:10px;padding:2px 8px;font-weight:800}"
        "</style>"
        f'<div class="map has-mail">{art["_home-hero"]}</div><div class="room has-mail">{art["_home-room"]}{plates}</div>'
    )
    out = os.path.join(here, "../../work/house_preview.html")
    open(out, "w").write(html)
    print("wrote", os.path.normpath(out))
