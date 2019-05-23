import logging
from PySide2.QtCore import Qt, QFile
from PySide2.QtWidgets import QMainWindow, QFileDialog
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep
from mailprep.view.fileinput import FileInput

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):



    def __init__(self):
        super(MainWindow, self).__init__()
        log.debug('Loading MainWindow')
        self.ui = Ui_MainWindow_MailPrep()
        self.ui.setupUi(self)

        # Create list to hold file input widgets
        self.fileInputWidgets = []
        self.ui.verticalLayout_files.setAlignment(Qt.AlignTop)

        self.ui.actionBrowseCustomCampus.triggered.connect(QFileDialog.getOpenFileName)
        self.ui.actionOpenJob.triggered.connect(self.openJob)
        self.ui.actionAddFiles.triggered.connect(self.addFiles)


    def openJob(self):
        log.debug(f'opening from job number: {self.ui.lineEdit_jobNumber.text()}')
        self.ui.actionClose.setEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(1)

    def addFiles(self):
        log.debug(f'addFiles')
        (addFiles, _) = QFileDialog.getOpenFileNames()
        log.debug(f'addFiles: {addFiles}')
        for filePath in addFiles:
            self.fileInputWidgets.append(FileInput(filePath))
        for fileInputWidget in self.fileInputWidgets:
            self.ui.verticalLayout_files.addWidget(fileInputWidget)

