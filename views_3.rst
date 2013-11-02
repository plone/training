Views III: A Talk list
=======================


Now we don't want to provide information about one specific item but on several items. What now? We can't look at several items at the same time as context.


Using portal_catalog
--------------------

Let's say we want so show a list of all the talks that were submitted for our conference. We can just go to the folder and select a display-method that suits us. But none does because we want to show the target-audience in our listing.

So we need to get all the talks. For this we use the python-class of the view to query the catalog for the talks.

The catalog is like a search-engine for the content on our site. It holds information about all the objects as well as some of their attributes like title, decription, workflow_state, keywords that they were tagged with, author, content_type, it's path in the site etc. But it does not hold the content of "heavy" fields like images or files, richtext-fields and field that we just defined ourselves.

It is the fast way to get content that exists in the site and do something with it. From the results of the catalog we can get the objects themselves but often we don't need them, but only the properties that the results already have.

::

    # -*- coding: UTF-8 -*-
    from five import grok
    from zope.interface import Interface
    from Products.CMFCore.utils import getToolByName


    class TalkDefaultView(grok.View):
        grok.context(Interface)
        grok.require('zope2.View')


    class TalkListView(grok.View):
        grok.context(Interface)
        grok.require("zope2.View")

        def talks(self):
            results = []
            portal_catalog = getToolByName(self.context, 'portal_catalog')
            current_path = "/".join(self.context.getPhysicalPath())

            talks = portal_catalog(portal_type="talk",
                                   path=current_path)
            for brain in talks:
                # hold on to your hats, we're awaking the brains!
                talk = brain.getObject()

                results.append({
                    'title': brain.Title,
                    'url': brain.getURL(),
                    'audience': talk.audience,
                    'uuid': brain.UID,
                    })
            return results

We query the catalog for two things:

* ``portal_type = "talk"``
* ``path = "/".join(self.context.getPhysicalPath())``

We get the path of the current context to query only for objects in the current path. Otherwise we'd get all talks in the whole site. If we moved some talks to a different part of the site (e.g. a sub-conference for univerities with a special talk-list) we might not want so see them in our listing.

We iterate over the list of results that the catalog returns us::

We create a dictionary that holds all the information we want to show in the template. This way we don't have to put any complex logic into the template.

brains and objects
------------------

Objects are normally not loaded into memory but lie dormant in the Database ZODB. Waking objects up can be slow, especially if you're waking up a lot of objects. Fortunately out talks are not especially heavy since they are

* dexterity-objects which are lighter than their archetypes-brothers
* relatively few since we don't have thousands of talks at our conference

We want to show the target-audience but that attributes of the talks is not in the catalog. This is why we need to get to the objects themselves.

We could also add a new index to the catalog that will add 'audience' to the properties of the brains. We have to weight pros and cons:

* talks are important and thus most likely always in memory
* prevent bloating of catalog with indexes

The code to add such an index would look like this::

    from plone.indexer.decorator import indexer
    from plonekonf.talk.talk import ITalk

    @indexer(ITalk)
    def talk_audience(object, **kw):
         return object.audience

We'd have to register this factory function as a named adapter using ZCML. Assuming you've put the code above into a file named indexers.py::

    <adapter name="audience" factory=".indexers.talk_audience" />

Why use the catalog at all? It checks for permissions, and only returns the talks that the current user may see. They might be private or hidden to you since they are part of a top-secret conference for core-develeopers (there is no such thing!).

Most objects in plone act like dictionaries, so I could do context.values() to get all it's contents.

For historical reasons only the same attributes of brains and objects are written differently::

    >>> brain.Title == obj.title
    True

