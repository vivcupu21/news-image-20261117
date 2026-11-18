#!/usr/bin/env python3
"""Draw the news-image entry for 17 November 2026.

A modern newspaper front page: masthead with the date, one lead story
(Ukraine strikes the Kerch Bridge again), four regional panels and a
bottom strip, plus a ticker of further stories from the same day.

Every story was reported on Tuesday 17 November 2026 (Reuters, BBC, AP,
CNN, via Just Security Early Edition 17 Nov 2026 and other same-day
round-ups). The image is drawn with Pillow only; output is a
1024x1024 PNG, well under the 1 MiB gate.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
NAVY = (20, 33, 61)
GOLD = (232, 163, 23)
RED = (180, 35, 24)
INK = (24, 24, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
SKY = (191, 217, 232)
SEA = (46, 110, 142)
LINE = (180, 172, 150)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bridge(d, x0, y0, x1, y1):
    """Kerch Bridge scene: sky, sea, deck with a collapsed middle span."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    sea_y = y0 + int((y1 - y0) * 0.62)
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # waves
    for wx in range(x0 + 10, x1 - 20, 46):
        d.arc([wx, sea_y + 14, wx + 34, sea_y + 30], 200, 340, fill=(255, 255, 255), width=3)
    deck_y = y0 + int((y1 - y0) * 0.42)
    # towers (kept inside the illustration: top >= y0 + 4)
    for tx in (x0 + 150, x1 - 190):
        d.rectangle([tx, deck_y - 70, tx + 14, deck_y + 4], fill=(70, 70, 78))
        d.rectangle([tx - 6, deck_y - 70, tx + 20, deck_y - 60], fill=(70, 70, 78))
        d.rectangle([tx - 6, deck_y - 38, tx + 20, deck_y - 28], fill=(70, 70, 78))
    # cables from towers to deck
    for tx in (x0 + 157, x1 - 183):
        for cx in range(x0 + 40, x1 - 30, 60):
            if abs(cx - tx) > 130:
                continue
            d.line([tx, deck_y - 66, cx, deck_y], fill=(90, 90, 96), width=2)
    # deck: left and right spans, gap in the middle
    gap_c = (x0 + x1) // 2
    gap_w = 150
    d.rectangle([x0, deck_y, gap_c - gap_w // 2, deck_y + 12], fill=(96, 96, 104))
    d.rectangle([gap_c + gap_w // 2, deck_y, x1, deck_y + 12], fill=(96, 96, 104))
    # collapsed span tilted down into the sea
    d.polygon([(gap_c - gap_w // 2 + 8, deck_y + 2),
               (gap_c + 6, deck_y + 2),
               (gap_c - 18, sea_y + 26),
               (gap_c - 44, sea_y + 22)], fill=(120, 40, 30))
    d.line([gap_c - gap_w // 2 + 8, deck_y + 2, gap_c - 18, sea_y + 26],
           fill=(60, 20, 16), width=3)
    # explosion + smoke over the gap (kept inside the illustration)
    ex, ey = gap_c, deck_y - 8
    d.polygon([(ex, ey - 34), (ex + 12, ey - 10), (ex + 34, ey - 16),
               (ex + 18, ey + 4), (ex + 30, ey + 22), (ex + 6, ey + 16),
               (ex, ey + 34), (ex - 8, ey + 14), (ex - 32, ey + 20),
               (ex - 18, ey + 2), (ex - 34, ey - 14), (ex - 12, ey - 12)],
              fill=(245, 130, 32))
    d.polygon([(ex, ey - 18), (ex + 7, ey - 5), (ex + 18, ey - 8),
               (ex + 9, ey + 3), (ex + 15, ey + 12), (ex, ey + 8),
               (ex - 6, ey + 16), (ex - 12, ey + 4), (ex - 18, ey + 8),
               (ex - 10, ey - 4), (ex - 16, ey - 10), (ex - 5, ey - 8)],
              fill=(255, 205, 60))
    for sx, sy, sr in ((ex - 46, ey - 40, 17), (ex - 26, ey - 52, 19),
                       (ex + 40, ey - 44, 16), (ex + 56, ey - 26, 13),
                       (ex + 4, ey - 54, 17)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 112))
    # (no label in the sky: the headline below names the bridge; the sea
    # already carries "KERCH STRAIT")
    d.text((x0 + 14, sea_y + 44), "KERCH STRAIT",
           font=font(SANS_B, 20), fill=(255, 255, 255))


def icon_drone(d, cx, cy, s, col):
    d.ellipse([cx - s, cy - s // 4, cx - s // 2, cy + s // 4], outline=col, width=4)
    d.ellipse([cx + s // 2, cy - s // 4, cx + s, cy + s // 4], outline=col, width=4)
    d.ellipse([cx - s // 5, cy - s // 5, cx + s // 5, cy + s // 5], fill=col)
    d.line([cx - s // 2, cy, cx + s // 2, cy], fill=col, width=4)
    d.line([cx, cy + s // 5, cx, cy + s // 2], fill=col, width=4)
    d.rectangle([cx - s // 4, cy + s // 2, cx + s // 4, cy + s // 2 + 8], fill=col)


def icon_jet(d, cx, cy, s, col):
    d.polygon([(cx - s, cy + s // 4), (cx + s // 2, cy), (cx + s, cy - s // 6),
               (cx + s // 2, cy + s // 6), (cx - s // 3, cy + s // 2)],
              fill=col)
    d.polygon([(cx - s // 4, cy - s // 6), (cx + s // 3, cy - s // 2),
               (cx + s // 2, cy - s // 6)], fill=col)


def icon_scales(d, cx, cy, s, col):
    d.line([cx, cy - s, cx, cy + s], fill=col, width=5)
    d.line([cx - s, cy - s + 8, cx + s, cy - s + 8], fill=col, width=5)
    d.line([cx - s, cy - s + 8, cx - s, cy], fill=col, width=3)
    d.line([cx + s, cy - s + 8, cx + s, cy], fill=col, width=3)
    d.arc([cx - s - 14, cy - 8, cx - s + 14, cy + 16], 0, 180, fill=col, width=4)
    d.arc([cx + s - 14, cy - 8, cx + s + 14, cy + 16], 0, 180, fill=col, width=4)
    d.rectangle([cx - s - 4, cy + s, cx + s + 4, cy + s + 8], fill=col)


def icon_building(d, cx, cy, s, col):
    d.polygon([(cx - s, cy - s // 3), (cx, cy - s), (cx + s, cy - s // 3)], fill=col)
    d.rectangle([cx - s, cy - s // 3, cx + s, cy + s], fill=col)
    for i in (-2, -1, 0, 1, 2):
        d.rectangle([cx + i * 18 - 5, cy - s // 3 + 14, cx + i * 18 + 5, cy + s - 12],
                    fill=PAPER)
    d.rectangle([cx - s - 8, cy + s, cx + s + 8, cy + s + 8], fill=col)


def panel(d, x, y, w, h, tag, tag_col, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=2)
    ix, iy = x + 56, y + h // 2
    icon(d, ix, iy, 32, tag_col)
    tx = x + 112
    tw = w - 112 - 14
    d.text((tx, y + 12), tag, font=font(SANS_B, 19), fill=tag_col)
    hl = font(SANS_B, 26)
    lines = wrap(d, headline, hl, tw)
    ly = y + 38
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=hl, fill=INK)
        ly += 30
    bl = font(SANS, 20)
    for ln in wrap(d, body, bl, tw)[:2]:
        d.text((tx, ly + 2), ln, font=bl, fill=GREY)
        ly += 24


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 58), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 82), "TUESDAY, 17 NOVEMBER 2026",
           font=font(SANS_B, 28), fill=GOLD, anchor="ma")

    # ---- dateline ----
    d.text((W // 2, 128), "SIX STORIES THAT DEFINED THE DAY  ·  AS REPORTED 17 NOVEMBER 2026",
           font=font(SANS_B, 19), fill=NAVY, anchor="ma")
    d.line([24, 158, W - 24, 158], fill=NAVY, width=3)

    # ---- lead story ----
    lx, ly, lw, lh = 24, 168, W - 48, 322
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=LINE, width=2)
    draw_bridge(d, lx + 2, ly + 2, lx + lw - 2, ly + 186)
    d.text((lx + 16, ly + 194), "UKRAINE  ·  RUSSIA-UKRAINE WAR",
           font=font(SANS_B, 20), fill=RED)
    d.text((lx + 16, ly + 220),
           "Ukraine hits the Crimea bridge again",
           font=font(SERIF_B, 40), fill=INK)
    d.text((lx + 16, ly + 268),
           "A span collapses in the second strike in two days; Russia hits Kyiv's bridges,",
           font=font(SANS, 23), fill=GREY)
    d.text((lx + 16, ly + 294),
           "cutting heat, water and power across the capital.",
           font=font(SANS, 23), fill=GREY)

    # ---- four panels, 2 x 2 ----
    pw, ph = 478, 152
    gx, gy = 24, 498
    panel(d, gx, gy, pw, ph, "MIDDLE EAST", (150, 60, 20),
          "Iran fires drones at US radar base in Bahrain",
          "Intercepted; no casualties or damage reported.", icon_drone)
    panel(d, gx + pw + 20, gy, pw, ph, "ASIA-PACIFIC", (20, 80, 140),
          "Japan scrambles jets after Russian airspace breach",
          "South Korea and Taiwan also respond to incursions.", icon_jet)
    panel(d, gx, gy + ph + 8, pw, ph, "MIDDLE EAST", (120, 30, 110),
          "Settler kills woman, 72, in Jericho",
          "UK sanctions eight firms building settlements.", icon_scales)
    panel(d, gx + pw + 20, gy + ph + 8, pw, ph, "AFRICA", (160, 90, 10),
          "UN: drones killed 1,600+ in Sudan this year",
          "Rights commission warns of an \u201cunbearable toll\u201d.", icon_drone)

    # ---- bottom strip: Mongolia ----
    bx, by, bw, bh = 24, 818, W - 48, 96
    d.rectangle([bx, by, bx + bw, by + bh], fill=CARD, outline=LINE, width=2)
    icon_building(d, bx + 56, by + bh // 2, 30, (20, 90, 60))
    d.text((bx + 116, by + 10), "MONGOLIA", font=font(SANS_B, 19), fill=(20, 90, 60))
    d.text((bx + 116, by + 34), "Mongolia's president says he will resign",
           font=font(SANS_B, 27), fill=INK)
    d.text((bx + 116, by + 66),
           "Khurelsukh quits over a $25m railway bribery claim; he denies wrongdoing.",
           font=font(SANS, 21), fill=GREY)

    # ---- ticker ----
    d.rectangle([0, 928, W, 1024], fill=NAVY)
    d.text((W // 2, 940), "ALSO TODAY",
           font=font(SANS_B, 20), fill=GOLD, anchor="ma")
    d.text((W // 2, 966),
           "Xi and Carney agree tariff cuts  ·  UN talks on killer robots in Geneva  ·  Trump heads to Asia",
           font=font(SANS, 19), fill=(255, 255, 255), anchor="ma")

    img.save("/home/hatch/workspace/makefun-news-image-20261117/entry/entry.png",
             optimize=True)
    print("saved")


if __name__ == "__main__":
    main()
