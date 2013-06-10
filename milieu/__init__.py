from __future__ import unicode_literals

import io
import os
import urlparse
import yaml


class FolderStorage(dict):
    def __init__(self, path):
        self.path = path

    def _open(self, name, mode='r'):
        return io.open(os.path.join(self.path, name), mode)

    def get(self, name, failobj=None):
        try:
            # If we need to optimize the amount of IO calls we make over the
            # time, we just have to cache the modified data when we open the
            # file and compare with the current time when we need the file
            # again.
            super(FolderStorage, self).__setitem__(
                name, self._open(name).read().strip())
            return self[name]
        except IOError:
            return failobj

    def __setitem__(self, name, value):
        super(FolderStorage, self).__setitem__(
            name, self._open(name, 'w').write(unicode(value)))

    def __delitem__(self, name):
        os.unlink(os.path.join(self.path, name))
        super(FolderStorage, self).__delitem__(name)

    def items(self):
        return [(i, self.get(i)) for i in os.listdir(self.path)]


class Environment(object):

    def __init__(self, base=None, storage=os.environ):
        self.storage = storage
        self.storage.update(base or {})

    @classmethod
    def from_file(cls, path):
        return cls(storage=yaml.load(io.open(path)))

    @classmethod
    def from_folder(cls, path):
        return cls(storage=FolderStorage(path))

    def __delitem__(self, name):
        del self.storage[name]

    def items(self):
        return self.storage.items()

    def set(self, name, val):
        self.storage[name] = val

    def get(self, name, failobj=None):
        return self.storage.get(name, failobj)

    def get_int(self, name, failobj=None):
        return int(self.get(name, failobj))

    def get_float(self, name, failobj=None):
        return float(self.get(name, failobj))

    def get_bool(self, name, failobj=None):
        val = unicode(self.get(name, failobj)).lower()
        try:
            return bool(int(val))
        except ValueError:
            return val == 'true'

    def get_uri(self, name, default=None):
        uri = self.storage.get(name, default)
        if not uri:
            return None

        obj = urlparse.urlparse(uri)

        # Our internal aliases
        obj.host = obj.hostname
        obj.user = obj.username
        obj.relative_path = obj.path

        # Cleaning up the relative_path variable
        while obj.relative_path and obj.relative_path[0] == '/':
            obj.relative_path = obj.relative_path[1:]
        return obj
