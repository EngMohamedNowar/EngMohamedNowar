"""Generate the animated SVG artwork used by README.md.

Run from the repo root:   python scripts/build_profile.py
Writes light + dark variants of banner, about, stats, architecture, footer and trust badges,
a theme-neutral divider, and animated 48px icons (assets/icons/) for headings and cards.

Rules kept by every generator here:
- Text is static. Animation only moves decoration or slides elements with transform; every
  keyframe loop starts in the resting look, so a frozen timeline or prefers-reduced-motion
  still shows everything. Nothing fades in from opacity 0.
- Syne / Syne Mono are inlined (see brand.py) because <img> SVGs cannot load web fonts.
- Sizes target ~850px display width on GitHub (see brand.py).
"""
import os
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from brand import CYAN, FONT, FONT_FACE, MONO, MONO_FACE, REDUCED, THEMES, VIOLET, grad  # noqa: E402

ASSETS = os.path.join(ROOT, "assets")
TRUST_OUT = os.path.join(ASSETS, "trust")
ICON_OUT = os.path.join(ASSETS, "icons")
for d in (TRUST_OUT, ICON_OUT):
    os.makedirs(d, exist_ok=True)

CHAR_W = 0.569  # Syne Mono advance in em (measured with getBBox)


def e(s):
    return escape(s, quote=True)


def write(path, s):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)


# shared motion: entrance slides (transform only), glow drift, sheen sweep, flowing dashes
BASE_CSS = """
.in{animation:in .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes in{from{transform:translateY(14px)}to{transform:none}}
.inx{animation:inx .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes inx{from{transform:translateX(-18px)}to{transform:none}}
.gl1{animation:drift 14s ease-in-out infinite}
.gl2{animation:drift 18s ease-in-out infinite reverse}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,14px)}}
.flow{stroke-dasharray:6 8;animation:flow 1.1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-28}}
.caret{animation:blink 1.1s steps(1) infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
.edge{stroke-dasharray:14 86;animation:edge 9s linear infinite}
@keyframes edge{to{stroke-dashoffset:-100}}"""


