"""Video ra mắt Zombie TheZone – 1080x1920, 30 fps, 60 giây. Ghép hình trong game + cảnh chơi quay từ game thật."""
import math, os, random, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS, DUR = 1080, 1920, 30, 60
REPO = '/home/claude/zonezgame.github.io'
REC = '/home/claude/work/rec'
TOP = '/tmp/claude-0/-home-claude/d4e43fb9-3395-52fa-bc3f-2b7a49fda871/scratchpad/topping/out/icon'
FD = '/usr/share/fonts/opentype/inter/'
def F(name, size): return ImageFont.truetype(FD + name, size)
BLACK, XB, BOLD, SEMI = 'InterDisplay-Black.otf', 'InterDisplay-ExtraBold.otf', 'Inter-Bold.otf', 'Inter-SemiBold.otf'
OR, CREAM, RED, LIME, GOLD = (255, 181, 71), (246, 242, 234), (255, 77, 77), (205, 232, 107), (255, 211, 107)
random.seed(7)

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def clamp(v, a, b): return max(a, min(b, v))

# ---------- tài nguyên ----------
ART = Image.open(f'{REPO}/img/home.webp').convert('RGB')
def cover(im, w, h):
    s = max(w / im.width, h / im.height); im2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im2.width - w) // 2, 0; return im2.crop((x, y, x + w, y + h))
BG_BLUR = ImageEnhance.Brightness(cover(ART, W, H).filter(ImageFilter.GaussianBlur(28))).enhance(.32)
SPR = {}
def spr(id, k):
    key = (id, k)
    if key not in SPR: SPR[key] = Image.open(f'{REPO}/img/nv/{id}-{k}.webp').convert('RGBA')
    return SPR[key]
SHOT = {n: Image.open(f'{REC}/s/{n}.png').convert('RGB') for n in ['shop1', 'shop2', 'shop3', 'chars']}
POSTER = Image.open(f'{REC}/s/poster.png').convert('RGB'); POSTER = POSTER.crop((0, 196, POSTER.width, min(POSTER.height, 196 + 1985)))
TOPS = [Image.open(f'{TOP}/{n}.png').convert('RGBA') for n in ['thit-bo', 'pho-mai-keo-soi', 'dimsum', 'tom-vien', 'cha-ca-hinh-thu', 'rong-bien-me', 'xuc-xich-lat', 'banh-gao']]
QR = open(f'{REC}/qr.txt').read().split()

def clip_frame(name, i):
    fs = sorted(os.listdir(f'{REC}/{name}')); i = clamp(i, 0, len(fs) - 1)
    return Image.open(f'{REC}/{name}/{fs[i]}').convert('RGB')

# ---------- chữ ----------
def text_w(d, s, f): return d.textlength(s, font=f)
def caption(im, lines, y, size=86, alpha=1.0, shadow=True, font=BLACK, align='c'):
    """lines: list các dòng; mỗi dòng là list (chữ, màu)."""
    if alpha <= 0: return im
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer); f = F(font, size)
    yy = y
    for ln in lines:
        tw = sum(text_w(d, s, f) for s, _ in ln)
        while tw > W - 100 and f.size > 30:
            f = F(font, f.size - 4); tw = sum(text_w(d, s, f) for s, _ in ln)
        x = (W - tw) / 2 if align == 'c' else 80
        for s, col in ln:
            if shadow:
                for dx, dy in ((0, 6), (0, 3)): d.text((x + dx, yy + dy), s, font=f, fill=(0, 0, 0, int(200 * alpha)))
            d.text((x, yy), s, font=f, fill=col + (int(255 * alpha),)); x += text_w(d, s, f)
        yy += int(f.size * 1.18)
    im = im.convert('RGBA'); im.alpha_composite(layer); return im.convert('RGB')

def band(im, y0, y1, a=.62):
    """dải tối mờ sau chữ"""
    arr = np.asarray(im).astype(np.float32); h = y1 - y0
    m = np.zeros((H, 1, 1), np.float32)
    for y in range(max(0, y0), min(H, y1)):
        t = (y - y0) / h; m[y] = a * math.sin(math.pi * t) ** .6
    arr = arr * (1 - m); return Image.fromarray(arr.astype(np.uint8))

