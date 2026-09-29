import sys, re, subprocess, os, pathlib
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def render(svg_path, out_png, bg="#ffffff", scale=2):
    svg = pathlib.Path(svg_path).read_text()
    h = float(re.search(r'viewBox="0 0 680 ([\d.]+)"', svg).group(1))
    html = f"""<html><head><style>:root{{--font-sans:-apple-system,'Helvetica Neue',Arial,sans-serif}}
body{{margin:0;background:{bg}}}.wrap{{width:680px}}</style></head><body><div class="wrap">{svg}</div></body></html>"""
    hp = pathlib.Path(out_png).with_suffix(".html")
    hp.write_text(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--force-device-scale-factor={scale}", f"--window-size=680,{int(h)}",
        f"--screenshot={os.path.abspath(out_png)}", f"file://{os.path.abspath(hp)}"],
        capture_output=True)
    print("rendered", out_png, "h=", h)
if __name__ == "__main__":
    svg = sys.argv[1]; out = sys.argv[2]
    bg = sys.argv[3] if len(sys.argv) > 3 else "#ffffff"
    render(svg, out, bg)
