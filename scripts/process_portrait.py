"""
Process Reference C with its ORIGINAL photographic tones (no artificial red duotone):
1. Rotate 90 degrees CCW (upright).
2. Clean head & shoulders crop with expressive hand gesture.
3. Natural photographic tone curve & contrast enhancement (authentic photo, no red tint).
4. Save optimized web PNG <= 150KB with zero EXIF.
"""

import os
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

SOURCE_PATH = "/Users/ananyabiju/.gemini/antigravity/brain/0d3eb288-58f8-4dfd-abb2-4fdebf973bea/.user_uploaded/media_1794001570130_bc3ea220.jpg"
OUTPUT_DIR = "/Users/ananyabiju/Projects/itsananyaaa/assets/hero"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "portrait_original.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Open and Rotate 90 deg CCW
img = Image.open(SOURCE_PATH).convert("L")
img_rot = img.rotate(90, expand=True)

w, h = img_rot.size
print(f"Rotated dimensions: {w}x{h}")

# 2. Crop head and shoulders
crop_box = (120, 40, 920, 640)
cropped = img_rot.crop(crop_box)
cw, ch = cropped.size

# Resize to crisp display size
target_w = 480
target_h = int(ch * (target_w / cw))
resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

# 3. Enhance natural contrast & subtle sharpening
enhancer = ImageEnhance.Contrast(resized)
contrast_img = enhancer.enhance(1.18)

enhancer_bright = ImageEnhance.Brightness(contrast_img)
bright_img = enhancer_bright.enhance(1.05)

# Convert to RGB preserving original natural photographic tones
rgb_img = bright_img.convert("RGB")

# 4. Quantize to 256 colors for optimal web size
quantized = rgb_img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
quantized.save(OUTPUT_PATH, format="PNG", optimize=True)

size_kb = os.path.getsize(OUTPUT_PATH) / 1024.0
print(f"Saved natural portrait to {OUTPUT_PATH} ({size_kb:.1f} KB)")
assert size_kb <= 150.0, f"File size {size_kb} KB exceeds 150 KB limit!"
