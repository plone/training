Creating addons to customize Plone
==================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -Rf src/ploneconf.site_sneak/chapters/12_eggs1/ src/ploneconf.site

Using zopeskel to create an egg
-------------------------------

Our own code has to be organised as an egg. An egg is a zip file or a directory that follows certain conventions. We are going to use `ZopeSkel <https://pypi.python.org/pypi/ZopeSkel>`_ to create a skeleton project. We only need to fill the holes.

.. note::

    In the training we use ZopeSkel 2.21.2, a relatively old version. We do this because this version is shipped with Plone's Unified Installer. In our own projects we mostly use `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ to create eggs.

We move to the ``src`` directory and call a script called ``zopeskel`` from our projects bin-directory.

.. code-block:: bash

    $ mkdir src
    $ cd src
    $ ../bin/zopeskel

This returns a list of available templates we might use. We choose dexerity since it is pretty small but already has some of the right dependencies we need.

.. code-block:: bash

    $ ../bin/zopeskel dexterity

We answer some questions:

* Enter project name: ``ploneconf.site``
* Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']: ``easy``
* Version (Version number for project) ['1.0']: ``1.0.0``
* Description (One-line description of the project) ['Example Dexterity Product']: ``PloneConf Site``
* Grok-Based? (True/False: Use grok conventions to simplify coding?) [True]: ``False``
* Use relations? (True/False: include support for relations?) [False]: ``True``

.. only:: not presentation

    If this is your first egg, this is a very special moment. We are going to create the egg with a script that generates a lot of necessary files. They all are necessary, but sometimes in a subtle way. It takes a while do understand their full meaning. Only last year I learnt and understood why I should have a ``manifest.in`` file. You can get along without one, but trust me, you get along better with a proper manifest file.

Inspecting the package
----------------------

Let's have a look at some of it's files.

bootstrap.py, buildout.cfg, plone.cfg
    You can ignore these files for now. They are here to create a buildout only for this egg to make testing easier. Once we start writing tests for this package we will have to update these files to the current best-practices and versions.

docs, README.txt
    The documentation and changelog of your egg goes in there

setup.py
    This file configures the package, it's name, dependencies and some metadata like the authors name. The dependencies listed here are automatically added by buildout.

ploneconf/site/configure.zcml
    The phone-book of the packages. By reading it you can find out which functionality is registered though the component architecture.

ploneconf/site/locales/
    This holds translation-files (see http://docs.plone.org/develop/plone/i18n/internationalisation.html). We won't use it during the training.

ploneconf/site/resources/
    A directory that holds static resources (images/css/js). They are accessible through URLs like ``++resource++ploneconf.site/myawesome.css``

ploneconf/site/profiles/default/
    The folder contains the GenericSetup-profile. During the training will put some xml-files there that hold configuration for the site.

ploneconf/site/profiles/default/metadata.xml
    Version-number and dependencies that are auto-installed.

    We could replace ``<dependency>profile-plone.app.dexterity:default</dependency>`` with ``<dependency>profile-plone.app.contenttypes:plone-content</dependency>`` to depend the addon we picked when creating our site with this egg.

ploneconf/site/profiles/default/types.xml
    Registration of types

There are also some files that can be deleted because they use outdated approaches to testing: ``ploneconf/site/tests.py`` and ``ploneconf/site/INTEGRATION.txt``.


Including the egg in Plone
--------------------------

Before we can use our new addon we have to tell Plone about it. Edit ``buildout.cfg`` and uncomment ``ploneconf.site`` in the `eggs` and `sources` sections:

.. code-block:: cfg
    :emphasize-lines: 4, 11

    eggs =
        Plone
        ...
        ploneconf.site
    #    starzel.votable_behavior

    ...

    [sources]
    collective.behavior.banner = git https://github.com/collective/collective.behavior.banner.git pushurl=git@github.com:collective/collective.behavior.banner.git rev=af2dc1f21b23270e4b8583cf04eb8e962ade4c4d
    ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site
    # starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git

This tells Buildout to add the egg ``ploneconf.site``. Since it is also in the `sources`-section Buildout will not try to download it from pypi but will expect it in ``src/ploneconf.site``. *fs* allows you to add packages on the filesystem without a version control system, or with an unsupported one.

Now run buildout to reconfigure Plone with the updated configuration:

.. code-block:: bash

    $ ./bin/buildout

After restarting Plone with ``./bin/instance fg`` the new addon `ploneconf.site` is available for install like PloneFormGen or Plone True Gallery.

We will not install it now since we did not add any of our own code or configuration yet. Instead we will first create a new content-type through the web. We will then export it and add it as code to the egg. This way the content-type will be available for everyone who installs our addon.

