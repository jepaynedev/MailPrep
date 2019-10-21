"""User inputs data for a bulk mail job and processing is automated"""
import sys
import logging
import queue
from PySide2.QtWidgets import QApplication
from mailprepgui.view.mainwindow import MainWindow
from mailprepgui.controller.mainwindow_controller import MainWindowController
from mailprepgui.controller.settings_manager import SettingsManager
from mailprepgui.controller.std_stream_monitor import QueueStream


# pylint: disable = fixme
# TODO: Remove no-member lint suppressions when fixed for PySide2 Signal connect and emit methods
# TODO: See https://github.com/PyCQA/pylint/issues/2585
# pylint: enable = fixme


def setup_std_stream_queue(std_stream_queue):
    """Given a queue, redirect stdout and stderr to write to the queue"""
    stdout_original = sys.stdout
    stderr_original = sys.stderr
    sys.stdout = QueueStream(std_stream_queue, stdout_original.flush)
    sys.stderr = QueueStream(std_stream_queue, stderr_original.flush)


def setup_logger(level):
    """Define logger at root of main module so all submodules inherit"""
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)  # Define lowest handled (not output)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    stdout_handler.setFormatter(formatter)

    log.addHandler(stdout_handler)


def main():
    """Entry point for running the interface from the command line"""
    # First setup redirect from stdout and stderr to a queue for multi-threading purposes
    std_stream_queue = queue.Queue()
    setup_std_stream_queue(std_stream_queue)

    # Set up default global logger
    setup_logger(logging.DEBUG)

    # Set up Qt settings manager for global application settings
    SettingsManager.set_application_values(
        application="MailPrep",
        organization="UW-Madison Postal Mail",
        domain="postalmail.wisc.edu"
    )

    # Init and show interface
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    main_window = MainWindow()
    main_controller = MainWindowController(main_window, std_stream_queue)
    main_window.show()
    app.aboutToQuit.connect(main_controller.destroy.emit)  # pylint: disable = no-member

    sys.exit(app.exec_())