def svg(w, h, body, css, t, defs="", mono=False, title=""):
    faces = FONT_FACE + ("\n" + MONO_FACE if mono else "")
    head = f"<title>{e(title)}</title>\n" if title else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">
{head}<style>
{faces}
.mono{{font-family:{MONO}}}
{BASE_CSS}
{css}
{REDUCED}
</style>
<defs>
{grad("acc", t)}
{grad("accd", t, x2="1", y2="1")}
{grad("accv", t, x2="0", y2="1")}
<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".10"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
{defs}
</defs>
{body}
</svg>
'''


def backdrop(w, h, t, rx=22):
    """Rounded panel: gradient background, grid, drifting glows and a travelling edge light."""
    defs = "\n".join([
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>',
        f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}"/></pattern>',
        f'<radialGradient id="g1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["c1"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["c1"]}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="g2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["c2"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["c2"]}" stop-opacity="0"/></radialGradient>',
        f'<clipPath id="panel"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}"/></clipPath>'])
    body = "\n".join([
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="url(#bg)"/>',
        f'<g clip-path="url(#panel)"><rect width="{w}" height="{h}" fill="url(#grid)"/>',
        f'<ellipse class="gl1" cx="{w * .12:.0f}" cy="{h * .1:.0f}" rx="{w * .32:.0f}" ry="{h * .9:.0f}" fill="url(#g2)"/>',
        f'<ellipse class="gl2" cx="{w * .9:.0f}" cy="{h * .85:.0f}" rx="{w * .3:.0f}" ry="{h * .9:.0f}" fill="url(#g1)"/></g>',
        f'<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="{rx - .5}" fill="none" stroke="{t["line"]}"/>',
        f'<rect class="edge" x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="{rx - .5}" fill="none" stroke="url(#accd)" stroke-width="2" pathLength="100"/>'])
    return defs, body


def delay(s):
    return f' style="animation-delay:{s:.2f}s"'


# --------------------------------------------------------------------------- banner
LAYERS = [("API", "Controllers · JWT"), ("Application", "CQRS · MediatR"),
          ("Domain", "Entities · Rules"), ("Infrastructure", "EF Core · Redis")]
CHIPS = ["Cairo, Egypt", "Open to remote & freelance", "583 automated tests"]


def banner(mode):
    t = THEMES[mode]
    W, H = 1280, 420
    defs, back = backdrop(W, H, t)
    css = f"""
.ly{{animation:ly 4.8s ease-in-out infinite}}
@keyframes ly{{0%,30%,100%{{stroke-opacity:.35}}12%{{stroke-opacity:1}}}}
.ok{{animation:ok 2.4s ease-in-out infinite}}
@keyframes ok{{0%,100%{{fill-opacity:.14}}50%{{fill-opacity:.3}}}}
.chip{{animation:chip 6s ease-in-out infinite}}
@keyframes chip{{0%,22%,100%{{transform:translateY(0)}}11%{{transform:translateY(-4px)}}}}
.sw{{animation:sw 9s ease-in-out infinite}}
@keyframes sw{{0%{{transform:translateX(-300px)}}50%,100%{{transform:translateX(1500px)}}}}"""
    b = [back, '<g class="inx">',
         f'<text x="80" y="76" font-size="17" font-weight="600" letter-spacing="4.5" fill="{t["c1"]}">SOFTWARE ENGINEER  ·  J. SERVO LLC</text>',
         f'<rect x="80" y="92" width="64" height="4" rx="2" fill="url(#acc)"/>',
         f'<text x="74" y="166" font-size="72" font-weight="800" letter-spacing="-1" fill="{t["title"]}">Mohamed</text>',
         f'<text x="74" y="236" font-size="72" font-weight="800" letter-spacing="-1" fill="url(#acc)">Nowar<tspan fill="{t["c1"]}">.</tspan></text>',
         '</g>',
         f'<g class="in"{delay(.15)}>',
         f'<text x="80" y="286" font-size="27" font-weight="500" fill="{t["text"]}">.NET backend engineer building secure, tested APIs</text>',
         f'<text x="80" y="322" font-size="19" font-weight="400" fill="{t["muted"]}">ASP.NET Core · C# · EF Core · SQL Server · Clean Architecture</text>',
         '</g>']
    x = 80
    for k, c in enumerate(CHIPS):
        w = round(len(c) * 10.2 + 50)
        col = t["c2"] if k % 2 else t["c1"]
        b.append(f'<g class="chip"{delay(k * .5)}><rect x="{x}" y="346" width="{w}" height="40" rx="20" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6"/>'
                 f'<circle cx="{x + 20}" cy="366" r="5" fill="{col}"/>'
                 f'<text x="{x + 34}" y="372" font-size="17" font-weight="600" fill="{t["text"]}">{e(c)}</text></g>')
        x += w + 12
    # right column: one request travelling through the layers
    rx0, cw = 846, 394
    lx = rx0 + 18
    b += [f'<g class="in"{delay(.3)}>',
          f'<rect x="{rx0}" y="40" width="{cw}" height="60" rx="16" fill="{t["card"]}" stroke="url(#accd)"/>',
          f'<text class="mono" x="{rx0 + 22}" y="78" font-size="19" fill="{t["muted"]}"><tspan fill="{t["c1"]}">GET</tspan> <tspan fill="{t["title"]}">/api/orders/42</tspan></text>',
          f'<rect class="caret" x="{rx0 + 22 + 18 * 19 * CHAR_W + 4:.0f}" y="62" width="10" height="22" rx="1" fill="{t["c1"]}"/>',
          f'<rect class="ok" x="{rx0 + cw - 120}" y="56" width="104" height="30" rx="15" fill="{t["ok"]}" fill-opacity=".14" stroke="{t["ok"]}" stroke-opacity=".6"/>',
          f'<text class="mono" x="{rx0 + cw - 68}" y="77" font-size="16" text-anchor="middle" fill="{t["ok"]}">200 OK</text>',
          f'<line x1="{lx}" y1="100" x2="{lx}" y2="372" stroke="{t["line"]}" stroke-width="2"/>',
          f'<line class="flow" x1="{lx}" y1="100" x2="{lx}" y2="372" stroke="url(#accv)" stroke-width="2"/>']
    for k, (name, sub) in enumerate(LAYERS):
        y = 118 + k * 56
        col = t["c2"] if k % 2 else t["c1"]
        b += [f'<rect x="{lx + 26}" y="{y}" width="{cw - 44}" height="44" rx="12" fill="{t["card"]}" fill-opacity=".94"/>',
              f'<rect class="ly"{delay(k * .6)} x="{lx + 26.5}" y="{y + .5}" width="{cw - 45}" height="43" rx="11.5" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.5"/>',
              f'<circle cx="{lx}" cy="{y + 22}" r="7" fill="{t["card"]}" stroke="{col}" stroke-width="2.5"/>',
              f'<text x="{lx + 44}" y="{y + 29}" font-size="20" font-weight="700" fill="{t["title"]}">{e(name)}</text>',
              f'<text class="mono" x="{rx0 + cw - 16}" y="{y + 28}" font-size="16" text-anchor="end" fill="{t["muted"]}">{e(sub)}</text>']
    dy = 348
    b += [f'<g transform="translate({lx + 26} {dy})">'
          f'<path d="M0 7 v22 c0 5 16 9 34 9 s34 -4 34 -9 v-22" fill="{t["card"]}" stroke="{t["c1"]}" stroke-width="1.8"/>'
          f'<ellipse cx="34" cy="7" rx="34" ry="8" fill="{t["card2"]}" stroke="{t["c1"]}" stroke-width="1.8"/>'
          f'<text x="84" y="30" font-size="19" font-weight="700" fill="{t["title"]}">SQL Server</text>'
          f'<text class="mono" x="206" y="29" font-size="16" fill="{t["muted"]}">+ Redis</text></g>',
          '</g>',
          f'<circle r="6" fill="{t["c1"]}"><animateMotion dur="4.8s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.45;1" calcMode="linear" path="M{lx} 100 V372"/></circle>',
          f'<circle r="6" fill="{t["c2"]}"><animateMotion dur="4.8s" repeatCount="indefinite" keyPoints="1;1;0;0" keyTimes="0;.5;.95;1" calcMode="linear" path="M{lx} 100 V372"/></circle>',
          f'<g clip-path="url(#panel)"><g transform="skewX(-18)"><rect class="sw" x="0" y="0" width="200" height="{H}" fill="url(#sheen)"/></g></g>']
    return svg(W, H, "\n".join(b), css, t, defs, mono=True,
               title="Mohamed Nowar — Software Engineer at J. Servo LLC, .NET backend engineer")


# --------------------------------------------------------------------------- divider (theme neutral)
def divider():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="14" viewBox="0 0 1200 14" preserveAspectRatio="none">
<defs><linearGradient id="dv" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient></defs>
<style>.m{{animation:mv 4.5s cubic-bezier(.45,0,.55,1) infinite}}@keyframes mv{{0%{{transform:translateX(-420px)}}100%{{transform:translateX(1200px)}}}}
.p{{transform-box:fill-box;transform-origin:center;animation:p 2.4s ease-in-out infinite}}@keyframes p{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.6)}}}}{REDUCED}</style>
<rect y="6.5" width="1200" height="1" fill="{CYAN}" fill-opacity=".22"/>
<rect class="m" y="6" width="420" height="2" rx="1" fill="url(#dv)"/>
<circle class="p" cx="600" cy="7" r="3" fill="{CYAN}"/><circle cx="584" cy="7" r="2" fill="{VIOLET}"/><circle cx="616" cy="7" r="2" fill="{VIOLET}"/>
</svg>
'''


