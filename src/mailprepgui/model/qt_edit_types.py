"""Enumeration for property key value pairs types for managing editors"""
from enum import IntEnum


class QtEditTypes(IntEnum):
    """Enumeration managing editors types for QStandardItems using QtUserRole.EditTypeRole"""
    Str = 1
    Bool = 2
    Combo = 3
