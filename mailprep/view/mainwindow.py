import logging
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtCore import QFile
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        log.debug('Loading MainWindow')
        self.ui = Ui_MainWindow_MailPrep()
        self.ui.setupUi(self)

        self.ui.actionBrowseCustomCampus.triggered.connect(QFileDialog.getOpenFileName)
        self.ui.actionOpenJob.triggered.connect(self.openJob)

    def openJob(self):
        log.debug(f'opening from job number: {self.ui.lineEdit_jobNumber.text()}')
        self.ui.actionClose.setEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(1)
