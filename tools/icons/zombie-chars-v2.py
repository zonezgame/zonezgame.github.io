"""Nhân vật ZONE Z – chibi vector, 2 trạng thái: zombie (z) và đã chữa (h). Cùng nét với icon topping."""
import json, math, os, sys

INK = "#2b1d16"
def O(w=9): return f'stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def circ(cx, cy, r, f, w=9): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" {O(w)}/>'
def ell(cx, cy, rx, ry, f, rot=0, w=9): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{f}" transform="rotate({rot} {cx} {cy})" {O(w)}/>'
def rr(x, y, w, h, r, f, rot=None, sw=9):
    t = f' transform="rotate({rot[0]} {rot[1]} {rot[2]})"' if rot else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"{t} {O(sw)}/>'
def line(x1, y1, x2, y2, col, w): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
def hl(cx, cy, rx, ry, rot=-25, op=.45): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="#fff" opacity="{op}"/>'
def spark(x, y, s, col="#fff"):
    return f'<path d="M{x},{y-s} Q{x+s*.18},{y-s*.18} {x+s},{y} Q{x+s*.18},{y+s*.18} {x},{y+s} Q{x-s*.18},{y+s*.18} {x-s},{y} Q{x-s*.18},{y-s*.18} {x},{y-s}Z" fill="{col}" {O(5)}/>'

ZSKIN, ZSHADE, ZBAG = "#8a9f84", "#55684f", "#3f4d3c"
def mixc(a, b, k):
    A = [int(a[i:i+2], 16) for i in (1, 3, 5)]; B = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x+(y-x)*k):02x}" for x, y in zip(A, B))
def zcloth(c): return mixc(c, "#4f5650", .5)
DEFS = '<defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter></defs>'

HSKIN, HSHADE = "#f4c6a0", "#e3a982"

