"""Shared utilities for standardizing starting up a QThread with a worker process"""
from PySide2.QtCore import QThread, Qt


def start_thread(worker):
    """Given a ThreadWorkerBase implementation, start it in a thread after an hook up all signals"""
    thread = QThread()
    worker.moveToThread(thread)

    # Wire up signals and slots in a standardized fashion
    thread.started.connect(worker.run)  # pylint: disable = no-member
    # To the best that I can figure, here's what Qt.DirectConnection does for us:
    # If we have to wait for a thread (if it's in a polling, blocking loop) before it
    # emits a finished signal, a cleanup issue arises from unexpected exits to the application.
    # When cleaning up threads with QApplication aboutToQuit handlers, the main thread even loop
    # has already resolved. Therefore, while we can process slots in the separate thread,
    # no more slots are resolved in the main thread. If the finished signal is not emitted until
    # this main application loop is exited, the thread can still be cleaned up and will emit
    # the finished signal, but this connection that called the thread quit() method will no longer
    # be handled. However, it seem this is only for QueuedConnections, which seems to make sense
    # as the signal would be put on a queue the main event handler is no longer processing.
    # Therefore, as some example I found illustrated, a DirectConnection seems to bypass this
    # queue and the slot will still be executed despite having left the main thread event loop.
    # I simply don't know enough to know if there are downsides to using DirectConnection, but this
    # seems to make sense and fixed my thread cleanup issues.
    worker.finished.connect(thread.quit, Qt.DirectConnection)
    # From some reading I found at some point, it seems that in newer versions of Qt (4.8+?), there
    # is special interaction with the deleteLater slot that renders the DirectConnection
    # unnecessary, although I can't quite figure out how. Perhaps deleteLater isn't actually being
    # called properly, but no error messages are being shown, so for now I'm going to leave this
    # with the default QueuedConnection
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)  # pylint: disable = no-member

    # Start the spawned thread
    thread.start()

    # Return created thread. A reference needs to be saved by the main thread or the spawned thread
    # will be cleaned up and prematurely exit
    return thread
