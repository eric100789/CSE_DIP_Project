from PyQt5 import QtWidgets,QtGui,QtCore
from ui import Ui_MainWindow
from PIL import ImageQt
from os import listdir
from os.path import isfile,join
class FileList():
    def __init__(self):
        self.pointer=0
        self.file_list=[]
    def __init__(self,dir):
        self.pointer=0
        self.file_list = [f for f in listdir(dir) if isfile(join(dir, f)) and self.isImage(join(dir, f))]
        self.file=self.file_list[self.pointer]
    def isImage(self,file):
        if ".jpg" in file or ".png" in file or ".jpeg" in file or ".gif" in file or ".bmp" in file:
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
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.image=None
        self.isVerticalFlip=False
        self.isHorizontalFlip=False
        self.rotation_degree=0
        self.ui.setupUi(self)
        self.setup()
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
        self.ui.file_tree.clicked.connect(self.file_clicked)
        self.ui.next_img.clicked.connect(self.next_clicked)
        self.ui.next_img.setShortcut("Right")
        self.ui.prev_img.clicked.connect(self.prev_clicked)
        self.ui.prev_img.setShortcut("Left")
        self.ui.exit_ascii_displayer_btn.clicked.connect(self.exit_ascii)
    def set_img(self):
        
        self.image=QtGui.QImage(self.dir+"/"+self.file_list.file)
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
        
    def model_element_append(self):
        self.model = QtGui.QStandardItemModel()
        for file in self.file_list.file_list:
            i = QtGui.QStandardItem(file)
            self.model.appendRow(i)

            i.setData(QtGui.QIcon(join(self.dir,'ico','image.png')),1)
    def open_im(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        if fileName:
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
        ascii = image_to_ascii_converter(ImageQt.fromqimage(self.image))
        self.ui.ascii_displayer.setText(ascii)
    def exit_ascii(self):
        self.ui.ascii_displayer.hide()
        self.ui.exit_ascii_displayer_btn.hide()
    def file_clicked(self):
        index=self.ui.file_tree.selectedIndexes()[0]
        dir_or_img = self.model.itemFromIndex(index).text()
        if ".jpg" in dir_or_img or ".png" in dir_or_img or ".jpeg" in dir_or_img or ".gif" in dir_or_img or ".bmp" in dir_or_img :
            self.file_list.find_file(dir_or_img)
            self.set_img()

    def next_clicked(self):
        self.file_list.next()
        self.set_img()

    def prev_clicked(self):
        self.file_list.prev()
        self.set_img()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

    


