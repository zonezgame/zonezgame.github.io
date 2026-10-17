// Quay bằng CDP screencast ở độ phân giải thiết bị. Dùng: node rec2.js <tên> <kịch bản: cure|bite|tour>
const { chromium } = require('playwright');const fs=require('fs');
const [,,NAME,MODE]=process.argv;const OUT='/home/claude/work/rec/'+NAME;fs.rmSync(OUT,{recursive:true,force:true});fs.mkdirSync(OUT,{recursive:true});
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:432,height:768},deviceScaleFactor:2.5,isMobile:true,hasTouch:true});
await c.route('**/firebase-config.js',r=>r.fulfill({body:'window.ZONEZ_FIREBASE=null;',contentType:'text/javascript'}));
await c.addInitScript(()=>{if(!sessionStorage.getItem('i')){sessionStorage.setItem('i','1');localStorage.setItem('zonez.v1',JSON.stringify({tz:2450,flash:12,profile:{name:'Tín Đạo Sĩ',avatar:'ceo'},equip:{frame:'f_gold',scope:'s_gold',fx:'x_star'},owned:{f_gold:1,s_gold:1,x_star:1,f_pumpkin:1},seen:{ngugat:3,deadline:2,trasua:2,songao:1,shipper:1,doidem:1,bingo:1},cured:{ngugat:3,deadline:1,trasua:2,shipper:1},cfg:{pQuick:100,pMid:0,cap:45,firstFast:false,topDay:1},lastHuntDay:'x',mute:true}))}});
const p=await c.newPage();await p.goto('http://localhost:8767/index.html');await p.waitForTimeout(2000);
const cdp=await c.newCDPSession(p);const frames=[];
cdp.on('Page.screencastFrame',async f=>{frames.push({t:f.metadata.timestamp,d:f.data});cdp.send('Page.screencastFrameAck',{sessionId:f.sessionId}).catch(()=>{})});
await cdp.send('Page.startScreencast',{format:'jpeg',quality:88,maxWidth:1080,maxHeight:1920,everyNthFrame:1});
const T0=Date.now();const mark=n=>console.log(n,((Date.now()-T0)/1000).toFixed(2));
const fire=a=>p.evaluate(a=>window.dispatchEvent(Object.assign(new Event('deviceorientation'),{alpha:a,beta:85,gamma:0})),a);
if(MODE==='tour'){await p.waitForTimeout(1200);await p.tap('#tChars');await p.waitForTimeout(900);await p.evaluate(()=>document.querySelector('#screen').scrollBy({top:500,behavior:'smooth'}));await p.waitForTimeout(1300);
 await p.tap('#tab-shop');await p.waitForTimeout(900);for(let i=0;i<3;i++){await p.evaluate(()=>document.querySelector('#screen').scrollBy({top:520,behavior:'smooth'}));await p.waitForTimeout(1000)}
 await p.tap('#tab-home');await p.waitForTimeout(800);await p.tap('#tEvent');await p.waitForTimeout(1800);}
else{await p.waitForTimeout(800);await p.tap('#go');mark('hunt');let a=100;
 for(let i=0;i<600;i++){await fire(a);await p.waitForTimeout(33);
  const s=await p.evaluate(()=>({aim:!document.querySelector('#hudAim').hidden,res:!document.querySelector('#result').hidden,hint:document.querySelector('#aimHint').textContent,lock:document.querySelector('#shoot').classList.contains('lock'),d:parseFloat(document.querySelector('#distM').textContent)}));
  if(s.res){mark('result '+await p.evaluate(()=>document.querySelector('#result h3').textContent));break}
  if(!s.aim)continue;if(s.hint.includes('TRÁI'))a+=1.2;else if(s.hint.includes('PHẢI'))a-=1.2;
  if(MODE==='cure'&&s.lock&&s.d<3.2){await p.locator('#shoot').dispatchEvent('pointerdown');mark('shot');await p.waitForTimeout(700)}}
 await p.waitForTimeout(2200)}
await cdp.send('Page.stopScreencast');await p.waitForTimeout(300);
let list='';frames.forEach((f,i)=>{const fn=`${OUT}/${String(i).padStart(5,'0')}.jpg`;fs.writeFileSync(fn,Buffer.from(f.d,'base64'));const dur=i<frames.length-1?frames[i+1].t-f.t:0.04;list+=`file '${fn}'\nduration ${Math.max(0.01,dur).toFixed(4)}\n`});
fs.writeFileSync(OUT+'/list.txt',list);console.log('frames',frames.length,'span',(frames.at(-1).t-frames[0].t).toFixed(1));await b.close()})();
