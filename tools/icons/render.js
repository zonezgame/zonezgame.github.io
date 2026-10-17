const { chromium } = require('playwright');const fs=require('fs');
const meta=JSON.parse(fs.readFileSync('svg/meta.json'));
const svgOf=(m,size)=>fs.readFileSync('svg/'+m.slug+'.svg','utf8').replace('width="512" height="512"',`width="${size}" height="${size}"`);
const fmt=n=>n.toLocaleString('vi-VN');
const css=`*{box-sizing:border-box}body{margin:0;background:transparent;font-family:Inter,sans-serif}
.card{width:600px;height:780px;border-radius:32px;position:relative;overflow:hidden;background:radial-gradient(120% 80% at 50% 0%,#1d2840 0%,#0d1220 70%);border:6px solid var(--c);display:flex;flex-direction:column;align-items:center;padding:30px 34px}
.card.hot{box-shadow:inset 0 0 60px -10px var(--c)}
.top{width:100%;display:flex;justify-content:space-between;align-items:center}
.brand{font:800 18px "Inter Display",Inter;letter-spacing:.18em;color:#8e98ab}.brand b{color:#ffb547}
.chip{font:900 26px "Inter Display",Inter;padding:8px 18px;border-radius:999px;background:var(--c);color:#14110a;letter-spacing:.02em}
.glow{position:absolute;left:50%;top:330px;width:460px;height:460px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--c) 38%,transparent) 0%,transparent 65%)}
.ic{position:relative;margin-top:6px}
.nm{font:900 50px/1.08 "Inter Display",Inter;color:#f4f6fa;text-align:center;letter-spacing:-.01em;margin-top:2px;text-wrap:balance}
.sub{margin-top:14px;font:500 19px Inter;color:#9aa4b7}
.pips{position:absolute;bottom:26px;display:flex;gap:8px}.pips i{width:34px;height:7px;border-radius:4px;background:#273247}.pips i.on{background:var(--c)}`;
const order=[5,6,8,10,15,20];const MIN={5:20,6:25,8:35,10:40,15:60,20:80};
const card=m=>`<div class="card ${m.k>=15?'hot':''}" style="--c:${m.color}"><div class="glow"></div><div class="top"><span class="brand">ZONE <b>Z</b> · TOPPING</span><span class="chip">${fmt(m.tz)} TZ</span></div><div class="ic">${svgOf(m,420)}</div><div class="nm">${m.name}</div><div class="sub">Đổi tại THEZONE · kèm đơn từ ${MIN[m.k]}K</div><div class="pips">${order.map(k=>`<i class="${k<=m.k?'on':''}"></i>`).join('')}</div></div>`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:700,height:900}});
for(const m of meta){
 await p.setContent(`<html><body>${svgOf(m,512)}</body></html>`);await p.locator('svg').screenshot({path:`out/icon/${m.slug}.png`,omitBackground:true});
 await p.setContent(`<html><head><style>${css}</style></head><body>${card(m)}</body></html>`);await p.locator('.card').screenshot({path:`out/the/${m.slug}.png`,omitBackground:true});}
// bảng tổng hợp 1080 x auto
const groups=order.map(k=>({k,items:meta.filter(m=>m.k===k)}));
const board=`<div class="board"><div class="hd"><div><div class="t">BẢNG ĐỔI TOPPING</div><div class="s">Chữa zombie, nhận TZ đồng, đổi topping tại THEZONE</div></div><div class="wm">ZONE <b>Z</b></div></div>
${groups.map(g=>`<div class="grp" style="--c:${g.items[0].color}"><div class="gl"><span>${fmt(g.k*100)} TZ</span><small>kèm đơn từ ${MIN[g.k]}K</small></div><div class="row">${g.items.map(m=>`<div class="it">${svgOf(m,150)}<div>${m.name}</div></div>`).join('')}</div></div>`).join('')}
<div class="ft">Mỗi tài khoản đổi 1 lần/ngày · Mã dùng 1 lần, hạn 7 ngày · Số suất mỗi ngày có hạn</div></div>`;
const bcss=`*{box-sizing:border-box}body{margin:0;font-family:Inter}.board{width:1080px;background:radial-gradient(100% 40% at 50% 0%,#1d2840,#0b1019 70%);padding:56px 48px 44px;color:#eef1f6}
.hd{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:34px}.t{font:900 58px "Inter Display",Inter;letter-spacing:-.01em}.s{font:500 21px Inter;color:#9aa4b7;margin-top:8px;max-width:640px}
.wm{font:900 44px "Inter Display",Inter}.wm b{color:#ffb547}
.grp{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;padding:16px 0;border-top:1px solid #222c3f}
.gl small{display:block;margin-top:8px;font:600 16px Inter;color:#9aa4b7}.gl span{display:inline-block;font:900 26px "Inter Display",Inter;padding:10px 16px;border-radius:14px;background:var(--c);color:#14110a;white-space:nowrap}
.row{display:flex;flex-wrap:wrap;gap:6px 8px}.it{width:150px;text-align:center;font:700 18px Inter;line-height:1.2}.it svg{display:block;margin:0 auto 2px}
.ft{margin-top:26px;padding-top:20px;border-top:1px solid #222c3f;font:500 19px Inter;color:#9aa4b7;text-align:center}`;
await p.setViewportSize({width:1080,height:1400});await p.setContent(`<html><head><style>${bcss}</style></head><body>${board}</body></html>`);await p.locator('.board').screenshot({path:'out/bang-doi-topping.png'});
await b.close();console.log('rendered',meta.length)})();
