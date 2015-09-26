
Grok
====

Grok is an alternative declaration language for declaring your components. It is compatible with the Zope Component Architecture, it used just an alternative syntax. It is recommended to not use it! We still document it here in case you have to deal with a legacy-codebase that uses it.

Instead of writing separate zcml files, you annotate your code and you create content conforming to specific file names so that they are automatically found.
There has been discussions whether grok should be used in the plone core. The plone community decided against it, because it increases the technology stack without adding functionality.

Some people are even against using it in Add Ons, because there would not be just one way to declare components, but two. Then there is only last disadvantage, grok components cannot be overridden by z3c.jbot. I would not be surprised if this could be fixed though.

After all these negative things let us tell you why we still like it: We like to write as few lines of code and configuration as possible.

So, we will write our browser view as a grok view. From the component architecture side, nothing changes. We still need to write a multi adapter. All the details like which template to use or for which browser layer the view shall be used is declared with a single line annotation or deduced from file names.

.. seealso::

    http://docs.plone.org/develop/addons/five-grok/index.html

Grok is not part of plone. We have to add it as a dependency to our egg.

Open setup.py, and add ``five.grok`` to the list off add-ons in ``install_requires``::

    ...
        zip_safe=False,
        install_requires=[
            'setuptools',
            'five.grok',
        ],

You need to run buildout now.

Grok nearly magically does find all its annotations. Since its not complete magic, you have to tell grok where to look for grok code. This requires a single line of zcml, that line ensures that your complete package is `grokked`.

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6,12

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        xmlns:grok="http://namespaces.zope.org/grok"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="ploneconf.site">

        <includeDependencies package="." />

        <grok:grok package="." />
        ....

This new grok statement takes care of finding everything grok related.

Now we can add a grok view in a new file ``views.py``:

.. code-block:: python
    :linenos:

    from five import grok
    from plone.directives import dexterity
    from zope.interface import Interface


    class TalkView(dexterity.DisplayForm):
        grok.require("zope2.View")
        grok.context(Interface)

By convention the template must be in a subdirectory called ``views_templates`` and it must be named `talkview.pt`

If we used ``grok`` for viewlets we would not need to register them in the ``configure.zcml`` but do that in python. We would add a file viewlets.py containing the viewlet-class.

.. code-block:: python
    :linenos:

    from five import grok
    from plone.app.layout.viewlets import interfaces as viewletIFs
    from zope.component import Interface

    class SocialViewlet(grok.Viewlet):
        grok.viewletmanager(viewletIFs.IBelowContentTitle)

This would do the same as the code above using grok's paradigm of convention over configuration. In browser views the reference is called view, note that in grok viewlets it is called viewlets (in that case ``viewlet/lanyrd_link``).
