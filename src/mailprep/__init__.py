"""User inputs data for a bulk mail job and processing is automated"""

import sys
import logging
from PySide2.QtWidgets import QApplication
from mailprep.view.mainwindow import MainWindow
from mailprep.controller.mainwindow_controller import MainWindowController
from mailprep.controller.settings_manager import SettingsManager

def setup_logger(level):
    """Define logger at root of main module so all submodules inherit"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Define lowest handled (not output)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def main():
    """Entry point for running the interface from the command line"""
    setup_logger(logging.DEBUG)
    SettingsManager.set_application_values(
        application="MailPrep",
        organization="UW-Madison Postal Mail",
        domain="postalmail.wisc.edu"
    )

    # Init and show interface
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    main_controller = MainWindowController()
    main_window = MainWindow(main_controller)
    main_window.show()

    sys.exit(app.exec_())
