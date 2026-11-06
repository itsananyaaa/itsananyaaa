#!/usr/bin/env python3
"""Generate the still plates of The Crimson Archive.

Run from anywhere: python3 scripts/generate_archive.py
Stats plates are a separate script so the GitHub Action stays small.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from svgtext import contrast_ratio, text_path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets"
DATA = ROOT / "data"

OBSIDIAN = "#080809"
NEAR = "#111014"
CRIMSON = "#8B0000"
BURGUNDY = "#4A0710"
WINE = "#30050B"
GOLD = "#C5A46D"
PARCHMENT = "#D8C8B0"
GREY = "#77717A"
PAGE = "#E6D5C0"
PAGE_SHADOW = "#CDBBA4"
INK = "#24110E"
# Derived only as a page surface and as ink on that page.
# Crimson #8B0000 and grey #77717A are never used for small text.

CINZEL = "cinzel-semibold.ttf"
CINZEL_REG = "cinzel.ttf"
ITALIC = "cormorant-italic.ttf"
MONO = "plex.ttf"
MONO_MED = "plex-medium.ttf"

MOTION_STYLE = """<style type="text/css"><![CDATA[
@media (prefers-reduced-motion: reduce) {
  .motion { display: none !important; }
}
]]></style>"""


def doc(view_w: int, view_h: int, body: str, motion: bool = False) -> str:
    style = MOTION_STYLE if motion else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" role="img">\n'
        f"{style}\n"
        f'<rect width="{view_w}" height="{view_h}" fill="{OBSIDIAN}"/>\n'
        f"{body}\n</svg>\n"
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"{path.relative_to(ROOT)}  {path.stat().st_size:7d} bytes")


def rule_svg() -> str:
    body = f"""
<line x1="80" y1="24" x2="560" y2="24" stroke="{GOLD}" stroke-width="1" opacity="0.85"/>
<path d="M640 14 L650 24 L640 34 L630 24 Z" fill="{CRIMSON}"/>
<path d="M640 18 L646 24 L640 30 L634 24 Z" fill="{GOLD}"/>
<line x1="720" y1="24" x2="1200" y2="24" stroke="{GOLD}" stroke-width="1" opacity="0.85"/>
"""
    return doc(1280, 48, body)


def _leather_filter() -> str:
    return f"""
<defs>
  <filter id="leather" x="-2%" y="-2%" width="104%" height="104%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4" result="noise"/>
    <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
    <feComponentTransfer in="mono" result="grain">
      <feFuncA type="linear" slope="0.22"/>
    </feComponentTransfer>
    <feBlend in="SourceGraphic" in2="grain" mode="multiply"/>
  </filter>
  <radialGradient id="glow" cx="50%" cy="46%" r="48%">
    <stop offset="0%" stop-color="{CRIMSON}" stop-opacity="0.55"/>
    <stop offset="55%" stop-color="{BURGUNDY}" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="{OBSIDIAN}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="page" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#F3E6D4"/>
    <stop offset="100%" stop-color="{PAGE}"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{GOLD}" stop-opacity="0.2"/>
    <stop offset="50%" stop-color="{GOLD}" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="{GOLD}" stop-opacity="0.25"/>
  </linearGradient>