But ``brain.title`` returns the name of the catalog :-(

Look there to find out how to query for date, language: http://collective-docs.readthedocs.org/en/latest/searching_and_indexing/index.html.


The template for the listing
----------------------------

Next the template in which we use the results of our method 'talks'.

We try to keep logic mostly in python. This is for two reasons:

Readability:
    It's much simpler to read python that complex tal-structures

Speed:
    Python-code is faster than code executed in templates. It's also easy to add caching to methods.

The MVC-Schema does not directly apply to Plone but look at it like this:

Model:
    the object

View:
    the template

Controller:
    the view

The view and the controller are very much mixed in Plone.

When you look at some of the older code of Plone you'll see that the policy of keeping login insice python and representation in templates was not always enforced. You should nevertheless do it. You'll end up with more than enough logic in the templates anyway. You'll see now.

Let's add this simple table to our template 'talklistview.pt':

.. code-block:: html

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

After we transform it we have a listing:

.. code-block:: html

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

I'll explain some of the things in the TAL:

``tal:repeat="talk view/talks"``
    we iterate over the list of dictionaries returned by our view. ``view/talks`` calles the method ``talks`` of our view and each ``talk`` is in turn a dictionary. Since TAL's path-expressions for the lookup of values in dictionaries is the same as the attributes of objects we can write ``talk/somekey`` as we could ``view/somemethod``. Handy but sometimes irritating since from looking at the page-template alone we have often no way of knowing if something is an attribute, a method or the value of a dict.

``tal:content="talk/speaker"``
    'speaker' is a key in the dict 'talk'. We could also write ``tal:content="python:talk['speaker']"``

``tal:condition="not:view/talks"``
    this is a fallback for when no talks are returned by out method talks. It then return an empty list (remember ``results = []``?)

``tal:content="talk/average_rating | nothing"``
    you might remember there is no key 'average_rating' in the dict that we return. The '|' ("or") character is used to find an alternative value to a path if the first path evaluates to ``nothing`` or does not exist. The | ("or") is the logical 'or' and will be used if no value exists.

    What will not work is ``tal:content="python:talk['average_rating'] or ''"``. Who knows what it will yield? We'll get ``KeyError: 'average_rating'``. In fact it is bad practice to use | too often since it'll swallow errors like a typo in ``tal:content="talk/averange_ratting | nothing"`` and you might wonder why there are no ratings later on...

    Keep in mind that you can't and should not use it to prevent errors like a try/except-block. But in this case it's pretty useful since our code does not break event though we have not implemented ratings yet.


Setting a custom view as default-view on an object
--------------------------------------------------

We don't want to always have to append /@@talklistview to out folder to get the view. There is a very easy way to set the view to the folder using the ZMI.

If we append /manage_propertiesForm we can set the property "layout" to "talklistview".

To make views configurable so that editors can choose them like folder_Summary_view etc. We'd have to register it for the content-type at hand (Folder) in it's FTI (folder.xml).

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="Folder">
     <property name="view_methods" purge="False">
      <element value="talklistview"/>
     </property>
      <alias from="@@talklistview" to="talklistview"/>
    </object>

After reapplying the profile the configuration of the content-type "Folder" would be extended with our additional view-method and it would appear in the display-dropdown.


Adding some javascript (collective.js.datatables)
-------------------------------------------------

Here we use one of many nice feature build into Plone. The class="listing" gives the table a nice style and makes the table sortable with some javascript.

But we could improve that table further by using a nice javascript-library called "datatables". It might even become part of the Plone-core at some point.

Like for many js-libraries there is already a package that doe the plone-integration for us: ``collective.js.datatables``. Like all python-packages you can find it on pypi: http://pypi.python.org/pypi/collective.js.datatables

We already added the addon to our buildout and just have to activate it in our template.

.. code-block:: html

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

We don't need the css-class ``listing`` anymore since it might clash with datatables (it does not but still...).

The documentation of datatables is beyond our training.

We use METAL again but this time to fill a different slot. The "javascript_head_slot" is part of the html's ``<head>``-area in Plone and can be extended this way. We could also just put the code inline but having nicely ordered html is a good practice.

Let's test it.
