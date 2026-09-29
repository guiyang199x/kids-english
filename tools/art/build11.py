"""Where is it? The cat and a cardboard box (plus the table for "under").
Each drawing is centered on (0,0), roughly within x -80..80, y -66..66."""
from common import INK
from build1 import shadow, CAT
from build10 import table

BOX, BOX_DARK, BOX_LIGHT = "#e0a86a", "#c98a4b", "#f2c58e"


def cat(x, y, s):
    return f'<g transform="translate({x} {y}) scale({s})">{CAT}</g>'


def box_body(x, y, w=84, h=56):
    """Closed box, front face spanning x-w/2..x+w/2, y..y+h, with a top lid."""
    l, r = x - w / 2, x + w / 2
    return (
        f'<path class="k-o" d="M{l} {y}L{l + 12} {y - 12}H{r + 12}L{r} {y}Z" fill="{BOX_LIGHT}"/>'
        f'<path class="k-o" d="M{r} {y}L{r + 12} {y - 12}V{y + h - 12}L{r} {y + h}Z" fill="{BOX_DARK}"/>'
        f'<rect class="k-o" x="{l}" y="{y}" width="{w}" height="{h}" rx="2" fill="{BOX}"/>'
        f'<path d="M{x - 8} {y}V{y + 18}H{x + 8}V{y}" fill="#f7e3c4" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    )


def open_box_back(x, y, w=84):
    """Back flaps and dark inside of an open box whose front top edge is at y."""
    l, r = x - w / 2, x + w / 2
    return (
        f'<path class="k-o" d="M{l + 12} {y - 12}L{l + 2} {y - 34}H{r + 2}L{r + 12} {y - 12}Z" fill="{BOX_LIGHT}"/>'
        f'<path class="k-o" d="M{l} {y}L{l + 12} {y - 12}H{r + 12}L{r} {y}Z" fill="#8a5a2e"/>'
    )


def open_box_front(x, y, w=84, h=56):
    l, r = x - w / 2, x + w / 2
    return (
        f'<path class="k-o" d="M{r} {y}L{r + 12} {y - 12}V{y + h - 12}L{r} {y + h}Z" fill="{BOX_DARK}"/>'
        f'<rect class="k-o" x="{l}" y="{y}" width="{w}" height="{h}" rx="2" fill="{BOX}"/>'
        f'<path class="k-o" d="M{l} {y}L{l - 14} {y + 20}L{l - 4} {y + 24}L{l + 2} {y + 6}Z" fill="{BOX_LIGHT}" stroke-width="2.5"/>'
        f'<path class="k-o" d="M{r} {y}L{r + 16} {y + 16}L{r + 24} {y + 10}L{r + 12} {y - 12}Z" fill="{BOX_LIGHT}" stroke-width="2.5"/>'
    )


def p_in():
    return shadow(58, 56) + open_box_back(-6, 6) + cat(-6, -14, 0.5) + open_box_front(-6, 6)


def p_on():
    return shadow(58, 56) + box_body(-6, 10) + cat(-2, -26, 0.46)


def p_under():
    return table() + cat(-4, 30, 0.42)


def p_next_to():
    return shadow(58, 72) + box_body(-30, 6) + cat(48, 32, 0.42)


def p_behind():
    return shadow(58, 56) + cat(18, -14, 0.36) + box_body(-6, 6)


def p_in_front_of():
    return shadow(60, 56) + box_body(-6, -8) + cat(-6, 30, 0.5)


def box():
    return shadow(58, 56) + box_body(-6, 6)


# (art key, drawing); lesson items point at these with an `art` key.
PREPOSITIONS = [
    ("where-in", p_in), ("where-on", p_on), ("where-under", p_under),
    ("where-next-to", p_next_to), ("where-behind", p_behind), ("where-in-front-of", p_in_front_of),
    ("box", box),
]
