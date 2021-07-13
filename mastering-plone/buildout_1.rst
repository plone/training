.. _buildout1-label:

Buildout I
==========

In this part you will:

* learn about how to configure and document a setup of a Plone installation

Topics covered:

* Buildout
* Recipes
* Buildout Configuration
* mr.developer

.. only:: not presentation

    `Buildout <https://pypi.org/project/zc.buildout>`_ composes your Plone application according to your rules.

    .. note::

        For the Volto frontend this building task is done by the tool ``yarn``.

    To compose your application you have to define the python packages (eggs) you need, which version, what configuration files Buildout has to generate for you, what to download and compile, and so on.

    Buildout downloads the eggs you requested and resolves all dependencies. You might need five different eggs, but in the end, Buildout has to install 300 eggs, all with the correct version in order to resolve all the dependencies.

    Buildout does this without touching your system Python or affecting any other package. The commands created by buildout bring all the required packages into the Python environment. Each command it creates may use different libraries or even different versions of the same library.

    Plone needs folders for logfiles, databases and configuration files. Buildout assembles all of this for you.

    You will need a lot of functionality that Buildout does not provide out of the box, so you'll need several extensions.

    Some extensions provide new functionality, like mr.developer, the best way to manage your checked out sources.


Minimal Example
---------------

Here is a functioning minimal example from https://github.com/collective/minimalplone5:

.. code-block:: ini

    [buildout]
    parts = instance
    extends = https://dist.plone.org/release/5.2-latest/versions.cfg

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        Plone

.. _buildout1-syntax-label:

Syntax
------

.. only:: not presentation

    The syntax of Buildout configuration files is similar to classic ini files. You write a parameter name, an equals sign and the value. If you enter another value in the next line and indent it, Buildout understands that both values belong to the parameter name, and the parameter stores all values as a list.

    A Buildout consists of multiple sections. Sections start with the section name in square brackets. Each section declares a different part of your application. As a rough analogy, your Buildout file is a cookbook with multiple recipes.

    There is a special section, called `[buildout]`. This section can change the behavior of Buildout itself. The variable :samp:`parts` defines which of the existing sections should actually be used.

.. _buildout1-recipes-label:

Recipes
-------

Buildout itself has no idea how to install Zope.
Buildout is a plugin based system, it comes with a small set of plugins to create configuration files and download eggs with their dependencies and the proper version.

To install a Zope site, you need a third-party plugin.
Plugins provide recipes that have to be declared and configured in their own respective buildout sections.

One example is the section

.. code-block:: ini

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin

This uses the python package `plone.recipe.zope2instance <https://pypi.org/project/plone.recipe.zope2instance>`_
to create and configure the Zope 2 instance which we use to run Plone.

All the lines after :samp:`recipe = xyz` are the configuration of the specified recipe.

.. note::

    Find a list of buildout recipes at https://pypi.org/search/?q=buildout+recipe

.. _buildout1-references-label:

Variables and References
------------------------

.. only:: not presentation

    A variable is declared with a ``=`` and can be used with a ``${}``:

    .. code-block:: ini

        [buildout]
        devtool = pdbpp

        more_devtools =
            plone.reload
            Products.PDBDebugMode
            Products.PrintingMailHost
            plone.app.debugtoolbar

        eggs =
            Plone
            ${devtool}
            ${more_devtools}

    Buildout allows you to use references in the configuration. A variable declaration may not only hold the variable value, but also a reference to where to look for the variable value.

    .. code-block:: ini

        [buildout]
        devtool = pdbpp

        more_devtools =
            plone.reload
            Products.PDBDebugMode
            Products.PrintingMailHost
            plone.app.debugtoolbar

        [production]
        eggs =
            Plone
            ${buildout:devtool}
            ${buildout:more_devtools}

    If you have a big setup with many Plone sites with minor changes between each configuration, you can generate a template configuration, and each site references everything from the template and overrides just what needs to be changed.

    Even in smaller buildouts this is a useful feature. For example in the part ``[packages]`` we are using `collective.recipe.omelette <https://pypi.org/project/collective.recipe.omelette>`_. A very practical recipe that creates a directory with `symbolic links <https://en.m.wikipedia.org/wiki/Symbolic_link>`_ that eases the navigation to the source code of each egg used in our project.

    The omelette recipe needs to know which eggs to symlink. We want the same eggs that our project uses, so we point it to the already defined list of eggs with ``${buildout:eggs}`` instead of repeating the whole list.

    Another example: Say you create configuration files for a webserver like nginx, you can define the target port for the reverse proxy by looking it up from the zope2instance recipe.

    Configuring complex systems always involves a lot of duplication of information. Using references in the buildout configuration allows you to minimize these duplications.

    .. code-block:: ini

        [instance]
        recipe = plone.recipe.zope2instance
        …
        file-storage = ${buildout:buildout_dir}/var/filestorage/Data.fs
        blob-storage = ${buildout:buildout_dir}/var/blobstorage

    :samp:`${{buildout:buildout_dir}}`:
    :samp:`buildout` is the section whose variable :samp:`buildout_dir` is overwritten in the section instance.


