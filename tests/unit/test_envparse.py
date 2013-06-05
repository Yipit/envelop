# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import os
from mock import patch
from envparse import Environment


def test_envparse_environment_set():
    # Given that I have an empty environment
    env = Environment()

    # When I set something
    env.set('myvar', 'myvalue')

    # I'll be able to get it properly
    env.items().should.contain(('myvar', 'myvalue'))


def test_envparse_environment_get():
    # Given that I have an environment
    env = Environment({'val1': 'yo'})

    # When I set something
    env.get('val1').should.equal('yo')


def test_envparse_environment_get_uri():
    # Given that I have an environment with a variable containing a uri
    env = Environment()
    env.set('githubpage', 'https://clarete:passwd!!@github.com/yipit/envparse')

    # When I try to get the value as a Uri
    uri = env.get_uri('githubpage')

    # Then I see things working
    uri.scheme.should.equal('https')
    uri.host.should.equal('github.com')
    uri.port.should.equal(None)
    uri.user.should.equal('clarete')
    uri.password.should.equal('passwd!!')
    uri.path.should.equal('/yipit/envparse')
    uri.relative_path.should.equal('yipit/envparse')


def test_envparse_environment_get_uri_returning_none():
    # Given that I have an empty environment
    env = Environment()

    # When I try to get a uri variable that doesn't exist, then I get None
    env.get_uri('blah').should.be.none

    # And When I try to get a variable that doesn't exist but I provide a
    # default value, it will be returned instead of none
    env.get_uri('blah', 'http://yipit.com').host.should.equal('yipit.com')


def test_envparse_with_a_real_environment():
    # Given that I have an environment
    env = Environment()

    # When I set a variable in that environment
    env.set('yo-dawg', 'I heard you like variables')

    # Then I see that it was set in the actual environment
    os.environ.get('yo-dawg').should.equal('I heard you like variables')


@patch('envparse.io')
def test_envparse_environment_from_file(_io):
    # Given that I load variables to my environment from a file
    _io.open.return_value = io.StringIO('FAVORITE_SUPER_HERO: Batman!')
    env = Environment.from_file('myfile.cfg')

    # When I try to find a variable defined in that file, then I see that it
    # works
    env.get('FAVORITE_SUPER_HERO').should.equal('Batman!')
