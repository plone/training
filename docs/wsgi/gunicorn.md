---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Gunicorn

[Gunicorn](https://gunicorn.org/) is another widely used WSGI server.

## Possible Worker models

Gunicorn offers a wide range of possible worker models.
The default is the `sync` worker model which uses "traditional" multi-threading based on the standard library.
Unlike waitress Gunicorn doesn't use an `asyncore` dispatcher to clear the request queue.
Each worker is using [select](https://github.com/benoitc/gunicorn/blob/e147feaf8b12267ff9bb3c06ad45a2738a4027df/gunicorn/workers/sync.py#L34) by itself to check for incoming client requests.
The official [Gunicorn documentation for worker types](https://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type) recommends to put a buffering proxy in front of a default configuration Gunicorn.

Other possible worker types are asynchronous workers based on [greenlets](https://greenlet.readthedocs.io/en/latest/), [AsyncIO](https://docs.python.org/3/library/asyncio.html#module-asyncio) workers and a [Tornado](https://www.tornadoweb.org/en/stable/) worker class.
The different worker types and how to choose one suitable for your application is covered in detail in the [Gunicorn docs](https://docs.gunicorn.org/en/latest/design.html).

## Use gunicorn in our buildout

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c gunicorn.cfg
```
````

Gunicorn has a built-in PasteDeploy entry point, so we don't need a shim package like the one we used for `bjoern`.
On the downside, there is no easy way of passing `plone.recipe.zope2instances http-address` parameter to gunicorn since the `bind` directive doesn't seem to work in the `ini` file.
The PasteDeploy entry point is covered in the [gunicorn configuration documentation](https://docs.gunicorn.org/en/stable/configure.html).

We resolve to hard code the socket in the `ini` template.

From `templates/gunicorn.ini.in`:

```ini
[server:main]
use = egg:gunicorn#main
host = 0.0.0.0
port = 8080
proc_name = plone

[app:zope]
use = egg:Zope#main
...
```

We use this template in our buildout and add `gunicorn` to our list of eggs:

```ini
[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
zeo-client = on
zeo-address = 8100
shared-blob = on
blob-storage = ${buildout:directory}/var/blobstorage
eggs =
    Plone
    wsgitraining.site
    gunicorn
wsgi-ini-template = ${buildout:directory}/templates/gunicorn.ini.in
```

## Alternative method for using gunicorn

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c gunicorn-alt.cfg
```
````

An alternative method for using gunicorn with Plone is taken from the [Plone Core Development Buildout](https://github.com/plone/buildout.coredev) bypasses `plone.recipe.zope2instances` wsgi-ini-template option and builds three more parts instead.
These parts are working together to create the gunicorn configuration and startup scripts.
We do not use an `ini` template in this case but rather use inline templates to render the gunicorn command line and the WSGI application entry point in two scripts:

```ini
[buildout]
extends = base.cfg
parts +=
    gunicorn
    gunicornapp
    gunicorn-instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
zeo-client = on
zeo-address = 8100
shared-blob = on
blob-storage = ${buildout:directory}/var/blobstorage
eggs =
    Plone
    wsgitraining.site

[gunicornapp]
recipe = collective.recipe.template
input = inline:
    from Zope2.Startup.run import make_wsgi_app
    wsgiapp = make_wsgi_app({}, '${buildout:parts-directory}/instance/etc/zope.conf')
    def application(*args, **kwargs):return wsgiapp(*args, **kwargs)
output = ${buildout:bin-directory}/gunicornapp.py

[gunicorn]
recipe = zc.recipe.egg
eggs =
    gunicorn
    ${instance:eggs}
scripts =
    gunicorn

[gunicorn-instance]
recipe = collective.recipe.template
input = inline:
    #!/bin/sh
    ${buildout:directory}/bin/gunicorn -b localhost:8080 --threads 4 gunicornapp:application
output = ${buildout:bin-directory}/gunicorn-instance
mode = 755
```

Note that in this case we still create the default instance (using waitress).
But for starting up Plone with gunicorn we use the new `gunicorn-instance` script instead, without any parameters:

```shell
(wsgitraining) $ bin/gunicorn-instance
[2019-10-01 11:55:41 +0200] [11048] [INFO] Starting gunicorn 19.9.0
[2019-10-01 11:55:41 +0200] [11048] [INFO] Listening at: http://127.0.0.1:8080 (11048)
[2019-10-01 11:55:41 +0200] [11048] [INFO] Using worker: threads
[2019-10-01 11:55:41 +0200] [11051] [INFO] Booting worker with pid: 11051
```

As a side effect we get rid of the deprecation warning for not starting gunicorn with `--paste`.

```{note}
The Zope documentations reports several performance issues with gunicorn, s. <https://zope.readthedocs.io/en/latest/operation.html#test-criteria-for-recommendations> for details.
```

### Exercise 1

Modify `gunicorn-alt.cfg` so it uses the `eventlet` worker class. Check the number of database connections in the ZMI. What do you notice?

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

You need to add `eventlet` to the list of eggs of the `[gunicorn]` part and modify the command line for `[gunicorn-instance]`

```{code-block} ini
:emphasize-lines: 6,15

...
[gunicorn]
recipe = zc.recipe.egg
eggs =
    gunicorn
    eventlet
    ${instance:eggs}
scripts =
    gunicorn

[gunicorn-instance]
recipe = collective.recipe.template
input = inline:
    #!/bin/sh
    ${buildout:directory}/bin/gunicorn -b localhost:8080 --workers 4 gunicornapp:application --worker-class eventlet
output = ${buildout:bin-directory}/gunicorn-instance
mode = 755
...
```

After running `buildout -c gunicorn-alt.cfg`, you can start the instance with `gunicorn-instance`.

Open the [database controlpanel](http://localhost:8080/Control_Panel/Database/main/manage_main) in a browser to check the number of database connection. You will see only one connection despite the 4 workers.
ZODB connections are [not thread safe](https://zodb.org/en/latest/guide/transactions-and-threading.html#concurrency-threads-and-processes) so this is not a recommended configuration.
The [asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio) based `gthread` worker class (doesn't need additional packages) will show one database connection per worker.
````