</defs>
"""


def hero() -> str:
    title = text_path(CINZEL, "THE CRIMSON ARCHIVE", 640, 118, 58, PARCHMENT, "middle", 0.06)
    kicker = text_path(
        MONO_MED, "A CLASSIFIED COLLECTION", 640, 158, 15, GOLD, "middle", 0.22
    )
    left_lines = [
        (248, "FILE  /  PERSONAL"),
        (278, "ANANYA BIJU"),
        (318, "COMPUTER SCIENCE"),
        (348, "2024  —  2028"),
        (392, "IRINJALAKUDA"),
    ]
    left = []
    for y, line in left_lines:
        left.append(text_path(MONO, line, 400, y, 15, INK, "middle", 0.08))
    right_lines = [
        (300, "The world is full of things"),
        (338, "that have not yet"),
        (376, "been built."),
    ]
    right = []
    for y, line in right_lines:
        right.append(text_path(ITALIC, line, 880, y, 28, INK, "middle"))
    particles = []
    specs = [
        (180, 250, 1.4, "0s"),
        (260, 180, 1.1, "1.4s"),
        (1080, 210, 1.6, "0.6s"),
        (1160, 340, 1.2, "2s"),
        (150, 520, 1.3, "2.6s"),
        (1120, 560, 1.5, "1s"),
        (520, 160, 1.0, "3s"),
        (760, 640, 1.2, "1.8s"),
    ]
    for cx, cy, r, begin in specs:
        particles.append(
            f'<circle class="motion" cx="{cx}" cy="{cy}" r="{r}" fill="{PARCHMENT}" opacity="0.0">'
            f'<animate attributeName="opacity" values="0;0.65;0" dur="8s" begin="{begin}" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{cy};{cy - 28}" dur="8s" begin="{begin}" repeatCount="indefinite"/>'
            f"</circle>"
        )
    body = f"""
{_leather_filter()}
<ellipse cx="640" cy="430" rx="520" ry="250" fill="url(#glow)"/>
<ellipse class="motion" cx="640" cy="430" rx="420" ry="180" fill="{CRIMSON}" opacity="0.18">
  <animate attributeName="opacity" values="0.10;0.28;0.10" dur="9s" repeatCount="indefinite"/>
</ellipse>
<ellipse cx="640" cy="640" rx="340" ry="18" fill="#000000" opacity="0.45"/>
<g filter="url(#leather)">
  <rect x="168" y="196" width="450" height="430" rx="8" fill="{WINE}"/>
  <rect x="662" y="196" width="450" height="430" rx="8" fill="{WINE}"/>
</g>
<rect x="186" y="214" width="414" height="394" rx="3" fill="none" stroke="{GOLD}" stroke-width="1.25" opacity="0.8"/>
<rect x="680" y="214" width="414" height="394" rx="3" fill="none" stroke="{GOLD}" stroke-width="1.25" opacity="0.8"/>
<path d="M196 214 H250 M196 214 V268" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M590 214 H536 M590 214 V268" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M196 598 H250 M196 598 V544" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M590 598 H536 M590 598 V544" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M690 214 H744 M690 214 V268" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M1084 214 H1030 M1084 214 V268" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M690 598 H744 M690 598 V544" fill="none" stroke="{GOLD}" stroke-width="2"/>
<path d="M1084 598 H1030 M1084 598 V544" fill="none" stroke="{GOLD}" stroke-width="2"/>
<rect x="206" y="232" width="390" height="362" fill="url(#page)"/>
<rect x="684" y="232" width="390" height="362" fill="url(#page)"/>
<rect x="206" y="232" width="8" height="362" fill="url(#edge)"/>
<rect x="1066" y="232" width="8" height="362" fill="url(#edge)"/>
<rect class="motion" x="1064" y="232" width="12" height="362" fill="{GOLD}" opacity="0.25">
  <animate attributeName="opacity" values="0.15;0.7;0.15" dur="6.5s" repeatCount="indefinite"/>
</rect>
<rect x="608" y="220" width="64" height="388" fill="#14080B"/>
<line x1="640" y1="236" x2="640" y2="590" stroke="{GOLD}" stroke-width="0.6" opacity="0.55"/>
<rect x="1074" y="240" width="16" height="346" fill="#EFE2D0"/>
<g stroke="{PAGE_SHADOW}" stroke-width="1">
  <line x1="1078" y1="240" x2="1078" y2="586"/>
  <line x1="1082" y1="244" x2="1082" y2="582"/>
  <line x1="1086" y1="248" x2="1086" y2="578"/>
</g>
<rect x="190" y="240" width="16" height="346" fill="#EFE2D0"/>
<g stroke="{PAGE_SHADOW}" stroke-width="1">
  <line x1="194" y1="244" x2="194" y2="582"/>
  <line x1="198" y1="248" x2="198" y2="578"/>
  <line x1="202" y1="252" x2="202" y2="574"/>
