.. _frontpage-label:

Creating a Dynamic Front Page
=============================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/XXX/ src/ploneconf.site


In this chapter we will:

* Create a standalone view used for the front page
* Show some dynamic content on said view
* Embed tweets about ploneconf

The topics we cover are:

* standalone views
* querying the catalog by date
* working with datetime objects
* DRY
* macros


The Front Page
--------------

Register the view in ``browser/configure.zcml``:


..  code-block:: xml

    <browser:page
        name="frontpageview"
        for="*"
        layer="..interfaces.IPloneconfSiteLayer"
        class=".frontpage.frontpageView"
        template="templates/frontpageview.pt"
        permission="zope2.View"
        />

Add the view to a file ``browser/frontpage.py``. We want a list of all talks that happen today.

..  code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-
    from plone import api
    from Products.Five.browser import BrowserView

    import datetime


    class frontpageView(BrowserView):
        """The view of the conference frontpage
        """

        def talks(self):
            """Get today's talks"""
            results = []
            catalog = api.portal.get_tool('portal_catalog')
            today = datetime.date.today()
            brains = catalog(
                portal_type='talk',
                sort_on='start',
                sort_order='descending'
            )
            for brain in brains:
                if brain.start.date() == today:
                    results.append({
                        'title': brain.Title,
                        'description': brain.Description,
                        'url': brain.getURL(),
                        'audience': ', '.join(brain.audience or []),
                        'type_of_talk': brain.type_of_talk,
                        'speaker': brain.speaker,
                        'uuid': brain.UID,
                        'start': brain.start,
                        'room': brain.room,
                        })
            return results

* With ``if brain.start.date() == today:`` we test if the talk is today.
* It would be more effective to query the catalog for events that happen in the daterange between today and tomorrow:

  ..  code-block:: python
      :linenos:
      :emphasize-lines: 2, 3, 6

      today = datetime.date.today()
      tomorrow = today + datetime.timedelta(days=1)
      date_range_query = {'query': (today, tomorrow), 'range': 'min:max'}
      brains = catalog(
          portal_type='talk',
          start=date_range_query,
          sort_on='start',
          sort_order='ascending'
      )

* The ``sort_on='start'`` sorts the results returned by the catalog by start-date.
* By removing the ``portal_type='talk'`` from the query you could include other events in the schedule (like the party or sightseeing-tours). But you'd have to take care to not create AttributeErrors by accessing fields that are specific to talk. To work around that use ``speaker = getattr(brain, 'speaker', None)`` and testing with ``if speaker is not None:``
* The rest is identical to what the talklistview does.


The template
------------

Create the template ``browser/templates/frontpageview.pt`` (for now without talks). Display the rich text field talk to allow the frontpage to be edited.

..  code-block:: html
    :linenos:


    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>

    <metal:content-core fill-slot="content-core">

        <div id="parent-fieldname-text"
            tal:condition="python: getattr(context, 'text', None)"
            tal:content="structure python:context.text.output_relative_to(view.context)" />

    </metal:content-core>

    </body>
    </html>

Now you could add the whole code again that we used for the talklistview. But instead we go D.R.Y. and reuse the talklistview by turning it into a macro.

Edit ``browser/templates/talkslistview.pt`` and wrap the list in a macro definition:

..  code-block:: html
    :linenos:
    :emphasize-lines: 8, 70

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>

    <metal:content-core fill-slot="content-core">

    <metal:talklist define-macro="talklist">

    <table class="listing pat-tablesorter" id="talks">
        <thead>
            <tr>
                <th>
                    Title
                </th>
                <th>
                    Speaker
                </th>
                <th>
                    Audience
                </th>
                <th>
                    Time
                </th>
                <th>
                    Room
                </th>
            </tr>
        </thead>
        <tbody>
            <tr tal:repeat="talk view/talks">
                <td>
                    <a href=""
                       class="pat-contentloader"
                       data-pat-contentloader="url:${talk/url}?ajax_load=1; target:.talkinfo > *"
                       tal:attributes="href string:${talk/url};
                                       title talk/description"
                       tal:content="talk/title">
                       The 7 sins of plone development
                    </a>
                </td>
                <td tal:content="talk/speaker">
                    Philip Bauer
                </td>
                <td tal:content="talk/audience">
                    Advanced
                </td>
                <td tal:content="talk/start"
                    class="pat-moment"
                    data-pat-moment="format: LT">
                    12:00 a.m.
                </td>
                <td tal:content="talk/room">
                    Room 212
                </td>

            </tr>
            <tr tal:condition="not:view/talks">
                <td colspan=3>
                    No talks
                </td>
            </tr>
        </tbody>
    </table>

    <div class="talkinfo">
        <span />
    </div>

    </metal:talklist>

    </metal:content-core>
    </body>
    </html>

Now use that macro in ``browser/templates/frontpageview.pt``

..  code-block:: html
    :linenos:
    :emphasize-lines: 8, 70

    <div class="col-lg-6">
        <h2>Todays Talks</h2>
        <div metal:use-macro="context/@@talklistview/talklist">
            Instead of this the content of the macro will appear...
        </div>
    </div>

Calling the macro in python looks like this  ``metal:use-macro="python:context.restrictedTraverse('talklistview')['talklist']"``

.. note::

    In ``talklistview.pt`` the call ``view/talks"`` calls the method ``talks`` from the browser view ``TalkListView`` to get the talks. Reused as a macro on the frontpage it now uses the method ``talks`` by the ``frontpageView`` to get a different list!

    Also: It is not always smart to do that since maybe you want to display other data.


Twitter
-------

You might also want to embed a twitter feed into the page. Luckily twitter makes it easy to do that. Please browse to the `twitter docs <https://dev.twitter.com/web/embedded-timelines>`_ and learn how to create the appropriate snippet of code and paste it in the template wrapped in a ``<div class="col-lg-6">...</div>`` to have the talklist next to the feeds:

..  code-block:: html

    <div class="col-lg-6">
        <a class="twitter-timeline"  href="https://twitter.com/hashtag/ploneconf" data-widget-id="571666061712687104">#ploneconf-Tweets</a>
        <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
    </div>


Activating the view
-------------------

The view is meant to be used with documents (or any other type that has a rich text field 'text'). The easiest way to use it is setting it as the default view for the Document that is currently the default page for the portal. By default that document has the id ``front-page``.

You can either access it directly at http://localhost:8080/Plone/front-page or by disabling the default page for the portal and it should show up in the navigation. Try out the new view like this: http://localhost:8080/Plone/front-page/frontpageview.

To set that view by hand as the default view for ``front-page`` in the ZMI: http://localhost:8080/Plone/front-page/manage_propertiesForm. Add a new property ``layout`` and set it to ``frontpageview``.

Done. This way you can still use the button *Edit* to edit the frontpage.


.. seealso::

   * Querying by date: http://docs.plone.org/develop/plone/searching_and_indexing/query.html#querying-by-date
