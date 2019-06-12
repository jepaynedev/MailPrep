"""Controls logic for the main window"""
import logging
from PySide2.QtCore import QObject, QSettings
from PySide2.QtWidgets import QFileSystemModel

log = logging.getLogger(__name__)


class JobFileSystemModel(QFileSystemModel):
    """File system model to control File List view"""

    def __init__(self):
        super(JobFileSystemModel, self).__init__()
        self.current_root = None
        self.root_path_index = None

    def set_current_root(self, path):
        """Sets the root path for the model"""
        log.debug('setting current_root: %s', path)
        self.current_root = path
        self.setRootPath(self.current_root)
        self.root_path_index = self.index(self.current_root)


class MainWindowController(QObject):
    """General controller for the main view"""

    def __init__(self):
        super(MainWindowController, self).__init__()
        self.file_system_model = JobFileSystemModel()
        self.settings = QSettings()
