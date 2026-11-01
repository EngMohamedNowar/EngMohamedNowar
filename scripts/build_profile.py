"""Generate the branded SVG artwork used by README.md.

Run from the repo root:   python scripts/build_profile.py
Writes light + dark variants into assets/ (banner, about, stats, architecture, footer,
trust badges) plus a theme-neutral divider.

Rules kept by every generator here:
- Text is static. Animation only moves decoration, and every keyframe loop starts in the
  resting look, so a frozen timeline or prefers-reduced-motion still shows everything.
- Syne / Syne Mono are inlined (see brand.py) because <img> SVGs cannot load web fonts.
"""
import os
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from brand import (CYAN, CYAN_SOFT, FONT, FONT_FACE, MONO, MONO_FACE, PURPLE, PURPLE_SOFT,  # noqa: E402
                   REDUCED, THEMES, brand_gradient)

ASSETS = os.path.join(ROOT, "assets")
CHAR_W = 9.67  # Syne Mono advance at 17px; measured with getBBox in the browser
TRUST_OUT = os.path.join(ASSETS, "trust")
os.makedirs(TRUST_OUT, exist_ok=True)


def e(s):
    return escape(s, quote=True)


def write(path, s):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)


def svg(w, h, body, css="", defs="", mono=False, title=""):
    faces = FONT_FACE + ("\n" + MONO_FACE if mono else "")
    t = f"<title>{e(title)}</title>\n" if title else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">
{t}<style>
{faces}
.mono{{font-family:{MONO}}}
{css}
{REDUCED}
</style>
<defs>
{brand_gradient("brand")}
{brand_gradient("brandd", x2="1", y2="1")}
<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
{defs}
</defs>
{body}
</svg>
'''


def backdrop(w, h, t, rx=22, glow=True):
    """Rounded panel with brand gradient background, grid and soft glows."""
    dark = t is THEMES["dark"]
    out = [f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
           f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}"/></pattern>',
           f'<radialGradient id="gp" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{PURPLE}" stop-opacity="{.45 if dark else .18}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>',
           f'<radialGradient id="gc" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity="{.30 if dark else .16}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
           f'<clipPath id="panel"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}"/></clipPath>']
    body = [f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="url(#bg)"/>',
            f'<g clip-path="url(#panel)"><rect width="{w}" height="{h}" fill="url(#grid)"/>']
    if glow:
        body += [f'<ellipse class="gl1" cx="{w * .12:.0f}" cy="{h * .1:.0f}" rx="{w * .32:.0f}" ry="{h * .9:.0f}" fill="url(#gp)"/>',
                 f'<ellipse class="gl2" cx="{w * .9:.0f}" cy="{h * .85:.0f}" rx="{w * .3:.0f}" ry="{h * .9:.0f}" fill="url(#gc)"/>']
    body.append("</g>")
    body.append(f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="{rx - .5}" fill="none" stroke="url(#brandd)" stroke-opacity=".55"/>')
    return "\n".join(out), "\n".join(body)


GLOW_CSS = """
.gl1{animation:drift 14s ease-in-out infinite}
.gl2{animation:drift 18s ease-in-out infinite reverse}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,14px)}}"""


# --------------------------------------------------------------------------- banner
LAYERS = [("API", "Controllers · JWT"), ("Application", "CQRS · MediatR"),
          ("Domain", "Entities · Rules"), ("Infrastructure", "EF Core · Redis")]
CHIPS = ["Cairo, Egypt", "Open to remote & freelance", "583 automated tests"]


def banner(mode):
    t = THEMES[mode]
    dark = mode == "dark"
    W, H = 1280, 380
    defs, back = backdrop(W, H, t)
    css = GLOW_CSS + f"""
.flow{{stroke-dasharray:5 7;animation:flow 1.1s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-24}}}}
.ly{{animation:ly 4.8s ease-in-out infinite}}
@keyframes ly{{0%,30%,100%{{stroke-opacity:.35}}12%{{stroke-opacity:1}}}}
.dot{{animation:dot 4.8s ease-in-out infinite}}
@keyframes dot{{0%,30%,100%{{fill:{t["card"]}}}12%{{fill:{CYAN}}}}}
.ok{{animation:ok 2.4s ease-in-out infinite}}
@keyframes ok{{0%,100%{{fill-opacity:.16}}50%{{fill-opacity:.32}}}}
.caret{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
.sw{{animation:sw 9s ease-in-out infinite}}
@keyframes sw{{0%{{transform:translateX(-300px)}}50%,100%{{transform:translateX(1500px)}}}}"""
    b = [back]
    # ---- left column: identity
    b += [f'<text x="80" y="70" font-size="14" font-weight="600" letter-spacing="4" fill="{t["accent"] if not dark else CYAN}">SOFTWARE ENGINEER  ·  J. SERVO LLC</text>',
          f'<rect x="80" y="84" width="56" height="3" rx="1.5" fill="url(#brand)"/>',
          f'<text x="75" y="148" font-size="64" font-weight="800" letter-spacing="-1" fill="{t["title"]}">Mohamed</text>',
          f'<text x="75" y="206" font-size="64" font-weight="800" letter-spacing="-1" fill="url(#brandName)">Nowar<tspan fill="{CYAN}">.</tspan></text>',
          f'<text x="80" y="248" font-size="24" font-weight="500" fill="{t["text"]}">.NET backend engineer building secure, tested APIs</text>',
          f'<text x="80" y="278" font-size="15" font-weight="400" fill="{t["muted"]}">ASP.NET Core · C# · EF Core · SQL Server · Clean Architecture · CQRS</text>']
    x = 80
    for k, c in enumerate(CHIPS):
        w = round(len(c) * 8.4 + 44)
        col = CYAN if k % 2 else (PURPLE_SOFT if dark else PURPLE)
        b.append(f'<g><rect x="{x}" y="298" width="{w}" height="34" rx="17" fill="{col}" fill-opacity="{.14 if dark else .08}" stroke="{col}" stroke-opacity=".55"/>'
                 f'<circle cx="{x + 18}" cy="315" r="4" fill="{col}"/>'
                 f'<text x="{x + 30}" y="320" font-size="14" font-weight="600" fill="{t["text"]}">{e(c)}</text></g>')
        x += w + 12
    # ---- right column: request travelling through the layers
    rx0 = 850
    b += [f'<rect x="{rx0}" y="44" width="380" height="54" rx="14" fill="{t["card"]}" stroke="url(#brandd)" stroke-opacity=".8"/>',
          f'<text class="mono" x="{rx0 + 20}" y="77" font-size="16" fill="{t["muted"]}"><tspan fill="{CYAN if dark else PURPLE}">GET</tspan> <tspan fill="{t["title"]}">/api/orders/42</tspan></text>',
          f'<rect class="caret" x="{rx0 + 186}" y="62" width="9" height="20" rx="1" fill="{CYAN}"/>',
          f'<rect class="ok" x="{rx0 + 262}" y="58" width="100" height="26" rx="13" fill="{t["ok"]}" fill-opacity=".16" stroke="{t["ok"]}" stroke-opacity=".6"/>',
          f'<text class="mono" x="{rx0 + 312}" y="76" font-size="14" text-anchor="middle" fill="{t["ok"]}">200 OK</text>']
    lx = rx0 + 20       # connector x
    b.append(f'<line x1="{lx}" y1="98" x2="{lx}" y2="330" stroke="{t["line"]}" stroke-width="2"/>')
    b.append(f'<line class="flow" x1="{lx}" y1="98" x2="{lx}" y2="330" stroke="url(#brandV)" stroke-width="2"/>')
    for k, (name, sub) in enumerate(LAYERS):
        y = 118 + k * 50
        d = f"animation-delay:{k * .6:.1f}s"
        b += [f'<rect x="{lx + 26}" y="{y}" width="334" height="38" rx="12" fill="{t["card"]}" fill-opacity=".92"/>',
              f'<rect class="ly" style="{d}" x="{lx + 26.5}" y="{y + .5}" width="333" height="37" rx="11.5" fill="none" stroke="{CYAN if k % 2 else (PURPLE_SOFT if dark else PURPLE)}" stroke-opacity=".35" stroke-width="1.4"/>',
              f'<circle cx="{lx}" cy="{y + 19}" r="6" fill="{t["card"]}" stroke="{CYAN}" stroke-width="2"/>',
              f'<circle class="dot" style="{d}" cx="{lx}" cy="{y + 19}" r="3" fill="{t["card"]}"/>',
              f'<text x="{lx + 44}" y="{y + 25}" font-size="16" font-weight="700" fill="{t["title"]}">{e(name)}</text>',
              f'<text class="mono" x="{lx + 344}" y="{y + 24}" font-size="13" text-anchor="end" fill="{t["muted"]}">{e(sub)}</text>']
    # database
    dy = 318
    b += [f'<g transform="translate({lx + 26} {dy})">'
          f'<path d="M0 6 v20 c0 4 14 8 30 8 s30 -4 30 -8 v-20" fill="{t["card"]}" stroke="{CYAN}" stroke-width="1.6"/>'
          f'<ellipse cx="30" cy="6" rx="30" ry="7" fill="{t["card2"]}" stroke="{CYAN}" stroke-width="1.6"/>'
          f'<text x="76" y="25" font-size="15" font-weight="700" fill="{t["title"]}">SQL Server</text>'
          f'<text class="mono" x="174" y="24" font-size="13" fill="{t["muted"]}">+ Redis cache</text></g>']
    # packets: request travels down (cyan), response travels up (purple)
    b += [f'<circle r="5" fill="{CYAN}"><animateMotion dur="4.8s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.45;1" calcMode="linear" path="M{lx} 98 V330"/></circle>',
          f'<circle r="5" fill="{PURPLE_SOFT if dark else PURPLE}"><animateMotion dur="4.8s" repeatCount="indefinite" keyPoints="1;1;0;0" keyTimes="0;.5;.95;1" calcMode="linear" path="M{lx} 98 V330"/></circle>',
          f'<g clip-path="url(#panel)"><g transform="skewX(-18)"><rect class="sw" x="0" y="0" width="200" height="{H}" fill="url(#sheen)"/></g></g>']
    defs += (f'\n<linearGradient id="brandName" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE if not dark else PURPLE_SOFT}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
             f'\n<linearGradient id="brandV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>')
    return svg(W, H, "\n".join(b), css, defs, mono=True,
               title="Mohamed Nowar — Software Engineer at J. Servo LLC, .NET backend engineer")


# --------------------------------------------------------------------------- divider (theme neutral)
def divider():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="14" viewBox="0 0 1200 14" preserveAspectRatio="none">
<defs><linearGradient id="dv" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/><stop offset=".35" stop-color="{PURPLE}"/><stop offset=".65" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="base" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".05"/><stop offset=".5" stop-color="{PURPLE}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".05"/></linearGradient></defs>
<style>.m{{animation:mv 5s cubic-bezier(.45,0,.55,1) infinite}}@keyframes mv{{0%{{transform:translateX(-420px)}}100%{{transform:translateX(1200px)}}}}{REDUCED}</style>
<rect y="6.5" width="1200" height="1" fill="url(#base)"/>
<rect class="m" y="6" width="420" height="2" rx="1" fill="url(#dv)"/>
<circle cx="600" cy="7" r="3.5" fill="{PURPLE}"/><circle cx="614" cy="7" r="2.5" fill="{CYAN}"/><circle cx="586" cy="7" r="2.5" fill="{CYAN}"/>
</svg>
'''


