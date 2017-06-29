.. _dexterity2-label:

Dexterity Types II: Growing Up
==============================

.. sidebar:: Get the code!

    Get the code for this chapter (:doc:`More info <code>`):

    ..  code-block:: bash

        git checkout dexterity_2


The existing talks are still lacking some functionality we want to use.

In this part we will:

* add a marker interface to our talk type,
* create custom catalog indexes,
* query the catalog for them,
* enable some more default features for our type.


.. _dexterity2-marker-label:

Add a marker interface to the talk type
---------------------------------------

Marker Interfaces
+++++++++++++++++

The content type `Talk` is not yet a *first class citizen* because it does not implement its own interface.
Interfaces are like nametags, telling other elements who and what you are and what you can do. A marker interface is like such a nametag. The talks actually have an auto-generated marker interface ``plone.dexterity.schema.generated.Plone_0_talk``.

One problem is that the name of the Plone instance ``Plone`` is part of that interface name. If you now moved these types to a site with another name the code that uses these interfaces would no longer find the objects in question.

To create a real name-tag we add a new :py:class:`Interface` to :file:`interfaces.py`:

.. code-block:: python
    :linenos:
    :emphasize-lines: 5,12-13

    # -*- coding: utf-8 -*-
    """Module where all interfaces, events and exceptions live."""

    from zope.publisher.interfaces.browser import IDefaultBrowserLayer
    from zope.interface import Interface


    class IPloneconfSiteLayer(IDefaultBrowserLayer):
        """Marker interface that defines a browser layer."""


    class ITalk(Interface):
        """Marker interface for Talks"""

:py:class:`ITalk` is a marker interface. We can bind Views and Viewlets to content that provide these interfaces. Lets see how we can provide this Interface. There are two solutions for this.

1. Let them be instances of a class that implements this Interface.
2. Register this interface as a behavior and enable it on talks.

The first option has an important drawback: only *new* talks would be instances of the new class. We would either have to migrate the existing talks or delete them.

So let's register the interface as a behavior in :file:`behaviors/configure.zcml`

.. code-block:: xml

  <plone:behavior
      title="Talk"
      description="Marker interface for talks to be able to bind views to."
      provides="..interfaces.ITalk"
      />

And enable it on the type in :file:`profiles/default/types/talk.xml`

.. code-block:: xml
    :linenos:
    :emphasize-lines: 5

    <property name="behaviors">
     <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
     <element value="plone.app.content.interfaces.INameFromTitle"/>
     <element value="ploneconf.site.behaviors.social.ISocial"/>
     <element value="ploneconf.site.interfaces.ITalk"/>
    </property>

Either reinstall the add-on, apply the behavior by hand or run an upgrade step (see below) and the interface will be there.

Then we can safely bind the ``talkview`` to the new marker interface.

.. code-block:: xml
    :emphasize-lines: 3

    <browser:page
        name="talkview"
        for="ploneconf.site.interfaces.ITalk"
        layer="zope.interface.Interface"
        class=".views.TalkView"
        template="templates/talkview.pt"
        permission="zope2.View"
        />

Now the ``/talkview`` can only be used on objects that implement said interface. We can now also query the catalog for objects providing this interface :py:meth:`catalog(object_provides="ploneconf.site.interfaces.ITalk")`. The ``talklistview`` and the ``demoview`` do not get this constraint since they are not only used on talks.

.. note::

    Just for completeness sake, this is what would have to happen for the first option (associating the :py:class:`ITalk` interface with a :py:class:`Talk` class):

    * Create a new class that inherits from :py:class:`plone.dexterity.content.Container` and implements the marker interface.

      .. code-block:: python

          from plone.dexterity.content import Container
          from ploneconf.site.interfaces import ITalk
          from zope.interface import implementer

          @implementer(ITalk)
          class Talk(Container):
              """Class for Talks"""

    * Modify the class for new talks in :file:`profiles/default/types/talk.xml`

      .. code-block:: xml
          :linenos:
          :emphasize-lines: 3

          ...
          <property name="add_permission">cmf.AddPortalContent</property>
          <property name="klass">ploneconf.site.content.talk.Talk</property>
          <property name="behaviors">
          ...

    * Create an upgrade step that changes the class of the existing talks. A reuseable method to do such a thing is in `plone.app.contenttypes.migration.dxmigration.migrate_base_class_to_new_class <https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/migration/dxmigration.py#L130>`_.

