from PIL import Image
from PyQt5 import QtWidgets
import subprocess
import os
# def openfile_compress():
#     filename = filedialog.askopenfilename(filetypes=[('All files','*.*')])
#     if filename=='':
#         return "ERROR"
#     return filename
# def savefile_compress():
#     filename = filedialog.asksaveasfilename(filetypes=[('Text file','*.txt')])
#     if filename=='':
#         return "ERROR"
#     filename = filename if filename.find(".txt") !=-1 else filename+".txt"
#     return filename


# def openfile_uncompress():
#     filename = filedialog.askopenfilename(filetypes=[('Text file','*.txt')])
#     if filename=='':
#         return "ERROR"
#     return filename
# def savefile_uncompress(extension):
#     extension = extension[:-1]
#     filename = filedialog.asksaveasfilename(filetypes=[(extension,'*'+extension)])
#     # print(filename,extension)
#     if filename=='':
#         return "ERROR"
#     filename = filename if filename.find(extension) !=-1 else filename+extension
#     return filename


def compress(ifname,ofname):
    global tb
    open_f=ifname
    


    save_f=ofname
    if(".dip" not in ofname):ofname+=".dip"
    # print(save_f)
    
    # print(r'.\hw8-b103040008 -c -i '+open_f+" -o "+save_f)
    subprocess.run([r'.\hw8-b103040008','-c','-i',open_f,'-o',save_f],shell=True)
    with open(save_f,"rb") as f:
        string=f.readline()
        while string!=b"00\n":
            # print(string)
            string=f.readline()
        f.readline()
        f.readline()
        output_text = (f.readline() + f.readline() + f.readline()).decode('ascii')
    

# def uncompress(ifname,ofname):
#     open_f=ifname


#     with open(open_f,"rb") as f:
#         string=f.readline()
#         while string!=b"00\n":
#             string=f.readline()
#         trash,extension = os.path.splitext(f.readline().decode('ascii'))
#         # print(trash,extension)

#         save_f=ofname
#         fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
#         # print(open_f,save_f)
#         # print(r'.\hw8-b103040008 -u -i '+open_f+" -o "+save_f)
#         subprocess.run([r'.\hw8-b103040008','-u','-i',open_f,"-o",save_f],shell=True)



