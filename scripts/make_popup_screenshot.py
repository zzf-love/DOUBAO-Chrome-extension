"""
Render the real popup.html via headless Chromium, then compose a 1280x800
store screenshot with a bilingual brand banner. Pixel-perfect mock of the
v1.3.4 popup with sample API Key already filled in.
"""
import json
import re
import tempfile
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

REPO = Path("/home/user/DOUBAO-Chrome-extension")
OUT = REPO / "store"
OUT.mkdir(exist_ok=True)

FONT_ZH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
BANNER_H = 80
TARGET = (1280, 800)
BANNER_GRAD_FROM = (79, 140, 255)
BANNER_GRAD_TO   = (122, 92, 255)
BG = (248, 249, 252)

# Load zh_CN messages so we can shim chrome.i18n.getMessage
zh = json.load(open(REPO / "_locales/zh_CN/messages.json"))
i18n_map = {k: v["message"] for k, v in zh.items()}

# Read popup.html and inject a shim
popup_html = (REPO / "popup.html").read_text()
shim = f"""
<script>
window.chrome = {{
  runtime: {{
    getManifest: () => ({{ version: "1.3.4" }}),
    sendMessage: () => Promise.resolve({{ ok: true }}),
    onMessage: {{ addListener: () => {{}} }},
  }},
  i18n: {{
    getMessage: (k) => ({json.dumps(i18n_map, ensure_ascii=False)})[k] || "",
    getUILanguage: () => "zh-CN",
  }},
  storage: {{
    local: {{
      // Pre-fill apiKey so the warning banner doesn't show, simulating a
      // configured user; pendingCapture absent.
      get: (keys, cb) => {{
        const data = {{
          apiKey: "ark-2024xxxxxxxxxxxxxxxxxxxxxx",
          endpoint: "https://ark.cn-beijing.volces.com/api/v3/responses",
          model: "doubao-seed-2-0-mini-260428",
          customPrompts: ["", "", ""],
          theme: "aurora"
        }};
        const out = {{}};
        const arr = Array.isArray(keys) ? keys : Object.keys(keys || data);
        for (const k of arr) out[k] = data[k];
        if (cb) cb(out);
        return Promise.resolve(out);
      }},
      set: (obj, cb) => {{ if (cb) cb(); return Promise.resolve(); }},
      remove: () => Promise.resolve(),
    }}
  }},
  tabs: {{ create: () => {{}} }},
}};
</script>
"""
patched = popup_html.replace("<head>", "<head>" + shim, 1)

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
    # Inline scripts/css continue to resolve relative to file: ; copy popup.js
    # and icons into the temp dir.
    tmp_dir = Path(tempfile.mkdtemp())
    (tmp_dir / "popup.js").write_text((REPO / "popup.js").read_text())
    (tmp_dir / "icons").mkdir(exist_ok=True)
    for name in ["icon16.png", "icon48.png", "icon128.png"]:
        (tmp_dir / "icons" / name).write_bytes((REPO / "icons" / name).read_bytes())
    tmp_html = tmp_dir / "popup.html"
    tmp_html.write_text(patched)

print(f"Rendering popup from {tmp_html} ...")

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    )
    ctx = browser.new_context(
        viewport={"width": 360, "height": 800},
        device_scale_factor=2,  # retina for crisp text
    )
    page = ctx.new_page()
    page.goto(f"file://{tmp_html}")
    page.wait_for_timeout(500)  # let JS finish render
    body = page.locator("body")
    box = body.bounding_box()
    print(f"popup body box: {box}")
    page.screenshot(path="/tmp/popup_raw.png", clip={
        "x": 0, "y": 0, "width": box["width"], "height": box["height"]
    }, omit_background=False)
    browser.close()

raw = Image.open("/tmp/popup_raw.png").convert("RGBA")
print(f"raw size: {raw.size}")

# Compose 1280x800 store screenshot
canvas = Image.new("RGB", TARGET, BG)

# gradient banner
def gradient(w, h, c1, c2):
    im = Image.new("RGB", (w, h), c1)
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x/(w-1))*0.6 + (y/(h-1))*0.4
            px[x, y] = (
                int(c1[0]+(c2[0]-c1[0])*t),
                int(c1[1]+(c2[1]-c1[1])*t),
                int(c1[2]+(c2[2]-c1[2])*t),
            )
    return im