# ---------- vật cầm tay (vẽ quanh điểm tay x,y) ----------
def item(name, x, y, st):
    z = st == "z"
    if name == "pillow":
        return rr(x-46, y-30, 92, 60, 22, "#f3f0ff") + line(x-30, y-14, x+28, y-14, "#d9d2f5", 5)
    if name == "papers":
        s = ""
        for i, r in enumerate([-14, 6, 18] if z else [0, 4, 8]):
            s += rr(x-34+i*(10 if z else 3), y-50-i*(14 if z else 4), 70, 86, 6, "#fbf8ef", (r, x, y-10), 7)
        s += line(x-18, y-30, x+20, y-30, "#b9c0cc", 5) + line(x-18, y-16, x+20, y-16, "#b9c0cc", 5)
        if not z: s += f'<path d="M{x-12},{y+2} l10,10 l20,-24" fill="none" stroke="#3fb56b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
        return s
    if name == "cup":
        s = f'<path d="M{x-32},{y-60} L{x+32},{y-60} L{x+24},{y+30} L{x-24},{y+30}Z" fill="#d8b08a" {O(8)}/>'
        s += f'<path d="M{x-34},{y-60} A34,22 0 0,1 {x+34},{y-60}Z" fill="#f6f2ff" {O(8)}/>' + line(x+8, y-100, x, y-64, "#ef5d7c", 9)
        s += "".join(f'<circle cx="{x-14+i*14}" cy="{y+14}" r="7" fill="{INK}"/>' for i in range(3))
        return s
    if name == "phone":
        return rr(x-24, y-74, 48, 82, 10, "#1c1f27", None, 8) + f'<rect x="{x-17}" y="{y-66}" width="34" height="62" rx="5" fill="{"#7fd0ff" if not z else "#bfe9ff"}"/>'
    if name == "box":
        return rr(x-58, y-50, 116, 92, 8, "#d9a866") + f'<rect x="{x-58}" y="{y-12}" width="116" height="14" fill="#b88442"/>' + f'<rect x="{x-8}" y="{y-50}" width="16" height="92" fill="#f2e3c4" opacity=".8"/>'
    if name == "book":
        s = f'<path d="M{x-62},{y-38} Q{x-30},{y-50} {x},{y-36} Q{x+30},{y-50} {x+62},{y-38} L{x+62},{y+30} Q{x+30},{y+18} {x},{y+32} Q{x-30},{y+18} {x-62},{y+30}Z" fill="#fbf8ef" {O(8)}/>'
        s += line(x, y-36, x, y+32, INK, 6) + "".join(line(x-50, y-24+i*12, x-12, y-28+i*12, "#b9c0cc", 4) + line(x+12, y-28+i*12, x+50, y-24+i*12, "#b9c0cc", 4) for i in range(4))
        if not z: s += circ(x+44, y-46, 20, "#ff6f5c", 6) + f'<text x="{x+44}" y="{y-39}" font-family="Inter Display,Inter,sans-serif" font-weight="900" font-size="18" fill="#fff" text-anchor="middle">A+</text>'
        return s
    if name == "bowl":
        s = f'<path d="M{x-62},{y-22} A62,46 0 0,0 {x+62},{y-22}Z" fill="#c0392b" {O(8)}/>' + ell(x, y-22, 62, 14, "#f3d27a", 0, 7)
        s += line(x+20, y-90, x-6, y-24, "#c8925a", 7) + line(x+36, y-86, x+6, y-24, "#c8925a", 7)
        s += "".join(f'<path d="M{x-30+i*22},{y-40} q12,-16 0,-32 q-12,-16 0,-30" fill="none" stroke="#fff" stroke-width="6" opacity=".55" stroke-linecap="round"/>' for i in range(3))
        return s
    if name == "tablet":
        s = rr(x-54, y-74, 108, 82, 10, "#1c1f27", None, 8) + f'<rect x="{x-46}" y="{y-66}" width="92" height="66" rx="5" fill="#f8f6ef"/>'
        pts = [(x-38, y-14), (x-14, y-26), (x+8, y-20), (x+36, y-56)] if not z else [(x-38, y-50), (x-14, y-36), (x+8, y-44), (x+36, y-16)]
        s += f'<polyline points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="none" stroke="{"#3fb56b" if not z else "#e5484d"}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        return s
    if name == "redpen":
        return f'<g transform="rotate(-35 {x} {y})">' + rr(x-9, y-70, 18, 80, 6, "#e5484d", None, 7) + f'<path d="M{x-9},{y+10} L{x},{y+28} L{x+9},{y+10}Z" fill="#f3e0c4" {O(6)}/></g>'
    if name == "flower":
        s = line(x, y+20, x, y-40, "#3e8f4f", 8)
        for a in range(5):
            px, py = x+math.cos(a*1.256)*20, y-58+math.sin(a*1.256)*20
            s += circ(round(px), round(py), 16, "#ff9fb8", 6)
        return s + circ(x, y-58, 12, "#ffd36b", 6)
    if name == "bucket":
        s = f'<path d="M{x-44},{y-40} L{x+44},{y-40} L{x+36},{y+30} L{x-36},{y+30}Z" fill="#ff8a2b" {O(8)}/>'
        s += f'<path d="M{x-44},{y-40} Q{x},{y-110} {x+44},{y-40}" fill="none" {O(7)}/>' + f'<path d="M{x-20},{y-14} l10,-12 l10,12Z M{x+0},{y-14} l10,-12 l10,12Z" fill="{INK}"/>' + f'<path d="M{x-22},{y+8} q22,14 44,0" fill="none" {O(6)}/>'
        if not z: s += circ(x-14, y-46, 10, "#e5484d", 5) + circ(x+12, y-50, 10, "#62a9ff", 5)
        return s
    if name == "sack":
        return f'<path d="M{x-50},{y+40} Q{x-70},{y-40} {x-20},{y-60} L{x+20},{y-60} Q{x+70},{y-40} {x+50},{y+40}Z" fill="#b8743d" {O(8)}/>' + line(x-24, y-58, x+24, y-58, "#ffd36b", 9)
    return ""

