import io
import unittest

from mailprep.merge import create_map_dict, FieldMapper, _wrap_in_braces, ConfigMergeMapping

class TestConfigMergeMapping(unittest.TestCase):

    def test_from_stream(self):
        stream_contents = (
            '[filename.xlsx]\n'
            'id       = {ID1}:{ID2}\n'
            'first    = {name1}, {name9}\n'
            'title    = {Title}, {title2}\n'
            'company  = {Firm}, {company}\n'
            'address  = {Line1}\n'
            'address2 = {Line2}\n'
            'city     = {City} {State} {Zip}\n'
            'salline  = {mr}\n'
            'list_id  = {list_id}\n'
            '\n'
            '[second.xlsx]\n'
            'id       = {id}\n'
            'first    = {name_line}\n'
            'title    = {title}\n'
            'address  = {address}\n'
            'city     = {last_line}\n'
            '\n'
        )
        input_stream = io.StringIO(stream_contents)
        mapping = ConfigMergeMapping.from_stream(input_stream)

        # Test all files loaded
        expected_filenames = ['filename.xlsx', 'second.xlsx']
        self.assertSequenceEqual(expected_filenames, list(mapping.get_files()))

        # Test mapping
        expected_map = {
            'id': '{id}',
            'first': '{name_line}',
            'title': '{title}',
            'address': '{address}',
            'city': '{last_line}',
        }
        actual_map = mapping.get_mappings('second.xlsx')
        self.assertDictEqual(expected_map, actual_map)

    def test_multiple_files(self):
        file1_name = 'filename.xlsx'
        file1_headers = [
            'index',
            'mr',
            'ID1',
            'ID2',
            'name1',
            'name9',
            'Title',
            'title2',
            'Firm',
            'company',
            'Line1',
            'Line2',
            'City',
            'State',
            'Zip',
            'list_id',
        ]
        file2_name = 'second.xlsx'
        file2_headers = [
            'id',
            'name_line',
            'title',
            'address',
            'last_line',
        ]

        mapping = ConfigMergeMapping()
        mapping.set_file_mappings(file1_name, create_map_dict(file1_headers))
        mapping.set_file_mappings(file2_name, create_map_dict(file2_headers))
        f = io.StringIO()
        mapping.write_to_stream(f)
        actual = f.getvalue()

        expected = (
            '[filename.xlsx]\n'
            'id       = {ID1}:{ID2}\n'
            'first    = {name1}, {name9}\n'
            'title    = {Title}, {title2}\n'
            'company  = {Firm}, {company}\n'
            'address  = {Line1}\n'
            'address2 = {Line2}\n'
            'city     = {City} {State} {Zip}\n'
            'salline  = {mr}\n'
            'list_id  = {list_id}\n'
            '\n'
            '[second.xlsx]\n'
            'id       = {id}\n'
            'first    = {name_line}\n'
            'title    = {title}\n'
            'address  = {address}\n'
            'city     = {last_line}\n'
            '\n'
        )
        self.assertEqual(expected, actual)

    def test_write_read_write_reversible(self):
        file1_name = 'filename.xlsx'
        file1_headers = [
            'index',
            'mr',
            'ID1',
            'ID2',
            'name1',
            'name9',
            'Title',
            'title2',
            'Firm',
            'company',
            'Line1',
            'Line2',
            'City',
            'State',
            'Zip',
            'list_id',
        ]
        file2_name = 'second.xlsx'
        file2_headers = [
            'id',
            'name_line',
            'title',
            'address',
            'last_line',
        ]

        mapping = ConfigMergeMapping()
        mapping.set_file_mappings(file1_name, create_map_dict(file1_headers))
        mapping.set_file_mappings(file2_name, create_map_dict(file2_headers))
        f = io.StringIO()
        mapping.write_to_stream(f)

        # Read and write again to test revisiblity and idempotency
        f.seek(0)
        mapping2 = ConfigMergeMapping.from_stream(f)
        f2 = io.StringIO()
        mapping2.write_to_stream(f2)
        actual = f2.getvalue()

        expected = (
            '[filename.xlsx]\n'
            'id       = {ID1}:{ID2}\n'
            'first    = {name1}, {name9}\n'
            'title    = {Title}, {title2}\n'
            'company  = {Firm}, {company}\n'
            'address  = {Line1}\n'
            'address2 = {Line2}\n'
            'city     = {City} {State} {Zip}\n'
            'salline  = {mr}\n'
            'list_id  = {list_id}\n'
            '\n'
            '[second.xlsx]\n'
            'id       = {id}\n'
            'first    = {name_line}\n'
            'title    = {title}\n'
            'address  = {address}\n'
            'city     = {last_line}\n'
            '\n'
        )
        self.assertEqual(expected, actual)

    def test_create_from_file_name_and_headers(self):
        file_name = 'filename.xlsx'
        file_headers = [
            'index',
            'mr',
            'ID1',
            'ID2',
            'name1',
            'name9',
            'Title',
            'title2',
            'Firm',
            'company',
            'Line1',
            'Line2',
            'City',
            'State',
            'Zip',
            'list_id',
        ]
        mapping = ConfigMergeMapping()
        mapping.set_file_mappings(file_name, create_map_dict(file_headers))
        f = io.StringIO()
        mapping.write_to_stream(f)
        actual = f.getvalue()
        expected = (
            '[filename.xlsx]\n'
            'id       = {ID1}:{ID2}\n'
            'first    = {name1}, {name9}\n'
            'title    = {Title}, {title2}\n'
            'company  = {Firm}, {company}\n'
            'address  = {Line1}\n'
            'address2 = {Line2}\n'
            'city     = {City} {State} {Zip}\n'
            'salline  = {mr}\n'
            'list_id  = {list_id}\n'
            '\n'
        )
        self.assertEqual(expected, actual)


