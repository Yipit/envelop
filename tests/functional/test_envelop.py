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
import os
import pytest


def test_envelop_environment_from_file():
    # Given that I load variables to my environment from a file
    env = Environment.from_file(
        os.path.join(os.path.dirname(__file__), './fixtures/env.cfg'))

    # When I try to find a variable defined in that file, then I see that it
    # works
    assert env.get('FAVORITE_SUPER_HERO') == 'Batman NANANANANA'


def test_envelop_environment_from_directory():
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    # When I try to list all the variables inside of that folder
    assert sorted(env.items(), key=lambda x: x[0]) == [
        ('ALLOWED_IPS', '10.0.0.1,10.0.0.2'),
        ('ENABLE_SOMETHING', u''),
        ('PI', u'3.14'),
        ('SERVER_URI', u'smtp://user@mserver.com:passwd@mserver.com:25'),
    ]

    # When I try to find the variables, then I see they're there correctly
    assert env.get_bool('ENABLE_SOMETHING') is False
    assert env.get_bool('ENABLE_SOMETHING_ELSE', True) is True
    assert env.get_float('PI') == 3.14
    assert env.get_uri('SERVER_URI').host == 'mserver.com'
    assert env.get_uri('SERVER_URI').user == 'user@mserver.com'


def test_envelop_environment_from_directory_that_does_not_exist():
    # When I try to load the environment from a folder that does not exist,
    # Then I see that I receive an OSError
    with pytest.raises(OSError):
        Environment.from_folder('something-that-does-not-exist')


def test_envelop_environment_from_directory_set():
    # Given that I load variables to my env from a folder
    path = os.path.join(os.path.dirname(__file__), './fixtures/env')
    env = Environment.from_folder(path)

    # When I set a new variable to my folder env
    env.set('CITY', 'NEW-YORK')

    # Then I see the file was created with the right content
    target = os.path.join(path, 'CITY')
    assert os.path.exists(target)

    # And then I see that the value is also right
    assert open(target).read() == 'NEW-YORK'

    # And then I see that after removing the item, the file will also go away
    del env['CITY']
    assert os.path.exists(target) is False
