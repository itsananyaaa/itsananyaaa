"""Outline text into SVG paths. GitHub cannot load webfonts inside an <img> SVG."""

from __future__ import annotations

import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
FONT_DIR = ROOT / "fonts"

_CACHE: dict[str, TTFont] = {}


def font(name: str) -> TTFont:
    if name not in _CACHE:
        path = FONT_DIR / name
        if not path.exists():
            raise FileNotFoundError(path)
        _CACHE[name] = TTFont(str(path))
    return _CACHE[name]


def _scale(face: TTFont, size: float) -> float:
    return size / face["head"].unitsPerEm


def measure(face: TTFont, text: str, size: float, tracking: float = 0.0) -> float:
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
    face_name: str,
    text: str,
    x: float,
    y: float,
    size: float,
    fill: str,
    anchor: str = "start",
    tracking: float = 0.0,
    opacity: float | None = None,
) -> str:
    """Draw `text` with the baseline at `y`. anchor is start, middle, or end."""
    face = font(face_name)
    width = measure(face, text, size, tracking)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    elif anchor != "start":
        raise ValueError(anchor)

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
        transform = TransformPen(pen, (scale, 0, 0, -scale, x, y))
        glyphset[glyph].draw(transform)
        path = pen.getCommands()
        if path:
            commands.append(path)
        x += hmtx[glyph][0] * scale + size * tracking
    if not commands:
        return ""
    extra = f' fill-opacity="{opacity}"' if opacity is not None else ""
    d = _quantize(" ".join(commands))
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def _quantize(path: str) -> str:
    def repl(match: re.Match[str]) -> str:
        value = float(match.group())
        rendered = f"{value:.1f}"
        if rendered in {"-0.0", "0.0"}:
            return "0"
        return rendered.rstrip("0").rstrip(".")

    return re.sub(r"-?\d+\.\d+", repl, path)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    def channel(value: int) -> float:
        c = value / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def luminance(color: str) -> float:
        h = color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    lighter = max(luminance(hex_a), luminance(hex_b))
    darker = min(luminance(hex_a), luminance(hex_b))
    return (lighter + 0.05) / (darker + 0.05)
