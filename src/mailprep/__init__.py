import sys
import logging
from PySide2.QtWidgets import QApplication
from mailprep.view.mainwindow import MainWindow

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
    setup_logger(logging.DEBUG)

    # Init and show interface
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