def vignette(im, a, col=(150, 0, 18)):
    if a <= 0: return im
    if not hasattr(vignette, 'M'):
        yy, xx = np.mgrid[0:H, 0:W]; dd = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.25
        vignette.M = np.clip((dd - .32) / .68, 0, 1) ** 1.3
    m = Image.fromarray((vignette.M * 255 * min(1, a)).astype(np.uint8))
    return Image.composite(Image.new('RGB', (W, H), col), im, m)

def fade(im, a, col=(0, 0, 0)):
    if a <= 0: return im
    return Image.blend(im, Image.new('RGB', im.size, col), min(1, a))

def paste_c(im, src, cx, cy, size, alpha=1.0, rot=0):
    s = src.resize((size, size), Image.LANCZOS) if src.width != size else src
    if rot: s = s.rotate(rot, resample=Image.BICUBIC)
    if alpha < 1: a = s.getchannel('A').point(lambda v: int(v * alpha)); s = s.copy(); s.putalpha(a)
    im = im.convert('RGBA'); im.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2))); return im.convert('RGB')

def phone(im, shot, cx, cy, scale, scroll=0):
    """khung điện thoại bo góc"""
    w, h = int(1080 * scale), int(1920 * scale)
    src = shot.resize((w, int(shot.height * scale)), Image.LANCZOS).crop((0, scroll, w, scroll + h))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(70 * scale), fill=255)
    frame = Image.new('RGBA', (w + 28, h + 28), (0, 0, 0, 0)); fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle((0, 0, w + 27, h + 27), radius=int(70 * scale) + 14, fill=(18, 20, 28, 255), outline=(255, 181, 71, 255), width=4)
    frame.paste(src, (14, 14), m)
    im = im.convert('RGBA'); im.alpha_composite(frame, (int(cx - frame.width / 2), int(cy - frame.height / 2))); return im.convert('RGB')

TIER = {1: ('THƯỜNG', (185, 194, 208)), 2: ('HIẾM', (98, 169, 255)), 3: ('ĐỘT BIẾN', (185, 147, 255)), 4: ('BOSS', (255, 107, 74)), 5: ('HUYỀN THOẠI', (255, 211, 107))}
CHARS = [('ngugat', 'Ngủ Gật', 1, (40, 70, 140)), ('deadline', 'Deadline', 1, (130, 50, 30)), ('trasua', 'Trà Sữa', 1, (140, 40, 100)),
         ('songao', 'Sống Ảo', 2, (80, 60, 160)), ('shipper', 'Shipper', 2, (150, 30, 30)), ('onthi', 'Ôn Thi', 3, (90, 40, 130)),
         ('doidem', 'Đói Đêm', 3, (70, 30, 140)), ('bingo', 'Bí Ngô', 4, (170, 70, 10)), ('ceo', 'CEO', 5, (150, 110, 20))]

def radial_bg(col):
    yy, xx = np.mgrid[0:H, 0:W]; dd = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .45) / H) ** 2)
    k = np.clip(1 - dd * 1.6, 0, 1)[..., None]
    base = np.array([8, 10, 18], np.float32); c = np.array(col, np.float32)
    return Image.fromarray((base + (c - base) * k).astype(np.uint8))
CBG = {c[0]: radial_bg(c[3]) for c in CHARS}

def chip(im, text, col, cy):
    d = ImageDraw.Draw(im); f = F(BOLD, 40); tw = text_w(d, text, f)
    d.rounded_rectangle((W / 2 - tw / 2 - 28, cy - 34, W / 2 + tw / 2 + 28, cy + 34), radius=34, outline=col, width=4)
    d.text((W / 2, cy), text, font=f, fill=col, anchor='mm'); return im

