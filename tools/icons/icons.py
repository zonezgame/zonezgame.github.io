"""Bộ icon topping ZONE Z – vector phẳng, nét viền nâu đậm, một mảng sáng, một tia flash."""
import json, math, random

INK = "#2b1d16"
SW = 10
def O(w=SW): return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def shadow(cx=256, cy=430, rx=160, ry=20): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity=".16"/>'
def hl(cx, cy, rx, ry, rot=-25, op=.45): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="#fff" opacity="{op}"/>'
def spark(x=410, y=110, s=26, col="#fff"):
    p = f"M{x},{y-s} Q{x+s*.18},{y-s*.18} {x+s},{y} Q{x+s*.18},{y+s*.18} {x},{y+s} Q{x-s*.18},{y+s*.18} {x-s},{y} Q{x-s*.18},{y-s*.18} {x},{y-s}Z"
    return f'<path d="{p}" fill="{col}" {O(6)}/>'
def circ(cx, cy, r, fill, w=SW): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {O(w)}/>'
def ell(cx, cy, rx, ry, fill, rot=0, w=SW): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" transform="rotate({rot} {cx} {cy})" {O(w)}/>'
def dots(pts, r, fill): return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>' for x, y in pts)

def rau_cu_say():
    s = shadow(rx=170)
    # đậu que
    s += f'<rect x="250" y="200" width="120" height="40" rx="20" fill="#6cc04a" transform="rotate(35 310 220)" {O()}/>'
    s += f'<rect x="120" y="300" width="120" height="40" rx="20" fill="#5aae3c" transform="rotate(-25 180 320)" {O()}/>'
    # cà rốt
    for cx, cy in [(200, 250), (318, 318)]:
        s += circ(cx, cy, 62, "#ff8a3d") + f'<circle cx="{cx}" cy="{cy}" r="36" fill="none" stroke="#ffc08f" stroke-width="7"/>' + f'<circle cx="{cx}" cy="{cy}" r="9" fill="#ffc08f"/>'
    # củ dền
    s += circ(375, 380, 40, "#b8467a") + f'<circle cx="375" cy="380" r="22" fill="none" stroke="#e07aa6" stroke-width="5"/>'
    # bắp
    for x, y in [(230, 375), (262, 392), (196, 398), (250, 352)]:
        s += f'<rect x="{x-15}" y="{y-14}" width="30" height="28" rx="9" fill="#ffd34d" {O(7)}/>'
    s += hl(185, 230, 18, 9) + hl(305, 300, 18, 9)
    return s

def tom_vien():
    s = shadow(rx=175)
    random.seed(2)
    for cx, cy in [(180, 320), (332, 320), (256, 200)]:
        s += circ(cx, cy, 82, "#f7d9c8")
        for _ in range(7):
            a = random.uniform(0, 6.28); r = random.uniform(10, 58)
            s += f'<ellipse cx="{cx+math.cos(a)*r:.0f}" cy="{cy+math.sin(a)*r:.0f}" rx="11" ry="6" transform="rotate({random.randint(0,180)} {cx+math.cos(a)*r:.0f} {cy+math.sin(a)*r:.0f})" fill="#ff7a59"/>'
        s += hl(cx-30, cy-38, 24, 12)
    return s

def xuc_xich_lat():
    s = shadow(rx=175)
    s += f'<rect x="70" y="170" width="300" height="104" rx="52" fill="#c2452d" transform="rotate(-18 220 222)" {O()}/>'
    s += hl(170, 205, 70, 12, -18, .35)
    for cx, cy in [(220, 352), (326, 330), (404, 268)]:
        s += circ(cx, cy, 58, "#b33a24") + f'<circle cx="{cx}" cy="{cy}" r="44" fill="#ee9078"/>'
        s += dots([(cx-14, cy-10), (cx+12, cy-16), (cx+4, cy+14), (cx-18, cy+16), (cx+20, cy+8)], 4.5, "#fff3ec")
    return s

