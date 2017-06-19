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
from envelop import Environment
from mock import patch
import io
import os
import pytest


def test_envelop_environment_set():
    # Given that I have an empty environment
    env = Environment()

    # When I set something
    env.set('myvar', 'myvalue')

    # I'll be able to get it properly
    assert ('myvar', 'myvalue') in env.items()


def test_envelop_environment_get():
    # Given that I have an environment
    env = Environment({'val1': 'yo'})

    # When I set something
    assert env.get('val1') == 'yo'


def test_envelop_environment_get_uri():
    # Given that I have an environment with a variable containing a uri
    env = Environment()
    env.set('githubpage', 'https://clarete:passwd!!@github.com/yipit/envelop')

    # When I try to get the value as a Uri
    uri = env.get_uri('githubpage')

    # Then I see things working
    assert uri.scheme == 'https'
    assert uri.host == 'github.com'
    assert uri.port is None
    assert uri.user == 'clarete'
    assert uri.password == 'passwd!!'
    assert uri.path == '/yipit/envelop'
    assert uri.relative_path == 'yipit/envelop'


def test_envelop_environment_get_uri_returning_none():
    # Given that I have an empty environment
    env = Environment()

    # When I try to get a uri variable that doesn't exist, then I get None
    assert env.get_uri('blah') is None

    # And When I try to get a variable that doesn't exist but I provide a
    # default value, it will be returned instead of none
    assert env.get_uri('blah', 'http://yipit.com').host == 'yipit.com'


def test_envelop_with_a_real_environment():
    # Given that I have an environment
    env = Environment()

    # When I set a variable in that environment
    env.set('yo-dawg', 'I heard you like variables')

    # Then I see that it was set in the actual environment
    assert os.environ.get('yo-dawg') == 'I heard you like variables'


def test_envelop_helper_methods():
    # Given that I have an environment with some variables set
    data = {
        'str': 'I heard you like variables',
        'int': '42',
        'float': '3.14',
        'bool0': 'True',
        'bool1': 'true',
        'bool2': '1',
        'bool3': '2',
        'bool4': 'False',
        'bool5': 'false',
        'bool6': '0',
        'list': 'foo,bar,baz'
    }
    env = Environment(storage=data)

    # Let's retrieve things with their correct types
    assert env.get_int('int') == 42
    assert env.get_float('float') == 3.14
    assert env.get_bool('bool0') is True
    assert env.get_bool('bool1') is True
    assert env.get_bool('bool2') is True
    assert env.get_bool('bool3') is True
    assert env.get_bool('bool4') is False
    assert env.get_bool('bool5') is False
    assert env.get_bool('bool6') is False
    assert env.get_list('list') == ['foo', 'bar', 'baz']

    # Sanity checks
    with pytest.raises(ValueError):
        env.get_int('str')
    with pytest.raises(ValueError):
        env.get_float('str')
    assert env.get_bool('str') is False

    # Testing default values
    assert env.get('i-dont-exist', 'blah') == 'blah'
    assert env.get_int('i-dont-exist', 2) == 2
    assert env.get_float('i-dont-exist', 2.5) == 2.5
    assert env.get_bool('i-dont-exist', True) is True


@patch('envelop.io')
def test_envelop_environment_from_file(_io):
    # Given that I load variables to my environment from a file
    _io.open.return_value = io.StringIO('FAVORITE_SUPER_HERO: Batman!')
    env = Environment.from_file('myfile.cfg')

    # When I try to find a variable defined in that file, then I see that it
    # works
    assert env.get('FAVORITE_SUPER_HERO') == 'Batman!'


@patch('envelop.io')
@patch('envelop.os')
def test_envelop_environment_from_directory_items(_os, _io):
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    _os.listdir.return_value = ['ENABLE_SOMETHING', 'PI', 'SERVER_URI']
    _io.open.return_value.read.side_effect = [
        '',
        '3.14',
        'smtp://user@mserver.com:passwd@mserver.com:25',
    ]

    # When I try to list all the variables inside of that folder
    assert sorted(env.items(), key=lambda x: x[0]) == [
        ('ENABLE_SOMETHING', u''),
        ('PI', u'3.14'),
        ('SERVER_URI', u'smtp://user@mserver.com:passwd@mserver.com:25'),
    ]


@patch('envelop.io')
@patch('envelop.os')
def test_envelop_environment_from_directory_get(_os, _io):
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    _os.listdir.return_value = ['ENABLE_SOMETHING', 'PI', 'SERVER_URI']
    _io.open.return_value.read.side_effect = [
        '',
        IOError,
        '3.14',
        'smtp://user@mserver.com:passwd@mserver.com:25',
        'smtp://user@mserver.com:passwd@mserver.com:25',
    ]

    # When I try to find the variables, then I see they're there correctly
    assert env.get_bool('ENABLE_SOMETHING') is False
    assert env.get_bool('ENABLE_SOMETHING_ELSE', True) is True
    assert env.get_float('PI') == 3.14
    assert env.get_uri('SERVER_URI').host == 'mserver.com'
    assert env.get_uri('SERVER_URI').user == 'user@mserver.com'


@patch('envelop.io')
@patch('envelop.os.path.isdir', lambda *a: True)
def test_envelop_environment_from_directory_set(_io):
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    # When I set some stuff
    env.set('CITY', 'NEW-YORK')

    # Then I see that we always try to write the file
    _io.open.return_value.write.assert_called_once_with('NEW-YORK')


@patch('envelop.io')
@patch('envelop.os')
def test_envelop_environment_from_directory_del(_os, _io):
    # Given that I have a folder environment with an item `CITY`
    env = Environment.from_folder('./path')
    env.set('CITY', 'NEW-YORK')

    # We need the path.join function over there, so we need to restore it
    # manually
    _os.path.join.side_effect = os.path.join

    # When I remove that item
    del env['CITY']

    # Then I can see that the unlink function was called properly
    _os.unlink.assert_called_once_with('./path/CITY')
