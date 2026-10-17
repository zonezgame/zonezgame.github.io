import numpy as np,json,sys
from PIL import Image,ImageDraw
ids=['ngugat','deadline','trasua','songao','shipper','onthi','doidem','bingo','ceo']
ADJ=json.load(open('adj.json')) if __import__('os').path.exists('adj.json') else {}
def bbox(im):return im.getchannel('A').point(lambda v:255 if v>40 else 0).getbbox()
def head(im,bb,frac):
    a=np.asarray(im.getchannel('A'))>40;x0,y0,x1,y1=bb;h=y1-y0
    band=a[y0:y0+int(h*frac)];ys,xs=np.nonzero(band)
    return xs.mean(), y0+ys.mean()
META={}
for c in ids:
    z=Image.open(f'cut4/{c}-z.png');hm=Image.open(f'cut4/{c}-h.png')
    zb=bbox(z);hb=bbox(hm)
    zx,zy=head(z,zb,.22);hx,hy=head(hm,hb,.30)
    a=ADJ.get(c,{});zx+=a.get('zx',0);zy+=a.get('zy',0);hx+=a.get('hx',0);hy+=a.get('hy',0)
    zh=zb[3]-zb[1];zw=zb[2]-zb[0]
    s=min(400/zh,470/zw)
    # zombie: feet at 452, centered by bbox
    Z=Image.new('RGBA',(512,512));zs=z.resize((round(z.width*s),round(z.height*s)),Image.LANCZOS)
    ox=256-(zb[0]+zb[2])/2*s; oy=452-zb[3]*s
    za=np.asarray(zs.getchannel('A')).astype(np.float32);zb3=round(zb[3]*s);zf=int(zh*s*.07)
    for i in range(zf):za[zb3-zf+i]*=(1-i/zf)**1.5
    zs.putalpha(Image.fromarray(za.astype(np.uint8)))
    Z.alpha_composite(zs,(round(ox),round(oy)))
    HX=zx*s+ox;HY=zy*s+oy
    # human: same scale, head aligned to zombie head
    H=Image.new('RGBA',(512,512));hs=hm.resize((round(hm.width*s),round(hm.height*s)),Image.LANCZOS)
    a_=np.asarray(hs.getchannel('A')).astype(np.float32)
    bot=round(hb[3]*s);fade=int((hb[3]-hb[1])*s*.18)
    for i in range(fade):a_[bot-fade+i]*= (1-i/fade)
    hs.putalpha(Image.fromarray(a_.astype(np.uint8)))
    H.alpha_composite(hs,(round(HX-hx*s),round(HY-hy*s))) if True else None
    Z.save(f'out/{c}-zombie.png');H.save(f'out/{c}-nguoi.png')
    META[c]=[round(float(HX)/512,3),round(float(HY)/512+.02,3)]
json.dump(META,open('out/meta.json','w'))
# preview
P=Image.new('RGB',(9*200,420),(70,74,84));d=ImageDraw.Draw(P)
for i,c in enumerate(ids):
    for j,k in enumerate(['zombie','nguoi']):
        im=Image.open(f'out/{c}-{k}.png').resize((200,200));t=Image.new('RGBA',(200,200),(70,74,84,255));t.alpha_composite(im);P.paste(t,(i*200,j*210))
        hx,hy=META[c];d.ellipse((i*200+hx*200-4,j*210+hy*200-4,i*200+hx*200+4,j*210+hy*200+4),outline='red',width=2)
P.save('preview.png');print(META)
