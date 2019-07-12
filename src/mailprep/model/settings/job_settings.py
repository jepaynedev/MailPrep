"""Defines format for YAML based MailPrep job definition file (.mpjob)"""
import unicodedata
import yaml

from mailprep.model.qt_edit_types import QtEditTypes


def normalize_caseless(text):
    """Standard normalization rules for accepted serialization string comparison"""
    return unicodedata.normalize("NFKD", text.casefold()).strip()


class SupportedDataType:  # pylint: disable = too-few-public-methods
    """Data class for mapping data types between python objects, enums, and serializations"""

    def __init__(self, object_type, edit_type, accepted_serializations):
        self.object_type = object_type
        self.edit_type = edit_type
        self.accepted_serializations = accepted_serializations
        self._normal_accepted_serializations = [
            normalize_caseless(x) for x in self.accepted_serializations
        ]

    def is_accepted_serialization(self, text):
        """Normalizes a serialization in the same format as accepts options are and checks"""
        return normalize_caseless(text) in self._normal_accepted_serializations


class PropertyTag(yaml.YAMLObject):
    """Custom YAML tag defining a property with name, value and data type"""

    yaml_tag = "!Property"
    yaml_loader = yaml.SafeLoader  # Marks this object to be used by safe_load

    supported_data_types = [
        SupportedDataType(bool, QtEditTypes.Bool, ['bool', 'boolean']),
        SupportedDataType(str, QtEditTypes.Str, ['str']),
    ]

    def __init__(self, name, data_type, value=None):
        self.name = name
        self.data_type = data_type
        self.value = value

    @classmethod
    def serialize_data_type(cls, data_type):
        """Given an enum edit type QtEditTypes, returns first default string serialization"""
        # Mapping defined multiple accepted serializations to parse
        # When application serializes, use the first option as the default
        return next(
            filter(lambda x: x.edit_type == data_type, cls.supported_data_types)
        ).accepted_serializations[0]

    @classmethod
    def get_data_type(cls, data_type):
        """Given a serialized data type, return the first SupportedDataType instance it matches"""
        return next(
            filter(lambda x: x.is_accepted_serialization(data_type), cls.supported_data_types))

    @classmethod
    def from_yaml(cls, loader, node):
        """Creates an instance of the class from serialized YAML"""
        scalars = {
            loader.construct_scalar(k): loader.construct_scalar(v)
            for k, v in node.value
        }
        data_type = cls.get_data_type(scalars["data_type"])
        value = data_type.object_type(scalars["value"])
        return PropertyTag(
            scalars["name"],
            data_type.edit_type,
            value)

    @classmethod
    def to_yaml(cls, dumper, data):
        """Converts and instance of the class into serialized YAML"""
        print(data)
        return dumper.represent_mapping(cls.yaml_tag, {
            'name': data.name,
            'data_type': cls.serialize_data_type(data.data_type),
            'value': data.value,
        })

    def __eq__(self, other):
        return (self.name == other.name and
                self.data_type == other.data_type and
                self.value == other.value)

    def __repr__(self):
        return (f"<{self.__class__.__name__}"
                f"(name={self.name},data_type={self.data_type},value={self.value})>")


# Custom tag added in global scope - required for safe_load() and safe_dump()
yaml.SafeDumper.add_multi_representer(PropertyTag, PropertyTag.to_yaml)
