"""Controls logic for the main window"""
import logging
import os
from PySide2.QtCore import Qt, QObject, Signal, Slot, QModelIndex
from PySide2.QtWidgets import QFileSystemModel
from mailprep.controller.std_stream_monitor import QueueMonitorWorker
from mailprep.controller.thread_wrapper import start_thread
from mailprep.controller.settings_manager import SettingsManager
from mailprep.model.job.job_controller import JobManager
from mailprep.model.property_model import PropertyModel
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.model.settings.job_settings import JobSettings
from utils.logging_decorators import log_call


log = logging.getLogger(__name__)


class JobFileSystemModel(QFileSystemModel):
    """File system model to control File List view"""

    # Note offsets area applied from the end of the list of columns
    additional_columns = [
        'Type',
        'List ID',
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_root = None
        self.root_path_index = None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # If one of the custom column indexes, handle separately
        if orientation == Qt.Horizontal:
            custom_offset = self._custom_column_index(section)
            if custom_offset is not None and role == Qt.DisplayRole:
                return self.additional_columns[custom_offset]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if self._custom_column_index(index.column()) is not None:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        return super().flags(index)

    def custom_column_count(self):
        return len(self.additional_columns)

    def hide_column_indexes(self):
        # Don't include 0 or the custom columns by their offsets
        return list(range(1, super().columnCount()))

    def edit_column_indexes(self):
        # Only the custom columns can be edited
        return list(range(super().columnCount(), self.columnCount()))

    def set_current_root(self, path):
        """Sets the root path for the model"""
        log.debug('setting current_root: %s', path)
        self.current_root = path
        self.setRootPath(self.current_root)
        self.root_path_index = self.index(self.current_root)

    def columnCount(self, parent=None):
        parent = parent if parent is not None else QModelIndex()
        return super().columnCount(parent) + self.custom_column_count()

    def data(self, index, role):
        # If one of the custom column indexes, handle separately
        custom_offset = self._custom_column_index(index.column())
        if custom_offset is not None:
            if role == Qt.DisplayRole:
                return self.additional_columns[custom_offset]
        return super().data(index, role)

    def _custom_column_index(self, column_index):
        if column_index >= super().columnCount():
            return column_index - super().columnCount()
        return None

    def __repr__(self):
        return f'<JobFileSystemModel()>'


class JobController:

    def __init__(self, job_file_path, settings):
        self.job_file_path = job_file_path
        self.settings = settings



class MainWindowController(QObject):
    """General controller for the main view"""

    destroy = Signal()
    set_job_properties = Signal(object)

    def __init__(self, main_view, std_stream_queue):
        super().__init__()
        self.main_view = main_view
        self.std_stream_queue = std_stream_queue
        self.app_settings = SettingsManager()

        # Set up thread to watch std stream queue and pop contents and emit with a signal
        self.queue_monitor_worker = QueueMonitorWorker(self.std_stream_queue)
        self.thread = start_thread(self.queue_monitor_worker)

        # Initialize main view
        self.main_view.initialize(self.app_settings)
        self.main_view.set_output_signal(self.queue_monitor_worker.std_stream_signal)

        # Initialize any models
        self.files_model = JobFileSystemModel()
        log.debug(self.files_model)

        # Connect signals
        self.main_view.open_job.connect(self.open_job)
        self.destroy.connect(self.clean_up)  # pylint: disable = no-member

        # Initialize any class variables
        self.job = None
        self.job_properties = self.create_job_property_model()

    def create_job_property_model(self):
        property_model = PropertyModel()
        property_model.add_property('Customer Information', 'Customer', QtEditTypes.Str)
        property_model.add_property('Customer Information', 'Department', QtEditTypes.Str)
        property_model.add_property('Merge Settings', 'Use Custom Campus', QtEditTypes.Bool)
        property_model.add_property('Merge Settings', 'Custom Campus Path', QtEditTypes.Str)
        return property_model

    @Slot()
    def clean_up(self):
        """Cleans up background worker threads gracefully and deletes self"""
        self.thread.requestInterruption()
        self.thread.wait(1000)
        self.deleteLater()

    @Slot()
    @log_call(log)
    def open_job(self, job_file_path):
        try:
            # Create a job settings instance from the job file path
            with open(job_file_path, 'r') as job_file:
                job_settings = JobSettings.from_file(job_file)
        except FileNotFoundError:
            log.exception("Job definition file %s could not be found", job_file)
            return

        self.job = JobManager(job_file_path, job_settings)
        self.set_window_title_job(False)
        self.job.job_is_changed.connect(self.set_window_title_job)
        log.debug('Opened job: %s', self.job)

        # Show job properties and set to values from the job settings
        self.main_view.set_job_properties_model(self.job.property_model)

        # Set job file directory based on job file directory location
        # (Job file is always assumed to be at the root directory of a job folder)
        self.files_model.set_current_root(self.job.directory)
        self.main_view.set_job_files_model(self.files_model)

    @Slot()
    def set_window_title_job(self, job_is_changed):
        open_file_name = self.job.file_base_name
        is_changed_indicator = "*" if job_is_changed else ""
        self.main_view.setWindowTitle(f"{open_file_name}{is_changed_indicator} - MailPrep")