def hat_say():
    s = shadow(rx=165)
    # hạnh nhân
    for cx, cy, r in [(170, 300, -30), (300, 220, 20)]:
        s += f'<path d="M{cx},{cy-70} C{cx+50},{cy-30} {cx+46},{cy+40} {cx},{cy+70} C{cx-46},{cy+40} {cx-50},{cy-30} {cx},{cy-70}Z" fill="#b8743d" transform="rotate({r} {cx} {cy})" {O()}/>'
        s += f'<path d="M{cx-14},{cy-30} q10,30 0,60 M{cx+12},{cy-34} q-8,34 4,64" fill="none" stroke="#8f5427" stroke-width="5" transform="rotate({r} {cx} {cy})"/>'
    # hạt điều
    s += f'<path d="M300,330 C300,270 380,250 400,300 C412,330 388,350 370,330 C356,312 336,318 340,346 C344,380 300,380 300,330Z" fill="#f2cc8a" {O()}/>'
    s += f'<path d="M210,170 C210,120 280,105 296,148 C306,172 286,188 272,172 C260,158 244,164 248,186 C252,214 210,214 210,170Z" fill="#f2cc8a" {O()}/>'
    # đậu phộng
    s += f'<path d="M150,390 c-10,-30 30,-50 50,-30 c20,-20 60,0 46,30 c-10,25 -40,25 -48,10 c-8,15 -40,15 -48,-10Z" fill="#d9a35f" {O()}/>'
    s += hl(160, 270, 14, 8) + hl(380, 285, 12, 7)
    return s

def cha_tom():
    s = shadow(rx=170)
    s += f'<path d="M110,280 C100,190 220,170 280,180 C380,190 420,240 410,300 C400,370 300,390 240,385 C150,380 116,340 110,280Z" fill="#e8955a" {O()}/>'
    s += f'<path d="M140,282 C135,215 230,205 280,212 C360,222 385,255 378,298 C370,350 296,360 245,356 C175,350 144,330 140,282Z" fill="#f7c08f"/>'
    for x, y, r in [(210, 260, 0), (300, 250, 40), (270, 320, -30), (340, 310, 10)]:
        s += f'<path d="M{x-22},{y} a22,22 0 1,1 22,22" fill="none" stroke="#ff6f5a" stroke-width="12" stroke-linecap="round" transform="rotate({r} {x} {y})"/>'
    s += hl(190, 228, 30, 12)
    return s

def cha_bo():
    s = shadow(rx=170)
    random.seed(5)
    for cx, cy in [(200, 260), (310, 320)]:
        s += circ(cx, cy, 100, "#7f5a4a") + f'<circle cx="{cx}" cy="{cy}" r="84" fill="#b08b78"/>'
        s += dots([(cx+random.uniform(-62, 62), cy+random.uniform(-62, 62)) for _ in range(16)], 4, INK)
        s += hl(cx-36, cy-44, 22, 10, -25, .35)
    return s

def cha_ca_tam_giac():
    s = shadow(rx=170)
    def tri(cx, cy, sz, rot):
        h = sz*0.87
        top = f"M{cx},{cy-h*0.66} L{cx+sz/2},{cy+h*0.34} L{cx-sz/2},{cy+h*0.34}Z"
        side = f"M{cx+sz/2},{cy+h*0.34} L{cx+sz/2+14},{cy+h*0.34+16} L{cx-sz/2+14},{cy+h*0.34+16} L{cx-sz/2},{cy+h*0.34}Z"
        return f'<g transform="rotate({rot} {cx} {cy})"><path d="{side}" fill="#c98a2c" {O()}/><path d="{top}" fill="#f0b85a" {O()}/><path d="M{cx},{cy-h*0.66+28} L{cx-sz/2+30},{cy+h*0.34-14}" stroke="#fff" stroke-width="10" opacity=".45" stroke-linecap="round"/></g>'
    s += tri(200, 300, 190, -12) + tri(325, 250, 170, 16)
    return s

def banh_gao():
    s = shadow(rx=170)
    for i, (cx, cy) in enumerate([(240, 190), (210, 270), (285, 330)]):
        s += f'<g transform="rotate(-20 {cx} {cy})"><rect x="{cx-120}" y="{cy-34}" width="240" height="68" rx="34" fill="#f8f4ea" {O()}/><ellipse cx="{cx+100}" cy="{cy}" rx="20" ry="32" fill="#ebe2cf" {O(7)}/>{hl(cx-40, cy-16, 60, 8, 0, .8)}</g>'
    return s

