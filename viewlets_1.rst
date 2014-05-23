Writing Viewlets
================

A viewlet for the social behavior
---------------------------------

.. only:: manual

    A viewlet is no view but a snippet of html and logic that can be put in various places in the site. These places are called ``viewletmanager``.

* Inspect existing viewlets and their managers by going to http://localhost:8080/Plone/@@manage-viewlets.
* We already customized a viewlet (:file:`collophon.pt`). Now we add a new one.
* Viewlets don't save data (portlets do)
* Viewlets have no user-interface (portlets do)

social-viewlet
--------------

.. only:: manual

    Let's add a link to the site that uses the information that we collected using the social-behavior.

We register the viewlet in :file:`browser/configure.zcml`.

.. code-block:: xml
    :linenos:

    <browser:viewlet
      name="social"
      for="ploneconf.site.behaviors.social.ISocial"
      manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
      class=".viewlets.SocialViewlet"
      layer="zope.interface.Interface"
      template="templates/social_viewlet.pt"
      permission="zope2.View"
      />

.. only:: manual

    This registers a viewlet called ``social``.
    It is visible on all content that implements the interface ``ISocial`` from our behavior.
    It is also good practice to bind it to the `BrowserLayer`_ ``IPloneconfSiteLayer`` of our addon so it only shows up if our addon is actually installed.

The viewlet-class ``SocialViewlet`` is expected in a file ``browser/viewlets.py``.

.. _BrowserLayer: http://docs.plone.org/develop/plone/views/layers.html?highlight=browserlayer#introduction

.. code-block:: python
    :linenos:

    from plone.app.layout.viewlets import ViewletBase

    class SocialViewlet(ViewletBase):
        pass


.. only:: manual

    This class does nothing except rendering the associated template (That we have to write yet)

    .. note::

        If we used ``grok`` we would not need to register the viewlets in the ``configure.zcml`` but do that in python. We would add a file viewlets.py containing the viewlet-class.

        .. code-block:: python
            :linenos:

            from five import grok
            from plone.app.layout.viewlets import interfaces as viewletIFs
            from zope.component import Interface

            class Social(grok.Viewlet):
                grok.viewletmanager(viewletIFs.IBelowContentTitle)

        This would do the same as the coe above using grok's paradigm of convention over configuration.

Let's add the missing template :file:`templates/social_viewlet.pt`.

.. code-block:: html
    :linenos:

    <div id="social-links">
        <a href="#"
           class="lanyrd-link"
           tal:define="link view/lanyrd_link"
           tal:condition="link"
           tal:attributes="href link">
             See this talk on Lanyrd!
        </a>
    </div>


.. only:: manual

    As you can see this is not a valid html document. That is not needed, because we don't want a complete view here, just a html snippet.

    There is a tal define statement, querying for viewlet/lanyrd_link. Like in page templates the template has access to its class. In browser views the reference is called view, in viewlets it is called viewlets.

We have to extend the Social Viewlet now to add the missing attribute:


.. only:: manual

    .. sidebar:: Why not to access context directly

        In this example, :samp:`ISocial(self.context)` does return the context directly. It is still good to use this idiom for two reasons:

          #. It makes it clear, that we only want to use the ISocial aspect of the object
          #. If we decide to use a factory, for example to store our attributes in an annotation, we would `not` get back our context, but the adapter

.. code-block:: python
    :linenos:
    :emphasize-lines: 5-7
    
    ...
    from ploneconf.site.behaviors.social import ISocial

    class Social(ViewletBase):

        def lanyrd_link(self):
            adapted = ISocial(self.context)
            return adapted.lanyrd

So far, we

  * register the viewlet to content that has the ISocial Interface.
  * adapt the object to it's behavior to be able to access the fields of the behavior
  * return the link
