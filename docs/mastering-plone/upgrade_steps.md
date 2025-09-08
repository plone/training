---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(upgrade-steps-label)=

# Upgrade-steps

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend
:class: logo
```

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout registry
```

Code for the end of this chapter:

```shell
git checkout upgrade_steps
```
````

In this part we will:

- Write code to update, create or move content
- Create custom catalog indexes
- Query the catalog for them,
- Enable more default features for our type

(upgrade-steps-upgrades-label)=

## Upgrade steps

You recently changed existing content, when you added the behavior `ploneconf.featured` or when you turned talks into events in the chapter {doc}`events`.

When projects evolve you sometimes want to modify various things while the site is already up and brimming with content and users.
Upgrade steps are pieces of code that run when upgrading from one version of an add-on to a newer one.
They can do just about anything.
We will use an upgrade step to enable the new behavior instead of reinstalling the add-on.

We will create an upgrade step that:

- runs the typeinfo step (i.e. loads the GenericSetup configuration stored in `profiles/default/types.xml` and `profiles/default/types/...` so we don't have to reinstall the add-on to have our changes from above take effect) and
- cleans up existing talks that might be scattered around the site in the early stages of creating it.
  We will move all talks to a folder `talks` (unless they already are there).

Upgrade steps can be registered in their own ZCML file to prevent cluttering the main {file}`configure.zcml`.
Create the new {file}`upgrades.zcml` include it in our {file}`configure.zcml`:

```xml
<include file="upgrades.zcml" />
```

You register the first upgrade-step in {file}`upgrades.zcml`:

```{code-block} xml
:linenos:

<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:i18n="http://namespaces.zope.org/i18n"
  xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
  i18n_domain="ploneconf.site">

  <genericsetup:upgradeStep
      title="Update and cleanup talks"
      description="Update typeinfo and move talks to to their folder"
      source="1000"
      destination="1001"
      handler="ploneconf.site.upgrades.upgrade_site"
      sortkey="1"
      profile="ploneconf.site:default"
      />

</configure>
```

The upgrade step bumps the version number of the GenericSetup profile of {py:mod}`ploneconf.site` from 1000 to 1001.
The version is stored in {file}`profiles/default/metadata.xml`.

Change it to

```xml
<version>1001</version>
```

`GenericSetup` now expects the code as a method {py:meth}`upgrade_site` in the file {file}`upgrades.py`.
Let's create it.

```{code-block} python
:linenos:

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging

default_profile = 'profile-ploneconf.site:default'
logger = logging.getLogger(__name__)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-ploneconf.site:default',
    )


def upgrade_site(context=None):
    # reload type info
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()

    # Create the expected folder-structure
    if 'training' not in portal:
        training_folder = api.content.create(
            container=portal,
            type='Document',
            id='training',
            title=u'Training')
    else:
        training_folder = portal['training']

    if 'schedule' not in portal:
        schedule_folder = api.content.create(
            container=portal,
            type='Document',
            id='schedule',
            title=u'Schedule')
    else:
        schedule_folder = portal['schedule']
    schedule_folder_url = schedule_folder.absolute_url()

    if 'location' not in portal:
        location_folder = api.content.create(
            container=portal,
            type='Document',
            id='location',
            title=u'Location')
    else:
        location_folder = portal['location']

    if 'sponsors' not in portal:
        sponsors_folder = api.content.create(
            container=portal,
            type='Document',
            id='sponsors',
            title=u'Sponsors')
    else:
        sponsors_folder = portal['sponsors']

    if 'sprint' not in portal:
        sprint_folder = api.content.create(
            container=portal,
            type='Document',
            id='sprint',
            title=u'Sprint')
    else:
        sprint_folder = portal['sprint']

    # Find all talks
    brains = api.content.find(portal_type='talk')
    for brain in brains:
        if schedule_folder_url in brain.getURL():
            # Skip if the talk is already somewhere inside the target folder
            continue
        obj = brain.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), schedule_folder_url))
        # Move talk to the folder '/schedule'
        api.content.move(
            source=obj,
            target=schedule_folder,
            safe_id=True)
```

Note:

- They are simple python methods, nothing fancy about them except the registration.
- When running a upgrade-step they get the tool `portal_setup` passed as a argument. To make it easier to call these steps from a pdb or from other methods it is a good idea to set it as `context=None` and not use the argument at all but instead use `portal_setup = api.portal.get_tool('portal_setup')` if you need it.
- The `portal_setup` tool has a method {py:meth}`runImportStepFromProfile`. In this example it is used to load the file `profiles/default/types.xml` and `profiles/default/types/talk.xml` to enable new behaviors, views or other settings.
- In Python we create the required folder structure if it does not exist yet making extensive use of `plone.api` as discussed in the chapter {doc}`api`.

After restarting the site we can run the step:

- Go to the {guilabel}`Add-ons` control panel <http://localhost:8080/Plone/prefs_install_products_form>.
  There should now be a new section **Upgrades** and a button to upgrade from 1000 to 1001.
- Run the upgrade step by clicking on it.

On the console you should see logging messages like:

```
INFO ploneconf.site.upgrades Moving http://localhost:8080/Plone/old-talk1 to http://localhost:8080/Plone/schedule
```

Alternatively you also select which upgrade steps to run like this:

- In the ZMI go to _portal_setup_
- Go to the tab {guilabel}`Upgrades`
- Select {guilabel}`ploneconf.site` from the dropdown and click {guilabel}`Choose profile`
- Run the upgrade step.

```{seealso}
<https://5.docs.plone.org/develop/addons/components/genericsetup.html#upgrade-steps>
```

```{note}
Upgrading from an older version of Plone to a newer one also runs upgrade steps from the package {py:mod}`plone.app.upgrade`.
You should be able to upgrade a clean site from 2.5 to 5.0 with one click.

Find the upgrade steps in <https://github.com/plone/plone.app.upgrade/tree/master/plone/app/upgrade/>
```

(upgrade-steps-browserlayer-label)=

## Browserlayers

```{note}
This section is only relevant for Plone Classic since Volto does not use Viewlets or BrowserViews.
```

A browserlayer is a marker on the request.
Browserlayers allow us to easily enable and disable views and other site functionality based on installed add-ons and themes.

Since we want the features we write only to be available when {py:mod}`ploneconf.site` actually is installed we can bind them to a browserlayer.

Our package already has a browserlayer (added by {py:mod}`bobtemplates.plone`). See {file}`interfaces.py`:

```{code-block} python
:emphasize-lines: 4, 8-9
:linenos:

# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IPloneconfSiteLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
```

It is enabled by GenericSetup when installing the package since it is registered in the {file}`profiles/default/browserlayer.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<layers>
  <layer
      name="ploneconf.site"
      interface="ploneconf.site.interfaces.IPloneconfSiteLayer"
      />
</layers>
```

You should bind all your custom BrowserViews and Viewlets to it.

Here is an example using the `talklistview` from {doc}`views_3`.

```{code-block} xml
:emphasize-lines: 4

<browser:page
    name="talklistview"
    for="*"
    layer="..interfaces.IPloneconfSiteLayer"
    class=".views.TalkListView"
    template="templates/talklistview.pt"
    permission="zope2.View"
    />
```

Note the relative Python path {py:class}`..interfaces.IPloneconfSiteLayer`.
It is equivalent to the absolute path {py:class}`ploneconf.site.interfaces.IPloneconfSiteLayer`.

```{seealso}
<https://5.docs.plone.org/develop/plone/views/layers.html>
```

## Add catalog indexes

In the `talklistview` we had to get the full objects to access some of their attributes.
That is OK if we don't have many objects and they are light dexterity objects.
If we had thousands of objects this might not be a good idea.

```{note}
Is is about 10 times slower to get the full objects instead of only using the resutls of a search!
For 3000 objects that can make a difference of 2 seconds.
```

Instead of loading them all into memory we will use catalog indexes and metadata to get the data we want to display.

Add the new indexes to {file}`profiles/default/catalog.xml`

```{code-block} xml
:emphasize-lines: 6-17, 20-23
:linenos:

<?xml version="1.0"?>
<object name="portal_catalog">
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>
  <index name="type_of_talk" meta_type="FieldIndex">
    <indexed_attr value="type_of_talk"/>
  </index>
  <index name="speaker" meta_type="FieldIndex">
    <indexed_attr value="speaker"/>
  </index>
  <index name="audience" meta_type="KeywordIndex">
    <indexed_attr value="audience"/>
  </index>
  <index name="room" meta_type="FieldIndex">
    <indexed_attr value="room"/>
  </index>

  <column value="featured" />
  <column value="type_of_talk" />
  <column value="speaker" />
  <column value="audience" />
  <column value="room" />
</object>
```

This adds new indexes for the three fields we want to show in the listing. Note that _audience_ is a {py:class}`KeywordIndex` because the field is multi-valued, but we want a separate index entry for every value in an object.

The `column ..` entries allow us to display the values of these indexes in the tableview of collections.

- Reinstall the add-on
- Go to <http://localhost:8080/Plone/portal_catalog/manage_catalogAdvanced> to update the catalog
- Go to <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes> to inspect and manage the new indexes

```{seealso}
<https://5.docs.plone.org/develop/plone/searching_and_indexing/indexing.html>
```

````{note}
The new indexes are still empty.
We'll have to reindex them.
To do so by hand go to <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes>, select the new indexes and click {guilabel}`Reindex`.
We could also rebuild the whole catalog by going to the {guilabel}`Advanced` tab and clicking {guilabel}`Clear and Rebuild`.
For large sites that can take a long time.

We could also write an upgrade step to enable the catalog indexes and reindex all talks:

```python
def add_some_indexes(setup):
    setup.runImportStepFromProfile(default_profile, 'catalog')
    for brain in api.content.find(portal_type='talk'):
        obj = brain.getObject()
        obj.reindexObject(idxs=[
          'type_of_talk',
          'speaker',
          'audience',
          'room',
          'featured',
          ])
```
````

```{eval-rst}
..  todo::

    1. Adapt the ``TalkListView`` in Volto to not use ``fullobjects``.
       Instead either pass a list of metadata-fields or use ``metadata_fields=_all`` to get the equivalent of brains as documented in {ref}`plone6docs:retrieving-additional-metadata`.

    2. Adapt the colored audience-blocks in ``TalkView`` in Volto to use the custom index to find all talks for that audience.
       The Volto search needs to support all indexes dynamically for that to work!

        ..  code-block:: jsx

            <Link
              className={`ui label ${color}`}
              to={`/search?portal_type=talk&audience=${audience}`}
              key={audience}
            >
              {audience}
            </Link>
```

(upgrade-steps-customindex-label)=

## Query for custom indexes

The new indexes behave like the ones that Plone has already built in:

```pycon
>>> (Pdb) from Products.CMFCore.utils import getToolByName
>>> (Pdb) catalog = getToolByName(self.context, 'portal_catalog')
>>> (Pdb) catalog(type_of_talk='Keynote')
[<Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
>>> (Pdb) catalog(audience=('Advanced', 'Professional'))
[<Products.ZCatalog.Catalog.mybrains object at 0x10737b870>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b940>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
>>> (Pdb) brain = catalog(type_of_talk='Keynote')[0]
>>> (Pdb) brain.speaker
u'David Glick'
```

If you use the classic frontend with the BrowserView `talklistview` you can now use these new indexes to improve it so we don't have to _wake up_ the objects anymore.

Instead you can use the brains' new attributes.

```{code-block} python
:emphasize-lines: 13-16
:linenos:

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
                'room': brain.room,
                'uuid': brain.UID,
                })
        return results
```

The template does not need to be changed and the result in the browser did not change either.
But when listing a large number of objects the site will now be faster since all the data you use comes from the catalog and the objects do not have to be loaded into memory.

```{eval-rst}
.. todo::

    Explain when having custom indexes and metadata makes sense with Volto.

```

(upgrade-steps-use-indexes-label)=

## Exercise 1

```{note}
This exercise is only relevant for Plone Classic.
```

In fact we could now simplify the view even further by only returning the brains.

Modify {py:class}`TalkListView` to return only brains and adapt the template to these changes. Remember to move `', '.join(brain.audience or [])` into the template.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Here is the class:

```{code-block} python
:linenos:

class TalkListView(BrowserView):
    """ A list of talks
    """

    def talks(self):
        return api.content.find(context=self.context, portal_type='talk')
```

Here is the template:

```{code-block} html
:linenos:

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="ploneconf.site">
<body>
  <metal:content-core fill-slot="content-core">

  <table class="listing"
         id="talks"
         tal:define="brains python:view.talks()">
    <thead>
      <tr>
        <th>Title</th>
        <th>Speaker</th>
        <th>Audience</th>
        <th>Room</th>
      </tr>
    </thead>
    <tbody>
      <tr tal:repeat="brain brains">
        <td>
          <a href=""
             tal:attributes="href python:brain.getURL();
                             title python:brain.Description"
             tal:content="python:brain.Title">
             The 7 sins of Plone development
          </a>
        </td>
        <td tal:content="python:brain.speaker">
            Philip Bauer
        </td>
        <td tal:content="python:', '.join(brain.audience or [])">
            Advanced
        </td>
        <td tal:content="python:brain.room">
            Room 101
        </td>
      </tr>
      <tr tal:condition="not:brains">
        <td colspan=4>
            No talks so far :-(
        </td>
      </tr>
    </tbody>
  </table>

  </metal:content-core>
</body>
</html>
```
````

(upgrade-steps-collection-criteria-label)=

## Add collection criteria

In chapter {doc}`behaviors_1` you already added the field `featured` as a querystring-criterion.

To be able to search content using these new indexes in collections and listing blocks we need to register them as well.

As with all features make sure you only do this if you really need it!

Add criteria for audience, type_of_talk and speaker to the file {file}`profiles/default/registry/querystring.xml`.


```{code-block} xml
:emphasize-lines: 17-54
:linenos:

<?xml version="1.0" encoding="UTF-8"?>
<registry xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          i18n:domain="plone">

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.featured">
    <value key="title">Featured</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.boolean.isTrue</element>
      <element>plone.app.querystring.operation.boolean.isFalse</element>
    </value>
    <value key="group" i18n:translate="">Metadata</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.audience">
    <value key="title">Audience</value>
    <value key="description">A custom speaker index</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.string.is</element>
      <element>plone.app.querystring.operation.string.contains</element>
    </value>
    <value key="group" i18n:translate="">Metadata</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.type_of_talk">
    <value key="title">Type of Talk</value>
    <value key="description">A custom index</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.string.is</element>
      <element>plone.app.querystring.operation.string.contains</element>
    </value>
    <value key="group" i18n:translate="">Metadata</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.speaker">
    <value key="title">Speaker</value>
    <value key="description">A custom index</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.string.is</element>
      <element>plone.app.querystring.operation.string.contains</element>
    </value>
    <value key="group" i18n:translate="">Metadata</value>
  </records>

</registry>
```

```{seealso}
<https://5.docs.plone.org/develop/plone/functionality/collections.html#add-new-collection-criteria-new-style-plone-app-collection-installed>
```

(upgrade-steps-gs-label)=

## Add versioning through GenericSetup

You already enabled the versioning behavior on the content type.
It allows you to specify if versioning should be enabled for each individual object instead of using a default-setting per content type.
See {file}`profiles/default/types/talk.xml`:

```{code-block} xml
:emphasize-lines: 4
:linenos:

<property name="behaviors">
 <element value="plone.dublincore"/>
 <element value="plone.namefromtitle"/>
 <element value="plone.versioning" />
 <element value="ploneconf.featuered"/>
</property>
```

You still need to configure the versioning policy and a diff view for talks.

Add new file {file}`profiles/default/repositorytool.xml`

```{code-block} xml
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
```

Add new file {file}`profiles/default/diff_tool.xml`

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<object>
  <difftypes>
    <type portal_type="talk">
      <field name="any" difftype="Compound Diff for Dexterity types"/>
    </type>
  </difftypes>
</object>
```

## Summary

- You wrote your first upgrade step to move the talks around: yipee!
- Some fields are indexed in the catalog allowing to search for these and making listings much faster
- Versioning for Talks is now properly configured
