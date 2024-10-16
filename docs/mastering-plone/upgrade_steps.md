---
myst:
  html_meta:
    "description": "Provide upgrade steps for your changes."
    "property=og:description": "Provide upgrade steps for your changes."
    "property=og:title": "Upgrade steps"
    "keywords": "Plone, upgrade, versions"
---

(upgrade-steps-label)=

# Upgrade steps

```{card}
In this part you will:

- Write code to update, create and move content
- Create custom catalog indexes
- Create criteria for search and listing blocks
- Enable features with upgrade steps

Tools and techniques covered:

- upgrade steps
```

````{card} Backend chapter

Checkout `ploneconf.site` at tag "schema":

```shell
git checkout schema
```

The code at the end of the chapter:

```shell
git checkout upgrade_steps
```

More info in {doc}`code`
````


(upgrade-steps-upgrades-label)=

## Upgrade steps

You recently changed existing content, when you added the behavior `ploneconf.featured` or when you turned talks into events in the chapter {doc}`events`.

When projects evolve you sometimes want to modify various things while the site is already up and brimming with content and users.
Upgrade steps are pieces of code that run when upgrading from one version of an add-on to a newer one.
They can do just about anything.
We will use an upgrade step to enable the new behavior instead of reinstalling the add-on.

We will create an upgrade step that:

- runs the typeinfo step, i.e. loads the GenericSetup configuration stored in `profiles/default/types.xml` and `profiles/default/types/...` so we don't have to reinstall the add-on to have our changes from above take effect and
- cleans up existing talks that might be scattered around the site in the early stages of creating it.
  We will move all talks to a (folderish) page `talks` (unless they already are there).

Upgrade steps can be registered in their own ZCML file to prevent cluttering the main {file}`configure.zcml`.

Update the {file}`upgrades/configure.zcml`:

```{code-block} xml
:emphasize-lines: 9, 14
  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1000"
      destination="1001"
      >
    <genericsetup:upgradeStep
        title="Update types"
        description="Enable new behaviors et cetera"
        handler="ploneconf.site.upgrades.v1001.update_types"
        />
    <genericsetup:upgradeStep
        title="Clean up site structure"
        description="Move talks to to their page"
        handler="ploneconf.site.upgrades.v1001.cleanup_site_structure"
        />
  </genericsetup:upgradeSteps>
```

The upgrade steps bumps the version number of the GenericSetup profile of {py:mod}`ploneconf.site` from 1000 to 1001.
The version is stored in {file}`profiles/default/metadata.xml`.

Change it to

```xml
<version>1001</version>
```

`GenericSetup` now expects the code as a method {py:meth}`cleanup_site_structure` and {py:meth}`update_types` in the file {file}`upgrades/v1001.py`.
Let's create it.

(upgrade-steps-pycode-label)=

{file}`upgrades/v1001.py`

```{code-block} python
:linenos:

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


default_profile = "profile-ploneconf.site:default"
logger = logging.getLogger(__name__)


def reload_gs_profile(setup_tool):
    """Load default profile"""
    loadMigrationProfile(
        setup_tool,
        default_profile,
    )


def update_types(setup_tool):
    setup_tool.runImportStepFromProfile(default_profile, "typeinfo")


def cleanup_site_structure(setup_tool):
    # Load default profile including new type info
    # This makes 'update_types' superfluous.
    reload_gs_profile(setup_tool)

    portal = api.portal.get()

    # Create the expected site structure
    if "training" not in portal:
        api.content.create(
            container=portal, type="Document", id="training", title="Training"
        )

    if "schedule" not in portal:
        schedule_folder = api.content.create(
            container=portal, type="Document", id="schedule", title="Schedule"
        )
    else:
        schedule_folder = portal["schedule"]
    schedule_folder_url = schedule_folder.absolute_url()

    if "location" not in portal:
        api.content.create(
            container=portal, type="Document", id="location", title="Location"
        )

    if "sponsors" not in portal:
        api.content.create(
            container=portal, type="Document", id="sponsors", title="Sponsors"
        )

    if "sprint" not in portal:
        api.content.create(
            container=portal, type="Document", id="sprint", title="Sprint"
        )

    # Find all talks
    brains = api.content.find(portal_type="talk")
    for brain in brains:
        if schedule_folder_url in brain.getURL():
            # Skip if the talk is already somewhere inside the target folder
            continue
        obj = brain.getObject()
        # Move talk to the folder '/schedule'
        api.content.move(source=obj, target=schedule_folder, safe_id=True)
        logger.info(f"{obj.absolute_url()} moved to {schedule_folder_url}")
```


We create the required site structure if it does not exist yet making extensive use of `plone.api` as discussed in the chapter {doc}`api`.

Have a look at ZMI import steps http://localhost:8080/Plone/portal_setup/manage_importSteps to find the upgrade step id for the type upgrade.

```{figure} _static/import_steps.png
:alt: Import steps

Import step ids for runImportStepFromProfile
```

After restarting the site we can run the upgrade step:

- Go to the {guilabel}`Add-ons` control panel <http://localhost:3000/controlpanel/addons>.
  The add-on `ploneconf.site` should now be marked with an {guilabel}`Upgrade` label and have a button to upgrade from 1000 to 1001.
- Run the upgrade step by clicking on it.

On the console you should see logging messages like:

```
2024-09-15 11:26:14,114 INFO    [ploneconf.site.upgrades.v1001:83][waitress-0] http://localhost:3000/talks/test-talk moved to http://localhost:3000/schedule
```

Alternatively you can also select which upgrade steps to run like this:

