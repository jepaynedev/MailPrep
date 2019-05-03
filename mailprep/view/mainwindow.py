import logging
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QFile
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        log.debug('Loading MainWindow')
        self.ui = Ui_MainWindow_MailPrep()
        self.ui.setupUi(self)
