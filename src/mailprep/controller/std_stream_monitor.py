"""Standardized utilities for redirecting stdout and stderr to a queue"""
import logging
import queue
from PySide2.QtCore import Signal, Slot, QObject, QThread

log = logging.getLogger(__name__)


class QueueStream:
    """Stream-like object that wraps a Queue with write and flush"""

    def __init__(self, std_queue, source_flush):
        self.std_queue = std_queue
        self.source_flush = source_flush

    def write(self, value):
        """Puts the given text written to the stream-like object to the underlying queue"""
        self.std_queue.put(value.strip())

    def flush(self):
        """Flushes the stream-like object which should push to write"""
        self.source_flush()


class QueueMonitorWorker(QObject):
    """Worker object for a background thread to emit Queue messages as Signals"""

    std_stream_signal = Signal(str)
    finished = Signal()

    def __init__(self, std_queue):
        super().__init__()
        self.std_queue = std_queue

    @Slot()
    def run(self):
        """Emit queue contents as signals indefinitely, periodically checking for termination"""
        while not QThread.currentThread().isInterruptionRequested():
            try:
                value = self.std_queue.get(timeout=0.5)
                self.std_stream_signal.emit(value)  # pylint: disable = no-member
            except queue.Empty:
                pass
        self.finished.emit()  # pylint: disable = no-member