# ---------- mũ / tóc ----------
def hair(p, z, hx, hy, R):
    c = p["hair"]; style = p.get("hairstyle", "short")
    s = ""
    if style == "bun": s += circ(hx, hy-R-12, 34, c)
    if style == "pony": s += ell(hx+R-6, hy+10, 26, 54, c, -15)
    cap = f'M{hx-R-4},{hy+6} C{hx-R-6},{hy-R*1.2} {hx+R+6},{hy-R*1.2} {hx+R+4},{hy+6} '
    if style == "slick":
        cap += f'C{hx+R-20},{hy-40} {hx-10},{hy-56} {hx-R+10},{hy-30} Z'
    elif z:
        cap += "".join(f'L{hx+R-i*(2*R/7)},{hy-36+(18 if i%2 else -6)} ' for i in range(8)) + 'Z'
    else:
        cap += f'Q{hx+R/2},{hy-60} {hx},{hy-44} Q{hx-R/2},{hy-62} {hx-R-4},{hy+6}Z'
    s += f'<path d="{cap}" fill="{c}" {O()}/>'
    if z and style != "slick":
        s += f'<path d="M{hx-20},{hy-R-2} q-6,-26 10,-34 M{hx+18},{hy-R} q14,-24 -2,-36" fill="none" {O(7)}/>'
    return s

def headwear(p, z, hx, hy, R):
    w = p.get("hat")
    if w == "nightcap":
        tip = (hx+R+30, hy-R+30) if z else (hx+R+10, hy-R-30)
        return f'<path d="M{hx-R-6},{hy-34} Q{hx-20},{hy-R*1.45} {tip[0]},{tip[1]} Q{hx+R-10},{hy-R*.6} {hx+R+6},{hy-30}Z" fill="#7b8fe0" {O()}/>' + rr(hx-R-12, hy-50, 2*R+24, 30, 14, "#f3f0ff") + circ(tip[0], tip[1], 16, "#f3f0ff", 7)
    if w == "helmet":
        return f'<path d="M{hx-R-10},{hy-6} A{R+10},{R+6} 0 0,1 {hx+R+10},{hy-6}Z" fill="#2fae6a" {O()}/>' + rr(hx-R-14, hy-14, 2*R+28, 18, 8, "#24894f") + hl(hx-36, hy-R+10, 28, 10)
    if w == "santa":
        tip = (hx+R+20, hy-R+50) if z else (hx+R+4, hy-R-10)
        return f'<path d="M{hx-R-6},{hy-34} Q{hx-10},{hy-R*1.5} {tip[0]},{tip[1]} Q{hx+R-14},{hy-R*.55} {hx+R+6},{hy-30}Z" fill="#d93636" {O()}/>' + rr(hx-R-14, hy-52, 2*R+28, 32, 15, "#fbfbfb") + circ(tip[0], tip[1], 17, "#fbfbfb", 7)
    if w == "cap":
        return f'<path d="M{hx-R-2},{hy-24} A{R+2},{R} 0 0,1 {hx+R+2},{hy-24}Z" fill="#5a4f8a" {O()}/>' + rr(hx-20, hy-34, R+60, 18, 9, "#4a4078")
    return ""

def glasses(p, z, hx, hy):
    if not p.get("glasses"): return ""
    col = p.get("glasses_col", INK)
    t = 'transform="rotate(-8 %d %d)"' % (hx, hy) if z else ''
    return f'<g {t}><circle cx="{hx-38}" cy="{hy+4}" r="27" fill="#fff" fill-opacity=".25" stroke="{col}" stroke-width="7"/><circle cx="{hx+38}" cy="{hy+4}" r="27" fill="#fff" fill-opacity=".25" stroke="{col}" stroke-width="7"/><line x1="{hx-11}" y1="{hy+2}" x2="{hx+11}" y2="{hy+2}" stroke="{col}" stroke-width="7"/></g>'