.. _buildout1-examples-label:

A real life example
-------------------

Let us walk through the :file:`buildout.cfg` for the training and look at some important variables:

.. code-block:: ini

    [buildout]
    extends =
        http://dist.plone.org/release/5.2.3/versions.cfg
        versions.cfg
    extends-cache = extends-cache

    extensions = mr.developer
    # Tell mr.developer to ask before updating a checkout.
    always-checkout = true
    show-picked-versions = true
    sources = sources

    # The directory this buildout is in. Modified when using vagrant.
    buildout_dir = ${buildout:directory}

    # We want to checkouts these eggs directly from github
    auto-checkout =
        ploneconf.site
    #    starzel.votable_behavior

    parts =
        checkversions
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
        plone.reload
        Products.PDBDebugMode
        plone.app.debugtoolbar
        Products.PrintingMailHost
        pdbpp

    # TTW Forms
        collective.easyform

    # The add-on we develop in the training
        ploneconf.site

    # Voting on content
    #    starzel.votable_behavior

    zcml =

    test-eggs +=
        ploneconf.site [test]

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    debug-mode = on
    verbose-security = on
    deprecation-warnings = on
    eggs = ${buildout:eggs}
    zcml = ${buildout:zcml}
    file-storage = ${buildout:buildout_dir}/var/filestorage/Data.fs
    blob-storage = ${buildout:buildout_dir}/var/blobstorage

    [test]
    recipe = zc.recipe.testrunner
    eggs = ${buildout:test-eggs}
    defaults = ['--auto-color', '-vvv']

    [robot]
    recipe = zc.recipe.egg
    eggs =
        ${buildout:test-eggs}
        Pillow
        plone.app.robotframework[reload,debug]

    [packages]
    recipe = collective.recipe.omelette
    eggs = ${buildout:eggs}
    location = ${buildout:buildout_dir}/packages

    [checkversions]
    recipe = zc.recipe.egg
    eggs = z3c.checkversions [buildout]

    [zopepy]
    recipe = zc.recipe.egg
    eggs =
        ${buildout:eggs}
    # need to explicitly mention plone.staticresources in order for plone-compile-resources to be found
        plone.staticresources
    interpreter = zopepy
    scripts =
        zopepy
        plone-compile-resources

    [mrbob]
    recipe = zc.recipe.egg
    eggs =
        mr.bob
        bobtemplates.plone

    [sources]
    ploneconf.site = git https://github.com/collective/ploneconf.site.git pushurl=git@github.com:collective/ploneconf.site.git
    starzel.votable_behavior = git https://github.com/collective/starzel.votable_behavior.git pushurl=git://github.com/collective/starzel.votable_behavior.git


When you run :command:`./bin/buildout` without any arguments, Buildout will look for this file.

.. note::
    If you are using the vagrant installation, you will have to activate your `virtualenv` and run the command :command:`buildout` only.
    In the vagrant setup `zc.buildout` and `setuptools` are installed in the virtualenv and therefore available without specifying the
    preceding path. This is possible because in recent versions of `zc.buildout` the `bootstrap` step is no longer necessary.

.. only:: not presentation

    Let us look closer at some variables.

.. only:: not presentation

    .. code-block:: cfg

        extends =
            http://dist.plone.org/release/5.2.3/versions.cfg

    This line tells Buildout to read another configuration file. You can refer to configuration files on your computer or to configuration files on the Internet, reachable via http. You can use multiple configuration files to share configurations between multiple Buildouts, or to separate different aspects of your configuration into different files. Typical examples are version specifications, or configurations that differ between different environments.

    ..  code-block:: cfg

        eggs =
            Plone

        # development tools
            z3c.jbot
            plone.reload
            Products.PDBDebugMode
            plone.app.debugtoolbar
            Products.PrintingMailHost
            pdbpp

        # TTW Forms
            collective.easyform

        # The add-on we develop in the training
            ploneconf.site

        # Voting on content
        #    starzel.votable_behavior

        zcml =

        test-eggs +=
            ploneconf.site [test]

    This is the list of eggs that we configure to be available for Zope. These eggs are put in the python path of the script :command:`bin/instance` with which we start and stop Plone.

    The egg ``Plone`` is a wrapper without code. Among its dependencies is :py:mod:`Products.CMFPlone`  which is the egg that is at the center of Plone.

    The rest are add-ons we already used or will use later. The last eggs are commented out so they will not be installed by Buildout.

    The file :file:`versions.cfg` that is included by the :samp:`extends = ...` statement holds the version pins:

    .. code-block:: cfg

        [versions]
        # dev tools and their dependencies
        pdbpp = 0.10.0
        fancycompleter = 0.8
        pyrepl = 0.9.0

        # pins for Add-ons
        collective.easyform = 2.1.0
        Products.validation = 2.1.1

        # pins for mr.bob and bobtemplates.plone
        bobtemplates.plone = 4.1.3
        case-conversion = 2.1.0
        mr.bob = 0.1.2

        # Some other pins from coredev
        argh = 0.26.2
        pathtools = 0.1.2
        prompt-toolkit = 1.0.16
        PyYAML = 5.1.2
        regex = 2019.8.19
        watchdog = 0.9.0
        wcwidth = 0.1.7
        wmctrl = 0.3


    This is another special section. By default buildout will look for version pins in a section called ``[versions]``. This is why we included the file :file:`versions.cfg`.