# --------------------------------------------------------------------------- about (code card + now)
NOW = [("NOW", "Software Engineer", "J. Servo LLC · since Jun 2026"),
       ("LEARNING", "Elevate Bootcamp", "Backend Advanced · .NET track"),
       ("BUILDING", "Accounting Platform", "ASP.NET Core · React · EF Core"),
       ("EXPLORING", "Microservices", "RabbitMQ · Azure Service Bus")]


def about(mode):
    t = THEMES[mode]
    kw, ty, st, pu = t["c2"], t["c1"], t["str"], t["muted"]
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
        return out + [P("]")]

    def prop(name, *val):
        return [X("    " + name.ljust(9)), P("= ")] + list(val) + [P(",")]

    lines = [
        [K("using "), T("Nowar"), P("."), T("Engineering"), P(";")],
        [],
        [K("var "), X("engineer "), P("= "), K("new "), T("SoftwareEngineer")],
        [P("{")],
        prop("Name", S("Mohamed Nowar")),
        prop("Role", S("Software Engineer @ J. Servo")),
        prop("Focus", S(".NET backend · REST APIs")),
        prop("Stack", *arr("C#", "ASP.NET Core", "EF Core", "SQL")),
        prop("Patterns", *arr("Clean Arch", "CQRS", "UoW")),
        prop("Testing", *arr("xUnit", "NSubstitute")),
        prop("Location", S("Cairo, Egypt")),
        prop("OpenTo", *arr("Remote", "Hybrid", "Freelance")),
        [P("};")],
        [("// Build succeeded · 0 warnings · 0 errors ✔", t["ok"])],
    ]
    W, FS, LH, top = 1280, 19, 31, 106
    H = top + len(lines) * LH + 30
    defs, back = backdrop(W, H, t, rx=20)
    css = """
.hl{animation:hl 9s ease-in-out infinite}
@keyframes hl{0%{transform:translateY(0)}100%{transform:translateY(SPANpx)}}
.node{transform-box:fill-box;transform-origin:center;animation:node 6s ease-in-out infinite}
@keyframes node{0%,20%,100%{transform:scale(1)}10%{transform:scale(1.35)}}""".replace("SPAN", str((len(lines) - 1) * LH))
    b = [back,
         f'<rect x="1" y="1" width="{W - 2}" height="60" rx="20" fill="{t["card"]}" fill-opacity=".9"/>',
         f'<rect x="1" y="40" width="{W - 2}" height="21" fill="{t["card"]}" fill-opacity=".9"/>',
         f'<line x1="1" y1="61" x2="{W - 1}" y2="61" stroke="{t["line"]}"/>',
         f'<circle cx="32" cy="31" r="7.5" fill="#FF5F57"/><circle cx="57" cy="31" r="7.5" fill="#FEBC2E"/><circle cx="82" cy="31" r="7.5" fill="#28C840"/>',
         f'<text x="{W / 2:.0f}" y="37" font-size="17" font-weight="600" letter-spacing="1" text-anchor="middle" fill="{t["muted"]}">Engineer.cs  —  dotnet run</text>',
         f'<text x="{W - 30}" y="37" font-size="15" font-weight="700" letter-spacing="2.5" text-anchor="end" fill="{t["c1"]}">C# · .NET</text>',
         f'<rect class="hl" x="2" y="{top - 22}" width="770" height="{LH}" fill="{t["c1"]}" fill-opacity=".07"/>',
         '<g class="in">']
    for i, segs in enumerate(lines):
        y = top + i * LH
        b.append(f'<text class="mono" x="52" y="{y}" font-size="16" text-anchor="end" fill="{t["muted"]}" fill-opacity=".6">{i + 1}</text>')
        if segs:
            spans = "".join(f'<tspan fill="{c}">{e(s)}</tspan>' for s, c in segs)
            b.append(f'<text class="mono" x="74" y="{y}" font-size="{FS}" xml:space="preserve">{spans}</text>')
    b.append('</g>')
    last = top + (len(lines) - 1) * LH
    chars = sum(len(s) for s, _ in lines[-1])
    b.append(f'<rect class="caret" x="{74 + chars * FS * CHAR_W + 8:.0f}" y="{last - 18}" width="11" height="23" fill="{t["c1"]}"/>')
    # right column
    px = 820
    b += [f'<line x1="{px - 36}" y1="84" x2="{px - 36}" y2="{H - 30}" stroke="{t["line"]}"/>',
          f'<g class="in"{delay(.2)}>',
          f'<text x="{px}" y="{top}" font-size="15" font-weight="600" letter-spacing="3.5" fill="{t["muted"]}">RIGHT NOW</text>',
          f'<line x1="{px + 9}" y1="{top + 40}" x2="{px + 9}" y2="{top + 40 + 3 * 92}" stroke="{t["line"]}" stroke-width="2"/>',
          f'<line class="flow" x1="{px + 9}" y1="{top + 40}" x2="{px + 9}" y2="{top + 40 + 3 * 92}" stroke="url(#accv)" stroke-width="2"/>']
    for k, (tag, head, sub) in enumerate(NOW):
        y = top + 46 + k * 92
        col = t["c2"] if k % 2 else t["c1"]
        b += [f'<circle cx="{px + 9}" cy="{y - 6}" r="8" fill="{t["card"]}" stroke="{col}" stroke-width="3"/>',
              f'<circle class="node"{delay(k * 1.5)} cx="{px + 9}" cy="{y - 6}" r="3.5" fill="{col}"/>',
              f'<text x="{px + 34}" y="{y}" font-size="14" font-weight="700" letter-spacing="2.6" fill="{col}">{e(tag)}</text>',
              f'<text x="{px + 34}" y="{y + 28}" font-size="22" font-weight="800" fill="{t["title"]}">{e(head)}</text>',
              f'<text x="{px + 34}" y="{y + 52}" font-size="18" fill="{t["muted"]}">{e(sub)}</text>']
    b.append('</g>')
    return svg(W, H, "\n".join(b), css, t, defs, mono=True,
               title="Mohamed Nowar: Software Engineer at J. Servo LLC, .NET backend, Cairo, Egypt")


