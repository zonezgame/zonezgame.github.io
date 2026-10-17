const fs=require('fs');const vm=require('vm');
const src=fs.readFileSync('/home/claude/zonezgame.github.io/lib/qrcode.js','utf8');
const ctx={module:{},exports:{},window:{}};vm.createContext(ctx);vm.runInContext(src+';this.qrcode=qrcode;',ctx);
const qr=ctx.qrcode(0,'Q');qr.addData('https://zonezgame.github.io');qr.make();
const n=qr.getModuleCount();let d='';
for(let r=0;r<n;r++)for(let c=0;c<n;c++)if(qr.isDark(r,c))d+=`M${c} ${r}h1v1h-1z`;
fs.writeFileSync(process.argv[2],`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n} ${n}" width="${n*10}" height="${n*10}" shape-rendering="crispEdges"><rect width="${n}" height="${n}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`);
console.log('modules',n);