# ---------- các cảnh ----------
def s_hook(t):  # 0–3.5
    sc = 1.08 + .04 * t / 3.5; hh = int(H * sc); big = ART.resize((round(ART.width * hh / ART.height), hh), Image.LANCZOS)
    x = int((big.width - W) * .5); im = big.crop((x, int((hh - H) * .3), x + W, int((hh - H) * .3) + H)).filter(ImageFilter.GaussianBlur(22))
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(.6)).enhance(.38)
    im = Image.blend(im, Image.new('RGB', im.size, (10, 16, 34)), .35)
    a1 = ease((t - .2) / .4); a2 = ease((t - 1.2) / .4); a3 = ease((t - 2.2) / .3)
    im = caption(im, [[('Gặp zombie,', CREAM)]], 640, 110, a1)
    im = caption(im, [[('mấy ní chạy…', CREAM)]], 790, 110, a2)
    if a3 > 0:
        sc = 1 + .25 * (1 - ease((t - 2.2) / .25))
        im = caption(im, [[('hay ', CREAM), ('CHỤP?', OR)]], 1000, int(170 * sc), a3)
    return im

def s_title(t):  # 3.5–8
    k = t / 4.5; sc = 1.0 + .10 * k
    hh = int(H * sc); big = ART.resize((round(ART.width * hh / ART.height), hh), Image.LANCZOS); x = int((big.width - W) * (.0 + .45 * ease(k))); im = big.crop((x, 0, x + W, H))
    im = fade(im, 1 - ease(t / .25), (255, 255, 255)) if t < .25 else im
    im = band(im, 1330, 1780, .75)
    im = caption(im, [[('Game camera săn zombie', CREAM)]], 1430, 66, ease((t - .6) / .5), font=XB)
    im = caption(im, [[('của ', CREAM), ('THEZONE', OR)]], 1530, 66, ease((t - .9) / .5), font=XB)
    return im

CAP_CURE = [(0, 3.2, [[('Xoay máy.', CREAM)], [('Tìm zombie.', OR)]]),
            (3.2, 7.0, [[('Chờ nó lại gần…', CREAM)], [('flash mạnh hơn.', OR)]]),
            (7.0, 9.5, [[('CHỤP!', OR)]]),
            (9.5, 11.5, [[('Zombie tỉnh lại.', CREAM)], [('Ưng hết ý.', LIME)]])]
def s_cure(t):  # 8–19.5 (11.5s) từ khung 70
    im = clip_frame('cure', 70 + int(t * 30))
    for a, b, lines in CAP_CURE:
        if a <= t < b:
            al = min(ease((t - a) / .25), ease((b - t) / .25))
            im = band(im, 1240, 1560, .7); im = caption(im, lines, 1300, 92 if len(lines) > 1 else 150, al)
    return im

CAP_BITE = [(0, 2.8, [[('Càng gần,', CREAM)], [('càng hồi hộp.', OR)]]),
            (2.8, 4.6, [[('Tim đập thình thịch…', CREAM)]]),
            (5.0, 8.0, [[('Chậm một nhịp', CREAM)], [('là hoá zombie 30 phút.', LIME)]])]
def soft(im):
    """giảm đỏ, giảm bão hoà cho cảnh rượt"""
    a = np.asarray(im).astype(np.float32); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = np.clip((r - np.maximum(g, b)) / 120, 0, 1)
    a[..., 0] = r - red * (r - (g + b) / 2) * .75
    return ImageEnhance.Color(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))).enhance(.7)
def s_bite(t):  # 19.5–27.5
    if t < 4.7: fr = clip_frame('bite', 135 + int(t * 18))        # chậm lại, dừng ở ~5 m, chưa cận mặt
    else: fr = clip_frame('bite', 345)                           # thẻ kết quả "Bạn bị cắn!" (nền xanh)
    im = BG_BLUR.copy(); im = phone(im, soft(fr), W / 2, 860, .66)
    for a, b, lines in CAP_BITE:
        if a <= t < b:
            al = min(ease((t - a) / .25), ease((b - t) / .25))
            im = band(im, 1560, 1900, .8); im = caption(im, lines, 1640, 80, al)
    if 4.6 <= t < 4.8: im = fade(im, 1 - abs(t - 4.7) / .1, (255, 255, 255))
    return im

