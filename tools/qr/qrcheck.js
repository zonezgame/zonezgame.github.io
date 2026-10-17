const {chromium}=require('/home/claude/.npm-global/lib/node_modules/@playwright/mcp/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:500,height:500}});
const svg=fs.readFileSync('poster/qr-zonez.svg','utf8');
await p.setContent(`<body style="margin:0;background:#fff;padding:40px">${svg.replace('width="290" height="290"','width="400" height="400"')}</body>`);
await p.addScriptTag({path:'/home/claude/zonezgame.github.io/lib/jsQR.js'});
const r=await p.evaluate(async()=>{const img=new Image();const s=document.querySelector('svg').outerHTML;img.src='data:image/svg+xml;base64,'+btoa(s);await img.decode();const c=document.createElement('canvas');c.width=480;c.height=480;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,480,480);x.drawImage(img,40,40,400,400);const d=x.getImageData(0,0,480,480);const q=jsQR(d.data,480,480);return q&&q.data});
console.log('decoded:',r);await b.close()})();
