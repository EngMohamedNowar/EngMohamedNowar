"""Phone-width (480px canvas) variants of the README artwork.

Run after build_profile.py:   python scripts/build_mobile.py
Writes assets/m/<name>-{dark,light}.svg. README.md serves them through <picture> sources with
media="(max-width: 1199px) ...", so phones get stacked layouts with readable type while desktops
keep the wide versions. A 480 canvas shows ~350px wide on a phone (scale ~0.73), so body text is
set at 17-20 and labels at 14-15.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from build_profile import (CHAR_W, CLAUDE, CRM_KPIS, CRM_STAGES, DIAR_STATS, GOLD, ICON_CSS, ICONS,  # noqa: E402
                           PROJECTS, SCREENS, STATS, STEPS, THEMES, TRUST, _shot, about, backdrop, delay, e,
                           svg, trust, write)

OUT = os.path.join(ROOT, "assets", "m")
os.makedirs(OUT, exist_ok=True)
MW = 480


def wrap(text, n):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def chips_rows(items, t, y, x0=24, fs=15, h=34, maxw=MW - 24, cls="chip"):
    """Lay chips out left to right, wrapping onto new rows."""
    out, x, row = [], x0, 0
    for k, c in enumerate(items):
        w = round(len(c) * fs * .6 + 40)
        if x + w > maxw:
            x, row = x0, row + 1
        yy = y + row * (h + 10)
        col = t["c2"] if k % 2 else t["c1"]
        out.append(f'<g class="{cls}"{delay(k * .5)}><rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="{h / 2}" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6"/>'
                   f'<circle cx="{x + 16}" cy="{yy + h / 2}" r="4" fill="{col}"/>'
                   f'<text x="{x + 27}" y="{yy + h / 2 + fs * .36:.1f}" font-size="{fs}" font-weight="600" fill="{t["text"]}">{e(c)}</text></g>')
        x += w + 8
    return out, y + (row + 1) * (h + 10)


CHIP_CSS = """
.chip{animation:chip 6s ease-in-out infinite}
@keyframes chip{0%,22%,100%{transform:translateY(0)}11%{transform:translateY(-3px)}}"""


def banner(mode):
    t = THEMES[mode]
    b = ['<g class="inx">',
         f'<text x="24" y="54" font-size="13" font-weight="600" letter-spacing="3" fill="{t["c1"]}">SOFTWARE ENGINEER · J. SERVO</text>',
         f'<rect x="24" y="66" width="48" height="3" rx="1.5" fill="url(#acc)"/>',
         f'<text x="20" y="126" font-size="54" font-weight="800" letter-spacing="-1" fill="{t["title"]}">Mohamed</text>',
         f'<text x="20" y="182" font-size="54" font-weight="800" letter-spacing="-1" fill="url(#acc)">Nowar<tspan fill="{t["c1"]}">.</tspan></text>',
         '</g>', f'<g class="in"{delay(.15)}>',
         f'<text x="24" y="222" font-size="19" font-weight="500" fill="{t["text"]}">.NET backend engineer building</text>',
         f'<text x="24" y="246" font-size="19" font-weight="500" fill="{t["text"]}">secure, tested APIs</text>',
         f'<text x="24" y="276" font-size="15" fill="{t["muted"]}">ASP.NET Core · C# · EF Core · SQL Server</text>',
         '</g>']
    chips, y = chips_rows(["Cairo, Egypt", "583 automated tests", "Open to remote & freelance"], t, 296)
    b += chips
    # compact request card
    ry = y + 6
    b += [f'<g class="in"{delay(.3)}><rect x="24" y="{ry}" width="{MW - 48}" height="52" rx="14" fill="{t["card"]}" stroke="url(#accd)"/>',
          f'<text class="mono" x="42" y="{ry + 32}" font-size="16" fill="{t["muted"]}"><tspan fill="{t["c1"]}">GET</tspan> <tspan fill="{t["title"]}">/api/orders/42</tspan></text>',
          f'<rect class="caret" x="{42 + 18 * 16 * CHAR_W + 4:.0f}" y="{ry + 16}" width="9" height="20" fill="{t["c1"]}"/>',
          f'<rect class="ok" x="{MW - 132}" y="{ry + 12}" width="92" height="28" rx="14" fill="{t["ok"]}" fill-opacity=".14" stroke="{t["ok"]}" stroke-opacity=".6"/>',
          f'<text class="mono" x="{MW - 86}" y="{ry + 31}" font-size="14" text-anchor="middle" fill="{t["ok"]}">200 OK</text></g>']
    H = ry + 52 + 24
    defs, back = backdrop(MW, H, t)
    css = CHIP_CSS + """
