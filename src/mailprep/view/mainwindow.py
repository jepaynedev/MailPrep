"""Main window view with view-specific logic"""
import logging
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QMainWindow, QFileDialog
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep  # pylint: disable=no-name-in-module,import-error
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

        # Set default window state
        self.setWindowState(Qt.WindowMaximized)
        self.ui.dockWidget_output.setVisible(False)
        self.ui.treeView_fileList.setModel(self.ctrl.file_system_model)
        self.splitDockWidget(
            self.ui.dockWidget__fileList,
            self.ui.dockWidget_jobProperties,
            Qt.Vertical
        )

        self.new_job_dialog = NewJobDialog()

        # Create list to hold file input widgets
        self.file_input_widgets = []

        # Register signals
        # pylint: disable = no-member, fixme
        # TODO: Remove no-member lint suppression when fixed for PySide2 Signal connect methods
        # TODO: See https://github.com/PyCQA/pylint/issues/2585
        self.ui.actionNewJob.triggered.connect(self.on_new_job)
        self.ui.actionBrowseCustomCampus.triggered.connect(QFileDialog.getOpenFileName)
        self.ui.actionOpenJob.triggered.connect(self.on_open_job)
        self.ui.actionAddFiles.triggered.connect(self.on_add_files)
        # pylint: enable = no-member, fixme

    @Slot()
    def set_file_list_view(self, path):
        """Sets a given path for the file list tree view"""
        self.ctrl.file_system_model.set_current_root(path)
        self.ui.treeView_fileList.setRootIndex(self.ctrl.file_system_model.root_path_index)
        for i in range(1, self.ctrl.file_system_model.columnCount()):
            self.ui.treeView_fileList.hideColumn(i)

    @Slot()
    def on_new_job(self):
        """Trigger on new job action to prompt for new job data"""
        self.new_job_dialog.show()

    @Slot()
    def on_open_job(self):
        """View updates trigged when opening a job instance"""
        self.ui.actionClose.setEnabled(True)

    @Slot()
    def on_add_files(self):  # pylint: disable = no-self-use
        """View updates trigged adding files to a job"""
        log.debug('addFiles')
        (add_paths, _) = QFileDialog.getOpenFileNames()
        log.debug('add_paths: %s', add_paths)
        # TODO: Add code to add files and remove pylint disable when finished  # pylint: disable = fixme
