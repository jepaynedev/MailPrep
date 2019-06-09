from PySide2.QtCore import QObject, Signal


class MainWindowController(QObject):

    new_job_signal = Signal()

    def new_job(self):

        self.new_job_signal.emit()