def dau_hu_trung():
    s = shadow(rx=165)
    for cx, cy in [(180, 290), (320, 310), (250, 190)]:
        s += f'<path d="M{cx-74},{cy} L{cx-74},{cy+62} A74,28 0 0,0 {cx+74},{cy+62} L{cx+74},{cy}" fill="#f4cf63" {O()}/>'
        s += f'<path d="M{cx-60},{cy+20} L{cx-60},{cy+70}" stroke="#fff" stroke-width="8" opacity=".35" stroke-linecap="round"/>'
        s += ell(cx, cy, 74, 28, "#fff1b3")
        s += hl(cx-22, cy-6, 26, 8, 0, .6)
    return s

def thanh_cua_vien():
    s = shadow(rx=170)
    s += '<defs><clipPath id="c1"><circle cx="190" cy="300" r="84"/></clipPath><clipPath id="c2"><circle cx="325" cy="250" r="84"/></clipPath></defs>'
    for cx, cy, cid in [(190, 300, "c1"), (325, 250, "c2")]:
        s += f'<circle cx="{cx}" cy="{cy}" r="84" fill="#fff6ef"/>'
        s += f'<g clip-path="url(#{cid})">' + "".join(f'<path d="M{cx-100},{cy-60+i*44} Q{cx},{cy-90+i*44} {cx+100},{cy-60+i*44}" stroke="#ff5a3c" stroke-width="18" fill="none"/>' for i in range(4)) + '</g>'
        s += f'<circle cx="{cx}" cy="{cy}" r="84" fill="none" {O()}/>' + hl(cx-32, cy-40, 22, 10)
    return s

def dau_hu_dai():
    s = shadow(rx=170)
    def cube(x, y, a):
        t = f"M{x},{y} L{x+a},{y-a*.5} L{x+2*a},{y} L{x+a},{y+a*.5}Z"
        l = f"M{x},{y} L{x+a},{y+a*.5} L{x+a},{y+a*1.5} L{x},{y+a}Z"
        r = f"M{x+a},{y+a*.5} L{x+2*a},{y} L{x+2*a},{y+a} L{x+a},{y+a*1.5}Z"
        return f'<path d="{l}" fill="#d98e26" {O()}/><path d="{r}" fill="#bb7419" {O()}/><path d="{t}" fill="#ffcf6b" {O()}/>' + dots([(x+a*.7, y-a*.05), (x+a*1.2, y+a*.1), (x+a*.95, y+a*.25)], 5, "#e9a53b")
    s += cube(110, 260, 80) + cube(260, 290, 76) + cube(200, 150, 70)
    return s

def cha_ca_xoan():
    s = shadow(rx=170)
    s += f'<line x1="100" y1="410" x2="390" y2="146" stroke="#8a5a2b" stroke-width="16" stroke-linecap="round"/><line x1="100" y1="410" x2="390" y2="146" stroke="#c8925a" stroke-width="6" stroke-linecap="round"/>'
    for i in range(7):
        t = i/6; x = 140+t*230; y = 375-t*210
        col = "#f0b45a" if i % 2 == 0 else "#d9902f"
        s += ell(round(x), round(y), 46, 30, col, -42+(28 if i % 2 else -28))
    s += hl(190, 320, 16, 7) + hl(280, 240, 16, 7)
    return s

def cha_ca_hinh_thu():
    s = shadow(rx=175)
    # cá
    s += f'<path d="M110,300 C140,240 240,240 270,300 C240,360 140,360 110,300Z" fill="#f2b55c" {O()}/><path d="M268,300 L320,262 L316,338Z" fill="#e39d3d" {O()}/>'
    s += circ(150, 292, 9, "#fff", 5) + f'<circle cx="152" cy="292" r="4" fill="{INK}"/>' + f'<path d="M190,275 q14,25 0,50 M222,278 q12,22 0,44" stroke="#d48a2e" stroke-width="6" fill="none"/>'
    # gấu
    s += circ(330, 190, 30, "#e9a64a") + circ(410, 190, 30, "#e9a64a") + circ(370, 230, 70, "#f0b45a")
    s += dots([(348, 220), (392, 220)], 8, INK) + ell(370, 252, 22, 15, "#ffd89a", 0, 6) + f'<circle cx="370" cy="247" r="6" fill="{INK}"/>'
    # sao
    pts = " ".join(f"{300+math.cos(math.radians(-90+i*36))*(52 if i%2==0 else 24):.0f},{385+math.sin(math.radians(-90+i*36))*(52 if i%2==0 else 24):.0f}" for i in range(10))
    s += f'<polygon points="{pts}" fill="#f7c76a" {O()}/>'
    s += hl(345, 200, 18, 8)
    return '<g transform="translate(-40 -30) scale(1.12)">' + s + '</g>'

