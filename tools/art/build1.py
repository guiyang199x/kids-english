import math
from common import INK, fmt, smooth_path, svg_wrap

SHADOW = f'<ellipse cx="0" cy="{{y}}" rx="{{rx}}" ry="6" fill="{INK}" opacity=".12"/>'


def shadow(y, rx):
    return SHADOW.format(y=y, rx=rx)


APPLE_BODY = "M0 -28C12 -42 50 -42 50 -4C50 30 28 52 14 50C8 49 4 46 0 46C-4 46 -8 49 -14 50C-28 52 -50 30 -50 -4C-50 -42 -12 -42 0 -28Z"
APPLE = (
    shadow(54, 38)
    + f'<path d="M0 -26C0 -38 3 -46 9 -52" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
    + '<path d="M0 -26C0 -38 3 -46 9 -52" fill="none" stroke="#8b5a3c" stroke-width="4" stroke-linecap="round"/>'
    + '<path class="k-o" d="M5 -40C14 -56 32 -60 42 -52C34 -40 18 -34 5 -40Z" fill="#6cc070"/>'
    + '<path d="M10 -42Q24 -49 35 -52" fill="none" stroke="#4a9a4f" stroke-width="2" stroke-linecap="round"/>'
    + f'<path d="{APPLE_BODY}" fill="#ef5b56"/>'
    + '<path d="M29.5 -35.5C40.5 -32.5 50 -23 50 -4C50 30 28 52 14 50C30 40 40 22 39 0C38 -16 35 -27 29.5 -35.5Z" fill="#d8453f"/>'
    + f'<path class="k-o" d="{APPLE_BODY}" fill="none"/>'
    + '<path d="M-37 -10C-37 -21 -30 -28 -21 -30" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".85"/>'
    + '<circle cx="-38" cy="2" r="3.5" fill="#fff" opacity=".85"/>'
)


