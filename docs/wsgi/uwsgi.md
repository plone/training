---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# uWSGI

[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) is a very flexible WSGI server that comes with tons of configuration options.
Only a few of them work with Zope and Plone, though.

## Possible Worker models

- synchronous threading
- asynchronous worker models
- worker processes

## Using uWSGI in our buildout

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c uwsgi.cfg
```
````

Again we look into the [Plone Core Development Buildout](https://github.com/plone/buildout.coredev) for how to use uWSGI in our buildout.
With 5 additional buildout parts things get even more complex than for gunicorn.
These parts are:

- `[wsgi.py]` providing the application entry point
- `[uwsgi]` and `[uwsgi-buildenv]` needed to build the uWSGI binary
- `[uwsgiini]` providing the `uwsgi.ini` file.
  The uWSGI `ini` configuration is different from the PasteDeploy configurations we have seen with other servers
- `[uwsgi-instance]` providing the actual startup script

```ini
...
[wsgi.py]
recipe = zc.recipe.egg
eggs =
    ${instance:eggs}
scripts =
    wsgi.py
interpreter =
    wsgi.py
initialization =
    from Zope2.Startup.run import make_wsgi_app;
    wsgiapp = make_wsgi_app({}, '${buildout:parts-directory}/instance/etc/zope.conf')
    def application(*args, **kwargs):return wsgiapp(*args, **kwargs)

[uwsgi]
recipe = zc.recipe.egg
environment = uwsgi-buildenv
eggs =
    greenlet
    uwsgi
    ${instance:eggs}
scripts =
    uwsgi

[uwsgi-buildenv]
UWSGI_PROFILE="asyncio"

[uwsgiini]
recipe = collective.recipe.template
input = inline:
    [uwsgi]
    http-socket = 0.0.0.0:8080
    socket = 127.0.0.1:8081
    chdir  = ${buildout:directory}/bin
    module = wsgi:application
    # s. https://github.com/zopefoundation/Zope/issues/283, https://github.com/zopefoundation/Zope/issues/284
    master = false
    enable-threads = true
    processes = 1
    threads = 4
    #asyncio = 4
    #greenlet = true
output = ${buildout:directory}/etc/uwsgi.ini

[uwsgi-instance]
recipe = collective.recipe.template
input = inline:
    #!/bin/sh
    ${buildout:directory}/bin/uwsgi --ini ${buildout:directory}/etc/uwsgi.ini
output = ${buildout:bin-directory}/uwsgi-instance
mode = 755
```

Like with gunicorn in the previous chapter, we can start Plone behind uWSGI with the `uwsgi-instance` script:

```shell
(wsgitraining) $ bin/uwsgi-instance
[uWSGI] getting INI configuration from /vagrant/wsgitraining/etc/uwsgi.ini
*** Starting uWSGI 2.0.18 (64bit) on [Tue Oct  1 13:50:21 2019] ***
compiled with version: 7.4.0 on 01 October 2019 13:25:29
os: Linux-4.15.0-64-generic #73-Ubuntu SMP Thu Sep 12 13:16:13 UTC 2019
nodename: training
machine: x86_64
clock source: unix
pcre jit disabled
detected number of CPU cores: 2
current working directory: /vagrant/wsgitraining
detected binary path: /vagrant/wsgitraining/bin/uwsgi
chdir() to /vagrant/wsgitraining/bin
*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 5855
your memory page size is 4096 bytes
detected max file descriptor number: 1024
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
uwsgi socket 0 bound to TCP address 0.0.0.0:8080 fd 3
uwsgi socket 1 bound to TCP address 127.0.0.1:8081 fd 4
Python version: 3.7.3 (default, Apr  3 2019, 19:16:38)  [GCC 8.0.1 20180414 (experimental) [trunk revision 259383]]
Python main interpreter initialized at 0x55cbb37e2810
python threads support enabled
your server socket listen backlog is limited to 100 connections
your mercy for graceful operations on workers is 60 seconds
mapped 104288 bytes (101 KB) for 4 cores
*** Operational MODE: threaded ***
...
```

As you can see the uWSGI output is pretty verbose.

### Exercise 1

Benchmark the front page of your setup with two different tools: [siege](https://github.com/JoeDog/siege/) and [wrk](https://github.com/wg/wrk).
You will probably find a package for your Linux distribution for at least siege.
If so, use the distribution package, otherwise follow the official installation instructions.

For both tools we use 100 concurrent connections and 100 seconds of test duration.
For siege, the command line looks like this:

```shell
$ siege -c 100 -t 100s http://localhost:8080/Plone
```

For wrk, use:

```shell
$ wrk -c 100 -d 100s -t 1 --timeout 300s --latency http://localhost:8080/Plone
```

Note that siege always uses a single thread to execute the test.
For wrk, you can specify the number of threads to use with the `-t` option.

Record and discuss the results.

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

tbd.
```

## Using uWSGI Emperor from the distribution

For managing multi-app deployment uWSGI comes with a special feature called Emperor mode.
It is supported by many Linux distributions and also by Ubuntu.
It is controlled by the systemd service manager and can replace supervisor or a generic systemd configuration for Plone.
We want to turn our uWSGI based Plone setup into one that is controlled by the distro's uWSGI Emperor.
To get there, we need to consider a couple of things.
uWSGI uses a plugin based approach to support different programming languages.
It comes with both Python version 2 and 3 plugins.
However the distro's uWSGI Python plugins will match the distro's main Python versions, so for the Python 3 plugin this is Python 3.6 for Ubuntu Bionic.
If we used a different Python version, we have two choices:

- Create a new virtualenv with the main system Python 3 and rerun buildout
- Recompile uWSGIs Python 3 plugin so it matches the Python version we are currently using

Although the first approach has the important advantage that we retain the possibility to obtain updates and security fixes from the distribution, we will go for the second here because it looks more interesting.
We will roughly follow [this blog post](https://www.paulox.net/2019/03/13/how-to-use-uwsgi-with-python-3-7-in-ubuntu-18-x/).

Let's first install the necessary packages:

```shell
$ sudo apt install uwsgi-emperor python3-distutils uwsgi-src uuid-dev libcap-dev libpcre3-dev
```

Next we will rebuild uWSGI's Python 3 plugin (and change to a temporary location before doing so):

```shell
$ cd /tmp
$ PYTHON=python3.7 uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python37"
```

Then we move the plugin to the location where uWSGI expects to find its plugins:

```shell
$ sudo mv python37_plugin.so /usr/lib/uwsgi/plugins/python37_plugin.so
$ sudo chmod 644 /usr/lib/uwsgi/plugins/python37_plugin.so
```

Note that we are not replacing the existing Python 3 plugin, but we add a new one specifically for Python 3.7.
We can check the Python version of our new plugin:

```shell
$ uwsgi --plugin python37 -s :0
...
Python version: 3.7.3 (default, Apr  3 2019, 19:16:38)  [GCC 8.0.1 20180414 (experimental) [trunk revision 259383]]
...
```

So now we got a running Plone uWSGI setup and a matching Python 3 plugin.
What is left to do is to setup a Plone vassal for the uWSGI emperor.
You can find general information on this topic in the official [uWSGI documentation](https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html).
By default, Ubuntu's uWSGI emperor will run under user/group id `www-data` and it will use these settings for its vassals.
However Plone needs to be able to write to the filesystem e.g. for caching and creating compiled files, so we want it to run under the user id we used for running buildout (probably your user name for a local installation or `vagrant`).
uWSGI emperor comes with a so called "tyrant mode" for secure multi-user hosting to achieve this, and we go for the [paranoid sysadmins](https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html#tyrant-mode-for-paranoid-sysadmins-linux-only) variant here.
POSIX capabilities are enabled in Ubuntu's uWSGI by default, so we only need to add two lines to `/etc/uwsgi-emperor/emperor.ini` to enable tyrant mode:

```{code-block} ini
:emphasize-lines: 25,26

# try to autoload appropriate plugin if "unknown" option has been specified
autoload = true

# enable master process manager
master = true

# spawn 2 uWSGI emperor worker processes
workers = 2

# automatically kill workers on master's death
no-orphans = true

# place timestamps into log
log-date = true

# user identifier of uWSGI processes
uid = www-data

# group identifier of uWSGI processes
gid = www-data

# vassals directory
emperor = /etc/uwsgi-emperor/vassals

emperor-tyrant = true
cap = setgid,setuid
```

We also need to create a vassal configuration for Plone.
It will go to `/etc/uwsgi-emperor/vassals/plone.ini` and its contents are:

```ini
[uwsgi]
uid = vagrant
gid = vagrant
http-socket = 0.0.0.0:8080
socket = 127.0.0.1:8081
plugins = python37
virtualenv = /vagrant/wsgitraining
wsgi-file = /vagrant/wsgitraining/bin/wsgi.py
master = false
enable-threads = true
processes = 1
threads = 4
```

The important (and not quite obvious from the docs, see this [mail post](https://web.archive.org/web/20190905042643/http://lists.unbit.it/pipermail/uwsgi/2015-March/007918.html)) thing to note here as that this file must be owned by the same user we intend to use for running the vassal:

```shell
sudo chown vagrant.vagrant /etc/uwsgi-emperor/vassals/plone.ini
```

The final step is to restart the uWSGI emperor `systemd` service (make sure you have a running ZEO server before this):

```ini
$ sudo service uwsgi-emperor restart
```

We can then use `sudo tail -f /var/log/uwsgi/emperor.log` to see what is going on.

### Exercise 2

Change the Plone vassal configuration so that it uses its own logfile.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

You will first need to add the logfile location to `/etc/uwsgi/vassals/plone.ini`:

```{code-block} ini
:emphasize-lines: 13

[uwsgi]
uid = vagrant
gid = vagrant
http-socket = 0.0.0.0:8080
socket = 127.0.0.1:8081
plugins = python37
virtualenv = /vagrant/wsgitraining
wsgi-file = /vagrant/wsgitraining/bin/wsgi.py
master = false
enable-threads = true
processes = 1
threads = 4
daemonize = /var/log/uwsgi/plone.log
```

The tricky part however is to get the file permissions right.
By default, only root is allowed to write to `/var/log/uwsgi`, but the vassal is running as `vagrant.vagrant`.
We resolve to changing the group ownership for `/var/log/uwsgi` and giving the group write access:

```shell
$ sudo chgrp vagrant /var/log/uwsgi
$ sudo chmod g+w /var/log/uwsgi
$ ls -ld /var/log/uwsgi
drwxrwxr-x 2 root vagrant 4096 Oct  2 09:51 /var/log/uwsgi
```

Alternatively we could of course write the logfile to a different location, e.g. `${buildout:directory}/var/log`.
````