def vien_cha_trung_muoi():
    s = shadow(rx=170)
    random.seed(9)
    s += circ(175, 290, 92, "#f1d6b5") + dots([(175+random.uniform(-60, 60), 290+random.uniform(-60, 60)) for _ in range(14)], 4, "#d9b18a") + hl(140, 248, 26, 12)
    s += circ(330, 300, 92, "#f1d6b5") + f'<circle cx="330" cy="300" r="74" fill="#fff4e2"/>'
    s += circ(330, 300, 40, "#ff9f1c", 7) + f'<circle cx="330" cy="300" r="22" fill="#ffc24b"/>' + hl(318, 288, 10, 5, -25, .7)
    return s

def rong_bien_me():
    s = shadow(rx=170)
    s += f'<rect x="120" y="140" width="260" height="210" rx="22" fill="#2f6a4f" transform="rotate(-12 250 245)" {O()}/>'
    s += f'<rect x="140" y="190" width="260" height="210" rx="22" fill="#1f4a35" transform="rotate(8 270 295)" {O()}/>'
    s += "".join(f'<path d="M{160+i*30},{215+i*4} q20,90 0,170" stroke="#2c6047" stroke-width="5" fill="none" transform="rotate(8 270 295)"/>' for i in range(8))
    random.seed(4)
    for _ in range(26):
        x, y = random.uniform(170, 380), random.uniform(215, 380)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="4" transform="rotate({random.randint(0,180)} {x:.0f} {y:.0f})" fill="#f5ecd5"/>'
    return s

def dimsum():
    s = shadow(rx=180)
    s += f'<path d="M86,300 L86,370 A170,48 0 0,0 426,370 L426,300" fill="#c8964f" {O()}/>'
    s += "".join(f'<line x1="{100+i*40}" y1="325" x2="{100+i*40}" y2="395" stroke="#a87734" stroke-width="5"/>' for i in range(9))
    s += ell(256, 300, 170, 48, "#e3b874")
    for cx in [175, 256, 337]:
        cy = 270 if cx != 256 else 250
        s += f'<path d="M{cx-48},{cy+20} L{cx-40},{cy-40} L{cx+40},{cy-40} L{cx+48},{cy+20} A48,16 0 0,1 {cx-48},{cy+20}Z" fill="#ffd56b" {O()}/>'
        s += "".join(f'<line x1="{cx-30+i*15}" y1="{cy-30}" x2="{cx-34+i*17}" y2="{cy+22}" stroke="#e6b444" stroke-width="5"/>' for i in range(5))
        s += ell(cx, cy-42, 40, 13, "#ffe8a8", 0, 7) + circ(cx, cy-46, 11, "#ff7a3d", 6)
    s += hl(140, 240, 10, 18, 10, .5)
    return s

def pho_mai_vang():
    s = shadow(rx=165)
    s += f'<rect x="150" y="130" width="230" height="230" rx="18" fill="#f2b62a" transform="rotate(10 265 245)" {O()}/>'
    s += f'<path d="M120,170 L340,150 Q358,150 358,168 L362,330 Q362,346 346,348 L300,352 Q296,400 274,400 Q254,400 254,354 L136,362 Q118,362 118,344Z" fill="#ffd347" {O()}/>'
    s += hl(170, 200, 50, 14, -5, .5)
    return s

