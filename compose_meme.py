#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme from the AI-generated base scene.

Inputs (assets/):
  base.png      - AI-generated office scene, ghost mascot at the desk, no text
  mark-1024.png - make.fun logo mark (ghost in magenta circle), from make.fun/press
Output:
  meme.png      - 1024x1024, classic top-text / bottom-text meme + logo badge

Text is drawn with PIL (never by the image model) so every letter is exact.
Run: python3 compose_meme.py
"""
from PIL import Image, ImageDraw, ImageFont

BASE = "assets/base.png"
MARK = "assets/mark-1024.png"
OUT = "meme.png"
SIZE = 1024

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

TOP_LINES = ["MAY 26, 2026:", "GTA VI LAUNCH DAY"]
BOTTOM_LINES = ["THE WHOLE OFFICE", "CALLED IN SICK."]


def outlined_text(draw, cx, y, text, font, fill="white", stroke="black", stroke_w=7):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke)


def main():
    img = Image.open(BASE).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    top_font = ImageFont.truetype(FONT_PATH, 76)
    bottom_font = ImageFont.truetype(FONT_PATH, 76)

    y = 28
    for line in TOP_LINES:
        outlined_text(draw, SIZE // 2, y, line, top_font)
        y += 92

    y = SIZE - 28 - 92 * len(BOTTOM_LINES)
    for line in BOTTOM_LINES:
        outlined_text(draw, SIZE // 2, y, line, bottom_font)
        y += 92

    # make.fun logo mark, top-right corner badge
    mark = Image.open(MARK).convert("RGBA")
    mark = mark.resize((112, 112), Image.LANCZOS)
    img.paste(mark, (SIZE - 128, 16), mark)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
