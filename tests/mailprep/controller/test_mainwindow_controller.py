import unittest

from mailprep.controller.mainwindow_controller import MainWindowController, JobFileSystemModel


# QSignalSpy does not appear to yet be ported to PySide2,
# therefore this is being used as a naive check a signal was emitted
class SignalCheck:

    def __init__(self):
        self.signal_emitted = False

    def slot(self):
        self.signal_emitted = True


class TestMainWindowController(unittest.TestCase):
    pass


class TestJobFileSystemModel(unittest.TestCase):

    def test_hide_column_indexes(self):
        file_system_model = JobFileSystemModel()
        actual = file_system_model.hide_column_indexes()
        assert [1, 2, 3] == actual

    def test_edit_column_indexes(self):
        file_system_model = JobFileSystemModel()
        actual = file_system_model.edit_column_indexes()
        assert [4, 5] == actual

    def test_columnCount(self):
        file_system_model = JobFileSystemModel()
        actual = file_system_model.columnCount()
        assert 6 == actual
