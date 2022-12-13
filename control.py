from PyQt5 import QtWidgets,QtGui,QtCore
from ui import Ui_MainWindow
from PIL import ImageQt
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
    def open_im(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Image','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
        if fileName:
            self.type=fileType
            self.image=QtGui.QImage(fileName)
            if self.ui.imgLabel.size().height() < self.image.size().height() or  self.self.ui.imgLabel.size().width() < self.image.size().width():
                self.show_image=QtGui.QPixmap.fromImage(self.image).scaled(self.ui.imgLabel.size(),aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            else:
                self.show_image=QtGui.QPixmap.fromImage(self.image)
            self.path=fileName
            if self.image.isNull():
                QtWidgets.QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return
            self.zoom_factor=1.0
            
            self.ui.imgLabel.setPixmap(self.show_image)
            self.ui.filename.setText(fileName)
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
        self.image.save(self.path)
    def save_as_im(self):
        if self.image is None or self.image.isNull():
            QtWidgets.QMessageBox.information(self, "Image Viewer", "An Error has occured when loading the Image.")
            return
        fileName, fileType = QtWidgets.QFileDialog.getSaveFileName(self, 'QFileDialog.getOpenFileName()','','Images (*.png *.jpeg *.jpg *.bmp *.gif)')
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
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

    


