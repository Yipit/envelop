# -*- coding: utf-8 -*-
# milieu - Environment variables manager
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
from milieu import Environment
from mock import patch
import io
import os


def test_milieu_environment_set():
    # Given that I have an empty environment
    env = Environment()

    # When I set something
    env.set('myvar', 'myvalue')

    # I'll be able to get it properly
    env.items().should.contain(('myvar', 'myvalue'))


def test_milieu_environment_get():
    # Given that I have an environment
    env = Environment({'val1': 'yo'})

    # When I set something
    env.get('val1').should.equal('yo')


def test_milieu_environment_get_uri():
    # Given that I have an environment with a variable containing a uri
    env = Environment()
    env.set('githubpage', 'https://clarete:passwd!!@github.com/yipit/milieu')

    # When I try to get the value as a Uri
    uri = env.get_uri('githubpage')

    # Then I see things working
    uri.scheme.should.equal('https')
    uri.host.should.equal('github.com')
    uri.port.should.equal(None)
    uri.user.should.equal('clarete')
    uri.password.should.equal('passwd!!')
    uri.path.should.equal('/yipit/milieu')
    uri.relative_path.should.equal('yipit/milieu')


def test_milieu_environment_get_uri_returning_none():
    # Given that I have an empty environment
    env = Environment()

    # When I try to get a uri variable that doesn't exist, then I get None
    env.get_uri.when.called_with('blah').should.throw(
        RuntimeError,
        'there is no such environment variable as \033[0;33m`blah`\033[0m'
    )

    # And When I try to get a variable that doesn't exist but I provide a
    # default value, it will be returned instead of none
    env.get_uri('blah', 'http://yipit.com').host.should.equal('yipit.com')


def test_milieu_with_a_real_environment():
    # Given that I have an environment
    env = Environment()

    # When I set a variable in that environment
    env.set('yo-dawg', 'I heard you like variables')

    # Then I see that it was set in the actual environment
    os.environ.get('yo-dawg').should.equal('I heard you like variables')


def test_milieu_helper_methods():
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
    }
    env = Environment(storage=data)

    # Let's retrieve things with their correct types
    env.get_int('int').should.equal(42)
    env.get_float('float').should.equal(3.14)
    env.get_bool('bool0').should.be.true
    env.get_bool('bool1').should.be.true
    env.get_bool('bool2').should.be.true
    env.get_bool('bool3').should.be.true
    env.get_bool('bool4').should.be.false
    env.get_bool('bool5').should.be.false
    env.get_bool('bool6').should.be.false

    # Sanity checks
    env.get_int.when.called_with('str').should.throw(ValueError)
    env.get_float.when.called_with('str').should.throw(ValueError)
    env.get_bool('str').should.be.false

    # Testing default values
    env.get('i-dont-exist', 'blah').should.equal('blah')
    env.get_int('i-dont-exist', 2).should.equal(2)
    env.get_float('i-dont-exist', 2.5).should.equal(2.5)
    env.get_bool('i-dont-exist', True).should.be.true


@patch('milieu.io')
def test_milieu_environment_from_file(_io):
    # Given that I load variables to my environment from a file
    _io.open.return_value = io.StringIO('FAVORITE_SUPER_HERO: Batman!')
    env = Environment.from_file('myfile.cfg')

    # When I try to find a variable defined in that file, then I see that it
    # works
    env.get('FAVORITE_SUPER_HERO').should.equal('Batman!')


@patch('milieu.io')
@patch('milieu.os')
def test_milieu_environment_from_directory_items(_os, _io):
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
    sorted(env.items(), key=lambda x: x[0]).should.equal([
        ('ENABLE_SOMETHING', u''),
        ('PI', u'3.14'),
        ('SERVER_URI', u'smtp://user@mserver.com:passwd@mserver.com:25'),
    ])


@patch('milieu.io')
@patch('milieu.os')
def test_milieu_environment_from_directory_get(_os, _io):
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
    env.get_bool('ENABLE_SOMETHING').should.be.false
    env.get_bool('ENABLE_SOMETHING_ELSE', True).should.be.true
    env.get_float('PI').should.equal(3.14)
    env.get_uri('SERVER_URI').host.should.equal('mserver.com')
    env.get_uri('SERVER_URI').user.should.equal('user@mserver.com')


@patch('milieu.io')
def test_milieu_environment_from_directory_set(_io):
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    # When I set some stuff
    env.set('CITY', 'NEW-YORK')

    # Then I see that we always try to write the file
    _io.open.return_value.write.assert_called_once_with('NEW-YORK')


@patch('milieu.io')
@patch('milieu.os')
def test_milieu_environment_from_directory_del(_os, _io):
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
