"""Design tokens shared by every SVG generator in this repo.

Palette : the profile's original colours, cyan #36BCF7 + violet #A78BFA on GitHub-dark surfaces
          (with deeper equivalents for the light theme so text keeps its contrast).
Type    : Syne (display / UI, weights 400-800) and Syne Mono (code), SIL Open Font License
          (scripts/fonts/OFL.txt).

GitHub embeds README SVGs through <img>, which cannot fetch web fonts, so a Latin subset of
each face is inlined as a base64 data URI. Rebuild a subset with
  https://fonts.googleapis.com/css2?family=Syne:wght@400..800&text=<url-encoded chars>
  https://fonts.googleapis.com/css2?family=Syne+Mono&text=<url-encoded chars>
(send a desktop Chrome User-Agent so Google returns woff2).

Font sizes: a 1280-wide README image is shown about 850px wide on GitHub (scale ~0.66), so
artwork sizes are chosen to land at >= 12px rendered for labels and >= 13px for body text.
Stdlib only: gen_stats.py imports this on a bare GitHub Actions runner.
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

CYAN = "#36BCF7"      # primary accent (original profile colour)
VIOLET = "#A78BFA"    # secondary accent
GREEN = "#4ADE80"

FONT = "Syne, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Syne Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def _b64(name):
    with open(os.path.join(HERE, "fonts", name), "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


FONT_FACE = ("@font-face{font-family:'Syne';font-style:normal;font-weight:400 800;"
             f"src:url(data:font/woff2;base64,{_b64('syne-subset.woff2')}) format('woff2')}}")
MONO_FACE = ("@font-face{font-family:'Syne Mono';font-style:normal;font-weight:400;"
             f"src:url(data:font/woff2;base64,{_b64('syne-mono-subset.woff2')}) format('woff2')}}")

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

THEMES = {
    "dark": dict(bg1="#0D1117", bg2="#0B1B2B", card="#161B22", card2="#1C2330", line="#30363D",
                 grid="#FFFFFF", grid_op=".04", title="#FFFFFF", text="#E6EDF3", muted="#8B949E",
                 c1=CYAN, c2=VIOLET, ok=GREEN, str="#A5D6FF", glow=".30"),
    "light": dict(bg1="#FFFFFF", bg2="#EAF6FD", card="#FFFFFF", card2="#F6F8FA", line="#D0D7DE",
                  grid="#1F2328", grid_op=".05", title="#1F2328", text="#24292F", muted="#57606A",
                  c1="#0A85C2", c2="#7C3AED", ok="#1A7F37", str="#0A3069", glow=".16"),
}


def grad(gid, t, x1="0", y1="0", x2="1", y2="0"):
    """Cyan-to-violet linear gradient definition for theme t."""
    return (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{t["c1"]}"/><stop offset="1" stop-color="{t["c2"]}"/></linearGradient>')


# Light type scale: the artwork is drawn with semantic weights (800 display, 700 titles, 600 labels,
# 500 taglines) and thin() maps them onto Syne's lighter end, so the whole profile reads thin.
THIN = {"800": "500", "700": "500", "600": "400", "500": "400"}


def thin(svg_text):
    """Lighten every font-weight in an SVG string (attributes and inline CSS)."""
    svg_text = re.sub(r'font-weight="(\d+)"', lambda m: f'font-weight="{THIN.get(m.group(1), m.group(1))}"', svg_text)
    return re.sub(r'font-weight:(\d+)', lambda m: f'font-weight:{THIN.get(m.group(1), m.group(1))}', svg_text)
