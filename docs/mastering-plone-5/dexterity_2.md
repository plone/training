---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-dexterity2-label)=

# Dexterity Types II: Growing Up

````{sidebar} Get the code!

Code for the beginning of this chapter:

```shell
git checkout viewlets_1
```

Code for the end of this chapter:

```shell
git checkout dexterity_2
```

{doc}`code`
````

The existing talks are still lacking some functionality we want to use.

In this part we will:

- add a marker interface to our talk type,
- create custom catalog indexes,
- query the catalog for them,
- enable some more default features for our type.

(plone5-dexterity2-marker-label)=

## Add a marker interface to the talk type

### Marker Interfaces

The content type `Talk` is not yet a _first class citizen_ because it does not implement its own interface.
Interfaces are like nametags, telling other elements who and what you are and what you can do.
A marker interface is like such a nametag.
The talks actually have an auto-generated marker interface `plone.dexterity.schema.generated.Plone_0_talk`.

One problem is that the name of the Plone instance `Plone` is part of that interface name.
If you now moved these types to a site with another name the code that uses these interfaces would no longer find the objects in question.

To create a real name tag we add a new {py:class}`Interface` to {file}`interfaces.py`:

```{code-block} python
:emphasize-lines: 5,12-13
:linenos:

# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface


class IPloneconfSiteLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ITalk(Interface):
    """Marker interface for Talks"""
```

{py:class}`ITalk` is a marker interface.
We can bind Views and Viewlets to content that provide these interfaces.
Lets see how we can provide this Interface.

There are two solutions for this.

1. Let them be instances of a class that implements this Interface.
2. Register this interface as a behavior and enable it on talks.

The first option has an important drawback: only _new_ talks would be instances of the new class.
We would either have to migrate the existing talks or delete them.

So let's register the interface as a behavior in {file}`behaviors/configure.zcml`

```xml
<plone:behavior
    title="Talk"
    name="ploneconf.talk"
    description="Marker interface for talks to be able to bind views to."
    provides="..interfaces.ITalk"
    />
```

And enable it on the type in {file}`profiles/default/types/talk.xml`

```{code-block} xml
:emphasize-lines: 5
:linenos:

<property name="behaviors">
 <element value="plone.dublincore"/>
 <element value="plone.namefromtitle"/>
 <element value="ploneconf.social"/>
 <element value="ploneconf.talk"/>
</property>
```

Either reinstall the add-on, apply the behavior by hand or run an upgrade step (see below) and the interface will be there.

Then we can safely bind the `talkview` to the new marker interface.

```{code-block} xml
:emphasize-lines: 3

<browser:page
    name="talkview"
    for="ploneconf.site.interfaces.ITalk"
    layer="zope.interface.Interface"
    class=".views.TalkView"
    template="templates/talkview.pt"
    permission="zope2.View"
    />
```

Now the `/talkview` can only be used on objects that implement said interface. We can now also query the catalog for objects providing this interface {py:meth}`catalog(object_provides="ploneconf.site.interfaces.ITalk")`.
The `talklistview` and the `demoview` do not get this constraint since they are not only used on talks.

````{note}
Just for completeness sake, this is what would have to happen for the first option (associating the {py:class}`ITalk` interface with a {py:class}`Talk` class):

- Create a new class that inherits from {py:class}`plone.dexterity.content.Container` and implements the marker interface.

  ```python
  from plone.dexterity.content import Container
  from ploneconf.site.interfaces import ITalk
  from zope.interface import implementer

  @implementer(ITalk)
  class Talk(Container):
      """Class for Talks"""
  ```

- Modify the class for new talks in {file}`profiles/default/types/talk.xml`

  ```{code-block} xml
  :emphasize-lines: 3
  :linenos:

  ...
  <property name="add_permission">cmf.AddPortalContent</property>
  <property name="klass">ploneconf.site.content.talk.Talk</property>
  <property name="behaviors">
  ...
  ```

