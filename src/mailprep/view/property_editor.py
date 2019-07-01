"""Custom implementation of QTreeView for generalized and grouped property editing"""
import logging
from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QTreeView, QCheckBox, QStyledItemDelegate
from mailprep.model.qt_edit_types import QtEditTypes
from mailprep.model.qt_user_roles import QtUserRole


EDIT_COLUMN_INDEX = 1


log = logging.getLogger(__name__)


class PropertyEditorDelegate(QStyledItemDelegate):
    """Delegate managing different editor widgets based on items QtUserRole.EditTypeRole value"""

    def __init__(self, parent):
        super(PropertyEditorDelegate, self).__init__(parent)
        self.parent = parent

    def paint(self, painter, option, index):
        """Overrides base paint method to hide display if boolean value"""
        item = self.parent.model().itemFromIndex(index)
        edit_type = item.data(QtUserRole.EditTypeRole)
        # Don't paint display for boolean values as "True" or "False" strings
        # are visible under the persistent editor checkboxes being used
        if edit_type == QtEditTypes.Bool:
            return
        super(PropertyEditorDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        """Overrides base createEditor method to specify editor from QtUserRole.EditTypeRole"""
        item = self.parent.model().itemFromIndex(index)
        edit_type = item.data(QtUserRole.EditTypeRole)
        if edit_type == QtEditTypes.Bool:
            return QCheckBox(parent)
        return super(PropertyEditorDelegate, self).createEditor(parent, option, index)


class PropertyEditor(QTreeView):
    """QTreeView subclass with style and editor modifications for generalized and grouped editors"""

    def __init__(self, parent):
        super(PropertyEditor, self).__init__(parent)
        property_editor_delegate = PropertyEditorDelegate(self)
        self.setItemDelegateForColumn(EDIT_COLUMN_INDEX, property_editor_delegate)
        self.setEditTriggers(QTreeView.AllEditTriggers)

    def set_model(self, model):
        """Sets a model for the view and calls custom view modifications dependent on the model"""
        self.setModel(model)
        self.initialize_with_model()

    def initialize_with_model(self):
        """Initialize custom view modifications dependent of the model"""
        root_index = self.model().indexFromItem(self.model().invisibleRootItem())
        for i in range(0, len(self.model().groups)):
            self.model().item(i).setBackground(QBrush(QColor('#3d3d3d')))
            self.model().item(i).setForeground(QBrush(QColor('#ffffff')))
            self.setFirstColumnSpanned(i, root_index, True)

            parent_index = self.model().index(i, 0)
            parent = self.model().item(i)
            for child_row, child in enumerate(children(parent, EDIT_COLUMN_INDEX)):
                child_index = self.model().index(child_row, EDIT_COLUMN_INDEX, parent_index)
                if child.data(QtUserRole.EditTypeRole) == QtEditTypes.Bool:
                    self.openPersistentEditor(child_index)


def children(item, column=0):
    """Iterates over all child QStandardItems of given QStandardItem with given column"""
    if item.hasChildren():
        child_row = 0
        while True:
            child = item.child(child_row, column)
            if child is None:
                return
            yield child
            child_row += 1
