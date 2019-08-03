"""Defines format for YAML based MailPrep job definition file (.mpjob)"""
import unicodedata
import json
import yaml
import collections.abc

from mailprep.model.qt_edit_types import QtEditTypes

PROPERTIES_KEY = 'properties'


def recursive_merge(origin_dict, merge_dict, default=dict):
    """Deep merge two dict object, assigning merge dict back into origin"""
    for key, value in merge_dict.items():
        if isinstance(value, collections.abc.Mapping):
            origin_value = origin_dict.setdefault(key, default())  # Gets origin value for key or sets to empty dict
            if isinstance(origin_value, collections.abc.Mapping):
                recursive_merge(origin_value, value)
            else:
                origin_value = value
        else:
            origin_dict[key] = value


class InsensitiveDict(collections.abc.MutableMapping):
    """Mapping with normalized and case insensitive keys (stored as lower case)"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(*args, **kwargs)  # Set with update to apply transforms

    def __getitem__(self, key):
        return self.store[self.keytransform(key)]

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            print(f'__setitem__({key},{value})')
            self.store[self.keytransform(key)] = InsensitiveDict(value)
        else:
            self.store[self.keytransform(key)] = value

    def __delitem__(self, key):
        del self.store[self.keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def keytransform(self, key):
        """Normalized text key and converts to lower case if string, else pass through"""
        if isinstance(key, str):
            return ' '.join(unicodedata.normalize("NFKD", key.casefold()).strip().split())
        return key

    def __repr__(self):
        return repr(self.store)


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
        self.settings = InsensitiveDict()

    def get(self, key, *args, **kwargs):
        return self.settings.get(key, *args, **kwargs)

    def get_property(self, key, default):
        if PROPERTIES_KEY not in self.settings:
            return default
        return self.get(PROPERTIES_KEY).get(key, default)

    def set_property(self, key, value):
        """Returns boolean indicating if the value was modified"""
        # Creates properties if not existing and initially checks if key exists
        is_modified = key not in self.settings.setdefault(PROPERTIES_KEY, InsensitiveDict)
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
        recursive_merge(self.settings, InsensitiveDict(settings_object), default=InsensitiveDict)

    def save(self, fp):
        """Serializes and writes the settings content to the file object"""
        json.dump(self.settings, fp)

    def __repr__(self):
        return repr(self.settings)


# def normalize_caseless(text):
#     """Standard normalization rules for accepted serialization string comparison"""
#     return unicodedata.normalize("NFKD", text.casefold()).strip()


# class SupportedDataType:  # pylint: disable = too-few-public-methods
#     """Data class for mapping data types between python objects, enums, and serializations"""

#     def __init__(self, object_type, edit_type, accepted_serializations):
#         self.object_type = object_type
#         self.edit_type = edit_type
#         self.accepted_serializations = accepted_serializations
#         self._normal_accepted_serializations = [
#             normalize_caseless(x) for x in self.accepted_serializations
#         ]

#     def is_accepted_serialization(self, text):
#         """Normalizes a serialization in the same format as accepts options are and checks"""
#         return normalize_caseless(text) in self._normal_accepted_serializations


# class PropertyTag(yaml.YAMLObject):
#     """Custom YAML tag defining a property with name, value and data type"""

#     yaml_tag = "!Property"
#     yaml_loader = yaml.SafeLoader  # Marks this object to be used by safe_load

#     supported_data_types = [
#         SupportedDataType(bool, QtEditTypes.Bool, ['bool', 'boolean']),
#         SupportedDataType(str, QtEditTypes.Str, ['str']),
#     ]

#     def __init__(self, name, data_type, value=None):
#         self.name = name
#         self.data_type = data_type
#         self.value = value

#     @classmethod
#     def serialize_data_type(cls, data_type):
#         """Given an enum edit type QtEditTypes, returns first default string serialization"""
#         # Mapping defined multiple accepted serializations to parse
#         # When application serializes, use the first option as the default
#         return next(
#             filter(lambda x: x.edit_type == data_type, cls.supported_data_types)
#         ).accepted_serializations[0]

#     @classmethod
#     def get_data_type(cls, data_type):
#         """Given a serialized data type, return the first SupportedDataType instance it matches"""
#         return next(
#             filter(lambda x: x.is_accepted_serialization(data_type), cls.supported_data_types))

#     @classmethod
#     def from_yaml(cls, loader, node):
#         """Creates an instance of the class from serialized YAML"""
#         scalars = {
#             loader.construct_scalar(k): loader.construct_scalar(v)
#             for k, v in node.value
#         }
#         data_type = cls.get_data_type(scalars["data_type"])
#         value = data_type.object_type(scalars["value"])
#         return PropertyTag(
#             scalars["name"],
#             data_type.edit_type,
#             value)

#     @classmethod
#     def to_yaml(cls, dumper, data):
#         """Converts and instance of the class into serialized YAML"""
#         print(data)
#         return dumper.represent_mapping(cls.yaml_tag, {
#             'name': data.name,
#             'data_type': cls.serialize_data_type(data.data_type),
#             'value': data.value,
#         })

#     def __eq__(self, other):
#         return (self.name == other.name and
#                 self.data_type == other.data_type and
#                 self.value == other.value)

#     def __repr__(self):
#         return (f"<{self.__class__.__name__}"
#                 f"(name={self.name},data_type={self.data_type},value={self.value})>")


# # Custom tag added in global scope - required for safe_load() and safe_dump()
# yaml.SafeDumper.add_multi_representer(PropertyTag, PropertyTag.to_yaml)
