from PIL import Image
import numpy as np
import time
import os
import sys
x=95
d="@QB#NgWM8RDHdOKq9$6khEPXwmeZaoS2yjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,'.-` "
ss="\n"*x
def image_to_ascii_converter(name):
    global d
    im =Image.open(name)
    im=im.convert("L")
    im.thumbnail((im.size[0]/im.size[1]*x,x))
    arr=np.array(im)/256*69
    arr=arr.astype(int)
    s=[]
    sss=""
    for i in arr:
        t="".join(d[j] for j in i)
        s.append(t)
    for i in s:
        sss+="\n"+i
    # write
    # os.system('cls')
    print(sss)
    time.sleep(1/60-0.0002)