class TestFieldMapper(unittest.TestCase):

    def test_pattern(self):
        actual = FieldMapper('id', [r'id\d?'], ':').pattern
        expected = r'\bid\d?\b'
        self.assertEqual(expected, actual)

    def test_is_match_true(self):
        mapper = FieldMapper('id', [r'id\d?'], ':')
        self.assertTrue(mapper.is_match('ID'))
        self.assertTrue(mapper.is_match('id1'))
        self.assertTrue(mapper.is_match(' id1'))

    def test_is_match_false(self):
        mapper = FieldMapper('id', [r'id\d?'], ':')
        self.assertFalse(mapper.is_match('ida'))
        self.assertFalse(mapper.is_match('test'))
        self.assertFalse(mapper.is_match('i d'))


class TestWrapInBraces(unittest.TestCase):

    def test_wrap_in_braces(self):
        actual = _wrap_in_braces('name1')
        expected = '{name1}'
        self.assertEqual(expected, actual)


class TestGetHeaders(unittest.TestCase):

    def test_create_map_dict_basic(self):
        headers = [
            'id',
            'first',
            'title',
            'company',
            'address',
            'address2',
            'city',
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{id}',
            'first': '{first}',
            'title': '{title}',
            'company': '{company}',
            'address': '{address}',
            'address2': '{address2}',
            'city': '{city}',
        }
        self.assertDictEqual(expected_map, actual_map)

    def test_create_map_dict_with_extra(self):
        headers = [
            'id',
            'first',
            'title',
            'company',
            'address',
            'address2',
            'city',
            'index',  # 'index' is specifically Ignored
            'salutation_line',  # Converted to salline
            'anythingelse',  # Mapped Directly
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{id}',
            'first': '{first}',
            'title': '{title}',
            'company': '{company}',
            'address': '{address}',
            'address2': '{address2}',
            'city': '{city}',
            'salline': '{salutation_line}',
            'anythingelse': '{anythingelse}',
        }
        self.assertDictEqual(expected_map, actual_map)

    def test_create_map_dict_headers(self):
        headers = [
            'id',
            'first',
            'title',
            'company',
            'address',
            'last_line',
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{id}',
            'first': '{first}',
            'title': '{title}',
            'company': '{company}',
            'address': '{address}',
            'city': '{last_line}',
        }
        self.assertDictEqual(expected_map, actual_map)

    def test_create_map_dict_city_mapping(self):
        headers = [
            'id',
            'first',
            'title',
            'company',
            'address',
            'address2',
            'last_line',
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{id}',
            'first': '{first}',
            'title': '{title}',
            'company': '{company}',
            'address': '{address}',
            'address2': '{address2}',
            'city': '{last_line}',
        }
        self.assertDictEqual(expected_map, actual_map)

    def test_create_map_dict_complex(self):
        headers = [
            'index',
            'mr',
            'ID1',
            'ID2',
            'name_line',
            'name9',
            'Title',
            'title2',
            'Firm',
            'company',
            'Line1',
            'Line2',
            'City',
            'State',
            'Zip',
            'list_id',
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{ID1}:{ID2}',
            'first': '{name9} {name_line}',
            'title': '{Title}, {title2}',
            'company': '{Firm}, {company}',
            'address': '{Line1}',
            'address2': '{Line2}',
            'city': '{City} {State} {Zip}',
            'salline': '{mr}',
            'list_id': '{list_id}',
        }
        self.assertDictEqual(expected_map, actual_map)

    def test_create_map_dict_complex_name9(self):
        headers = [
            'index',
            'mr',
            'ID1',
            'ID2',
            'name1',
            'name9',
            'Title',
            'title2',
            'Firm',
            'company',
            'Line1',
            'Line2',
            'City',
            'State',
            'Zip',
            'list_id',
        ]
        actual_map = create_map_dict(headers)
        expected_map = {
            'id': '{ID1}:{ID2}',
            'first': '{name1}, {name9}',
            'title': '{Title}, {title2}',
            'company': '{Firm}, {company}',
            'address': '{Line1}',
            'address2': '{Line2}',
            'city': '{City} {State} {Zip}',
            'salline': '{mr}',
            'list_id': '{list_id}',
        }
        self.assertDictEqual(expected_map, actual_map)
