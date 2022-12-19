from PIL import Image
import cv2
import os
import collections
import numpy as np

def pre() :
    before_pic_path = r"./train" #這裡改成我附給你的資料夾，你存在電腦的位置
    after_process_path = r"./processing" #這裡改成我附給你的資料夾，預處理後，你存在電腦的位置
    all_file = os.listdir( before_pic_path )
    num = 0
    for file in all_file:
        num += 1
        img_path = before_pic_path + "//" + file
        image = cv2.imread ( img_path )
        image = cv2.resize ( image ,(100,100) )
        cv2.imwrite( after_process_path + "//" + file , image )
        print( num )

def index():
    after_process_path = r"./processing"
    all_file = os.listdir( after_process_path )
    num = 0
    string = ''
    for file in all_file  :
        num += 1
        img_path = after_process_path + "//" + file
        image = cv2.imread( img_path )
        list_one = []
        for i in range(100):
            for j in range(100):
                b = image [i,j,0]
                g = image [i,j,1]
                r = image [i,j,2]
                list_one.append( ( b , g , r ) )
        m = collections.Counter( list_one ).most_common( 1 )
        string += file
        string += ":"
        string += str( m[0][0] ).replace( "(" , "" ).replace( ")" , "" )
        string += "\n"
        print( num )
    file_output = open( 'index.txt','w' )
    file_output.write( string )


def readIndex():
    index_file = open( "index.txt","r" )
    num = 0
    dic_index =[]
    for line in index_file.readlines():
        num += 1
        temp = line.split( ":" )
        file = temp[0]
        color = temp[1].split( "," )
        b = int( color[0] )
        g = int( color[1] )
        r = int( color[2] )
        dic_index.append( ( file , ( b , g , r ) ) )
    return dic_index

def montage ( img_input ):
    pre()
    index()
    after_process_path = r"./processing"
    image_to_montage = cv2.cvtColor(np.asarray(img_input), cv2.COLOR_RGB2BGR)
    m_photo = np.shape ( image_to_montage )
    big_pic = np.zeros ( ( 100 * m_photo[0] , 100 * m_photo[1] , 3 ), dtype = np.uint8 )
    small_list = readIndex() 
    for i in range( m_photo[0] ):
        for j in range( m_photo[1] ):
            print( i )
            m_photo_b = image_to_montage[i, j, 0]
            m_photo_g = image_to_montage[i, j, 1]
            m_photo_r = image_to_montage[i, j, 2]
            np.random.shuffle( small_list ) 
            for item in small_list :
                s_photo_b = item[1][0]
                s_photo_g = item[1][1]
                s_photo_r = item[1][2]
                odistance=( s_photo_b - m_photo_b ) ** 2 + ( s_photo_g - m_photo_g ) ** 2 + ( s_photo_r - m_photo_r ) ** 2
                if odistance < 500:
                    file_path = after_process_path + "//" + str( item[0] )
                    break
            little_pic = cv2.imread(file_path)
            big_pic [i * 100 : ( i + 1 ) * 100 , j * 100 : ( j + 1 ) * 100] = little_pic
    
    image_return = Image.fromarray( big_pic )
    return image_return

