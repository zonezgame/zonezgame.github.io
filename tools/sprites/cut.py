import cv2,numpy as np,sys,os
from PIL import Image
os.makedirs('cut',exist_ok=True)
def cut(src,dst,kind):
    img=cv2.imread(src);h,w=img.shape[:2]
    big=cv2.resize(img,(w*2,h*2),interpolation=cv2.INTER_CUBIC);H,W=big.shape[:2]
    m=np.full((H,W),cv2.GC_PR_BGD,np.uint8)
    b=6
    m[:b,:]=cv2.GC_BGD;m[:, :b]=cv2.GC_BGD;m[:, -b:]=cv2.GC_BGD
    if kind=='z': m[-b:,:]=cv2.GC_BGD
    cv2.ellipse(m,(W//2,int(H*.5)),(int(W*.28),int(H*.36)),0,0,360,cv2.GC_PR_FGD,-1)
    cv2.ellipse(m,(W//2,int(H*(.3 if kind=='z' else .4))),(int(W*.12),int(H*.1)),0,0,360,cv2.GC_FGD,-1)
    bg=np.zeros((1,65),np.float64);fg=np.zeros((1,65),np.float64)
    cv2.grabCut(big,m,None,bg,fg,10,cv2.GC_INIT_WITH_MASK)
    a=np.where((m==cv2.GC_FGD)|(m==cv2.GC_PR_FGD),255,0).astype(np.uint8)
    # keep largest component
    n,lab,st,_=cv2.connectedComponentsWithStats(a)
    if n>1:
        k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]);a=np.where(lab==k,255,0).astype(np.uint8)
    a=cv2.morphologyEx(a,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    # fill holes
    ff=a.copy();msk=np.zeros((H+2,W+2),np.uint8);cv2.floodFill(ff,msk,(0,0),255);a=a|cv2.bitwise_not(ff)
    a=cv2.GaussianBlur(a,(5,5),0)
    rgba=cv2.cvtColor(big,cv2.COLOR_BGR2BGRA);rgba[:,:,3]=a
    cv2.imwrite(dst,rgba)
for f in sorted(os.listdir('raw')):
    cut('raw/'+f,'cut/'+f,f.split('-')[1][0])