# --------------------------------------------------------------------------- about (code card)
def about(mode):
    t = THEMES[mode]
    dark = mode == "dark"
    kw = PURPLE_SOFT if dark else PURPLE
    ty = CYAN if dark else "#1688A8"
    st = "#E9C46A" if dark else "#9A6A00"
    pu = t["muted"]
    K = lambda s: (s, kw)          # noqa: E731
    T = lambda s: (s, ty)          # noqa: E731
    S = lambda s: (f'"{s}"', st)   # noqa: E731
    P = lambda s: (s, pu)          # noqa: E731
    X = lambda s: (s, t["text"])   # noqa: E731

    def arr(*items):
        out = [P("[")]
        for i, it in enumerate(items):
            out.append(S(it))
            if i < len(items) - 1:
                out.append(P(", "))
        out.append(P("]"))
        return out

    def prop(name, pad, *val):
        return [X("    " + name + " " * (pad - len(name))), P("= ")] + list(val) + [P(",")]

    lines = [
        [K("using "), T("Nowar"), P("."), T("Engineering"), P(";")],
        [],
        [K("var "), X("engineer "), P("= "), K("new "), T("SoftwareEngineer")],
        [P("{")],
        prop("Name", 9, S("Mohamed Nowar")),
        prop("Role", 9, S("Software Engineer @ J. Servo LLC")),
        prop("Focus", 9, S(".NET backend · REST APIs")),
        prop("Stack", 9, *arr("C#", "ASP.NET Core", "EF Core", "SQL Server")),
        prop("Patterns", 9, *arr("Clean Architecture", "CQRS", "UoW")),
        prop("Testing", 9, *arr("xUnit", "NSubstitute", "Coverlet")),
        prop("Learning", 9, *arr("Microservices", "RabbitMQ", "CI/CD")),
        prop("Location", 9, S("Cairo, Egypt")),
        prop("OpenTo", 9, *arr("Remote", "Hybrid", "Freelance")),
        [P("};")],
        [("// Build succeeded · 0 warnings · 0 errors ✔", t["ok"])],
    ]
    W, LH, top = 1180, 27, 92
    H = top + len(lines) * LH + 34
    defs, back = backdrop(W, H, t, rx=20, glow=True)
    css = GLOW_CSS + """
.caret{animation:blink 1.1s steps(1) infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
.hl{animation:hl 9s ease-in-out infinite}
@keyframes hl{0%{transform:translateY(0)}100%{transform:translateY(SPANpx)}}""".replace("SPAN", str((len(lines) - 1) * LH))
    b = [back,
         f'<rect x="1" y="1" width="{W - 2}" height="52" rx="20" fill="{t["card"]}" fill-opacity=".85"/>',
         f'<rect x="1" y="34" width="{W - 2}" height="19" fill="{t["card"]}" fill-opacity=".85"/>',
         f'<line x1="1" y1="53" x2="{W - 1}" y2="53" stroke="{t["line"]}"/>',
         f'<circle cx="30" cy="27" r="6.5" fill="{PURPLE}"/><circle cx="52" cy="27" r="6.5" fill="{CYAN}"/><circle cx="74" cy="27" r="6.5" fill="{t["muted"]}" fill-opacity=".5"/>',
         f'<text x="{W / 2:.0f}" y="32" font-size="14" font-weight="600" letter-spacing="1" text-anchor="middle" fill="{t["muted"]}">Engineer.cs  —  dotnet run</text>',
         f'<text x="{W - 28}" y="32" font-size="12" font-weight="700" letter-spacing="2" text-anchor="end" fill="{CYAN}">C# · .NET</text>',
         f'<rect class="hl" x="2" y="{top - 19}" width="{W - 4}" height="{LH}" fill="{PURPLE}" fill-opacity="{.10 if dark else .06}"/>']
    for i, segs in enumerate(lines):
        y = top + i * LH
        b.append(f'<text class="mono" x="46" y="{y}" font-size="14" text-anchor="end" fill="{t["muted"]}" fill-opacity=".55">{i + 1}</text>')
        if segs:
            spans = "".join(f'<tspan fill="{c}">{e(s)}</tspan>' for s, c in segs)
            b.append(f'<text class="mono" x="70" y="{y}" font-size="17" xml:space="preserve">{spans}</text>')
    # right column: what I'm doing now
    px = 720
    b += [f'<line x1="{px - 30}" y1="76" x2="{px - 30}" y2="{H - 30}" stroke="{t["line"]}"/>',
          f'<text x="{px}" y="{top}" font-size="12" font-weight="600" letter-spacing="3" fill="{t["muted"]}">RIGHT NOW</text>',
          f'<line x1="{px + 7}" y1="{top + 34}" x2="{px + 7}" y2="{top + 34 + 3 * 82}" stroke="url(#brandV)" stroke-width="2"/>']
    for k, (tag, head, sub) in enumerate(NOW):
        y = top + 40 + k * 82
        col = CYAN if k % 2 else kw
        b += [f'<circle cx="{px + 7}" cy="{y - 6}" r="7" fill="{t["card"]}" stroke="{col}" stroke-width="2.5"/>',
              f'<text x="{px + 28}" y="{y - 1}" font-size="11" font-weight="700" letter-spacing="2.4" fill="{col}">{e(tag)}</text>',
              f'<text x="{px + 28}" y="{y + 22}" font-size="16" font-weight="800" fill="{t["title"]}">{e(head)}</text>',
              f'<text x="{px + 28}" y="{y + 42}" font-size="12.5" fill="{t["muted"]}">{e(sub)}</text>']
    defs += f'\n<linearGradient id="brandV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
    last = top + (len(lines) - 1) * LH
    chars = sum(len(s) for s, _ in lines[-1])
    b.append(f'<rect class="caret" x="{70 + chars * CHAR_W + 6:.0f}" y="{last - 16}" width="10" height="21" fill="{CYAN}"/>')
    return svg(W, H, "\n".join(b), css, defs, mono=True,
               title="Mohamed Nowar: Software Engineer at J. Servo LLC, .NET backend, Cairo, Egypt")


