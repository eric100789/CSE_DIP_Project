from PIL import Image, ImageDraw, ImageFont
import numpy as np

def BWpicture(im):
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if(im.getpixel((i,j))>150):
                im.putpixel((i,j),255)
            else:
                im.putpixel((i,j),0)
    return im

def LSB_text(tarImage, text, color, size, fontname):
    x,y = tarImage.size
    im = Image.new(mode='L', size=(x, y), color="white")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(fontname, size)
    draw.text( (0,0), text, font=font)
    im = LSB(tarImage, im, color)
    return im

def LSB(tarImage, keyImage, color):
    if color not in "RGB":
        raise KeyError
    keyImage = BWpicture(keyImage)
    x,y = tarImage.size
    keyImage = keyImage.resize( (x,y) )

    tarNp = np.array(tarImage)
    keyNp = np.array(keyImage)

    for i in range(x):
        for j in range(y):
            r,g,b = tarNp[i][j]
            key = keyNp[i][j]
            if(color == 'R'):
                if(key==0):
                    tarNp[i][j][0] = r+(r%2-1)
                else:
                    tarNp[i][j][0] = r+(r%2)
            elif(color == 'G'):
                if(key==0):
                    tarNp[i][j][1] = g+(g%2-1)
                else:
                    tarNp[i][j][1] = g+(g%2)
            elif(color == 'B'):
                if(key==0):
                    tarNp[i][j][2] = b+(b%2-1)
                else:
                    tarNp[i][j][2] = b+(b%2)
    im = Image.fromarray(tarNp)
    return im
    
def LSB_decode(tarImage,color):
    if color not in "RGB":
        raise KeyError
    x,y = tarImage.size
    im = Image.new(mode='L', size=(x, y))

    for i in range(x):
        for j in range(y):
            r,g,b = tarImage.getpixel((i,j))
            if(color == 'R' and r%2==0):
                im.putpixel((i,j),255) 
            elif(color == 'G' and g%2==0):
                im.putpixel((i,j),255)
            elif(color == 'B' and b%2==0):
                im.putpixel((i,j),255)
    return im
    

if __name__ == '__main__':
    im = Image.open("input/test1.jpg")
    r = Image.open("input/test2.jpg").convert('L')
    im = LSB(im,r,'R')
    g = Image.open("input/test4.png").convert('L')
    im = LSB(im,g,'G')
    text =\
    """
    We're no strangers to love
    You know the rules and so do I (do I)
    A full commitment's what I'm thinking of
    You wouldn't get this from any other guy
    I just wanna tell you how I'm feeling
    Gotta make you understand
    Never gonna give you up
    Never gonna let you down
    Never gonna run around and desert you
    Never gonna make you cry
    Never gonna say goodbye
    Never gonna tell a lie and hurt you
    """
    im = LSB_text(im, text, 'B', 50, "font/MustardSmile.ttf")
    im.save("output/LSB_output1.png")

    decode = Image.open("output/LSB_output1.png")
    LSB_decode(decode,"R").save("output/LSB_output2.png")
    LSB_decode(decode,"G").save("output/LSB_output3.png")
    LSB_decode(decode,"B").save("output/LSB_output4.png")
