Buildout I
==========

.. only:: manual

    Buildout composes your application for you, according to your rules.

    To compose your application you must define the eggs you need, which version, what configuration files Buildout has to generate for you, what to download and compile, and so on.
    Buildout downloads the eggs you requested and resolves all dependencies. You might need five different eggs, but in the end, Buildout has to install 300 eggs, all with the correct version.

    Plone needs folders for logfiles, databases and configuration files. Buildout assembles all of this for you.

    You will need a lot of functionality that Buildout does not provide out of the box, so you'll need several extensions.
    Some extensions provide whole new functionality, like mr.developer, the only way to manage your checked out sources.


Syntax
------

.. only:: manual

    The syntax of Buildout configuration files is similar to classic ini files. You write a parameter name, an equals sign and the value. If you enter another value in the next line and indent it, Buildout understands that both values belong to the parameter name, and the parameter stores all values as a list.

    A Buildout consists of multiple sections. Sections start with the section name in square brackets. Each section declares a different part of your application. As a rough analogy, your Buildout file is a cookbook with multiple recipes.

    There is a special section, called Buildout.
    This section can change the behavior of Buildout, but what is most important, is the variable :samp:`parts` here. This defines, which sections should actually be used.

    Buildout itself has no idea how to install Zope. Buildout is a plugin based system, it comes with a small set of plugins to create configuration files and download eggs with their dependencies and the proper version. To install a Zope site, you need a third-party plugin. The plugin provide new recipes that you have to declare and configure in a section.

References
----------

.. only:: manual

    Buildout allows you to use references in the configuration. A variable declaration may not only hold the variable value, but a reference to where to look for the variable value.

    If you have a big setup with many Plone sites with minor changes between each configuration, you can generate a template configuration, and each site references everything from the template and overrides just what needs to be changed.

    Even in smaller buildouts this is a useful feature. We are using the omelette. A very practical recipe that creates a virtual directory that eases the navigation to the source code of each egg.

    The recipe needs to know which eggs to reference. We want the same eggs as our instance uses, so we reference the eggs of the instance.
    If you create configuration files for nginx, you can define the target port for the reverse proxy by looking it up from the zope2instance recipe.

    Configuring complex systems always involves a lot of duplication of information. Using references in the buildout configuration allows you to minimize these duplications.

A real life example
-------------------

Let us walk through our ``buildout.cfg`` and look at some important variables:

.. code-block:: cfg
    :linenos:

    [buildout]
    parts =
        instance
        omelette
        codeintel
        zopeskel

    extends =
        http://dist.plone.org/release/4.3.3/versions.cfg
        versions.cfg

    extensions = mr.developer
    sources = sources
    auto-checkout = *

    versions = versions

    eggs =
        Plone
        Pillow
    # development tools
        z3c.jbot
        plone.api
        plone.reload
        Products.PDBDebugMode
        plone.app.debugtoolbar
        Paste
    # 3rd party addons
        Products.PloneFormGen
        collective.plonetruegallery
        collective.js.datatables
        eea.facetednavigation
        collective.behavior.banner
    # dexterity default types
        plone.app.contenttypes
    # our addons
    #    ploneconf.site
    #    starzel.votable_behavior

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    eggs = ${buildout:eggs}
    # The following is only used when we use vagrant.
    # The shared folder should not contain "big data" or symbolic links.
    file-storage = /home/vagrant/var/filestorage/Data.fs
    blob-storage = /home/vagrant/var/blobstorage

    [omelette]
    recipe = collective.recipe.omelette
    eggs = ${instance:eggs}
    # Same as above: We don't want links in the shared folder.
    # The default omelette-dir is parts/omelette
    location = /home/vagrant/omelette

    [codeintel]
    recipe = corneti.recipes.codeintel
    eggs = ${instance:eggs}
    extra-paths = ${omelette:location}

    [zopeskel]
    recipe = zc.recipe.egg
    eggs =
        ZopeSkel
        Paste
        PasteDeploy
        PasteScript
        zopeskel.diazotheme
        zopeskel.dexterity
        zest.releaser
        ${buildout:eggs}

    [sources]
    collective.behavior.banner = git https://github.com/starzel/collective.behavior.banner.git pushurl=git@github.com:starzel/collective.behavior.banner.git rev=af2dc1f21b23270e4b8583cf04eb8e962ade4c4d
    # ploneconf.site = fs ploneconf.site full-path=${buildout:directory}/src/ploneconf.site
    # starzel.votable_behavior = git git://github.com/starzel/starzel.votable_behavior.git


