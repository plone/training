.. _eggs1-label:

Write Your Own Add-Ons to Customize Plone
=========================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: bash

        git checkout eggs1

.. _eggs1-create-label:


In this part you will:

* Create a custom Python package :py:mod:`ploneconf.site` to hold all the code
* Modify buildout to install that package


Topics covered:

* :py:mod:`mr.bob` and :py:mod:`bobtemplates.plone`
* the structure of eggs


Creating the package
-------------------------

Our own code has to be organized as a Python package, also called *egg*. An egg is a zip file or a directory that follows certain conventions. We are going to use `bobtemplates.plone <https://pypi.python.org/pypi/bobtemplates.plone>`_ to create a skeleton project. We only need to fill in the blanks.

We create and enter the :file:`src` directory (*src* is short for *sources*) and call a script called :command:`mrbob` from our buildout's :file:`bin` directory:

.. code-block:: bash

    $ mkdir src      # (if src does not exist already)
    $ cd src
    $ ../bin/mrbob -O ploneconf.site bobtemplates:plone_addon

We have to answer some questions about the add-on. We will press :kbd:`Enter` (i.e. choosing the default value) for all questions except 3 (where you enter your GitHub username if you have one) and 5 (Plone version), where we enter :kbd:`5.0.6`::

    --> What kind of package would you like to create? Choose between 'Basic', 'Dexterity', and 'Theme'. [Basic]:

    --> Author's name [Philip Bauer]:

    --> Author's email [bauer@starzel.de]:

    --> Author's GitHub username: fulv

    --> Package description [An add-on for Plone]:

    --> Plone version [5.0.5]: 5.0.6

    Generated file structure at /vagrant/buildout/src/ploneconf.site

.. only:: not presentation

    If this is your first egg, this is a very special moment.
    We are going to create the egg with a script that generates a lot of necessary files.
    They all are necessary, but sometimes in a subtle way.
    It takes a while to understand their full meaning.
    Only last year I learned and understood why I should have a :file:`MANIFEST.in` file.
    You can get along without one, but trust me, you get along better with a proper manifest file.


.. _eggs1-inspect-label:

Inspecting the package
---------------------------

In :file:`src` there is now a new folder :file:`ploneconf.site` and in there is the new package. Let's have a look at some of the files:

:file:`bootstrap-buildout.py`, :file:`buildout.cfg`, :file:`travis.cfg`, :file:`.travis.yml`, :file:`.coveragerc`
    You can ignore these files for now. They are here to create a buildout only for this egg to make testing it easier. Once we start writing tests for this package we will have another look at them.

:file:`README.rst`, :file:`CHANGES.rst`, :file:`CONTRIBUTORS.rst`, :file:`docs/`
    The documentation, changelog, the list of contributors and the license of your egg goes in here.

:file:`setup.py`
    This file configures the package, its name, dependencies and some metadata like the author's name and email address. The dependencies listed here are automatically downloaded when running buildout.

:file:`src/ploneconf/site/`
    The package itself lives inside a special folder structure.
    That seems confusing but is necessary for good testability.
    Our package contains a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_ called *ploneconf.site* and because of this there is a folder :file:`ploneconf` with a :file:`__init__.py` and in there another folder :file:`site` and in there finally is our code.
    From the buildout's perspective our code is in :file:`{your buildout directory}/src/ploneconf.site/src/ploneconf/site/{real code}`


.. note::

    Unless discussing the buildout we will from now on silently omit these folders when describing files and assume that :file:`{your buildout directory}/src/ploneconf.site/src/ploneconf/site/` is the root of our package!


:file:`configure.zcml` (:file:`src/ploneconf/site/configure.zcml`)
    The phone book of the distribution. By reading it you can find out which functionality is registered using the component architecture.

:file:`setuphandlers.py` (:file:`src/ploneconf/site/setuphandlers.py`)
    This holds code that is automatically run when installing and uninstalling our add-on.

:file:`interfaces.py` (:file:`src/ploneconf/site/interfaces.py`)
    Here a browserlayer is defined in a straightforward python class. We will need it later.

:file:`testing.py`
    This holds the setup for running tests.

:file:`tests/`
    This holds the tests.

:file:`browser/`
    This directory is a python package (because it has a :file:`__init__.py`) and will by convention hold most things that are visible in the browser.

:file:`browser/configure.zcml`
    The phonebook of the browser package. Here views, resources and overrides are registered.

:file:`browser/overrides/`
    This add-on is already configured to allow overriding existing default Plone templates.

:file:`browser/static/`
    A directory that holds static resources (images/css/js). The files in here will be accessible through URLs like ``++resource++ploneconf.site/myawesome.css``

:file:`profiles/default/`
    This folder contains the GenericSetup profile. During the training we will put some XML files here that hold configuration for the site.

:file:`profiles/default/metadata.xml`
    Version number and dependencies that are auto-installed when installing our add-on.

..    profiles/uninstall/
      This folder holds another GenericSetup profile. The steps in here are executed on uninstalling.


.. _eggs1-include-label:

Including the package in Plone
-----------------------------------

Before we can use our new package we have to tell Plone about it. Look at :file:`buildout.cfg` and see how ``ploneconf.site`` is included in `auto-checkout`, `eggs` and `test`:

.. code-block:: cfg
    :emphasize-lines: 2, 31, 40

    auto-checkout +=
        ploneconf.site
    #    starzel.votable_behavior

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
        Products.PrintingMailHost

    # TTW Forms (based on Archetypes)
        Products.PloneFormGen

    # The add-on we develop in the training
        ploneconf.site

    # Voting on content
    #    starzel.votable_behavior

    zcml =

    test-eggs +=
        ploneconf.site [test]

This tells Buildout to add the egg :py:mod:`ploneconf.site`. The sources for this eggs are defined in the section ``[sources]`` at the bottom of :file:`buildout.cfg`.

..  code-block:: cfg
    :emphasize-lines: 2

    [sources]
    ploneconf.site = git https://github.com/collective/ploneconf.site.git pushurl=git@github.com:collective/ploneconf.site.git
    starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git

This tells buildout not to download it from pypi but to do a checkout from GitHub put the code in :file:`src/ploneconf.site`.

..  note::

    The package ``ploneconf.site`` is now downloaded from GitHub and automatically in the branch master

..  note::

    If you do **not** want to use the prepared package for ploneconf.site from GitHub but write it yourself (we suggest you try that) then add the following instead:

    ..  code-block:: cfg
        :emphasize-lines: 2

        [sources]
        ploneconf.site = fs ploneconf.site path=src
        starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git

    This tells buildout to expect `ploneconf.site` in :file:`src/ploneconf.site`.
    The directive ``fs`` allows you to add eggs on the filesystem without a version control system.

Now run buildout to reconfigure Plone with the updated configuration:

.. code-block:: bash

    $ ./bin/buildout

After restarting Plone with :command:`./bin/instance fg` the new add-on :py:mod:`ploneconf.site` is available for install like PloneFormGen or Plone True Gallery.

We will not install it now since we did not add any of our own code or configuration yet. Let's do that next.