def face(p, z, hx, hy, R):
    if z:
        eye = p.get("eye", "#e4ff6e")
        s = f'<ellipse cx="{hx-38}" cy="{hy+6}" rx="32" ry="28" fill="{ZBAG}" opacity=".75"/><ellipse cx="{hx+38}" cy="{hy+12}" rx="26" ry="22" fill="{ZBAG}" opacity=".75"/>'
        # vết nứt + sẹo khâu
        s += f'<path d="M{hx-70},{hy-40} l14,10 l-4,14 l12,8 M{hx+60},{hy+36} l-10,10 l6,12" fill="none" stroke="#2f3a2d" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        s += line(hx+44, hy+44, hx+78, hy+28, "#2f3a2d", 5) + "".join(line(hx+48+i*10, hy+34-i*5, hx+54+i*10, hy+48-i*5, "#2f3a2d", 3) for i in range(3))
        if p.get("sleepy"):
            s += f'<path d="M{hx-62},{hy+4} q24,16 48,0" fill="#2a3328" {O(7)}/><path d="M{hx+16},{hy+10} q22,14 44,0" fill="#2a3328" {O(7)}/>'
            s += f'<circle cx="{hx-38}" cy="{hy+10}" r="20" fill="{eye}" opacity=".55" filter="url(#gl)"/>' + f'<path d="M{hx-52},{hy+8} q14,8 28,0" stroke="{eye}" stroke-width="5" fill="none"/>'
        else:
            s += f'<circle cx="{hx-38}" cy="{hy+6}" r="28" fill="{eye}" opacity=".6" filter="url(#gl)"/><circle cx="{hx+38}" cy="{hy+12}" r="20" fill="{eye}" opacity=".5" filter="url(#gl)"/>'
            s += circ(hx-38, hy+6, 18, eye, 6) + f'<circle cx="{hx-34}" cy="{hy+8}" r="5" fill="#d7263d"/>'
            s += circ(hx+38, hy+12, 11, eye, 6) + f'<circle cx="{hx+39}" cy="{hy+13}" r="3.5" fill="#d7263d"/>'
        s += f'<path d="M{hx-66},{hy-24} L{hx-18},{hy-12} M{hx+18},{hy-8} L{hx+62},{hy-22}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        # miệng rộng nhiều răng
        s += f'<path d="M{hx-40},{hy+44} Q{hx},{hy+36} {hx+40},{hy+46} Q{hx+34},{hy+82} {hx},{hy+84} Q{hx-36},{hy+82} {hx-40},{hy+44}Z" fill="#2a1414" {O(7)}/>'
        s += "".join(f'<path d="M{hx-32+i*13},{hy+44-(i%2)} l6,13 l6,-13Z" fill="#efe4bd"/>' for i in range(5))
        s += "".join(f'<path d="M{hx-22+i*14},{hy+80} l6,-11 l6,11Z" fill="#efe4bd"/>' for i in range(3))
        s += f'<path d="M{hx+22},{hy+78} q4,22 -2,34" stroke="#b9d88a" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"/><circle cx="{hx+20}" cy="{hy+114}" r="5" fill="#b9d88a" opacity=".85"/>'
        return s
    s = f'<ellipse cx="{hx-58}" cy="{hy+36}" rx="17" ry="10" fill="#ff8f9a" opacity=".55"/><ellipse cx="{hx+58}" cy="{hy+36}" rx="17" ry="10" fill="#ff8f9a" opacity=".55"/>'
    if p.get("happy_closed"):
        s += f'<path d="M{hx-54},{hy+10} q16,-18 32,0 M{hx+22},{hy+10} q16,-18 32,0" fill="none" {O(8)}/>'
    else:
        for d in (-1, 1):
            s += f'<circle cx="{hx+d*38}" cy="{hy+6}" r="12" fill="{INK}"/><circle cx="{hx+d*38+4}" cy="{hy+1}" r="4.5" fill="#fff"/>'
    s += f'<path d="M{hx-24},{hy+40} Q{hx},{hy+74} {hx+24},{hy+40}Z" fill="#7a2f2f" {O(7)}/><path d="M{hx-10},{hy+56} q10,10 20,0" fill="#ff8f8f"/>'
    return s

