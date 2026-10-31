"""Animated certificate cards + timeline for the profile README.

Usage: python scripts/gen_certs.py   (needs Pillow; run from the repo root)
Reads certificates/*.jpg, writes assets/certs/*.svg with the image embedded (SVGs in <img> can't load external files).
"""
import base64, html, io, os
from PIL import Image, ImageFilter

OUT = "assets/certs"
os.makedirs(OUT, exist_ok=True)
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
FG, SUB, CARD, LINE, BG = "#E6EDF3", "#8B949E", "#161B22", "#30363D", "#0D1117"
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

# slug, image, title, issuer, meta, category, accent, highlight
CERTS = [
    ("bsc", "bachelor-certificate.jpg", "B.Sc. Graduation Certificate", "Egyptian E-Learning University", "Bachelor's degree · 2025", "Degree", "#FBBF24", ""),
    ("route", "route-aspnet-core.jpg", "ASP.NET Core Back-End", "Route Academy", "Dec 2025 – Jul 2026 · Certificate of Achievement", "Diploma", "#36BCF7", ""),
    ("hcia", "huawei-hcia-ai.jpg", "HCIA-AI V3.5", "Huawei", "Huawei Talent Online · 2024", "Certification", "#F43F5E", "96%"),
    ("nti", "nti.jpg", "AI Talent Academy Track", "NTI × Huawei", "80 hours · Sep – Oct 2024", "Bootcamp", "#F59E0B", "96%"),
    ("python", "iti-python.jpg", "Full Stack Python", "ITI", "120 hours · Jul – Aug 2024", "Training", "#A78BFA", ""),
    ("oop", "mastering-oop.jpg", "Mastering OOP using C++", "ITI · Mahara-Tech", "Oct 2025", "Course", "#4ADE80", ""),
    ("cleancode", "clean-code.jpg", "Principles of Clean Code", "ITI · Mahara-Tech", "Oct 2025", "Course", "#2DD4BF", ""),
    ("db", "database.jpg", "Database Fundamentals", "ITI · Mahara-Tech", "Oct 2024", "Course", "#60A5FA", ""),
]


