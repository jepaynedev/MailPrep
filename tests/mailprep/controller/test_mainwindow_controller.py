import unittest

from mailprep.controller.mainwindow_controller import MainWindowController


# QSignalSpy does not appear to yet be ported to PySide2,
# therefore this is being used as a naive check a signal was emitted
class SignalCheck:

    def __init__(self):
        self.signal_emitted = False

    def slot(self):
        self.signal_emitted = True


class TestMainWindowController(unittest.TestCase):
    pass
