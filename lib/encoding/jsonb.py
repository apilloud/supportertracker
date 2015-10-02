'''
This module impliments Canonical json objects.
These objects are compatible with Postgres jsonb.
'''
import collections
import json


class Canonical(object):

    def __new__(cls, *args, **kwargs):
        if kwargs:
            raise TypeError
        if len(args) != 1:
            raise TypeError
        if isinstance(args[0], Canonical):
            cls = type(args[0])
            assert cls != Canonical
        elif isinstance(args[0], (list, tuple)):
            cls = CanonicalList
        elif isinstance(args[0], dict):
            cls = CanonicalDict
        else:
            return args[0]
        self = cls.__new__(cls, *args, **kwargs)
        self.__init__(*args, **kwargs)
        return self

    def __unicode__(self):
        out = json.dumps(self, allow_nan=False)
        # Undo json dumps downgrade to ASCII.
        # RFC4627: All Unicode characters may be placed within the
        # quotation marks except for the characters that must be escaped:
        # quotation mark, reverse solidus, and the control characters (U+0000
        # through U+001F).
        out = out.replace('\\\\', '\\\\\\\\')
        out = out.replace('\\"', '\\\\"')
        out = out.replace('\\b', '\\\\b')
        out = out.replace('\\f', '\\\\f')
        out = out.replace('\\n', '\\\\n')
        out = out.replace('\\r', '\\\\r')
        out = out.replace('\\t', '\\\\t')
        out = out.replace('\\u000', '\\\\u000')
        out = out.replace('\\u001', '\\\\u001')
        return out.decode('unicode_escape')

    def __str__(self):
        return self.__unicode__().encode('utf_8')

    def __repr__(self):
        return self.__str__()


class CanonicalList(Canonical, list):

    def __new__(cls, *args, **kwargs):
        return list.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Canonical.__init__(self, *args, **kwargs)
        list.__init__(self, *args, **kwargs)
        for key, value in enumerate(self):
            self.__setitem__(key, value)

    def __setitem__(self, key, value):
        list.__setitem__(self, key, Canonical(value))


class CanonicalDict(Canonical, collections.MutableMapping, dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Canonical.__init__(self, *args, **kwargs)
        dict.__init__(self, *args, **kwargs)
        self._keys = self._sort_keys()
        for key, value in dict.items(self):
            self.__setitem__(key, Canonical(value))

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, Canonical(value))
        if key not in self._keys:
            self._keys = self._sort_keys()

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __iter__(self):
        return self._keys.__iter__()

    def _sort_keys(self):
        return [x[1] for x in sorted([(len(x), x) for x in dict.keys(self)])]