def pumpkin_head(hx, hy, R, z, k=1):
    s = ""
    for o in (-0.5, 0, 0.5):
        s += ell(round(hx+o*R*.9), hy+6, round(R*.62), R, "#ff8a2b")
    s += rr(hx-10, hy-R-22, 20, 30, 6, "#3f7a3a", None, 7)
    glow = "#ffe28a"
    if z:
        s += f'<circle cx="{hx}" cy="{hy+10}" r="70" fill="#ff7a00" opacity=".45" filter="url(#gl)"/>'
        s += f'<path d="M{hx-80},{hy+40} q4,30 -2,46 M{hx+70},{hy+50} q6,24 0,40" stroke="#3a2a1a" stroke-width="8" stroke-linecap="round" fill="none"/>'
        s += f'<g fill="{glow}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"><path d="M{hx-56},{hy-10} l30,-26 l12,34Z"/><path d="M{hx+56},{hy-10} l-30,-26 l-12,34Z"/>'
        s += f'<path d="M{hx-58},{hy+30} l14,14 l14,-14 l14,14 l14,-14 l14,14 l14,-14 l14,14 l16,-14 q-10,48 -60,48 q-50,0 -64,-48Z"/></g>'
    return s

def body(p, z):
    shirt, pants = p["shirt"], p.get("pants", "#2f3646")
    if z: shirt, pants = zcloth(shirt), zcloth(pants)
    s = ""
    # chân
    s += rr(208, 392, 40, 50, 14, pants) + rr(264, 392, 40, 50, 14, pants)
    s += ell(224, 446, 30, 14, "#1c1f27", 0, 7) + ell(290, 446, 30, 14, "#1c1f27", 0, 7)
    # thân áo
    if z:
        hem = "".join(f'L{330-i*18.6:.0f},{404 if i%2 else 390} ' for i in range(9))
        s += f'<path d="M196,282 Q256,262 316,282 L332,392 {hem} L180,392 Z" fill="{shirt}" {O()}/>'
        s += ell(296, 330, 14, 10, "#14171d", 20, 5) + ell(214, 370, 10, 7, "#14171d", -10, 5)
        s += '<g opacity=".32" fill="#3b2f22">' + ell(236, 304, 22, 12, "#3b2f22", 10, 0) + ell(304, 376, 18, 10, "#3b2f22", -20, 0) + '</g>'
    else:
        s += f'<path d="M196,282 Q256,262 316,282 L332,400 Q256,412 180,400 Z" fill="{shirt}" {O()}/>'
    d = p.get("detail")
    if d == "stars":
        s += "".join(spark(x, y, 9, "#fff5c2") for x, y in [(222, 318), (282, 300), (300, 362), (236, 372)])
    if d == "tie":
        s += f'<path d="M244,282 L268,282 L262,300 L270,360 L256,378 L242,360 L250,300Z" fill="{p.get("tie","#c0392b")}" {O(7)}/>'
        s += f'<path d="M224,276 L256,300 L288,276" fill="{p.get("collar","#fbfbfb")}" {O(7)}/>'
    if d == "apron":
        s += rr(214, 300, 84, 96, 12, "#fff3e0", None, 7) + circ(256, 340, 14, "#ffb547", 6)
    if d == "hoodie":
        s += f'<path d="M222,280 q34,40 68,0" fill="none" {O(7)}/>' + line(244, 300, 242, 330, INK, 5) + line(268, 300, 270, 330, INK, 5) + rr(222, 344, 68, 34, 12, p["shirt"], None, 7)
    if d == "uniform":
        s += f'<path d="M226,278 L256,306 L286,278" fill="#fbfbfb" {O(7)}/>' + f'<path d="M244,300 l12,10 l12,-10 l-6,26 l-12,0Z" fill="#2f5aa8" {O(6)}/>'
    if d == "suit":
        s += f'<path d="M226,278 L256,330 L286,278" fill="#fbfbfb" {O(7)}/>' + f'<path d="M248,292 L264,292 L260,306 L266,350 L256,362 L246,350 L252,306Z" fill="#ffd36b" {O(6)}/>'
        s += f'<path d="M226,278 L246,340 L232,350 M286,278 L266,340 L280,350" fill="none" {O(6)}/>'
    if d == "jacket":
        s += line(256, 282, 256, 398, INK, 6) + rr(212, 330, 30, 22, 6, "#24894f", None, 6) + rr(270, 330, 30, 22, 6, "#24894f", None, 6)
    if d == "cardigan":
        s += f'<path d="M232,278 L256,330 L280,278" fill="#fbfbfb" {O(7)}/>' + "".join(circ(246, 348+i*18, 5, "#ffd36b", 4) for i in range(3))
    if d == "santa":
        s += rr(180, 352, 152, 22, 8, "#1c1f27", None, 7) + rr(244, 348, 26, 30, 4, "#ffd36b", None, 6) + line(256, 282, 256, 350, "#fbfbfb", 14)
    if d == "cape":
        s += f'<path d="M220,282 L256,320 L292,282" fill="#5a3a7a" {O(7)}/>'
    if z: s += '<path d="M180,282 L332,282 L340,410 L172,410Z" fill="#2c3a2a" opacity=".22"/>'
    return s

