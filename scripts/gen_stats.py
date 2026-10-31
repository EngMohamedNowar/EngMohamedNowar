"""Self-hosted, animated GitHub stats cards for the profile README.

Usage:  GH_TOKEN=... python scripts/gen_stats.py OUT_DIR [login]
Writes: stats-overview.svg, stats-activity.svg, stats-languages.svg
Stdlib only, so it runs on a bare GitHub Actions runner.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist"
LOGIN = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("GH_LOGIN", "EngMohamedNowar")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

ACC, ACC2 = "#36BCF7", "#A78BFA"
BG1, BG2, CARD, LINE = "#0D1117", "#0B1B2B", "#161B22", "#30363D"
FG, SUB, OK = "#E6EDF3", "#8B949E", "#4ADE80"
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    pullRequests{totalCount}
    repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){
      totalCount
      nodes{ stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}} }
    }
    contributionsCollection{
      totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions
      contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
    }
  }
}"""


def fetch():
    if not TOKEN:
        sys.exit("GH_TOKEN is not set")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(json.dumps(data["errors"]))
    return data["data"]["user"]


def w(name, s):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def odometer(uid, value, x, y, fs, fill, delay=0.0, anchor_end=False):
    """Rolling-digit counter. Base transforms hold the final value, so static renderers show it."""
    s = f"{value:,}"
    cw, h = fs * 0.62, fs * 1.25
    width = sum(cw if ch.isdigit() else fs * 0.3 for ch in s)
    x0 = x - width if anchor_end else x
    out = f'<clipPath id="{uid}"><rect x="{x0}" y="{y-fs}" width="{width+4:.1f}" height="{h:.1f}"/></clipPath><g clip-path="url(#{uid})" font-size="{fs}" font-weight="800" fill="{fill}">'
    cx = x0
    digits = [c for c in s if c.isdigit()]
    di = 0
    for ch in s:
        if not ch.isdigit():
            out += f'<text x="{cx:.1f}" y="{y}">{ch}</text>'
            cx += fs * 0.3
            continue
        d = int(ch)
        idx = 10 + d
        stack = "".join(f'<text x="{cx:.1f}" y="{y + k*h:.1f}">{k % 10}</text>' for k in range(20))
        roll = 1.4 + (len(digits) - di) * 0.25
        dur = roll + delay
        k = delay / dur
        out += (f'<g transform="translate(0 {-idx*h:.1f})">{stack}'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 {-idx*h:.1f}" '
                f'dur="{dur:.2f}s" begin="0s" fill="freeze" calcMode="spline" keyTimes="0;{k:.3f};1" keySplines="0 0 1 1;.2 .7 .2 1"/></g>')
        cx += cw
        di += 1
    return out + "</g>"


