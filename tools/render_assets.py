#!/usr/bin/env python3
"""
Render watch-face glyph bitmaps from the project typeface + palette.

The Huawei Band format is bitmap-only: the firmware has no font engine, so every
digit, colon, and label must be shipped as a pre-rendered image. This script is
the bridge from our design sources (Chakra Petch in assets/fonts/, colors in
src/colors.xml) to those bitmaps.

Output goes to build/rendered/. Import those images into Huawei Theme Studio,
place them as DIGITALIMAGE widgets per docs/layout-spec.md, and export the .hwt.

Usage:
    python3 tools/render_assets.py

Requires: Pillow (pip install Pillow)
"""
import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageFont, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(ROOT, "build", "rendered")

# ---- Palette (parsed from the single source of truth: src/colors.xml) --------
def load_palette():
    tree = ET.parse(os.path.join(ROOT, "src", "colors.xml"))
    return {c.get("name"): c.get("value") for c in tree.getroot().findall("Color")}

def hex_to_rgba(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

# ---- Glyph-set renderer ------------------------------------------------------
def render_glyph_set(name, glyphs, font_path, px, color_rgba, pad=6):
    """Render each glyph into a uniform, tightly-cropped cell so digits align.

    A fixed cell width (the widest glyph) keeps HH:MM columns steady when the
    firmware swaps one digit for another. Files are named 0.png..9.png; the
    colon is saved as colon.png.
    """
    font = ImageFont.truetype(font_path, px)
    # Measure every glyph to find a common cell size.
    boxes = {g: font.getbbox(g) for g in glyphs}
    cell_w = max(b[2] - b[0] for b in boxes.values()) + 2 * pad
    cell_h = max(b[3] - b[1] for b in boxes.values()) + 2 * pad

    outdir = os.path.join(OUT, name)
    os.makedirs(outdir, exist_ok=True)
    for g in glyphs:
        img = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        l, t, r, b = boxes[g]
        # Center the glyph in the cell, correcting for its bearing.
        x = (cell_w - (r - l)) / 2 - l
        y = (cell_h - (b - t)) / 2 - t
        d.text((x, y), g, font=font, fill=color_rgba)
        fname = {":": "colon"}.get(g, g) + ".png"
        img.save(os.path.join(outdir, fname))
    print(f"  {name}: {len(glyphs)} glyphs @ {cell_w}x{cell_h}px -> {outdir}")

# ---- Placeholder preview (Gadgetbridge shows preview/cover.jpg) --------------
def render_cover(palette):
    W, H = 194, 368  # Band 9 panel
    img = Image.new("RGB", (W, H), hex_to_rgba(palette["background"])[:3])
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(FONTS, "ChakraPetch-Bold.ttf"), 26)
    txt = "12:48"
    bb = d.textbbox((0, 0), txt, font=font)
    d.text(((W - (bb[2] - bb[0])) / 2, 150), txt, font=font,
           fill=hex_to_rgba(palette["primary"])[:3])
    cover_dir = os.path.join(ROOT, "preview")
    os.makedirs(cover_dir, exist_ok=True)
    img.save(os.path.join(cover_dir, "cover.jpg"), quality=90)
    print(f"  preview/cover.jpg ({W}x{H})")

def main():
    palette = load_palette()
    bold = os.path.join(FONTS, "ChakraPetch-Bold.ttf")
    reg = os.path.join(FONTS, "ChakraPetch-Regular.ttf")

    print("Rendering glyph sets:")
    # Hero clock digits: Bold, primary amber, large.
    render_glyph_set("clock", "0123456789:", bold, 120,
                     hex_to_rgba(palette["primary"]))
    # Data digits (steps/battery): Regular, standard tan, small.
    render_glyph_set("data", "0123456789", reg, 40,
                     hex_to_rgba(palette["standard"]))
    # Heart-rate digits: Regular, danger_red.
    render_glyph_set("data_hr", "0123456789", reg, 40,
                     hex_to_rgba(palette["danger_red"]))
    print("Rendering preview:")
    render_cover(palette)
    print("Done. Import build/rendered/ into Huawei Theme Studio.")

if __name__ == "__main__":
    main()