</g>
<rect x="1012" y="196" width="18" height="430" fill="{CRIMSON}"/>
<path d="M1012 626 L1021 600 L1030 626 L1030 664 L1021 642 L1012 664 Z" fill="{CRIMSON}"/>
<rect x="1016" y="196" width="3" height="430" fill="{GOLD}" opacity="0.35"/>
<path d="M250 470 H470" stroke="{BURGUNDY}" stroke-width="0.6" opacity="0.45"/>
<path d="M250 490 H430" stroke="{BURGUNDY}" stroke-width="0.6" opacity="0.35"/>
<path d="M250 510 H450" stroke="{BURGUNDY}" stroke-width="0.6" opacity="0.28"/>
<path d="M748 470 H980" stroke="{PAGE_SHADOW}" stroke-width="0.7"/>
<path d="M760 500 H960" stroke="{PAGE_SHADOW}" stroke-width="0.7"/>
<path d="M790 530 H990" stroke="{PAGE_SHADOW}" stroke-width="0.7"/>
<circle cx="640" cy="250" r="3" fill="{GOLD}"/>
{''.join(left)}
{''.join(right)}
{title}
{kicker}
<line x1="430" y1="132" x2="500" y2="132" stroke="{GOLD}" stroke-width="1"/>
<line x1="780" y1="132" x2="850" y2="132" stroke="{GOLD}" stroke-width="1"/>
{''.join(particles)}
"""
    return doc(1280, 720, body, motion=True)


def cover(title_lines: list[str], volume: str, kind: str) -> str:
    lines = []
    start = 168 if len(title_lines) == 1 else 150
    for i, line in enumerate(title_lines):
        lines.append(text_path(CINZEL, line, 110, start + i * 28, 18, PARCHMENT, "middle", 0.04))
    vol = text_path(MONO, volume, 110, 78, 11, GOLD, "middle", 0.16)
    kind_path = text_path(MONO, kind, 110, 248, 10, PARCHMENT, "middle", 0.12)
    body = f"""
<defs>
  <filter id="grain" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer>
      <feFuncA type="linear" slope="0.28"/>
    </feComponentTransfer>
    <feBlend in="SourceGraphic" mode="multiply"/>
  </filter>
</defs>
<rect x="18" y="16" width="184" height="268" rx="4" fill="{WINE}" filter="url(#grain)"/>
<rect x="28" y="26" width="164" height="248" fill="none" stroke="{GOLD}" stroke-width="1.1"/>
<path d="M36 34 H58 M36 34 V56" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
<path d="M184 34 H162 M184 34 V56" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
<path d="M36 266 H58 M36 266 V244" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
<path d="M184 266 H162 M184 266 V244" fill="none" stroke="{GOLD}" stroke-width="1.6"/>
<line x1="48" y1="108" x2="172" y2="108" stroke="{CRIMSON}" stroke-width="1"/>
<line x1="48" y1="220" x2="172" y2="220" stroke="{GOLD}" stroke-width="0.6" opacity="0.7"/>
{vol}
{''.join(lines)}
{kind_path}
"""
    return doc(220, 300, body)


def frontispiece() -> str:
    kicker = text_path(MONO_MED, "FRONTISPIECE   ·   PATENT APPLICATION", 640, 78, 14, GOLD, "middle", 0.14)
    title = text_path(CINZEL, "GUARDIAN WING", 640, 168, 64, PARCHMENT, "middle", 0.08)
    sub = text_path(ITALIC, "A collaborative fleet intelligence system", 640, 214, 26, PARCHMENT, "middle")
    filed = text_path(CINZEL, "FILED", 640, 300, 28, GOLD, "middle", 0.2)
    number = text_path(MONO_MED, "APPLICATION  202641048328", 640, 348, 20, PARCHMENT, "middle", 0.08)
    caveat = text_path(MONO, "NOT GRANTED   ·   APRIL 2026   ·   NO PUBLIC REPOSITORY", 640, 392, 13, PARCHMENT, "middle", 0.08)
    body = f"""
