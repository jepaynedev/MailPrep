"""Controls logic for the main window"""
import logging
import os.path
import collections
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtWidgets import QFileSystemModel
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.model.qt_user_roles import QtUserRole
from utils.logging_decorators import log_call


log = logging.getLogger(__name__)


class FileInfo:

    def __init__(self):
        self.selected = False
        self.type = None
        self.list_id = None
        self._initialized = False

    def set_selected(self, selected):
        self.selected = selected
        if selected and not self._initialized:
            self._initialized = True
            self.type = 'Normal'
            self.list_id = 'UW#001'


class JobFileSystemModel(QFileSystemModel):
    """File system model to control File List view"""

    # Editable file types
    editable_file_extensions = [
        '.xlsx',
        '.xls'
    ]

    # Additional columns appened to the end of the list of columns
    additional_columns = [
        'Input',  # First so the model can move the appropriate column in front
        'Type',
        'List ID',
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.file_info = collections.defaultdict(FileInfo)

        self.current_root = None
        self.root_path_index = None

        self.dataChanged.connect(self.onDataChanged)

    def onDataChanged(self, topLeft, bottomRight, roles):
        log.debug(topLeft)
        log.debug(bottomRight)
        log.debug(roles)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            custom_offset = self._custom_column_index(section)
            if custom_offset is not None and role == Qt.DisplayRole:
                return self.additional_columns[custom_offset]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        custom_index = self._custom_column_index(index.column())
        if custom_index is not None:
            file_index = self._get_first_column_index(index)
            if file_index.isValid() and not self.isDir(file_index):
                file_name = self.fileName(file_index)
                if (custom_index == 0 or self.file_info[file_name].selected) and os.path.splitext(file_name)[1] in self.editable_file_extensions:
                    return Qt.ItemIsEnabled | Qt.ItemIsEditable
            return Qt.NoItemFlags
        return super().flags(index)

    def custom_column_count(self):
        return len(self.additional_columns)

    def hide_column_indexes(self):
        """Hide all default columns except for the Name (0) and added custom columns (end)"""
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
            if role == QtUserRole.EditTypeRole:
                if custom_offset == 0: return QtEditTypes.Bool
                if custom_offset == 1: return QtEditTypes.Combo
                if custom_offset == 2: return QtEditTypes.Str
            if role == Qt.EditRole and custom_offset == 0:
                return self.file_info[self._get_file_name(index)].selected
            if role == Qt.DisplayRole:
                file_index = self._get_first_column_index(index)
                if file_index.isValid() and not self.isDir(file_index):
                    file_name = self.fileName(file_index)
                    if self.file_info[file_name].selected and os.path.splitext(file_name)[1] in self.editable_file_extensions:
                        if custom_offset == 1:
                            return self.file_info[file_name].type
                        if custom_offset == 2:
                            return self.file_info[file_name].list_id
            return None
        return super().data(index, role)

    @log_call(log)
    def setData(self, index, value, role=Qt.EditRole):
        custom_offset = self._custom_column_index(index.column())
        if custom_offset == 0:
            self.file_info[self._get_file_name(index)].set_selected(value)
            self.dataChanged.emit(index, index, [role])
        return False

    def _get_file_name(self, index):
        file_index = self._get_first_column_index(index)
        if file_index.isValid() and not self.isDir(file_index):
            return self.fileName(file_index)
        return None

    def _get_first_column_index(self, index):
        """For any index, return the first column index (FileName) for the row"""
        return self.index(index.row(), 0, index.parent())

    def _custom_column_index(self, column_index):
        if column_index >= super().columnCount():
            return column_index - super().columnCount()
        return None

    def __repr__(self):
        return f'<JobFileSystemModel()>'
