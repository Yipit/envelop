A helper for storing more complex variables using the system environment.

## It's easy to use and to save some typing

```python
>>> from envparse import Environment
>>> env = Environment()
>>> env.set('myurl', 'http://gnu.org')
>>> env.get_uri('myurl').host
u'gnu.org'
```

## Just a proxy to the real environment

```python
>>> import os
>>> from envparse import Environment
>>> env = Environment()
>>> env.set('myurl', 'http://gnu.org')
>>> os.environ['myurl'] == 'http://gnu.org'
True
>>> os.environ['fsf'] = 'http://fsf.org'
>>> env.get('fsf') == 'http://fsf.org'
True
```
