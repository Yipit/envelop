from future import standard_library
standard_library.install_aliases()

import sys
import subprocess

# Aliasing to avoid typing and caching the dot resolution
run = subprocess.getoutput


def test_get():
    # Given that I have a variable inside of a file,
    # When I try to get its value,
    # Then I see the value is right
    assert run(sys.executable + ' envelop -f tests/functional/fixtures/env.cfg get FAVORITE_SUPER_HERO') == 'Batman NANANANANA'


def test_get_uri():
    assert run(sys.executable + ' envelop -d tests/functional/fixtures/env get-uri user SERVER_URI') == 'user@mserver.com'
    assert run(sys.executable + ' envelop -d tests/functional/fixtures/env get-uri password SERVER_URI') == 'passwd'
    assert run(sys.executable + ' envelop -d tests/functional/fixtures/env get-uri host SERVER_URI') == 'mserver.com'
    assert run(sys.executable + ' envelop -d tests/functional/fixtures/env get-uri port SERVER_URI') == '25'