NOW = [("NOW", "Software Engineer", "J. Servo LLC · since Jun 2026"),
       ("LEARNING", "Backend Advanced Bootcamp", "Elevate · .NET track"),
       ("BUILDING", "Accounting Platform MVP", "ASP.NET Core · React · EF Core"),
       ("EXPLORING", "Microservices & messaging", "RabbitMQ · Azure Service Bus")]


# --------------------------------------------------------------------------- stats strip
STATS = [("7", "Shipped projects", "API · MVC · WPF · REACT"),
         ("583", "Automated tests", "XUNIT · NSUBSTITUTE"),
         ("8", "Certifications", "ROUTE · ITI · HUAWEI"),
         ("96%", "HCIA-AI score", "HUAWEI · 2024")]


def stats(mode):
    t = THEMES[mode]
    dark = mode == "dark"
    W, H, gap = 1280, 168, 20
    cw = (W - gap * 3) / 4
    css = """
.bar{animation:bar 6s ease-in-out infinite;transform-box:fill-box;transform-origin:left}
@keyframes bar{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.55)}}
.sw{animation:sw 8s ease-in-out infinite}
@keyframes sw{0%{transform:translateX(-200px)}45%,100%{transform:translateX(560px)}}"""
    b, defs = [], []
    for i, (num, label, sub) in enumerate(STATS):
        x = i * (cw + gap)
        d = f"animation-delay:{i * .7:.1f}s"
        defs.append(f'<clipPath id="c{i}"><rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18"/></clipPath>')
        b += [f'<rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="{t["card"]}"/>',
              f'<rect x="{x + 1.5:.1f}" y="1.5" width="{cw - 3:.1f}" height="{H - 3}" rx="17.5" fill="none" stroke="url(#brandd)" stroke-opacity=".5"/>',
              f'<text x="{x + 28:.1f}" y="78" font-size="54" font-weight="800" letter-spacing="-1" fill="url(#num)">{e(num)}</text>',
              f'<text x="{x + 28:.1f}" y="108" font-size="17" font-weight="700" fill="{t["title"]}">{e(label)}</text>',
              f'<text x="{x + 28:.1f}" y="132" font-size="11.5" font-weight="600" letter-spacing="2" fill="{t["muted"]}">{e(sub)}</text>',
              f'<rect x="{x + 28:.1f}" y="146" width="{cw - 56:.1f}" height="4" rx="2" fill="{t["line"]}"/>',
              f'<rect class="bar" style="{d}" x="{x + 28:.1f}" y="146" width="{cw - 56:.1f}" height="4" rx="2" fill="url(#brand)"/>',
              f'<g clip-path="url(#c{i})"><g transform="translate({x:.1f} 0)"><rect class="sw" style="{d}" x="0" y="0" width="120" height="{H}" fill="url(#sheen)"/></g></g>']
    defs.append(f'<linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE_SOFT if dark else PURPLE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>')
    return svg(W, H, "\n".join(b), css, "\n".join(defs),
               title="7 shipped projects · 583 automated tests · 8 certifications · 96% HCIA-AI score")


