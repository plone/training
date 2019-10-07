.. _prz-label:

Deploying Plone with WSGI using zc.buildout, plone.recipe.zope2instance and Waitress
====================================================================================

The `plone.recipe.zope2instance` creates and configures a Zope instance in a buildout part.
In order to provide a smooth transition to Plone 5.2 and WSGI it tries to guess sensible defaults.
The goal when providing WSGI support in `plone.recipe.zope2instance` was to keep the buildout configuration close to the ZServer configuration.
Many options formerly used for ZServer are working in pretty much the same way for WSGI.
WSGI is the default in recent `plone.recipe.zope2instance` versions.
It can be overriden by ZServer for Python 2.
`Waitress <https://docs.pylonsproject.org/projects/waitress/en/stable>`_ is the default WSGI server configured by `plone.recipe.zope2instance`.
Waitress is a pure Python WSGI server implementation originating from the Pylons project.

.. note::

    XXX Maybe explain general idea and purpose of the plone.recipe.zope2instance with respect to the changes introduced for WSGI.

With this information in mind, creating a minimial WSGI buildout for Plone is fairly easy.
A working example is contained in `basic.cfg` in the training buildout, here are the file contents:

.. code-block:: ini

    [buildout]
    extensions = mr.developer
    parts = instance
    extends = https://dist.plone.org/release/5.2-latest/versions.cfg
    auto-checkout =
        plone.recipe.zope2instance
        wsgitraining.site
    sources = sources

    [sources]
    plone.recipe.zope2instance = git https://github.com/plone/plone.recipe.zope2instance.git
    wsgitraining.site = fs wsgitraining.site

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    eggs =
        Plone
        Pillow
        wsgitraining.site

As you can see, we are using a custom addon named `wsgitraining.site` contained in the buildout.
We will not use the addon immediately so you don't need to activate it yet.
We use `mr.developer` to checkout the source code of this addon.
We also use a source checkout of the `plone.recipe.zope2instance` buildout recipe to get the latest (maybe not yet released on PyPI) functionality for this training.

As a first exercise in this training run the above buildout configuration from the command line:

Activate your virtualenv if you haven't done so already:

.. code-block:: bash

    ~/plone52$ . bin/activate

Run buildout:

.. code-block:: bash

    (plone52) ~/plone52$ buildout -c basic.cfg

After a successful buildout, you can start Plone in the foreground as usual.
Start `zeo` first:

.. code-block:: bash

    (wsgitraining) $ bin/zeo start

Then start the application server:

.. code:: bash

    (plone52) ~/plone52$ bin/instance fg

You can then create a Plone instance by pointing your browser to `http://localhost:8080`.