# --------------------------------------------------------------------------- stats strip
STATS = [("7", "Shipped projects", "API · MVC · WPF · REACT"),
         ("583", "Automated tests", "XUNIT · NSUBSTITUTE"),
         ("8", "Certifications", "ROUTE · ITI · HUAWEI"),
         ("96%", "HCIA-AI score", "HUAWEI · 2024")]


def stats(mode):
    t = THEMES[mode]
    W, H, gap = 1280, 200, 20
    cw = (W - gap * 3) / 4
    css = """
.bar{animation:bar 6s ease-in-out infinite;transform-box:fill-box;transform-origin:left}
@keyframes bar{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.55)}}
.sw{animation:sw 8s ease-in-out infinite}
@keyframes sw{0%{transform:translateX(-200px)}45%,100%{transform:translateX(560px)}}
.num{animation:num 6s ease-in-out infinite}
@keyframes num{0%,16%,100%{transform:translateY(0)}8%{transform:translateY(-5px)}}"""
    b, defs = [], []
    for i, (num, label, sub) in enumerate(STATS):
        x = i * (cw + gap)
        d = delay(i * .7)
        defs.append(f'<clipPath id="c{i}"><rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18"/></clipPath>')
        b += [f'<g class="in"{delay(i * .12)}>',
              f'<rect x="{x + 1:.1f}" y="1" width="{cw - 2:.1f}" height="{H - 2}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>',
              f'<rect class="edge"{delay(-i * 2.2)} x="{x + 1.5:.1f}" y="1.5" width="{cw - 3:.1f}" height="{H - 3}" rx="17.5" fill="none" stroke="url(#accd)" stroke-width="2" pathLength="100"/>',
              f'<g class="num"{d}><text x="{x + 30:.1f}" y="88" font-size="64" font-weight="800" letter-spacing="-1" fill="url(#acc)">{e(num)}</text></g>',
              f'<text x="{x + 30:.1f}" y="126" font-size="22" font-weight="700" fill="{t["title"]}">{e(label)}</text>',
              f'<text x="{x + 30:.1f}" y="154" font-size="14" font-weight="600" letter-spacing="2" fill="{t["muted"]}">{e(sub)}</text>',
              f'<rect x="{x + 30:.1f}" y="172" width="{cw - 60:.1f}" height="5" rx="2.5" fill="{t["line"]}"/>',
              f'<rect class="bar"{d} x="{x + 30:.1f}" y="172" width="{cw - 60:.1f}" height="5" rx="2.5" fill="url(#acc)"/>',
              f'<g clip-path="url(#c{i})"><g transform="translate({x:.1f} 0)"><rect class="sw"{d} x="0" y="0" width="120" height="{H}" fill="url(#sheen)"/></g></g>',
              '</g>']
    return svg(W, H, "\n".join(b), css, t, "\n".join(defs),
               title="7 shipped projects · 583 automated tests · 8 certifications · 96% HCIA-AI score")