def arms(p, z):
    """trả về (vẽ tay sau, vẽ tay trước, tọa độ tay cầm vật)"""
    skin = ZSKIN if z else HSKIN
    sl = p.get("sleeve", p["shirt"])
    if z:
        sl = zcloth(sl)
        L, R = (138, 300), (374, 300)
        a = line(204, 296, L[0], L[1], INK, 46) + line(204, 296, L[0], L[1], sl, 30) + line(308, 296, R[0], R[1], INK, 46) + line(308, 296, R[0], R[1], sl, 30)
        hands = circ(L[0]-8, L[1], 22, skin, 8) + circ(R[0]+8, R[1], 22, skin, 8)
        hands += "".join(f'<path d="M{L[0]-24},{L[1]-12+i*11} L{L[0]-50},{L[1]-16+i*12} L{L[0]-26},{L[1]-4+i*11}Z" fill="#2a2420"/>' for i in range(3))
        hands += "".join(f'<path d="M{R[0]+24},{R[1]-12+i*11} L{R[0]+50},{R[1]-16+i*12} L{R[0]+26},{R[1]-4+i*11}Z" fill="#2a2420"/>' for i in range(3))
        return a, hands, (R[0]+8, R[1]-6)
    L, R = (150, 214), (346, 352)
    a = line(206, 294, L[0], L[1], INK, 46) + line(206, 294, L[0], L[1], sl, 30) + line(306, 294, R[0], R[1], INK, 46) + line(306, 294, R[0], R[1], sl, 30)
    hands = circ(L[0], L[1]-6, 22, skin, 8) + line(L[0]-6, L[1]-26, L[0]-12, L[1]-40, INK, 7) + line(L[0]+8, L[1]-26, L[0]+10, L[1]-42, INK, 7)
    hands += circ(R[0], R[1], 22, skin, 8)
    return a, hands, R

