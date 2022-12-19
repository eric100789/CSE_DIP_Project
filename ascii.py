from PIL import Image
import numpy as np
import time
LENGTH=325
GREY_MAP="@QB#NgWM8RDHdOKq9$6khEPXwmeZaoS2yjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,'.-` "
ss="\n"*LENGTH
def image_to_ascii_converter(im):
    im=im.convert("L")
    im.thumbnail((im.size[0]/im.size[1]*LENGTH,LENGTH))
    # im.show()
    arr=np.array(im)/256*69
    arr=arr.astype(int)
    im_in_ascii_arr=[]
    im_in_ascii=""
    for i in arr:
        t="".join(GREY_MAP[j]*3 for j in i)
        im_in_ascii_arr.append(t)
    for i in im_in_ascii_arr:
        im_in_ascii+="\n"+i
    return im_in_ascii
# a=image_to_ascii_converter(Image.open("test.jpg"))
# print(a)
# print(len(a))