<rect x="48" y="36" width="1184" height="400" fill="{NEAR}" stroke="{GOLD}" stroke-width="1"/>
<rect x="64" y="52" width="1152" height="368" fill="none" stroke="{BURGUNDY}" stroke-width="1"/>
<path d="M96 88 H180" stroke="{CRIMSON}" stroke-width="2"/>
<path d="M1100 88 H1184" stroke="{CRIMSON}" stroke-width="2"/>
<circle cx="112" cy="360" r="36" fill="{CRIMSON}"/>
<circle cx="112" cy="360" r="28" fill="none" stroke="{GOLD}" stroke-width="1"/>
{text_path(CINZEL, "AB", 112, 368, 18, PARCHMENT, "middle", 0.04)}
{kicker}
{title}
{sub}
{filed}
{number}
{caveat}
"""
    return doc(1280, 470, body)


def constellation() -> str:
    spec = json.loads((DATA / "constellation.json").read_text())
    cx, cy = 500, 430
    primary_r = 168
    child_r = 292
    clusters = spec["clusters"]
    # Leave the lower arc open so the caption can sit in parchment, not across a node.
    angles = [-90, 18, 162]
    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="318" fill="none" stroke="{BURGUNDY}" stroke-width="1"/>',
        f'<circle cx="{cx}" cy="{cy}" r="168" fill="none" stroke="{GOLD}" stroke-width="0.6" opacity="0.5"/>',
        f'<circle cx="{cx}" cy="{cy}" r="46" fill="{NEAR}" stroke="{GOLD}" stroke-width="1.2"/>',
        text_path(MONO_MED, spec["center"].upper(), cx, cy + 5, 13, PARCHMENT, "middle", 0.12),
    ]
    for cluster, angle in zip(clusters, angles):
        rad = math.radians(angle)
        px = cx + primary_r * math.cos(rad)
        py = cy + primary_r * math.sin(rad)
        parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{CRIMSON}" stroke-width="1.25"/>'
        )
        children = cluster["children"]
        spread = 34
        start = angle - spread * (len(children) - 1) / 2
        for i, child in enumerate(children):
            crad = math.radians(start + i * spread)
            ccx = cx + child_r * math.cos(crad)
            ccy = cy + child_r * math.sin(crad)
            parts.append(
                f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{ccx:.1f}" y2="{ccy:.1f}" stroke="{BURGUNDY}" stroke-width="1"/>'
            )
            parts.append(f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="5" fill="{NEAR}" stroke="{GOLD}" stroke-width="1"/>')
            # Push labels away from the hub so they do not sit on the spokes.
            lx = ccx + 12 * math.cos(crad)
            ly = ccy + 12 * math.sin(crad) 
            anchor = "start" if math.cos(crad) >= 0 else "end"
            if abs(math.cos(crad)) < 0.35:
                anchor = "middle"
                ly -= 16
            parts.append(text_path(MONO, child, lx, ly + 4, 13, PARCHMENT, anchor, 0.02))
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="16" fill="{WINE}" stroke="{GOLD}" stroke-width="1.2"/>')
        parts.append(
            f'<circle class="motion" cx="{px:.1f}" cy="{py:.1f}" r="22" fill="none" stroke="{CRIMSON}" stroke-width="1" opacity="0.2">'
            f'<animate attributeName="opacity" values="0.15;0.7;0.15" dur="5.5s" repeatCount="indefinite"/>'
            f'<animate attributeName="r" values="18;26;18" dur="5.5s" repeatCount="indefinite"/>'
            f"</circle>"
        )
        label_y = py - 28
        parts.append(text_path(CINZEL_REG, cluster["label"].upper(), px, label_y, 13, GOLD, "middle", 0.06))
    parts.append(
        text_path(
            ITALIC,
            "Three disciplines, and the practices that keep pulling on them.",
            500,
            800,
            22,
            PARCHMENT,
            "middle",
        )
    )
    return doc(1000, 860, "\n".join(parts), motion=True)


def reading_room() -> str:
    spines = [
        (150, 210, WINE, None),
        (250, 250, "#3A1018", None),
        (360, 230, BURGUNDY, "NEVER LIE"),
        (470, 200, "#25080C", None),
        (580, 240, "#5C1822", None),
        (690, 215, WINE, None),
        (800, 255, "#2C0C12", None),
    ]
    books = []
    for x, h, color, title in spines:
        y = 470 - h
        books.append(f'<rect x="{x}" y="{y}" width="62" height="{h}" rx="2" fill="{color}" stroke="{GOLD}" stroke-width="0.7"/>')
        books.append(f'<rect x="{x + 6}" y="{y + 8}" width="2" height="{h - 16}" fill="{GOLD}" opacity="0.45"/>')
        if title:
            books.append(
                f'<g transform="translate({x + 40},{y + h / 2}) rotate(-90)">'
                + text_path(CINZEL_REG, title, 0, 0, 15, PARCHMENT, "middle", 0.12)
                + "</g>"
            )
    caption = text_path(ITALIC, "One title is enough to keep on the desk.", 500, 530, 26, PARCHMENT, "middle")
    credit = text_path(MONO, "FREIDA McFADDEN", 500, 568, 13, GOLD, "middle", 0.18)
    body = f"""
