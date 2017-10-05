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

The most important tool nowadays for plone developers is the add-on `plone.api <https://docs.plone.org/develop/plone.api/docs/index.html>`_ that covers 20% of the tasks any Plone developer does 80% of the time. If you are not sure how to handle a certain task be sure to first check if plone.api has a solution for you.

The API is divided in five sections. Here is one example from each:

* `Content:` `Create content <https://docs.plone.org/develop/plone.api/docs/content.html#create-content>`_
* `Portal:` `Send E-Mail <https://docs.plone.org/develop/plone.api/docs/portal.html#send-e-mail>`_
* `Groups:` `Grant roles to group <https://docs.plone.org/develop/plone.api/docs/group.html#grant-roles-to-group>`_
* `Users:` `Get user roles <https://docs.plone.org/develop/plone.api/docs/user.html#get-user-roles>`_
* `Environment:` `Switch roles inside a block <https://docs.plone.org/develop/plone.api/docs/env.html#switch-roles-inside-a-block>`_

:py:mod:`plone.api` is a great tool for integrators and developers that is included when you install Plone, though for technical reasons it is not used by the code of Plone itself.

In existing code you'll often encounter methods that don't mean anything to you. You'll have to use the source to find out  what they do.

Some of these methods will be replaced by :py:mod:`plone.api` in the future:

- :py:meth:`Products.CMFCore.utils.getToolByName` -> :py:meth:`api.portal.get_tool`
- :py:meth:`zope.component.getMultiAdapter` -> :py:meth:`api.content.get_view`


.. _api-portal-tools-label:

portal-tools
------------

Some parts of Plone are very complex modules in themselves (e.g. the versioning machinery of :py:mod:`Products.CMFEditions`).
Most of them have an API of themselves that you will have to look up at when you need to implement a feature that is not covered by plone.api.

Here are a few examples:

portal_catalog
    :py:meth:`unrestrictedSearchResults()` returns search results without checking if the current user has the permission to access the objects.

    :py:meth:`uniqueValuesFor()` returns all entries in an index

portal_setup
    :py:meth:`runAllExportSteps()` generates a tarball containing artifacts from all export steps.

portal_quickinstaller
    :py:meth:`isProductInstalled()` checks if a product is installed.

Usually the best way to learn about the API of a tool is to look in the :file:`interfaces.py` in the respective package and read the docstrings. But sometimes the only way to figure out which features a tool offers is to read its code.

To use a tool you usually first get the tool with :py:mod:`plone.api` and then invoke the method.

Here is an example where we get the tool `portal_membership` and use one of its methods to logout a user:

.. code-block:: python

    mt = api.portal.get_tool('portal_membership')
    mt.logoutUser(request)

.. note::

    The code for :py:meth:`logoutUser()` is in :py:meth:`Products.PlonePAS.tools.membership.MembershipTool.logoutUser`. Many tools that are used in Plone are actually subclasses of tools from the package :py:mod:`Products.CMFCore`. For example `portal_membership` is subclassing and extending the same tool from :py:class:`Products.CMFCore.MembershipTool.MembershipTool`. That can make it hard to know which options a tool has. There is a ongoing effort by the Plone Community to consolidate tools to make it easier to work with them as a developer.

.. _api-debugging-label:

Debugging
---------

Here are some tools and techniques we often use when developing and debugging. We use some of them in various situations during the training.

tracebacks and the log
    The log (and the console when running in foreground) collects all log messages Plone prints. When an exception occurs Plone throws a traceback. Most of the time the traceback is everything you need to find out what is going wrong. Also adding your own information to the log is very simple.

pdb
    The python debugger pdb is the single most important tool for us when programming. Just add ``import pdb; pdb.set_trace()`` in your code and debug away!

    Since Plone 5 you can even add it to templates: add ``<?python import pdb; pdb.set_trace() ?>`` to a template and you end up in a pdb shell on calling the template. Look at the variable :py:obj:`econtext` to see what might have gone wrong.

ipdb
    Enhanced pdb with the power of IPython, e.g. tab completion, syntax highlighting, better tracebacks and introspection. It also works nicely with :py:mod:`Products.PDBDebugMode`.

Products.PDBDebugMode
    An add-on that has two killer features.

    **Post-mortem debugging**: throws you in a pdb whenever an exception occurs. This way you can find out what is going wrong.

    **pdb view**: simply adding ``/pdb`` to a url drops you in a pdb session with the current context as :py:obj:`self.context`. From there you can do just about anything.

Debug mode
    When starting Plone using :command:`./bin/instance debug` you'll end up in an interactive debugger.

plone.app.debugtoolbar
    An add-on that allows you to inspect nearly everything. It even has an interactive console, a tester for TALES-expressions and includs a reload-feature like :py:mod:`plone.reload`.

plone.reload
    An add-on that allows to reload code that you changed without restarting the site. It is also used by :py:mod:`plone.app.debugtoolbar`.

Products.PrintingMailHost
    An add-on that prevents Plone from sending mails. Instead, they are logged.

Products.enablesettrace or Products.Ienablesettrace
    Add-on that allows to use pdb and ipdb in Python skin scripts. Very useful when debugging legacy code.

``verbose-security = on``
    An option for the recipe :py:mod:`plone.recipe.zope2instance` that logs the detailed reasons why a user might not be authorized to see something.

:command:`./bin/buildout annotate`
    An option when running buildout that logs all the pulled packages and versions.

Sentry
    `Sentry <https://github.com/getsentry/sentry>`_ is an error logging application you can host yourself.
    It aggregates tracebacks from many sources and (here comes the killer feature) even the values of variables in the traceback. We use it in all our production sites.

zopepy
    Buildout can create a python shell for you that has all the packages from your Plone site in its python path. Add the part like this::

        [zopepy]
        recipe = zc.recipe.egg
        eggs = ${instance:eggs}
        interpreter = zopepy