def frame(wd, ht, uid, title, subtitle, body, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{wd}" height="{ht}" viewBox="0 0 {wd} {ht}">
<style>
  text{{font-family:{FONT};font-variant-numeric:tabular-nums}}
  .edge{{stroke-dasharray:12 88;animation:edge 8s linear infinite}}
  .in{{animation:in .8s cubic-bezier(.2,.7,.2,1) both}}
  @keyframes edge{{to{{stroke-dashoffset:-100}}}}
  @keyframes in{{from{{transform:translateY(12px)}}to{{transform:none}}}}
  {extra_css}
  {RM}
</style>
<defs>
  <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
  <pattern id="{uid}grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#FFFFFF" stroke-opacity=".035"/></pattern>
  <linearGradient id="{uid}acc" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient>
</defs>
<rect x="1" y="1" width="{wd-2}" height="{ht-2}" rx="16" fill="url(#{uid}bg)"/>
<rect x="1" y="1" width="{wd-2}" height="{ht-2}" rx="16" fill="url(#{uid}grid)"/>
<rect x="1" y="1" width="{wd-2}" height="{ht-2}" rx="16" fill="none" stroke="{LINE}"/>
<rect class="edge" x="1" y="1" width="{wd-2}" height="{ht-2}" rx="16" fill="none" stroke="url(#{uid}acc)" stroke-width="2" pathLength="100"/>
<rect x="32" y="30" width="4" height="26" rx="2" fill="{ACC}"/>
<text x="46" y="50" font-size="20" font-weight="700" fill="{FG}">{title}</text>
<text x="{wd-32}" y="50" text-anchor="end" font-size="13" fill="{SUB}">{subtitle}</text>
{body}
</svg>
'''


ICONS = {  # 24px stroke icons
    "flame": "M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-3 2-4 2-7 1 1 2 2 3 2 0-2 0-3 0-5z",
    "commit": "M3 12h5M16 12h5M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8",
    "pr": "M6 3v12M6 15a3 3 0 1 0 0 6a3 3 0 1 0 0-6M18 21V9a3 3 0 0 0-3-3h-4M13 3l-2 3 2 3",
    "repo": "M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3zM5 17a3 3 0 0 1 3-3h11",
    "cal": "M4 6h16v14H4zM4 10h16M8 3v5M16 3v5",
    "star": "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z",
}


def overview(u, days):
    cc = u["contributionsCollection"]
    active = sum(1 for d in days if d["contributionCount"] > 0)
    best = max((d["contributionCount"] for d in days), default=0)
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    tiles = [
        ("flame", "Contributions", cc["contributionCalendar"]["totalContributions"], "last 12 months"),
        ("commit", "Commits", cc["totalCommitContributions"], "last 12 months"),
        ("pr", "Pull Requests", u["pullRequests"]["totalCount"], "all time"),
        ("repo", "Public Repos", u["repositories"]["totalCount"], "original, non-fork"),
        ("cal", "Active Days", active, "last 12 months"),
        ("star", "Best Day", best, "contributions"),
    ]
    W, cols = 1160, 3
    tw, th, gx, gy, x0, y0 = 352, 112, 20, 18, 32, 78
    body = ""
    for i, (ic, label, val, sub) in enumerate(tiles):
        c, r = i % cols, i // cols
        x, y = x0 + c * (tw + gx), y0 + r * (th + gy)
        d = 0.15 * i
        body += f'''<g class="in" style="animation-delay:{d:.2f}s">
<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{CARD}" stroke="{LINE}"/>
<rect class="hl" style="animation-delay:{i*0.7:.1f}s" x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="none" stroke="{ACC}"/>
<circle cx="{x+44}" cy="{y+th/2}" r="26" fill="{ACC}" fill-opacity=".12" stroke="{ACC}" stroke-opacity=".4"/>
<circle class="halo" style="animation-delay:{i*0.4:.1f}s" cx="{x+44}" cy="{y+th/2}" r="26" fill="none" stroke="{ACC}"/>
<g transform="translate({x+32} {y+th/2-12})" fill="none" stroke="{ACC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[ic]}"/></g>
<text x="{x+88}" y="{y+40}" font-size="14" font-weight="600" fill="{SUB}">{label}</text>
{odometer(f"ov{i}", val, x+88, y+82, 38, FG, delay=0.3+d)}
<text x="{x+tw-18}" y="{y+82}" text-anchor="end" font-size="12" fill="{SUB}">{sub}</text>
</g>'''
    H = y0 + 2 * th + gy + 32
    css = (".hl{stroke-opacity:0;animation:hl 4.2s ease-in-out infinite}"
           "@keyframes hl{0%,100%{stroke-opacity:0}15%{stroke-opacity:.9}35%{stroke-opacity:0}}"
           ".halo{transform-box:fill-box;transform-origin:center;stroke-opacity:0;animation:halo 2.8s ease-out infinite}"
           "@keyframes halo{0%{stroke-opacity:.7;transform:scale(1)}100%{stroke-opacity:0;transform:scale(1.5)}}")
    return frame(W, H, "so", "GitHub Stats", f"@{LOGIN} · updated {dt.date.today():%d %b %Y}", body, css)


def activity(days):
    days = days[-90:]
    totals = [d["contributionCount"] for d in days]
    W, H = 1160, 300
    left, right, top, bottom = 56, 32, 84, 250
    cw = (W - left - right) / len(totals)
    mx = max(totals + [1])
    body = ""
    for k in range(5):
        v = round(mx * k / 4)
        y = bottom - (bottom - top) * k / 4
        body += f'<line x1="{left}" x2="{W-right}" y1="{y:.1f}" y2="{y:.1f}" stroke="#FFFFFF" stroke-opacity=".06"/>'
        body += f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="{SUB}">{v}</text>'
    pts = []
    for i, (t, d) in enumerate(zip(totals, days)):
        x = left + i * cw
        hgt = (bottom - top) * t / mx
        y = bottom - hgt
        pts.append((x + cw / 2, y))
        if t:
            body += (f'<rect class="bar" style="animation-delay:{0.2+i*0.012:.2f}s" x="{x+cw*0.15:.1f}" y="{y:.1f}" '
                     f'width="{cw*0.7:.1f}" height="{hgt:.1f}" rx="2" fill="url(#saBar)"/>')
        else:
            body += f'<rect x="{x+cw*0.15:.1f}" y="{bottom-2}" width="{cw*0.7:.1f}" height="2" rx="1" fill="#FFFFFF" fill-opacity=".08"/>'
        dd = dt.date.fromisoformat(d["date"])
        if dd.day in (1, 15):
            body += f'<text x="{x+cw/2:.1f}" y="{bottom+22}" text-anchor="middle" font-size="11" fill="{SUB}">{dd:%d %b}</text>'
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{pts[-1][0]:.1f} {bottom} L{pts[0][0]:.1f} {bottom} Z"
    lx, ly = pts[-1]
    body = (f'<defs><linearGradient id="saBar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{ACC}" stop-opacity=".25"/><stop offset="1" stop-color="{ACC}" stop-opacity=".85"/></linearGradient>'
            f'<linearGradient id="saArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC2}" stop-opacity=".25"/><stop offset="1" stop-color="{ACC2}" stop-opacity="0"/></linearGradient></defs>'
            + body +
            f'<path d="{area}" fill="url(#saArea)"/>'
            f'<path class="ln" d="{line}" fill="none" stroke="{ACC2}" stroke-width="2.2" stroke-linejoin="round" pathLength="100"/>'
            f'<circle r="4" fill="{FG}"><animateMotion dur="9s" repeatCount="indefinite" path="{line}"/></circle>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="{OK}"/><circle class="ping" cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="none" stroke="{OK}" stroke-width="2"/>')
    css = (".bar{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}"
           "@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
           ".ln{stroke-dasharray:100;animation:draw 2.4s .6s ease-out both}"
           "@keyframes draw{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}"
           ".ping{transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}"
           "@keyframes ping{from{opacity:1;transform:scale(1)}to{opacity:0;transform:scale(3)}}"
           "@media (prefers-reduced-motion: reduce){.bar{transform:none}.ln{stroke-dashoffset:0}}")
    return frame(W, H, "sa", "Contribution Activity", f"{sum(totals)} contributions in the last 90 days · daily", body, css)


def languages(u):
    agg = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            a = agg.setdefault(n, [0, e["node"]["color"] or SUB])
            a[0] += e["size"]
    tot = sum(v[0] for v in agg.values()) or 1
    top = sorted(agg.items(), key=lambda kv: -kv[1][0])[:6]
    W = 1160
    body = ""
    # stacked bar
    x, bx, bw, by = 32, 32, W - 64, 82
    body += f'<clipPath id="slClip"><rect x="{bx}" y="{by}" width="{bw}" height="14" rx="7"/></clipPath><g clip-path="url(#slClip)"><rect x="{bx}" y="{by}" width="{bw}" height="14" fill="{CARD}"/>'
    cx = bx
    for i, (n, (sz, col)) in enumerate(top):
        wd = bw * sz / tot
        body += f'<rect class="seg" style="animation-delay:{0.2+i*0.15:.2f}s" x="{cx:.1f}" y="{by}" width="{wd:.1f}" height="14" fill="{col}"/>'
        cx += wd
    body += "</g>"
    # rows: 2 columns x 3
    rw, y0 = (W - 64 - 40) / 2, 128
    for i, (n, (sz, col)) in enumerate(top):
        c, r = i // 3, i % 3
        x = 32 + c * (rw + 40)
        y = y0 + r * 46
        pct = 100 * sz / tot
        fw = max(rw * pct / 100, 4)
        d = 0.3 + i * 0.12
        body += f'''<g class="in" style="animation-delay:{d:.2f}s">
<circle cx="{x+7}" cy="{y+6}" r="6" fill="{col}"/>
<text x="{x+22}" y="{y+11}" font-size="15" font-weight="600" fill="{FG}">{n}</text>
<text x="{x+rw}" y="{y+11}" text-anchor="end" font-size="14" font-weight="700" fill="{ACC}">{pct:.1f}%</text>
<rect x="{x}" y="{y+20}" width="{rw:.1f}" height="8" rx="4" fill="{CARD}"/>
<clipPath id="slf{i}"><rect x="{x}" y="{y+20}" width="{fw:.1f}" height="8" rx="4"/></clipPath>
<rect class="fillbar" style="animation-delay:{d+.2:.2f}s" x="{x}" y="{y+20}" width="{fw:.1f}" height="8" rx="4" fill="{col}"/>
<g clip-path="url(#slf{i})"><rect class="shine" style="animation-delay:{i*0.5:.1f}s;--w:{fw:.0f}px" x="{x-40}" y="{y+20}" width="40" height="8" fill="#FFFFFF" fill-opacity=".45"/></g>
</g>'''
    H = y0 + 3 * 46 + 22
    css = (".seg,.fillbar{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both}"
           "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".shine{animation:shine 3.5s ease-in-out infinite}"
           "@keyframes shine{0%{opacity:1;transform:translateX(0)}60%,100%{opacity:1;transform:translateX(calc(var(--w) + 40px))}}"
           "@media (prefers-reduced-motion: reduce){.seg,.fillbar{transform:none}}")
    return frame(W, H, "sl", "Most Used Languages", f"by code size across {u['repositories']['totalCount']} public repos", body, css)


if __name__ == "__main__":
    u = fetch()
    days = [d for wk in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in wk["contributionDays"]]
    w("stats-overview.svg", overview(u, days))
    w("stats-activity.svg", activity(days))
    w("stats-languages.svg", languages(u))
    print("wrote", sorted(os.listdir(OUT)))
