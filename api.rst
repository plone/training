Programming Plone
=================

plone.api
---------

The most important tool nowadays for plone-developers is the addon `plone.api <http://docs.plone.org/external/plone.api/docs/index.html>`_ hat covers 20% of the tasks any Plone developer does 80% of the time. If you are not sure how to handle a certain task be sure to first check if plone.api has a solution for you.

The api is devided in five sections. Here is one example from each:

* `Content`: `Create content <http://docs.plone.org/external/plone.api/docs/content.html#create-content>`_
* `Portal`: `Send E-Mail <http://docs.plone.org/external/plone.api/docs/portal.html#send-e-mail>`_
* `Groups`: `Grant roles to group <http://docs.plone.org/external/plone.api/docs/group.html#grant-roles-to-group>`_
* `Users`: `Get user roles <http://docs.plone.org/external/plone.api/docs/user.html#get-user-roles>`_
* `Environment`: `Switch roles inside a block <http://docs.plone.org/external/plone.api/docs/env.html#switch-roles-inside-a-block>`_

plone.api is not yet part of the Plone core. Therefore you will not see any use of plone.api in in Plone itself. But we are sure it will be part of Plone 5 if someone gets around to submitting the PLIP.

In existing code you'll often encounter methods that don't mean anything to you. You'll have to use the source to find out about what they do.

Some of these methods will be replaced by plone.api in the future:

- ``Products.CMFCore.utils.getToolByName`` -> ``api.portal.get_tool``
- ``zope.component.getMultiAdapter`` -> ``api.content.get_view``


portal-tools
------------

Some parts of Plone are very complex modules in themselves (e.g. the while versioning-machinery of ``Products.CMFEditions``). Some of them have an api that you will have to learn sooner or later.

Here are a few examples:

portal_catalog
    ``unrestrictedSearchResults()`` returns search-results without checking if the current user has the permission to access the objects.

    ``uniqueValuesFor()`` returns all entries in a index

portal_setup
    ``runAllExportSteps()`` generates a tarball containing artifacts from all export steps.

portal_quickinstaller
    ``isProductInstalled()`` checks wether a product is installed.

Usually the best way to learn about the api of a tool is to look in the ``interfaces.py`` in the respective package and read the docstrings.


Debugging
---------

Here are some tools and techniques we often use when developing and debugging. We use some of them in various situations during the training.

tracebacks and the log
    The log (and the console when running in foreground) collect all log-messages Plone prints. When a exception occurs Plone thows a traceback. Most of th time the traceback is everything you need to find out what is going wrong. Also adding your own information to the log is very simple.

pdb
    The python debugger pdb is the single most important tool for us when programming. Just add ``import pdb; pdb.set_trace()`` in your code and debug away!

Products.PDBDebugMode
    A addon that has two killer-features.

    **Post-mortem debugging**: throws you in a pdb whenever a exception occurs. This way you can find ou what is going wrong.

    **pdb-view**: simply adding ``/pdb`` to a url drops you in a pdb-session with the current context as ``self.context``. From there you can do just about anything.

Debug-mode
    When starting Plone using ``./bin/instance debug -O Plone`` you'# end up in interactive debugger.

plone.app.debugtoolbar
    A addon that allows you to inspect nearly everything. It even has a interactive console and a tester for TALES-expressions.

plone.reload
    An addon that allows to reload code that you changed without restarting the site. It is also used by plone.app.debugtoolbar.

Products.PrintingMailHost
    A addon that prevents Plone from sending mails. They are instead logged.

Products.Ienablesettrace
    Addon that allows to use pdb and ipdb in python skin-scripts. Very useful.

``verbose-security = on``
    A option for the recipe *plone.recipe.zope2instance* that logs the detailed reasons why a user might not be authorized to see something.

``./bin/buildout annotate``
    A option when running buildout that logs all the pulled packages and versions.

Sentry
    `Sentry <https://github.com/getsentry/sentry>`_ is a error logging application you can host yourself. It aggregarates tracebacks from many sources and (here comes the killer-feature) even the values of variables in the stacktrace. We use in on all our production-sites.

zopepy
    Buildout can create a python-shell for you that has all the packages from your plone-site in it's python-path. Add the part like this::

        [zopepy]
        recipe = zc.recipe.egg
        eggs = ${instance:eggs}
        interpreter = zopepy
