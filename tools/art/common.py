import math

INK = "#3f3345"
FONT = "var(--font-sans, -apple-system, 'Helvetica Neue', Arial, sans-serif)"


def style(extra=""):
    return (
        "<style>"
        f".k-o{{stroke:{INK};stroke-width:3;stroke-linejoin:round;stroke-linecap:round}}"
        f".k-f{{font-family:{FONT};font-weight:500}}"
        f"{extra}"
        "</style>"
    )


def fmt(v):
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    if s == "-0":
        s = "0"
    return s


def smooth_path(pts, closed=False, start_cmd=True):
    """Catmull-Rom through pts -> cubic bezier path string."""
    n = len(pts)
    out = []
    if start_cmd:
        out.append(f"M{fmt(pts[0][0])} {fmt(pts[0][1])}")
    rng = range(n if closed else n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(
            f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
        )
    if closed:
        out.append("Z")
    return "".join(out)


def svg_wrap(h, title, desc, body, extra_style=""):
    return (
        f'<svg width="100%" viewBox="0 0 680 {h}" xmlns="http://www.w3.org/2000/svg" role="img">'
        f"<title>{title}</title><desc>{desc}</desc>"
        f"{style(extra_style)}{body}</svg>"
    )
