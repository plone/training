.. _viewlets1-label:

Writing Viewlets
================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/08_viewlets_1_p5/ src/ploneconf.site


In this part you will:

* Display data from a behavior in a viewlet

Topics covered:

* Viewlets

.. _viewlets1-social-label:

A viewlet for the social behavior
---------------------------------

.. only:: not presentation

    A viewlet is not a view but a snippet of html and logic that can be put in various places in the site. These places are called ``viewletmanager``.

* Inspect existing viewlets and their managers by going to http://localhost:8080/Plone/@@manage-viewlets.
* We already customized a viewlet (:file:`colophon.pt`). Now we add a new one.
* Viewlets don't save data (portlets do)
* Viewlets have no user interface (portlets do)

.. _viewlets1-social2-label:

Social viewlet
--------------

.. only:: not presentation

    Let's add a link to the site that uses the information that we collected using the social behavior.

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

``for``, ``manager``, ``layer`` and ``permission`` are constraints that limit the contexts in which the viewlet is loaded and rendered, by filtering out all the contexts that do not match those constraints.

.. only:: not presentation

    This registers a viewlet called ``social``.
    It is visible on all content that implements the interface ``ISocial`` from our behavior.
    It is also good practice to bind it to a specific ``layer``, so it only shows up if our add-on is actually installed.  We will return to this in a later chapter.

The viewlet class ``SocialViewlet`` is expected in a file ``browser/viewlets.py``.

.. _BrowserLayer: http://docs.plone.org/develop/plone/views/layers.html?highlight=browserlayer#introduction

.. code-block:: python
    :linenos:

    from plone.app.layout.viewlets import ViewletBase

    class SocialViewlet(ViewletBase):
        pass


.. only:: not presentation

    This class does nothing except rendering the associated template (That we have yet to write)

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


.. only:: not presentation

    As you can see this is not a valid html document. That is not needed, because we don't want a complete view here, just a html snippet.

    There is a tal define statement, querying for ``view/lanyrd_link``. Same as for views, viewlets have access to their class in page templates, as well.

We have to extend the Social Viewlet now to add the missing attribute:


.. only:: not presentation

    .. sidebar:: Why not to access context directly

        In this example, :samp:`ISocial(self.context)` does return the context directly. It is still good to use this idiom for two reasons:

          #. It makes it clear that we only want to use the ISocial aspect of the object
          #. If we decide to use a factory, for example to store our attributes in an annotation, we would `not` get back our context, but the adapter.

        Therefore in this example you could simply write ``return self.context.lanyrd``.

.. code-block:: python
    :linenos:
    :emphasize-lines: 2, 6-8

    from plone.app.layout.viewlets import ViewletBase
    from ploneconf.site.behaviors.social import ISocial

    class SocialViewlet(ViewletBase):

        def lanyrd_link(self):
            adapted = ISocial(self.context)
            return adapted.lanyrd

So far, we

  * register the viewlet to content that has the ISocial Interface.
  * adapt the object to its behavior to be able to access the fields of the behavior
  * return the link


.. _viewlets1-excercises-label:

Exercise 1
----------

Register a viewlet 'number_of_talks' in the footer that is only visible to admins (the permission you are looking for is ``cmf.ManagePortal``). Use only a template (no class) to display the number of talks already submitted. Hint: Use Acquisition to get the catalog (You know, you should not do this but there is plenty of code out there that does it...)

..  admonition:: Solution
    :class: toggle

    Register the viewlet in :file:`browser/configure.zcml`

    ..  code-block:: xml

        <browser:viewlet
          name="number_of_talks"
          for="*"
          manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
          layer="zope.interface.Interface"
          template="templates/number_of_talks.pt"
          permission="cmf.ManagePortal"
          />


    For the ``for`` and ``layer``-parameters ``*`` is shorthand for ``zope.interface.Interface`` and the same effect as omitting them: The viewlet will be shown for all types of pages and for all Plone sites within your Zope instance.

    Add the template :file:`browser/templates/number_of_talks.pt`:

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog python:context.portal_catalog;
                         talks python:len(catalog(portal_type='talk'));">
            There are <span tal:replace="talks" /> talks.
        </div>

    ``python:context.portal_catalog`` will return the catalog through Acquisition. Be careful if you want to use path expressions: ``content/portal_catalog`` calls the catalog (and returns all brains). You need to prevent this by using ``nocall:content/portal_catalog``.

    Relying on Acquisition is a bad idea. It would be much better to use the helper view ``plone_tools`` from ``plone/app/layout/globals/tools.py`` to get the catalog.

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog context/@@plone_tools/catalog;
                         talks python:len(catalog(portal_type='talk'));">
            There are <span tal:replace="talks" /> talks.
        </div>

    ``context/@@plone_tools/catalog`` traverses to the view ``plone_tools`` and calls its method ``catalog``. In python it would look like this:

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog python:context.restrictedTraverse('plone_tools').catalog();
                         talks python:len(catalog(portal_type='talk'));">
            There are <span tal:replace="talks" /> talks.
        </div>

    It is not a good practice to query the catalog within a template since even simple logic like this should live in Python. But it is very powerful if you are debugging or need a quick and dirty solution.

    In Plone 5 you could even write it like this:

    ..  code-block:: html

        <?python

        from plone import api
        catalog = api.portal.get_tool('portal_catalog')
        talks_amount = len(catalog(portal_type='talk'))

        ?>

        <div class="number_of_talks">
            There are ${talks_amount} talks.
        </div>


Exercise 2
----------

Register a viewlet 'days_to_conference' in the header. Use a class and a template to display the number of days until the conference. You get bonus points if you display it in a nice format (think "In 2 days" and "Last Month") by using either javascript or a python library.

..  admonition:: Solution
    :class: toggle

    In ``configure.zcml``:

    ..  code-block:: xml

        <browser:viewlet
          name="days_to_conference"
          for="*"
          manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
          layer="*"
          class=".viewlets.DaysToConferenceViewlet"
          template="templates/days_to_conference.pt"
          permission="zope2.View"
          />

    In ``viewlets.py``:

    ..  code-block:: python

        from plone.app.layout.viewlets import ViewletBase
        from datetime import datetime
        import arrow

        CONFERENCE_START_DATE = datetime(2015, 10, 12)


        class DaysToConferenceViewlet(ViewletBase):

            def date(self):
                return CONFERENCE_START_DATE

            def human(self):
                return arrow.get(CONFERENCE_START_DATE).humanize()


    And in ``templates/days_to_conference.pt``:

    ..  code-block:: html

        <div class="days_to_conf">
            ${python: view.human()}
        </div>

    Or using the moment pattern in Plone 5:

    ..  code-block:: html

        <div class="pat-moment"
             data-pat-moment="format: relative">
            ${python: view.date()}
        </div>
