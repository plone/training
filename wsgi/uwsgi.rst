uWSGI
=====

`uWSGI <https://uwsgi-docs.readthedocs.io/>`_ is a very flexible WSGI server that comes with tons of configuration options.
Only a few of them work with Zope and Plone, though.

Possible Worker models
----------------------

* synchronous threading
* asynchronous worker models
* worker processes

Using uWSGI in our buildout
---------------------------

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c uwsgi.cfg

Again we look into the `Plone Core Development Buildout <https://github.com/plone/buildout.coredev>`_ for how to use uWSGI in our buildout.
With 5 additional buildout parts things get even more complex than for gunicorn.
These parts are:

* `[wsgi.py]` providing the application entry point
* `[uwsgi]` and `[uwsgi-buildenv]` needed to build the uWSGI binary
* `[uwsgiini]` providing the `uwsgi.ini` file.
  The uWSGI `ini` configuration is different from the `PasteDeploy` configurations we have seen with other servers
* `[uwsgi-instance]` providing the actual startup script

.. code-block:: ini

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

Like with gunicorn in the previous chapter, we can start Plone behind uWSGI with the `uwsgi-instance` script:

.. code-block:: bash

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

As you can see the uWSGI output is pretty verbose.

Workers and ZODB connections
----------------------------

XXX tbd.
