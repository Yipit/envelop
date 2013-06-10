A helping hand to manage your settings among different environments

## Intro

Managing application configuration that runs on multiple environments
can be tough. So, **milieu** comes to help you pretend you have only
one settings and they'll just work when you deploy your stuff.

Here at Yipit, we use Chef to coordinate the deploy process and to
maintain the configuration using attributes or data bags.

After that, we use [envdir](http://cr.yp.to/daemontools/envdir.html)
to run our applications with variables set in Chef. Then, we use
**milieu** to read those variables and feed the application
configuration system.

## Production

The system environment will be the first place **milieu** will try to find
things. So, when the application runs inside of an environment with the right
variables set, it will just work.

So, if you know you have the environment variable `DATABASE_URI` like this:

```bash
$ export DATABASE_URI=mysql://root@localhost:3306/mydb
```

The application settings glue code will look like this:

```python
# steadymark:ignore
>>> from milieu import Environment
>>> env = Environment()
>>> dburi = env.get_uri('DATABASE_URI')
>>> dburi.host
u'localhost'
>>> dburi.port
3306
```

## Local

If you just want to load things from a file cause it's local, the
`Environment.from_file()` constructor will help you out.

```python
# steadymark:ignore
>>> from milieu import Environment
>>> env = Environment.from_file('/etc/app.cfg')
>>> env.get_bool('BOOL_FLAG')
True
>>> env.get_float('FLOAT_VAL')
3.14
```

The file `app.cfg` will look like this:

```yaml
BOOL_FLAG: True

FLOAT_VAL: 3.14
```
