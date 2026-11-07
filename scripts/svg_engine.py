"""
SVG Engine: Outlines typography using fonttools into pure SVG paths.
Produces zero-dependency vector assets for GitHub profile display.
"""

from __future__ import annotations
import re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

_CACHE: dict[str, TTFont] = {}


def get_font(path: str) -> TTFont:
    if path not in _CACHE:
        if not Path(path).exists():
            raise FileNotFoundError(f"Font file not found: {path}")
        _CACHE[path] = TTFont(path)
    return _CACHE[path]


def _scale(face: TTFont, size: float) -> float:
    return size / face["head"].unitsPerEm


def measure_text(font_path: str, text: str, size: float, tracking: float = 0.0) -> float:
    face = get_font(font_path)
    cmap = face.getBestCmap()
    hmtx = face["hmtx"]
    scale = _scale(face, size)
    width = 0.0
    for ch in text:
        glyph = cmap.get(ord(ch))
        if glyph is None:
            width += size * 0.5
        else:
            width += hmtx[glyph][0] * scale
        width += size * tracking
    return width


def text_path(
    font_path: str,
    text: str,
    x: float,
    y: float,
    size: float,
    fill: str = "#F7F7F7",
    stroke: str | None = None,
    stroke_width: float = 1.0,
    anchor: str = "start",
    tracking: float = 0.0,
    opacity: float | None = None,
) -> str:
    """Renders text with baseline at y as an SVG path. anchor can be start, middle, or end."""
    face = get_font(font_path)
    width = measure_text(font_path, text, size, tracking)

    if anchor == "middle":
        x -= width / 2.0
    elif anchor == "end":
        x -= width
    elif anchor != "start":
        raise ValueError(f"Unknown anchor: {anchor}")

    cmap = face.getBestCmap()
    hmtx = face["hmtx"]
    glyphset = face.getGlyphSet()
    scale = _scale(face, size)
    commands: list[str] = []

    for ch in text:
        glyph = cmap.get(ord(ch))
        if glyph is None:
            x += size * 0.5 + size * tracking
            continue
        pen = SVGPathPen(glyphset)
        # Flip Y since font coordinates are Y-up while SVG is Y-down
        transform = TransformPen(pen, (scale, 0, 0, -scale, x, y))
        glyphset[glyph].draw(transform)
        cmd = pen.getCommands()
        if cmd:
            commands.append(cmd)
        x += hmtx[glyph][0] * scale + size * tracking

    if not commands:
        return ""

    d = _quantize(" ".join(commands))
    attrs = []
    if fill == "none":
        attrs.append('fill="none"')
    else:
        attrs.append(f'fill="{fill}"')

    if stroke:
        attrs.append(f'stroke="{stroke}" stroke-width="{stroke_width:.1f}"')

    if opacity is not None and opacity < 1.0:
        attrs.append(f'opacity="{opacity:.2f}"')

    return f'<path d="{d}" {" ".join(attrs)}/>'


def _quantize(path: str) -> str:
    def repl(m: re.Match[str]) -> str:
        val = float(m.group())
        r = f"{val:.1f}"
        if r in ("-0.0", "0.0"):
            return "0"
        return r.rstrip("0").rstrip(".") if "." in r else r

    return re.sub(r"-?\d+\.\d+", repl, path)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    def channel(v: int) -> float:
        c = v / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def luminance(hex_col: str) -> float:
        h = hex_col.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    l1 = luminance(hex_a)
    l2 = luminance(hex_b)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

