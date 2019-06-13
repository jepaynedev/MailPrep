from PySide2.QtWidgets import QTreeView
from PySide2.QtGui import QBrush, QColor


class PropertyEditor(QTreeView):

    def __init__(self, parent):
        super(PropertyEditor, self).__init__(parent)

    def initialize(self):
        self.expandAll()
        parent_index = self.model().indexFromItem(self.model().invisibleRootItem())
        for i in range(0, len(self.model().groups)):
            self.model().item(i, 0).setBackground(QBrush(QColor('#3d3d3d')))
            self.model().item(i, 0).setForeground(QBrush(QColor('#ffffff')))
            self.setFirstColumnSpanned(i, parent_index, True)
