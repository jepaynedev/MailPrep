import unittest

from utils.mapping import CaseInsensitiveDict, recursive_merge


class TestInsensitiveDict(unittest.TestCase):

    def test_insensitive_dict_basic_create(self):
        test_dict = CaseInsensitiveDict({ "a": 1 })
        assert test_dict["a"] == 1

    def test_insensitive_dict_basic_insensitve_use(self):
        test_dict = CaseInsensitiveDict({ "a": 1, "B": 2 })
        assert test_dict["A"] == 1
        assert test_dict["b"] == 2

    def test_insensitive_dict_basic_stripped_use(self):
        test_dict = CaseInsensitiveDict()
        test_dict[" a "] = 1
        assert test_dict["A"] == 1

    def test_insensitive_dict_basic_insensitive_override(self):
        test_dict = CaseInsensitiveDict()
        test_dict["a"] = 1
        test_dict["A"] = 2
        assert test_dict["a"] == 2

    def test_insensitive_dict_basic_interior_whitespace(self):
        test_dict = CaseInsensitiveDict()
        test_dict["a  b"] = 1
        assert test_dict["a b"] == 1

    def test_insensitive_dict_basic_deep(self):
        test_dict = CaseInsensitiveDict({ "a": { "b": 1 } })
        assert test_dict["A"]["B"] == 1

    def test_insensitive_dict_get_with_default(self):
        test_dict = CaseInsensitiveDict({ "a": 1 })
        assert test_dict.get("b", 2) == 2


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

