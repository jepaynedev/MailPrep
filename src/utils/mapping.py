"""Custom Mapping/Dict implementations and utility functions for working with Mapping/Dicts"""
import unicodedata
import collections.abc


class CaseInsensitiveDict(collections.abc.MutableMapping):
    """Mapping with normalized and case insensitive keys (stored as lower case)"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(*args, **kwargs)  # Set with update to apply transforms

    def __getitem__(self, key):
        return self.store[self.keytransform(key)]

    def __setitem__(self, key, value):
        # If any value in the dict is a dict itself, it should also be converted to a CaseInsensitiveDict
        if isinstance(value, dict):
            print(f'__setitem__({key},{value})')
            self.store[self.keytransform(key)] = CaseInsensitiveDict(value)
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