def s_chars(t):  # 27.5–36.5: 9 nhân vật x 1s
    i = min(8, int(t)); k = t - i; cid, nm, tier, col = CHARS[i]
    im = CBG[cid].copy()
    human = k >= .55
    if not human:
        bob = abs(math.sin(k * math.pi * 3.2)) * 18; rot = math.sin(k * math.pi * 3.2) * 3
        im = paste_c(im, spr(cid, 'z'), W / 2, 930 - bob, 1080, 1, rot)
    else:
        kk = (k - .55) / .45
        im = paste_c(im, spr(cid, 'h'), W / 2, 930 - 20 * ease(kk), 1080)
    if .5 <= k < .7: im = fade(im, 1 - (k - .5) / .2, (255, 255, 255))
    d = ImageDraw.Draw(im)
    if i == 0 and k < .35: im = caption(im, [[('9 zombie', CREAM)], [('chờ mấy ní cứu', OR)]], 160, 84, ease(k / .2))
    else: im = caption(im, [[(('Zombie ' + nm) if not human else (nm + ' · đã tỉnh'), CREAM if not human else LIME)]], 210, 76)
    tn, tc = TIER[tier]; im = chip(im, tn, tc, 1690)
    return im

def s_reward(t):  # 36.5–44.5 (8s)
    im = radial_bg((120, 80, 10)); im = fade(im, .25)
    # đồng TZ đếm lên
    if t < 3.2:
        n = int(2450 * ease(t / 1.8)); a = ease(t / .3) * (1 - ease((t - 2.9) / .3))
        im = caption(im, [[('Chữa zombie', CREAM)], [('nhận ', CREAM), ('TZ đồng', OR)]], 520, 96, a)
        im = caption(im, [[(f'+{n:,}'.replace(',', '.') + ' TZ', GOLD)]], 900, 170, a)
    else:
        tt = t - 3.2
        im = caption(im, [[('Đổi ', CREAM), ('topping thật', OR)], [('tại THEZONE', CREAM)]], 300, 92, ease(tt / .3))
        for j, ic in enumerate(TOPS):
            r, c = divmod(j, 4); x = 180 + c * 240; y = 820 + r * 280
            a = ease((tt - .25 - j * .12) / .25)
            if a > 0: im = paste_c(im, ic, x, y + (1 - a) * 60, 220, a)
        im = caption(im, [[('+ frame photobooth ', CREAM), ('M BOOTH', LIME)]], 1500, 64, ease((tt - 1.6) / .4), font=XB)
    return im

def s_shop(t):  # 44.5–50.5 (6s)
    im = BG_BLUR.copy()
    if t < 4:
        sh = SHOT['shop1'] if t < 1.3 else SHOT['shop2'] if t < 2.6 else SHOT['shop3']
        im = phone(im, sh, W / 2, 1080, .66)
        im = caption(im, [[('Shop', OR)], [('khung avatar · ống ngắm', CREAM)], [('hiệu ứng flash', CREAM)]], 90, 72, ease(t / .3) * (1 - ease((t - 3.7) / .3)))
    else:
        tt = t - 4; im = radial_bg((140, 100, 10)); im = fade(im, .2)
        im = caption(im, [[('Hết flash?', CREAM)], [('Ghé ', CREAM), ('Trạm nạp', OR), (' là đầy.', CREAM)]], 300, 88, ease(tt / .3))
        d = ImageDraw.Draw(im); cx, cy, r = W / 2, 930, 190
        pul = .5 + .5 * math.sin(tt * 9)
        for k in range(6, 0, -1): d.ellipse((cx - r - k * 14, cy - r - k * 14, cx + r + k * 14, cy + r + k * 14), outline=(255, 190, 60, ), width=2) if k % 2 else None
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(28, 22, 8), outline=(255, 211, 107), width=10)
        bolt = [(cx + 20, cy - 130), (cx - 90, cy + 20), (cx - 10, cy + 20), (cx - 40, cy + 140), (cx + 95, cy - 25), (cx + 10, cy - 25)]
        d.polygon(bolt, fill=(255, int(200 + 40 * pul), 70))
        n = min(15, int(15 * ease((tt - .2) / 1.2))); pw, gap = 46, 10; x0 = W / 2 - (15 * pw + 14 * gap) / 2
        for i in range(15): d.rounded_rectangle((x0 + i * (pw + gap), 1240, x0 + i * (pw + gap) + pw, 1300), radius=8, fill=(255, 211, 107) if i < n else (60, 60, 70))
        im = caption(im, [[(f'FLASH {n}/15', GOLD)]], 1340, 70, 1, font=XB)
        im = caption(im, [[('Trạm nạp ở các cửa hàng đối tác', (220, 222, 230))]], 1480, 50, ease((tt - .5) / .4), font=SEMI)
    return im