# --------------------------------------------------------------------------- architecture
CORE = [("01", "Clients", "Web · Mobile · Swagger · Postman"),
        ("02", "API layer", "Controllers · Middleware · JWT · Rate limiting"),
        ("03", "Application layer", "CQRS · MediatR · DTOs · Validation"),
        ("04", "Domain layer", "Entities · Specifications · Business rules")]
STORES = [("SQL Server", "Relational data"), ("Redis", "Cache · Baskets"), ("Azure", "Cloud hosting")]


def architecture(mode):
    t = THEMES[mode]
    W, H = 1280, 620
    defs, back = backdrop(W, H, t)
    css = """
.ly{animation:ly 6s ease-in-out infinite}
@keyframes ly{0%,24%,100%{stroke-opacity:.4}10%{stroke-opacity:1}}"""
    b = [back, '<g class="inx">',
         f'<text x="48" y="64" font-size="16" font-weight="600" letter-spacing="3.5" fill="{t["muted"]}">CLEAN ARCHITECTURE  ·  REQUEST FLOW</text>',
         f'<text x="48" y="106" font-size="36" font-weight="800" fill="{t["title"]}">How my APIs are <tspan fill="url(#acc)">layered</tspan></text>',
         f'<text x="{W - 48}" y="64" font-size="16" font-weight="600" letter-spacing="2.5" text-anchor="end" fill="{t["c1"]}">ASP.NET CORE · .NET 10</text>',
         '</g>']
    cx, cw, bh = 48, 600, 92
    ys = [140 + i * 116 for i in range(4)]
    mid = cx + cw / 2
    for i in range(3):
        y1, y2 = ys[i] + bh, ys[i + 1]
        b += [f'<line x1="{mid}" y1="{y1}" x2="{mid}" y2="{y2}" stroke="{t["line"]}" stroke-width="2"/>',
              f'<line class="flow" x1="{mid}" y1="{y1}" x2="{mid}" y2="{y2}" stroke="{t["c1"]}" stroke-width="2"/>',
              f'<path d="M{mid - 7} {y2 - 9} l7 8 7 -8" fill="none" stroke="{t["c1"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>']
    b.append(f'<circle r="7" fill="{t["c1"]}"><animateMotion dur="5s" repeatCount="indefinite" path="M{mid} {ys[0] + bh} V{ys[3]}"/></circle>')
    for i, (idx, name, sub) in enumerate(CORE):
        y = ys[i]
        col = t["c2"] if i % 2 else t["c1"]
        b += [f'<g class="in"{delay(.1 + i * .12)}>',
              f'<rect x="{cx}" y="{y}" width="{cw}" height="{bh}" rx="16" fill="{t["card"]}"/>',
              f'<rect class="ly"{delay(i * 1.2)} x="{cx + .5}" y="{y + .5}" width="{cw - 1}" height="{bh - 1}" rx="15.5" fill="none" stroke="{col}" stroke-opacity=".4" stroke-width="1.6"/>',
              f'<rect x="{cx}" y="{y + 20}" width="5" height="{bh - 40}" rx="2.5" fill="url(#accv)"/>',
              f'<text class="mono" x="{cx + 28}" y="{y + 54}" font-size="19" fill="{col}">{idx}</text>',
              f'<text x="{cx + 76}" y="{y + 41}" font-size="25" font-weight="800" fill="{t["title"]}">{e(name)}</text>',
              f'<text x="{cx + 76}" y="{y + 69}" font-size="18" fill="{t["muted"]}">{e(sub)}</text>',
              '</g>']
    ix, iw, iy = 760, 472, ys[2]
    b += [f'<g class="in"{delay(.45)}>',
          f'<rect x="{ix}" y="{iy}" width="{iw}" height="{bh}" rx="16" fill="{t["card"]}"/>',
          f'<rect class="ly"{delay(2.4)} x="{ix + .5}" y="{iy + .5}" width="{iw - 1}" height="{bh - 1}" rx="15.5" fill="none" stroke="{t["c1"]}" stroke-opacity=".4" stroke-width="1.6"/>',
          f'<text class="mono" x="{ix + 24}" y="{iy + 54}" font-size="19" fill="{t["c1"]}">05</text>',
          f'<text x="{ix + 70}" y="{iy + 41}" font-size="25" font-weight="800" fill="{t["title"]}">Infrastructure</text>',
          f'<text x="{ix + 70}" y="{iy + 69}" font-size="18" fill="{t["muted"]}">EF Core · Repositories · UoW</text>',
          '</g>',
          f'<line class="flow" x1="{ix}" y1="{iy + bh / 2}" x2="{cx + cw + 10}" y2="{iy + bh / 2}" stroke="{t["c2"]}" stroke-width="2"/>',
          f'<path d="M{cx + cw + 18} {iy + bh / 2 - 7} l-8 7 8 7" fill="none" stroke="{t["c2"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<text x="{(ix + cx + cw) / 2 + 4:.0f}" y="{iy + bh / 2 - 12}" font-size="12" font-weight="700" letter-spacing="1" text-anchor="middle" fill="{t["muted"]}">IMPLEMENTS</text>',
          f'<path class="flow" d="M{cx + cw} {ys[1] + bh / 2} H{ix + iw / 2} V{iy - 10}" fill="none" stroke="{t["c1"]}" stroke-width="2"/>',
          f'<path d="M{ix + iw / 2 - 7} {iy - 17} l7 8 7 -8" fill="none" stroke="{t["c1"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<text x="{ix + iw / 2 + 14}" y="{ys[1] + bh / 2 - 12}" font-size="14" font-weight="700" letter-spacing="1.5" fill="{t["muted"]}">DI REGISTRATION</text>']
    sy = ys[3]
    sw = (iw - 24) / 3
    for k, (name, sub) in enumerate(STORES):
        x = ix + k * (sw + 12)
        b += [f'<line class="flow" x1="{x + sw / 2:.1f}" y1="{iy + bh}" x2="{x + sw / 2:.1f}" y2="{sy}" stroke="{t["muted"]}" stroke-opacity=".7" stroke-width="1.6"/>',
              f'<g class="in"{delay(.6 + k * .1)}>',
              f'<rect x="{x:.1f}" y="{sy}" width="{sw:.1f}" height="{bh}" rx="14" fill="{t["card2"]}" stroke="{t["line"]}"/>',
              f'<text x="{x + sw / 2:.1f}" y="{sy + 40}" font-size="16" font-weight="800" text-anchor="middle" fill="{t["title"]}">{e(name)}</text>',
              f'<text x="{x + sw / 2:.1f}" y="{sy + 66}" font-size="14" text-anchor="middle" fill="{t["muted"]}">{e(sub)}</text>',
              '</g>']
    return svg(W, H, "\n".join(b), css, t, defs, mono=True,
               title="Clean Architecture request flow: Clients, API, Application, Domain, Infrastructure, SQL Server, Redis, Azure")


