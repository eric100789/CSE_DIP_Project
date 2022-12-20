import time
from PyQt5 import QtWidgets,QtGui,QtCore,QtTest
from ui import Ui_MainWindow
from PIL import ImageQt,Image
import os
import subprocess
from os import listdir
from os.path import isfile,join
import win32clipboard
class FileList():
    def __init__(self):
        self.pointer=0
        self.file_list=[]
    def __init__(self,dir):
        self.pointer=0
        self.file_list = [f for f in listdir(dir) if isfile(join(dir, f)) and self.isImage(join(dir, f))]
        self.file=self.file_list[self.pointer]
    def isImage(self,file):
        if ".jpg" in file or ".png" in file or ".jpeg" in file or ".gif" in file or ".bmp" in file or ".dip" in file:
            return True
        return False

    def printf(self):
        print(self.file_list[self.pointer])
    def next(self):
        self.pointer = (self.pointer+1) % len(self.file_list)
        self.file=self.file_list[self.pointer]
    def prev(self):
        self.pointer = (self.pointer-1) % len(self.file_list)
        self.file=self.file_list[self.pointer]
    def find_file(self,s):
        self.pointer = self.file_list.index(s)
        self.file=self.file_list[self.pointer]

class Undo_List():
    def __init__(self):
        self.pointer=-1
        self.undo_list=[]
    def __init__(self,im):
        self.pointer=0
        self.undo_list=[im]
    def img_add(self,img):
        self.undo_list=self.undo_list[:self.pointer+1]
        self.undo_list.append(img)
        self.pointer+=1
    def undo(self):
        if self.pointer==0:
            return self.undo_list[0]
        self.pointer-=1
        return self.undo_list[self.pointer]
    def redo(self):
        if self.pointer==len(self.undo_list)-1:
            return self.undo_list[self.pointer]
        self.pointer+=1
        return self.undo_list[self.pointer]
    def isFront(self):
        return self.pointer==0
    def isNull(self):
        return len(self.undo_list)==0
    def isBack(self):
        return self.pointer==len(self.undo_list)-1
       
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setStyleSheet('background-color:"#C5222222";color: "#E6E6FA"')
        self.ui = Ui_MainWindow()
        self.eyedroppered=False
        self.Saved=True
        self.image=None
        # self.setMouseTracking(True)
       
        self.ui.setupUi(self)
        # self.ui.imgLabel.setMouseTracking(True)
        self.setup()
        self.ui.imgLabel.mouseMoveEvent = self.mouseMoveEvent
    def setup(self):
        self.ui.ascii_displayer.hide()
        self.ui.exit_ascii_displayer_btn.hide()
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.ui.actionOpen.triggered.connect(self.open_im)
        self.ui.actionOpen.setShortcut("Ctrl+O")
        self.ui.actionSave.triggered.connect(self.save_im)
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave_as.triggered.connect(self.save_as_im)
        self.ui.actionSave_as.setShortcut("Ctrl+Shift+S")
        self.ui.actionZoom_In.triggered.connect(self.zoom_in)
        self.ui.actionZoom_In.setShortcut("Ctrl+=")
        self.ui.actionZoom_Out.triggered.connect(self.zoom_out)
        self.ui.actionZoom_Out.setShortcut("Ctrl+-")
        self.ui.actionDefault_Size.triggered.connect(self.zoom_to_default)
        self.ui.actionDefault_Size.setShortcut("Ctrl+\\")
        self.ui.actionAscii_Art.triggered.connect(self.show_ascii)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionUndo.setShortcut("Ctrl+Z")
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionRedo.setShortcut("Ctrl+Shift+Z")
        self.ui.actionRotate_90.triggered.connect(self.rotate_90)
        self.ui.actionRotate_91.triggered.connect(self.rotate_91)
        self.ui.actionhorizontal_flip.triggered.connect(self.horizonal_flip)
        self.ui.actionVertical_Flip.triggered.connect(self.vertical_flip)
        self.ui.file_tree.clicked.connect(self.file_clicked)
        self.ui.next_img.clicked.connect(self.next_clicked)
        self.ui.next_img.setShortcut("Right")
        self.ui.prev_img.clicked.connect(self.prev_clicked)
        self.ui.prev_img.setShortcut("Left")
        self.ui.exit_ascii_displayer_btn.clicked.connect(self.exit_ascii)
        self.ui.actionImage_Color_Picker.triggered.connect(self.eyedropper)
        self.ui.actionImage_Color_Picker.setShortcut("Alt+E")
        self.ui.actionLSB_Encode.triggered.connect(self.lsb_encode)
        self.ui.actionLSB_Decode.triggered.connect(self.lsb_decode)
        self.ui.actionLSB_full_grey.triggered.connect(self.lsb_grey)
        self.ui.actionMontage.triggered.connect(self.im_montage)
        self.ui.actionCompression.triggered.connect(self.im_compress)
        self.ui.actionUncompression.triggered.connect(self.im_uncompress)
    def set_img(self,im=None):
        # print(self.name)
        if not im:
            if '.dip' in self.name:
                subprocess.run([r'.\hw8-b103040008','-u','-i',self.name,'-o','ABL@#Ff$43KSJFLKJFSLKFJ.jpg'],shell=True)
                # time.sleep(1)
                self.image=QtGui.QImage(self.dir+"/"+'ABL@#Ff$43KSJFLKJFSLKFJ.jpg')
                # print(self.image)
                self.undolist=Undo_List(ImageQt.fromqimage(self.image))
            else:
                self.image=QtGui.QImage(self.dir+"/"+self.file_list.file)
                self.undolist=Undo_List(ImageQt.fromqimage(self.image))
        else:
            self.image=ImageQt.ImageQt(im)
            self.Saved=self.undolist.isFront()
        if self.image.isNull():
            QtWidgets.QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.file_list.file)
            return
        if self.ui.imgLabel.size().height() < self.image.size().height() or  self.ui.imgLabel.size().width() < self.image.size().width():
            self.show_image=QtGui.QPixmap.fromImage(self.image).scaled(self.ui.imgLabel.size(),aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.show_image=QtGui.QPixmap.fromImage(self.image)
        self.ui.imgLabel.setPixmap(self.show_image)
        self.ui.filename.setText(self.dir+'/'+self.file_list.file)
        self.zoom_factor=1.0
        self.zoom_to_default()
        self.degree=0
        
    def model_element_append(self):
        self.model = QtGui.QStandardItemModel()
        for file in self.file_list.file_list:
            i = QtGui.QStandardItem(file)
            self.model.appendRow(i)

            i.setData(QtGui.QIcon(join('.','ico','image.png')),1)
    def open_im(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image','','Images (*.png *.jpeg *.jpg *.bmp *.gif *.dip)')
        if fileName:
            self.name=fileName
            self.type=fileType
            self.dir=fileName[:fileName.rfind('/')]
            self.file_list=FileList(self.dir)
            self.file_list.find_file(fileName[fileName.rindex('/')+1:])
            self.set_img()
            if self.image.isNull():
                return
            # self.model = QtWidgets.QFileSystemModel()
            # self.model.setRootPath(self.dir)
            # self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
            # self.model.setNameFilters(("*.png","*.jpeg","*.jpg","*.bmp","*.gif"))
            # self.model.setNameFilterDisables(False)
            self.model_element_append()
            self.ui.file_tree.setModel(self.model)
            # self.ui.file_tree.setRootIndex(self.model.index(self.dir))
            self.scaleFactor = 1.0
            self.ui.actionSave.setEnabled(True)
            self.ui.actionSave_as.setEnabled(True)
            self.ui.menuDisplay.setEnabled(True)
            self.ui.menuEdit.setEnabled(True)
            self.ui.menuTools.setEnabled(True)
    def save_im(self):
        if self.image is None or self.image.isNull():
            QtWidgets.QMessageBox.information(self, "Image Viewer", "An Error has occured when loading the Image.")
            return
        self.image.save(self.dir+'/'+self.file_list.file)
    def save_as_im(self):
        if self.image is None or self.image.isNull():
            QtWidgets.QMessageBox.information(self, "Image Viewer", "An Error has occured when loading the Image.")
            return
        fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        self.image.save(fileName)
        self.file_reload(fileName)
        # pass
    def zoom_in(self):
        self.zoom_factor*=1.25
        self.show_image = QtGui.QPixmap.fromImage(self.image).scaled(self.zoom_factor*self.image.size())
        self.zoom_factor_check()
        self.ui.imgLabel.setPixmap(self.show_image)
    def zoom_out(self):
        self.zoom_factor*=0.8
        self.show_image = QtGui.QPixmap.fromImage(self.image).scaled(self.zoom_factor*self.image.size())
        self.zoom_factor_check()
        self.ui.imgLabel.setPixmap(self.show_image)
    def zoom_factor_check(self):
        self.ui.actionZoom_Out.setEnabled(0.333 < self.zoom_factor )
        self.ui.actionZoom_In.setEnabled(self.zoom_factor <3)
    def zoom_to_default(self):
        self.zoom_factor=1.0
        if self.ui.imgLabel.size().height() < self.image.size().height() or  self.ui.imgLabel.size().width() < self.image.size().width():
            self.show_image=QtGui.QPixmap.fromImage(self.image).scaled(self.ui.imgLabel.size(),aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.show_image=QtGui.QPixmap.fromImage(self.image)
        self.ui.actionZoom_Out.setEnabled(True)
        self.ui.actionZoom_In.setEnabled(True)
        self.ui.imgLabel.setPixmap(self.show_image)
        # pass
    def show_ascii(self):
        from ascii import image_to_ascii_converter
        self.ui.ascii_displayer.show()
        self.ui.exit_ascii_displayer_btn.show()
        im=ImageQt.fromqimage(self.image)
        ascii = image_to_ascii_converter(im)
        LENGTH=325
        im.thumbnail((im.size[0]/im.size[1]*LENGTH,LENGTH))
        self.ui.ascii_displayer.setText(ascii)
        
    def exit_ascii(self):
        self.ui.ascii_displayer.hide()
        self.ui.exit_ascii_displayer_btn.hide()
    def file_clicked(self):
        index=self.ui.file_tree.selectedIndexes()[0]
        dir_or_img = self.model.itemFromIndex(index).text()
        if ".jpg" in dir_or_img or ".png" in dir_or_img or ".jpeg" in dir_or_img or ".gif" in dir_or_img or ".bmp" in dir_or_img or ".dip" in dir_or_img:
            try:
                os.remove("./ABL@#Ff$43KSJFLKJFSLKFJ.jpg")
            except:
                pass
            self.name=dir_or_img
            self.file_list.find_file(dir_or_img)
            self.set_img()

    def next_clicked(self):
        self.file_list.next()
        self.name=self.file_list.file
        self.set_img()

    def prev_clicked(self):
        self.file_list.prev()
        self.name=self.file_list.file
        self.set_img()

    def undo(self):
        if not self.undolist.isFront():
            im=self.undolist.undo()
            self.set_img(im)
    
    def redo(self):
        if not self.undolist.isBack():
            im=self.undolist.redo()
            self.set_img(im)
    
    def rotate_90(self):
        im = ImageQt.fromqimage(self.image)
        im=im.rotate(90,expand=1)
        self.undolist.img_add(im)
        self.set_img(im)
        self.Saved=False

    def rotate_91(self):
        im = ImageQt.fromqimage(self.image)
        im=im.rotate(270,expand=1)
        self.undolist.img_add(im)
        self.set_img(im)
        self.Saved=False

    def horizonal_flip(self):
        im = ImageQt.fromqimage(self.image)
        im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.undolist.img_add(im)
        self.set_img(im)
        self.Saved=False

    def vertical_flip(self):
        im = ImageQt.fromqimage(self.image)
        im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.undolist.img_add(im)
        self.set_img(im)
        self.Saved=False
    # def mouseMoveEvent(self, event):
    #     print(event.x(),event.y())
    def mouseMoveEvent(self,event):
        if self.eyedroppered:
            im=ImageQt.fromqpixmap(self.ui.imgLabel.grab())
            pos=(event.x(),event.y())#-631,-233
            # print(event.x(),event.y())
            self.ui.color_label.setStyleSheet("background-color:rgb{}".format(str(im.getpixel(pos))))
    def eyedropper(self):
        self.ui.imgLabel.mouseReleaseEvent = self.release_eyedropper
        self.ui.imgLabel.setMouseTracking(True)
        self.eyedroppered=True
       
        # pass
    # def move_eyedropper(self,event):
    #     self.setMouseTracking(True)
    #     im=ImageQt.fromqpixmap(self.ui.imgLabel.grab())
    #     pos=QtGui.QCursor.pos()
    #     pos=(pos.x()-631,pos.y()-233)
    #     print(pos,event.x(),event.y())
    #     self.ui.color_label.setStyleSheet("background-color:rgb{}".format(str(im.getpixel(pos))))
    def release_eyedropper(self,event):
        # print("release"*10)
        im=ImageQt.fromqpixmap(self.ui.imgLabel.grab())
        pos=(event.x(),event.y())#-631,-233
        # print(event.x(),event.y())
        self.ui.color_label.setStyleSheet("background-color:rgb{}".format(str(im.getpixel(pos))))
        # print(im.getpixel(pos))
        self.ui.imgLabel.mouseReleaseEvent = None
        self.ui.imgLabel.setMouseTracking(False)
        self.eyedroppered=False
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(str(im.getpixel(pos)))
        win32clipboard.CloseClipboard()
        # print(im.getpixel((QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y())))
        self.ui.filename.setText("Copy Successed!")
        QtTest.QTest.qWait(2500)
        self.ui.filename.setText(self.dir+'/'+self.file_list.file)
    def file_reload(self,fileName):
        # print(fileName)
        self.file_list=FileList(self.dir)
        self.file_list.find_file(fileName[fileName.rindex('/')+1:])
        self.set_img()
        self.model_element_append()
        self.ui.file_tree.setModel(self.model)
    def lsb_encode(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        if fileName:
            from lsb_encoding import LSB,LSB_decode
            # print(self.name,fileName)
            o_im=Image.open(self.name)
            k_im=Image.open(fileName).convert('L')
            msgbox=QtWidgets.QMessageBox()
            msgbox.setText('Which Color')
            rb=msgbox.addButton('R',QtWidgets.QMessageBox.ButtonRole.YesRole)
            gb=msgbox.addButton('G',QtWidgets.QMessageBox.ButtonRole.NoRole)
            bb=msgbox.addButton('B',QtWidgets.QMessageBox.ButtonRole.RejectRole)
            msgbox.exec_()
            s=""
            if msgbox.clickedButton() == rb:
                s='R'
            elif msgbox.clickedButton() == gb:
                s='G'
            elif msgbox.clickedButton() == bb:
                s='B'
            new_im=LSB(o_im,k_im,s)
            fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
            new_im.save(fileName)
            self.image=ImageQt.toqimage(new_im)
            self.file_reload(fileName)
    def lsb_decode(self):
        from lsb_encoding import LSB_decode
        o_im=ImageQt.fromqimage(self.image)
        msgbox=QtWidgets.QMessageBox()
        msgbox.setText('Which Color')
        rb=msgbox.addButton('R',QtWidgets.QMessageBox.ButtonRole.YesRole)
        gb=msgbox.addButton('G',QtWidgets.QMessageBox.ButtonRole.NoRole)
        bb=msgbox.addButton('B',QtWidgets.QMessageBox.ButtonRole.RejectRole)
        msgbox.exec_()
        s=""
        if msgbox.clickedButton() == rb:
            s='R'
        elif msgbox.clickedButton() == gb:
            s='G'
        elif msgbox.clickedButton() == bb:
            s='B'

        new_im=LSB_decode(o_im,s)
        fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        new_im.save(fileName)
        self.image=ImageQt.toqimage(new_im)
        self.file_reload(fileName)
    def lsb_grey(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        if fileName:
            from lsb_greyencode import LSB_full_grey
            # print(self.name,fileName)
            o_im=Image.open(self.name)
            k_im=Image.open(fileName)
            new_im=LSB_full_grey(o_im,k_im,4,4)
            fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
            new_im.save(fileName)
            self.image=ImageQt.toqimage(new_im)
            self.file_reload(fileName)
    def im_montage(self):
        from hsiang import montage
        new_im=montage(ImageQt.fromqimage(self.image))
        fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        new_im.save(fileName)
        self.image=ImageQt.toqimage(new_im)
        self.file_reload(fileName)
    def im_compress(self):
        from compress import compress
        fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','Compresseed Images (*.dip)')
        if fileName:compress(self.name,fileName)
    def im_uncompress(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Compresseed Images','','Compresseed Images (*.dip)')
        with open(fileName,"rb") as f:
            string=f.readline()
            while string!=b"00\n":
                string=f.readline()
            trash,extension = os.path.splitext(f.readline().decode('ascii'))
            # print(trash,extension)

            save_f,type = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as','','(*%s)'%extension)
            # print(open_f,save_f)
            # print(r'.\hw8-b103040008 -u -i '+open_f+" -o "+save_f)
            subprocess.run([r'.\hw8-b103040008','-u','-i',fileName,"-o",save_f],shell=True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
    

    


