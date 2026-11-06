"""Builds the SVGs for Kerem Kaya's GitHub profile README (light + dark).

Run:  python3 build.py ../assets
Edit the text in hero() and card_ftactics(), then run again.

GitHub shows README images in a sandbox that cannot load web fonts, so every
font is cut down to the characters actually used and embedded in the SVG.
Needs: pip install fonttools
"""
import base64, io, re, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
OUT.mkdir(parents=True, exist_ok=True)

# Colors taken from FTactics' own interface: pitch green and kit amber.
THEMES = {
    "light": dict(ink="#1A2420", muted="#5D6964", rule="#D5DCD8", accent="#A8681A",
                  pitch="#2F6A49", line="#FFFFFF", dot="#F2B35C", dotring="#1A2420",
                  chip="#F6EEE2"),
    "dark":  dict(ink="#E9EDEB", muted="#98A49F", rule="#2B3531", accent="#E8AE5C",
                  pitch="#24533A", line="#FFFFFF", dot="#F2B35C", dotring="#0D1117",
                  chip="#2A2418"),
}

FONTS = {  # family name used in CSS -> font file
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
# 5-3-2, attacking to the right. (x, y) are fractions of the pitch.
FORMATION = [
    ("GK", .07, .50),
    ("WB", .26, .10), ("CD", .22, .30), ("CD", .20, .50), ("CD", .22, .70), ("WB", .26, .90),
    ("CM", .47, .26), ("CM", .44, .50), ("CM", .47, .74),
    ("ST", .72, .40), ("ST", .72, .60),
]

def hero():
    px, py, pw, ph = 560, 34, 340, 214          # pitch box
    L = 'stroke="{line}" stroke-opacity=".55" stroke-width="1.5" fill="none"'
    pitch = [
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="{{pitch}}"/>',
        f'<rect x="{px+10}" y="{py+10}" width="{pw-20}" height="{ph-20}" {L}/>',
        f'<line x1="{px+pw/2}" y1="{py+10}" x2="{px+pw/2}" y2="{py+ph-10}" {L}/>',
        f'<circle cx="{px+pw/2}" cy="{py+ph/2}" r="28" {L}/>',
        f'<rect x="{px+10}" y="{py+ph/2-48}" width="46" height="96" {L}/>',
        f'<rect x="{px+pw-56}" y="{py+ph/2-48}" width="46" height="96" {L}/>',
        f'<rect x="{px+10}" y="{py+ph/2-20}" width="16" height="40" {L}/>',
        f'<rect x="{px+pw-26}" y="{py+ph/2-20}" width="16" height="40" {L}/>',
    ]
    # Players start bunched at the centre spot and run to their positions once.
    sx, sy = px + pw / 2, py + ph / 2
    keyframes, players = [], []
    for i, (role, fx, fy) in enumerate(FORMATION):
        x = px + 10 + fx * (pw - 20)
        y = py + 10 + fy * (ph - 20)
        dx, dy = sx - x, sy - y
        keyframes.append(f"@keyframes p{i}{{from{{transform:translate({dx:.1f}px,{dy:.1f}px)}}"
                         f"to{{transform:translate(0,0)}}}}")
        players.append(
            f'<g class="pl" style="animation-name:p{i};animation-delay:{0.15 + i*0.05:.2f}s">'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{{dot}}" stroke="{{dotring}}" stroke-width="1.5"/>'
            f'<text x="{x:.1f}" y="{y+3.6:.1f}" text-anchor="middle" class="i5" font-size="9.5" '
            f'fill="#1A2420">{role}</text></g>')
    style = ("<style>.pl{animation-duration:.9s;animation-timing-function:cubic-bezier(.2,.8,.2,1);"
             "animation-fill-mode:both}" + "".join(keyframes) +
             "@media (prefers-reduced-motion:reduce){.pl{animation:none}}</style>")
    return 900, 280, f"""
{style}
<text x="0" y="92" class="cond ink" font-size="70" letter-spacing="-.5">Kerem Kaya</text>
<text x="2" y="132" class="i4 muted" font-size="17">Computer Science, Sabancı University</text>
<text x="2" y="196" class="i4 ink" font-size="20">I'm building a football management game</text>
<text x="2" y="224" class="i4 ink" font-size="20">for Android, on my own, in Unity and C#.</text>
{''.join(pitch)}
{''.join(players)}
<text x="{px}" y="272" class="i4 muted" font-size="13">5-3-2, as set up on the FTactics tactics screen</text>
"""

# ------------------------------------------------------------------ FTactics card
SYSTEMS = [
    ("Match simulation", "passing, shooting, movement and possession"),
    ("Tactics", "formations, roles and instructions that change play"),
    ("Career", "seasons, transfers, contracts, finances, fatigue"),
    ("3D presentation", "animated players, broadcast camera, stadium"),
    ("Save and load", "multi-season careers, older saves still open"),
    ("Android builds", "installable builds, device loading issues fixed"),
]

def card_ftactics():
    rows = []
    for i, (title, gloss) in enumerate(SYSTEMS):
        col, row = i % 2, i // 2
        x = col * 460
        y = 136 + row * 54
        rows.append(f'<rect x="{x}" y="{y-14}" width="4" height="34" rx="2" fill="{{accent}}"/>')
        rows.append(f'<text x="{x+18}" y="{y+1}" class="i5 ink" font-size="15">{title}</text>')
        rows.append(f'<text x="{x+18}" y="{y+20}" class="i4 muted" font-size="13.5">{gloss}</text>')
    return 900, 300, f"""
<line x1="0" y1="0.5" x2="900" y2="0.5" stroke="{{rule}}"/>
<text x="0" y="54" class="cond ink" font-size="38" letter-spacing="-.2">FTactics</text>
<rect x="142.5" y="28.5" width="122" height="28" rx="14" fill="{{chip}}" stroke="{{accent}}"/>
<text x="203.5" y="47" text-anchor="middle" class="i5 acc" font-size="13">In development</text>
<text x="1" y="88" class="i4 muted" font-size="16.5">Football management meets a real-time 3D match. Solo project, Unity and C#, for Android.</text>
{''.join(rows)}
"""

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
    for key, fn in {"hero": hero, "ftactics": card_ftactics}.items():
        w, h, body = fn()
        fonts = embed(used_chars(body))
        for theme, t in THEMES.items():
            style, b = STYLE, body
            for k, v in t.items():
                style = style.replace("{" + k + "}", v)
                b = b.replace("{" + k + "}", v)
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                   f'viewBox="0 0 {w} {h}" role="img"><style>{fonts}{style}</style>{b}</svg>')
            p = OUT / f"{key}-{theme}.svg"
            p.write_text(svg, encoding="utf-8")
            print(p, f"{len(svg)/1024:.0f} KB")

main()
