"""Mappings for common field and merging data into columns using a given mapping"""
import re
import collections
import configparser

from utils.common import coalesce, pad_right


class ConfigMergeMapping:
    """Manages merge field mappings"""

    def __init__(self, file_mappings=None):
        self.set_all_mappings(coalesce(file_mappings, collections.OrderedDict()))

    @classmethod
    def from_stream(cls, stream):
        """Create new instance from a steam object parsed as a ConfigParser"""
        config = configparser.ConfigParser()
        config.read_file(stream)
        file_mapping = collections.OrderedDict([
            (section, collections.OrderedDict(config.items(section)))
            for section in config.sections()
        ])
        return cls(file_mapping)

    def get_files(self):
        """Returns all files with mappings (i.e. top level section headers)"""
        return self.file_mappings.keys()

    def get_mappings(self, file_name):
        """Gets all field mappings for the specified file"""
        return self.file_mappings[file_name]

    def get_mapping(self, file_name, field_name):
        """Gets a mappings given the file name and field name"""
        return self.get_mappings(file_name)[field_name]

    def set_file_mappings(self, file_name, mappings):
        """Sets the given file mappings to a mappings OrderedDict"""
        self.file_mappings[file_name] = mappings

    def set_all_mappings(self, full_mapping):
        """Sets all mappings to the given two level OrderedDict"""
        self.file_mappings = full_mapping

    def write_to_stream(self, stream):
        """Writes all mappings to a stream in a pretty formatted format"""
        # Get max field length for all keys in all files (to line of equals sign in entire file)
        all_fields = [
            key
            for file_name in self.get_files()
            for key in self.get_mappings(file_name).keys()
        ]
        max_field_length = len(max(all_fields, key=len))
        config = configparser.ConfigParser()
        for file_name in self.get_files():
            config.add_section(file_name)
            for option, value in self.get_mappings(file_name).items():
                config.set(file_name, pad_right(option, max_field_length), value)
        config.write(stream)


class FieldMapper:
    """Matches specified headers and formats into a string defining the mapping"""

    def __init__(self, output_field_name, input_field_patterns, join_string=' '):
        self.output_field_name = output_field_name
        self.pattern = self._build_pattern(input_field_patterns)
        self.join_string = join_string

    def is_match(self, value):
        """Checks if the given string matches the pattern for this FieldMapper instance"""
        return re.match(self.pattern, value.strip(), re.IGNORECASE) is not None

    def get_matching_headers(self, headers):
        """Returns a list of all given headers that match for this FieldMapper instance"""
        return [header for header in headers if self.is_match(header)]

    def get_mapping_string(self, matching_headers):
        """Joins the given matched fields into a single string wrapping fields in curly braces"""
        return self.join_string.join([_wrap_in_braces(header) for header in matching_headers])

    def _build_pattern(self, input_field_patterns):
        """Wraps input field patterns with word breaks and join with optional regex character"""
        return '|'.join([fr'\b{pattern}\b' for pattern in input_field_patterns])


def _wrap_in_braces(value):
    """Wraps the input string in curly braces"""
    return f'{{{value}}}'


class NameFieldMapper(FieldMapper):
    """Matches specified headers and formats into a string defining the mapping

    Includes name field specific mapping formatting (adds ',' before possible 'name9' field)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_mapping_string(self, matching_headers):
        """Override to substitude a comma before the name9 field if present"""
        base_mapping = super().get_mapping_string(matching_headers)
        # Add comma before {name9} field
        name9_pattern = r"(?<=\})\s+(?=\{name9\})"  # Match 1+ whitespace between '}' and '{name9}'
        return re.sub(name9_pattern, ", ", base_mapping, re.IGNORECASE)


def create_map_dict(headers):
    """ Creates a dictionary of default mappings for the map file """
    # List of mappings to match input headers and return output fields with defined join string
    field_mapping_definitions = [
        FieldMapper('id', [r'id\d?'], join_string=':'),
        NameFieldMapper('first', [r'name\d?', r'name_?line', r'first', r'suffix', r'_prefix']),
        FieldMapper('title', [r'title\d?'], join_string=', '),
        FieldMapper('company', [r'firm\d?', r'company\d?'], join_string=', '),
        FieldMapper('address', [r'address1?', r'line1?']),
        FieldMapper('address2', [r'address2', r'line2']),
        FieldMapper('city', [r'city', r'last_?line', r'st(ate)?\d?', r'zip']),
        FieldMapper('salline', [
            r'dr', r'mrs?',
            r'nameprefix', r'nametitle',
            r'sal', r'salutation', r'salutation_line']),
    ]
    # List of fields to be ignore regardless of their presence
    field_mapping_blacklist = ['index']

    # Create a copy of all headers to mutate without affecting input list
    unhandled_headers = [header for header in headers if header not in field_mapping_blacklist]
    # New dictionary to return mapping (orderd for consistency)
    mapped_fields = collections.OrderedDict()

    for field_mapper in field_mapping_definitions:
        # Get all fields that match the current field_mapper
        map_fields = field_mapper.get_matching_headers(unhandled_headers)
        # Lexegraphically sort the matching fields (mostly to order numbered fields correctly)
        map_fields.sort()

        # If any fields matched, add the mapping string to the mapped fields to be returned
        if map_fields:
            output_field = field_mapper.output_field_name
            mapped_fields[output_field] = field_mapper.get_mapping_string(map_fields)

        # Remove mapped fields from total field list as they are now handled
        unhandled_headers = [header for header in unhandled_headers if header not in map_fields]

    # Add any remaining fields directly as their original name
    # (basically just includes the columns entirely unchanged in the mapping)
    for field in unhandled_headers:
        mapped_fields[field] = _wrap_in_braces(field)

    return mapped_fields
