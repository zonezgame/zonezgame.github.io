import numpy as np,cv2,os
from PIL import Image
# remove leftover background: pixels similar to column bg colour where model was unsure
for f in sorted(os.listdir('cut4')):
    if f.startswith(('doidem','bingo')): continue
    raw=np.asarray(Image.open('raw/'+f).convert('RGB').resize(Image.open('cut4/'+f).size,Image.LANCZOS)).astype(np.float32)
    c4=Image.open('cut4/'+f);a=np.asarray(c4.getchannel('A')).astype(np.float32)
    p=np.asarray(Image.open('cut2/'+f).getchannel('A')).astype(np.float32)/255
    H,W=a.shape
    # bg samples: outer 6% frame where model says background
    frame=np.zeros((H,W),bool);k=int(W*.06);frame[:, :k]=1;frame[:, -k:]=1;frame[:int(H*.05)]=1
    samp=raw[frame&(p<0.1)]
    if len(samp)<50: continue
    lab=cv2.cvtColor((raw/255).astype(np.float32),cv2.COLOR_RGB2LAB)
    sl=cv2.cvtColor((samp[None]/255).astype(np.float32),cv2.COLOR_RGB2LAB)[0]
    # distance to nearest of 64 kmeans bg colours
    crit=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,20,1.0)
    _,_,cent=cv2.kmeans(sl.astype(np.float32),min(16,len(sl)//10),None,crit,2,cv2.KMEANS_PP_CENTERS)
    d=np.min(np.linalg.norm(lab.reshape(-1,1,3)-cent[None],axis=2),axis=1).reshape(H,W)
    kill=(d<9)&(p<0.97)
    kill=cv2.morphologyEx(kill.astype(np.uint8),cv2.MORPH_OPEN,np.ones((5,5),np.uint8))>0
    a2=a.copy();a2[kill]=0
    s=(a2>128).astype(np.uint8);n,lb,st,_=cv2.connectedComponentsWithStats(s)
    if n>1:
        big=st[1:,cv2.CC_STAT_AREA].max();keep=np.zeros_like(s)
        for i in range(1,n):
            if st[i,cv2.CC_STAT_AREA]>=big*.05:keep[lb==i]=1
        a2=np.where(cv2.dilate(keep,np.ones((5,5),np.uint8))>0,a2,0)
    a2=cv2.GaussianBlur(a2,(3,3),0)
    c4.putalpha(Image.fromarray(a2.astype(np.uint8)));c4.save('cut4/'+f)
    print(f,round(kill.mean()*100,1))