- In the ZMI go to _portal_setup_
- Go to the tab {guilabel}`Upgrades`
- Select {guilabel}`ploneconf.site` from the dropdown and click {guilabel}`Choose profile`
- Run the upgrade step.

```{seealso}
<https://5.docs.plone.org/develop/addons/components/genericsetup.html#upgrade-steps>
```

(upgrade-steps-catalog-label)=

## Add catalog index

For the next chapter we need to search for sponsors and get the results with the values of field 'url' and 'level.
We add a metadata column for these fields to not wake up objects on search request.
This would be OK, but time consuming.
The search request gets an attribute from catalog brains unless the attribute is not available, then fetches the real object.

Add the new meta data columns 'level' and 'url' to {file}`profiles/default/catalog.xml`

```{code-block} xml

  <column value="level" />
  <column value="url" />
```

While we are at it, we also add some more indexes and criteria for fields of type talk.
With these indexes and criteria we can create listing and search blocks with facets.

```{code-block} xml
:emphasize-lines: 18-36

<?xml version="1.0" encoding="utf-8"?>
<object name="portal_catalog">
  <index meta_type="BooleanIndex"
         name="featured"
  >
    <indexed_attr value="featured" />
  </index>
  <column value="featured" />

  <index meta_type="KeywordIndex"
         name="type_of_talk"
  >
    <indexed_attr value="type_of_talk" />
  </index>
  <column value="type_of_talk" />


  <index meta_type="FieldIndex"
         name="speaker"
  >
    <indexed_attr value="speaker" />
  </index>
  <index meta_type="KeywordIndex"
         name="audience"
  >
    <indexed_attr value="audience" />
  </index>
  <index meta_type="FieldIndex"
         name="room"
  >
    <indexed_attr value="room" />
  </index>

  <column value="speaker" />
  <column value="audience" />
  <column value="room" />


  <column value="level" />
  <column value="url" />
</object>
```

This adds new indexes for the three fields we want to show in the listing.
Note that _audience_ is a {py:class}`KeywordIndex` because the field is multi-valued, but we want a separate index entry for every value in an object.

A reinstallation of the add-on would leave the new catalog indexes empty.
Therefore we write an upgrade step to not only add indexes and criteria, but also reindex all talks:

`src/ploneconf/site/upgrades/v1001.py`:

```python
def update_indexes(setup_tool):
    # Indexes and metadata
    setup_tool.runImportStepFromProfile(default_profile, "catalog")
    # Criteria
    setup_tool.runImportStepFromProfile(default_profile, "plone.app.registry")
    # Reindexing content
    for brain in api.content.find(portal_type=["talk", "sponsor"]):
        obj = brain.getObject()
        obj.reindexObject()
        logger.info(f"{obj.id} reindexed.")
```

`src/ploneconf/site/upgrades/configure.zcml`:

```{code-block} xml
:emphasize-lines: 21-25
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    >

  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1000"
      destination="1001"
      >
    <genericsetup:upgradeStep
        title="Update types"
        description="Enable new behaviors et cetera"
        handler="ploneconf.site.upgrades.v1001.update_types"
        />
    <genericsetup:upgradeStep
        title="Clean up site structure"
        description="Move talks to to their page"
        handler="ploneconf.site.upgrades.v1001.cleanup_site_structure"
        />
    <genericsetup:upgradeStep
        title="Update catalog"
        description="Add and populate new indexes. Add criteria."
        handler="ploneconf.site.upgrades.v1001.update_indexes"
        />
  </genericsetup:upgradeSteps>

</configure>
```

From time to time you may want to update the catalog manually. To do so, go to <http://localhost:8080/Plone/portal_catalog/manage_catalogIndexes>, select the new indexes and click {guilabel}`Reindex`.
You can also rebuild the whole catalog by going to the {guilabel}`Advanced` tab and clicking {guilabel}`Clear and Rebuild`.


(upgrade-steps-collection-criteria-label)=

## Add collection criteria

The following additional criteria allow us to create a search block constrained to talks with facets to filter for audience, speaker and room.

`profiles/default/registry/querystring.xml`

```{code-block} xml

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.speaker"
  >
    <value key="title">Speaker</value>
    <value key="enabled">True</value>
    <value key="sortable">True</value>
    <value key="operations">
      <element>plone.app.querystring.operation.string.is</element>
      <element>plone.app.querystring.operation.string.contains</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.audience"
  >
    <value key="title">Audience</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.selection.any</element>
      <element>plone.app.querystring.operation.selection.all</element>
      <element>plone.app.querystring.operation.selection.none</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
    <value key="vocabulary">ploneconf.audiences</value>
  </records>

  <records interface="plone.app.querystring.interfaces.IQueryField"
           prefix="plone.app.querystring.field.room"
  >
    <value key="title">Room</value>
    <value key="enabled">True</value>
    <value key="sortable">False</value>
    <value key="operations">
      <element>plone.app.querystring.operation.selection.any</element>
      <element>plone.app.querystring.operation.selection.all</element>
      <element>plone.app.querystring.operation.selection.none</element>
    </value>
    <value key="group"
           i18n:translate=""
    >Metadata</value>
    <value key="vocabulary">ploneconf.rooms</value>
  </records>
```

```{seealso}
For a full list of all existing QueryField declarations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L197.

For a full list of all existing operations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L1.
```


(upgrade-steps-search-block-label)=

## Apply the new criterion to create a search block for talks

As soon as you run the upgrade steps, you can now add a search block to your 'schedule' page that provides facets to filter for audience, et cetera.

```{figure} _static/search_block.png
:alt: search block

search block
```


(upgrade-steps-summary-label)=

## Summary

- You wrote your first upgrade step
  - to enable changes on types
  - update content
  - prepare your site for search and listing blocks for your custom types
