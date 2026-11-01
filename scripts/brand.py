"""Brand tokens shared by every SVG generator in this repo.

Palette : purple #804199 + cyan #20AACF (plus lighter tints for text on dark backgrounds)
Type    : Syne (display / UI, weights 400-800) and Syne Mono (code), SIL Open Font License
          (scripts/fonts/OFL.txt).

GitHub embeds README SVGs through <img>, which cannot fetch web fonts, so a Latin subset of
each face is inlined as a base64 data URI. Rebuild a subset with
  https://fonts.googleapis.com/css2?family=Syne:wght@400..800&text=<url-encoded chars>
  https://fonts.googleapis.com/css2?family=Syne+Mono&text=<url-encoded chars>
(send a desktop Chrome User-Agent so Google returns woff2).
Stdlib only: gen_stats.py imports this on a bare GitHub Actions runner.
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PURPLE = "#804199"
CYAN = "#20AACF"
PURPLE_SOFT = "#B57FCB"   # purple tint readable on dark backgrounds
CYAN_SOFT = "#7FD3EA"

FONT = "Syne, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Syne Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Weight scale used across the artwork
W_DISPLAY = 800   # name, headline numbers, card titles
W_BOLD = 700      # sub-titles
W_SEMI = 600      # eyebrows (uppercase, tracked), chips, labels
W_MEDIUM = 500    # taglines
W_BODY = 400      # body copy


def _b64(name):
    with open(os.path.join(HERE, "fonts", name), "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


FONT_FACE = ("@font-face{font-family:'Syne';font-style:normal;font-weight:400 800;"
             f"src:url(data:font/woff2;base64,{_b64('syne-subset.woff2')}) format('woff2')}}")
MONO_FACE = ("@font-face{font-family:'Syne Mono';font-style:normal;font-weight:400;"
             f"src:url(data:font/woff2;base64,{_b64('syne-mono-subset.woff2')}) format('woff2')}}")

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

THEMES = {
    "dark": dict(bg1="#0C0A18", bg2="#1A1233", card="#15112A", card2="#1C1736", line="#2E2650",
                 grid="#FFFFFF", grid_op=".045", title="#FFFFFF", text="#E2DCEF", muted="#A79CC0",
                 accent=CYAN, accent2=PURPLE_SOFT, ok="#4ADE80"),
    "light": dict(bg1="#FBF9FD", bg2="#EEE6F5", card="#FFFFFF", card2="#F7F2FA", line="#E2D6EC",
                  grid="#1B1030", grid_op=".05", title="#1B1030", text="#2F2545", muted="#5D536F",
                  accent=PURPLE, accent2="#1688A8", ok="#15803D"),
}


def brand_gradient(gid, x1="0", y1="0", x2="1", y2="0", op1="1", op2="1"):
    """Purple-to-cyan linear gradient definition."""
    return (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{PURPLE}" stop-opacity="{op1}"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity="{op2}"/></linearGradient>')
