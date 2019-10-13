"""Defines format for YAML based MailPrep job definition file (.mpjob)"""
import json

from mailprep.model.qt_edit_types import QtEditTypes
from utils.mapping import CaseInsensitiveDict, recursive_merge

PROPERTIES_KEY = 'properties'


class JobSettings:
    """Wrap job settings into an abstraction managing read and write access"""

    @classmethod
    def from_file(cls, fp):
        """Creates a new job settings instance seeded from a source file contents"""
        source_settings = None
        try:
            source_settings = json.load(fp)
        except json.JSONDecodeError:
            # Handles case where the source job file is not valid json,
            # and therefore not a valid job definition file
            pass
        return cls().initialize(source_settings)

    def __init__(self):
        self.settings = CaseInsensitiveDict()

    def get(self, key, *args, **kwargs):
        return self.settings.get(key, *args, **kwargs)

    def get_property(self, key, default):
        if PROPERTIES_KEY not in self.settings:
            return default
        return self.get(PROPERTIES_KEY).get(key, default)

    def set_property(self, key, value):
        """Returns boolean indicating if the value was modified"""
        # Creates properties if not existing and initially checks if key exists
        is_modified = key not in self.settings.setdefault(PROPERTIES_KEY, CaseInsensitiveDict)
        # If key does exist then we are updating existing values and need to check if modifying
        if not is_modified:
            is_modified = self.settings[PROPERTIES_KEY][key] != value
        if is_modified:
            self.settings[PROPERTIES_KEY][key] = value
        return is_modified

    def initialize(self, initial_settings):
        """Initializes job setting from values. Intended to be called after base init"""
        if initial_settings is not None:
            self.merge(initial_settings)
        return self

    def merge(self, settings_object):
        """Merges settings from the given object into existing job settings"""
        recursive_merge(self.settings, CaseInsensitiveDict(settings_object), default=CaseInsensitiveDict)

    def save(self, fp):
        """Serializes and writes the settings content to the file object"""
        json.dump(self.settings, fp)

    def __repr__(self):
        return repr(self.settings)
