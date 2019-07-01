"""File input widget view with view-specific logic"""
import logging
import os.path
from PySide2.QtWidgets import QWidget
from mailprep.ui.fileinput_ui import Ui_FileInput  # pylint: disable=no-name-in-module,import-error

log = logging.getLogger(__name__)


class FileInput(QWidget):
    """File input widget view for data entry for a single file"""

    def __init__(self, file_path):
        super().__init__()
        log.debug('FileInput.__init__(%s)', file_path)

        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)

        self.ui = Ui_FileInput()
        self.ui.setupUi(self)

        self.ui.lineEdit_fileName.setText(self.file_name)
