import logging
import os.path
from PySide2.QtWidgets import QWidget
from mailprep.ui.fileinput_ui import Ui_FileInput

log = logging.getLogger(__name__)

class FileInput(QWidget):
    def __init__(self, filePath):
        super(FileInput, self).__init__()
        log.debug(f'FileInput.__init__({filePath})')

        self.filePath = filePath
        self.fileName = os.path.basename(self.filePath)

        self.ui = Ui_FileInput()
        self.ui.setupUi(self)

        self.ui.lineEdit_fileName.setText(self.fileName)

