import unittest

import io
import yaml

from mailprep.model.settings.job_settings import recursive_merge, InsensitiveDict, JobSettings #, PropertyTag
from mailprep.model.qt_edit_types import QtEditTypes


class TestRecusiveMerge(unittest.TestCase):

    def test_recursive_merge_deep_merge(self):
        origin_dict = { "a": { "b": 2 } }
        merge_dict = { "a": { "c": 3 } }
        recursive_merge(origin_dict, merge_dict)
        assert origin_dict["a"] == { "b": 2, "c": 3 }
        assert len(origin_dict) == 1  # Make sure no other keys added

    def test_recursive_merge_overwrite_if_not_dict(self):
        origin_dict = { "a": { "b": 2 } }
        merge_dict = { "a": 'c' }
        recursive_merge(origin_dict, merge_dict)
        assert origin_dict["a"] == 'c'
        assert len(origin_dict) == 1  # Make sure no other keys added

    def test_recursive_merge_deep_merge_seperate_roots(self):
        origin_dict = { "a": { "b": 2 } }
        merge_dict = { "b": { "c": 3 } }
        recursive_merge(origin_dict, merge_dict)
        assert origin_dict["a"] == { "b": 2 }
        assert origin_dict["b"] == { "c": 3 }
        assert len(origin_dict) == 2  # Make sure no other keys added


class TestInsensitiveDict(unittest.TestCase):

    def test_insensitive_dict_basic_create(self):
        test_dict = InsensitiveDict({ "a": 1 })
        assert test_dict["a"] == 1

    def test_insensitive_dict_basic_insensitve_use(self):
        test_dict = InsensitiveDict({ "a": 1, "B": 2 })
        assert test_dict["A"] == 1
        assert test_dict["b"] == 2

    def test_insensitive_dict_basic_stripped_use(self):
        test_dict = InsensitiveDict()
        test_dict[" a "] = 1
        assert test_dict["A"] == 1

    def test_insensitive_dict_basic_insensitive_override(self):
        test_dict = InsensitiveDict()
        test_dict["a"] = 1
        test_dict["A"] = 2
        assert test_dict["a"] == 2

    def test_insensitive_dict_basic_interior_whitespace(self):
        test_dict = InsensitiveDict()
        test_dict["a  b"] = 1
        assert test_dict["a b"] == 1

    def test_insensitive_dict_basic_deep(self):
        test_dict = InsensitiveDict({ "a": { "b": 1 } })
        assert test_dict["A"]["B"] == 1

    def test_insensitive_dict_get_with_default(self):
        test_dict = InsensitiveDict({ "a": 1 })
        assert test_dict.get("b", 2) == 2


class TestJobSettings(unittest.TestCase):

    def test_job_setting_from_file(self):
        source_file = io.StringIO('{"properties":{"name": "value"}}')
        job_settings = JobSettings.from_file(source_file)
        actual_value = job_settings.get('properties').get('name')
        assert actual_value == 'value'

    def test_job_settings_merge(self):
        job_settings = JobSettings().initialize({"properties":{"name": "value"}})
        job_settings.merge({"properties":{"name2": "value2"}})
        assert job_settings.get('properties').get('name') == 'value'
        assert job_settings.get('properties').get('name2') == 'value2'


# class TestPropertyTag(unittest.TestCase):

#     def setUp(self):
#         self.property_str = PropertyTag("Name", QtEditTypes.Str, "NameValue")
#         self.yaml_str = ("key: !Property\n"
#                          "  data_type: str\n"
#                          "  name: Name\n"
#                          "  value: NameValue\n")

#         self.property_bool = PropertyTag("Use This", QtEditTypes.Bool, True)
#         self.yaml_bool = ("key: !Property\n"
#                           "  data_type: bool\n"
#                           "  name: Use This\n"
#                           "  value: true\n")

#     def test_safe_dump_str(self):
#         to_dump = { "key": self.property_str }
#         dumped = yaml.safe_dump(to_dump)
#         assert dumped == self.yaml_str

#     def test_safe_load_str(self):
#         expected_loaded = { "key": self.property_str }
#         loaded = yaml.safe_load(self.yaml_str)
#         assert loaded == expected_loaded

#     def test_safe_dump_bool(self):
#         to_dump = { "key": self.property_bool }
#         dumped = yaml.safe_dump(to_dump)
#         assert dumped == self.yaml_bool

#     def test_safe_load_bool(self):
#         expected_loaded = { "key": self.property_bool }
#         loaded = yaml.safe_load(self.yaml_bool)
#         assert loaded == expected_loaded

#     def test_safe_load_boolean(self):
#         expected_loaded = { "key": self.property_bool }
#         # Note different using "boolean" data type instead of default "bool"
#         loaded = yaml.safe_load(("key: !Property\n"
#                                  "  data_type: boolean\n"
#                                  "  name: Use This\n"
#                                  "  value: true\n"))
#         assert loaded == expected_loaded

#     def test_safe_load_boo_case_insensitive(self):
#         expected_loaded = { "key": self.property_bool }
#         # Note different using "boolean" data type instead of default "bool"
#         loaded = yaml.safe_load(("key: !Property\n"
#                                  "  data_type: bOoL\n"
#                                  "  name: Use This\n"
#                                  "  value: true\n"))
#         assert loaded == expected_loaded