- Create an upgrade step that changes the class of the existing talks.
  A reuseable method to do such a thing is in [plone.app.contenttypes.migration.dxmigration.migrate_base_class_to_new_class](https://github.com/plone/plone.app.contenttypes/blob/ab8ea9f101ea10e1229b0ab1863ffda7c699d72c/plone/app/contenttypes/migration/dxmigration.py#L134).
````

(plone5-dexterity2-upgrades-label)=

## Upgrade steps

When projects evolve you sometimes want to modify various things while the site is already up and brimming with content and users.
Upgrade steps are pieces of code that run when upgrading from one version of an add-on to a newer one.
They can do just about anything.
We will use an upgrade step to enable the new behavior instead of reinstalling the add-on.

We will create an upgrade step that:

- runs the typeinfo step (i.e. loads the GenericSetup configuration stored in `profiles/default/types.xml` and `profiles/default/types/...` so we don't have to reinstall the add-on to have our changes from above take effect) and
- cleans up the talks that might be scattered around the site in the early stages of creating it.
  We will move all talks to a folder `talks` (unless they already are there).

Upgrade steps can be registered in their own ZCML file to prevent cluttering the main {file}`configure.zcml`.
The add-on you created already has a registration for the {file}`upgrades.zcml` in our {file}`configure.zcml`:

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
      description="Update typeinfo and move talks to a folder 'talks'"
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
            # Skip if the talk is already somewhere inside the target folder
            continue
        obj = brain.getObject()
        logger.info('Moving {} to {}'.format(
            obj.absolute_url(), talks_folder.absolute_url()))
        # Move talk to the folder '/the-event/talks'
        api.content.move(
            source=obj,
            target=talks_folder,
            safe_id=True)
```

Note:

- Upgrade steps get the tool `portal_setup` passed as their argument.
- The `portal_setup` tool has a method {py:meth}`runImportStepFromProfile`
- We create the needed folder structure if it does not exists.

After restarting the site we can run the step:

- Go to the {guilabel}`Add-ons` control panel <http://localhost:8080/Plone/prefs_install_products_form>.
  There should now be a new section **Upgrades** and a button to upgrade from 1000 to 1001.
- Run the upgrade step by clicking on it.

On the console you should see logging messages like:

```
INFO ploneconf.site.upgrades Moving http://localhost:8080/Plone/old-talk1 to http://localhost:8080/Plone/the-event/talks
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

(plone5-dexterity2-browserlayer-label)=

## Add a browserlayer

A browserlayer is another such marker interface, but this time on the request.
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


class ITalk(Interface):
    """Marker interface for Talks"""
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

We should bind all views to it.
Here is an example using the `talklistview`.

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

### Exercise

Do you need to bind the viewlet `featured` from the chapter {doc}`viewlets_1` to this new browser layer?

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

No, it would make no difference since the viewlet is already bound to the marker interface {py:class}`ploneconf.site.behaviors.social.ISocial`.
```

(plone5-dexterity2-catalogindex-label)=

## Add catalog indexes

In the `talklistview` we had to wake up all objects to access some of their attributes.
That is OK if we don't have many objects and they are light dexterity objects.
If we had thousands of objects this might not be a good idea.

Instead of loading them all into memory we will use catalog indexes to get the data we want to display.

Add a new file {file}`profiles/default/catalog.xml`

```{code-block} xml
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
  <index name="room" meta_type="FieldIndex">
    <indexed_attr value="room"/>
  </index>
  <index name="featured" meta_type="BooleanIndex">
    <indexed_attr value="featured"/>
  </index>

  <column value="audience" />
  <column value="type_of_talk" />
  <column value="speaker" />
  <column value="room" />
  <column value="featured" />
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

(plone5-dexterity2-customindex-label)=

## Query for custom indexes

The new indexes behave like the ones that Plone has already built in:

```pycon
>>> (Pdb) from Products.CMFCore.utils import getToolByName
>>> (Pdb) catalog = getToolByName(self.context, 'portal_catalog')
>>> (Pdb) catalog(type_of_talk='Keynote')
[<Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
>>> (Pdb) catalog(audience=('Advanced', 'Professionals'))
[<Products.ZCatalog.Catalog.mybrains object at 0x10737b870>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b940>, <Products.ZCatalog.Catalog.mybrains object at 0x10737b9a8>]
>>> (Pdb) brain = catalog(type_of_talk='Keynote')[0]
>>> (Pdb) brain.speaker
u'David Glick'
```

We now can use the new indexes to improve the `talklistview` so we don't have to _wake up_ the objects anymore.
Instead we use the brains' new attributes.

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

(plone5-dexterity2-use-indexes-label)=

## Exercise 1

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

(plone5-dexterity2-collection-criteria-label)=

## Add collection criteria

To be able to search content in collections using these new indexes we would have to register them as criteria for the `querystring` widget that collections use.
As with all features make sure you only do this if you really need it!

Add a new file {file}`profiles/default/registry.xml`

```{code-block} xml
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
```

```{seealso}
<https://5.docs.plone.org/develop/plone/functionality/collections.html#add-new-collection-criteria-new-style-plone-app-collection-installed>
```

(plone5-dexterity2-gs-label)=

## Add versioning through GenericSetup

Configure the versioning policy and a diff view for talks through GenericSetup.

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

Finally you need to activate the versioning behavior on the content type.
Edit {file}`profiles/default/types/talk.xml`:

```{code-block} xml
:emphasize-lines: 6
:linenos:

<property name="behaviors">
 <element value="plone.dublincore"/>
 <element value="plone.namefromtitle"/>
 <element value="ploneconf.social"/>
 <element value="ploneconf.talk"/>
 <element value="plone.versioning" />
</property>
```

```{note}
There is currently a bug that breaks showing diffs when multiple-choice fields were changed.
```

## Summary

The talks are now grown up:

- They provide a interface to which you can bind features like views
- Some fields are indexed in the catalog making the listing faster
- Talks are now versioned
- You wrote your first upgrade step to move the talks around: yipee!
