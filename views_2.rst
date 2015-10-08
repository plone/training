.. _views2-label:

Views II: A Default View for "Talk"
===================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/05_views_2_p5/ src/ploneconf.site

In this part you will:

* Register a view with a python class
* Write a template used in the default view for talks


Topics covered:

* View classes
* BrowserView and DefaultView
* displaying data from fields


.. _views2-classes-label:

View Classes
------------

Earlier we wrote a demo view which we also used to experiment with page templates.
Now we are going to enhance that view so that it will have some python code, in addition to a template.
Let us have a look at the zcml and the code.

``browser/configure.zcml``

.. code-block:: xml
    :linenos:
    :emphasize-lines:  8-9

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="ploneconf.site">

        <browser:page
           name="demoview"
           for="*"
           layer="zope.interface.Interface"
           class=".views.DemoView"
           template="templates/training.pt"
           permission="zope2.View"
           />

    </configure>

We are adding a file called ``views.py`` in the ``browser`` folder.

``browser/views.py``

.. code-block:: python
    :linenos:

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):
        """ This does nothing so far
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def __call__(self):
            # Implement your own actions

            # This renders the template that was registered in zcml like this:
            #   template="templates/training.pt"
            return super(DemoView, self).__call__()
            # If you don't register a template in zcml the Superclass of
            # DemoView will have no __call__-method!
            # In that case you have to call the template like this:
            # from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
            # class DemoView(BrowserView):
            # template = ViewPageTemplateFile('templates/training.pt')
            # def __call__(self):
            #    return self.template()

Do you remember the term MultiAdapter? The browser page is just a MultiAdapter. The ZCML statement ``browser:page`` registers a MultiAdapter and adds additional things needed for a browser view.

An adapter adapts things, a MultiAdapter adapts multiple things.

When you enter a url, Zope tries to find an object for it. At the end, when Zope does not find any more objects but there is still a path item left, or there are no more path items, Zope looks for an adapter that will reply to the request.

The adapter adapts the request and the object that Zope found with the URL. The adapter class gets instantiated with the objects to be adapted, then it gets called.

The code above does the same thing that the standard implementation would do. It makes ``context`` and ``request`` available as variables on the object.

I have written down these methods because it is important to understand some important concepts.

The ``__init__`` method gets called while Zope is still *trying* to find a view. At that phase, the security has not been resolved. Your code is not security checked. For historical reasons, many errors that happen in the ``__init__`` method can result in a page not found error instead of an exception.

Use the ``__init__`` method to do as little as possible, if at all. Instead, you have the guarantee that the ``__call__`` method is called before anything else (but after the ``__init__`` method). It has the security checks in place and so on.

From a practical standpoint, consider the ``__call__`` method your ``__init__`` method, the biggest difference is that this method is supposed to return the html already.
Let your base class handle the html generation.




.. _views2-default-label:

The default view
----------------

Now we finally add the default view for talks in views.py

``browser/configure.zcml``

.. code-block:: xml

    <browser:page
       name="talkview"
       for="*"
       layer="zope.interface.Interface"
       class=".views.TalkView"
       template="templates/talkview.pt"
       permission="zope2.View"
       />

``browser/views.py``

.. code-block:: python

    from plone.dexterity.browser.view import DefaultView

    ...

    class TalkView(DefaultView):
        """ The default view for talks
        """

The DefaultView base class in plone.dexterity only exists for Dexterity Objects and has some very useful properties available to the template:

* ``view.w`` is a dictionary of all the display widgets, keyed by field names. This includes widgets from alternative fieldsets.
* ``view.widgets`` contains a list of widgets in schema order for the default fieldset.
* ``view.groups`` contains a list of fieldsets in fieldset order.
* ``view.fieldsets`` contains a dict mapping fieldset name to fieldset
* On a fieldset (group), you can access a widget list to get widgets in that fieldset

.. note::

    ``plone.dexterity.browser.view.DefaultView`` has the same features as the grok equivalent ``plone.directives.dexterity.DisplayForm``.

The template ``templates/talkview.pt`` uses the pattern ``view/w/<fieldname>/render`` to render some widgets.

.. code-block:: xml
    :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en"
        metal:use-macro="context/main_template/macros/master"
        i18n:domain="ploneconf.site">
    <body>
        <metal:content-core fill-slot="content-core">
            <p>Suitable for <em tal:replace="structure view/w/audience/render"></em>
            </p>

            <div tal:content="structure view/w/details/render" />

            <div tal:content="context/speaker">
                User
            </div>
        </metal:content-core>
    </body>
    </html>

After a restart, we can test our view by going to a talk and adding */talkview* to the url.

We should tell Plone that the talkview should be used as the default view for talks instead of the built-in view.

This is a configuration that you can change during runtime and is stored in the database, as such it is also managed by GenericSetup profiles.

open ``profiles/default/types/talk.xml``:

.. code-block:: xml
    :linenos:
    :emphasize-lines: 2,4

    ...
    <property name="default_view">talkview</property>
    <property name="view_methods">
        <element value="talkview"/>
        <element value="view"/>
    </property>
    ...

We will have to either reinstall our add-on or run the GenericSetup import step ``typeinfo`` so Plone learns about the change.

..  note::

    To change it ttw got to the ZMI (http://localhost:8080/Plone/manage), go to ``portal_types`` and select the type for which the new view should be selectable (*talk*). Now add ``talkview`` to the list *Available view methods*. Now the new view is available in the menu *Display*. To make it the default view enter it in ``Default view method``.

Let's improve the talkview to show all the info we want.

``templates/talkview.pt``:

.. code-block:: xml
    :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>
        <metal:content-core fill-slot="content-core">

            <p>
                <span tal:content="context/type_of_talk">
                    Talk
                </span>
                suitable for
                <span tal:replace="structure view/w/audience/render">
                    Audience
                </span>
            </p>

            <div tal:content="structure view/w/details/render">
                Details
            </div>

            <div class="newsImageContainer">
                <img tal:condition="python:getattr(context, 'image', None)"
                     tal:attributes="src string:${context/absolute_url}/@@images/image/thumb" />
            </div>

            <div>
                <a class="email-link" tal:attributes="href string:mailto:${context/email}">
                    <strong tal:content="context/speaker">
                        Jane Doe
                    </strong>
                </a>
                <div tal:content="structure view/w/speaker_biography/render">
                    Biography
                </div>
            </div>

        </metal:content-core>
    </body>
    </html>

.. _views2-exercise-label:

Exercise
--------

Add the new choice field "room" to the Talk type (TTW) and display it below Audience in the browser view, it should contain the following data:

* Title: Room
* Possible values: Room 101, Room 102, Auditorium

..  admonition:: Solution
        :class: toggle

        * Go to http://localhost:8080/Plone/dexterity-types/talk/@@fields and add the new field
        * Add the new HTML below the audience part:

        .. code-block:: xml

            <p>
                <span tal:replace="structure view/w/room/render">
                    Room
                </span>
            </p>


.. seealso::

    http://docs.plone.org/develop/plone/views/browserviews.html

