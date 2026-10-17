import numpy as np,json
from PIL import Image
ids=['ngugat','deadline','trasua','songao','shipper','onthi','doidem','bingo','ceo']
S=1024;FEET=int(S*452/512);BODY=int(S*400/512)
meta={}
for c in ids:
    for k in 'zh':
        im=Image.open(f'ref/gen/{c}-{k}.png').convert('RGBA');a=np.asarray(im.getchannel('A'))
        ys,xs=np.nonzero(a>150);x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
        h=y1-y0;s=min(BODY/h,(S*.9)/(x1-x0))
        im2=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
        ox=S/2-(x0+x1)/2*s;oy=FEET-y1*s
        out=Image.new('RGBA',(S,S));out.alpha_composite(im2,(int(round(ox)),int(round(oy)))) if ox>=0 and oy>=0 else None
        if ox<0 or oy<0:
            out.paste(im2,(int(round(ox)),int(round(oy))),im2)
        out.save(f'img/nv/{c}-{k}.webp','WEBP',quality=82,method=6)
        A=np.asarray(out.getchannel('A'));ys,xs=np.nonzero(A>150);top=ys.min();band=(A>150)[top:top+int(BODY*.2)]
        by,bx=np.nonzero(band);hx,hy=bx.mean()/S,(top+by.mean())/S+.02
        if k=='z':meta[c]=[round(float(hx),3),round(float(hy),3)]
        # face crop around head
        cx,cy=int(hx*S),int((hy+.03)*S);half=int(S*.16)
        out.crop((cx-half,cy-half,cx+half,cy+half)).resize((256,256),Image.LANCZOS).save(f'img/nv/{c}-{k}a.webp','WEBP',quality=85,method=6)
json.dump(meta,open('/home/claude/work/gen/meta.json','w'));print(meta)
