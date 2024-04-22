"""
Implement own hashmap class (put, get methods are required).
write tests for this class.
add notes with argumentation for choosen implementation.
"""


class HashTable:
    def __init__(self, capacity):
        self.values = capacity * [None]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def put(self, key, value):
        self.__setitem__(key, value)

    def __len__(self):
        return len(self.values)

    def __setitem__(self, key, value):
        self.values[self._index(key)] = value

    def __getitem__(self, key):
        value = self.values[self._index(key)]
        if value is None:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __delitem__(self, key):
        if key in self:
            self[key] = None
        else:
            raise KeyError(key)

    def _index(self, key):
        return hash(key) % len(self)
