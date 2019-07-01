"""Manages Qt.UserRole assignments in an Enum to share across application in a single definition"""
from enum import IntEnum
from PySide2.QtCore import Qt


class QtUserRole(IntEnum):
    """Custom UserRole enumeration to share definitions over entire application"""
    EditTypeRole = Qt.UserRole + 1
