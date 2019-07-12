"""Controls logic for the main window"""
import logging
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QFileSystemModel
from mailprep.controller.std_stream_monitor import QueueMonitorWorker
from mailprep.controller.thread_wrapper import start_thread


log = logging.getLogger(__name__)


class JobFileSystemModel(QFileSystemModel):
    """File system model to control File List view"""

    def __init__(self):
        super().__init__()
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

    destroy = Signal()

    def __init__(self, main_view, std_stream_queue):
        super().__init__()
        self.main_view = main_view
        self.std_stream_queue = std_stream_queue

        # Set up thread to watch std stream queue and pop contents and emit with a signal
        self.queue_monitor_worker = QueueMonitorWorker(self.std_stream_queue)
        self.thread = start_thread(self.queue_monitor_worker)

        # Initialize main view
        self.main_view.initialize()
        self.main_view.set_output_signal(self.queue_monitor_worker.std_stream_signal)

        # Initialize any models
        self.file_system_model = JobFileSystemModel()

        # Connect signals
        self.destroy.connect(self.clean_up)  # pylint: disable = no-member

    @Slot()
    def clean_up(self):
        """Cleans up background worker threads gracefully and deletes self"""
        self.thread.requestInterruption()
        self.thread.wait(1000)
        self.deleteLater()
