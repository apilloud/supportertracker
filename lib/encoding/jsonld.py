'''
This module impliments Linked json objects.
These objects are compatable with the JSON-LD standard.
'''
import jsonb
import hashlib


class Linked(jsonb.Canonical):

    def __new__(cls, *args, **kwargs):
        if kwargs:
            raise TypeError
        if len(args) != 1:
            raise TypeError
        if isinstance(args[0], Linked):
            cls = type(args[0])
            assert cls != Linked
        elif isinstance(args[0], (list, tuple)):
            cls = LinkedList
        elif isinstance(args[0], dict):
            cls = LinkedDict
        else:
            return args[0]
        return cls.__new__(cls, *args, **kwargs)


class LinkedList(Linked, jsonb.CanonicalList):

    def __new__(cls, *args, **kwargs):
        return jsonb.CanonicalList.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Linked.__init__(self, *args, **kwargs)
        jsonb.CanonicalList.__init__(self, *args, **kwargs)
        # JSON-LD has unordered lists, those are hard. Don't support for now.
        raise TypeError

    def __setitem__(self, key, value):
        jsonb.CanonicalList.__setitem__(self, key, Linked(value))


class LinkedDict(Linked, jsonb.CanonicalDict):

    def __new__(cls, *args, **kwargs):
        return jsonb.CanonicalDict.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        Linked.__init__(self, *args, **kwargs)
        jsonb.CanonicalDict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        if not key:
            raise KeyError(key)
        if key[0] == '@' and key not in ('@context', '@id', '@type'):
            raise KeyError(key)
        if ':' in key:
            raise KeyError(key)
        if key == '@context' and value != 'http://schema.org':
            raise ValueError((key, value))
        if key in ('@id', '@type') and not isinstance(value, str):
            raise ValueError((key, value))
        jsonb.CanonicalDict.__setitem__(self, key, Linked(value))

    def id(self):
        assert '@id' not in self
        return hashlib.sha1(str(self)).hexdigest()
