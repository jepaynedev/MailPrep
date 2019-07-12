"""Main window view with view-specific logic"""
import logging
from PySide2.QtCore import Qt, Slot, QSettings
from PySide2.QtWidgets import QMainWindow, QFileDialog, QApplication
from mailprep.ui.mainwindow_ui import Ui_MainWindow_MailPrep  # pylint: disable=no-name-in-module,import-error
from mailprep.view.new_job_dialog import NewJobDialog
from mailprep.model.property_model import PropertyModel
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.controller.logging_decorators import log_call


log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window view for the application"""

    def __init__(self):
        super().__init__()
        self.file_input_widgets = None
        self.new_job_dialog = None
        self.state_settings = None
        self.ui = None

    def initialize(self):
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
        self.ui.actionOpenJob.triggered.connect(self.on_open_job)
        self.ui.actionAddFiles.triggered.connect(self.on_add_files)
        # pylint: enable = no-member

        job_properties = PropertyModel()
        job_properties.add_property('Customer Information', 'Customer', QtEditTypes.Str)
        job_properties.add_property('Customer Information', 'Department', QtEditTypes.Str)
        job_properties.add_property('Merge Settings', 'Use Custom Campus', QtEditTypes.Bool)
        job_properties.add_property('Merge Settings', 'Custom Campus Path', QtEditTypes.Str)
        self.ui.treeView_jobProperties.set_model(job_properties)
        # First time we initialize the property editor we should expand all items
        self.ui.treeView_jobProperties.expandAll()
        self.ui.treeView_jobProperties.setColumnWidth(0, 200)

    def set_output_signal(self, output_signal):
        """Connects the given signal with a string argument to the output window text display"""
        output_signal.connect(self.ui.plainTextEdit_output.appendPlainText)
        log.debug('Output window properly connected -- Visibility Test')

    def set_to_default_state(self):
        """Sets default locations for widgets for when existing state is not restored"""
        self.ui.dockWidget_outputWindow.setVisible(False)
        self.splitDockWidget(
            self.ui.dockWidget__fileList,
            self.ui.dockWidget_jobProperties,
            Qt.Vertical
        )

    # @Slot()
    # def set_file_list_view(self, path):
    #     """Sets a given path for the file list tree view"""
    #     self.ctrl.file_system_model.set_current_root(path)
    #     self.ui.treeView_fileList.setRootIndex(self.ctrl.file_system_model.root_path_index)
    #     for i in range(1, self.ctrl.file_system_model.columnCount()):
    #         self.ui.treeView_fileList.hideColumn(i)

    @Slot()
    @log_call(log)
    def on_new_job(self):
        """Trigger on new job action to prompt for new job data"""
        self.new_job_dialog.show()

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
