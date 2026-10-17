const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8767/sfxtest.html');const b64=await p.evaluate(()=>render());fs.writeFileSync('/home/claude/work/rec/promo.wav',Buffer.from(b64,'base64'));console.log(errs);await b.close()})();
