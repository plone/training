---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Understanding the contents of `wsgi.ini`

The file `wsgi.ini` references the `zope.conf` file, `zope.conf` is passed as an argument to the WSGI application defined by the Zope package.

WSGI server configuration.

```ini
[server:main]
paste.server_factory = plone.recipe.zope2instance:main
use = egg:plone.recipe.zope2instance#main
listen = 0.0.0.0:8080
threads = 4
```

WSGI application configuration

```ini
[app:zope]
use = egg:Zope#main
zope_conf = /home/thomas/devel/plone/minimal52/parts/instance/etc/zope.conf
```

Paste Deploy's filters are a powerful concept for non-intrusively glueing middleware/infrastructure components together.

```ini
[filter:translogger]
use = egg:Paste#translogger
setup_console_handler = False

[filter:sentry]
use = egg:plone.recipe.zope2instance#sentry
dsn = https://3cfa2cdda6614de9966ce008416cae00@sentry.io/1537247
level = DEBUG
event_level = WARNING
ignorelist = waitress.queue
```

Applications and filters are combined in pipelines.

```ini
[pipeline:main]
pipeline =
    translogger
    egg:Zope#httpexceptions
    sentry
    zope
```

Following the pipeline section up to the end of the file is the logging configuration.
The logging configuration is passed to the standard libraries `logging.config` module and follows the [configuration file format described in the Python documentation](https://docs.python.org/3/library/logging.config.html#configuration-file-format).
The `handler_accesslog` and `handler_eventlog` sections configure the instance access and event log files, respectively.

```ini
[loggers]
keys = root, plone, waitress.queue, waitress, wsgi

[handlers]
keys = console, accesslog, eventlog

[formatters]
keys = generic, message

[logger_root]
level = INFO
handlers = console, eventlog

[logger_plone]
level = INFO
handlers = eventlog
qualname = plone

[logger_waitress.queue]
level = INFO
handlers = eventlog
qualname = waitress.queue
propagate = 0

[logger_waitress]
level = INFO
handlers = eventlog
qualname = waitress

[logger_wsgi]
level = INFO
handlers = accesslog
qualname = wsgi
propagate = 0

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[handler_accesslog]
class = FileHandler
args = ('/home/thomas/devel/plone/minimal52/var/log/instance-access.log','a')
level = INFO
formatter = message

[handler_eventlog]
class = FileHandler
args = ('/home/thomas/devel/plone/minimal52/var/log/instance.log', 'a')
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-7.7s [%(name)s:%(lineno)s][%(threadName)s] %(message)s

[formatter_message]
format = %(message)s
```

## The WSGI pipeline

- <https://github.com/plone/plone.recipe.zope2instance/issues/116>
