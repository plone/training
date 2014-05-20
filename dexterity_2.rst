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

Now we can bind the talkview to the new interface.

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

Actually this is considered harmful because reinstalling the addon purges the indexes! Instead add a index in the `setuphandler.py <http://docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py>`_ as described in http://www.starzel.de/blog/a-reminder-about-catalog-indexes.

To be professional we have to do the following:

Create a new file ``setuphandlers.py``

.. code-block:: python
    :linenos:

    # -*- coding: UTF-8 -*-
    import logging
    from Products.CMFCore.utils import getToolByName
    PROFILE_ID = 'profile-ploneconf.site:default'


    def setupVarious(context):

        # Ordinarily, GenericSetup handlers check for the existence of XML files.
        # Here, we are not parsing an XML file, but we use this text file as a
        # flag to check that we actually meant for this import step to be run.
        # The file is found in profiles/default.

        if context.readDataFile('ploneconf.site_various.txt') is None:
            return

        # Add additional setup code here
        logger = context.getLogger('ploneconf.site')
        site = context.getSite()
        add_catalog_indexes(site, logger)


    def add_catalog_indexes(context, logger=None):
        """Method to add our wanted indexes to the portal_catalog.

        @parameters:

        When called from the import_various method below, 'context' is
        the plone site and 'logger' is the portal_setup logger.  But
        this method can also be used as upgrade step, in which case
        'context' will be portal_setup and 'logger' will be None.
        """
        if logger is None:
            # Called as upgrade step: define our own logger.
            logger = logging.getLogger('ploneconf.site')

        # Run the catalog.xml step as that may have defined new metadata
        # columns.  We could instead add <depends name="catalog"/> to
        # the registration of our import step in zcml, but doing it in
        # code makes this method usable as upgrade step as well.  Note that
        # this silently does nothing when there is no catalog.xml, so it
        # is quite safe.
        setup = getToolByName(context, 'portal_setup')
        setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

        catalog = getToolByName(context, 'portal_catalog')
        indexes = catalog.indexes()
        # Specify the indexes you want, with
        # ('index_name', 'index_type', 'indexed_attribute')
        wanted = (
            ('type_of_talk', 'FieldIndex', 'type_of_talk'),
            ('speaker', 'FieldIndex', 'speaker'),
            ('audience', 'KeywordIndex', 'audience'),
        )
        indexables = []
        for name, meta_type, attribute in wanted:
            if name not in indexes:
                if attribute:
                    extra = {'indexed_attrs': attribute}
                    catalog.addIndex(name, meta_type, extra=extra)
                else:
                    catalog.addIndex(name, meta_type)
                indexables.append(name)
                if not attribute:
                    attribute = name
                logger.info("Added %s '%s' for attribute '%s'.", meta_type, name, extra)
        if len(indexables) > 0:
            logger.info("Indexing new indexes %s.", ', '.join(indexables))
            catalog.manage_reindexIndex(ids=indexables)


Add the marker-file ``profile/default/ploneconf.site_various.txt`` mentioned in line 14::

    The ploneconf.site_various step is run if this file is present in the profile

Register the setuphandlers in``configure.zcml``

.. code-block:: xml

    <!-- Register the import step -->
    <genericsetup:importStep
        name="ploneconf.site"
        title="ploneconf.site special import handlers"
        description=""
        handler="ploneconf.site.setuphandlers.setupVarious"
        />

Remove the indexes from ``catalog.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_catalog">
      <!-- Add indexes here on penalty of death or worse.
           See add_catalog_indexes in setuphandlers.py instead. -->

        <column value="audience" />
        <column value="type_of_talk" />
        <column value="speaker" />
    </object>

.. note::

  The ``column ..`` entry allows us to display these values of these indexes in the tableview of collections.

Finally done!

* Reinstall addon
* Go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes to inspect the new indexes
* Clear & rebuild catalog to populate indexes.

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
