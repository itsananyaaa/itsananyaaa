"""
Design Tokens sampled from Reference A (Colour & Typography Authority).
"""

from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).resolve().parent.parent

# Color Palette
COLOR_BG          = "#0B0B0B"  # Near-black canvas background
COLOR_CARD        = "#141414"  # Card / Surface elevated fill
COLOR_CARD_HOVER  = "#1C1C1E"  # Slightly lighter card surface
COLOR_BORDER      = "#282828"  # Hairline grid dividers
COLOR_BORDER_HOT  = "#E2232F"  # Highlighted hot red border
COLOR_RED_HOT     = "#E2232F"  # High-intensity asterisk / display red (4.23:1 on #0B0B0B)
COLOR_RED_ACCENT  = "#D81119"  # Editorial rich crimson (3.76:1 on #0B0B0B)
COLOR_RED_DEEP    = "#720000"  # Duotone shadow depth / isometric shadow
COLOR_RED_MUTED   = "#450A0D"  # Subtle dark red backing
COLOR_WHITE       = "#F7F7F7"  # High-contrast text & outlines (21:1 on #0B0B0B)
COLOR_GREY_MUTED  = "#888888"  # Secondary micro-labels (7.5:1 on #0B0B0B)
COLOR_GREY_CHIP   = "#222222"  # Chip tag background

# Fonts
FONTS_DIR = Path("/Users/ananyabiju/.gemini/antigravity/brain/0d3eb288-58f8-4dfd-abb2-4fdebf973bea/scratch/fonts")
FONT_ANTON = str(FONTS_DIR / "Anton-Regular.ttf")
FONT_INTER = str(FONTS_DIR / "Inter-Bold.ttf")