def beach_ball(r=46, cx=0.0, cy=0.0, tilt=38, rho=26, offset=8):
    t = math.radians(tilt)
    rh = math.radians(rho)

    def proj(lam, phi):
        x = math.cos(lam) * math.sin(phi)
        y = -math.sin(lam)
        z = math.cos(lam) * math.cos(phi)
        y2 = y * math.cos(t) + z * math.sin(t)
        z2 = -y * math.sin(t) + z * math.cos(t)
        x3 = x * math.cos(rh) - y2 * math.sin(rh)
        y3 = x * math.sin(rh) + y2 * math.cos(rh)
        return (cx + r * x3, cy + r * y3, z2)

    def lam_star(phi):
        return math.atan2(-math.cos(phi) * math.cos(t), math.sin(t))

    def meridian(phi, step=15):
        ls = lam_star(phi)
        lams = []
        a = math.pi / 2
        while a > ls + 1e-9:
            lams.append(a)
            a -= math.radians(step)
        lams.append(ls)
        return [proj(l, phi)[:2] for l in lams]

    def ang(p):
        return math.atan2(p[1] - cy, p[0] - cx)

    parts = []
    colors = ["#ef5b56", "#ffc93c", "#4a9be8"]
    for k, col in enumerate(colors):
        p1 = math.radians(offset + k * 120)
        p2 = p1 + math.radians(60)
        m1 = meridian(p1)
        m2 = meridian(p2)[::-1]
        a_pt, b_pt = m1[-1], m2[0]
        mid = proj(lam_star((p1 + p2) / 2), (p1 + p2) / 2)
        a0, a1, am = ang(a_pt), ang(b_pt), ang(mid)
        d = (a1 - a0) % (2 * math.pi)
        dm = (am - a0) % (2 * math.pi)
        sweep = 1 if dm < d else 0
        span = d if sweep == 1 else 2 * math.pi - d
        large = 1 if span > math.pi else 0
        path = smooth_path(m1)
        path += f"A{r} {r} 0 {large} {sweep} {fmt(b_pt[0])} {fmt(b_pt[1])}"
        path += smooth_path(m2, start_cmd=False)[0:]
        parts.append(f'<path d="{path}Z" fill="{col}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
    cap = [proj(math.radians(76), math.radians(a))[:2] for a in range(0, 360, 30)]
    parts.append(f'<path d="{smooth_path(cap, closed=True)}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    return parts


def ball():
    r = 46
    parts = beach_ball(r=r, cx=0, cy=0, tilt=55, rho=22, offset=-20)
    hl = (
        '<path d="M-37 -14A40 40 0 0 1 -18 -35" fill="none" stroke="#fff" stroke-width="5" '
        'stroke-linecap="round" opacity=".7"/>'
    )
    return (
        shadow(54, 36)
        + f'<circle cx="0" cy="0" r="{r}" fill="#fff"/>'
        + "".join(parts)
        + hl
        + f'<circle class="k-o" cx="0" cy="0" r="{r}" fill="none"/>'
    )


CAT_EAR = (
    '<path class="k-o" d="M-46 -4C-52 -28 -50 -48 -44 -58C-41 -62 -37 -61 -33 -58C-26 -52 -17 -42 -10 -30Z" fill="#ffb54c"/>'
    + '<path d="M-41 -20C-43 -34 -42 -44 -39.5 -50C-35 -46 -28 -40 -22 -32Z" fill="#ffb3bd"/>'
)
CAT = (
    shadow(58, 40)
    + CAT_EAR
    + f'<g transform="scale(-1 1)">{CAT_EAR}</g>'
    + '<path class="k-o" d="M-54 12C-54 -22 -30 -36 0 -36C30 -36 54 -22 54 12C54 40 30 52 0 52C-30 52 -54 40 -54 12Z" fill="#ffb54c"/>'
    + '<path d="M-11 -31L-9 -22M0 -32L0 -23M11 -31L9 -22" stroke="#e8892b" stroke-width="4" stroke-linecap="round"/>'
    + '<ellipse cx="0" cy="28" rx="17" ry="11" fill="#ffe7c4"/>'
    + '<ellipse cx="-36" cy="15" rx="8" ry="5" fill="#ff7d93" opacity=".45"/>'
    + '<ellipse cx="36" cy="15" rx="8" ry="5" fill="#ff7d93" opacity=".45"/>'
    + f'<ellipse cx="-21" cy="5" rx="7" ry="8.5" fill="{INK}"/><ellipse cx="21" cy="5" rx="7" ry="8.5" fill="{INK}"/>'
    + '<circle cx="-18.5" cy="1.5" r="2.8" fill="#fff"/><circle cx="23.5" cy="1.5" r="2.8" fill="#fff"/>'
    + '<circle cx="-23" cy="9.5" r="1.3" fill="#fff"/><circle cx="19" cy="9.5" r="1.3" fill="#fff"/>'
    + f'<path d="M-26 27L-62 21M-26 33L-62 37M26 27L62 21M26 33L62 37" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
    + f'<path d="M-5.5 19L5.5 19L0 25Z" fill="#f47c96" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    + f'<path d="M0 25C0 31 -7 33 -10 28M0 25C0 31 7 33 10 28" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
)

DOG_EAR = '<path class="k-o" d="M-24 -42C-42 -50 -62 -40 -66 -16C-69 4 -62 22 -52 24C-42 26 -38 14 -36 -2C-34 -18 -30 -32 -24 -42Z" fill="#b5774a"/>'
DOG = (
    shadow(56, 40)
    + '<path class="k-o" d="M-44 -2C-44 -32 -24 -44 0 -44C24 -44 44 -32 44 -2C44 30 26 50 0 50C-26 50 -44 30 -44 -2Z" fill="#f2cf98"/>'
    + '<path d="M8 -20C18 -26 32 -22 34 -10C36 2 26 8 16 6C6 4 2 -12 8 -20Z" fill="#dca565"/>'
    + DOG_EAR
    + f'<g transform="scale(-1 1)">{DOG_EAR}</g>'
    + '<ellipse cx="0" cy="25" rx="22" ry="17" fill="#fff4e2"/>'
    + '<ellipse cx="-29" cy="13" rx="7" ry="4.5" fill="#ff7d93" opacity=".45"/>'
    + '<ellipse cx="29" cy="13" rx="7" ry="4.5" fill="#ff7d93" opacity=".45"/>'
    + f'<circle cx="-17" cy="-6" r="6.5" fill="{INK}"/><circle cx="17" cy="-6" r="6.5" fill="{INK}"/>'
    + '<circle cx="-15" cy="-8.5" r="2.3" fill="#fff"/><circle cx="19" cy="-8.5" r="2.3" fill="#fff"/>'
    + f'<path d="M-5 29C-6 39 6 39 5 29Z" fill="#ff7c93" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    + f'<path d="M0 20L0 26M0 26C-3 31 -11 31 -13 26M0 26C3 31 11 31 13 26" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    + f'<ellipse cx="0" cy="15" rx="9" ry="6.5" fill="{INK}"/>'
    + '<ellipse cx="-3" cy="13" rx="3" ry="1.6" fill="#fff" opacity=".8"/>'
)

ELE_COL = "#a9bcd6"
ELE_EAR = (
    f'<ellipse class="k-o" cx="-44" cy="-6" rx="28" ry="34" fill="{ELE_COL}" transform="rotate(-12 -44 -6)"/>'
    + '<ellipse cx="-46" cy="-4" rx="17" ry="23" fill="#f6b7c9" transform="rotate(-12 -46 -4)"/>'
)
TRUNK = "M0 6C0 26 -4 40 4 48C10 54 20 52 20 42"
ELEPHANT = (
    shadow(62, 46)
    + ELE_EAR
    + f'<g transform="scale(-1 1)">{ELE_EAR}</g>'
    + f'<path d="{TRUNK}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
    + f'<path class="k-o" d="M-32 -10C-32 -38 -18 -46 0 -46C18 -46 32 -38 32 -10C32 12 20 26 0 26C-20 26 -32 12 -32 -10Z" fill="{ELE_COL}"/>'
    + f'<path d="{TRUNK}" fill="none" stroke="{ELE_COL}" stroke-width="16" stroke-linecap="round"/>'
    + f'<path d="M-7 31Q-1 34 5 31M-7 39Q-1 42 5 39" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" opacity=".45"/>'
    + '<ellipse cx="-21" cy="4" rx="6" ry="4" fill="#ff7d93" opacity=".45"/>'
    + '<ellipse cx="21" cy="4" rx="6" ry="4" fill="#ff7d93" opacity=".45"/>'
    + f'<circle cx="-13" cy="-12" r="5.5" fill="{INK}"/><circle cx="13" cy="-12" r="5.5" fill="{INK}"/>'
    + '<circle cx="-11" cy="-14" r="2" fill="#fff"/><circle cx="15" cy="-14" r="2" fill="#fff"/>'
    + f'<path d="M-3 -46Q-6 -55 -1 -58M3 -46Q4 -54 9 -55" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
)

FIN = "#ffd166"
FISH = (
    '<g transform="translate(6 0)">'
    + f'<path class="k-o" d="M30 0L56 -24C61 -28 67 -25 65 -18L58 0L65 18C67 25 61 28 56 24Z" fill="{FIN}"/>'
    + f'<path class="k-o" d="M-20 -26C-14 -48 8 -50 18 -24Z" fill="{FIN}"/>'
    + f'<path class="k-o" d="M-2 28C2 44 14 44 18 24Z" fill="{FIN}"/>'
    + '<path class="k-o" d="M-54 2C-48 -24 -16 -36 8 -31C20 -28 30 -18 36 -6C38 -2 38 4 36 8C30 20 20 28 8 31C-16 36 -48 26 -54 2Z" fill="#ff9a52"/>'
    + '<path d="M10 -20q5 5 10 0M22 -11q5 5 10 0M18 10q5 5 10 0M6 19q5 5 10 0" fill="none" stroke="#e36f2a" stroke-width="2.5" stroke-linecap="round"/>'
    + f'<path d="M-6 6C2 -2 14 0 14 10C6 14 -2 12 -6 6Z" fill="{FIN}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    + f'<circle cx="-32" cy="-6" r="9" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
    + f'<circle cx="-34" cy="-5" r="5" fill="{INK}"/><circle cx="-35.5" cy="-7" r="1.8" fill="#fff"/>'
    + '<ellipse cx="-24" cy="10" rx="5.5" ry="3.5" fill="#ff5d73" opacity=".4"/>'
    + f'<path d="M-52 8Q-47 13 -42 9" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    + "</g>"
    + f'<circle cx="-62" cy="-20" r="6" fill="#fff" fill-opacity=".75" stroke="{INK}" stroke-width="2"/>'
    + f'<circle cx="-70" cy="-38" r="4.5" fill="#fff" fill-opacity=".75" stroke="{INK}" stroke-width="2"/>'
    + f'<circle cx="-60" cy="-51" r="3" fill="#fff" fill-opacity=".75" stroke="{INK}" stroke-width="2"/>'
)

CARDS = [
    ("A", "a", "apple", APPLE, "#ffe8e6", "#f9c6c1", "#e2443e"),
    ("B", "b", "ball", ball(), "#e3f0ff", "#bcd8f7", "#2f7fd0"),
    ("C", "c", "cat", CAT, "#fff3d6", "#f6dc9c", "#d98a0b"),
    ("D", "d", "dog", DOG, "#e6f6e6", "#c2e5c2", "#2f9a44"),
    ("E", "e", "elephant", ELEPHANT, "#efe8ff", "#d6c8fa", "#7550d2"),
    ("F", "f", "fish", FISH, "#dff6f3", "#b3e4dc", "#12978b"),
]

W, H, GAP = 184, 250, 24
X0 = [40, 248, 456]
Y0 = [20, 20 + H + GAP]


def card(i, spec):
    up, lo, word, art, bg, border, accent = spec
    x = X0[i % 3]
    y = Y0[i // 3]
    cx = x + W / 2
    s = []
    s.append(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="20" fill="{bg}" stroke="{border}" stroke-width="2"/>')
    s.append(f'<text class="k-f" x="{x + 18}" y="{y + 52}" font-size="40" fill="{accent}">{up}{lo}</text>')
    s.append(f'<g transform="translate({fmt(cx)} {y + 130})">{art}</g>')
    s.append(
        f'<text class="k-f" x="{fmt(cx)}" y="{y + 228}" font-size="26" fill="{INK}" text-anchor="middle">'
        f'<tspan fill="{accent}">{word[0]}</tspan>{word[1:]}</text>'
    )
    return "".join(s)


if __name__ == "__main__":
    body = "".join(card(i, c) for i, c in enumerate(CARDS))
    total_h = Y0[1] + H + 20
    svg = svg_wrap(
        total_h,
        "Alphabet flashcards A to F",
        "Six picture cards: A for apple, B for ball, C for cat, D for dog, E for elephant, F for fish.",
        body,
    )
    open("alphabet.svg", "w").write(svg)
    print(len(svg), "bytes")
