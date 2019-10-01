Bjoern
======

`bjoern <https://github.com/jonashaag/bjoern>`_ is a fast And ultra-lightweight HTTP/1.1 WSGI Server for CPython2 and 3 written in C.
It claims to be the fastest, smallest and most lightweight WSGI server.
Features:

* ~ 1000 lines of C code
* Memory footprint ~ 600KB
* supports Python 2 and 3
* Single-threaded
* supports TCP `host:port` addresses and Unix sockets
* Full persistent connection ("*keep-alive*") support in both HTTP/1.0 and 1.1,
  including support for HTTP/1.1 chunked responses

.. note::

    In a load test involving `bjoern`, `cheroot`, `gunicorn`, `waitress` and `werkzeug` ``bjoern`` (version: 3.0.0) was the clear speed winner against both a ZEO and a non-ZEO Zope instance.
    Source: Zope/docs/wsgi.rst:

Prerequisites
-------------

Bjoern uses libev and you will need to install both the library and the development header files on your box:

.. code-block:: bash

    $ sudo apt install libev-dev

Use bjoern in our buildout
--------------------------

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c bjoern.cfg

`bjoern <https://github.com/jonashaag/bjoern>`_ can be integrated using a shim package called `dataflake.wsgi.bjoern <https://dataflakewsgibjoern.readthedocs.io/>`_.

You can use this package together with `plone.recipe.zope2instance` to build a bjoern based wSGI setup:

.. code-block:: ini

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    zeo-client = on
    zeo-address = 8100
    shared-blob = on
    blob-storage = ${buildout:directory}/var/blobstorage
    eggs =
        Plone
        Pillow
        wsgitraining.site
        dataflake.wsgi.bjoern
    wsgi-ini-template = ${buildout:directory}/templates/bjoern.ini.in

In addition to adding `dataflake.wsgi.bjoern` to the `eggs` list we specify the location of our `bjoern.ini` configuration file.
It is important to note that this file is not automatically created for us, we have to provide it ourself.

In addition to the PasteDeploy entry point and the p.r.zope2instance integration, `dataflake.wsgi.bjoern`  provides facilities to create a set of Zope configuration files for bjoern with the included `mkbjoerninstance` utility.
We will however not use this option since it is easier for us to provide a custom template for the `wsgi.ini` file to `plone.recipe.zope2instance`.
A suitable template is included in the buildout for the training (file `bjoern.ini.in` in the `templates` folder).
It is basically a copy from the template contained in the buildout recipe with a slightly changed `[server:main]` section:

.. code-block:: ini

    [server:main]
    use = egg:dataflake.wsgi.bjoern#main
    listen = %(http_address)s
    reuse_port = True
    ...

.. note::

    Let's run some checks in order to verify that `bin/instance` actually invokes bjoern:
    Let's first find the processes' PID:

    .. code-block:: console

        $ ps -ef | grep wsgi.ini
        thomas   20009 20006  0 10:26 pts/1    00:00:22 /home/thomas/devel/plone/minimal52/bin/python /home/thomas/devel/plone/minimal52/parts/instance/bin/interpreter /home/thomas/.buildout/eggs/cp37m/Zope-4.1.1-py3.7.egg/Zope2/Startup/serve.py /home/thomas/devel/plone/minimal52/parts/instance/etc/wsgi.ini -d debug-mode=on
        ...

    Using the above PID  we can check the process map to see whether bjoern's C extension has been loaded:

    .. code-block:: console

        thomas@blake:~$ pmap 17245 | grep bjoern
        17245:   /home/thomas/devel/plone/minimal52/bin/python /home/thomas/devel/plone/minimal52/parts/instance/bin/interpreter /home/thomas/.buildout/eggs/cp37m/Zope-4.1.1-py3.7.egg/Zope2/Startup/serve.py /home/thomas/devel/plone/minimal52/etc/bjoern.ini -d debug-mode=on
        00007f7537fa5000     44K r-x-- _bjoern.cpython-37m-x86_64-linux-gnu.so
        00007f7537fb0000   2048K ----- _bjoern.cpython-37m-x86_64-linux-gnu.so
        00007f75381b0000      4K r---- _bjoern.cpython-37m-x86_64-linux-gnu.so
        00007f75381b1000      4K rw--- _bjoern.cpython-37m-x86_64-linux-gnu.so
