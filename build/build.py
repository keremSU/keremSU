"""Builds the header SVG for Kerem Kaya's GitHub profile README (light + dark).

Run:  python3 build.py ../assets      (needs: pip install fonttools)
Edit the text in header() and run again.

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
    "light": dict(ink="#14203A", muted="#5B6679", accent="#2A4596"),
    "dark":  dict(ink="#E7ECF5", muted="#98A3B8", accent="#8FA9EA"),
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

# Right-hand column: what a recruiter checks first.
FACTS = [
    ("Graduating", "January 2028 (expected)"),
    ("Work authorization", "EU citizen, no visa needed in the EU"),
    ("Languages", "Turkish, English C1, German A2"),
]

SUMMARY = [
    "Computer Science and Engineering student who",
    "builds software end to end: C# and Unity, C and",
    "C++ on Linux, SQL and NoSQL databases, Flutter.",
]

def header():
    p = [
        '<text x="0" y="74" class="cond ink" font-size="70" letter-spacing="-.5">Kerem Kaya</text>',
        '<text x="2" y="112" class="i5 acc" font-size="17">Sabancı University, Istanbul</text>',
    ]
    for i, line in enumerate(SUMMARY):
        p.append(f'<text x="2" y="{160 + i*28}" class="i4 ink" font-size="19">{line}</text>')
    p.append('<rect x="596" y="24" width="3" height="200" rx="1.5" fill="{accent}"/>')
    for i, (label, value) in enumerate(FACTS):
        y = 52 + i * 68
        p.append(f'<text x="624" y="{y}" class="i4 muted" font-size="13">{label}</text>')
        p.append(f'<text x="624" y="{y+24}" class="i5 ink" font-size="15">{value}</text>')
    return 900, 248, "\n".join(p)

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
    w, h, body = header()
    fonts = embed(used_chars(body))
    for theme, t in THEMES.items():
        style, b = STYLE, body
        for k, v in t.items():
            style = style.replace("{" + k + "}", v)
            b = b.replace("{" + k + "}", v)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
               f'viewBox="0 0 {w} {h}" role="img"><style>{fonts}{style}</style>{b}</svg>')
        (OUT / f"header-{theme}.svg").write_text(svg, encoding="utf-8")
        print("header", theme, f"{len(svg)/1024:.0f} KB")

main()
