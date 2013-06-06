import os
from envparse import Environment


def test_envparse_environment_from_file():
    # Given that I load variables to my environment from a file
    env = Environment.from_file(
        os.path.join(os.path.dirname(__file__), './fixtures/env.cfg'))

    # When I try to find a variable defined in that file, then I see that it
    # works
    env.get('FAVORITE_SUPER_HERO').should.equal('Batman NANANANANA')


def test_envparse_environment_from_directory():
    # Given that I load variables to my env from a folder
    env = Environment.from_folder(
        os.path.join(os.path.dirname(__file__), './fixtures/env'))

    # When I try to list all the variables inside of that folder
    sorted(env.items(), key=lambda x: x[0]).should.equal([
        ('ENABLE_SOMETHING', u''),
        ('PI', u'3.14'),
        ('SERVER_URI', u'smtp://user@mserver.com:passwd@mserver.com:25'),
    ])

    # When I try to find the variables, then I see they're there correctly
    env.get_bool('ENABLE_SOMETHING').should.be.false
    env.get_bool('ENABLE_SOMETHING_ELSE', True).should.be.true
    env.get_float('PI').should.equal(3.14)
    env.get_uri('SERVER_URI').host.should.equal('mserver.com')
    env.get_uri('SERVER_URI').user.should.equal('user@mserver.com')


def test_envparse_environment_from_directory_set():
    # Given that I load variables to my env from a folder
    path = os.path.join(os.path.dirname(__file__), './fixtures/env')
    env = Environment.from_folder(path)

    # When I set a new variable to my folder env
    env.set('CITY', 'NEW-YORK')

    # Then I see the file was created with the right content
    target = os.path.join(path, 'CITY')
    os.path.exists(target).should.be.true

    # And then I see that the value is also right
    open(target).read().should.equal('NEW-YORK')

    # And then I see that after removing the item, the file will also go away
    del env['CITY']
    os.path.exists(target).should.be.false