def character(p, st):
    z = st == "z"
    hx, hy, R = 256, 172, 100
    s = '<ellipse cx="256" cy="452" rx="130" ry="18" fill="#000" opacity=".16"/>'
    if p.get("back") == "ringlight" and True:
        s += f'<circle cx="256" cy="176" r="150" fill="none" stroke="#fff" stroke-width="16" opacity="{.5 if z else .9}"/>' + f'<circle cx="256" cy="176" r="150" fill="none" stroke="{INK}" stroke-width="4" opacity=".4"/>'
    if p.get("back") == "cape":
        s += f'<path d="M196,282 Q120,380 150,440 L362,440 Q392,380 316,282Z" fill="#5a3a7a" {O()}/>'
    a, hands, hand = arms(p, z)
    s += a + body(p, z)
    held = p.get("item")
    s += hands
    if held: s += item(held, hand[0], hand[1], st)
    # đầu
    tilt = -14 if z else 4
    if z: hy += 12
    g = ""
    if p.get("pumpkin") and z:
        g += pumpkin_head(hx, hy, R, z)
    else:
        skin = ZSKIN if z else HSKIN
        g += circ(hx-R+4, hy+16, 20, skin) + circ(hx+R-4, hy+16, 20, skin)
        g += circ(hx, hy, R, skin)
        if z:
            g += f'<path d="M{hx+20},{hy-R+4} A{R},{R} 0 0,1 {hx+R-6},{hy+30} A{R},{R} 0 0,1 {hx+30},{hy+R-4} Q{hx+80},{hy+10} {hx+20},{hy-R+4}Z" fill="{ZSHADE}" opacity=".55"/>'
        if p.get("beard"):
            g += f'<path d="M{hx-R+10},{hy+20} Q{hx-R+10},{hy+R+60} {hx},{hy+R+40} Q{hx+R-10},{hy+R+60} {hx+R-10},{hy+20} Q{hx},{hy+60} {hx-R+10},{hy+20}Z" fill="{"#e9ecef" if z else "#ffffff"}" {O()}/>'
        if not p.get("hat") in ("helmet",):
            g += hair(p, z, hx, hy, R) if not p.get("hat") in ("nightcap", "santa") else ""
        g += face(p, z, hx, hy, R)
        if p.get("beard"):
            g += f'<path d="M{hx-40},{hy+46} Q{hx},{hy+30} {hx+40},{hy+46}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round"/><path d="M{hx-40},{hy+46} Q{hx},{hy+30} {hx+40},{hy+46}" fill="none" {O(5)}/>'
        g += glasses(p, z, hx, hy)
        g += headwear(p, z, hx, hy, R)
        g += hl(hx-50, hy-50, 26, 12, -30, .35 if not z else .12)
    s += f'<g transform="rotate({tilt} {hx} {hy+90})">{g}</g>'
    if p.get("item2") and not z: s += item(p["item2"], 150, 260, st)
    # hiệu ứng
    if z:
        if p.get("sleepy"):
            s += f'<text x="372" y="96" font-family="Inter Display,Inter,sans-serif" font-weight="900" font-size="44" fill="#cfe3c8" stroke="{INK}" stroke-width="3">Z</text><text x="408" y="62" font-family="Inter Display,Inter,sans-serif" font-weight="900" font-size="30" fill="#cfe3c8" stroke="{INK}" stroke-width="3">z</text>'
        s += "".join(f'<path d="M{x},{y} q-14,-10 0,-20 q14,-10 0,-20" fill="none" stroke="#7f9a6f" stroke-width="8" stroke-linecap="round" opacity=".9"/>' for x, y in [(96, 140), (420, 200), (80, 300)])
    else:
        s += spark(410, 80, 22) + spark(96, 120, 16) + spark(430, 260, 13, "#fff5c2")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">{DEFS}{s}</svg>'

