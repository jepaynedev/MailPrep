"""Main window view with view-specific logic"""
import logging
from PySide2.QtCore import Qt, Signal, Slot, QSettings
from PySide2.QtWidgets import QMainWindow, QFileDialog, QApplication
from PySide2.QtGui import QTextCursor
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep  # pylint: disable=no-name-in-module,import-error
from mailprep.view.new_job_dialog import NewJobDialog
from mailprep.model.qt_edit_types import QtEditTypes
from utils.logging_decorators import log_call


log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window view for the application"""

    open_job = Signal(str)

    def __init__(self):
        super().__init__()
        self.file_input_widgets = None
        self.new_job_dialog = None
        self.state_settings = None
        self.ui = None
        self.app_settings = None

    def initialize(self, app_settings):
        """Initialize in manual call so we can set up other application settings before the view"""
        # Has to be called ASAP to save and restore application state
        self.state_settings = QSettings(
            QSettings.NativeFormat,
            QSettings.UserScope,
            QApplication.organizationName(),
            QApplication.applicationName()
        )

        log.debug('Loading MainWindow')
        self.ui = Ui_MainWindow_MailPrep()
        self.ui.setupUi(self)

        self.app_settings = app_settings

        # Attach actions to the menu that have to be done in code as the designer doesn't seem to
        # be able to set actions created from widget methods
        self.ui.menuView.addAction(self.ui.dockWidget_outputWindow.toggleViewAction())

        # Set default window state
        if not self.restore_geometry():
            self.setWindowState(Qt.WindowMaximized)
        if not self.restore_state():
            self.set_to_default_state()
        # self.ui.treeView_fileList.setModel(self.ctrl.file_system_model)

        self.new_job_dialog = NewJobDialog()

        # Create list to hold file input widgets
        self.file_input_widgets = []

        # Register signals
        # pylint: disable = no-member
        self.ui.actionNewJob.triggered.connect(self.on_new_job)
        self.ui.actionBrowseCustomCampus.triggered.connect(QFileDialog.getOpenFileName)
        self.ui.actionOpenJob.triggered.connect(self.job_open_file_picker)
        self.ui.actionAddFiles.triggered.connect(self.on_add_files)
        # pylint: enable = no-member

    def set_output_signal(self, output_signal):
        """Connects the given signal with a string argument to the output window text display"""
        output_signal.connect(self.append_text_to_output_windows)
        log.debug('Output window properly connected -- Visibility Test')

    @Slot()
    def append_text_to_output_windows(self, text):
        self.ui.plainTextEdit_output.moveCursor(QTextCursor.End)
        self.ui.plainTextEdit_output.insertPlainText(text)
        self.ui.plainTextEdit_output.moveCursor(QTextCursor.End)


    def set_to_default_state(self):
        """Sets default locations for widgets for when existing state is not restored"""
        self.ui.dockWidget_outputWindow.setVisible(False)
        self.splitDockWidget(
            self.ui.dockWidget__fileList,
            self.ui.dockWidget_jobProperties,
            Qt.Vertical
        )

    def set_job_properties_model(self, property_model):
        self.ui.treeView_jobProperties.set_model(property_model)

        # First time we initialize the property editor for a job we should expand all items
        self.ui.treeView_jobProperties.expandAll()
        self.ui.treeView_jobProperties.setColumnWidth(0, 200)

    def set_job_files_model(self, files_model):
        self.ui.treeView_fileList.set_model(files_model)

    @Slot()
    @log_call(log)
    def on_new_job(self):
        """Trigger on new job action to prompt for new job data"""
        self.new_job_dialog.show()

    @Slot()
    def job_open_file_picker(self):
        """Triggers on request to open a job to display a file picker"""
        dft_open_dir = self.app_settings.default_job_path
        (open_path, _) = QFileDialog.getOpenFileName(
            self, 'Open', dft_open_dir, 'MailPrep Job Definition (*.mpjob)')
        if open_path:
            self.open_job.emit(open_path)

    @Slot()
    def on_open_job(self):
        """View updates trigged when opening a job instance"""
        self.ui.actionClose.setEnabled(True)

    @Slot()
    @log_call(log)
    def on_add_files(self):  # pylint: disable = no-self-use
        """View updates trigged adding files to a job"""
        (add_paths, _) = QFileDialog.getOpenFileNames()
        log.debug('add_paths: %s', add_paths)
        # TODO: Add code to add files and remove pylint disable when finished  # pylint: disable = fixme

    def closeEvent(self, event):
        """Overload for event handler on main window closing (i.e. application closing)"""
        self.state_settings.setValue('ApplicationState/geometry', self.saveGeometry())
        self.state_settings.setValue('ApplicationState/windowState', self.saveState())
        super().closeEvent(event)

    def restore_geometry(self):
        """Restores saved geometry state if it was saved"""
        if self.state_settings.contains('ApplicationState/geometry'):
            self.restoreGeometry(self.state_settings.value("ApplicationState/geometry"))
            return True
        return False

    def restore_state(self):
        """Restores saved application state if it was saved"""
        if self.state_settings.contains('ApplicationState/windowState'):
            self.restoreState(self.state_settings.value("ApplicationState/windowState"))
            return True
        return False
