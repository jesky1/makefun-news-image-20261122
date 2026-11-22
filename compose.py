#!/usr/bin/env python3
"""Render the make.fun news-image-20261122 entry: a one-page newspaper
front page summing up Sunday 22 November 2026, drawn from scratch with
Pillow. Fully deterministic: no clock, no randomness, no network, no
external images. Running this script twice produces byte-identical PNGs.
"""

import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 232)
INK = (18, 18, 18)
NAVY = (13, 26, 46)
GOLD = (176, 141, 58)
RULE = (120, 110, 88)
RED = (150, 28, 22)
MUTED = (84, 78, 66)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw wrapped paragraph; return y after last line."""
    if leading is None:
        leading = fnt.size + 5
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def deterministic_stars(n, w, h, seed=7):
    """Fixed star positions from a simple integer hash (no random module)."""
    pts = []
    for i in range(n):
        v = (i * 2654435761 + seed * 40503) & 0xFFFFFFFF
        x = (v >> 8) % w
        y = (v >> 20) % h
        r = 1 + ((v >> 4) % 2)
        pts.append((x, y, r))
    return pts


def draw_hero(draw, base, x0, y0, x1, y1):
    """Night sky over the Gulf: missile and interceptor trails above a
    silhouetted air base with Patriot radar dishes. All drawn, no photo."""
    hw, hh = x1 - x0, y1 - y0
    horizon = y0 + int(hh * 0.72)

    # Sky gradient: deep navy at top to steel blue at the horizon.
    top = (8, 16, 32)
    bot = (43, 79, 112)
    for yy in range(y0, horizon):
        t = (yy - y0) / max(1, horizon - y0)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=c)

    # Stars.
    for sx, sy, sr in deterministic_stars(90, hw, horizon - y0):
        draw.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                     fill=(220, 226, 238))

    # Moon with soft halo, upper right.
    mx, my, mr = x0 + hw - 120, y0 + 62, 30
    for rr, alpha in ((52, 26), (42, 40)):
        halo = Image.new("RGBA", (rr * 2, rr * 2), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        hd.ellipse([0, 0, rr * 2 - 1, rr * 2 - 1], fill=(235, 238, 245, alpha))
        base.alpha_composite(halo, (mx - rr, my - rr))
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(238, 240, 244))
    draw.ellipse([mx - mr + 9, my - mr + 12, mx - mr + 20, my - mr + 23],
                 fill=(205, 210, 220))
    draw.ellipse([mx + 2, my + 6, mx + 12, my + 16], fill=(205, 210, 220))

    # Sea: dark band below the horizon with pale reflections.
    for yy in range(horizon, y1):
        t = (yy - horizon) / max(1, y1 - horizon)
        c = tuple(int(16 + 10 * t) for _ in range(3))
        c = (c[0], c[1] + 8, c[2] + 18)
        draw.line([(x0, yy), (x1, yy)], fill=c)
    for i, rx in enumerate((180, 420, 700, 880)):
        ry = horizon + 14 + (i % 3) * 12
        draw.line([(x0 + rx, ry), (x0 + rx + 46, ry)], fill=(120, 150, 180),
                  width=2)

    # Missile trails: orange arcs diving from upper left toward the base.
    def arc_trail(p0, p1, ctrl, color, width, head=True):
        pts = []
        for k in range(41):
            t = k / 40
            bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * ctrl[0] + t * t * p1[0]
            by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * ctrl[1] + t * t * p1[1]
            pts.append((bx, by))
        draw.line(pts, fill=color, width=width, joint="curve")
        if head:
            hx, hy = pts[-1]
            for rr, col in ((9, (255, 190, 90)), (5, (255, 230, 160))):
                draw.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=col)

    arc_trail((x0 + 60, y0 + 30), (x0 + 300, horizon - 58),
              (x0 + 150, y0 + 150), (255, 122, 40), 4)
    arc_trail((x0 + 330, y0 + 12), (x0 + 560, horizon - 66),
              (x0 + 470, y0 + 120), (255, 140, 60), 4)
    arc_trail((x0 + 620, y0 + 44), (x0 + 760, horizon - 52),
              (x0 + 700, y0 + 150), (255, 110, 30), 3)

    # Interceptor trails: pale streaks rising from the base.
    arc_trail((x0 + 340, horizon - 40), (x0 + 250, y0 + 96),
              (x0 + 300, y0 + 200), (190, 220, 245), 3, head=False)
    arc_trail((x0 + 700, horizon - 40), (x0 + 830, y0 + 70),
              (x0 + 780, y0 + 180), (190, 220, 245), 3, head=False)

    # Explosion glows where missiles meet the ground.
    for ex, ey, er in ((x0 + 300, horizon - 58, 26),
                       (x0 + 560, horizon - 66, 20),
                       (x0 + 760, horizon - 52, 16)):
        glow = Image.new("RGBA", (er * 4, er * 4), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([0, 0, er * 4 - 1, er * 4 - 1], fill=(255, 150, 50, 70))
        gd.ellipse([er, er, er * 3 - 1, er * 3 - 1], fill=(255, 190, 90, 130))
        base.alpha_composite(glow, (int(ex - er * 2), int(ey - er * 2)))
        draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 226, 150))

    # Ground silhouette: low buildings, masts, and two Patriot radar dishes.
    ground_y = horizon - 34
    draw.rectangle([x0, ground_y, x1, y1], fill=(6, 10, 18))
    for bx, bw, bh in ((x0 + 40, 90, 22), (x0 + 150, 60, 16),
                       (x0 + 830, 110, 24), (x0 + 640, 70, 15)):
        draw.rectangle([bx, ground_y - bh, bx + bw, ground_y], fill=(10, 15, 26))
        for wx in range(bx + 8, bx + bw - 6, 16):
            draw.rectangle([wx, ground_y - bh + 5, wx + 6, ground_y - bh + 10],
                           fill=(255, 190, 90))
    # Antenna masts with blinking-tip dots (fixed, deterministic).
    for ax in (x0 + 240, x0 + 560):
        draw.line([(ax, ground_y), (ax, ground_y - 52)], fill=(20, 28, 42),
                  width=3)
        draw.ellipse([ax - 3, ground_y - 58, ax + 3, ground_y - 52],
                     fill=(255, 80, 60))
    # Patriot radar dishes: tilted bowls on pedestals.
    for dx in (x0 + 330, x0 + 690):
        draw.line([(dx, ground_y), (dx, ground_y - 26)], fill=(24, 34, 50),
                  width=6)
        draw.arc([dx - 26, ground_y - 62, dx + 26, ground_y - 10],
                 start=200, end=340, fill=(150, 165, 185), width=5)
        draw.line([(dx - 22, ground_y - 36), (dx + 22, ground_y - 36)],
                  fill=(150, 165, 185), width=3)

    # Caption bar inside the hero, bottom.
    cap_h = 34
    cap = Image.new("RGBA", (hw, cap_h), (5, 8, 14, 215))
    base.alpha_composite(cap, (x0, y1 - cap_h))
    cap_font = font(SANS_B, 15)
    cap_text = ("BAHRAIN, SATURDAY NIGHT — Iranian missiles and drones rain "
                "on two U.S. Patriot radar sites")
    draw.text((x0 + 14, y1 - cap_h + 8), cap_text, font=cap_font,
              fill=(240, 238, 228))


def main():
    base = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(base)
    M = 44  # side margin

    # ---- Masthead ----
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.rectangle([0, 112, W, 116], fill=GOLD)
    centered(draw, W // 2, 10, "THE WORLD IN ONE DAY",
             font(SERIF_B, 46), (244, 240, 226))
    centered(draw, W // 2, 68,
             "SUNDAY 22 NOVEMBER 2026  •  ONE IMAGE, THE WHOLE DAY'S NEWS",
             font(SANS_B, 16), (198, 168, 96))

    # ---- Hero illustration ----
    draw_hero(draw, base, M, 128, W - M, 336)

    # ---- Lead headline ----
    y = 346
    centered(draw, W // 2, y, "IRAN STRIKES U.S. PATRIOT RADARS",
             font(SERIF_B, 35), INK)
    centered(draw, W // 2, y + 41, "IN BAHRAIN AS GULF CRISIS ERUPTS",
             font(SERIF_B, 35), RED)
    y = 434
    rule(draw, M, y, W - M, width=2)
    y += 10
    deck = ("Tehran says its combined missile-and-drone salvo destroyed two "
            "Patriot radars at al-Riffa and Awali, in retaliation for U.S. "
            "drone flights over Iranian airspace and a strike on a radar "
            "site on Hengam Island. Bahrain says the attack hit a civilian "
            "industrial facility, starting a fire with no injuries, as at "
            "least three oil tankers came under attack in or near the "
            "Strait of Hormuz.")
    y = para(draw, M, y, W - 2 * M, deck, font(SERIF, 18), leading=24)
    y += 2
    rule(draw, M, y, W - M, width=2)

    # ---- Four secondary stories, two columns ----
    stories = [
        ("UKRAINE  •  WAR IN EUROPE",
         "Russian missiles hit Lviv; two killed",
         "At least two people were killed and ten wounded as Russian "
         "missiles struck the western city of Lviv. A drone also hit a "
         "Russian cargo ship in the Baltic."),
        ("TRADE  •  AFTER TEN YEARS",
         "EU and Indonesia sign landmark trade deal",
         "Brussels and Jakarta signed a major trade agreement after a "
         "decade of talks, removing tariffs on about 98.5% of goods."),
        ("CLIMATE  •  COP31, ANTALYA",
         "Climate talks stall over fossil fuels",
         "The COP31 summit in Antalya ran past schedule, deadlocked over "
         "the future of fossil fuels, as negotiators struggled to agree."),
        ("EARTHQUAKE  •  PERU",
         "Magnitude 6.9 quake shakes the Andes",
         "A magnitude 6.9 earthquake struck the Andes in Peru, with a "
         "second tremor of 6.7 near Carhuamayo. A 4.1 quake hit Myanmar."),
    ]
    y += 12
    col_w = (W - 2 * M - 28) // 2
    col_y = [y, y]
    for i, (kicker, head, body) in enumerate(stories):
        col = i % 2
        x = M + col * (col_w + 28)
        cy = col_y[col]
        draw.text((x, cy), kicker, font=font(SANS_B, 13), fill=RED)
        cy += 19
        cy = para(draw, x, cy, col_w, head, font(SERIF_B, 20), leading=24)
        cy += 1
        cy = para(draw, x, cy, col_w, body, font(SERIF, 15), leading=19)
        col_y[col] = cy + 12
    y = max(col_y) + 2
    rule(draw, M, y, W - M, width=2)

    # ---- ALSO TODAY: six briefs, 3 x 2 ----
    y += 10
    draw.text((M, y), "ALSO TODAY", font=font(SANS_B, 16), fill=NAVY)
    y += 24
    briefs = [
        ("MEXICO", "Top cartel boss on the FBI's 10 most-wanted list "
         "captured after a shootout."),
        ("WASHINGTON", "The FBI is investigating a suspected hack of its "
         "criminal database."),
        ("DIPLOMACY", "Trump seeks a permanent nuclear deal with Iran; he "
         "also met Xi in Shenzhen."),
        ("HONG KONG", "Voting began for the Election Committee that picks "
         "the city's leader."),
        ("BALTICS", "Estonia says it will close its border with Russia."),
        ("BRAZIL", "Ex-president Jair Bolsonaro in intensive care with an "
         "acute bowel obstruction."),
    ]
    bw = (W - 2 * M - 2 * 20) // 3
    row_y = y
    for i, (kicker, text) in enumerate(briefs):
        col = i % 3
        row = i // 3
        x = M + col * (bw + 20)
        by = row_y + row * 56
        draw.text((x, by), kicker, font=font(SANS_B, 13), fill=RED)
        para(draw, x, by + 17, bw, text, font(SERIF, 13), leading=17)
    y = row_y + 2 * 56 + 2
    rule(draw, M, y, W - M, width=2)

    # ---- Footer ----
    y += 8
    centered(draw, W // 2, y,
             "Sources: Reuters  •  Associated Press  •  AFP  •  Bloomberg  —  "
             "Illustration drawn from scratch; no photographs.",
             font(SANS, 12), MUTED)
    centered(draw, W // 2, y + 18,
             "Sunday 22 November 2026.",
             font(SANS, 12), MUTED)
    assert y + 18 + 12 <= H, f"layout overflow: footer ends at {y + 30}"

    img = base.convert("RGB")
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
