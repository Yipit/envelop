import io
import os
import urlparse
import yaml


class Environment(object):

    def __init__(self, base=None, storage=os.environ):
        self.storage = storage
        self.storage.update(base or {})

    @classmethod
    def from_file(cls, path):
        return cls(storage=yaml.load(io.open(path)))

    def items(self):
        return self.storage.items()

    def get(self, name):
        return self.storage.get(name)

    def set(self, name, val):
        self.storage[name] = val

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
