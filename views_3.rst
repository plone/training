Views III: A Talk list
=======================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <sneak>`) using this command in the buildout-directory:

    .. code-block:: bash

        cp -R src/ploneconf.site_sneak/chapters/18_views_3/ src/ploneconf.site


Now we don't want to provide information about one specific item but on several items. What now? We can't look at several items at the same time as context.


Using portal_catalog
--------------------

Let's say we want to show a list of all the talks that were submitted for our conference. We can just go to the folder and select a display-method that suits us. But none does because we want to show the target-audience in our listing.

So we need to get all the talks. For this we use the python-class of the view to query the catalog for the talks.

The catalog is like a search-engine for the content on our site. It holds information about all the objects as well as some of their attributes like title, decription, workflow_state, keywords that they were tagged with, author, content_type, it's path in the site etc. But it does not hold the content of "heavy" fields like images or files, richtext-fields and field that we just defined ourselves.

It is the fast way to get content that exists in the site and do something with it. From the results of the catalog we can get the objects themselves but often we don't need them, but only the properties that the results already have.

``browser/configure.zcml``

.. code-block:: xml
    :linenos:

    <browser:page
       name="talklistview"
       for="*"
       layer="zope.interface.Interface"
       class=".views.TalkListView"
       template="templates/talklistview.pt"
       permission="zope2.View"
       />

``browser/views.py``

.. code-block:: python
    :linenos:

    from Products.Five.browser import BrowserView
    from plone import api
    from plone.dexterity.browser.view import DefaultView


    class DemoView(BrowserView):
        """ This does nothing so far
        """


    class TalkView(DefaultView):
        """ The default view for talks
        """


    class TalkListView(BrowserView):
        """ A list of talks
        """

        def talks(self):
            results = []
            portal_catalog = api.portal.get_tool('portal_catalog')
            current_path = "/".join(self.context.getPhysicalPath())

            brains = portal_catalog(portal_type="talk",
                                    path=current_path)
            for brain in brains:
                talk = brain.getObject()
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(talk.audience),
                    'type_of_talk': talk.type_of_talk,
                    'speaker': talk.speaker,
                    'uuid': brain.UID,
                    })
            return results

We query the catalog for two things:

* ``portal_type = "talk"``
* ``path = "/".join(self.context.getPhysicalPath())``

We get the path of the current context to query only for objects in the current path. Otherwise we'd get all talks in the whole site. If we moved some talks to a different part of the site (e.g. a sub-conference for universities with a special talk-list) we might not want so see them in our listing.

We iterate over the list of results that the catalog returns us.

We create a dictionary that holds all the information we want to show in the template. This way we don't have to put any complex logic into the template.

brains and objects
------------------

Objects are normally not loaded into memory but lie dormant in the Database ZODB. Waking objects up can be slow, especially if you're waking up a lot of objects. Fortunately our talks are not especially heavy since they are:

* dexterity-objects which are lighter than their archetypes-brothers
* relatively few since we don't have thousands of talks at our conference

We want to show the target-audience but that attributes of the talks is not in the catalog. This is why we need to get to the objects themselves.

We could also add a new index to the catalog that will add 'audience' to the properties of the brains, we have to weight pros and cons:

* talks are important and thus most likely always in memory
* prevent bloating of catalog with indexes

.. note::

    The code to add such an index would look like this::

        from plone.indexer.decorator import indexer
        from ploneconf.site.talk import ITalk

        @indexer(ITalk)
        def talk_audience(object, **kw):
             return object.audience

    We'd have to register this factory function as a named adapter in the ``configure.zcml``. Assuming you've put the code above into a file named indexers.py

    .. code-block:: xml

        <adapter name="audience" factory=".indexers.talk_audience" />

    We will add some indexers later on.

Why use the catalog at all? It checks for permissions, and only returns the talks that the current user may see. They might be private or hidden to you since they are part of a top-secret conference for core-develeopers (there is no such thing!).

Most objects in plone act like dictionaries, so you can do ``context.values()`` to get all it's contents.

For historical reasons some attributes of brains and objects are written differently::

    >>> obj = brain.getObject()

    >>> obj.title
    u'Talk-submission is open!'

    >>> brain.Title == obj.title
    True

    >>> brain.title == obj.title
    False

Who can guess what ``brain.title`` will return since the brain has no such attribute?

.. only:: not presentation

    .. note::

        Answer: Acquisition will get the attribute from the nearest parent. ``brain.__parent__`` is ``<CatalogTool at /Plone/portal_catalog>``. The attribute ``title`` of the ``portal_catalog`` is 'Indexes all content in the site'.

Acquisition can be harmfull. Brains have no attribute 'getLayout' ``brain.getLayout()``::

    >>> brain.getLayout()
    'folder_listing'

    >>> obj.getLayout()
    'newsitem_view'

    >>> brain.getLayout
    <bound method PloneSite.getLayout of <PloneSite at /Plone>>

The same is true for methods::

    >>> obj.absolute_url()
    'http://localhost:8080/Plone/news/talk-submission-is-open'
    >>> brain.getURL() == obj.absolute_url()
    True
    >>> brain.getPath() == '/'.join(obj.getPhysicalPath())
    True

Querying the catalog
--------------------

The are many `catalog indexes <http://docs.plone.org/develop/plone/searching_and_indexing/indexing.html>`_ to query. Here are some examples::

    >>> portal_catalog = getToolByName(self.context, 'portal_catalog')
    >>> portal_catalog(Subject=('cats', 'dogs'))
    []
    >>> portal_catalog(review_state='pending')
    []

