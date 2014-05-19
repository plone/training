Dexterity Types II: Python
==========================

Without sponsors a conference would be hard to finance plus it is a good opportunity for plone-companies to advertise their services.

In this part we will:

* *pythonify* our talk-type a little more.
* create the content-type *sponsor* that has a python-schema
* discuss image-scales
* create custom catalog-indexes
* query the catalog for them
* enable some more default-features for our types





Add a class and interface to the talk-type
------------------------------------------

There are some upsides to having a real python-class on a content-type.

For this we add new files ``ìnterfaces.py`` and ``content.py``:

interfaces.py

.. code-block:: python
    :linenos:

    class ITalk(Interface):
        """Marker interface for Talks
        """

    class ISponsor(Interface):
        """Marker interface for Sponsor
        """

These are marker-interfaces. We can bind Views and Viewlets to content that implements these interfaces.


Add a browserlayer
------------------

Since we want the features we write only to be availabe when ploneconf.site actually is installed we can bind them to a browserlayer. Layers allow us to easily enable and disable views and other site functionality based on installed add-ons and themes.

In ``interfaces.py`` we add:

.. code-block::

    class IPloneconfSiteLayer(Interface):
        """Marker interface for the Browserlayer
        """

Now we can bind the demoview, the talkview and the talklistview to our layer. Here is an example using the talklistview.

.. code-block:: xml
    :emphasize-lines: 4

    <browser:page
       name="talklistview"
       for="*"
       layer="..interfaces.IPloneconfSiteLayer"
       class=".views.TalkListView"
       template="templates/talklistview.pt"
       permission="zope2.View"
       />

Note the relative python-path ``..interfaces.IPloneconfSiteLayer``. It is equivalent to the absolute path ``ploneconf.path.interfaces.IPloneconfSiteLayer``.

.. seealso::

    http://docs.plone.org/develop/plone/views/layers.html


Add catalog-indexes
-------------------

* catalog.xml

Add browserlayer
----------------

* browserlayer.xml


Add more features through generic-setup
---------------------------------------

* repositorytool.xml
* diff_tool.xml
* browserlayer.xml


