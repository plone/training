Creating your own eggs to customize Plone
=========================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -Rf src/ploneconf.site_sneak/chapters/12_eggs1/ src/ploneconf.site


Our own code has to be organised as an egg. An Egg is a zip file or a directory that follows certain conventions. We are going to use `ZopeSkel <https://pypi.python.org/pypi/ZopeSkel>`_ to create a skeleton projekt. We only need to fill the holes.

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

We anwser some questions:

* Enter project name: ``ploneconf.site``
* Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']: ``easy``
* Version (Version number for project) ['1.0']: ``1.0.0``
* Description (One-line description of the project) ['Example Dexterity Product']: ``PloneConf Site``
* Grok-Based? (True/False: Use grok conventions to simplify coding?) [True]: ``False``
* Use relations? (True/False: include support for relations?) [False]: ``True``

.. only:: manual

    If this is your first egg, this is a very special moment. We are going to create the egg with a script that generates a lot of necessary files. They all are necessary, but sometimes in a subtle way. It takes a while do understand their full meaning. Only last year I learnt and understood why I should have a manifest.in file. You can get along without one, but trust me, you get along better with a proper manifest file.

Lets have a look at some of it's files.

bootstrap.py, buildout.cfg, plone.cfg
    You can ignore these files for now. They are here to create a buildout only for this egg to make testing easier.

docs, README.txt
    The documentation and changelog of your egg goes in there

setup.py
    This file configures the package, it's name, dependencies and some metadata like the authors name. The dependencies listed here are automatically added by buildout.

ploneconf/site/configure.zcml
    The phone-book of the packages. By reading it you can find out which functionality is registered thoughthe component architecture.

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