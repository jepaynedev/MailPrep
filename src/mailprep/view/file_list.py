import logging
from PySide2.QtWidgets import QTreeView, QStyledItemDelegate, QComboBox
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.model.qt_user_roles import QtUserRole
from utils.logging_decorators import log_call


log = logging.getLogger(__name__)


class FileListDelegate(QStyledItemDelegate):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        """Overrides base createEditor method to specify editor from QtUserRole.EditTypeRole"""
        edit_type = self.parent.model().data(index, QtUserRole.EditTypeRole)
        if edit_type == QtEditTypes.Combo:
            combo_model = self.parent.model().data(index, QtUserRole.EditComboModelRole)
            combo = QComboBox(parent)
            combo.setModel(combo_model)
            return combo
        return super().createEditor(parent, option, index)


class FileList(QTreeView):
    """QTreeView subclass with style and editor modifications for generalized and grouped editors"""

    def __init__(self, parent):
        super().__init__(parent)
        file_list_delegate = FileListDelegate(self)
        self.setItemDelegate(file_list_delegate)

    def set_model(self, model):
        """Sets a model for the view and calls custom view modifications dependent on the model"""
        self.setModel(model)
        self.initialize_with_model()

    @log_call(log)
    def initialize_with_model(self):
        """Initialize custom view modifications dependent of the model"""
        log.debug(self.model().hide_column_indexes())
        self.setRootIndex(self.model().root_path_index)
        for i in self.model().hide_column_indexes():
            self.hideColumn(i)

        # First time we initialize the view, set default column width
        self.setColumnWidth(0, 175)

        # Set editable
        # for i in self.model().edit_column_indexes():
        #     self.setItemDelegateForColumn(i, self.file_list_delegate)
            # index = self.model().index(i, 0)
            # self.openPersistentEditor.index(index)
