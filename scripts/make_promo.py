"""
Redesign the 440x280 small promo tile for CWS.
Goal: bigger primary message, cleaner hierarchy, single language (zh),
brand element (dashed frame) integrated into the headline rather than
sitting separately.
"""
import math
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path("/home/user/DOUBAO-Chrome-extension")
OUT = REPO / "store" / "promo-440x280.png"

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
W, H = 440, 280
BRAND_FROM = (79, 140, 255)
BRAND_TO   = (122, 92, 255)

def gradient(w, h, c1, c2):
    im = Image.new("RGB", (w, h), c1)
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x/(w-1))*0.55 + (y/(h-1))*0.45
            px[x, y] = (
                int(c1[0]+(c2[0]-c1[0])*t),
                int(c1[1]+(c2[1]-c1[1])*t),
                int(c1[2]+(c2[2]-c1[2])*t),
            )
    return im

def dashed_rect(d, box, color, w=2, dash=10, gap=6):
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), dash + gap):
        d.line([(x, y0), (min(x + dash, x1), y0)], fill=color, width=w)
        d.line([(x, y1), (min(x + dash, x1), y1)], fill=color, width=w)
    for y in range(int(y0), int(y1), dash + gap):
        d.line([(x0, y), (x0, min(y + dash, y1))], fill=color, width=w)
        d.line([(x1, y), (x1, min(y + dash, y1))], fill=color, width=w)

img = gradient(W, H, BRAND_FROM, BRAND_TO).convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

# --- Top: small product name + separator ---
name_font = ImageFont.truetype(FONT, 17)
d.text((28, 22), "AI 截图解读", fill=(255, 255, 255, 235), font=name_font)
d.line([(28, 50), (W - 28, 50)], fill=(255, 255, 255, 70), width=1)

# --- Big headline with "AI" wrapped in a dashed selection box ---
# Headline rendered as two parts so we can draw the dashed box around AI.
head_font = ImageFont.truetype(FONT, 58)
prefix = "框选 · 问 "
ai_text = "AI"

pre_w = d.textlength(prefix, font=head_font)
ai_w = d.textlength(ai_text, font=head_font)
ai_bb = d.textbbox((0, 0), ai_text, font=head_font)
ai_h = ai_bb[3] - ai_bb[1]
pre_bb = d.textbbox((0, 0), prefix, font=head_font)
pre_h = pre_bb[3] - pre_bb[1]

total_w = pre_w + ai_w + 24  # AI gets +24 horizontal padding for the box
hx = (W - total_w) // 2
hy = 78

# Draw prefix
d.text((hx, hy), prefix, fill="white", font=head_font)

# Position AI inside its box (slightly higher to align baselines visually)
ai_box_padding_x = 12
ai_box_padding_y = 6
ai_x = hx + pre_w + ai_box_padding_x
d.text((ai_x, hy), ai_text, fill="white", font=head_font)

# Dashed selection box around AI
ai_box = (
    ai_x - ai_box_padding_x,
    hy - ai_box_padding_y + 4,
    ai_x + ai_w + ai_box_padding_x,
    hy + ai_h + ai_box_padding_y + 8,
)
dashed_rect(d, ai_box, (255, 255, 255, 230), w=2, dash=9, gap=6)

# Tiny "Alt+S" badge clinging to the top-left corner of the dashed box
kbd_font = ImageFont.truetype(FONT, 12)
kbd_text = "Alt+S"
kbd_w = d.textlength(kbd_text, font=kbd_font)
bx0 = ai_box[0] - 4
by0 = ai_box[1] - 22
d.rounded_rectangle(
    (bx0, by0, bx0 + kbd_w + 14, by0 + 20),
    radius=5, fill=(255, 255, 255, 250)
)
d.text((bx0 + 7, by0 + 3), kbd_text, fill=BRAND_FROM, font=kbd_font)

# --- Subtitle ---
sub_font = ImageFont.truetype(FONT, 18)
sub = "拖拽框选任意区域，豆包多模态秒解读"
sb = d.textbbox((0, 0), sub, font=sub_font)
sw = sb[2] - sb[0]
sx = (W - sw) // 2 - sb[0]
d.text((sx, 205), sub, fill=(255, 255, 255, 230), font=sub_font)

# --- Brand strip at very bottom ---
brand_font = ImageFont.truetype(FONT, 12)
brand = "Chrome 扩展 · 国产 AI 驱动"
bbb = d.textbbox((0, 0), brand, font=brand_font)
bw = bbb[2] - bbb[0]
bx = (W - bw) // 2 - bbb[0]
d.text((bx, 248), brand, fill=(255, 255, 255, 170), font=brand_font)

img.convert("RGB").save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({img.size})")