# --------------------------------------------------------------------------- architecture
CORE = [("01", "Clients", "Web · Mobile · Swagger · Postman"),
        ("02", "API layer", "Controllers · Middleware · JWT auth · Rate limiting"),
        ("03", "Application layer", "CQRS · MediatR · DTOs · Validation · AutoMapper"),
        ("04", "Domain layer", "Entities · Specifications · Business rules")]
STORES = [("SQL Server", "Relational data"), ("Redis", "Caching · Baskets"), ("Azure", "Cloud hosting")]


def architecture(mode):
    t = THEMES[mode]
    dark = mode == "dark"
    W, H = 1280, 560
    defs, back = backdrop(W, H, t)
    css = GLOW_CSS + """
.flow{stroke-dasharray:5 7;animation:flow 1.1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-24}}
.ly{animation:ly 6s ease-in-out infinite}
@keyframes ly{0%,24%,100%{stroke-opacity:.4}10%{stroke-opacity:1}}"""
    soft = PURPLE_SOFT if dark else PURPLE
    b = [back,
         f'<text x="60" y="62" font-size="13" font-weight="600" letter-spacing="3.5" fill="{t["muted"]}">CLEAN ARCHITECTURE  ·  REQUEST FLOW</text>',
         f'<text x="60" y="96" font-size="28" font-weight="800" fill="{t["title"]}">How my APIs are <tspan fill="url(#brand)">layered</tspan></text>']
    cx, cw, bh = 60, 660, 78
    ys = [130 + i * 102 for i in range(4)]
    # connectors
    for i in range(3):
        y1, y2 = ys[i] + bh, ys[i + 1]
        b += [f'<line x1="{cx + cw / 2}" y1="{y1}" x2="{cx + cw / 2}" y2="{y2}" stroke="{t["line"]}" stroke-width="2"/>',
              f'<line class="flow" x1="{cx + cw / 2}" y1="{y1}" x2="{cx + cw / 2}" y2="{y2}" stroke="{CYAN}" stroke-width="2"/>',
              f'<path d="M{cx + cw / 2 - 6} {y2 - 8} l6 7 6 -7" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>']
    # request packet travels down the core column, drawn under the boxes
    b.append(f'<circle r="6" fill="{CYAN}"><animateMotion dur="5s" repeatCount="indefinite" path="M{cx + cw / 2} {ys[0] + bh} V{ys[3]}"/></circle>')
    for i, (idx, name, sub) in enumerate(CORE):
        y = ys[i]
        col = CYAN if i % 2 else soft
        b += [f'<rect x="{cx}" y="{y}" width="{cw}" height="{bh}" rx="16" fill="{t["card"]}"/>',
              f'<rect class="ly" style="animation-delay:{i * 1.2:.1f}s" x="{cx + .5}" y="{y + .5}" width="{cw - 1}" height="{bh - 1}" rx="15.5" fill="none" stroke="{col}" stroke-opacity=".4" stroke-width="1.5"/>',
              f'<rect x="{cx}" y="{y + 18}" width="4" height="{bh - 36}" rx="2" fill="url(#brandd)"/>',
              f'<text class="mono" x="{cx + 28}" y="{y + 47}" font-size="15" fill="{col}">{idx}</text>',
              f'<text x="{cx + 70}" y="{y + 36}" font-size="21" font-weight="800" fill="{t["title"]}">{e(name)}</text>',
              f'<text x="{cx + 70}" y="{y + 60}" font-size="14.5" font-weight="400" fill="{t["muted"]}">{e(sub)}</text>']
    # infrastructure (right)
    ix, iw, iy = 820, 400, ys[2]
    b += [f'<rect x="{ix}" y="{iy}" width="{iw}" height="{bh}" rx="16" fill="{t["card"]}"/>',
          f'<rect class="ly" style="animation-delay:2.4s" x="{ix + .5}" y="{iy + .5}" width="{iw - 1}" height="{bh - 1}" rx="15.5" fill="none" stroke="{CYAN}" stroke-opacity=".4" stroke-width="1.5"/>',
          f'<text class="mono" x="{ix + 24}" y="{iy + 47}" font-size="15" fill="{CYAN}">05</text>',
          f'<text x="{ix + 62}" y="{iy + 36}" font-size="21" font-weight="800" fill="{t["title"]}">Infrastructure</text>',
          f'<text x="{ix + 62}" y="{iy + 60}" font-size="14.5" fill="{t["muted"]}">EF Core · Repositories · UoW</text>',
          # implements arrow (infra -> application interfaces)
          f'<line class="flow" x1="{ix}" y1="{iy + bh / 2}" x2="{cx + cw + 8}" y2="{iy + bh / 2}" stroke="{soft}" stroke-width="2"/>',
          f'<path d="M{cx + cw + 16} {iy + bh / 2 - 6} l-7 6 7 6" fill="none" stroke="{soft}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<text x="{(ix + cx + cw) / 2:.0f}" y="{iy + bh / 2 + 24}" font-size="11" font-weight="600" letter-spacing="1" text-anchor="middle" fill="{t["muted"]}">IMPLEMENTS</text>',
          # DI registration (api -> infra)
          f'<path class="flow" d="M{cx + cw} {ys[1] + bh / 2} H{ix + iw / 2} V{iy - 8}" fill="none" stroke="{CYAN}" stroke-width="2"/>',
          f'<path d="M{ix + iw / 2 - 6} {iy - 14} l6 7 6 -7" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<text x="{ix + iw / 2 + 12}" y="{ys[1] + bh / 2 - 10}" font-size="12" font-weight="600" letter-spacing="1.5" fill="{t["muted"]}">DI REGISTRATION</text>']
    # stores
    sy = ys[3]
    sw = (iw - 20) / 3
    for k, (name, sub) in enumerate(STORES):
        x = ix + k * (sw + 10)
        b += [f'<rect x="{x:.1f}" y="{sy}" width="{sw:.1f}" height="{bh}" rx="14" fill="{t["card2"]}" stroke="{t["line"]}"/>',
              f'<text x="{x + sw / 2:.1f}" y="{sy + 35}" font-size="13" font-weight="800" text-anchor="middle" fill="{t["title"]}">{e(name)}</text>',
              f'<text x="{x + sw / 2:.1f}" y="{sy + 57}" font-size="11.5" text-anchor="middle" fill="{t["muted"]}">{e(sub)}</text>',
              f'<line class="flow" x1="{x + sw / 2:.1f}" y1="{iy + bh}" x2="{x + sw / 2:.1f}" y2="{sy}" stroke="{t["muted"]}" stroke-opacity=".6" stroke-width="1.5"/>']
    # request packet down the core column
    b.append(f'<text x="{W - 60}" y="62" font-size="13" font-weight="600" letter-spacing="2" text-anchor="end" fill="{CYAN}">ASP.NET CORE · .NET 10</text>')
    return svg(W, H, "\n".join(b), css, defs, mono=True,
               title="Clean Architecture request flow: Clients, API, Application, Domain, Infrastructure, SQL Server, Redis, Azure")


