from handy import Environment


def test_handy_environment_set():
    # Given that I have an empty environment
    env = Environment()
    env.items().should.equal([])

    # When I set something
    env.set('myvar', 'myvalue')

    # I'll be able to get it properly
    env.items().should.equal([('myvar', 'myvalue')])


def test_handy_environment_get():
    # Given that I have an environment
    env = Environment(val1='yo')

    # When I set something
    env.get('val1').should.equal('yo')


def test_handy_environment_get_uri():
    # Given that I have an environment with a variable containing a uri
    env = Environment()
    env.set('githubpage', 'https://clarete:passwd!!@github.com/yipit/handy')

    # When I try to get the value as a Uri
    uri = env.get_uri('githubpage')

    # Then I see things working
    uri.scheme.should.equal('https')
    uri.host.should.equal('github.com')
    uri.port.should.equal(None)
    uri.user.should.equal('clarete')
    uri.password.should.equal('passwd!!')
    uri.path.should.equal('/yipit/handy')
    uri.relative_path.should.equal('yipit/handy')