.ok{animation:ok 2.4s ease-in-out infinite}
@keyframes ok{0%,100%{fill-opacity:.14}50%{fill-opacity:.3}}"""
    return svg(MW, H, back + "\n" + "\n".join(b), css, t, defs, mono=True,
               title="Mohamed Nowar — Software Engineer at J. Servo LLC, .NET backend engineer")


def stats(mode):
    t = THEMES[mode]
    gap, cw, ch = 14, (MW - 14) / 2, 140
    css = """
.num{animation:num 6s ease-in-out infinite}
@keyframes num{0%,16%,100%{transform:translateY(0)}8%{transform:translateY(-4px)}}"""
    b = []
    for i, (num, label, _sub) in enumerate(STATS):
        x, y = (i % 2) * (cw + gap), (i // 2) * (ch + gap)
        b += [f'<g class="in"{delay(i * .12)}>',
              f'<rect x="{x + 1:.0f}" y="{y + 1}" width="{cw - 2:.0f}" height="{ch - 2}" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>',
              f'<rect class="edge"{delay(-i * 2.2)} x="{x + 1.5:.0f}" y="{y + 1.5}" width="{cw - 3:.0f}" height="{ch - 3}" rx="17.5" fill="none" stroke="url(#accd)" stroke-width="2" pathLength="100"/>',
              f'<g class="num"{delay(i * .7)}><text x="{x + 22:.0f}" y="{y + 72}" font-size="50" font-weight="800" fill="url(#acc)">{e(num)}</text></g>',
              f'<text x="{x + 22:.0f}" y="{y + 110}" font-size="18" font-weight="700" fill="{t["title"]}">{e(label)}</text>',
              '</g>']
    H = 2 * ch + gap
    return svg(MW, H, "\n".join(b), css, t, title="7 shipped projects · 583 automated tests · 8 certifications · 96% HCIA-AI score")


def jservo(mode):
    t = THEMES[mode]
    gold = GOLD[mode]
    b = ['<g class="inx">',
         f'<rect x="24" y="28" width="64" height="64" rx="18" fill="url(#accd)"/>',
         f'<text x="56" y="72" font-size="30" font-weight="800" text-anchor="middle" fill="#FFFFFF">J.</text>',
         f'<text x="106" y="50" font-size="13" font-weight="600" letter-spacing="3" fill="{t["c1"]}">WHERE I WORK</text>',
         f'<text x="104" y="84" font-size="32" font-weight="800" fill="{t["title"]}">J. Servo LLC</text>',
         f'<text x="24" y="128" font-size="17" fill="{t["muted"]}">AI agents, automation and digital</text>',
         f'<text x="24" y="152" font-size="17" fill="{t["muted"]}">platforms for SMEs · Cairo &amp; GCC</text>',
         '</g>',
         f'<g class="chip"><rect x="24" y="172" width="{MW - 48}" height="40" rx="20" fill="{t["c1"]}" fill-opacity=".12" stroke="{t["c1"]}" stroke-opacity=".6"/>'
         f'<circle cx="46" cy="192" r="5" fill="{t["ok"]}"/>'
         f'<text x="62" y="198" font-size="16" font-weight="600" fill="{t["text"]}">Software Engineer · since Jun 2026</text></g>',
         f'<path d="M56 212 V262" stroke="{t["line"]}" stroke-width="2"/>',
         f'<path class="flow" d="M56 212 V262" stroke="url(#accv)" stroke-width="2"/>',
         f'<text x="70" y="244" font-size="12" font-weight="600" letter-spacing="2.4" fill="{t["muted"]}">CLIENT PROJECT</text>']
    py = 262
    b += [f'<g class="in"{delay(.2)}>',
          f'<rect x="12" y="{py}" width="{MW - 24}" height="330" rx="18" fill="{t["card"]}" stroke="{gold}" stroke-opacity=".55"/>',
          f'<rect class="edge" x="12.5" y="{py + .5}" width="{MW - 25}" height="329" rx="17.5" fill="none" stroke="{gold}" stroke-width="2" pathLength="100"/>',
          f'<text x="36" y="{py + 44}" font-size="13" font-weight="600" letter-spacing="3" fill="{gold}">MAKKAH · MADINAH</text>',
          f'<text x="34" y="{py + 88}" font-size="36" font-weight="800" fill="{t["title"]}">Diar Al <tspan fill="{gold}">Manasik</tspan></text>',
          f'<text x="36" y="{py + 124}" font-size="17" fill="{t["text"]}">Bilingual hotel platform for pilgrims,</text>',
          f'<text x="36" y="{py + 148}" font-size="17" fill="{t["text"]}">every hotel listed by its real walking</text>',
          f'<text x="36" y="{py + 172}" font-size="17" fill="{t["text"]}">distance to the mosque.</text>']
    x = 36
    for k, (num, lab) in enumerate(DIAR_STATS):
        b += [f'<text x="{x}" y="{py + 228}" font-size="26" font-weight="800" fill="{gold if k == 1 else t["title"]}">{e(num)}</text>',
              f'<text x="{x}" y="{py + 252}" font-size="13" fill="{t["muted"]}">{e(lab.split(",")[0])}</text>']
        x += 142
    # little route strip
    ry = py + 290
    b += [f'<path d="M36 {ry} H{MW - 36}" stroke="{t["line"]}" stroke-width="3"/>',
          f'<path class="flow" d="M36 {ry} H{MW - 36}" stroke="{gold}" stroke-width="2.5"/>',
          f'<circle cx="36" cy="{ry}" r="7" fill="{t["card"]}" stroke="{gold}" stroke-width="2.5"/>',
          f'<circle cx="{MW - 36}" cy="{ry}" r="7" fill="{t["card"]}" stroke="{gold}" stroke-width="2.5"/>',
          f'<text x="52" y="{ry + 26}" font-size="14" fill="{t["muted"]}">Makkah · 14 hotels</text>',
          f'<text x="{MW - 52}" y="{ry + 26}" font-size="14" text-anchor="end" fill="{t["muted"]}">Madinah · 8 hotels</text>',
          f'<circle r="5" fill="{t["c1"]}"><animateMotion dur="5s" repeatCount="indefinite" path="M36 {ry} H{MW - 36}"/></circle>',
          '</g>']
    H = py + 330 + 16
    defs, back = backdrop(MW, H, t)
    return svg(MW, H, back + "\n" + "\n".join(b), CHIP_CSS, t, defs,
               title="Where I work: J. Servo LLC. Client project: Diar Al Manasik, bilingual hotel platform for pilgrims")


def frame(b, defs, t, i, x, y, fw, fn, url):
    src, (iw, ih) = _shot(fn, 720)
    bar = 30
    vh = round(fw * ih / iw)
    defs.append(f'<clipPath id="v{i}"><rect x="{x}" y="{y + bar}" width="{fw}" height="{vh}"/></clipPath>')
    b += [f'<g class="fl"{delay(-i * 2.3)}><g filter="url(#sh)"><rect x="{x}" y="{y}" width="{fw}" height="{bar + vh}" rx="12" fill="{t["card2"]}" stroke="{t["line"]}"/></g>',
          f'<circle cx="{x + 16}" cy="{y + 15}" r="5" fill="#FF5F57"/><circle cx="{x + 32}" cy="{y + 15}" r="5" fill="#FEBC2E"/><circle cx="{x + 48}" cy="{y + 15}" r="5" fill="#28C840"/>',
          f'<text x="{x + 64}" y="{y + 20}" font-size="12" fill="{t["muted"]}">{e(url)}</text>',
          f'<image href="{src}" x="{x}" y="{y + bar}" width="{fw}" height="{vh}" clip-path="url(#v{i})" preserveAspectRatio="xMidYMin slice"/></g>']
    return y + bar + vh


def gallery(mode):
    t = THEMES[mode]
    b, defs = [], [f'<filter id="sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity="{.45 if mode == "dark" else .2}"/></filter>']
    css = """