<line x1="120" y1="470" x2="900" y2="470" stroke="{GOLD}" stroke-width="3"/>
<line x1="120" y1="478" x2="900" y2="478" stroke="{BURGUNDY}" stroke-width="8"/>
{''.join(books)}
{caption}
{credit}
"""
    return doc(1000, 620, body)


def seal() -> str:
    ring = text_path(MONO, "THE CRIMSON ARCHIVE", 240, 118, 13, GOLD, "middle", 0.18)
    monogram = text_path(CINZEL, "AB", 240, 268, 92, PARCHMENT, "middle", 0.02)
    under = text_path(MONO, "ANANYA BIJU", 240, 318, 13, GOLD, "middle", 0.2)
    body = f"""
<circle cx="240" cy="250" r="168" fill="{CRIMSON}"/>
<circle cx="240" cy="250" r="150" fill="none" stroke="{GOLD}" stroke-width="1.4"/>
<circle cx="240" cy="250" r="138" fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.7"/>
<circle cx="240" cy="250" r="118" fill="{WINE}"/>
{ring}
{monogram}
{under}
"""
    return doc(480, 500, body)


COVERS = [
    ("lucralens.svg", ["LUCRALENS", "AI"], "VOL. I", "COMPENSATION"),
    ("salary.svg", ["SALARY", "STUDY"], "VOL. I", "ESTIMATION"),
    ("modis.svg", ["MODIS", "FIELD"], "VOL. I", "SATELLITE"),
    ("cloak.svg", ["CLOAK"], "VOL. II", "PERCEPTION"),
    ("roadsense.svg", ["ROADSENSE"], "VOL. II", "PAVEMENT"),
    ("nids.svg", ["INTRUSION", "STUDY"], "VOL. III", "DEFENCE"),
    ("pocket.svg", ["POCKET", "PLANS"], "VOL. IV", "ITINERARY"),
    ("noteverse.svg", ["NOTEVERSE"], "VOL. IV", "NOTES"),
    ("silence.svg", ["SILENCE", "INDEX"], "VOL. IV", "HERITAGE"),
]


def assert_contrast() -> None:
    pairs = {
        "parchment on obsidian": (PARCHMENT, OBSIDIAN),
        "gold on obsidian": (GOLD, OBSIDIAN),
        "gold on near-black": (GOLD, NEAR),
        "parchment on wine": (PARCHMENT, WINE),
        "ink on page": (INK, PAGE),
        "gold on wine": (GOLD, WINE),
        "crimson on obsidian (ornament only)": (CRIMSON, OBSIDIAN),
        "grey on obsidian (ornament only)": (GREY, OBSIDIAN),
    }
    print("contrast")
    for name, (a, b) in pairs.items():
        ratio = contrast_ratio(a, b)
        print(f"  {ratio:5.2f}  {name}")
    for name in (
        "parchment on obsidian",
        "gold on obsidian",
        "gold on near-black",
        "parchment on wine",
        "ink on page",
        "gold on wine",
    ):
        ratio = contrast_ratio(*pairs[name])
        if ratio < 4.5:
            raise SystemExit(f"{name} is {ratio:.2f}, below 4.5")


def main() -> None:
    assert_contrast()
    write(ASSET / "rule.svg", rule_svg())
    write(ASSET / "hero.svg", hero())
    write(ASSET / "frontispiece.svg", frontispiece())
    write(ASSET / "constellation.svg", constellation())
    write(ASSET / "reading-room.svg", reading_room())
    write(ASSET / "seal.svg", seal())
    for filename, lines, volume, kind in COVERS:
        write(ASSET / "covers" / filename, cover(lines, volume, kind))


if __name__ == "__main__":
    main()
