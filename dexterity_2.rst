Dexterity Types II: Python
==========================

Without sponsors a conference would be hard to finance plus it is a good opportunity for plone-companies to advertise their services.

In this part we will:

* *pythonify* our talk-type a little more.
* create custom catalog-indexes
* query the catalog for them
* enable some more default-features for our type


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

``ITalk`` is a marker-interface. We can bind Views and Viewlets to content that provide these interfaces. To have talks provide this Interface we need them to be instances of a class that implements this Interface.

For this we create a new class that inherits ``plone.dexterity.content.Container``.

Add a file ``content.py``:

.. code-block:: python

    from plone.dexterity.content import Container
    from ploneconf.site.interfaces import ITalk
    from zope.interface import implements

    class Talk(Container):
        implements(ITalk)


To have our talk-instances to use this we'll have to modify its base-class from ``plone.dexterity.content.Container`` to the new class. Edit the profile's ``klass``-property in ``profiles/default/types/talk.xml``

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

.. note::

  Having a real python-class on a content-type has an additional upside: We can now add methods to the class ``Talk`` that can be used like ``obj.my_method()``.

Now we can bind the talkview to the new interface.

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

.. code-block:: python

    class IPloneconfSiteLayer(Interface):
        """Marker interface for the Browserlayer
        """

We register the browserlayer in generic setup in ``profiles/default/browserlayer.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <layers>
      <layer name="ploneconf.site"
        interface="ploneconf.site.interfaces.IPloneconfSiteLayer" />
    </layers>

After reinstalling the addon we can bind the talkview, the demoview and the talklistview to our layer. Here is an example using the talkview.

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

Note the relative python-path ``..interfaces.IPloneconfSiteLayer``. It is equivalent to the absolute path ``ploneconf.site.interfaces.IPloneconfSiteLayer``.

.. seealso::

    http://docs.plone.org/develop/plone/views/layers.html


Add catalog-indexes
-------------------

In the `talklistview` we had to wake up all objects to access some of their attributes. That is ok if we don't have many objects and they are light dexterity-objects. If we had thousands of objects this might not be a good idea.

Instead of loading them all into memory we could use catalog-indexes to get the data we want to display.

Add a new file ``catalog.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_catalog">
      <index name="type_of_talk" meta_type="FieldIndex">
        <indexed_attr value="type_of_talk"/>
      </index>
      <index name="speaker" meta_type="FieldIndex">
        <indexed_attr value="speaker"/>
      </index>
      <index name="audience" meta_type="KeywordIndex">
        <indexed_attr value="audience"/>
      </index>

      <column value="audience" />
      <column value="type_of_talk" />
      <column value="speaker" />
    </object>

This adds new indexes for the three fields we want to show in the listing. Not that *audience* is a ``KeywordIndex`` because the field is multi-valued, but we want a seperate index-entry for every value in on a object.

Actually this is considered harmful because reinstalling the addon purges the indexes! Instead add a index in the `setuphandler.py <http://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py>`_ as described in http://www.starzel.de/blog/a-reminder-about-catalog-indexes.

* Reinstall addon
* Go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes to inspect the new indexes
* Clear & rebuild catalog to populate indexes.

.. seealso::

    http://docs.plone.org/develop/plone/searching_and_indexing/indexing.html


Add collection criteria
-----------------------

To be able to use the new indexes in collection we would have to register them as criteria for the querystring-widget that collection use.

Add a new file ``profiles/default/registry.xml``

.. code-block:: xml

    <registry>
      <records interface="plone.app.querystring.interfaces.IQueryField"
               prefix="plone.app.querystring.field.audience">
        <value key="title">Audience</value>
        <value key="description">A custom speaker index</value>
        <value key="enabled">True</value>
        <value key="sortable">False</value>
        <value key="operations">
          <element>plone.app.querystring.operation.string.is</element>
        </value>
        <value key="group">Metadata</value>
      </records>
      <records interface="plone.app.querystring.interfaces.IQueryField"
               prefix="plone.app.querystring.field.type_of_talk">
        <value key="title">Type of Talk</value>
        <value key="description">A custom index</value>
        <value key="enabled">True</value>
        <value key="sortable">False</value>
        <value key="operations">
          <element>plone.app.querystring.operation.string.is</element>
        </value>
        <value key="group">Metadata</value>
      </records>
    </registry>

.. seealso::

  http://docs.plone.org/develop/plone/functionality/collections.html#add-new-collection-criteria-new-style-plone-app-collection-installed


Add more features through generic-setup
---------------------------------------

Enable versioning and a diff-view for talks through Generic Setup.

Add new file ``profiles/default/repositorytool.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <repositorytool>
      <policymap>
        <type name="talk">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
      </policymap>
    </repositorytool>


Add new file ``profiles/default/diff_tool.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object>
      <difftypes>
        <type portal_type="talk">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
      </difftypes>
    </object>
