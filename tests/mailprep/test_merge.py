import io
import unittest

from mailprep.merge import create_map_dict, FieldMapper, _wrap_in_braces, pad_right, create_config_object, create_config_mapping_from_headers

class TestConfigObject(unittest.TestCase):

    def test_create_config_mapping_from_headers(self):
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
        config = create_config_mapping_from_headers(headers)
        f = io.StringIO()
        config.write(f)
        actual = f.getvalue()
        expected = (
            '[FieldMap]\n'
            'id       = {ID1}:{ID2}\n'
            'first    = {name1}, {name9}\n'
            'title    = {Title}, {title2}\n'
            'company  = {Firm}, {company}\n'
            'address  = {Line1}\n'
            'address2 = {Line2}\n'
            'city     = {City} {State} {Zip}\n'
            'salline  = {mr}\n'
            'list_id  = {list_id}\n\n'
        )
        self.assertEqual(expected, actual)



    def test_create_config_object(self):
        source = {
            'test': 'something',
            'another': 'value'
        }
        f = io.StringIO()
        config = create_config_object(source)
        config.write(f)
        actual = f.getvalue()
        expected = (
            '[FieldMap]\n'
            'test    = something\n'
            'another = value\n\n'
        )
        self.assertEqual(expected, actual)

class TestPadRight(unittest.TestCase):

    def test_pad_right(self):
        actual = pad_right('a', 3)
        self.assertEqual('a  ', actual)

    def test_pad_too_long(self):
        actual = pad_right('abc', 2)
        self.assertEqual('abc', actual)


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
