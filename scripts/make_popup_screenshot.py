"""
Render the v1.3.7 popup in 3 themes via headless Chromium and compose a
1280x800 CWS store screenshot showing Aurora as the main popup plus
Dark/Sakura thumbnails on the right — so the viewer can actually see
the theme difference, not just read about it.
"""
import json
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = Path("/home/user/DOUBAO-Chrome-extension")
OUT = REPO / "store"
OUT.mkdir(exist_ok=True)

FONT_ZH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
BANNER_H = 80
TARGET = (1280, 800)
BANNER_GRAD_FROM = (79, 140, 255)
BANNER_GRAD_TO   = (122, 92, 255)
BG = (248, 249, 252)

# ----- Stage temp dir with the popup files + a shim -----
zh = json.load(open(REPO / "_locales/zh_CN/messages.json"))
i18n_map = {k: v["message"] for k, v in zh.items()}

shim = f"""
<script>
window.chrome = {{
  runtime: {{
    getManifest: () => ({{ version: "1.3.7" }}),
    sendMessage: () => Promise.resolve({{ ok: true }}),
    onMessage: {{ addListener: () => {{}} }},
  }},
  i18n: {{
    getMessage: (k) => ({json.dumps(i18n_map, ensure_ascii=False)})[k] || "",
    getUILanguage: () => "zh-CN",
  }},
  storage: {{
    local: {{
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
    }},
    onChanged: {{ addListener: () => {{}} }},
  }},
  tabs: {{ create: () => {{}} }},
}};
</script>
"""

popup_html = (REPO / "popup.html").read_text()
patched = popup_html.replace("<head>", "<head>" + shim, 1)

tmp_dir = Path(tempfile.mkdtemp())
(tmp_dir / "popup.js").write_text((REPO / "popup.js").read_text())
(tmp_dir / "icons").mkdir(exist_ok=True)
for n in ["icon16.png", "icon48.png", "icon128.png"]:
    (tmp_dir / "icons" / n).write_bytes((REPO / "icons" / n).read_bytes())
(tmp_dir / "popup.html").write_text(patched)
tmp_html = tmp_dir / "popup.html"
print(f"staged at {tmp_html}")

