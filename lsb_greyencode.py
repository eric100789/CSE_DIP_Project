from PIL import Image

def int_to_binary(integer, s):
    binary_string = ''
    while(integer > 0):
        digit = integer % 2
        binary_string += str(digit)
        integer = integer // 2
    binary_string = binary_string[::-1]
    while(len(binary_string) != s):
        binary_string = '0'+binary_string
    return binary_string

def LSB_full_grey(tarImage, keyImage, tarNum, keyNum):
    if( tarNum + keyNum !=8 ):
        raise ValueError
    x,y = tarImage.size
    keyImage = keyImage.resize( (x,y) )
    tarImage = tarImage.convert('L')
    keyImage = keyImage.convert('L')

    for i in range(x):
        for j in range(y):
            a = int_to_binary(tarImage.getpixel((i,j))//2**(8-tarNum),tarNum)
            b = int_to_binary(keyImage.getpixel((i,j))//2**(8-keyNum),keyNum)
            tarImage.putpixel((i,j), int(a+b, 2)) 
    
    return tarImage

if __name__ == '__main__':
    im = Image.open("input/test1.jpg")
    r = Image.open("input/test2.jpg")

    im = LSB_full_grey(im, r, 6, 2)
    im.show()