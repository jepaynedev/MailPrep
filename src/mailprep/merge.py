"""Mappings for common field and merging data into columns using a given mapping"""
import re
import collections
import configparser


DEFAULT_SECTION_NAME = 'FieldMap'


def create_config_mapping_from_headers(headers, config_section=DEFAULT_SECTION_NAME):
    """Given a list of file headers, create a ConfigParser instance with mapped fields"""
    mapping_dict = create_map_dict(headers)
    return create_config_object(mapping_dict, config_section)


def create_config_object(mapping_dict, header=DEFAULT_SECTION_NAME):
    """Writes mapping to a ConfigParser instance (with values aligned)"""
    config = configparser.ConfigParser()
    max_key_len = len(max(mapping_dict.keys(), key=len))
    config[header] = {pad_right(k, max_key_len): v for k, v in mapping_dict.items()}
    return config


def pad_right(value, pad_length):
    return f'{value: <{pad_length}}'

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
