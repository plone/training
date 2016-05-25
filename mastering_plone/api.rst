.. _api-label:

Programming Plone
=================

In this part you will:

* Learn about the right ways to do something in code in Plone.
* Learn to debug

Topics covered:

* Debugging
* Plone API
* Portal tools


.. _api-api-label:

plone.api
---------

The most important tool nowadays for plone developers is the add-on `plone.api <http://docs.plone.org/develop/plone.api/docs/index.html>`_ that covers 20% of the tasks any Plone developer does 80% of the time. If you are not sure how to handle a certain task be sure to first check if plone.api has a solution for you.

The api is divided in five sections. Here is one example from each:

* `Content:` `Create content <http://docs.plone.org/develop/plone.api/docs/content.html#create-content>`_
* `Portal:` `Send E-Mail <http://docs.plone.org/develop/plone.api/docs/portal.html#send-e-mail>`_
* `Groups:` `Grant roles to group <http://docs.plone.org/develop/plone.api/docs/group.html#grant-roles-to-group>`_
* `Users:` `Get user roles <http://docs.plone.org/develop/plone.api/docs/user.html#get-user-roles>`_
* `Environment:` `Switch roles inside a block <http://docs.plone.org/develop/plone.api/docs/env.html#switch-roles-inside-a-block>`_

plone.api is not yet part of the Plone core. Therefore you will not see any use of plone.api in Plone itself. It will be part of Plone 5.

In existing code you'll often encounter methods that don't mean anything to you. You'll have to use the source to find out  what they do.

Some of these methods will be replaced by plone.api in the future:

- ``Products.CMFCore.utils.getToolByName`` -> ``api.portal.get_tool``
- ``zope.component.getMultiAdapter`` -> ``api.content.get_view``


.. _api-portal-tools-label:

portal-tools
------------

Some parts of Plone are very complex modules in themselves (e.g. the versioning machinery of ``Products.CMFEditions``). Some of them have an api that you will have to learn sooner or later.

Here are a few examples:

portal_catalog
    ``unrestrictedSearchResults()`` returns search results without checking if the current user has the permission to access the objects.

    ``uniqueValuesFor()`` returns all entries in an index

portal_setup
    ``runAllExportSteps()`` generates a tarball containing artifacts from all export steps.

portal_quickinstaller
    ``isProductInstalled()`` checks if a product is installed.

Usually the best way to learn about the api of a tool is to look in the ``interfaces.py`` in the respective package and read the docstrings.


.. _api-debugging-label:

Debugging
---------

Here are some tools and techniques we often use when developing and debugging. We use some of them in various situations during the training.

tracebacks and the log
    The log (and the console when running in foreground) collects all log messages Plone prints. When an exception occurs Plone throws a traceback. Most of the time the traceback is everything you need to find out what is going wrong. Also adding your own information to the log is very simple.

pdb
    The python debugger pdb is the single most important tool for us when programming. Just add ``import pdb; pdb.set_trace()`` in your code and debug away!

    Since Plone 5 you can even add it to templates: add ``<?python import pdb; pdb.set_trace() ?>`` to a template and you end up in a pdb shell on calling the template. Look at the variable ``econtext`` to see what might have gone wrong.

ipdb
    Enhanced pdb with the power of IPython, e.g. tab completion, syntax highlighting, better tracebacks and introspection. It also works nicely with Products.PDBDebugMode.

Products.PDBDebugMode
    An add-on that has two killer features.

    **Post-mortem debugging**: throws you in a pdb whenever an exception occurs. This way you can find out what is going wrong.

    **pdb view**: simply adding ``/pdb`` to a url drops you in a pdb session with the current context as ``self.context``. From there you can do just about anything.

Debug mode
    When starting Plone using ``./bin/instance -O Plone debug`` you'll end up in an interactive debugger.

plone.app.debugtoolbar (not working yet in Plone 5!)
    An add-on that allows you to inspect nearly everything. It even has an interactive console and a tester for TALES-expressions.

plone.reload
    An add-on that allows to reload code that you changed without restarting the site. It is also used by plone.app.debugtoolbar.

Products.PrintingMailHost
    An add-on that prevents Plone from sending mails. Instead, they are logged.

Products.enablesettrace or Products.Ienablesettrace
    Add-on that allows to use pdb and ipdb in python skin scripts. Very useful when debugging legacy code.

``verbose-security = on``
    An option for the recipe *plone.recipe.zope2instance* that logs the detailed reasons why a user might not be authorized to see something.

``./bin/buildout annotate``
    An option when running buildout that logs all the pulled packages and versions.

Sentry
    `Sentry <https://github.com/getsentry/sentry>`_ is an error logging application you can host yourself. It aggregates tracebacks from many sources and (here comes the killer feature) even the values of variables in the traceback. We use it in all our production sites.

zopepy
    Buildout can create a python shell for you that has all the packages from your Plone site in its python path. Add the part like this::

        [zopepy]
        recipe = zc.recipe.egg
        eggs = ${instance:eggs}
        interpreter = zopepy