# ----- Render popup at 3 themes in one session -----
def render_themes():
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        )
        ctx = browser.new_context(
            viewport={"width": 360, "height": 800},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        page.goto(f"file://{tmp_html}")
        page.wait_for_timeout(500)
        for theme in ["aurora", "dark", "sakura"]:
            # applyTheme is a top-level function in popup.js
            page.evaluate(f"applyTheme('{theme}', false)")
            page.wait_for_timeout(120)
            box = page.locator("body").bounding_box()
            shot = page.screenshot(clip={
                "x": 0, "y": 0,
                "width": box["width"], "height": box["height"]
            })
            out[theme] = Image.open(__import__("io").BytesIO(shot)).convert("RGBA")
            print(f"  rendered {theme}: {out[theme].size}")
        browser.close()
    return out

themes = render_themes()

# ----- Compose 1280x800 store image -----
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

canvas = Image.new("RGB", TARGET, BG)
canvas.paste(gradient(TARGET[0], BANNER_H, BANNER_GRAD_FROM, BANNER_GRAD_TO), (0, 0))
d = ImageDraw.Draw(canvas)

# Banner text — updated for 3 themes
zh_title = "设置仅存本地，6 个内置 Prompt + 3 个自定义槽 + 3 套皮肤"
en_title = "All settings stored locally — 6 built-in prompts + 3 custom slots + 3 themes"
zh_font = ImageFont.truetype(FONT_ZH, 26)
en_font = ImageFont.truetype(FONT_ZH, 14)
zh_bb = d.textbbox((0, 0), zh_title, font=zh_font)
en_bb = d.textbbox((0, 0), en_title, font=en_font)
total_h = (zh_bb[3] - zh_bb[1]) + 4 + (en_bb[3] - en_bb[1])
y0 = (BANNER_H - total_h) // 2 - 4
d.text((40, y0), zh_title, fill=(255, 255, 255), font=zh_font)
d.text((40, y0 + (zh_bb[3] - zh_bb[1]) + 4), en_title,
       fill=(255, 255, 255, 230), font=en_font)

# Helper: paste with drop shadow
def paste_with_shadow(canvas_rgba, img, x, y, blur=18, shadow_alpha=70):
    nw, nh = img.size
    sh = Image.new("RGBA", (nw + 80, nh + 80), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((40, 40, 40 + nw, 40 + nh), radius=20,
                         fill=(0, 0, 0, shadow_alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas_rgba.alpha_composite(sh, (x - 40, y - 30))
    canvas_rgba.paste(img, (x, y), img)

# Main: Aurora on the left
aurora_raw = themes["aurora"]
aurora_scale = 640 / aurora_raw.size[1]  # 640px tall main
aurora = aurora_raw.resize(
    (int(aurora_raw.size[0] * aurora_scale), int(aurora_raw.size[1] * aurora_scale)),
    Image.LANCZOS
)
ax, ay = 60, 120

canvas_rgba = canvas.convert("RGBA")
paste_with_shadow(canvas_rgba, aurora, ax, ay, blur=22, shadow_alpha=90)

# Thumbnails: Dark + Sakura on the right, side by side
thumb_scale = 0.42
def make_thumb(raw):
    return raw.resize(
        (int(raw.size[0] * thumb_scale), int(raw.size[1] * thumb_scale)),
        Image.LANCZOS
    )

dark = make_thumb(themes["dark"])
sakura = make_thumb(themes["sakura"])

# Layout right column: two thumbs at top
right_x_start = ax + aurora.size[0] + 60  # 60px gap after main
tw, th = dark.size

dx = right_x_start
dy = 140
sx = right_x_start + tw + 35
sy = 140

paste_with_shadow(canvas_rgba, dark, dx, dy, blur=16, shadow_alpha=70)
paste_with_shadow(canvas_rgba, sakura, sx, sy, blur=16, shadow_alpha=70)

canvas = canvas_rgba.convert("RGB")
d = ImageDraw.Draw(canvas)

# Labels under each thumbnail
label_font = ImageFont.truetype(FONT_ZH, 22)
sub_font = ImageFont.truetype(FONT_ZH, 14)

def labeled(text_zh, text_en, cx, top_y):
    bb = d.textbbox((0, 0), text_zh, font=label_font)
    w = bb[2] - bb[0]
    d.text((cx - w // 2, top_y), text_zh, fill=(31, 35, 41), font=label_font)
    bb2 = d.textbbox((0, 0), text_en, font=sub_font)
    w2 = bb2[2] - bb2[0]
    d.text((cx - w2 // 2, top_y + 30), text_en,
           fill=(107, 114, 128), font=sub_font)

labeled("Dark 主题",   "Dark theme",   dx + tw // 2, dy + th + 14)
labeled("Sakura 主题", "Sakura theme", sx + tw // 2, sy + th + 14)

# Below thumbnails: a short check-list of v1.3 highlights
feat_font = ImageFont.truetype(FONT_ZH, 20)
feat_sub  = ImageFont.truetype(FONT_ZH, 13)
feats = [
    ("3 套皮肤实时切换", "switches the whole UI instantly"),
    ("6 + 3 个 Prompt 模板", "6 built-in + 3 custom slots"),
    ("快捷键可自定义",  "rebind via chrome://extensions/shortcuts"),
    ("免费领取 API Key", "tap the link in the popup"),
]
list_x = right_x_start
list_y = dy + th + 90
for i, (zh_, en_) in enumerate(feats):
    yi = list_y + i * 44
    # bullet dot
    d.ellipse((list_x, yi + 9, list_x + 10, yi + 19),
              fill=BANNER_GRAD_FROM)
    d.text((list_x + 22, yi), zh_, fill=(31, 35, 41), font=feat_font)
    d.text((list_x + 22, yi + 24), en_, fill=(107, 114, 128), font=feat_sub)

# "Aurora（默认）" label under main popup
amain_x = ax + aurora.size[0] // 2
amain_y = ay + aurora.size[1] + 14
labeled("Aurora 主题（默认）", "Aurora — default", amain_x, amain_y)

out_path = OUT / "store-03-popup-v137.png"
canvas.save(out_path, "PNG", optimize=True)
print(f"wrote {out_path} {canvas.size}")