# --------------------------------------------------------------------------- footer
def footer(mode):
    t = THEMES[mode]
    W, H = 1280, 210
    css = """
.w1{animation:wv 10s linear infinite}.w2{animation:wv 15s linear infinite reverse}.w3{animation:wv 22s linear infinite}
@keyframes wv{to{transform:translateX(-1280px)}}"""
    wave = lambda y, a: f"M0 {y} " + " ".join(f"Q{160 + 640 * k} {y - a} {320 + 640 * k} {y} T{640 + 640 * k} {y}" for k in range(4)) + f" V{H} H0Z"  # noqa: E731
    b = ['<g class="in">',
         f'<text x="640" y="40" font-size="17" font-weight="800" letter-spacing="8" text-anchor="middle" fill="url(#acc)">MOHAMED NOWAR</text>',
         f'<text x="640" y="88" font-size="29" font-weight="600" text-anchor="middle" fill="{t["title"]}">Building backend systems as <tspan font-weight="800" fill="url(#acc)">clean</tspan> as the code behind them.</text>',
         '</g>',
         f'<g class="w3" opacity=".22"><path fill="url(#acc)" d="{wave(146, 34)}"/></g>',
         f'<g class="w2" opacity=".42"><path fill="url(#acc)" d="{wave(166, 26)}"/></g>',
         f'<g class="w1" opacity=".9"><path fill="url(#acc)" d="{wave(186, 18)}"/></g>']
    return svg(W, H, "\n".join(b), css, t, title="Building backend systems as clean as the code behind them.")


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
    ("wikidata", "J. SERVO · ENTITY Q141189697", "Wikidata", ("path", WIKIDATA),
     "Structured company data for search engines and AI assistants"),
]


