"""8 张小红书 1080x1440 教程图（含真彩 emoji）。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

REPO = Path("/home/user/DOUBAO-Chrome-extension")
OUT = REPO / "xhs"
OUT.mkdir(exist_ok=True)

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

W, H = 1080, 1440
BRAND_FROM = (79, 140, 255)
BRAND_TO   = (122, 92, 255)
BG_LIGHT   = (248, 249, 252)
TEXT_DARK  = (31, 35, 41)
TEXT_GREY  = (75, 85, 99)
TEXT_HINT  = (156, 163, 175)
ACCENT     = (251, 191, 36)
OK         = (34, 197, 94)
ERR        = (239, 68, 68)
WHITE      = (255, 255, 255)

def F(size):
    return ImageFont.truetype(FONT, size)

_emoji_cache = {}
def emoji_img(char, size):
    """Render a single emoji glyph at requested px size (RGBA, tight crop)."""
    key = (char, size)
    if key in _emoji_cache:
        return _emoji_cache[key]
    canvas = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(EMOJI_FONT, 109,
                           layout_engine=ImageFont.Layout.RAQM)
    d.text((10, 10), char, font=f, embedded_color=True)
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop(bbox)
    ratio = size / canvas.height
    out = canvas.resize((max(1, int(canvas.width * ratio)), size),
                        Image.LANCZOS)
    _emoji_cache[key] = out
    return out

def paste_emoji(im, char, x, y, size):
    e = emoji_img(char, size)
    im.paste(e, (x, y), e)
    return e.width

def gradient(w, h, c1, c2):
    im = Image.new("RGB", (w, h), c1)
    px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x/(w-1))*0.5 + (y/(h-1))*0.5
            px[x, y] = (
                int(c1[0]+(c2[0]-c1[0])*t),
                int(c1[1]+(c2[1]-c1[1])*t),
                int(c1[2]+(c2[2]-c1[2])*t),
            )
    return im

def base_step(num, title):
    img = Image.new("RGB", (W, H), BG_LIGHT)
    strip_h = 220
    strip = gradient(W, strip_h, BRAND_FROM, BRAND_TO)
    img.paste(strip, (0, 0))
    d = ImageDraw.Draw(img)
    # numbered circle
    cx, cy, r = 130, strip_h//2, 60
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=WHITE)
    num_font = F(64)
    nb = d.textbbox((0, 0), str(num), font=num_font)
    nw_, nh_ = nb[2]-nb[0], nb[3]-nb[1]
    d.text((cx-nw_//2-nb[0], cy-nh_//2-nb[1]-3),
           str(num), fill=BRAND_FROM, font=num_font)
    d.text((cx-r, cy+r+10), "STEP", fill=(255, 255, 255), font=F(28))
    d.text((230, cy-50), title, fill=WHITE, font=F(64))
    # footer
    d.rectangle((0, H-72, W, H), fill=(245, 247, 252))
    d.text((40, H-52), "AI 截图解读 · Chrome 扩展", fill=TEXT_GREY, font=F(26))
    d.text((W-280, H-52), "@小红书 / GitHub", fill=TEXT_HINT, font=F(26))
    return img

# ---------- Slide 1: COVER ----------
def slide_cover():
    img = gradient(W, H, BRAND_FROM, BRAND_TO)
    d = ImageDraw.Draw(img)

    # title — centered top
    title1 = "看图直接问 AI"
    tf = F(132)
    tb = d.textbbox((0, 0), title1, font=tf)
    tw_ = tb[2]-tb[0]
    d.text(((W-tw_)//2-tb[0], 140), title1, fill=WHITE, font=tf)

    # subtitle below title
    sub = "Chrome 浏览器框选截图秒解读"
    sf = F(48)
    sb = d.textbbox((0, 0), sub, font=sf)
    sw_ = sb[2]-sb[0]
    d.text(((W-sw_)//2-sb[0], 320), sub, fill=(255, 255, 255), font=sf)

    # dashed rect centered with AI inside
    rw, rh = 460, 460
    rx0 = (W - rw) // 2
    ry0 = 460
    rect = (rx0, ry0, rx0+rw, ry0+rh)
    for x in range(rect[0], rect[2], 26):
        d.line([(x, rect[1]), (min(x+14, rect[2]), rect[1])], fill=WHITE, width=6)
        d.line([(x, rect[3]), (min(x+14, rect[2]), rect[3])], fill=WHITE, width=6)
    for y in range(rect[1], rect[3], 26):
        d.line([(rect[0], y), (rect[0], min(y+14, rect[3]))], fill=WHITE, width=6)
        d.line([(rect[2], y), (rect[2], min(y+14, rect[3]))], fill=WHITE, width=6)

    # Alt+S badge top-left inside rect
    bx, by = rect[0] + 22, rect[1] + 22
    d.rounded_rectangle((bx, by, bx+170, by+62), radius=12, fill=WHITE)
    d.text((bx+28, by+14), "Alt+S", fill=BRAND_FROM, font=F(36))

    # AI big text centered in rect
    ai_font = F(180)
    aib = d.textbbox((0, 0), "AI", font=ai_font)
    aiw, aih = aib[2]-aib[0], aib[3]-aib[1]
    d.text((rect[0]+(rw-aiw)//2-aib[0],
            rect[1]+(rh-aih)//2-aib[1]-30),
           "AI", fill=WHITE, font=ai_font)
    # caption
    cap = "解读中…"
    cf = F(44)
    cb = d.textbbox((0, 0), cap, font=cf)
    cw_ = cb[2]-cb[0]
    d.text((rect[0]+(rw-cw_)//2-cb[0], rect[1]+rh-110),
           cap, fill=(255, 255, 255), font=cf)

    # benefits line
    b = "无需 VPN · 不离开网页 · 0.5 秒出结果"
    bf = F(42)
    bb = d.textbbox((0, 0), b, font=bf)
    bw_ = bb[2]-bb[0]
    d.text(((W-bw_)//2-bb[0], 1010), b, fill=(255, 255, 255), font=bf)

    # chips (white pills with brand-color text — readable)
    chips = ["#chrome插件", "#AI工具", "#豆包", "#效率"]
    cf2 = F(34)
    total_w = 0
    widths = []
    for c in chips:
        cw_ = d.textlength(c, font=cf2) + 40
        widths.append(cw_)
        total_w += cw_
    total_w += 16 * (len(chips) - 1)
    cx = (W - total_w) // 2
    for c, cw_ in zip(chips, widths):
        d.rounded_rectangle((cx, 1110, cx+cw_, 1176), radius=33, fill=WHITE)
        d.text((cx+20, 1118), c, fill=BRAND_FROM, font=cf2)
        cx += cw_ + 16

    # bottom call-to-action
    cta = "👇 评论区扣 1，私你最新版安装包"
    cf3 = F(38)
    # mix emoji+text manually
    em_w = paste_emoji(img, "👇", 220, 1280, 52)
    d.text((220+em_w+18, 1280), "评论区扣 1，私你最新版安装包",
           fill=WHITE, font=cf3)
    return img

# ---------- Slide 2: STEP 1 解压 ----------
def slide_step1():
    img = base_step(1, "解压安装包")
    d = ImageDraw.Draw(img)
    y = 320

    # ZIP card
    box1 = (90, y, 360, y+240)
    d.rounded_rectangle(box1, radius=24, fill=(229, 231, 235),
                        outline=(160, 160, 180), width=3)
    d.text((box1[0]+50, box1[1]+50), "ZIP", fill=BRAND_FROM, font=F(90))
    d.text((box1[0]+10, box1[1]+170), "v1.2.0.zip", fill=TEXT_GREY, font=F(32))

    # arrow + label
    ax, ay = 400, y+105
    d.polygon([(ax, ay-20), (ax+110, ay), (ax, ay+20)], fill=BRAND_FROM)
    d.rectangle((ax, ay-8, ax+90, ay+8), fill=BRAND_FROM)
    d.text((385, ay+50), "右键解压", fill=BRAND_FROM, font=F(32))

    # folder card (with emoji)
    box2 = (570, y, 990, y+240)
    d.rounded_rectangle(box2, radius=24, fill=WHITE,
                        outline=BRAND_FROM, width=4)
    paste_emoji(img, "📁", box2[0]+30, box2[1]+30, 80)
    d = ImageDraw.Draw(img)
    d.text((box2[0]+130, box2[1]+50), "ai-explainer/", fill=TEXT_DARK, font=F(34))
    d.text((box2[0]+30, box2[1]+140), "manifest.json", fill=TEXT_GREY, font=F(26))
    d.text((box2[0]+30, box2[1]+175), "background.js", fill=TEXT_GREY, font=F(26))
    d.text((box2[0]+30, box2[1]+210), "...", fill=TEXT_GREY, font=F(26))

    # warning callout
    cy = 700
    d.rounded_rectangle((60, cy, W-60, cy+300), radius=24, fill=(255, 251, 235))
    d.rectangle((60, cy, 76, cy+300), fill=ACCENT)
    paste_emoji(img, "⚠️", 110, cy+30, 60)
    d = ImageDraw.Draw(img)
    d.text((190, cy+40), "重要：保留解压后的文件夹",
           fill=(146, 64, 14), font=F(48))
    d.text((110, cy+130),
           "Chrome 一直从这个文件夹读取插件",
           fill=(146, 64, 14), font=F(40))
    d.text((110, cy+190),
           "把文件夹删了，插件就用不了",
           fill=(146, 64, 14), font=F(40))

    # tip
    paste_emoji(img, "💡", 60, 1090, 48)
    d = ImageDraw.Draw(img)
    d.text((124, 1095), "建议放在 D 盘 / 应用 / 等不会乱删的位置",
           fill=TEXT_GREY, font=F(34))
    return img

# ---------- Slide 3: STEP 2 打开扩展页 ----------
def slide_step2():
    img = base_step(2, "打开浏览器扩展页")
    d = ImageDraw.Draw(img)
    y = 320

    # browser mock
    d.rounded_rectangle((60, y, W-60, y+360), radius=24,
                        fill=WHITE, outline=(220, 220, 230), width=2)
    d.rounded_rectangle((60, y, W-60, y+74), radius=24, fill=(243, 244, 246))
    # mask bottom of title bar
    d.rectangle((60, y+50, W-60, y+74), fill=(243, 244, 246))
    for i, c in enumerate([(239, 68, 68), (251, 191, 36), (34, 197, 94)]):
        d.ellipse((90+i*36, y+24, 116+i*36, y+50), fill=c)
    d.rounded_rectangle((220, y+18, W-100, y+62), radius=22,
                        fill=WHITE, outline=(200, 200, 210), width=2)
    d.text((250, y+24), "chrome://extensions/", fill=TEXT_DARK, font=F(40))
    d.text((W-130, y+18), "↑", fill=BRAND_FROM, font=F(50))

    # url highlight
    d.text((100, y+130), "在地址栏输入：", fill=TEXT_GREY, font=F(38))
    d.rounded_rectangle((100, y+200, W-100, y+296), radius=14,
                        fill=(238, 242, 255), outline=BRAND_FROM, width=3)
    d.text((125, y+220), "chrome://extensions/", fill=BRAND_FROM, font=F(56))

    # action items below
    iy = y+460
    paste_emoji(img, "✅", 60, iy, 50)
    d = ImageDraw.Draw(img)
    d.text((130, iy), "按下回车", fill=TEXT_DARK, font=F(46))

    paste_emoji(img, "✅", 60, iy+90, 50)
    d = ImageDraw.Draw(img)
    d.text((130, iy+90), "打开页面右上角的", fill=TEXT_DARK, font=F(46))
    d.text((130, iy+150), "\"开发者模式\" 开关", fill=BRAND_FROM, font=F(50))

    # toggle illustration
    tx, ty = 760, iy+105
    d.rounded_rectangle((tx, ty, tx+160, ty+78), radius=40, fill=BRAND_FROM)
    d.ellipse((tx+88, ty+8, tx+152, ty+70), fill=WHITE)

    paste_emoji(img, "💡", 60, 1290, 44)
    d = ImageDraw.Draw(img)
    d.text((118, 1294),
           "Edge：开关在左下角，叫\"开发人员模式\"",
           fill=TEXT_GREY, font=F(30))
    return img

# ---------- Slide 4: STEP 3 加载已解压 ----------
def slide_step3():
    img = base_step(3, "加载插件")
    d = ImageDraw.Draw(img)
    y = 320

    # button
    d.rounded_rectangle((80, y, W-80, y+140), radius=20, fill=BRAND_FROM)
    d.text((120, y+38), "+ 加载已解压的扩展程序",
           fill=WHITE, font=F(56))

    # downward arrow
    d.text((W//2-30, y+200), "↓", fill=BRAND_FROM, font=F(80))

    # folder card
    fy = y + 320
    d.rounded_rectangle((180, fy, W-180, fy+280),
                        radius=24, fill=WHITE,
                        outline=BRAND_FROM, width=4)
    paste_emoji(img, "📁", 210, fy+30, 80)
    d = ImageDraw.Draw(img)
    d.text((310, fy+50), "选择刚才解压出的", fill=TEXT_DARK, font=F(42))
    d.text((310, fy+105), "文件夹", fill=TEXT_DARK, font=F(42))
    d.text((210, fy+180), "ai-explainer/",
           fill=BRAND_FROM, font=F(50))
    d.text((210, fy+240),
           "（里面有 manifest.json 那一层）",
           fill=TEXT_GREY, font=F(30))

    # success card
    sy = 1130
    d.rounded_rectangle((60, sy, W-60, sy+180),
                        radius=20, fill=(220, 252, 231))
    paste_emoji(img, "🎉", 90, sy+30, 60)
    d = ImageDraw.Draw(img)
    d.text((180, sy+40), "插件出现在列表里就装好了",
           fill=(22, 101, 52), font=F(42))
    d.text((90, sy+110),
           "顺手在拼图图标里点图钉固定到工具栏",
           fill=(22, 101, 52), font=F(34))
    return img

# ---------- Slide 5: STEP 4 申请 API Key ----------
def slide_step4():
    img = base_step(4, "领取免费 API Key")
    d = ImageDraw.Draw(img)
    y = 320

    # URL card
    d.rounded_rectangle((60, y, W-60, y+170), radius=20,
                        fill=(238, 242, 255), outline=BRAND_FROM, width=3)
    paste_emoji(img, "🌐", 90, y+20, 56)
    d = ImageDraw.Draw(img)
    d.text((170, y+25), "访问火山方舟官网", fill=TEXT_GREY, font=F(34))
    d.text((90, y+90), "volcengine.com/product/ark",
           fill=BRAND_FROM, font=F(48))

    # steps
    bullets = [
        "手机号注册 → 实名认证（免费）",
        "进入「在线推理 → API 调用」",
        "点「创建 API Key」",
        "复制 ark- 开头的字符串",
    ]
    cy = y + 220
    for i, b in enumerate(bullets):
        d.ellipse((60, cy, 116, cy+56), fill=BRAND_FROM)
        d.text((78, cy+8), str(i+1), fill=WHITE, font=F(36))
        d.text((140, cy+4), b, fill=TEXT_DARK, font=F(42))
        cy += 100

    # key example block (terminal-style)
    ky = cy + 30
    d.rounded_rectangle((60, ky, W-60, ky+150), radius=18, fill=(17, 24, 39))
    d.text((90, ky+22), "API Key 长这样",
           fill=(156, 163, 175), font=F(28))
    paste_emoji(img, "👇", 290, ky+18, 38)
    d = ImageDraw.Draw(img)
    d.text((90, ky+70), "ark-2024xxxxxxxxxxxx",
           fill=(74, 222, 128), font=F(48))

    # free quota tip
    d.rounded_rectangle((60, 1240, W-60, 1340), radius=18,
                        fill=(254, 243, 199))
    paste_emoji(img, "🎁", 90, 1252, 56)
    d = ImageDraw.Draw(img)
    d.text((170, 1262), "新用户免费 token 额度够个人用很久",
           fill=(146, 64, 14), font=F(36))
    return img

# ---------- Slide 6: STEP 5 填 Key ----------
def slide_step5():
    img = base_step(5, "配置插件")
    d = ImageDraw.Draw(img)
    y = 300

    # popup mock
    pw, ph = 580, 740
    px, py = (W-pw)//2, y

    # shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((px+6, py+12, px+pw+6, py+ph+12),
                         radius=20, fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    base = img.convert("RGBA")
    base.alpha_composite(sh)
    img = base.convert("RGB")
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((px, py, px+pw, py+ph), radius=20,
                        fill=WHITE, outline=(220, 220, 230), width=2)
    head_h = 100
    head = gradient(pw, head_h, BRAND_FROM, BRAND_TO)
    mask = Image.new("L", (pw, head_h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, pw, head_h*2), radius=20, fill=255)
    img.paste(head, (px, py), mask)
    d = ImageDraw.Draw(img)
    d.text((px+24, py+18), "AI 截图解读", fill=WHITE, font=F(42))
    d.text((px+24, py+68), "由豆包多模态大模型驱动",
           fill=WHITE, font=F(24))

    # API key field
    d.text((px+30, py+head_h+30), "API Key *", fill=ERR, font=F(30))
    d.rounded_rectangle((px+30, py+head_h+72, px+pw-30, py+head_h+148),
                        radius=12, fill=WHITE, outline=BRAND_FROM, width=4)
    d.text((px+50, py+head_h+90), "ark-2024xxxxxxxxxxxx",
           fill=TEXT_DARK, font=F(34))
    d.text((px+pw+14, py+head_h+92), "← 粘进来",
           fill=BRAND_FROM, font=F(38))

    # other fields hint
    d.text((px+30, py+head_h+200), "模型 / Endpoint / Prompt",
           fill=TEXT_HINT, font=F(30))
    d.text((px+30, py+head_h+248), "保持默认即可",
           fill=TEXT_HINT, font=F(30))

    # save button
    bx0, by0 = px+30, py+head_h+360
    d.rounded_rectangle((bx0, by0, bx0+160, by0+76),
                        radius=14, fill=BRAND_FROM)
    d.text((bx0+50, by0+20), "保存", fill=WHITE, font=F(38))
    paste_emoji(img, "✅", bx0+200, by0+22, 40)
    d = ImageDraw.Draw(img)
    d.text((bx0+250, by0+22), "已保存", fill=OK, font=F(34))

    # bottom hint
    by = 1180
    paste_emoji(img, "📌", 60, by, 44)
    d = ImageDraw.Draw(img)
    d.text((124, by+2), "右上角拼图图标找到插件",
           fill=TEXT_DARK, font=F(38))
    d.text((124, by+62), "点图钉固定到工具栏",
           fill=TEXT_GREY, font=F(36))
    return img

# ---------- Slide 7: STEP 6 框选 ----------
def slide_step6():
    img = base_step(6, "按 Alt+S 框选")
    d = ImageDraw.Draw(img)
    y = 300

    # keyboard combo
    kx, ky = 200, y
    kbd_size = 150
    for i, key in enumerate(["Alt", "+", "S"]):
        if key == "+":
            d.text((kx + i*200 + 50, ky + 35), "+",
                   fill=TEXT_DARK, font=F(88))
            continue
        d.rounded_rectangle(
            (kx + i*200, ky, kx + i*200 + kbd_size, ky + kbd_size),
            radius=22, fill=WHITE, outline=(180, 180, 200), width=5
        )
        d.rounded_rectangle(
            (kx + i*200+8, ky+8, kx + i*200 + kbd_size,
             ky + kbd_size),
            radius=22, fill=(245, 247, 252),
            outline=(180, 180, 200), width=3
        )
        kf = F(64)
        kb = d.textbbox((0, 0), key, font=kf)
        kw_ = kb[2]-kb[0]; kh_ = kb[3]-kb[1]
        d.text((kx + i*200 + (kbd_size-kw_)//2 - kb[0],
                ky + (kbd_size-kh_)//2 - kb[1]),
               key, fill=TEXT_DARK, font=kf)

    cy = ky + kbd_size + 50
    hint = "在任意网页按下"
    hf = F(40)
    hb = d.textbbox((0, 0), hint, font=hf)
    hw_ = hb[2]-hb[0]
    d.text(((W-hw_)//2-hb[0], cy), hint, fill=TEXT_GREY, font=hf)
    cy += 80

    # mock webpage with darkened overlay + selection box
    rect = (140, cy, W-140, cy+460)
    d.rounded_rectangle(rect, radius=24, fill=(248, 249, 252),
                        outline=(220, 220, 230), width=2)
    overlay = Image.new("RGBA", (rect[2]-rect[0], rect[3]-rect[1]),
                         (0, 0, 0, 110))
    base = img.convert("RGBA")
    base.alpha_composite(overlay, dest=(rect[0], rect[1]))
    img = base.convert("RGB")
    d = ImageDraw.Draw(img)
    inner = (rect[0]+80, rect[1]+80, rect[2]-80, rect[3]-80)
    d.rectangle(inner, fill=WHITE)
    d.rectangle(inner, outline=BRAND_FROM, width=6)
    for cx_, cy_ in [(inner[0], inner[1]), (inner[2], inner[1]),
                     (inner[0], inner[3]), (inner[2], inner[3])]:
        d.rectangle((cx_-14, cy_-14, cx_+14, cy_+14), fill=BRAND_FROM)

    d.text((inner[0]+50, inner[1]+30), "拖拽框选",
           fill=TEXT_DARK, font=F(64))
    d.text((inner[0]+50, inner[1]+115), "想问 AI 的",
           fill=TEXT_DARK, font=F(56))
    d.text((inner[0]+50, inner[1]+195), "任意区域",
           fill=BRAND_FROM, font=F(64))

    paste_emoji(img, "💡", 60, 1290, 44)
    d = ImageDraw.Draw(img)
    d.text((118, 1294), "右键或 Esc 取消框选",
           fill=TEXT_GREY, font=F(36))
    return img

# ---------- Slide 8: 看结果 + 封底 ----------
def slide_step7():
    img = gradient(W, H, BRAND_FROM, BRAND_TO)
    d = ImageDraw.Draw(img)

    # 🎉 emoji big
    paste_emoji(img, "🎉", (W-180)//2, 80, 180)
    d = ImageDraw.Draw(img)

    # title
    title = "搞定！"
    tf = F(130)
    tb = d.textbbox((0, 0), title, font=tf)
    tw_ = tb[2]-tb[0]
    d.text(((W-tw_)//2-tb[0], 290), title, fill=WHITE, font=tf)

    # subtitle
    sub = "几秒后右上角浮动面板出现解读"
    sf = F(40)
    sb = d.textbbox((0, 0), sub, font=sf)
    sw_ = sb[2]-sb[0]
    d.text(((W-sw_)//2-sb[0], 450),
           sub, fill=WHITE, font=sf)

    # result panel illustration
    py = 540
    pw, ph = 800, 540
    px = (W-pw)//2
    d.rounded_rectangle((px, py, px+pw, py+ph), radius=20, fill=WHITE)
    hgrad = gradient(pw, 76, BRAND_FROM, BRAND_TO)
    mask = Image.new("L", (pw, 76), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, pw, 140), radius=20, fill=255)
    img.paste(hgrad, (px, py), mask)
    d = ImageDraw.Draw(img)
    d.text((px+22, py+18), "AI 解读", fill=WHITE, font=F(36))
    d.text((px+pw-90, py+18), "—  ×", fill=WHITE, font=F(40))

    cy = py + 110
    d.rounded_rectangle((px+24, cy, px+pw-24, cy+180),
                        radius=14, fill=(248, 249, 252))
    d.text((px+44, cy+18), "#2  完成", fill=OK, font=F(28))
    d.text((px+44, cy+70), "这段英文意思是「探索",
           fill=TEXT_DARK, font=F(36))
    d.text((px+44, cy+115), "全世界顶尖设计师作品」",
           fill=TEXT_DARK, font=F(36))
    d.text((px+44, cy+165), "Dribbble 主页 hero 标语",
           fill=TEXT_GREY, font=F(26))

    cy2 = cy + 200
    d.rounded_rectangle((px+24, cy2, px+pw-24, cy2+180),
                        radius=14, fill=(248, 249, 252))
    d.text((px+44, cy2+18), "#1  完成", fill=OK, font=F(28))
    d.text((px+44, cy2+70), "图表显示销售转化率",
           fill=TEXT_DARK, font=F(36))
    d.text((px+44, cy2+115), "较上月增长 19%……",
           fill=TEXT_DARK, font=F(36))
    d.text((px+44, cy2+165), "可连续框选，结果累积",
           fill=TEXT_GREY, font=F(26))

    # CTA
    paste_emoji(img, "💝", 60, 1170, 56)
    d = ImageDraw.Draw(img)
    d.text((140, 1180), "觉得好用记得点赞 + 收藏",
           fill=WHITE, font=F(44))

    paste_emoji(img, "👇", 60, 1270, 56)
    d = ImageDraw.Draw(img)
    d.text((140, 1280), "评论区扣 1 私你最新版安装包",
           fill=WHITE, font=F(40))
    return img

slides = [
    ("01-cover.png", slide_cover),
    ("02-step1-unzip.png", slide_step1),
    ("03-step2-extensions.png", slide_step2),
    ("04-step3-load.png", slide_step3),
    ("05-step4-apikey.png", slide_step4),
    ("06-step5-config.png", slide_step5),
    ("07-step6-frame.png", slide_step6),
    ("08-result.png", slide_step7),
]

for name, fn in slides:
    im = fn()
    p = OUT / name
    im.save(p, "PNG", optimize=True)
    print(f"wrote {p} {im.size}")
