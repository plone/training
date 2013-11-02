Views II: A default view for "talk"
===================================

Earlier we wrote a demo view which we also used to experiment with page templates.
Let us have a look at the zcml and the Page Template again.
I have extended the code just slightly.

ZCML

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="ploneconf.talk">

        <browser:page
           name="demoview"
           for="*"
           layer="zope.interface.Interface"
           class=".views.DemoView"
           template="templates/demoview.pt"
           permission="zope2.View"
           />

    </configure>

Code ::

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):
        """ This does nothing so far
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            # Do stuff
            return super(DemoView, self).__call__()

Do you remember the term MultiAdapter? The browser page is just a multiadapter.
The zcml Statement browser:page registeres a multiadapter and adds additional things needed for a browser view.
An adapter adapts things, a multi adapter adapts multiple things.
When you enter an url, Zope tries to find an object for it. At the end, when zope does not find any more objects but there is still a path item left, or there are no more path items, Zope looks for an adapter that will reply to the request.
The Adapter adapts the request and the object that zope found with the URL.
The adapter class gets instanciated with the objects to be adapted, then it gets called.

The code above does the same thing that the standard implementation would do. It makes context and request available as variables on the object.
I have written down these methods because it important to understand some important concepts.
The init method gets called while Zope is still *trying* to find a view. At that phase, the security has not been resolved. Your code is not security checked. For historic reasons, many errors that happen in the init method can result in a page not found error instead of an exception.
Don't do much at all in the init method.
Instead you have the guarantee the the call method is called before anything else (except the init method). It has the security checks in place and so on.
From a practical standpoint, consider the call method your init method, the biggest difference is that this method is suposed to return the html already.
Let your base class handle the html generation.


Grok
----
Now that we know how to read a zcml statement, we can continue with grok.
Grok is an alternative declaration language for declaring your components. It is compatible with the Zope Component Architecture, it used just an alternative syntax.
Instead of writing separate zcml files, you annotate your code and you create content conforming to specific file names so that they are automatically found.
There has been discussions whether grok should be used in the plone core. The plone community decided against it, because it increases the technology stack without adding functionality.
Some people are even against using it in Add Ons, because there would not be just one way to declare components, but two. Then there is onle last disadvantage, grok components cannot be overridden by z3c.jbot. I would not be surprised if this could be fixed though.
After all these negative things let us tell you why we still like it: We like to write as few lines of code and configuration as possible.

So, we will write our browser view as a grok view. From the component architecture side, nothing changes. We still need to write a multi adapter. All the details like which template to use or for which browser layer the view shall be used is declared with a single line annotation or deduced from file names.

Grok is not part of plone. We have to add it as a dependency to our egg.

open setup.py, extended it like this::

    ...
        zip_safe=False,
        install_requires=[
            'setuptools',
            'plone.app.dexterity [grok]',
            # -*- Extra requirements: -*-
        ],
        extras_require={'test': ['plone.app.testing']},
        ...

You need to run buildout now.

Grok nearly magicaly does find all its annotations. Since its not complete magic, you have to tell grok where to look for grok code. This requires a single line of zcml, that line ensures that your complete package is `grokked`.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        xmlns:grok="http://namespaces.zope.org/grok"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="ploneconf.talk">

        <includeDependencies package="." />

        <grok:grok package="." />
        ....

This new grok statement takes care of finding everything grok related.

Now finally on to the grok view in a new file views.py::

    from five import grok
    from plone.directives import dexterity
    from zope.interface import Interface


    class TalkView(dexterity.DisplayForm):  # grok.View + dexterity information
        grok.require("zope2.View")
        grok.context(Interface)

And the template. Important, the template must be in a subdirectory called `views_templates` and it must be named `talkview.pt`::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en"
        metal:use-macro="context/main_template/macros/master"
        i18n:domain="plonekonf.talk">
    <body>
        <metal:content-core fill-slot="content-core">
            <p>Suitable for <em tal:replace="structure view/w/audience/render"></em>
            </p>

            <div tal:content="structure view/w/details/render" />

            <div>Presenter:
                <p>
                    <strong tal:content="context/Creator">
                    User
                    </strong>
                </p>
            </div>
        </metal:content-core>
    </body>
    </html>

*Go through the code line by line*

After a restart, we can test our view by going to a talk and add /talkview to the url.

If you are happy with it, you must tell Plone, that this view shall be the default view.
This is a configuration that you can change during runtime and is stored in the database, as such it is also managed by genericsetup profiles.

open profiles/default/types/talk.xml::

    ...
    <property name="allow_discussion">False</property>
    <property name="default_view">talkdefaultview</property>
    <property name="view_methods">
        <element value="talkdefaultview"/>
    </property>
    <property name="default_view_fallback">False</property>
    ...
