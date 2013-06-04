import os
import urlparse


class Environment(object):

    def __init__(self, base=None):
        os.environ.update(base or {})

    def items(self):
        return os.environ.items()

    def get(self, name):
        return os.environ.get(name)

    def set(self, name, val):
        os.environ[name] = val

    def get_uri(self, name, default=None):
        uri = os.environ.get(name, default)
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