def trust(mode, i, eyebrow, name, mark, note=None):
    t = THEMES[mode]
    W, H = (1180 if note else 380), 96
    css = f'''
.sw{{animation:sw 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes sw{{0%{{transform:translateX(-200px)}}45%,100%{{transform:translateX({1400 if note else 560}px)}}}}
.tile{{animation:tile 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes tile{{0%,16%,100%{{stroke-opacity:.5}}7%{{stroke-opacity:1}}}}
.mk{{transform-box:fill-box;transform-origin:center;animation:mk 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes mk{{0%,16%,100%{{transform:scale(1)}}8%{{transform:scale(1.15)}}}}
.ar{{animation:ar 7s ease-in-out infinite;animation-delay:{i * .6:.1f}s}}
@keyframes ar{{0%,16%,100%{{transform:translate(0,0)}}8%{{transform:translate(3px,-3px)}}}}'''
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18"/></clipPath>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>',
         f'<rect class="edge"{delay(-i * 1.3)} x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="17.5" fill="none" stroke="url(#accd)" stroke-width="2" pathLength="100"/>',
         f'<rect x="20" y="20" width="56" height="56" rx="15" fill="{t["c1"]}" fill-opacity=".12"/>',
         f'<rect class="tile" x="20.5" y="20.5" width="55" height="55" rx="14.5" fill="none" stroke="url(#accd)" stroke-width="1.6"/>']
    kind, val = mark
    if kind == "path":
        b.append(f'<g class="mk"><g transform="translate(34 34) scale(1.17)"><path d="{val}" fill="{t["c1"]}"/></g></g>')
    else:
        size = {1: 27, 2: 21, 3: 15}[len(val)]
        b.append(f'<g class="mk"><text x="48" y="{48 + size * .36:.1f}" font-size="{size}" font-weight="800" text-anchor="middle" fill="{t["c1"]}">{e(val)}</text></g>')
    name_fs = 19 if len(name) > 11 else 24
    b += [f'<text x="94" y="42" font-size="14" font-weight="600" letter-spacing="2.4" fill="{t["muted"]}">{e(eyebrow)}</text>',
          f'<text x="93" y="72" font-size="{name_fs}" font-weight="800" fill="{t["title"]}">{e(name)}</text>',
          f'<g class="ar"><path d="M{W - 32} 30 l10 -10 M{W - 30} 20 h8 v8" fill="none" stroke="{t["c1"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>',
          f'<g clip-path="url(#c)"><rect class="sw" x="0" y="0" width="140" height="{H}" fill="url(#sheen)"/></g>']
    if note:
        b.append(f'<text x="{W - 56}" y="64" font-size="20" text-anchor="end" fill="{t["muted"]}">{e(note)}</text>')
    return svg(W, H, "\n".join(b), css, t, title=f"J. SERVO on {name}")


# --------------------------------------------------------------------------- animated icons (theme neutral)
# name: (glyph svg on a 24 grid, motion class). Glyph strokes use the accent; the tile is translucent,
# so one file reads on both GitHub themes. Every icon in a group loops in 7s with a staggered delay,
# producing a wave across the row; motion sits in the first ~20% of the loop.
ICONS = {
    # section headings
    "about": ('<g class="m-bob"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></g>', 0),
    "stack": ('<path d="M3 12l9 5 9-5"/><path d="M3 16.5l9 5 9-5"/><g class="m-lift"><path d="M12 2.5 3 7.5l9 5 9-5z"/></g>', 1),
    "architecture": ('<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/>'
                     '<path class="m-flow" d="M12 7v5M5 17v-5h14v5"/>', 2),
    "projects": ('<g class="m-bob"><path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M10 11l-2 2 2 2M14 11l2 2-2 2"/></g>', 3),
    "screenshots": ('<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/><path class="m-scan" d="M5 7h14" stroke-opacity=".7"/>', 4),
    "stats": ('<path d="M3 21h18"/><path class="m-bar" d="M6 18V11"/><path class="m-bar b2" d="M12 18V5"/><path class="m-bar b3" d="M18 18v-9"/>', 5),
    "certificates": ('<g class="m-swing"><circle cx="12" cy="9" r="6"/><path d="M8.2 13.6 7 22l5-3 5 3-1.2-8.4"/><path d="M10 9l1.5 1.5L14.5 7.5"/></g>', 6),
    "work": ('<g class="m-bob"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/></g>', 7),
    "connect": ('<g class="m-fly"><path d="M22 2 11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></g>', 8),
    # capability cards
    "cap-architecture": ('<g class="m-tilt"><path d="M12 2 3 7v10l9 5 9-5V7z"/><path d="M3 7l9 5 9-5M12 12v10"/></g>', 0),
    "cap-security": ('<g class="m-pulse"><path d="M12 2l8 3v6c0 5-3.5 9.5-8 11-4.5-1.5-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></g>', 1),
    "cap-data": ('<g class="m-bob"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></g>', 2),
    "cap-testing": ('<path d="M9 2h6M10 2v6L4 20a1.5 1.5 0 0 0 1.3 2h13.4a1.5 1.5 0 0 0 1.3-2L14 8V2"/><g class="m-rise"><circle cx="10" cy="17" r="1"/><circle cx="14" cy="15" r="1"/></g>', 3),
    # featured projects
    "p-accounting": ('<rect x="5" y="2" width="14" height="20" rx="2"/><rect class="m-pulse" x="8" y="5" width="8" height="4" rx="1"/><path d="M8.5 13h.01M12 13h.01M15.5 13h.01M8.5 17h.01M12 17h.01M15.5 17h.01" stroke-width="2.6"/>', 0),
    "p-coffee": ('<path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10.5h1.5a2.5 2.5 0 0 1 0 5H17"/><g class="m-rise"><path d="M8 2.5c-1 1 1 2 0 3.5M12 2.5c-1 1 1 2 0 3.5"/></g>', 1),
    "p-ecommerce": ('<g class="m-roll"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.7 12.4a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 2-1.6L22 7H6"/></g>', 2),
    "p-pos": ('<g class="m-print"><path d="M5 2h14v20l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 7h6M9 11h6M9 15h4"/></g>', 3),
    "p-todo": ('<path d="M10 6h11M10 12h11M10 18h11"/><g class="m-pulse"><path d="M3 6l1.5 1.5L7 5M3 12l1.5 1.5L7 11M3 18l1.5 1.5L7 17"/></g>', 4),
    "p-gym": ('<g class="m-lift"><path d="M6 7v10M18 7v10M3 9v6M21 9v6M6 12h12"/></g>', 5),
    "p-cinema": ('<rect x="2" y="9" width="20" height="12" rx="2"/><g class="m-clap"><path d="M2 9 20.5 4.5l.8 3.2L2.8 12.2z"/><path d="M7 7.8l2 3M12 6.6l2 3M17 5.4l2 3"/></g>', 6),
}