def s_event(t):  # 50.5–55 (4.5s)
    im = CBG['bingo'].copy(); im = vignette(im, .55, (120, 20, 0))
    sc = 1080 + int(140 * ease(t / 4.5)); shake = (random.uniform(-6, 6) if t > 1.2 else 0)
    im = paste_c(im, spr('bingo', 'z'), W / 2 + shake, 1050, sc)
    im = caption(im, [[('MÙA HALLOWEEN', OR)]], 150, 104, ease(t / .3))
    im = caption(im, [[('24/10 – 2/11', CREAM)]], 290, 84, ease((t - .3) / .3))
    im = band(im, 1560, 1840, .8)
    im = caption(im, [[('Boss Bí Ngô đã thức dậy.', CREAM)]], 1650, 70, ease((t - 1.0) / .4), font=XB)
    return im

def qr_img(size):
    n = len(QR); cell = size // (n + 8); s = cell * (n + 8)
    im = Image.new('RGB', (s, s), (255, 255, 255)); d = ImageDraw.Draw(im)
    for r, row in enumerate(QR):
        for c, ch in enumerate(row):
            if ch == '1': d.rectangle(((c + 4) * cell, (r + 4) * cell, (c + 5) * cell - 1, (r + 5) * cell - 1), fill=(11, 16, 25))
    return im
QRI = qr_img(380)
def s_cta(t):  # 55–60
    big = ART.resize((round(ART.width * H / ART.height), H), Image.LANCZOS).crop((0, 0, W, H)); im = ImageEnhance.Brightness(big).enhance(.42)
    im = band(im, 640, 1900, .7)
    im = caption(im, [[('RA MẮT', CREAM)]], 700, 150, ease(t / .3))
    im = caption(im, [[('TỐI NAY · 16/10', OR)]], 880, 96, ease((t - .3) / .3))
    im = caption(im, [[('Mở camera. Săn zombie.', CREAM)]], 1080, 70, ease((t - .7) / .4), font=XB)
    im = caption(im, [[('Đổi topping thật.', LIME)]], 1170, 70, ease((t - 1.0) / .4), font=XB)
    im = caption(im, [[('👉 Link ở bio', GOLD)]] if False else [[('Link chơi ở bio', GOLD)]], 1330, 76, ease((t - 1.4) / .4))
    im = caption(im, [[('THEZONE · Lê Duẩn, Phú Mỹ, Phú Tân', (200, 205, 215))]], 1500, 42, ease((t - 1.7) / .4), font=SEMI)
    if t > 4.6: im = fade(im, (t - 4.6) / .4)
    return im

SCENES = [(0, 3.5, s_hook), (3.5, 8, s_title), (8, 19.5, s_cure), (19.5, 27.5, s_bite), (27.5, 36.5, s_chars),
          (36.5, 44.5, s_reward), (44.5, 50.5, s_shop), (50.5, 55, s_event), (55, 60, s_cta)]
def frame(n):
    t = n / FPS
    for a, b, fn in SCENES:
        if a <= t < b:
            im = fn(t - a)
            if t - a < .12 and a > 0 and fn not in (s_title,): im = fade(im, 1 - (t - a) / .12)
            return im
    return Image.new('RGB', (W, H))

if __name__ == '__main__':
    out = sys.argv[1]; only = sys.argv[2:] and [float(x) for x in sys.argv[2:]]
    if only:
        for t in only: frame(int(t * FPS)).save(f'{REC}/chk_{t:05.1f}.png')
        sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', out], stdin=subprocess.PIPE)
    for n in range(DUR * FPS):
        p.stdin.write(frame(n).tobytes())
        if n % 300 == 0: print('frame', n, flush=True)
    p.stdin.close(); p.wait(); print('done', out)
