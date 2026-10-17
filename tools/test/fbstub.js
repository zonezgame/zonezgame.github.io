(()=>{const now=Date.now(),day=864e5;
const DATA={'config/staff':{emails:['nv@gmail.com'],admins:['tranduytin130591@gmail.com']},'config/game':{pQuick:30,pMid:50,cap:45,topDay:1,firstFast:true,season:'halloween'},
 users:[{id:'u1',d:{nick:'n1',name:'Tín Đạo Sĩ',profile:{name:'Tín Đạo Sĩ'},tz:1250,flash:4,infectedUntil:now+600000,cured:{a:12,b:3},hunts:new Array(30),bites:2,frames:{x:1},createdAt:now-3600e3,updatedAt:now-300e3}},
  {id:'u2',d:{nick:'n2',name:'Ngọc 🌸 Ánh',profile:{name:'Ngọc 🌸 Ánh'},tz:640,flash:12,cured:{a:5},hunts:new Array(9),bites:0,createdAt:now-3*day,updatedAt:now-2*day,locked:true}},
  {id:'u3',d:{guest:true,name:'Đạo hữu',tz:80,cured:{},hunts:[],createdAt:now-1000,updatedAt:now-1000}}],
 stations:[{id:'abc12345',d:{name:'Tạp hoá Cô Ba',level:'nho',cap:5,active:true,createdAt:now-5000}},{id:'k9m2p7q4',d:{name:'Quán chè Út Mập',level:'lon',cap:25,active:false,createdAt:now-9000}}],
 stationUse:[{id:'u1',d:{station:'abc12345',n:3,day:(d=>d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate())(new Date())}}],
 codes:[{id:'TZ-AAAA-BBBB',d:{uid:'u1',name:'Tín Đạo Sĩ',item:'Topping Tôm viên',kind:'topping',used:true,usedAt:now-1000,orderK:30,createdAt:now-5000,exp:now+6*day}}]};
const snap=(id,d)=>({id,exists:!!d,data:()=>d});
const qs=arr=>({size:arr.length,empty:!arr.length,docs:arr.map(x=>snap(x.id,x.d)),forEach:f=>arr.map(x=>snap(x.id,x.d)).forEach(f)});
function coll(name){let F=[];const api={doc:id=>({get:async()=>name==='config'?snap(id,DATA['config/'+id]):snap(id,(DATA[name].find(x=>x.id===id)||{}).d),update:async o=>{console.log('UPDATE',name,id,JSON.stringify(o))},set:async o=>{console.log('SET',name,id,JSON.stringify(o))}}),
 where:(f,op,v)=>{F.push([f,op,v]);return api},orderBy:()=>api,limit:()=>api,get:async()=>qs((DATA[name]||[]).filter(x=>F.every(([f,op,v])=>op==='=='?x.d[f]===v:(x.d[f]||0)>=v)))};return api}
const user={email:'tranduytin130591@gmail.com',isAnonymous:false,providerData:[{providerId:'google.com'}]};
window.firebase={initializeApp(){},auth:Object.assign(()=>({getRedirectResult:async()=>null,onAuthStateChanged:f=>setTimeout(()=>f(user),10)}),{GoogleAuthProvider:function(){this.setCustomParameters=()=>{}}}),firestore:()=>({collection:n=>coll(n)})};})();