banner = gradient(TARGET[0], BANNER_H, BANNER_GRAD_FROM, BANNER_GRAD_TO)
canvas.paste(banner, (0, 0))
d = ImageDraw.Draw(canvas)

zh_title = "设置仅存本地，6 个内置 Prompt + 3 个自定义槽 + 4 套皮肤"
en_title = "All settings stored locally — 6 built-in prompts + 3 custom slots + 4 themes"
zh_font = ImageFont.truetype(FONT_ZH, 26)
en_font = ImageFont.truetype(FONT_ZH, 14)
zh_bb = d.textbbox((0, 0), zh_title, font=zh_font)
en_bb = d.textbbox((0, 0), en_title, font=en_font)
total_h = (zh_bb[3] - zh_bb[1]) + 4 + (en_bb[3] - en_bb[1])
y0 = (BANNER_H - total_h) // 2 - 4
d.text((40, y0), zh_title, fill=(255, 255, 255), font=zh_font)
d.text((40, y0 + (zh_bb[3] - zh_bb[1]) + 4), en_title,
       fill=(255, 255, 255, 230), font=en_font)

# Place popup on the LEFT, leaving room for feature callouts on the RIGHT.
iw, ih = raw.size
avail_h = TARGET[1] - BANNER_H - 50
scale = avail_h / ih
nw, nh = int(iw * scale), int(ih * scale)
popup_resized = raw.resize((nw, nh), Image.LANCZOS)
x = 70
y = BANNER_H + 25

# drop shadow
from PIL import ImageFilter
shadow = Image.new("RGBA", (nw + 80, nh + 80), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle((40, 40, 40 + nw, 40 + nh), radius=20, fill=(0, 0, 0, 80))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
canvas_rgba = canvas.convert("RGBA")
canvas_rgba.alpha_composite(shadow, (x - 40, y - 30))
canvas_rgba.paste(popup_resized, (x, y), popup_resized)
canvas = canvas_rgba.convert("RGB")
d = ImageDraw.Draw(canvas)

# Right-side callouts pointing to features.
# Each callout: (text_zh, text_en, anchor_xy_on_popup, label_xy)
# anchor_xy is relative to popup origin (x, y).
popup_right = x + nw
label_x = popup_right + 50

# Anchors are in resized-popup coordinates (popup is now nw x nh).
# Hand-tuned to land on the right UI elements.
callouts = [
    # (zh, en, anchor_x, anchor_y, label_y on canvas)
    ("4 套皮肤切换",     "4 themes",         460,  32, 130),
    ("快捷键自定义",     "Custom shortcut",  400, 184, 245),
    ("免费领取 API Key", "Get free key",     380, 250, 360),
    ("6 + 3 模板",       "6+3 templates",    400, 415, 475),
]

cf_zh = ImageFont.truetype(FONT_ZH, 22)
cf_en = ImageFont.truetype(FONT_ZH, 13)

for zh_txt, en_txt, ax_rel, ay_rel, ly in callouts:
    ax, ay = x + ax_rel, y + ay_rel
    # bullet dot at anchor
    d.ellipse((ax - 7, ay - 7, ax + 7, ay + 7), fill=BANNER_GRAD_FROM, outline=(255, 255, 255), width=2)
    # curve / connector — simple two-segment polyline
    mid_x = (ax + label_x) // 2
    d.line([(ax + 7, ay), (mid_x, ay), (mid_x, ly + 18), (label_x - 10, ly + 18)],
           fill=BANNER_GRAD_FROM, width=2)
    # text labels
    d.text((label_x, ly), zh_txt, fill=(31, 35, 41), font=cf_zh)
    en_bb = d.textbbox((0, 0), en_txt, font=cf_en)
    d.text((label_x, ly + 32), en_txt, fill=(107, 114, 128), font=cf_en)

out_path = OUT / "store-03-popup-v134.png"
canvas.save(out_path, "PNG", optimize=True)
print(f"wrote {out_path} {canvas.size}")