.. _dexterity2-upgrades-label:

Upgrade steps
-------------

When projects evolve you sometimes want to modify various things while the site is already up and brimming with content and users. Upgrade steps are pieces of code that run when upgrading from one version of an add-on to a newer one. They can do just about anything.
We will use an upgrade-step to enable the new behavior instead of reinstalling the addon.

We will create an upgrade step that:

* runs the typeinfo step (i.e. loads the GenericSetup configuration stored in ``profiles/default/types.xml`` and ``profiles/default/types/...`` so we don't have to reinstall the add-on to have our changes from above take effect) and
* cleans up the talks that might be scattered around the site in the early stages of creating it. We will move all talks to a folder ``talks`` (unless they already are there).

Upgrade steps can be registered in their own ZCML file to prevent cluttering the main :file:`configure.zcml`. Include a new :file:`upgrades.zcml` in our :file:`configure.zcml` by adding:

..  code-block:: xml

    <include file="upgrades.zcml" />

Create :file:`upgrades.zcml`:

.. code-block:: xml
    :linenos:

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:i18n="http://namespaces.zope.org/i18n"
      xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
      i18n_domain="ploneconf.site">

      <genericsetup:upgradeStep
          title="Update and cleanup talks"
          description="Update typeinfo and move talks to a folder 'talks'"
          source="1000"
          destination="1001"
          handler="ploneconf.site.upgrades.upgrade_site"
          sortkey="1"
          profile="ploneconf.site:default"
          />

    </configure>

The upgrade step bumps the version number of the GenericSetup profile of :py:mod:`ploneconf.site` from 1000 to 1001. The version is stored in :file:`profiles/default/metadata.xml`. Change it to

..  code-block:: xml

    <version>1001</version>

GenericSetup now expects the code as a method :py:meth:`upgrade_site` in the file :file:`upgrades.py`. Let's create it.

..  code-block:: python
    :linenos:

    # -*- coding: utf-8 -*-
    from plone import api

    import logging

    default_profile = 'profile-ploneconf.site:default'
    logger = logging.getLogger(__name__)


    def upgrade_site(setup):
        setup.runImportStepFromProfile(default_profile, 'typeinfo')
        portal = api.portal.get()
        # Create a folder 'The event' if needed
        if 'the-event' not in portal:
            event_folder = api.content.create(
                container=portal,
                type='Folder',
                id='the-event',
                title=u'The event')
        else:
            event_folder = portal['the-event']

        # Create folder 'Talks' inside 'The event' if needed
        if 'talks' not in event_folder:
            talks_folder = api.content.create(
                container=event_folder,
                type='Folder',
                id='talks',
                title=u'Talks')
        else:
            talks_folder = event_folder['talks']
        talks_url = talks_folder.absolute_url()

        # Find all talks
        brains = api.content.find(portal_type='talk')
        for brain in brains:
            if talks_url in brain.getURL():
                # Skip if the talk is already somewhere inside the target-folder
                continue
            obj = brain.getObject()
            logger.info('Moving {} to {}'.format(
                obj.absolute_url(), talks_folder.absolute_url()))
            # Move talk to the folder '/the-event/talks'
            api.content.move(
                source=obj,
                target=talks_folder,
                safe_id=True)

Note:

* Upgrade-steps get the tool ``portal_setup`` passed as their argument.
* The ``portal_setup`` tool has a method :py:meth:`runImportStepFromProfile`
* We create the needed folder-structure if it does not exists.

After restarting the site we can run the step:

* Go to the :guilabel:`Add-ons` control panel http://localhost:8080/Plone/prefs_install_products_form.
  There should now be a new section **Upgrades** and a button to upgrade from 1000 to 1001.
* Run the upgrade step by clicking on it.

On the console you should see logging messages like::

    INFO ploneconf.site.upgrades Moving http://localhost:8080/Plone/old-talk1 to http://localhost:8080/Plone/the-event/talks

Alternatively you also select which upgrade steps to run like this:

* In the ZMI go to *portal_setup*
* Go to the tab :guilabel:`Upgrades`
* Select :guilabel:`ploneconf.site` from the dropdown and click :guilabel:`Choose profile`
* Run the upgrade step.

.. seealso::

    https://docs.plone.org/develop/addons/components/genericsetup.html#id1


.. note::

    Upgrading from an older version of Plone to a newer one also runs upgrade steps from the package :py:mod:`plone.app.upgrade`. You should be able to upgrade a clean site from 2.5 to 5.0 with one click.

    For an example see the upgrade-step to Plone 5.0a1 https://github.com/plone/plone.app.upgrade/blob/master/plone/app/upgrade/v50/alphas.py#L37



.. _dexterity2-browserlayer-label:

Add a browserlayer
------------------

A browserlayer is another such marker interface. Browserlayers allow us to easily enable and disable views and other site functionality based on installed add-ons and themes.

Since we want the features we write only to be available when :py:mod:`ploneconf.site` actually is installed we can bind them to a browserlayer.

Our package already has a browserlayer (added by :py:mod:`bobtemplates.plone`). See :file:`interfaces.py`:

..  code-block:: python
    :linenos:
    :emphasize-lines: 4, 8-9

    # -*- coding: utf-8 -*-
    """Module where all interfaces, events and exceptions live."""

    from zope.publisher.interfaces.browser import IDefaultBrowserLayer
    from zope.interface import Interface


    class IPloneconfSiteLayer(IDefaultBrowserLayer):
        """Marker interface that defines a browser layer."""


    class ITalk(Interface):
        """Marker interface for Talks"""


It is enabled by GenericSetup when installing the package since it is registered in the :file:`profiles/default/browserlayer.xml`

..  code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <layers>
      <layer
          name="ploneconf.site"
          interface="ploneconf.site.interfaces.IPloneconfSiteLayer"
          />
    </layers>

We should bind all views to it. Here is an example using the talkview.

..  code-block:: xml
    :emphasize-lines: 4

    <browser:page
        name="talklistview"
        for="*"
        layer="..interfaces.IPloneconfSiteLayer"
        class=".views.TalkListView"
        template="templates/talklistview.pt"
        permission="zope2.View"
        />

Note the relative Python path :py:class:`..interfaces.IPloneconfSiteLayer`. It is equivalent to the absolute path :py:class:`ploneconf.site.interfaces.IPloneconfSiteLayer`.

.. seealso::

    https://docs.plone.org/develop/plone/views/layers.html


Exercise
++++++++

Do you need to bind the :ref:`viewlets1-social2-label` from the chapter 'Writing Viewlets' to this new browser layer?

..  admonition:: Solution
    :class: toggle

    No, it would make no difference since the viewlet is already bound to the marker interface :py:class:`ploneconf.site.behaviors.social.ISocial`.

.. _dexterity2-catalogindex-label:

Add catalog indexes
-------------------

In the ``talklistview`` we had to wake up all objects to access some of their attributes.
That is OK if we don't have many objects and they are light dexterity objects. If we had thousands of objects this might not be a good idea.

Instead of loading them all into memory we will use catalog indexes to get the data we want to display.

Add a new file :file:`profiles/default/catalog.xml`

.. code-block:: xml
    :linenos:

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

This adds new indexes for the three fields we want to show in the listing. Note that *audience* is a :py:class:`KeywordIndex` because the field is multi-valued, but we want a separate index entry for every value in an object.

The ``column ..`` entries allow us to display the values of these indexes in the tableview of collections.

.. note::

    Until Plone 4.3.2 adding indexes in :file:`catalog.xml` was harmful because reinstalling the add-on purged the indexes! See https://www.starzel.de/blog/a-reminder-about-catalog-indexes.

* Reinstall the add-on
* Go to http://localhost:8080/Plone/portal_catalog/manage_catalogAdvanced to update the catalog
* Go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes to inspect and manage the new indexes

.. seealso::

    https://docs.plone.org/develop/plone/searching_and_indexing/indexing.html

.. note::

    The new indexes are still empty. We'll have to reindex them. To do so by hand go to http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes, select the new indexes and click :guilabel:`Reindex`. We could also rebuild the whole catalog by going to the :guilabel:`advanced`-tab and clicking :guilabel:`Clear and Rebuild`. For large sites that can take a long time.

    We could also write an upgrade step to enable the catalog-indexes and reindex all talks:

    .. code-block:: python

        def add_some_indexes(setup):
            setup.runImportStepFromProfile(default_profile, 'catalog')
            for brain in api.content.find(portal_type='talk'):
                obj = brain.getObject()
                obj.reindexObject(idxs=['type_of_talk', 'speaker', 'audience'])


.. _dexterity2-customindex-label:

Query for custom indexes
------------------------

The new indexes behave like the ones that Plone has already built in:

.. code-block:: pycon

    >>> (Pdb) from Products.CMFCore.utils import getToolByName
    >>> (Pdb) catalog = getToolByName(self.context, 'portal_catalog')
    >>> (Pdb) catalog(type_of_talk='Keynote')
    [<Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
    >>> (Pdb) catalog(audience=('Advanced', 'Professionals'))
    [<Products.ZCatalog.Catalog.mybrains object at 0x10737b870>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b940>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
    >>> (Pdb) brain = catalog(type_of_talk='Keynote')[0]
    >>> (Pdb) brain.speaker
    u'David Glick'

We now can use the new indexes to improve the talklistview so we don't have to *wake up* the objects any more. Instead we use the brains' new attributes.

.. code-block:: python
    :linenos:
    :emphasize-lines: 13-15

    class TalkListView(BrowserView):
        """ A list of talks
        """

        def talks(self):
            results = []
            brains = api.content.find(context=self.context, portal_type='talk')
            for brain in brains:
                results.append({
                    'title': brain.Title,
                    'description': brain.Description,
                    'url': brain.getURL(),
                    'audience': ', '.join(brain.audience or []),
                    'type_of_talk': brain.type_of_talk,
                    'speaker': brain.speaker,
                    'uuid': brain.UID,
                    })
            return results

The template does not need to be changed and the result in the browser did not change, either. But when listing a large number of objects the site will now be faster since all the data you use comes from the catalog and the objects do not have to be loaded into memory.

.. _dexterity2-collection-criteria-label:

Add collection criteria
-----------------------

To be able to search content in collections using these new indexes we would have to register them as criteria for the querystring widget that collections use. As with all features make sure you only do this if you really need it!


Add a new file :file:`profiles/default/registry.xml`

.. code-block:: xml
    :linenos:

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
      <records interface="plone.app.querystring.interfaces.IQueryField"
               prefix="plone.app.querystring.field.speaker">
        <value key="title">Speaker</value>
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

  https://docs.plone.org/develop/plone/functionality/collections.html#add-new-collection-criteria-new-style-plone-app-collection-installed


.. _dexterity2-GS-label:

Add versioning through GenericSetup
------------------------------------

Configure the versioning policy and a diff-view for talks through GenericSetup.

Add new file :file:`profiles/default/repositorytool.xml`

.. code-block:: xml
    :linenos:

    <?xml version="1.0"?>
    <repositorytool>
      <policymap>
        <type name="talk">
          <policy name="at_edit_autoversion"/>
          <policy name="version_on_revert"/>
        </type>
      </policymap>
    </repositorytool>


Add new file :file:`profiles/default/diff_tool.xml`

.. code-block:: xml
    :linenos:

    <?xml version="1.0"?>
    <object>
      <difftypes>
        <type portal_type="talk">
          <field name="any" difftype="Compound Diff for Dexterity types"/>
        </type>
      </difftypes>
    </object>

Finally you need to activate the versioning behavior on the content type. Edit :file:`profiles/default/types/talk.xml`:

.. code-block:: xml
    :linenos:
    :emphasize-lines: 6

    <property name="behaviors">
     <element value="plone.app.dexterity.behaviors.metadata.IDublinCore"/>
     <element value="plone.app.content.interfaces.INameFromTitle"/>
     <element value="ploneconf.site.behaviors.social.ISocial"/>
     <element value="ploneconf.site.interfaces.ITalk"/>
     <element value="plone.app.versioningbehavior.behaviors.IVersionable" />
    </property>

.. note::

    There is currently a bug that breaks showing diffs when multiple-choice fields were changed.


Summary
-------

The talks are now grown up:

* They provide a interface to which you can bind features like views
* Some fields are indexed in the catalog making the listing faster
* Talks are now versioned
* You wrote your first upgrade-step to move the talks around: Whopee!
