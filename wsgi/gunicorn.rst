Gunicorn
========

Gunicorn is another widely used WSGI server.

Possible Worker models
----------------------

* synchronous threading
* asynchronous worker models

XXX tbd

Use gunicorn in our buildout
----------------------------

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c gunicorn.cfg

The `gunicorn WSGI server <https://gunicorn.org/>`_ has a built-in `PasteDeploy` entry point, so we don't need a shim package like the one we used for `bjoern`.
On the downside, there is no easy way of passing `plone.recipe.zope2instance`s `http-address` parameter to gunicorn since the `bind` directive doesn't seem to work in the `ini` file.
The PasteDeploy entry point is covered in the `gunicorn documentation <http://docs.gunicorn.org/en/stable/configure.html>`_.

We resolve to hard code the socket in the `ini` template.

From `templates/gunicorn.ini.in`:

.. code-block:: ini

    [server:main]
    use = egg:gunicorn#main
    host = 0.0.0.0
    port = 8080
    proc_name = plone

    [app:zope]
    use = egg:Zope#main
    ...

We use this template in our buildout and add `gunicorn` to our list of eggs:

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
        gunicorn
    wsgi-ini-template = ${buildout:directory}/templates/gunicorn.ini.in

Alternative method for using gunicorn
-------------------------------------

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c gunicorn-alt.cfg

An alternative method for using gunicorn with Plone is taken from the `Plone Core Development Buildout <https://github.com/plone/buildout.coredev>`_ bypasses `plone.recipe.zope2instances` wsgi-ini-template option and builds three more parts instead.
These parts are working together to create the gunicorn configuration and startup scripts.
We do not use an `ini` template in this case but rather use inline templates to render the gunicorn command line and the WSGI application entry point in two scripts:

.. code-block:: ini

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
        Pillow
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

Note that in this case we still create the default instance (using waitress).
But for starting up Plone with gunicorn we use the new `gunicorn-instance` script instead, without any parameters:

.. code-block:: bash

    (wsgitraining) $ bin/gunicorn-instance
    [2019-10-01 11:55:41 +0200] [11048] [INFO] Starting gunicorn 19.9.0
    [2019-10-01 11:55:41 +0200] [11048] [INFO] Listening at: http://127.0.0.1:8080 (11048)
    [2019-10-01 11:55:41 +0200] [11048] [INFO] Using worker: threads
    [2019-10-01 11:55:41 +0200] [11051] [INFO] Booting worker with pid: 11051

As a side effect we get rid of the deprecation warning for not starting gunicorn with `--paste`.

.. note::

    The Zope documentations reports several performance issues with gunicorn, s. https://zope.readthedocs.io/en/latest/wsgi.html#test-criteria-for-recommendations for details.
