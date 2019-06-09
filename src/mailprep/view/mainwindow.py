"""Main window view with view-specific logic"""
import logging
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QMainWindow, QFileDialog
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep  # pylint: disable=no-name-in-module,import-error
from mailprep.view.fileinput import FileInput
from mailprep.view.new_job_dialog import NewJobDialog

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window view for the application"""

    def __init__(self, controller):
        super(MainWindow, self).__init__()
        self.ctrl = controller

        log.debug('Loading MainWindow')
        self.ui = Ui_MainWindow_MailPrep()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)

        self.new_job_dialog = NewJobDialog()

        # Create list to hold file input widgets
        self.file_input_widgets = []
        self.ui.verticalLayout_files.setAlignment(Qt.AlignTop)

        # Register signals
        self.ui.actionNewJob.triggered.connect(self.on_new_job)
        self.ui.actionBrowseCustomCampus.triggered.connect(QFileDialog.getOpenFileName)
        self.ui.actionOpenJob.triggered.connect(self.on_open_job)
        self.ui.actionAddFiles.triggered.connect(self.on_add_files)

    @Slot()
    def on_new_job(self):
        """Trigger on new job action to prompt for new job data"""
        dialog = self.new_job_dialog.show()

    @Slot()
    def on_open_job(self):
        """View updates trigged when opening a job instance"""
        log.debug('opening from job number: %s', self.ui.lineEdit_jobNumber.text())
        self.ui.actionClose.setEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(1)

    @Slot()
    def on_add_files(self):
        """View updates trigged adding files to a job"""
        log.debug('addFiles')
        (add_paths, _) = QFileDialog.getOpenFileNames()
        log.debug('add_paths: %s', add_paths)
        for file_path in add_paths:
            self.file_input_widgets.append(FileInput(file_path))
        for file_input_widget in self.file_input_widgets:
            self.ui.verticalLayout_files.addWidget(file_input_widget)
