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

Marker Interfaces
+++++++++++++++++

The content-type `Talk` is not yet a first-class plone-citizen because it does not implement his own interface. Interfaces are like name-tags, telling other elements who and what you are and what you can do. A marker interface is like such a nametag. The talks actually have a auto-generated marker-interface ``plone.dexterity.schema.generated.Plone_0_talk``.

The problem is that the name of the Plone-instance ``Plone`` is part of that interface-name. If you now moved these types to a site with another name, code that uses these Interfaces would no longer find the objects in question.

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

These are marker-interfaces. We can bind Views and Viewlets to content that implements these interfaces. Having a real python-class on a content-type has the additional upside: We can now add methods to this class that can be used like ``obj.my_method()``.

content.py

.. code-block:: python

    from plone.dexterity.content import Container
    from ploneconf.site.interfaces import ITalk
    from zope.interface import implements

    class Talk(Container):
        implements(ITalk)


To have our talk-instances to use this we'll have to modify its base-class from ``plone.dexterity.content.Container`` to the new class. Edit the talk-profile at ``profiles/default/types/talk.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 3

    <property name="default_view_fallback">False</property>
    <property name="add_permission">cmf.AddPortalContent</property>
    <property name="klass">ploneconf.site.content.Talk</property>
    <property name="behaviors">
      <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
      <element value="plone.app.content.interfaces.INameFromTitle"/>
    </property>

Now we can bind the talkview to the new interface

.. code-block:: xml
    :emphasize-lines: 3

    <browser:page
       name="talklistview"
       for="ploneconf.talk.interfaces.ITalk"
       layer="*"
       class=".views.TalkListView"
       template="templates/talklistview.pt"
       permission="zope2.View"
       />

Now the ``/talkview`` can only be used on objects that implent said interface.

Add a browserlayer
------------------

A browserlayer is another such marker-interface. Bowserlayers allow us to easily enable and disable views and other site functionality based on installed add-ons and themes.

Since we want the features we write only to be availabe when ploneconf.site actually is installed we can bind them to a browserlayer.

In ``interfaces.py`` we add:

.. code-block::

    class IPloneconfSiteLayer(Interface):
        """Marker interface for the Browserlayer
        """

We register teh browserlayer in generic setup in ``profiles/default/browserlayer.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <layers>
      <layer name="ploneconf.site"
        interface="ploneconf.site.interfaces.IPloneconfSiteLayer" />
    </layers>

After reinstalling the addon we can bind the demoview, the talkview and the talklistview to our layer. Here is an example using the talkview.

.. code-block:: xml
    :emphasize-lines: 4

    <browser:page
       name="talklistview"
       for="ploneconf.talk.interfaces.ITalk"
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


