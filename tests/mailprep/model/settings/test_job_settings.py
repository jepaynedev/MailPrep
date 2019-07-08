import unittest

import yaml

from mailprep.model.settings.job_settings import PropertyTag
from mailprep.model.qt_edit_types import QtEditTypes


class TestPropertyTag(unittest.TestCase):

    def setUp(self):
        self.property_str = PropertyTag("Name", QtEditTypes.Str, "NameValue")
        self.yaml_str = ("key: !Property\n"
                         "  data_type: str\n"
                         "  name: Name\n"
                         "  value: NameValue\n")

        self.property_bool = PropertyTag("Use This", QtEditTypes.Bool, True)
        self.yaml_bool = ("key: !Property\n"
                          "  data_type: bool\n"
                          "  name: Use This\n"
                          "  value: true\n")

    def test_safe_dump_str(self):
        to_dump = { "key": self.property_str }
        dumped = yaml.safe_dump(to_dump)
        assert dumped == self.yaml_str

    def test_safe_load_str(self):
        expected_loaded = { "key": self.property_str }
        loaded = yaml.safe_load(self.yaml_str)
        assert loaded == expected_loaded

    def test_safe_dump_bool(self):
        to_dump = { "key": self.property_bool }
        dumped = yaml.safe_dump(to_dump)
        assert dumped == self.yaml_bool

    def test_safe_load_bool(self):
        expected_loaded = { "key": self.property_bool }
        loaded = yaml.safe_load(self.yaml_bool)
        assert loaded == expected_loaded

    def test_safe_load_boolean(self):
        expected_loaded = { "key": self.property_bool }
        # Note different using "boolean" data type instead of default "bool"
        loaded = yaml.safe_load(("key: !Property\n"
                                 "  data_type: boolean\n"
                                 "  name: Use This\n"
                                 "  value: true\n"))
        assert loaded == expected_loaded

    def test_safe_load_boo_case_insensitive(self):
        expected_loaded = { "key": self.property_bool }
        # Note different using "boolean" data type instead of default "bool"
        loaded = yaml.safe_load(("key: !Property\n"
                                 "  data_type: bOoL\n"
                                 "  name: Use This\n"
                                 "  value: true\n"))
        assert loaded == expected_loaded
