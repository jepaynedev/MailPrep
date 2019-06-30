import logging
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QStyledItemDelegate, QComboBox
from mailprep.controller.logging_decorators import log_call


log = logging.getLogger(__name__)


class PropertyEditorDelegate(QStyledItemDelegate):

    def __init__(self, model, parent=None):
        super(PropertyEditorDelegate, self).__init__(parent)
        self.parent = parent
        self.model = model

    def createEditor(self, parent, option, index):
        if self.itemlist is None:
            self.itemlist = self.model.getItemList(index)

        editor = QComboBox(parent)
        editor.addItems(self.itemlist)
        editor.setCurrentIndex(0)
        editor.installEventFilter(self)
        return editor


class PropertyModel(QStandardItemModel):

    def __init__(self):
        super(PropertyModel, self).__init__()
        self.setHorizontalHeaderLabels(['Property', 'Value'])
        self.groups = {}
        self.parent_item = self.invisibleRootItem()

    @log_call(log)
    def add_property(self, group, property_key, value_type, default_value = None):
        # Create group if doesn't yet exist
        if group not in self.groups:
            group_item = QStandardItem(group)
            group_item.setFlags(Qt.ItemIsEnabled)
            self.parent_item.appendRow(group_item)
            self.groups[group] = group_item

        # Create property row items
        key_item = QStandardItem(property_key)
        key_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        value_item = QStandardItem(default_value)

        # Add property items to the group
        self.groups[group].appendRow([key_item, value_item])
