import numpy as np,cv2,os
from PIL import Image
os.makedirs('cut4',exist_ok=True)
for f in sorted(os.listdir('cut2')):
    im=Image.open('cut2/'+f);rgb=cv2.cvtColor(np.asarray(im.convert('RGB')),cv2.COLOR_RGB2BGR)
    p=np.asarray(im.getchannel('A')).astype(np.float32)/255;H,W=p.shape
    m=np.full((H,W),cv2.GC_PR_BGD,np.uint8)
    m[p>0.3]=cv2.GC_PR_FGD;m[p>0.85]=cv2.GC_FGD;m[p<0.08]=cv2.GC_BGD
    b=4;m[:b,:]=cv2.GC_BGD;m[:,:b]=cv2.GC_BGD;m[:,-b:]=cv2.GC_BGD
    bg=np.zeros((1,65));fg=np.zeros((1,65))
    cv2.grabCut(rgb,m,None,bg,fg,6,cv2.GC_INIT_WITH_MASK)
    s=np.where((m==1)|(m==3),255,0).astype(np.uint8)
    n,lab,st,_=cv2.connectedComponentsWithStats(s);keep=np.zeros_like(s)
    if n>1:
        big=st[1:,cv2.CC_STAT_AREA].max()
        for k in range(1,n):
            if st[k,cv2.CC_STAT_AREA]>=big*0.05: keep[lab==k]=255
    ff=keep.copy();msk=np.zeros((H+2,W+2),np.uint8);cv2.floodFill(ff,msk,(0,0),255);holes=cv2.bitwise_not(ff)
    n2,l2,s2,_=cv2.connectedComponentsWithStats(holes)
    for k in range(1,n2):
        if s2[k,cv2.CC_STAT_AREA]<H*W*0.0004: keep[l2==k]=255
    keep=cv2.morphologyEx(keep,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    a=cv2.GaussianBlur(keep,(5,5),0)
    o=im.copy();o.putalpha(Image.fromarray(a));o.save('cut4/'+f)