When you run Buildout without any arguments, Buildout will look for this file.

.. only:: manual

    Let us look closer at some variables.

.. only:: manual

    .. code-block:: cfg

        extends =

    This line tells Buildout to read more configuration files. You can refer to configuration files on your computer or to configuration files on the Internet, reachable via http. You can use multiple configuration files to share configurations between multiple Buildouts, or to separate different aspects of your configuration into different files. Typical examples are version specifications, or configuration that differ between different environments.

    .. code-block:: cfg

        eggs =

    This is the list of eggs that the Zope server must have available.

    .. code-block:: cfg

        develop =

    Here you list eggs that you are developing. They are not available as eggs but as a folder with a specific structure. Zope has to load eggs slightly different to these so-called ``checkouts``.

    .. code-block:: cfg

        [versions]

    This is another special section. It has become a special section by declaration. In our :samp:`[buildout]` section we set a variable :samp:`version = version`. This told buildout, that there is a section named versions, containing version information.

Hello mr.developer!
-------------------

.. only:: manual

    There are many more important things to know, and we can't go through them in all the detail but I want to focus on one specific feature: **mr.developer**

    With mr.developer you can declare which packages you want to check out from which version control system and which repository URL. You can check out sources from git, svn, bzr, hg and maybe more. Also, you can say that some source are in your local file system.

    ``mr.developer`` comes with a command, ``./bin/develop``. You can use it to update your code, to check for changes and so on. You can activate and deactivate your source checkouts. If you develop your extensions in eggs with separate checkouts, which is a good practice, you can plan releases by having all source checkouts deactivated, and only activate them, when you write changes that require a new release. You can activate and deactivate eggs via the develop command or the Buildout configuration. You should always use the Buildout way. Your commit serves as documentation.

Extensible
----------

.. only:: manual

    You might have noticed that most if not all functionality is only available via plugins. One of the things that Buildout excels at without any plugin, is the dependency resolution. You can help Plone in dependency resolution by declaring exactly which version of an egg you want. This is only one use case. Another one is much ,more important. If you want to have a repeatable Buildout, one that works two months from now also, you *must* declare all your egg versions. Else Buildout might install newer versions.

Be McGuyver
-----------

.. only:: manual

    As you can see, you can build very complex systems with Buildout. It is time for some warnings. Be selective in your recipes. Supervisor is a program to manage running servers, its pretty good. There is a recipe for it.

    The configuration is more complicated than the supervisor configuration itself! By using this recipe, you force others to understand the recipes specific configuration syntax *and* the supervisor syntax. For such cases, collective.recipe.template is a better match.

    Another problem is error handling. Buildout tries to install a weird dependency you do not actually want? Buildout will not tell you, where it is coming from.

    If there is a problem, you can always run Buildout with -v, to get more verbose output, sometimes it helps.

    .. code-block:: bash

        $ ./bin/buildout -v

    If strange egg versions are requested, check the dependencies declaration of your eggs and your version pinnings.

    Some parts of Buildout interpret egg names case-sensitive, others won't. This can result in funny problems.

    Always check out the ordering of your extends, always use the :samp:`annotate` command of Buildout to see if it interprets your configuration differently than you. Restrict yourself to simple Buildout files. You can reference variables from other sections, you can even use a whole section as a template. We learned that this does not work well with complex hierarchies and had to abandon that feature.

