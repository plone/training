.. _views2-label:

Views II: A Default View for "Talk"
===================================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: bash

        git checkout views_2

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
    :emphasize-lines:  8

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="ploneconf.site">

        <browser:page
           name="demoview"
           for="*"
           class=".views.DemoView"
           template="templates/training.pt"
           permission="zope2.View"
           />

    </configure>

We are adding a file called :file:`views.py` in the :file:`browser` folder.

:file:`browser/views.py`

.. code-block:: python
    :linenos:

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):
        """ This does nothing so far
        """

        def the_title(self):
            return u'A list of great trainings:'

In the template :file:`training.pt` we can now use this view as `view` and access all its methods and properties:

.. code-block:: html

    <h2 tal:content="python: view.the_title()" />

The logic contained in that file can now be moved to the class:

.. code-block:: python
    :linenos:
    :emphasize-lines: 3, 12-39

    # -*- coding: utf-8 -*-
    from Products.Five.browser import BrowserView
    from operator import itemgetter


    class DemoView(BrowserView):
        """A demo listing"""

        def the_title(self):
            return u'A list of talks:'

        def talks(self):
            results = []
            data = [
                {'title': 'Dexterity is the new default!',
                 'subjects': ('content-types', 'dexterity')},
                {'title': 'Mosaic will be the next big thing.',
                 'subjects': ('layout', 'deco', 'views'),
                 'url': 'https://www.youtube.com/watch?v=QSNufxaYb1M'},
                {'title': 'The State of Plone',
                 'subjects': ('keynote',)},
                {'title': 'Diazo is a powerful tool for theming!',
                 'subjects': ('design', 'diazo', 'xslt')},
                {'title': 'Magic templates in Plone 5',
                 'subjects': ('templates', 'TAL'),
                 'url': 'http://www.starzel.de/blog/magic-templates-in-plone-5'},
            ]
            for item in data:
                try:
                    url = item['url']
                except KeyError:
                    url = 'https://www.google.com/search?q=%s' % item['title']
                talk = dict(
                    title=item['title'],
                    subjects=', '.join(item['subjects']),
                    url=url
                )
                results.append(talk)
            return sorted(results, key=itemgetter('title'))

And the template will now be much simpler.

.. code-block:: html
    :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>

    <metal:content-core fill-slot="content-core">

    <h2 tal:content="python: view.the_title()" />

    <table class="listing">
        <tr>
            <th>Title</th>
            <th>Topics</th>
        </tr>

        <tr tal:repeat="talk python:view.talks()">
            <td>
                <a href="${python:talk['url']}">
                    ${python:talk['title']}
                </a>
            </td>
            <td>
                ${python:talk['subjects']}
            </td>
        </tr>
    </table>

    </metal:content-core>

    </body>
    </html>


.. _views2-default-label:

The default view
----------------

Using a view you can now create a nice view for talks in :file:`views.py`.
First we will not write any methods for `view` but instead access the fields from the talk-schema as `context.<fieldname>`.

Register a view `talkview` in :file:`browser/configure.zcml`:

.. code-block:: xml

    <browser:page
       name="talkview"
       for="*"
       layer="zope.interface.Interface"
       class=".views.TalkView"
       template="templates/talkview.pt"
       permission="zope2.View"
       />

:file:`browser/views.py`

.. code-block:: python

    class TalkView(BrowserView):
        """ The default view for talks"""

Add the template :file:`templates/talkview.pt`:

.. code-block:: xml
    :linenos:

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
        lang="en"
        metal:use-macro="context/main_template/macros/master"
        i18n:domain="ploneconf.site">
    <body>
        <metal:content-core fill-slot="content-core">
            <p>Suitable for <em tal:content="python: ', '.join(context.subject)"></em>
            </p>

            <div tal:condition="python: context.details"
                 tal:content="structure python: context.details.output" />

            <div tal:content="python: context.speaker">
                User
            </div>
        </metal:content-core>
    </body>
    </html>

After a restart, we can test our view by going to a talk and adding */talkview* to the url.


Using helper-methods from :py:class:`DefaultView`
-------------------------------------------------

Dexterity comes with a nice helper-class suited for views of content-types: The :py:class:`DefaultView` base class in :py:mod:`plone.dexterity`.
It only works for Dexterity Objects and has some very useful properties available to the template:

* :py:attr:`view.w` is a dictionary of all the display widgets, keyed by field names. This includes widgets from alternative fieldsets.
* :py:attr:`view.widgets` contains a list of widgets in schema order for the default fieldset.
* :py:attr:`view.groups` contains a list of fieldsets in fieldset order.
* :py:attr:`view.fieldsets` contains a dict mapping fieldset name to fieldset
* On a fieldset (group), you can access a widget list to get widgets in that fieldset

You can now change the :py:class:`TalkView` to use that

.. code-block:: python

    from plone.dexterity.browser.view import DefaultView

    ...

    class TalkView(DefaultView):
        """ The default view for talks
        """

The template :file:`templates/talkview.pt` still works but now you can modify it to use the pattern :samp:`view/w/<fieldname>/render` to render the widgets:

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

After a restart, we can test the modified view by going to a talk and adding */talkview* to the url.

We should tell Plone that the talkview should be used as the default view for talks instead of the built-in view.

This is a configuration that you can change during runtime and is stored in the database, as such it is also managed by GenericSetup profiles.

open :file:`profiles/default/types/talk.xml`:

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

:file:`templates/talkview.pt`:

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


Behind the scenes
-----------------

.. code-block:: python
    :linenos:

    from Products.Five.browser import BrowserView

    class DemoView(BrowserView):

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

Do you remember the term :py:class:`MultiAdapter`? The browser page is just a MultiAdapter. The ZCML statement :samp:`browser:page` registers a :py:class:`MultiAdapter` and adds additional things needed for a browser view.

An adapter adapts things, a :py:class:`MultiAdapter` adapts multiple things.

When you enter a url, Zope tries to find an object for it. At the end, when Zope does not find any more objects but there is still a path item left, or there are no more path items, Zope looks for an adapter that will reply to the request.

The adapter adapts the request and the object that Zope found with the URL. The adapter class gets instantiated with the objects to be adapted, then it gets called.

The code above does the same thing that the standard implementation would do. It makes :py:attr:`context` and :py:attr:`request` available as variables on the object.

I have written down these methods because it is important to understand some important concepts.

The :py:meth:`__init__` method gets called while Zope is still *trying* to find a view. At that phase, the security has not been resolved. Your code is not security checked. For historical reasons, many errors that happen in the :py:meth:`__init__` method can result in a page not found error instead of an exception.

Use the :py:meth:`__init__` method to do as little as possible, if at all. Instead, you have the guarantee that the :py:meth:`__call__` method is called before anything else (but after the :py:meth:`__init__` method). It has the security checks in place and so on.

From a practical standpoint, consider the :py:meth:`__call__` method your :py:meth:`__init__` method, the biggest difference is that this method is supposed to return the HTML already.
Let your base class handle the HTML generation.

.. seealso::

    http://docs.plone.org/develop/plone/views/browserviews.html

