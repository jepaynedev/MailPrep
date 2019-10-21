import unittest

from utils.common import  pad_right


class TestPadRight(unittest.TestCase):

    def test_pad_right(self):
        actual = pad_right('a', 3)
        self.assertEqual('a  ', actual)

    def test_pad_too_long(self):
        actual = pad_right('abc', 2)
        self.assertEqual('abc', actual)