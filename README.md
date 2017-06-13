A helping hand to manage your settings among different environments

## Intro

Managing application configuration that runs on multiple environments
can be tough. So, **envelop** comes to help you pretend you have only one
settings file that magically works whenever you deploy.

Here at Yipit, we use Chef to coordinate the deploy process and to maintain the
configuration, using attributes or data bags.

After that, we use [envdir](http://cr.yp.to/daemontools/envdir.html)
to run our applications with variables set in Chef. Then, we use
**envelop** to read those variables and feed the application configuration
system.

## Production

The system environment is the first place **envelop** will try to find
things. So, when the application runs inside of an environment with the right
variables set, it will just work.

So, if you know you have environment variables
`DATABASE_URI` and `ALLOWED_IPS` like this:

```bash
$ export DATABASE_URI=mysql://root@localhost:3306/mydb
$ export ALLOWED_IPS=10.0.0.1,10.0.0.2
```

The application settings glue code will look like this:

```python
>>> from envelop import Environment
>>> env = Environment()
>>> dburi = env.get_uri('DATABASE_URI')
>>> dburi.host
u'localhost'
>>> dburi.port
3306
>>> env.get_list('ALLOWED_IPS')
['10.0.0.1', '10.0.0.2']
```

## Local

If you just want to load things from a file locally, the
`Environment.from_file()` constructor will help you out.

```python
>>> from envelop import Environment
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

## From a folder

You can also load variables from a folder, where each file will be an
environment variable and the file's content will be the value. Just like
[envdir](http://cr.yp.to/daemontools/envdir.html).

Now, say that you have the folder `/etc/envdir/app` and this folder contains
the file `MYSQL_CONN_URI` with a database URL inside of it. Just like this one
here: `mysql://root:secret@localhost:3306/mydb`.

To read that directory and load the variable properly, you just have to do the
following:

```python
>>> from envelop import Environment
>>> env = Environment.from_folder('/etc/envdir/app')
>>> uri = env.get_uri('MYSQL_CONN_URI')
>>> uri.host
'localhost'
>>> uri.port
3306
>>> uri.user
'root'
>>> uri.password
'secret'
```

# Hacking on it

## Install dev dependencies

```console
pip install -r requirements-dev.txt
```

## Run tests

```console
make test
```

## Change it

Make sure you write tests for your new features and keep the test coverage in 100%

## Release it

After you already made your commits, run:

```console
make release
```

follow the instructions and do the [harlem shake](http://www.youtube.com/watch?v=8vJiSSAMNWw)


## Project history

This project was started by [Lincoln de Sousa](https://github.com/clarete) and was called ["Milieu"](https://github.com/clarete/milieu). We renamed it to "Envelop" on May 21st, 2014.
