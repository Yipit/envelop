import os
from envparse import Environment


def test_envparse_environment_from_file():
    # Given that I load variables to my environment from a file
    env = Environment.from_file(
        os.path.join(os.path.dirname(__file__), './fixtures/env.cfg'))

    # When I try to find a variable defined in that file, then I see that it
    # works
    env.get('FAVORITE_SUPER_HERO').should.equal('Batman NANANANANA')
