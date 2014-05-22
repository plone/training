Dexterity Types II: Growing up
==============================

The existing talks are still lacking some functionality we want to use.

In this part we will:

* *pythonify* our talk-type a little more
* create custom catalog-indexes
* query the catalog for them
* enable some more default-features for our type


Add a class and interface to the talk-type
------------------------------------------

Marker Interfaces
+++++++++++++++++

The content-type `Talk` is not yet a first-class plone-citizen because it does not implement his own interface. Interfaces are like name-tags, telling other elements who and what you are and what you can do. A marker interface is like such a nametag. The talks actually have a auto-generated marker-interface ``plone.dexterity.schema.generated.Plone_0_talk``.

The problem is that the name of the Plone-instance ``Plone`` is part of that interface-name. If you now moved these types to a site with another name, code that uses these Interfaces would no longer find the objects in question.

For this we add a new file ``ìnterfaces.py``:

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    from zope.interface import Interface


    class ITalk(Interface):
        """Marker interface for Talks
        """

``ITalk`` is a marker-interface. We can bind Views and Viewlets to content that provide these interfaces. To have talks provide this Interface we need them to be instances of a class that implements this Interface.

For this we create a new class that inherits ``plone.dexterity.content.Container``.

Add a new folder ``content/`` with a empty ``content/__init__.py`` and a new file ``content/talk.py``:

.. code-block:: python

    # -*- coding: UTF-8 -*-
    from plone.dexterity.content import Container
    from ploneconf.site.interfaces import ITalk
    from zope.interface import implements


    class Talk(Container):
        implements(ITalk)

.. note::

    For now we don't need a ``configure.zcml`` in the new folder, so we don't have to register it in the packages ``configure.zcml``.


To have our talk-instances to use this we'll have to modify its base-class from ``plone.dexterity.content.Container`` to the new class. Edit the profile's ``klass``-property in ``profiles/default/types/talk.xml``

.. code-block:: xml
    :linenos:
    :emphasize-lines: 3

    ...
    <property name="add_permission">cmf.AddPortalContent</property>
    <property name="klass">ploneconf.site.content.talk.Talk</property>
    <property name="behaviors">
    ...

.. note::

  Having a real python-class on a content-type has an additional upside: We can now add methods to the class ``Talk`` that can be used like ``obj.my_method()``.

.. warning::

  Now we have a problem: New talks will be instances of the class ``Talk`` while old onjects will still be instances of tha class ``Container``. So far the only difference is that the old object will not provide the interface ``ITalk``. This is bad since we want to bind our views to this interface. We will ahabe to write an upgrade-step for this.

Upgrade-steps
-------------

When projects evolve you'll sometimes have to modify various things while the site is already up and brimming with content and users.

Upgrade steps are usually registered in their own zcml-file. Create ``upgrades.zcml``

.. code-block:: xml
    :linenos:

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:i18n="http://namespaces.zope.org/i18n"
      xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
      i18n_domain="ploneconf.site">

      <genericsetup:upgradeStep
        title="Modifiy class of talks"
        description="Change the class of talks from 'plone.dexterity.content.Container' to 'ploneconf.site.content.talk.Talk'"
        source="1"
        destination="1001"
        handler="ploneconf.site.upgrades.migrate_talk_class"
        sortkey="1"
        profile="ploneconf.site:default"
        />

    </configure>

Include it in ``configure.zcml`` by adding:

.. code-block:: xml

    <include file="upgrades.zcml" />

Generic setup now expects the code to be a method ``migrate_talk_class`` in the file ``upgrades.py``. Let's create it.

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    from plone import api
    from ploneconf.site.content.talk import Talk
    import logging

    logger = logging.getLogger('ploneconf.site')


    def migrate_talk_class(self):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type="talk")
        for brain in brains:
            obj = brain.getObject()
            if obj.__class__ is not Talk:
                obj.__class__ = Talk
                logger.info('Migrated __class__ of %s' % obj.absolute_url())


After restarting the site we can run the step:

* In the ZMI got to *portal_setup*
* Go to the tab *Upgrades*
* Select *ploneconf.site* from the dropdown and click *Choose profile*
* Run the upgrade step. On the console you should see logging-messages like::

    INFO ploneconf.site.upgrades Migrated __class__ of http://localhost:8080/Plone/talks/old-talk1

.. seealso::

  http://docs.plone.org/develop/addons/components/genericsetup.html#id1


.. note::

    Upgrading from an older version of Plone to a newer one also runs upgrade steps from the package ``plone.app.upgrade``. You should be able to upgrade a clean site from 2.5 to 5.0a2 with a click.

    For an example see the upgrade-step to Plone 5.0a1 https://github.com/plone/plone.app.upgrade/blob/master/plone/app/upgrade/v50/alphas.py#L23


Now finally we can safely bind the talkview to the new marker interface.

.. code-block:: xml
    :emphasize-lines: 3

    <browser:page
      name="talklistview"
      for="ploneconf.site.interfaces.ITalk"
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
      for="ploneconf.site.interfaces.ITalk"
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

Instead of loading them all into memory we will use catalog-indexes to get the data we want to display.

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

The ``column ..`` entry allows us to display these values of these indexes in the tableview of collections.

.. note::

    Until Plone 4.3.2 adding indexes in catalog.xml was harmful because reinstalling the addon purged the indexes! See http://www.starzel.de/blog/a-reminder-about-catalog-indexes.

    To run additional custom code on (re-)installing an addon you should use a `setuphandler.py <http://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py>`_.

* Reinstall the addon
* Go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes to inspect populate and inspect the new indexes

.. seealso::

    http://docs.plone.org/develop/plone/searching_and_indexing/indexing.html


Query for custom indexes
------------------------

The new indexes behave like the ones that plone has built in:

.. code-block:: python

    >>> (Pdb) from Products.CMFCore.utils import getToolByName
    >>> (Pdb) catalog = getToolByName(self.context, 'portal_catalog')
    >>> (Pdb) catalog(type_of_talk='Keynote')
    [<Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
    >>> (Pdb) catalog(audience=('Advanced', 'Professionals'))
    [<Products.ZCatalog.Catalog.mybrains object at 0x10737b870>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b940>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
    >>> (Pdb) brain = catalog(type_of_talk='Keynote')[0]
    >>> (Pdb) brain.speaker
    u'David Glick'

We now can use the new indexes to improve the talklistview so we don't have to wake up the objects any more.

.. code-block:: python
    :linenos:

    class TalkListView(BrowserView):
        """ A list of talks
        """

        def talks(self):
            results = []
            portal_catalog = getToolByName(self.context, 'portal_catalog')
            current_path = "/".join(self.context.getPhysicalPath())

            brains = portal_catalog(portal_type="talk",
                                    path=current_path)
            for brain in brains:
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(brain.audience),
                    'type_of_talk': brain.type_of_talk,
                    'speaker': brain.speaker,
                    'uuid': brain.UID,
                    })
            return results

The template does not need to be changed and the result did not change as well.

Add collection criteria
-----------------------

To be able to search content in collection using the new indexes we would have to register them as criteria for the querystring-widget that collection use.

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
