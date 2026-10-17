(()=>{const DB=window.__DB||(window.__DB={'stations/abc12345':{name:'Tạp hoá Cô Ba',level:'nho',cap:5,active:true}});
const snap=(id,d)=>({id,exists:d!==undefined,data:()=>d===undefined?undefined:JSON.parse(JSON.stringify(d))});
function docRef(path){const id=path.split('/').pop();return{id,path,get:async()=>snap(id,DB[path]),set:async(o,opt)=>{DB[path]=opt&&opt.merge?Object.assign({},DB[path],o):o},update:async o=>{DB[path]=Object.assign({},DB[path],o)},onSnapshot:(f)=>{setTimeout(()=>f(snap(id,DB[path])),5);return()=>{}}}}
function coll(name){const q={doc:id=>docRef(name+'/'+id),where:()=>q,orderBy:()=>q,limit:()=>q,get:async()=>({empty:true,size:0,docs:[],forEach(){}}),add:async o=>{const id='x'+Math.random().toString(36).slice(2);DB[name+'/'+id]=o;return docRef(name+'/'+id)}};return q}
const user={uid:'u-test',isAnonymous:true,email:null};
const fs={collection:coll,runTransaction:async fn=>{const tx={get:r=>r.get(),set:(r,o)=>{DB[r.path]=o},update:(r,o)=>{DB[r.path]=Object.assign({},DB[r.path],o)}};return fn(tx)}};
window.firebase={initializeApp(){},auth:Object.assign(()=>({currentUser:user,getRedirectResult:async()=>null,onAuthStateChanged:f=>setTimeout(()=>f(user),10),signInAnonymously:async()=>({user})}),{EmailAuthProvider:{credential(){}}}),firestore:Object.assign(()=>fs,{FieldValue:{increment:n=>n}})};})();
