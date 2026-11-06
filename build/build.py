"""Builds the SVGs for Kerem Kaya's GitHub profile README (light + dark).

Run:  python3 build.py ../assets      (needs: pip install fonttools)
Edit the text in hero() / timeline() and run again.

GitHub shows README images in a sandbox that cannot load web fonts, so each
font is cut down to the characters used and embedded in the SVG.
"""
import base64, io, re, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "light": dict(ink="#14203A", muted="#5B6679", rule="#D4DAE4", accent="#2A4596",
                  bar="#2A4596", future="#2A4596",
                  l0="#1B2B66", l1="#26408F", l2="#3557B0", l3="#5A7CCF", l4="#A9BEEC",
                  t0="#FFFFFF", t1="#FFFFFF", t2="#FFFFFF", t3="#FFFFFF", t4="#14203A"),
    "dark":  dict(ink="#E7ECF5", muted="#98A3B8", rule="#2A3346", accent="#8FA9EA",
                  bar="#7593E0", future="#7593E0",
                  l0="#22367C", l1="#2E4CA3", l2="#4467C2", l3="#6D8DDB", l4="#B4C6F0",
                  t0="#FFFFFF", t1="#FFFFFF", t2="#FFFFFF", t3="#0D1117", t4="#0D1117"),
}

FONTS = {
    "Cond": "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheroscn-bold.otf",
    "Int4": "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    "Int5": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
}

STYLE = """
.cond{font-family:Cond;font-weight:700}
.i4{font-family:Int4} .i5{font-family:Int5}
.ink{fill:{ink}} .muted{fill:{muted}} .acc{fill:{accent}}
"""

# ------------------------------------------------------------------ hero
# Top to bottom: the layers my projects sit on, from gameplay down to hardware.
LAYERS = [
    ("Gameplay and 3D", "FTactics"),
    ("Mobile apps", "Real Estate CRM, AI Sleep Assistant"),
    ("Data", "Library Borrowing System"),
    ("Systems", "Linux concurrency, graph algorithms"),
    ("Hardware", "UART receiver in Verilog"),
]

def hero():
    x0, w, h, gap, top = 540, 360, 38, 6, 30
    n = len(LAYERS)
    blocks, kf = [], []
    for i, (name, proj) in enumerate(LAYERS):
        y = top + i * (h + gap)
        shade = n - 1 - i            # hardware is the darkest
        order = n - 1 - i            # hardware appears first
        blocks.append(
            f'<g class="ly" style="animation-delay:{0.15 + order*0.12:.2f}s">'
            f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" rx="5" fill="{{l{shade}}}"/>'
            f'<text x="{x0+14}" y="{y+24}" class="i5" font-size="14" fill="{{t{shade}}}">{name}</text>'
            f'<text x="{x0+w-14}" y="{y+24}" text-anchor="end" class="i4" font-size="12.5" '
            f'fill="{{t{shade}}}" fill-opacity=".85">{proj}</text></g>')
    style = ("<style>.ly{animation:rise .5s cubic-bezier(.2,.8,.2,1) both}"
             "@keyframes rise{from{transform:translateY(14px);opacity:0}to{transform:none;opacity:1}}"
             "@media (prefers-reduced-motion:reduce){.ly{animation:none}}</style>")
    cap_y = top + n * (h + gap) + 14
    return 900, 290, f"""
{style}
<text x="0" y="90" class="cond ink" font-size="70" letter-spacing="-.5">Kerem Kaya</text>
<text x="2" y="130" class="i4 muted" font-size="17">Computer Science and Engineering, Sabancı University</text>
<text x="2" y="154" class="i4 muted" font-size="17">Expected to graduate in January 2028</text>
<text x="2" y="214" class="i4 ink" font-size="20">I write software at every layer, from a UART</text>
<text x="2" y="242" class="i4 ink" font-size="20">receiver in Verilog to a 3D football game.</text>
{''.join(blocks)}
<text x="{x0}" y="{cap_y}" class="i4 muted" font-size="13">Where my projects sit, from hardware up</text>
"""