# --------------------------------------------------------------------------- footer
def footer(mode):
    t = THEMES[mode]
    W, H = 1280, 190
    css = """
.w1{animation:wv 10s linear infinite}.w2{animation:wv 15s linear infinite reverse}.w3{animation:wv 22s linear infinite}
@keyframes wv{to{transform:translateX(-1280px)}}"""
    wave = lambda y, a: f"M0 {y} " + " ".join(f"Q{160 + 640 * k} {y - a} {320 + 640 * k} {y} T{640 + 640 * k} {y}" for k in range(4)) + f" V{H} H0Z"  # noqa: E731
    b = [f'<text x="640" y="40" font-size="13" font-weight="800" letter-spacing="7" text-anchor="middle" fill="url(#brand)">MOHAMED NOWAR</text>',
         f'<text x="640" y="78" font-size="22" font-weight="600" text-anchor="middle" fill="{t["title"]}">Building backend systems that are as <tspan font-weight="800" fill="url(#brand)">clean</tspan> as the code that powers them.</text>',
         f'<g class="w3" opacity=".22"><path fill="url(#brand)" d="{wave(130, 34)}"/></g>',
         f'<g class="w2" opacity=".42"><path fill="url(#brand)" d="{wave(148, 26)}"/></g>',
         f'<g class="w1" opacity=".9"><path fill="url(#brand)" d="{wave(166, 18)}"/></g>']
    return svg(W, H, "\n".join(b), css, title="Building backend systems that are as clean as the code that powers them.")


