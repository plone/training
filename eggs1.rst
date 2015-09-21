.. _eggs1-label:

Write Your Own Add-Ons to Customize Plone
=========================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/01_eggs1_p5/ src/ploneconf.site

.. _eggs1-create-label:


In this part you will:

* Create a custom python package ``ploneconf.site`` to hold all the code
* Modify buildout to install that package


Topics covered:

* mr.bob and bobtemplates.plone
* the structure of eggs


Creating the package
--------------------

Our own code has to be organised as a python package, also called *egg*. An egg is a zip file or a directory that follows certain conventions. We are going to use `bobtemplates.plone <https://pypi.python.org/pypi/bobtemplates.plone>`_ to create a skeleton project. We only need to fill in the blanks.

.. warning::

    ``bobtemplates.plone`` is still under heavy development. Questions and the package it creates might change significantly until Plone 5 is finished. For this training use the current master at https://github.com/plone/bobtemplates.plone/tree/b09362f

We create and enter the ``src`` directory (*src* is short for *sources*) and call a script called ``mrbob`` from our buildout's bin directory:

.. code-block:: bash

    $ mkdir src
    $ cd src
    $ ../bin/mrbob -O ploneconf.site bobtemplates:plone_addon

We have to answer some questions about the addon. We will press :kbd:`Enter` (i.e. choosing the default value) for all questions except 3 (where you enter your github username if you have one) and 5 (Plone version), where we enter :kbd:`5.0`.

..  code-block:: bash

    --> Author's name [Philip Bauer]:

    --> Author's email [bauer@starzel.de]:

    --> Author's github username: pbauer

    --> Package description [An add-on for Plone]:

    --> Plone version [4.3.4]: 5.0

    --> Add example view? [True]:

    --> Add a diazo-theme? [False]:

.. only:: not presentation

    If this is your first egg, this is a very special moment. We are going to create the egg with a script that generates a lot of necessary files. They all are necessary, but sometimes in a subtle way. It takes a while to understand their full meaning. Only last year I learnt and understood why I should have a ``manifest.in`` file. You can get along without one, but trust me, you get along better with a proper manifest file.


.. _eggs1-inspect-label:

Inspecting the package
----------------------

In ``src`` there is now a new folder ``ploneconf.site`` and in there is the new package. Let's have a look at some of the files:

bootstrap-buildout.py, buildout.cfg, travis.cfg, .travis.yml, .coveragerc
    You can ignore these files for now. They are here to create a buildout only for this egg to make testing it easier. Once we start writing tests for this package we will have another look at them.

README.txt, CHANGES, CONTRIBUTORS, docs/
    The documentation, changelog, the list of contributors and the license of your egg goes in there.

setup.py
    This file configures the package, its name, dependencies and some metadata like the author's name and email adress. The dependencies listed here are automatically downloaded when running buildout.

src/ploneconf/site/
    The package itself lives inside a special folder stucture. That seems confusing but is necessary for good testability. Our package is a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_ called *ploneconf.site* and because of this there is a folder ``ploneconf`` with a ``__init__.py`` and in there another folder ``site`` and in there finally is our code.
    From the buildout's perspective our code is in ``<your buildout directory>/src/ploneconf.site/src/ploneconf/site/<real code>``


.. note::

    Unless discussing the buildout we will from now on silently omit these folders when describing files and assume that ``<your buildout directory>/src/ploneconf.site/src/ploneconf/site/`` is the root of our package!


configure.zcml (src/ploneconf/site/configure.zcml)
    The phone book of the packages. By reading it you can find out which functionality is registered though the component architecture.

setuphandlers.py (src/ploneconf/site/setuphandlers.py)
    This holds code that is automatically run when installing and uninstalling our addon.

interfaces.py (src/ploneconf/site/interfaces.py)
    Here a browserlayer is defined in a straightforward python class. We will need it later.

testing.py
    This holds the setup for running tests.

tests/
    This holds the tests.

browser/
    This directory is a python package (because it has a ``__init__.py``) and will by convention hold most things that are visible in the browser.

browser/configure.zcml
    The phonebook of the browser directory. Here views, resources and overrides are registered.

browser/views.py
    xxx

browser/templates/demoview.pt
    xxx

static/
    A directory that holds static resources (images/css/js). The files in there will be accessible through URLs like ``++resource++ploneconf.site/myawesome.css``

profiles/default/
    The folder contains the GenericSetup profile. During the training will put some xml files there that hold configuration for the site.

profiles/default/metadata.xml
    Version number and dependencies that are auto-installed when installing our addon.

..    profiles/uninstall/
      This folder holds another GenericSetup profile. The steps in there are executed on uninstalling.


.. _eggs1-include-label:

Including the package in Plone
------------------------------

Before we can use our new package we have to tell Plone about it. Edit ``buildout.cfg`` and uncomment ``ploneconf.site`` in the sections `auto-checkout`, `eggs` and `test`:

.. code-block:: cfg
    :emphasize-lines: 6, 33, 41

    auto-checkout +=
        Products.PloneFormGen
        bobtemplates.plone
        ploneconf.site_sneak
    #    starzel.votable_behavior
        ploneconf.site

    parts =
        checkversions
        codeintel
        instance
        mrbob
        packages
        robot
        test
        zopepy

    eggs =
        Plone
        Pillow

    # development tools
        z3c.jbot
        plone.api
        plone.reload
        Products.PDBDebugMode
        plone.app.debugtoolbar

    # TTW Forms (based on Archetypes)
        Products.PloneFormGen

    # The addon we develop in the training
        ploneconf.site

    # Voting on content
    #    starzel.votable_behavior

    zcml =

    test-eggs +=
        ploneconf.site [test]

This tells Buildout to add the egg ``ploneconf.site``. Since it is also in the `sources` section buildout will not try to download it from pypi but will expect it in ``src/ploneconf.site``. *fs* allows you to add packages on the filesystem without a version control system, or with an unsupported one.

Now run buildout to reconfigure Plone with the updated configuration:

.. code-block:: bash

    $ ./bin/buildout

After restarting Plone with ``./bin/instance fg`` the new addon `ploneconf.site` is available for install like PloneFormGen or Plone True Gallery.

We will not install it now since we did not add any of our own code or configuration yet. Let's do that.
