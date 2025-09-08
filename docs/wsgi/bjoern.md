---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# `Bjoern`

[bjoern](https://github.com/jonashaag/bjoern) is an HTTP/1.1 WSGI Server for CPython2 and 3 written in C.
It claims to be the fastest, smallest and most lightweight WSGI server.

```{note}
In a [load test](https://zope.readthedocs.io/en/latest/operation.html#test-criteria-for-recommendations) involving `bjoern`, `cheroot`, `gunicorn`, `waitress` and  `werkzeug`, `bjoern` (version: 3.0.0) was the clear speed winner against both a ZEO and a non-ZEO Zope instance.
```

## Prerequisites

`Bjoern` uses `libev` and you will need to install both the library and the development header files on your box:

```shell
$ sudo apt install libev-dev
```

## Use `bjoern` in our buildout

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c bjoern.cfg
```
````

[bjoern](https://github.com/jonashaag/bjoern) can be integrated using a shim package called [dataflake.wsgi.bjoern](https://dataflakewsgibjoern.readthedocs.io/en/latest/).

You can use this package together with `plone.recipe.zope2instance` to build a `bjoern` based WSGI setup:

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
    dataflake.wsgi.bjoern
wsgi-ini-template = ${buildout:directory}/templates/bjoern.ini.in
```

In addition to adding `dataflake.wsgi.bjoern` to the `eggs` list we specify the location of our `bjoern.ini` configuration file.
Note that this file is not automatically created for us, we have to provide it ourself.

In addition to the PasteDeploy entry point and the p.r.zope2instance integration, `dataflake.wsgi.bjoern`  provides facilities to create a set of Zope configuration files for `bjoern` with the included `kbjoerninstance` utility.
We will however not use this option since it is easier to provide a custom template for the `wsgi.ini` file to `plone.recipe.zope2instance`.
A suitable template is included in the buildout for the training (file `bjoern.ini.in` in the `templates` folder).
It is basically a copy from the template contained in the buildout recipe with a slightly changed `[server:main]` section:

```ini
[server:main]
use = egg:dataflake.wsgi.bjoern#main
listen = %(http_address)s
reuse_port = True
```

````{note}
Let's run some checks in order to verify that `bin/instance` actually invokes bjoern:
Let's first find the processes' PID:

```console
$ ps -ef | grep wsgi.ini
thomas   20009 20006  0 10:26 pts/1    00:00:22 /home/thomas/devel/plone/minimal52/bin/python /home/thomas/devel/plone/minimal52/parts/instance/bin/interpreter /home/thomas/.buildout/eggs/cp37m/Zope-4.1.1-py3.7.egg/Zope2/Startup/serve.py /home/thomas/devel/plone/minimal52/parts/instance/etc/wsgi.ini -d debug-mode=on
```

Using the above PID  we can check the process map to see whether bjoern's C extension has been loaded:

```console
thomas@blake:~$ pmap 17245 | grep bjoern
17245:   /home/thomas/devel/plone/minimal52/bin/python /home/thomas/devel/plone/minimal52/parts/instance/bin/interpreter /home/thomas/.buildout/eggs/cp37m/Zope-4.1.1-py3.7.egg/Zope2/Startup/serve.py /home/thomas/devel/plone/minimal52/etc/bjoern.ini -d debug-mode=on
00007f7537fa5000     44K r-x-- _bjoern.cpython-37m-x86_64-linux-gnu.so
00007f7537fb0000   2048K ----- _bjoern.cpython-37m-x86_64-linux-gnu.so
00007f75381b0000      4K r---- _bjoern.cpython-37m-x86_64-linux-gnu.so
00007f75381b1000      4K rw--- _bjoern.cpython-37m-x86_64-linux-gnu.so
```
````

### Exercise 1

Additional PasteDeploy entrypoints are available for the [werkzeug entrypoints](https://pypi.org/project/dataflake.wsgi.werkzeug) and [cheroot entrypoints](https://pypi.org/project/dataflake.wsgi.cheroot) WSGI servers.
Pick one and use it to run Plone behind [werkzeug](https://palletsprojects.com/p/werkzeug/) or [cheroot](https://cheroot.cherrypy.dev/en/latest/).

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

**cheroot:**

You will need to create two files, an `.ini` template and the buildout configuration.
As a starting point, copy `bjoern.cfg` to `cheroot.cfg` and `templates/bjoern.ini.in` to `templates/cheroot.ini.in` in your buildout directory:

```shell
$ cp bjoern.cfg cheroot.cfg
$ cp templates/bjoern.ini.in templates/cheroot.ini.in
```

Then edit the files so they pull in `cheroot` as WSGI server rather than bjoern.
`cheroot.cfg`:

```{code-block} ini
:emphasize-lines: 11-12

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
    dataflake.wsgi.cheroot
wsgi-ini-template = ${buildout:directory}/templates/cheroot.ini.in
```

And `templates/cheroot.ini.in`:

```{code-block} ini
:emphasize-lines: 1-4

[server:main]
use = egg:dataflake.wsgi.cheroot#main
host = localhost
port = 8080

[app:zope]
```

Note that the `dataflake.wsgi.cheroot` shim doesn't understand either `reuse_port` nor `listen`.
This means we cannot use the `http-address` parameter passed by `plone.recipe.zope2instance`.
We resolve to specifying host and port in the template instead.
`dataflake.wsgi.cheroot` accepts a couple of other options in the `.ini` file that we will not consider for this exercise.

Next run buildout with the new configuration:

```shell
(wsgitraining) $ buildout -c cheroot.cfg
```

You can now start your instance as usual:

```shell
(wsgitraining) $ bin/instance fg
2019-10-07 12:43:08,856 INFO    [Zope:45][MainThread] Ready to handle requests
Starting server in PID 3906.
```

**werkzeug:**

For `werkzeug` the steps are pretty much the same.
Copy the configuration files:

```shell
$ cp bjoern.cfg werkzeug.cfg
$ cp templates/bjoern.ini.in templates/werkzeig.ini.in
```

Edit them.
`werkzeug.cfg`:

```{code-block} ini
:emphasize-lines: 11-12

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
    dataflake.wsgi.werkzeug
wsgi-ini-template = ${buildout:directory}/templates/werkzeug.ini.in
```

`templates/werkzeug.ini.in`:

```{code-block} ini
:emphasize-lines: 1-4

[server:main]
use = egg:dataflake.wsgi.werkzeug#main
host = localhost
port = 8080

[app:zope]
```

After running `buildout -c werkzeug.cfg` you can start your Plone instance:

```shell
(wsgitraining) $ bin/instance fg
2019-10-07 12:58:54,660 INFO    [Zope:45][MainThread] Ready to handle requests
Starting server in PID 4337.
2019-10-07 12:58:54,661 INFO    [werkzeug:122][MainThread]  * Running on http://localhost:8080/ (Press CTRL+C to quit)
```

Like the `cheroot` shim, `dataflake.wsgi.werkzeug` accepts a couple of additional options in the `.ini` file that we will not use here.
````
