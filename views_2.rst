Views II: A default view for "talk"
===================================

View-Classes
------------

Earlier we wrote a demo view which we also used to experiment with page templates.
Let us have a look at the zcml and the Page Template again.
I have extended the code just slightly.

ZCML

.. code-block:: xml
    :linenos:

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="ploneconf.site">

        <browser:page
           name="demoview"
           for="*"
           layer="zope.interface.Interface"
           class=".views.DemoView"
           template="templates/demoview.pt"
           permission="zope2.View"
           />

    </configure>

Code

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
            # Do stuff
            return super(DemoView, self).__call__()

Do you remember the term MultiAdapter? The browser page is just a MultiAdapter. The ZCML statement ``browser:page`` registers a MultiAdapter and adds additional things needed for a browser view.

An adapter adapts things, a MultiAdapter adapts multiple things.

When you enter an url, Zope tries to find an object for it. At the end, when Zope does not find any more objects but there is still a path item left, or there are no more path items, Zope looks for an adapter that will reply to the request.

The adapter adapts the request and the object that Zope found with the URL. The adapter class gets instantiated with the objects to be adapted, then it gets called.

The code above does the same thing that the standard implementation would do. It makes context and request available as variables on the object.

I have written down these methods because it important to understand some important concepts.

The init method gets called while Zope is still *trying* to find a view. At that phase, the security has not been resolved. Your code is not security checked. For historic reasons, many errors that happen in the init method can result in a page not found error instead of an exception.

Don't do much at all in the init method. Instead you have the guarantee that the call method is called before anything else (except the init method). It has the security checks in place and so on.

From a practical standpoint, consider the call method your init method, the biggest difference is that this method is supposed to return the html already.
Let your base class handle the html generation.


The default-view
----------------

Now we finally add the default-view for talks in views.py

``configure.zcml``

.. code-block:: xml

    <browser:page
       name="talkview"
       for="*"
       layer="zope.interface.Interface"
       class=".views.TalkView"
       template="templates/talkview.pt"
       permission="zope2.View"
       />

``views.py``

.. code-block:: python

    from plone.dexterity.browser.view import DefaultView

    ...

    class TalkView(DefaultView):
        """ The default view for talks
        """

The DefaultView base class in plone.dexterity only exists for Dextertity-Objects and has some very useful available to the template:

* view.w is a dictionary of all the display widgets, keyed by field names. This includes widgets from alternative fieldsets.
* view.widgets contains a list of widgets in schema order for the default fieldset.
* view.groups contains a list of fieldsets in fieldset order.
* view.fieldsets contains a dict mapping fieldset name to fieldset
* On a fieldset (group), you can access a widgets list to get widgets in that fieldset

.. note::

    ``plone.dexterity.browser.view.DefaultView`` has the same features as the grok-equivalent ``plone.directives.dexterity.DisplayForm``.

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

After a restart, we can test our view by going to a talk and add /talkview to the url.

We should tell Plone, that the talkview should be used as the default view for talks instead of the built-in view.

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

We will have to either reinstall our addon or run the generic-setup step ``typeinfo`` so Plone learns about the change.

We could also tell plone about this in the ZMI: http://localhost:8080/Plone/portal_types/talk/manage_propertiesForm

Let's improve the talkview to show all the info we want.

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

.. seealso::

    http://docs.plone.org/develop/plone/views/browserviews.html

