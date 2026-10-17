import onnxruntime as ort,numpy as np,os
from PIL import Image
sess=ort.InferenceSession('/home/claude/work/isnet.onnx',providers=['CPUExecutionProvider'])
inp=sess.get_inputs()[0].name
os.makedirs('cut2',exist_ok=True)
def mask(im):
    x=np.asarray(im.convert('RGB').resize((1024,1024),Image.LANCZOS)).astype(np.float32)/255.
    x=x/max(x.max(),1e-6);x=(x-0.5)/1.0
    x=x.transpose(2,0,1)[None]
    p=sess.run(None,{inp:x})[0][0,0]
    p=(p-p.min())/(p.max()-p.min()+1e-8)
    return Image.fromarray((p*255).astype(np.uint8)).resize(im.size,Image.LANCZOS)
for f in sorted(os.listdir('raw')):
    im=Image.open('raw/'+f).convert('RGB');im=im.resize((im.width*2,im.height*2),Image.LANCZOS)
    m=mask(im);o=im.convert('RGBA');o.putalpha(m);o.save('cut2/'+f);print(f)
