from common import INK, fmt, svg_wrap

COLORS = [
    ("red", "#ef5b56", "#c9403b", "#c0392b", 150, -5),
    ("orange", "#ff9a3c", "#e07b1f", "#c95d05", 128, 3),
    ("yellow", "#ffd23f", "#e8b520", "#a47800", 160, -2),
    ("green", "#5cc36a", "#3f9e4d", "#2d8a3c", 138, 4),
    ("blue", "#4a9be8", "#2f7cc6", "#2268b0", 154, -4),
    ("purple", "#9b74e8", "#7a52cc", "#6a44c2", 130, 2),
    ("pink", "#f78fb3", "#e06b95", "#c9457a", 146, -3),
    ("brown", "#a8704a", "#87532f", "#7a4a2a", 122, 5),
]

BASE_Y = 236


def crayon(main, dark, hb):
    t = hb + 26
    return (
        f'<path class="k-o" d="M-15 {-hb}L-6 {-t}Q0 {-t - 5} 6 {-t}L15 {-hb}Z" fill="{main}"/>'
        f'<path d="M-9 {-hb - 5}L-5 {-t + 4}" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".45"/>'
        f'<rect class="k-o" x="-18" y="{-hb}" width="36" height="{hb}" rx="5" fill="{main}"/>'
        f'<rect x="-16.5" y="{-hb + 12}" width="33" height="7" fill="{dark}"/>'
        f'<rect x="-16.5" y="-22" width="33" height="7" fill="{dark}"/>'
        f'<path d="M-16.5 {fmt(-hb / 2 - 8)}q5.5 -5 11 0t11 0t11 0M-16.5 {fmt(-hb / 2 + 4)}q5.5 -5 11 0t11 0t11 0" '
        f'fill="none" stroke="{dark}" stroke-width="3"/>'
        f'<rect x="-12" y="{-hb + 4}" width="5" height="{hb - 8}" rx="2.5" fill="#fff" opacity=".3"/>'
    )


parts = ['<rect x="20" y="12" width="640" height="316" rx="24" fill="#fffaf0" stroke="#f2e2c2" stroke-width="2"/>']
for i, (name, main, dark, text, hb, rot) in enumerate(COLORS):
    cx = 77.5 + 75 * i
    parts.append(
        f'<g transform="translate({fmt(cx)} {BASE_Y})">'
        f'<g transform="rotate({rot})">{crayon(main, dark, hb)}</g>'
        f'<path d="M-24 24C-18 14 -12 14 -6 24S6 34 12 24S20 14 24 22" fill="none" stroke="{main}" stroke-width="7" stroke-linecap="round"/>'
        f'<text class="k-f" x="0" y="68" font-size="17" fill="{text}" text-anchor="middle">{name}</text>'
        "</g>"
    )

svg = svg_wrap(
    340,
    "Color words with crayons",
    "Eight crayons, each labeled with its color word: red, orange, yellow, green, blue, purple, pink, brown.",
    "".join(parts),
)
open("colors.svg", "w").write(svg)
print(len(svg), "bytes")
