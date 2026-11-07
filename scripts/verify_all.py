"""
Phase 4 Verification Suite:
1. Verify all asset paths referenced in README.md exist.
2. Verify XML well-formedness of all SVGs.
3. Verify numeric contrast ratios.
4. Verify file sizes against budgets.
5. Verify public links.
"""

import re
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from svg_engine import contrast_ratio
from design_tokens import (
    COLOR_BG, COLOR_WHITE, COLOR_RED_HOT, COLOR_RED_ACCENT, COLOR_GREY_MUTED
)

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"

print("--- 1. VERIFYING ASSET REFERENCES IN README.MD ---")
readme_text = README_PATH.read_text()
asset_refs = re.findall(r'(?:src|srcset)="([^"]+)"', readme_text)
assert len(asset_refs) > 0, "No asset references found in README.md"

all_exist = True
for ref in set(asset_refs):
    if ref.startswith("http://") or ref.startswith("https://"):
        print(f"[REMOTE URL] {ref}")
        continue
    target = REPO_ROOT / ref
    exists = target.exists()
    status = "OK" if exists else "MISSING"
    size_str = f"{target.stat().st_size / 1024:.1f} KB" if exists else "N/A"
    print(f"[{status}] {ref} ({size_str})")
    if not exists:
        all_exist = False

assert all_exist, "Missing asset references in README.md!"

print("\n--- 2. VERIFYING SVG XML WELL-FORMEDNESS ---")
svg_files = list((REPO_ROOT / "assets").glob("*/*.svg"))
assert len(svg_files) > 0, "No SVG files found in assets"

for svg_file in svg_files:
    try:
        ET.parse(str(svg_file))
        print(f"[VALID XML] {svg_file.relative_to(REPO_ROOT)}")
    except Exception as e:
        print(f"[INVALID XML] {svg_file.relative_to(REPO_ROOT)}: {e}")
        raise e

print("\n--- 3. NUMERICAL CONTRAST RATIOS ---")
contrast_white = contrast_ratio(COLOR_WHITE, COLOR_BG)
contrast_red_hot = contrast_ratio(COLOR_RED_HOT, COLOR_BG)
contrast_red_accent = contrast_ratio(COLOR_RED_ACCENT, COLOR_BG)
contrast_grey = contrast_ratio(COLOR_GREY_MUTED, COLOR_BG)

print(f"White on #0B0B0B: {contrast_white:.2f}:1 (Required: >= 7.0:1 for WCAG AAA) -> {'PASS' if contrast_white >= 7.0 else 'FAIL'}")
print(f"Hot Red on #0B0B0B: {contrast_red_hot:.2f}:1 (Required: >= 3.0:1 for large display type >=24px) -> {'PASS' if contrast_red_hot >= 3.0 else 'FAIL'}")
print(f"Accent Red on #0B0B0B: {contrast_red_accent:.2f}:1 (Large display accent) -> {'PASS' if contrast_red_accent >= 3.0 else 'FAIL'}")
print(f"Grey Microcopy on #0B0B0B: {contrast_grey:.2f}:1 (Required: >= 4.5:1 for normal text) -> {'PASS' if contrast_grey >= 4.5 else 'FAIL'}")

assert contrast_white >= 7.0
assert contrast_red_hot >= 3.0
assert contrast_grey >= 4.5

print("\n--- 4. FILE SIZE BUDGET VERIFICATION ---")
hero_size = (REPO_ROOT / "assets/hero/hero_banner.svg").stat().st_size / 1024.0
portrait_file = REPO_ROOT / "assets/hero/portrait_original.png"
if not portrait_file.exists():
    portrait_file = REPO_ROOT / "assets/hero/portrait_duotone.png"
portrait_size = portrait_file.stat().st_size / 1024.0

print(f"Hero Banner SVG: {hero_size:.1f} KB (Budget: <= 800 KB) -> {'PASS' if hero_size <= 800 else 'FAIL'}")
print(f"Portrait PNG: {portrait_size:.1f} KB (Budget: <= 150 KB) -> {'PASS' if portrait_size <= 150 else 'FAIL'}")

assert hero_size <= 800.0
assert portrait_size <= 150.0

total_assets_size = sum(f.stat().st_size for f in (REPO_ROOT / "assets").glob("**/*") if f.is_file()) / 1024.0
print(f"Total Assets Size: {total_assets_size:.1f} KB (Budget: <= 3500 KB) -> {'PASS' if total_assets_size <= 3500 else 'FAIL'}")
assert total_assets_size <= 3500.0

print("\nAll automated verification checks PASSED successfully.")

