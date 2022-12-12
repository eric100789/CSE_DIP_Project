from blind_watermark import WaterMark
from PIL import Image

encodePicture = WaterMark(password_wm=1, password_img=1) 

PROTECTED_NAME = 'input/test1.jpg'
WATERMARK_NAME = 'input/test2.jpg'
ENCODED_NAME = 'output/output1.png'
TEMP_NAME = 'output/temp.jpg'
DECODE_NAME = 'output/output2.png'

def EncodePicture():
    global PROTECTED_NAME, WATERMARK_NAME, ENCODED_NAME, TEMP_NAME, DECODE_NAME
    encodePicture.read_img(PROTECTED_NAME) #保護的圖
    encodePicture.read_wm(WATERMARK_NAME) #浮水印
    try:
        encodePicture.embed(ENCODED_NAME) #產出圖
    except AssertionError:
        img = Image.open(WATERMARK_NAME)
        (w, h) = img.size
        new_img = img.resize((120, 120))
        WATERMARK_NAME = TEMP_NAME
        new_img.save(WATERMARK_NAME)
        encodePicture.read_wm(WATERMARK_NAME)
        encodePicture.embed(ENCODED_NAME)

def DecodePicture(ENCODED_NAME):
    global PROTECTED_NAME, WATERMARK_NAME, TEMP_NAME, DECODE_NAME
    # img = Image.open(ENCODED_NAME)
    # (w, h) = img.size
    decodePicture = WaterMark(password_wm=1, password_img=1)
    decodePicture.extract(filename=ENCODED_NAME, wm_shape=(120, 120), out_wm_name= DECODE_NAME, )

# DecodePicture('input/attack1.png') #亂字攻擊
# DecodePicture('input/attack2.png') #模糊攻擊
# DecodePicture('input/attack3.png') #裁切攻擊