CHARS = [
 dict(id="ngugat", name="Zombie Ngủ Gật", tier=1, shirt="#8fa7d9", detail="stars", hair="#4a3426", hat="nightcap", item="pillow", sleepy=True, happy_closed=True,
      zq="Cho… ngủ… năm phút nữa…", hq="Ủa sáng rồi hả? Cảm ơn nha!"),
 dict(id="deadline", name="Zombie Deadline", tier=1, shirt="#e8e3d6", detail="tie", tie="#3e5f8a", hair="#3a2a20", item="papers",
      zq="Mai… nộp… mai nộp…", hq="Mình đi nộp bài liền đây!"),
 dict(id="trasua", name="Zombie Trà Sữa", tier=1, shirt="#f29bb5", detail="hoodie", hair="#6b4226", hairstyle="bun", item="cup",
      zq="Ít đường… nhiều trân châu…", hq="Tỉnh rồi, uống nước lọc thôi!"),
 dict(id="songao", name="Zombie Sống Ảo", tier=2, shirt="#8a7ad9", detail="hoodie", hair="#2b2030", hairstyle="pony", item="phone", back="ringlight", happy_closed=True,
      zq="Khoan… chụp… tấm nữa…", hq="Ảnh flash này đẹp ghê!"),
 dict(id="shipper", name="Zombie Shipper", tier=2, shirt="#2fae6a", detail="jacket", hair="#2b2020", hat="helmet", item="box",
      zq="Xuống… lấy hàng… đi…", hq="Giao xong đơn, về nghỉ thôi!"),
 dict(id="onthi", name="Zombie Ôn Thi", tier=3, shirt="#fbfbfb", detail="uniform", pants="#2f5aa8", hair="#1f1a18", glasses=True, item="book",
      zq="Đề cương… chương bảy… đâu…", hq="Nhớ hết bài rồi, cảm ơn!"),
 dict(id="doidem", name="Zombie Đói Đêm", tier=3, shirt="#ff9a4a", detail="apron", hair="#4a2c1c", hat="cap", item="bowl", happy_closed=True,
      zq="Ramen… nóng… ramen…", hq="Ghé THEZONE ăn tô thật thôi!"),
 dict(id="ceo", name="Zombie CEO", tier=5, eye="#ffd36b", shirt="#262b36", sleeve="#262b36", detail="suit", hair="#1c1716", hairstyle="slick", item="tablet",
      zq="Con số… không nói dối…", hq="Làm trước, đo sau, sửa ngay!"),
 dict(id="bingo", name="Zombie Bí Ngô", tier=4, season="Halloween", shirt="#3a2a4a", detail="cape", back="cape", hair="#6b3a1c", pumpkin=True, item="bucket",
      zq="Cho kẹo… hay bị cắn…", hq="Kẹo nè, chia bạn một viên!"),
 dict(id="chambai", name="Zombie Chấm Bài", tier=4, eye="#ff6a5c", season="20/11", shirt="#7fb08a", detail="cardigan", hair="#5a4a40", hairstyle="bun", glasses=True, glasses_col="#8a4a3a", item="redpen", item_h="flower",
      zq="Ai… chưa… nộp bài…", hq="Cả lớp được mười điểm!"),
 dict(id="ongtuyet", name="Zombie Ông Già Tuyết", tier=4, eye="#ff6a5c", season="Noel", shirt="#d93636", sleeve="#d93636", detail="santa", hair="#ffffff", hat="santa", beard=True, item="sack", happy_closed=True,
      zq="Hô… hô… đói quá…", hq="Giáng sinh vui vẻ nha!"),
]
TIERS = {1: ("Thường", "#aab3c2"), 2: ("Hiếm", "#62a9ff"), 3: ("Đột Biến", "#b993ff"), 4: ("Boss", "#ff6f5c"), 5: ("Huyền Thoại", "#ffd36b")}

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    meta = []
    for p in CHARS:
        for st in ("z", "h"):
            q = dict(p)
            if st == "h" and p.get("item_h"): q["item"] = p["item_h"]
            open(f"{out}/{p['id']}-{'zombie' if st=='z' else 'nguoi'}.svg", "w").write(character(q, st))
        t = TIERS[p["tier"]]
        meta.append(dict(id=p["id"], name=p["name"], tier=p["tier"], tierName=t[0], color=t[1], season=p.get("season"), zq=p["zq"], hq=p["hq"]))
    json.dump(meta, open(f"{out}/meta.json", "w"), ensure_ascii=False, indent=1)
    print(len(meta), "nhân vật")
