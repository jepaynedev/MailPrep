"""Dialog with input for new job creation"""
import logging
from PySide2.QtWidgets import QDialog
from mailprep.ui.new_job_dialog_ui import Ui_NewJobDialog  # pylint: disable=no-name-in-module,import-error

log = logging.getLogger(__name__)


class NewJobDialog(QDialog):
    """Dialog with input for new job creation"""

    def __init__(self):
        super(NewJobDialog, self).__init__()
        log.debug('NewJobDialog.__init__()')

        self.ui = Ui_NewJobDialog()
        self.ui.setupUi(self)
