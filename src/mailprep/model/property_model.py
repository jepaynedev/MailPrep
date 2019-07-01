"""QStandardItemModel implementation for use with PropertyView defining expected model settings"""
import logging
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from mailprep.model.qt_user_roles import QtUserRole


log = logging.getLogger(__name__)


class PropertyModel(QStandardItemModel):
    """QStandardItemModel implementation for use with PropertyView"""

    def __init__(self):
        super().__init__()
        self.setHorizontalHeaderLabels(['Property', 'Value'])
        self.groups = {}
        self.parent_item = self.invisibleRootItem()

    def add_property(self, group, property_key, edit_type, default_value=None):
        """Adds a property of a given type to a group (create if not exist) with optional value"""
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
        # Set editor type for delegate to select the appropriate editor
        value_item.setData(edit_type, QtUserRole.EditTypeRole)

        # Add property items to the group
        self.groups[group].appendRow([key_item, value_item])