# --------------------------------------------------------------------------- trust badges (J. SERVO review platforms)
TRUSTPILOT = ("M17.227 16.67l2.19 6.742-7.413-5.388 5.223-1.354zM24 9.31h-9.165L12.005.589l-2.84 8.723L0 9.3"
              "l7.422 5.397-2.84 8.714 7.422-5.388 4.583-3.326L24 9.311z")
WIKIDATA = ("M0 4.583v14.833h.865V4.583zm1.788 0v14.833h2.653V4.583zm3.518 0v14.832H7.96V4.583zm3.547 0v14.834h.866V4.583z"
            "m1.789 0v14.833h.865V4.583zm1.759 0v14.834h2.653V4.583zm3.518 0v14.834h.923V4.583zm1.788 0v14.833h2.653V4.583z"
            "m3.64 0v14.834h.865V4.583zm1.788 0v14.834H24V4.583Z")
TRUST = [
    ("trustpilot", "REVIEWS ON", "Trustpilot", ("path", TRUSTPILOT)),
    ("clutch", "REVIEWS ON", "Clutch", ("mono", "C")),
    ("goodfirms", "REVIEWS ON", "GoodFirms", ("mono", "GF")),
    ("techbehemoths", "VERIFIED ON", "TechBehemoths", ("mono", "TB")),
    ("sortlist", "LISTED ON", "Sortlist", ("mono", "S")),
    ("f6s", "PROFILE ON", "F6S", ("mono", "F6S")),
    ("wikidata", "ENTITY Q141189697", "Wikidata", ("path", WIKIDATA),
     "Structured company data for search engines and AI assistants"),
]


