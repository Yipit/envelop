import commands

# Aliasing to avoid typing and caching the dot resolution
run = commands.getoutput


def test_get():
    # Given that I have a variable inside of a file,
    # When I try to get its value,
    # Then I see the value is right
    (run('python milieu -f tests/functional/fixtures/env.cfg get FAVORITE_SUPER_HERO')
     .should.equal('Batman NANANANANA'))


def test_get_uri():
    (run('python milieu -d tests/functional/fixtures/env get-uri user SERVER_URI')
     .should.equal('user@mserver.com'))
    (run('python milieu -d tests/functional/fixtures/env get-uri password SERVER_URI')
     .should.equal('passwd'))
    (run('python milieu -d tests/functional/fixtures/env get-uri host SERVER_URI')
     .should.equal('mserver.com'))
    (run('python milieu -d tests/functional/fixtures/env get-uri port SERVER_URI')
     .should.equal('25'))
