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

    def test_new_job_show_signal_emitted(self):
        signal_check = SignalCheck()
        mainwindow_controller = MainWindowController()
        mainwindow_controller.new_job_signal.connect(signal_check.slot)

        mainwindow_controller.new_job()

        self.assertTrue(signal_check.signal_emitted)