.fl{animation:fl 8s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"""
    y = frame(b, defs, t, 0, 16, 16, MW - 32, SCREENS[0][0], "diarmanasik.cloud/en")
    b.append(f'<text x="{MW / 2}" y="{y + 28}" font-size="15" text-anchor="middle" fill="{t["text"]}">{e(SCREENS[0][2])}</text>')
    y += 50
    fw = (MW - 32 - 14) / 2
    y1 = frame(b, defs, t, 1, 16, y, fw, SCREENS[1][0], "/ar")
    frame(b, defs, t, 2, 16 + fw + 14, y, fw, SCREENS[2][0], "/hotels/makkah")
    b += [f'<text x="{16 + fw / 2:.0f}" y="{y1 + 26}" font-size="14" text-anchor="middle" fill="{t["text"]}">Arabic (RTL)</text>',
          f'<text x="{16 + fw * 1.5 + 14:.0f}" y="{y1 + 26}" font-size="14" text-anchor="middle" fill="{t["text"]}">Makkah hotels</text>']
    H = y1 + 44
    return svg(MW, H, "\n".join(b), css, t, "\n".join(defs), title="Diar Al Manasik live site screenshots")


def crm(mode):
    t = THEMES[mode]
    dark = mode == "dark"
    page = t["bg1"] if dark else "#F4F6FA"
    side = "#1B2433" if dark else "#25324A"
    H = 640
    css = """
.mv{animation:mv 7s ease-in-out infinite}
@keyframes mv{0%,30%,100%{transform:translateX(0)}12%,18%{transform:translateX(6px)}}"""
    defs = [f'<clipPath id="win"><rect x="8" y="8" width="{MW - 16}" height="{H - 16}" rx="14"/></clipPath>']
    b = [f'<rect x="8" y="8" width="{MW - 16}" height="{H - 16}" rx="14" fill="{page}" stroke="{t["line"]}"/>', '<g clip-path="url(#win)">',
         f'<rect x="8" y="8" width="{MW - 16}" height="40" fill="{t["card2"]}"/>',
         '<circle cx="28" cy="28" r="5.5" fill="#FF5F57"/><circle cx="45" cy="28" r="5.5" fill="#FEBC2E"/><circle cx="62" cy="28" r="5.5" fill="#28C840"/>',
         f'<text x="80" y="33" font-size="13" fill="{t["muted"]}">crm.diarmanasik.cloud</text>',
         f'<rect x="8" y="48" width="{MW - 16}" height="64" fill="{side}"/>',
         f'<text x="24" y="80" font-size="20" font-weight="800" fill="#FFFFFF">Diar CRM</text>',
         f'<text x="24" y="100" font-size="12" fill="#9AA7BD">EspoCRM · by J. Servo</text>',
         f'<rect x="{MW - 196}" y="66" width="172" height="28" rx="14" fill="{t["c2"]}" fill-opacity=".2" stroke="{t["c2"]}" stroke-opacity=".7"/>',
         f'<text x="{MW - 110}" y="85" font-size="11" font-weight="700" letter-spacing="1" text-anchor="middle" fill="#FFFFFF">MOCKUP · DEMO DATA</text>',
         f'<text x="24" y="148" font-size="22" font-weight="800" fill="{t["title"]}">Opportunities</text>']
    kw = (MW - 48 - 12) / 2
    for k, (lab, val) in enumerate(CRM_KPIS):
        x, y = 24 + (k % 2) * (kw + 12), 166 + (k // 2) * 78
        b += [f'<rect x="{x:.0f}" y="{y}" width="{kw:.0f}" height="66" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>',
              f'<text x="{x + 16:.0f}" y="{y + 26}" font-size="14" fill="{t["muted"]}">{lab}</text>',
              f'<text x="{x + 16:.0f}" y="{y + 54}" font-size="22" font-weight="800" fill="{t["c1"] if k % 2 == 0 else t["c2"]}">{val}</text>']
    cw = kw
    for k, (stage, cards) in enumerate([CRM_STAGES[0], CRM_STAGES[3]]):
        x = 24 + k * (cw + 12)
        col = t["ok"] if stage == "Closed Won" else t["c1"]
        b += [f'<rect x="{x:.0f}" y="332" width="{cw:.0f}" height="280" rx="12" fill="{t["card2"]}" stroke="{t["line"]}"/>',
              f'<rect x="{x:.0f}" y="332" width="{cw:.0f}" height="5" rx="2.5" fill="{col}"/>',
              f'<text x="{x + 14:.0f}" y="364" font-size="16" font-weight="700" fill="{t["title"]}">{stage}</text>']
        for j, (title, sub) in enumerate(cards):
            y = 382 + j * 104
            cls = ' class="mv"' if (k == 0 and j == 0) else ""
            b += [f'<g{cls}><rect x="{x + 10:.0f}" y="{y}" width="{cw - 20:.0f}" height="90" rx="10" fill="{t["card"]}" stroke="{t["line"]}"/>',
                  f'<rect x="{x + 10:.0f}" y="{y + 14}" width="4" height="62" rx="2" fill="{col}"/>',
                  f'<text x="{x + 24:.0f}" y="{y + 36}" font-size="16" font-weight="700" fill="{t["title"]}">{title}</text>',
                  f'<text x="{x + 24:.0f}" y="{y + 62}" font-size="13" fill="{t["muted"]}">{sub}</text></g>']
    b.append('</g>')
    return svg(MW, H, "\n".join(b), css, t, "\n".join(defs), title="Diar CRM illustrative mockup with demo data")


def claude(mode):
    t = THEMES[mode]
    cc = CLAUDE[mode]
    spark = "M12 2l2.2 6.8L21 11l-6.8 2.2L12 20l-2.2-6.8L3 11l6.8-2.2z"
    css = CHIP_CSS + """
.spark{transform-box:fill-box;transform-origin:center;animation:spark 6s ease-in-out infinite}
@keyframes spark{0%,100%{transform:rotate(0) scale(1)}12%{transform:rotate(45deg) scale(1.15)}24%{transform:rotate(90deg) scale(1)}}"""
    b = ['<g class="inx">',
         f'<g transform="translate(22 30)"><g class="spark"><path d="{spark}" transform="scale(1.2)" fill="{cc}"/></g></g>',
         f'<text x="60" y="52" font-size="13" font-weight="600" letter-spacing="3" fill="{t["c1"]}">AI-ASSISTED ENGINEERING</text>',
         f'<text x="22" y="110" font-size="40" font-weight="800" fill="{t["title"]}">Shipping with</text>',
         f'<text x="22" y="156" font-size="40" font-weight="800" fill="{cc}">Claude Code</text>',
         f'<text x="24" y="192" font-size="17" fill="{t["text"]}">AI pair programmer in my terminal for</text>',
         f'<text x="24" y="216" font-size="17" fill="{t["text"]}">C# and ASP.NET Core code and tests</text>',
         '</g>']
    chips, y = chips_rows([f"{n} {l}" for n, l in STEPS], t, 236, fs=15)
    b += chips
    tx, ty, tw = 16, y + 8, MW - 32
    lines = [
        [("✻ ", cc), ("Claude Code", t["title"])],
        [("> ", cc), ("move order logic into CQRS", t["text"])],
        [("  ", cc), ("handlers + xUnit tests", t["text"])],
        [("● ", t["c1"]), ("Edit  ", t["muted"]), ("CreateOrderHandler.cs", t["text"])],
        [("● ", t["c2"]), ("Write ", t["muted"]), ("CreateOrderTests.cs", t["text"])],
        [("● ", t["ok"]), ("Bash  ", t["muted"]), ("dotnet test", t["text"])],
        [("  ✔ ", t["ok"]), ("tests green", t["ok"])],
        [("> ", cc), ("review the diff", t["text"])],
    ]
    th = 46 + len(lines) * 27 + 16
    b += [f'<g class="in"{delay(.2)}>',
          f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/>',
          f'<circle cx="{tx + 20}" cy="{ty + 20}" r="5.5" fill="#FF5F57"/><circle cx="{tx + 37}" cy="{ty + 20}" r="5.5" fill="#FEBC2E"/><circle cx="{tx + 54}" cy="{ty + 20}" r="5.5" fill="#28C840"/>',
          f'<text x="{tx + tw - 14}" y="{ty + 25}" font-size="11" font-weight="700" letter-spacing="1.4" text-anchor="end" fill="{t["muted"]}">ILLUSTRATIVE</text>',
          f'<line x1="{tx}" y1="{ty + 40}" x2="{tx + tw}" y2="{ty + 40}" stroke="{t["line"]}"/>']
    for i, segs in enumerate(lines):
        yy = ty + 70 + i * 27
        spans = "".join(f'<tspan fill="{c}">{e(s)}</tspan>' for s, c in segs)
        b.append(f'<text class="mono" x="{tx + 18}" y="{yy}" font-size="15" xml:space="preserve">{spans}</text>')
    last = ty + 70 + (len(lines) - 1) * 27
    chars = sum(len(s) for s, _ in lines[-1])
    b += [f'<rect class="caret" x="{tx + 18 + chars * 15 * CHAR_W + 5:.0f}" y="{last - 14}" width="9" height="18" fill="{cc}"/>', '</g>']
    H = ty + th + 20
    defs, back = backdrop(MW, H, t)
    return svg(MW, H, back + "\n" + "\n".join(b), css, t, defs, mono=True,
               title="AI-assisted engineering with Claude Code for C# and ASP.NET Core code and tests")


def project(mode, i, slug, icon_name, title, desc, chips):
    t = THEMES[mode]
    glyph = ICONS[icon_name][0]
    css = ICON_CSS.replace("infinite}", f"infinite;animation-delay:{i * .55:.2f}s}}")
    b = [f'<rect x="1" y="1" width="{MW - 2}" height="198" rx="18" fill="{t["card"]}" stroke="{t["line"]}"/>',
         f'<rect class="edge"{delay(-i * 1.5)} x="1.5" y="1.5" width="{MW - 3}" height="197" rx="17.5" fill="none" stroke="url(#accd)" stroke-width="2" pathLength="100"/>',
         f'<rect x="20" y="20" width="60" height="60" rx="16" fill="{t["c1"]}" fill-opacity=".12"/>',
         f'<rect class="tile" x="20.5" y="20.5" width="59" height="59" rx="15.5" fill="none" stroke="url(#accd)" stroke-width="1.6"/>',
         f'<g transform="translate(32 32) scale(1.5)" fill="none" stroke="{t["c1"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>',
         f'<text x="98" y="48" font-size="25" font-weight="800" fill="{t["title"]}">{e(title)}</text>',
         *[f'<text x="98" y="{74 + k * 20}" font-size="15" fill="{t["muted"]}">{e(ln)}</text>' for k, ln in enumerate(wrap(desc, 30))],
         f'<path d="M{MW - 36} 34 l10 -10 M{MW - 33} 24 h7 v7" fill="none" stroke="{t["c1"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>']
    rows, _ = chips_rows(chips, t, 118, x0=20, fs=15, h=32, maxw=MW - 20, cls="c")
    b += rows
    return svg(MW, 200, "\n".join(b), css, t, title=f"{title}: {desc}")


def footer(mode):
    t = THEMES[mode]
    H = 200
    css = """
.w1{animation:wv 10s linear infinite}.w2{animation:wv 15s linear infinite reverse}
@keyframes wv{to{transform:translateX(-480px)}}"""
    wave = lambda y, a: f"M0 {y} " + " ".join(f"Q{60 + 240 * k} {y - a} {120 + 240 * k} {y} T{240 + 240 * k} {y}" for k in range(4)) + f" V{H} H0Z"  # noqa: E731
    b = [f'<text x="{MW / 2}" y="34" font-size="13" font-weight="800" letter-spacing="6" text-anchor="middle" fill="url(#acc)">MOHAMED NOWAR</text>',
         f'<text x="{MW / 2}" y="76" font-size="21" font-weight="600" text-anchor="middle" fill="{t["title"]}">Building backend systems as</text>',
         f'<text x="{MW / 2}" y="104" font-size="21" font-weight="600" text-anchor="middle" fill="{t["title"]}"><tspan fill="url(#acc)">clean</tspan> as the code behind them.</text>',
         f'<g class="w2" opacity=".4"><path fill="url(#acc)" d="{wave(160, 22)}"/></g>',
         f'<g class="w1" opacity=".9"><path fill="url(#acc)" d="{wave(178, 14)}"/></g>']
    return svg(MW, H, "\n".join(b), css, t, title="Building backend systems as clean as the code behind them.")


def main():
    for mode in THEMES:
        for name, fn in [("banner", banner), ("stats", stats), ("jservo", jservo), ("gallery", gallery),
                         ("crm", crm), ("claude", claude), ("footer", footer)]:
            write(os.path.join(OUT, f"{name}-{mode}.svg"), fn(mode))
        write(os.path.join(OUT, f"about-{mode}.svg"), about(mode, mobile=True))
        for i, (slug, icon_name, title, desc, chips) in enumerate(PROJECTS):
            write(os.path.join(OUT, f"project-{slug}-{mode}.svg"), project(mode, i, slug, icon_name, title, desc, chips))
        # Wikidata as a standard-size badge on phones
        slug, eyebrow, name, mark, _note = TRUST[-1]
        write(os.path.join(OUT, f"trust-{slug}-{mode}.svg"), trust(mode, 6, "ENTITY Q141189697", name, mark))
    print("wrote", len(os.listdir(OUT)), "mobile SVGs")


if __name__ == "__main__":
    main()
