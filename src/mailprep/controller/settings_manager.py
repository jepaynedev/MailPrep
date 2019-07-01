"""A system to expose common values that should be settable by the user as application settings"""
import os

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QSettings


class SettingsManager:
    """Common overidable application settings managed with a QSettings instance"""

    @staticmethod
    def set_application_values(application, organization, domain=None):
        """Set application level values to the QApplication and QSettings static managers"""
        QApplication.setApplicationName(application)
        QApplication.setOrganizationName(organization)
        QSettings.setDefaultFormat(QSettings.IniFormat)
        if domain is not None:
            QApplication.setOrganizationDomain(domain)

    def __init__(self):
        self.settings = QSettings()

    @property
    def default_job_path(self):
        """'MailPrep' directory under the users Documents directory on Windows"""
        return self.settings.value(
            'paths/defaultJobPath',
            os.path.normpath(os.path.expanduser('~/Documents/MailPrep'))
        )

    @default_job_path.setter
    def default_job_path(self, value):
        self.settings.setValue('paths/defaultJobPath', value)
