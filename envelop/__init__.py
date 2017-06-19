# -*- coding: utf-8 -*-
# envelop - Environment variables manager
#
# Copyright (c) 2013  Yipit, Inc <coders@yipit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from six.moves.urllib.parse import urlparse
from six import text_type
import io
import os
import yaml

version = __version__ = '0.3.0'


class FolderStorage(dict):
    def __init__(self, path):
        # We won't do anything before making sure it's a folder
        if not os.path.isdir(path):
            raise OSError('The path `{0}` does not exist'.format(path))
        self.path = path

    def _open(self, name, mode='r'):
        return io.open(os.path.join(self.path, name), mode)

    def get(self, name, failobj=None):
        try:
            # If we need to optimize the amount of IO calls we make over the
            # time, we just have to cache the modified data when we open the
            # file and compare with the current time when we need the file
            # again.
            with self._open(name) as f:
                result = f.read().strip()
        except IOError:
            return failobj
        else:
            super(FolderStorage, self).__setitem__(name, result)
            return self[name]


    def __setitem__(self, name, value):
        with self._open(name, 'w') as f:
            result = f.write(text_type(value))
        super(FolderStorage, self).__setitem__(name, result)

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
        val = text_type(self.get(name, failobj)).lower()
        try:
            return bool(int(val))
        except ValueError:
            return val == 'true'

    # FIXME: every other function uses `failobj` rather than `default`
    def get_uri(self, name, default=None):
        uri = self.storage.get(name, default)
        if not uri:
            return uri

        obj = urlparse(uri)

        # Parse result class using our internal aliases for some fields
        class CustomParseResult(object):
            def __init__(self, parse_result):
                self.scheme = parse_result.scheme
                self.host = parse_result.hostname
                self.port = parse_result.port
                self.user = parse_result.username
                self.password = parse_result.password
                self.path = parse_result.path
                # Cleaning up the relative_path variable
                relative_path = parse_result.path
                while relative_path and relative_path[0] == '/':
                    relative_path = relative_path[1:]
                self.relative_path = relative_path

        result = CustomParseResult(obj)

        return result

    def get_list(self, name, failobj=None, separator=','):
        return self.get(name, failobj).split(separator)
