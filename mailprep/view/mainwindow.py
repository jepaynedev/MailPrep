from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QFile
from mailprep.ui.mainwindow_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