.. _buildout1-mrdeveloper-label:

Mr. Developer
-------------

.. only:: not presentation

    There are many more important things to know, and we can't go through all of them in detail but I want to focus on one specific feature: :py:mod:`mr.developer`.

    With :py:mod:`mr.developer` you can declare which packages you want to check out from which version control system and which repository URL. You can check out sources from git, svn, bzr, hg and maybe more. Also, you can say that some sources are in your local file system.

    :py:mod:`mr.developer` comes with a command, :command:`./bin/develop`. You can use it to update your code, to check for changes and so on. You can activate and deactivate your source checkouts. If you develop your add-ons in separate eggs with associated checkouts, which is a good practice, you can plan releases by having all source checkouts deactivated, and only activate them when you write changes that require new releases. You can activate and deactivate eggs via the :command:`develop` command or the Buildout configuration. You should always use the Buildout way. Your commit comment serves as documentation of your Plone setup.

.. _buildout1-extensible-label:

Extensible
----------

.. only:: not presentation

    You might have noticed that most if not all functionality is only available via plugins.
    One of the things that Buildout excels at without any plugin is the dependency resolution.
    You can help Plone in dependency resolution by declaring exactly which version of an egg you want.

    This is only one use case.
    Another one is much more important: If you want to have a repeatable Buildout, one that works two months from now.

    Also, you *must* declare all your egg versions, else Buildout might install newer versions.

.. _buildout1-mcguyver-label:

Be McGuyver
-----------

.. only:: not presentation

    As you can see, you can build very complex systems with Buildout. It is time for some warnings. Be selective in your recipes. Supervisor is a program to manage running servers, and it's pretty good. There is a recipe for it.

    The configuration for this recipe is more complicated than the supervisor configuration itself! By using this recipe, you force others to understand the recipe's specific configuration syntax *and* the supervisor syntax. For such cases, `collective.recipe.template <https://pypi.org/project/collective.recipe.template>`_ is a better match.

    Another problem is error handling. Buildout tries to install a weird dependency you do not actually want? Buildout will not tell you where it is coming from.

    If there is a problem, you can always run Buildout with :option:`-v` to get more verbose output, sometimes it helps.

    .. code-block:: bash

        $ ./bin/buildout -v

    If strange egg versions are requested, check the dependencies declaration of your eggs and your version pinnings.
    Here is an invaluable shell command that allows you to find all packages that depend on a particular egg and version:

    .. code-block:: bash

        $ grep your.egg.name.here /home/vagrant/buildout-cache/eggs/*.egg/EGG-INFO/requires.txt

    Put the name of the egg with a version conflict as the first argument.  Also, change the path to the buildout cache folder according to your installation (the vagrant buildout is assumed in the example).

    Some parts of Buildout interpret egg names case sensitively, others don't. This can result in funny problems.

    Always check out the ordering of your extends, always use the :samp:`annotate` command of Buildout to see if it interprets your configuration differently than you. Restrict yourself to simple Buildout files. You can reference variables from other sections, you can even use a whole section as a template. We learned that this does not work well with complex hierarchies and had to abandon that feature.

    In the chapter :doc:`deployment_sites` we will have a look at a production-ready buildout for Plone that has many useful features.

.. seealso::

    Buildout-Documentation
        http://docs.buildout.org/en/latest/contents.html

    Troubleshooting
        https://docs.plone.org/manage/troubleshooting/buildout.html

    A minimal buildout for Plone 5
        https://github.com/collective/minimalplone5

    A minimal buildout for Plone 4
        https://github.com/collective/minimalplone4

    The buildout of the unified installer has some valuable documentation as inline-comment
        * https://github.com/plone/Installers-UnifiedInstaller/blob/master/buildout_templates/buildout.cfg
        * https://github.com/plone/Installers-UnifiedInstaller/blob/master/base_skeleton/base.cfg
        * https://github.com/plone/Installers-UnifiedInstaller/blob/master/base_skeleton/develop.cfg

    mr.developer
        https://pypi.org/project/mr.developer/