ICON_CSS = """
.tile{animation:tile 7s ease-in-out infinite}
@keyframes tile{0%,20%,100%{stroke-opacity:.45}9%{stroke-opacity:1}}
.m-bob,.m-lift{animation:bob 7s ease-in-out infinite}
@keyframes bob{0%,20%,100%{transform:translateY(0)}10%{transform:translateY(-2.5px)}}
.m-swing{transform-box:fill-box;transform-origin:50% 0;animation:swing 7s ease-in-out infinite}
@keyframes swing{0%,22%,100%{transform:rotate(0)}6%{transform:rotate(-12deg)}13%{transform:rotate(9deg)}18%{transform:rotate(-3deg)}}
.m-fly{animation:fly 7s ease-in-out infinite}
@keyframes fly{0%,20%,100%{transform:translate(0,0)}10%{transform:translate(3px,-3px)}}
.m-pulse{transform-box:fill-box;transform-origin:center;animation:pulse 7s ease-in-out infinite}
@keyframes pulse{0%,20%,100%{transform:scale(1)}10%{transform:scale(1.14)}}
.m-tilt{transform-box:fill-box;transform-origin:center;animation:tilt 7s ease-in-out infinite}
@keyframes tilt{0%,20%,100%{transform:rotate(0)}10%{transform:rotate(14deg)}}
.m-roll{animation:roll 7s ease-in-out infinite}
@keyframes roll{0%,20%,100%{transform:translateX(0)}10%{transform:translateX(3px)}}
.m-print{animation:print 7s ease-in-out infinite}
@keyframes print{0%,20%,100%{transform:translateY(0)}10%{transform:translateY(2.5px)}}
.m-rise{animation:rise 7s ease-in-out infinite}
@keyframes rise{0%,20%,100%{transform:translateY(0)}10%{transform:translateY(-3px)}}
.m-scan{animation:scan 7s ease-in-out infinite}
@keyframes scan{0%,24%,100%{transform:translateY(0)}12%{transform:translateY(7px)}}
.m-flow{stroke-dasharray:3 3;animation:mflow 1.4s linear infinite}
@keyframes mflow{to{stroke-dashoffset:-12}}
.m-bar{transform-box:fill-box;transform-origin:50% 100%;animation:bar 7s ease-in-out infinite}
.b2{animation-delay:.15s}.b3{animation-delay:.3s}
@keyframes bar{0%,22%,100%{transform:scaleY(1)}10%{transform:scaleY(.5)}}
.m-clap{transform-box:fill-box;transform-origin:0 100%;animation:clap 7s ease-in-out infinite}
@keyframes clap{0%,20%,100%{transform:rotate(0)}8%{transform:rotate(-14deg)}}"""


def icon(name, glyph, slot):
    d = slot * .55
    css = ICON_CSS.replace("infinite}", f"infinite;animation-delay:{d:.2f}s}}")
    css = css.replace(".b2{animation-delay:.15s}.b3{animation-delay:.3s}",
                      f".b2{{animation-delay:{d + .15:.2f}s}}.b3{{animation-delay:{d + .3:.2f}s}}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
<title>{e(name)}</title>
<style>{css}
{REDUCED}</style>
<defs><linearGradient id="t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>
<rect x="1" y="1" width="46" height="46" rx="13" fill="{CYAN}" fill-opacity=".12"/>
<rect class="tile" x="1.5" y="1.5" width="45" height="45" rx="12.5" fill="none" stroke="url(#t)" stroke-width="1.6"/>
<g transform="translate(12 12)" fill="none" stroke="{CYAN}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>
</svg>
'''


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
    for name, (glyph, slot) in ICONS.items():
        write(os.path.join(ICON_OUT, f"{name}.svg"), icon(name, glyph, slot))
    print("wrote", len(THEMES) * (5 + len(TRUST)) + 1 + len(ICONS), "SVGs")


if __name__ == "__main__":
    main()