# ------------------------------------------------------------------ timeline
NOW = 2026 + 10.2 / 12           # early November 2026

def timeline():
    ax0, ax1, y0, y1 = 130, 890, 2023.0, 2028.2
    X = lambda t: ax0 + (t - y0) / (y1 - y0) * (ax1 - ax0)
    p = []
    # lanes
    p.append('<text x="0" y="96" class="i5 muted" font-size="14">Education</text>')
    p.append('<text x="0" y="186" class="i5 muted" font-size="14">Work</text>')
    # Sabanci
    s0, s1 = X(2023 + 8 / 12), X(2028 + 0.5 / 12)
    p.append(f'<text x="{s0}" y="76" class="i5 ink" font-size="15">BSc Computer Science and Engineering, Sabancı University</text>')
    p.append(f'<rect x="{s0}" y="84" width="{X(NOW)-s0}" height="14" rx="3" fill="{{bar}}"/>')
    p.append(f'<rect x="{X(NOW)+.75}" y="84.75" width="{s1-X(NOW)-1.5}" height="12.5" rx="3" fill="none" '
             f'stroke="{{future}}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    p.append(f'<text x="{s0}" y="118" class="i4 muted" font-size="13.5">100% merit scholarship, ranked 224th nationally in the 2023 YKS</text>')
    # work
    for a, b, label in [(2023 + 10 / 12, 2025 + 1 / 12, "Sales Associate, Zey Optik"),
                        (2026 + 1 / 12, NOW, "Intern, Toastmasters International")]:
        p.append(f'<text x="{X(a)}" y="166" class="i5 ink" font-size="15">{label}</text>')
        p.append(f'<rect x="{X(a)}" y="174" width="{X(b)-X(a)}" height="14" rx="3" fill="{{bar}}"/>')
    # axis
    p.append(f'<line x1="{ax0}" y1="214.5" x2="{ax1}" y2="214.5" stroke="{{rule}}"/>')
    for yr in range(2023, 2029):
        x = X(yr)
        p.append(f'<line x1="{x}" y1="210" x2="{x}" y2="219" stroke="{{rule}}"/>')
        p.append(f'<text x="{x}" y="238" text-anchor="middle" class="i4 muted" font-size="13">{yr}</text>')
    xn = X(NOW)
    p.append(f'<line x1="{xn}" y1="172" x2="{xn}" y2="214" stroke="{{ink}}" stroke-width="1.25" stroke-dasharray="2 3"/>')
    p.append(f'<text x="{xn+6}" y="206" class="i5 ink" font-size="12.5">Now</text>')
    p.append('<text x="0" y="274" class="i4 muted" font-size="13.5">Alongside Sabancı, I study Business Administration at Istanbul University\'s open education faculty.</text>')
    return 900, 236, '<g transform="translate(0,-48)">' + "\n".join(p) + "</g>"

# ------------------------------------------------------------------ fonts
def used_chars(svg):
    return set(re.sub(r"<[^>]+>", " ", svg)) | set("0123456789-.,")

def embed(chars):
    css = []
    for name, path in FONTS.items():
        f = TTFont(path)
        opts = subset.Options()
        opts.layout_features = ["kern", "liga", "calt"]
        opts.name_IDs = []
        s = subset.Subsetter(opts)
        s.populate(text="".join(chars))
        s.subset(f)
        buf = io.BytesIO(); f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:{name};src:url(data:font/otf;base64,{b64}) format('opentype')}}")
    return "".join(css)

def main():
    for key, fn in {"hero": hero, "timeline": timeline}.items():
        w, h, body = fn()
        fonts = embed(used_chars(body))
        for theme, t in THEMES.items():
            style, b = STYLE, body
            for k, v in t.items():
                style = style.replace("{" + k + "}", v)
                b = b.replace("{" + k + "}", v)
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                   f'viewBox="0 0 {w} {h}" role="img"><style>{fonts}{style}</style>{b}</svg>')
            (OUT / f"{key}-{theme}.svg").write_text(svg, encoding="utf-8")
            print(key, theme, f"{len(svg)/1024:.0f} KB")

main()