def b64(img, maxside, q):
    im = img.copy().convert("RGB")
    im.thumbnail((maxside, maxside), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


def esc(s):
    return html.escape(s, quote=True)


def card(i, slug, fn, title, issuer, meta, cat, acc, hi):
    src = Image.open(os.path.join("certificates", fn))
    img, (iw, ih) = b64(src, 820, 74)
    blur = src.copy().convert("RGB")
    blur.thumbnail((120, 120))
    blur = blur.filter(ImageFilter.GaussianBlur(6))
    bg, _ = b64(blur, 120, 60)

    W, H = 600, 450
    px, py, pw, ph = 16, 16, W - 32, 300
    pad = 16
    # contain-fit the certificate inside the panel
    s = min((pw - 2 * pad) / iw, (ph - 2 * pad) / ih)
    dw, dh = iw * s, ih * s
    dx, dy = px + (pw - dw) / 2, py + (ph - dh) / 2
    u = f"c{slug}"
    chip_w = 34 + len(issuer) * 7.0
    cat_w = 18 + len(cat) * 7.4
    score = ""
    if hi:
        score = f'''<g transform="translate({W-58} {py+ph-42})">
  <circle r="30" fill="{BG}" fill-opacity=".85" stroke="{acc}" stroke-opacity=".35" stroke-width="4"/>
  <circle class="ring" r="30" fill="none" stroke="{acc}" stroke-width="4" stroke-linecap="round" stroke-dasharray="181 188" transform="rotate(-90)"/>
  <text y="2" text-anchor="middle" font-size="15" font-weight="800" fill="{FG}">{hi}</text>
  <text y="16" text-anchor="middle" font-size="8.5" font-weight="600" letter-spacing="1" fill="{SUB}">SCORE</text>
</g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{esc(title)} — {esc(issuer)}</title>
<style>
  text{{font-family:{FONT}}}
  .edge{{stroke-dasharray:14 86;animation:edge 7s linear infinite;animation-delay:-{i*0.9:.1f}s}}
  .shine{{animation:shine 5s ease-in-out infinite;animation-delay:{i*0.6:.1f}s}}
  .float{{animation:float 6s ease-in-out infinite;animation-delay:-{i*0.7:.1f}s}}
  .chk{{stroke-dasharray:14;animation:chk 3.2s ease-in-out infinite}}
  .dot{{transform-box:fill-box;transform-origin:center;animation:dot 2s ease-out infinite}}
  .arr{{animation:arr 1.6s ease-in-out infinite}}
  .ring{{animation:ring 4s ease-in-out infinite}}
  @keyframes in{{from{{transform:translateY(14px)}}to{{transform:none}}}}
  @keyframes edge{{to{{stroke-dashoffset:-100}}}}
  @keyframes shine{{0%{{transform:translateX(-260px)}}45%,100%{{transform:translateX({W+260}px)}}}}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
  @keyframes chk{{0%,55%,100%{{stroke-dashoffset:0}}70%{{stroke-dashoffset:14}}85%{{stroke-dashoffset:0}}}}
  @keyframes dot{{0%{{opacity:.8;transform:scale(1)}}100%{{opacity:0;transform:scale(2.6)}}}}
  @keyframes arr{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(5px)}}}}
  @keyframes ring{{0%,100%{{stroke-dashoffset:0}}50%{{stroke-dashoffset:-20}}}}
  {RM}
</style>
<defs>
  <linearGradient id="{u}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{acc}"/><stop offset="1" stop-color="#36BCF7"/></linearGradient>
  <linearGradient id="{u}s" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".28"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
  <linearGradient id="{u}fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".35"/><stop offset="1" stop-color="{BG}" stop-opacity=".75"/></linearGradient>
  <clipPath id="{u}p"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath>
  <filter id="{u}sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#000" flood-opacity=".55"/></filter>
</defs>
<g class="card">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{CARD}" stroke="{LINE}"/>
<rect class="edge" x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="url(#{u}g)" stroke-width="2" pathLength="100"/>
<g clip-path="url(#{u}p)">
  <image xlink:href="{bg}" x="{px-20}" y="{py-20}" width="{pw+40}" height="{ph+40}" preserveAspectRatio="xMidYMid slice"/>
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#{u}fade)"/>
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="{acc}" fill-opacity=".06"/>
  <g class="float"><image filter="url(#{u}sh)" xlink:href="{img}" x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh:.1f}" preserveAspectRatio="xMidYMid meet"/></g>
  <g transform="skewX(-18)"><rect class="shine" x="-200" y="{py}" width="160" height="{ph}" fill="url(#{u}s)"/></g>
</g>
<g transform="translate({px+12} {py+12})">
  <rect width="{chip_w:.0f}" height="26" rx="13" fill="{BG}" fill-opacity=".82" stroke="{acc}" stroke-opacity=".6"/>
  <circle cx="13" cy="13" r="4" fill="{acc}"/><circle class="dot" cx="13" cy="13" r="4" fill="{acc}"/>
  <text x="24" y="17.5" font-size="12" font-weight="600" fill="{FG}">{esc(issuer)}</text>
</g>
<g transform="translate({px+pw-12-cat_w:.0f} {py+12})">
  <rect width="{cat_w:.0f}" height="26" rx="13" fill="{acc}"/>
  <text x="{cat_w/2:.0f}" y="17.5" text-anchor="middle" font-size="12" font-weight="700" fill="{BG}">{esc(cat)}</text>
</g>
{score}
<rect x="24" y="334" width="4" height="22" rx="2" fill="{acc}"/>
<text x="38" y="352" font-size="22" font-weight="700" fill="{FG}">{esc(title)}</text>
<text x="38" y="378" font-size="14" fill="{SUB}">{esc(meta)}</text>
<line x1="24" x2="{W-24}" y1="398" y2="398" stroke="{LINE}"/>
<g transform="translate(24 410)">
  <rect width="92" height="26" rx="13" fill="#4ADE80" fill-opacity=".12" stroke="#4ADE80" stroke-opacity=".5"/>
  <path class="chk" d="M12 13.5l4 4 8-8.5" fill="none" stroke="#4ADE80" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="32" y="17.5" font-size="12" font-weight="700" fill="#4ADE80">Verified</text>
</g>
<g transform="translate({W-24} 428)"><text text-anchor="end" font-size="13" font-weight="600" fill="{acc}">View certificate <tspan class="arr">→</tspan></text></g>
</g>
</svg>
'''


def timeline():
    # chronological
    ev = [("Jul 2024", "Full Stack Python", "ITI", "#A78BFA"), ("Oct 2024", "AI Talent Track", "NTI × Huawei", "#F59E0B"),
          ("2024", "HCIA-AI V3.5", "Huawei", "#F43F5E"), ("Oct 2024", "Database", "Mahara-Tech", "#60A5FA"),
          ("2025", "B.Sc. Degree", "EELU", "#FBBF24"), ("Oct 2025", "OOP in C++", "Mahara-Tech", "#4ADE80"),
          ("Oct 2025", "Clean Code", "Mahara-Tech", "#2DD4BF"), ("Jul 2026", "ASP.NET Core", "Route", "#36BCF7")]
    W, H = 1200, 250
    x0, x1, y = 115, W - 115, 142
    step = (x1 - x0) / (len(ev) - 1)
    g = ""
    for i, (d, t, org, c) in enumerate(ev):
        x = x0 + i * step
        up = i % 2 == 0
        ty = y - 52 if up else y + 50
        g += f'''<g class="ev" style="animation-delay:{0.3+i*0.18:.2f}s">
<line x1="{x:.1f}" x2="{x:.1f}" y1="{y}" y2="{y-22 if up else y+22}" stroke="{c}" stroke-opacity=".5"/>
<circle class="pulse" style="animation-delay:{i*0.45:.2f}s" cx="{x:.1f}" cy="{y}" r="9" fill="none" stroke="{c}"/>
<circle cx="{x:.1f}" cy="{y}" r="9" fill="{BG}" stroke="{c}" stroke-width="3"/><circle cx="{x:.1f}" cy="{y}" r="3.5" fill="{c}"/>
<text x="{x:.1f}" y="{ty-18 if up else ty}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1" fill="{c}">{esc(d.upper())}</text>
<text x="{x:.1f}" y="{ty if up else ty+18}" text-anchor="middle" font-size="14" font-weight="700" fill="{FG}">{esc(t)}</text>
<text x="{x:.1f}" y="{ty+16 if up else ty+34}" text-anchor="middle" font-size="11.5" fill="{SUB}">{esc(org)}</text>
</g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text{{font-family:{FONT}}}
  .ev{{animation:in .8s cubic-bezier(.2,.7,.2,1) both}}
  .flow{{stroke-dasharray:6 8;animation:flow 1.4s linear infinite}}
  .pulse{{transform-box:fill-box;transform-origin:center;animation:p 3.6s ease-out infinite}}
  .edge{{stroke-dasharray:12 88;animation:edge 9s linear infinite}}
  @keyframes in{{from{{transform:translateY(10px)}}to{{transform:none}}}}
  @keyframes flow{{to{{stroke-dashoffset:-28}}}}
  @keyframes p{{0%{{opacity:.9;transform:scale(1)}}40%,100%{{opacity:0;transform:scale(2.6)}}}}
  @keyframes edge{{to{{stroke-dashoffset:-100}}}}
  {RM}
</style>
<defs>
  <linearGradient id="tlg" x1="0" x2="1"><stop offset="0" stop-color="#A78BFA"/><stop offset=".5" stop-color="#F59E0B"/><stop offset="1" stop-color="#36BCF7"/></linearGradient>
  <linearGradient id="tlbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0B1B2B"/></linearGradient>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#tlbg)" stroke="{LINE}"/>
<rect class="edge" x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="none" stroke="url(#tlg)" stroke-width="2" pathLength="100"/>
<text x="28" y="34" font-size="13" font-weight="700" letter-spacing="2" fill="{SUB}">LEARNING JOURNEY · 8 CERTIFICATES · 2024 → 2026</text>
<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>
<line class="flow" x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="url(#tlg)" stroke-width="2.5"/>
{g}
<circle r="6" fill="#FFFFFF"><animateMotion dur="8s" repeatCount="indefinite" path="M{x0} {y} H{x1}"/></circle>
<circle r="14" fill="#36BCF7" fill-opacity=".25"><animateMotion dur="8s" repeatCount="indefinite" path="M{x0} {y} H{x1}"/></circle>
</svg>
'''


for i, c in enumerate(CERTS):
    with open(os.path.join(OUT, f"{c[0]}.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(card(i, *c))
with open(os.path.join(OUT, "timeline.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(timeline())
for n in sorted(os.listdir(OUT)):
    print(n, os.path.getsize(os.path.join(OUT, n)) // 1024, "KB")