Calling the catalog without parameters return the whole site::

    >>> portal_catalog()
    [<Products.ZCatalog.Catalog.mybrains object at 0x1085a11f0>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a12c0>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a1328>, <Products.ZCatalog.Catalog.mybrains object at 0x1085a13 ...

.. seealso::

    http://docs.plone.org/develop/plone/searching_and_indexing/query.html


Exercises
---------

Since you now know how to query the catalog it is time for some exercise.

Exercise 1
**********

Add a method ``get_news`` to ``TalkListView`` that returns a list of brains of all News Items that are published and sort them in the order of their publishing-date.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python
        :linenos:

        def get_news(self):

            portal_catalog = api.portal.get_tool('portal_catalog')
            return portal_catalog(
                portal_type='News Item',
                review_state='published',
                sort_on='effective',
            )



Exercise 2
**********

Add a method that returns all published keynotes as objects.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python
        :linenos:

        def keynotes(self):

            portal_catalog = api.portal.get_tool('portal_catalog')
            brains = portal_catalog(
                portal_type='Talk',
                review_state='published')
            results = []
            for brain in brains:
                # There is no catalog-index for type_of_talk so we must check
                # the objects themselves.
                talk = brain.getObject()
                if talk.type_of_talk == 'Keynote':
                    results.append(talk)
            return results


The template for the listing
----------------------------

Next you create a template in which you use the results of the method 'talks'.

Try to keep logic mostly in python. This is for two reasons:

Readability:
    It's much easier to read python than complex tal-structures

Speed:
    Python-code is faster than code executed in templates. It's also easy to add caching to methods.

DRY:
    In Python you can reuse methods and easily refactor code. Refactoring TAL usually means having to do big changes in the html-structure which results in uncomprehensible diffs.


The MVC-Schema does not directly apply to Plone but look at it like this:

Model:
    the object

View:
    the template

Controller:
    the view

The view and the controller are very much mixed in Plone. Expecially when you look at some of the older code of Plone you'll see that the policy of keeping logic in python and representation in templates was not always enforced.

But you should nevertheless do it! You'll end up with more than enough logic in the templates anyway.

Add this simple table to ``templates/talklistview.pt``:

.. code-block:: html
    :linenos:

    <table class="listing">
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
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                   The 7 sins of plone-development
                </td>
                <td>
                    Philip Bauer
                </td>
                <td>
                    Advanced
                </td>
            </tr>
        </tbody>
    </table>

Afterwards you transform it into a listing:

.. code-block:: html
    :linenos:

    <table class="listing" id="talks">
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
            </tr>
        </thead>
        <tbody>
            <tr tal:repeat="talk view/talks">
                <td>
                    <a href=""
                       tal:attributes="href talk/url;
                                       title talk/description"
                       tal:content="talk/title">
                       The 7 sins of plone-development
                    </a>
                </td>
                <td tal:content="talk/speaker">
                    Philip Bauer
                </td>
                <td tal:content="talk/audience">
                    Advanced
                </td>
            </tr>
            <tr tal:condition="not:view/talks">
                <td colspan=3>
                    No talks so far :-(
                </td>
            </tr>
        </tbody>
    </table>

There are some some things that need explanation:

``tal:repeat="talk view/talks"``
    This iterates over the list of dictionaries returned by the view. ``view/talks`` calls the method ``talks`` of our view and each ``talk`` is in turn one of the dictionaries that are returned by this method. Since TAL's path-expressions for the lookup of values in dictionaries is the same as the attributes of objects we can write ``talk/somekey`` as we could ``view/somemethod``. Handy but sometimes irritating since from looking at the page-template alone we have often no way of knowing if something is an attribute, a method or the value of a dict. It would be a good practice to write ``tal:repeat="talk python:view.talks()"``.

``tal:content="talk/speaker"``
    'speaker' is a key in the dict 'talk'. We could also write ``tal:content="python:talk['speaker']"``

``tal:condition="not:view/talks"``
    This is a fallback if no talks are returned. It then return an empty list (remember ``results = []``?)


Exercise
********

Modify the view to only python-expressions.

..  admonition:: Solution
    :class: toggle

    .. code-block:: html
        :linenos:

        <table class="listing" id="talks">
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
                </tr>
            </thead>
            <tbody tal:define="talks python:view.talks()">
                <tr tal:repeat="talk talks">
                    <td>
                        <a href=""
                           tal:attributes="href python:talk['url'];
                                           title python:talk['description']"
                           tal:content="python:talk['title']">
                           The 7 sins of plone-development
                        </a>
                    </td>
                    <td tal:content="python:talk['speaker']">
                        Philip Bauer
                    </td>
                    <td tal:content="python:talk['audience']">
                        Advanced
                    </td>
                </tr>
                <tr tal:condition="python:not talks">
                    <td colspan=3>
                        No talks so far :-(
                    </td>
                </tr>
            </tbody>
        </table>

    To follow the mantra "don't repeat yourself" we define ``talks`` instead of calling the method twice.


Setting a custom view as default-view on an object
--------------------------------------------------

We don't want to always have to append /@@talklistview to out folder to get the view. There is a very easy way to set the view to the folder using the ZMI.

If we append ``/manage_propertiesForm`` we can set the property "layout" to ``talklistview``.

To make views configurable so that editors can choose them we have to register the view for the content-type at hand in it's FTI. To enable if for all folders we add a new file ``profiles/default/types/Folder.xml``

.. code-block:: xml
    :linenos:

    <?xml version="1.0"?>
    <object name="Folder">
     <property name="view_methods" purge="False">
      <element value="talklistview"/>
     </property>
      <alias from="@@talklistview" to="talklistview"/>
    </object>

After reapplying the typeinfo-profile of out addon (or simply reinstalling it) the content-type "Folder" is extended with our additional view-method and appears in the display-dropdown.

The ``purge="False"`` appends the view to the already existing ones instead of replacing them.


Adding some javascript (collective.js.datatables)
-------------------------------------------------

Here we use one of many nice feature build into Plone. The class="listing" gives the table a nice style and makes the table sortable with some javascript.

But we could improve that table further by using a nice javascript-library called "datatables". It might even become part of the Plone-core at some point.

Like for many js-libraries there is already a package that doe the plone-integration for us: ``collective.js.datatables``. Like all python-packages you can find it on pypi: http://pypi.python.org/pypi/collective.js.datatables

We already added the addon to our buildout, you just have to activate it in our template.

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6-16

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="ploneconf.site">
    <body>

    <metal:head fill-slot="javascript_head_slot">
        <link rel="stylesheet" type="text/css" media="screen" href="++resource++jquery.datatables/media/css/jquery.dataTables.css">

        <script type="text/javascript" src="++resource++jquery.datatables.js"></script>
        <script type="text/javascript">
            $(document).ready(function(){
                var oTable = $('#talks').dataTable({
                });
            })
        </script>
    </metal:head>

    <metal:content-core fill-slot="content-core">

        <table class="listing" id="talks">
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
                </tr>
            </thead>
            <tbody>
                <tr tal:repeat="talk view/talks">
                    <td>
                        <a href=""
                           tal:attributes="href talk/url;
                                           title talk/description"
                           tal:content="talk/title">
                           The 7 sins of plone-development
                        </a>
                    </td>
                    <td tal:content="talk/speaker">
                        Philip Bauer
                    </td>
                    <td tal:content="talk/audience">
                        Advanced
                    </td>
                </tr>
                <tr tal:condition="not:view/talks">
                    <td colspan=3>
                        No talks so far :-(
                    </td>
                </tr>
            </tbody>
        </table>

    </metal:content-core>
    </body>
    </html>

We don't need the css-class ``listing`` anymore since it might clash with datatables (it does not but still...).

The documentation of datatables is beyond our training.

We use METAL again but this time to fill a different slot. The "javascript_head_slot" is part of the html's ``<head>``-area in Plone and can be extended this way. We could also just put the code inline but having nicely ordered html is a good practice.

Let's test it: http://localhost:8080/Plone/talklistview

.. note::

    We add the ``jquery.datatables.js`` file directly to the HEAD slot of the HTML without using Plone JavaScript registry (portal_javascript). By using the registry you could enable merging of js files and advanced caching. A GenericSetup profile is included in the collective.js.datatables package.

Summary
-------

We created a nice listing, that can be called at any place in the website.