def trust(mode, i, eyebrow, name, mark, note=None):
    t = THEMES[mode]
    W, H = (1180 if note else 380), 84
    css = f'''
.sw{{animation:sw 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes sw{{0%{{transform:translateX(-200px)}}45%,100%{{transform:translateX({1400 if note else 560}px)}}}}
.tile{{animation:tile 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes tile{{0%,16%,100%{{stroke-opacity:.45}}7%{{stroke-opacity:1}}}}'''
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{t["card"]}"/>',
         f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="17.5" fill="none" stroke="url(#brandd)" stroke-opacity=".55"/>',
         f'<rect x="1" y="18" width="4" height="{H - 36}" rx="2" fill="url(#brandd)"/>',
         f'<rect x="20" y="16" width="52" height="52" rx="14" fill="{PURPLE}" fill-opacity=".14"/>',
         f'<rect class="tile" x="20.5" y="16.5" width="51" height="51" rx="13.5" fill="none" stroke="url(#brandd)" stroke-width="1.5"/>']
    kind, val = mark
    acc = t["accent"]
    if kind == "path":
        b.append(f'<g transform="translate(34 30)"><path d="{val}" fill="{acc}"/></g>')
    else:
        size = {1: 24, 2: 18, 3: 13}[len(val)]
        b.append(f'<text x="46" y="{42 + size * .36:.1f}" font-size="{size}" font-weight="800" text-anchor="middle" fill="{acc}">{e(val)}</text>')
    b += [f'<text x="90" y="36" font-size="11" font-weight="600" letter-spacing="2.2" fill="{t["muted"]}">J. SERVO · {e(eyebrow)}</text>',
          f'<text x="89" y="62" font-size="{18 if len(name) > 11 else 20}" font-weight="800" fill="{t["title"]}">{e(name)}</text>',
          f'<path d="M{W - 34} 32 l9 -9 M{W - 32} 23 h7 v7" fill="none" stroke="{acc}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<g clip-path="url(#c)"><rect class="sw" x="0" y="0" width="140" height="{H}" fill="url(#sheen)"/></g>']
    if note:
        b.append(f'<text x="{W - 56}" y="56" font-size="16" text-anchor="end" fill="{t["muted"]}">{e(note)}</text>')
    return svg(W, H, "\n".join(b), css, title=f"J. SERVO on {name}")


def main():
    for mode in THEMES:
        write(os.path.join(ASSETS, f"banner-{mode}.svg"), banner(mode))
        write(os.path.join(ASSETS, f"about-{mode}.svg"), about(mode))
        write(os.path.join(ASSETS, f"stats-{mode}.svg"), stats(mode))
        write(os.path.join(ASSETS, f"architecture-{mode}.svg"), architecture(mode))
        write(os.path.join(ASSETS, f"footer-{mode}.svg"), footer(mode))
        for i, (slug, eyebrow, name, mark, *note) in enumerate(TRUST):
            write(os.path.join(TRUST_OUT, f"{slug}-{mode}.svg"), trust(mode, i, eyebrow, name, mark, *note))
    write(os.path.join(ASSETS, "divider.svg"), divider())
    for root, _, files in os.walk(ASSETS):
        for f in sorted(files):
            if f.endswith(".svg") and "certs" not in root:
                p = os.path.join(root, f)
                print(os.path.relpath(p, ROOT), os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    main()
