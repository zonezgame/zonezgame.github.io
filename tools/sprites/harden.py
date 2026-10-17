import numpy as np,cv2,os
from PIL import Image
os.makedirs('cut3',exist_ok=True)
for f in sorted(os.listdir('cut2')):
    im=Image.open('cut2/'+f);a=np.asarray(im.getchannel('A')).astype(np.float32)/255
    core=(a>0.35).astype(np.uint8)*255
    n,lab,st,_=cv2.connectedComponentsWithStats(core)
    keep=np.zeros_like(core)
    if n>1:
        big=st[1:,cv2.CC_STAT_AREA].max()
        for k in range(1,n):
            if st[k,cv2.CC_STAT_AREA]>=big*0.04: keep[lab==k]=255
    H,W=keep.shape;ff=keep.copy();msk=np.zeros((H+2,W+2),np.uint8)
    cv2.floodFill(ff,msk,(0,0),255);holes=cv2.bitwise_not(ff)
    holes_small=np.zeros_like(holes);n2,l2,s2,_=cv2.connectedComponentsWithStats(holes)
    for k in range(1,n2):
        if s2[k,cv2.CC_STAT_AREA]<H*W*0.01: holes_small[l2==k]=255
    solid=keep|holes_small
    solid=cv2.morphologyEx(solid,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    edge=cv2.GaussianBlur(solid,(5,5),0).astype(np.float32)/255
    # inside solid: opaque; edges: soft
    out=np.where(solid>0,np.maximum(edge,np.clip((a-0.2)/0.3,0,1)),edge*0.0)
    o=im.copy();o.putalpha(Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)));o.save('cut3/'+f)