def pho_mai_keo_soi():
    s = shadow(rx=180)
    for i in range(6):
        y = 236 + i*12
        s += f'<path d="M185,{y} C240,{y+50+i*8} 290,{y+50+i*8} 330,{y-6}" fill="none" stroke="#fff1bf" stroke-width="{16-i*1.5}" stroke-linecap="round" {"" if i%2 else 'opacity=".9"'}/>'
    s += f'<g transform="translate(-30 0)"><path d="M80,210 L210,200 Q232,200 232,222 L232,300 Q232,320 212,320 L84,330 Q62,330 62,308 L62,232 Q62,210 80,210Z" fill="#dd9a35" {O()}/>'
    s += ell(220, 262, 24, 52, "#fff1bf", 0, 8) + '</g>'
    s += f'<g transform="translate(30 0)"><path d="M300,190 L428,176 Q450,174 450,196 L452,276 Q452,298 430,300 L306,312 Q284,314 284,292 L284,212 Q284,192 300,190Z" fill="#dd9a35" {O()}/>'
    s += ell(292, 252, 24, 52, "#fff1bf", 0, 8) + dots([(360, 220), (400, 270), (340, 280)], 6, "#b8741f") + hl(370, 206, 30, 8, -5, .45) + '</g>'
    s += '<g transform="translate(-30 0)">' + dots([(110, 240), (150, 290), (180, 236)], 6, "#b8741f") + hl(120, 228, 30, 8, -5, .45) + '</g>' 
    return s

def thit_bo():
    s = shadow(rx=185)
    def slice_(rot, col, dx):
        d = "M150,330 C120,260 170,170 260,160 C350,150 410,210 395,280 C385,330 330,360 260,362 C200,364 165,360 150,330Z"
        marb = "".join(f'<path d="{p}" fill="none" stroke="#ffe0d6" stroke-width="{w}" stroke-linecap="round"/>' for p, w in [
            ("M190,250 C230,230 260,280 300,250", 9), ("M220,310 C260,300 300,330 350,300", 7), ("M280,200 C300,215 330,200 360,225", 6), ("M180,300 C190,290 200,300 210,290", 5)])
        return f'<g transform="translate({dx} 0) rotate({rot} 270 260)"><path d="{d}" fill="{col}" {O()}/>{marb}<path d="M168,322 C150,270 190,190 262,182" fill="none" stroke="#fff" stroke-width="9" opacity=".25" stroke-linecap="round"/></g>'
    s += slice_(-24, "#b83434", -40) + slice_(0, "#cf4040", 0) + slice_(22, "#e04b4b", 40)
    return s

ITEMS = [
 ("rau-cu-say", "Rau củ sấy", 5, rau_cu_say), ("tom-vien", "Tôm viên", 5, tom_vien), ("xuc-xich-lat", "Xúc xích lát", 5, xuc_xich_lat), ("hat-say", "Hạt sấy", 5, hat_say),
 ("cha-tom", "Chả tôm", 6, cha_tom), ("cha-bo", "Chả bò", 6, cha_bo), ("cha-ca-tam-giac", "Chả cá tam giác", 6, cha_ca_tam_giac), ("banh-gao", "Bánh gạo", 6, banh_gao),
 ("dau-hu-trung", "Đậu hủ trứng", 6, dau_hu_trung), ("thanh-cua-vien", "Thanh cua viên", 6, thanh_cua_vien), ("dau-hu-dai", "Đậu hủ dai", 6, dau_hu_dai), ("cha-ca-xoan", "Chả cá xoắn", 6, cha_ca_xoan),
 ("cha-ca-hinh-thu", "Chả cá hình thú", 8, cha_ca_hinh_thu), ("vien-cha-trung-muoi", "Viên chả trứng muối", 8, vien_cha_trung_muoi), ("rong-bien-me", "Rong biển mè", 8, rong_bien_me),
 ("dimsum", "Dimsum", 10, dimsum), ("pho-mai-vang", "Phô mai vàng", 10, pho_mai_vang),
 ("pho-mai-keo-soi", "Phô mai kéo sợi", 15, pho_mai_keo_soi), ("thit-bo", "Thịt bò", 20, thit_bo),
]
TIERS = {5: "#b9c2d0", 6: "#7fd18b", 8: "#62a9ff", 10: "#b993ff", 15: "#ff8a5c", 20: "#ffd36b"}

def svg(body, k, sparkle=True):
    sp = spark(410, 108, 30 if k >= 15 else 24, "#fff" if k < 20 else "#fff6c8") if sparkle else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{body}{sp}</svg>'

if __name__ == "__main__":
    import os, sys
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    meta = []
    for slug, name, k, fn in ITEMS:
        open(f"{out}/{slug}.svg", "w").write(svg(fn(), k))
        meta.append({"slug": slug, "name": name, "k": k, "tz": k*100, "color": TIERS[k]})
    json.dump(meta, open(f"{out}/meta.json", "w"), ensure_ascii=False, indent=1)
    print(len(meta), "icons")
