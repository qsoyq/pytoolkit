from collections import OrderedDict
from collections.abc import MutableMapping


class _MutableMapping(MutableMapping):

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self._store[key] = value

    def __getitem__(self, key):
        return self._store[key]

    def __delitem__(self, key):
        del self._store[key]

    def __len__(self):
        return len(self._store)

    def __iter__(self):
        return iter(self._store)


class LRUCacheOrderedDict(_MutableMapping):

    def __init__(self, maxsize: int = 4096, *args, **kwargs):
        if maxsize <= 0:
            raise ValueError('maxsize must be grater equal than 1.')

        self._maxsize = maxsize
        self._store = OrderedDict()
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        super().__delitem__(key)
        super().__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        if key not in self and len(self._store) >= self._maxsize:
            self._store.popitem(last=False)
        super().__setitem__(key, value)


LRUCacheDict = LRUCacheOrderedDict
