// Quay từng khung 30 fps bằng đồng hồ ảo: node rec3.js <tên> <cure|bite> <số giây tối đa> <mã zombie ưu tiên>
const { chromium } = require('playwright');const fs=require('fs');
const [,,NAME,MODE,MAXS,PREF]=process.argv;const OUT='/home/claude/work/rec/'+NAME;fs.rmSync(OUT,{recursive:true,force:true});fs.mkdirSync(OUT,{recursive:true});
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:432,height:768},deviceScaleFactor:2.5,isMobile:true,hasTouch:true});
await c.route('**/firebase-config.js',r=>r.fulfill({body:'window.ZONEZ_FIREBASE=null;',contentType:'text/javascript'}));
await c.addInitScript(()=>{let VT=5000,cbs=[];performance.now=()=>VT;window.requestAnimationFrame=cb=>{cbs.push(cb);return cbs.length};window.cancelAnimationFrame=()=>{};
 window.__step=ms=>{VT+=ms;const q=cbs;cbs=[];q.forEach(f=>{try{f(VT)}catch(e){console.log('ERR '+e.message)}})};
 localStorage.setItem('zonez.v1',JSON.stringify({tz:2450,flash:12,profile:{name:'Tín Đạo Sĩ',avatar:'ceo'},equip:{frame:'f_gold',scope:'s_gold',fx:'x_star'},owned:{f_gold:1,s_gold:1,x_star:1},cfg:{pQuick:100,pMid:0,cap:45,firstFast:true,topDay:1},lastHuntDay:'x',mute:true}))});
const p=await c.newPage();p.on('console',m=>{if(m.text().startsWith('ERR'))console.log(m.text())});
await p.goto('http://localhost:8767/index.html');await p.waitForTimeout(1500);
for(let i=0;i<5;i++)await p.evaluate(()=>__step(33));
if(PREF)await p.evaluate(id=>{const r=Math.random;window.__pref=id},PREF);
await p.tap('#go');let a=100,n=0,shot=0;
const snap=async()=>{await p.screenshot({path:`${OUT}/${String(n++).padStart(5,'0')}.jpg`,quality:90,type:'jpeg'})};
for(let i=0;i<MAXS*30;i++){await p.evaluate(a=>{window.dispatchEvent(Object.assign(new Event('deviceorientation'),{alpha:a,beta:85,gamma:0}));__step(1000/30)},a);await snap();
 const s=await p.evaluate(()=>({aim:!document.querySelector('#hudAim').hidden,res:!document.querySelector('#result').hidden,hint:document.querySelector('#aimHint').textContent,lock:document.querySelector('#shoot').classList.contains('lock'),d:parseFloat(document.querySelector('#distM').textContent),name:(document.querySelector('#zName')||{}).textContent}));
 if(s.res){for(let k=0;k<75;k++){await p.evaluate(()=>__step(1000/30));await snap()}console.log('result',await p.evaluate(()=>document.querySelector('#result h3').textContent));break}
 if(!s.aim)continue;if(s.hint.includes('TRÁI'))a+=1;else if(s.hint.includes('PHẢI'))a-=1;
 if(MODE==='cure'&&s.lock&&s.d<3&&i-shot>18){await p.locator('#shoot').dispatchEvent('pointerdown');shot=i}}
console.log('frames',n);await b.close()})();
