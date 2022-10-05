---
myst:
  html_meta:
    "description": "Migrating  with collective.exportimport"
    "property=og:description": "Migrating Plone sites with collective.exportimport"
    "property=og:title": "Migrating with collective.exportimport"
    "keywords": "export, import, transmogrifier"
---

(exportimport-label)=

# Migrating with collective.exportimport

Export all content and settings that you want to keep from an old site and import it to a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3 and from Archetypes to Dexterity in one migration-step and is recommended for large and complex migrations.

The recommended tool for this is https://github.com/collective/collective.exportimport. An alternative is transmogrifier (see the training {ref}`training:transmogrifier-label`)

In export-import migrations you can shortcut most of the individual steps required for complex inplace migrations:

```{image} _static/exportimport-migration.png
:alt: The shortcut of a exportimport-migration.
```


## When to use it

You can use it for all migrations, but it is especially usefull when you encounter for complex migrations.

## How does it work?

`collective.exportimport` serializes content and configuration to json-files.
It uses and extends `plone.restapi` for serialising and deserialising.

Basically the export of content is a wrapper for this:

```python
from plone.restapi.interfaces import ISerializeToJson

serializer = getMultiAdapter((obj, request), ISerializeToJson)
data = serializer(include_items=False)
```

And the import of content is a wrapper for this:

```python
from plone.restapi.interfaces import IDeserializeFromJson

obj = _createObjectByType(item["@type"], container, item["id"], **factory_kwargs)
deserializer = getMultiAdapter((obj, request), IDeserializeFromJson)
obj = deserializer(validate_all=False, data=item)
```

It can export and import:

* Content
* Members and groups with their roles
* Relations
* Translations
* Local roles
* The sorting of content (position in parent)
* Discussions/comments
* Versions
* Redirects

Most of the additional exports and imports are separate from the content because they may require two or more content items.
During import you cannot be certain that both items already exist when one is imported.
It also makes it easier to adapt and/or skip these exports and imports to your need.

## Step 1: Cleanup

Like in in-place migrations it is a good idea to {ref}`cleanup your database <inplace-prepare-database-label>` first.

It is not required but a smaller database without revisions and obsolete content is smaller and easier to handle.
There is no need to uninstall outdated addons or migrate to dexterity, which is usually the hardest step.

The following steps are usually useful:

* Disable solr
* Disable ldap-plugin
* Reindex portal_catalog
* Delete obsolete content
* Remove all revisions by clearing out portal_historiesstorage
* Pack the database

## Step 2: Installation

You need to prepare the old site and the new site.

Both, the old site (the one with the 4.3 database) and the new site (without a database) need to be extended to have `collective.exportimport` and its dependencies made available.

### Installation in Plone 4.3

Since `plone.restapi` is not shipped with Plone 4.3 you need to add it to the buildout and pinn the latest version that supports Python 2 and Archetypes.

I recommend using custom config-files for that. Here is a `export.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the latest 7.x version for py2 and at support
plone.restapi = 7.8.0
pyrsistent = 0.15.7
hurry.filesize = 0.9
ijson = 3.1.4
```

### Installation in Plone 6.0

For Plone 6 you should use the version of restapi that is shipped with Plone.
You only need to add exportimport and pinn its dependencies:

Here is a `import.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the version that is shipped with your Plone version
# plone.restapi = 8.22.0
pyrsistent = 0.18.1
hurry.filesize = 0.9
ijson = 3.1.4
```


## Basic use and options

There is no need to install `collective.exportimport` in the extensions controlpanel.
You can open the export-form `/@@export_content` straight away and configure what you want to export.

Each form has links to all exports and imports.

### Export

In the export form (and in code) you can specify a couple of options:

Content Types to export (`portal_type=None`)
: The content types you want to have exported. Ignore those you don't need in the new site anymore.

Path (`path=<current context>`)
: The path in the portal you want exported. This allows you to only export parts of the site

Depth (`depth=-1`)
: Unlimited (`-1`): this item and all children , `0`: this object only, `1`: only direct children of this object, `2`-`10`: children of this object up to the specified level.

Include blobs (`include_blobs=1`)
: Choose between download urls (`0`), base-64 encoded strings (`1`) and blob paths (`2`). The best option is blob paths.

Modify exported data for migrations (`migration=True`)
: Use this if you want to import the data in a newer version of Plone or migrate from Archetypes to Dexterity. It does a multitude of changes, including renaming some default values like `excludeFromNav` (AT) to `exclude_from_nav` (DX).

Include revisions (`include_revisions=False`)
: This exports the content-history (versioning) of each exported item. Warning: This can significantly slow down the export!

Download (`download_to_server=False`)
: Download to local machine save to a file on the server

```{image} _static/export_form.png
:alt: The export form
```


### Import

The import also has some options:

Upload file (`jsonfile=None`)
: Optionally upload a file

File on server to import (`server_file=None`):
: Or choose a file that is in `/parts/instance/import/` or `/var/instance/import/`

Handle existing content (`handle_existing_content=0`)
: How should content be handled that exists with the same id/path?
  Options are:
  Skip: Don't import at all (`0`),
  Replace: Delete item and create new (`1`),
  Update: Reuse and only overwrite imported data (`2`),
  Ignore: Create with a new id (`3`)

Commit (`commit=None`)
: Do a commit after each number of items

Import all items into the current folder (`import_to_current_folder=False`)
: By default the old folder-structure is recreated. This allows you to import every item as flat content in a container.

Import all old revisions (`import_old_revisions=False`)
: This will import the content-history (versioning) for each item that has revisions. Warning: This can significantly slow down the import!

```{image} _static/import_form.png
:alt: The import form
```

## Step 3: Test export and import out-of-the-box

### Test the export

We will start with exporting all the content in a site. For a first test you should open `/@@export_content` and:

* Select all types (except those you want to drop)
* Select option `as blob paths` for **Include blobs**

Then click `Export`.

You will end up with a large json-file that you can inspect to see if it seems that the content was exported correctly.
Take some time to inspect custom content types.

Later when customizing the export and you have issues with a specific types you only export these types or even only export on of these (e.g. by using `/Plone/my-folder/a-special-type/@@export_content`) until you adapted the export to get it just right.

You should also inspect the console output to see if were any issues.

Don't worry about the other exports and imports for now.

### Test the import

Now startup the Plone 6 instance and open the import-form `/@@import_content`.

Upload the json-file created by the export and click `Import`.

Again you should also inspect the console output to see if were any issues.


## Step 4: Extend default export and import

The exports and imports of `collective.exportimport` are relatively easy to extend.
The preferred way to do that is subclassic and using the many hooks it offers to plug into the export and import process.

Here is a very simple example:

```python
from collective.exportimport.export_content import ExportContent

class CustomExportContent(ExportContent):

    def global_obj_hook(self, obj):
        """Inspect the content item before serialisation data.
        Bad: Changing the content-item is a horrible idea.
        Good: Return None if you want to skip this particular object.
        """
        return obj

    def global_dict_hook(self, item, obj):
        """Use this to modify or skip the serialized data.
        Return None if you want to skip this particular object.
        """
        return item
```

You need to register this overrride in zcml.
To make the override effective it is registered for a custom browserlayer.
This way when you use the view `/@@export_content` your custom code will be used.

```xml
<browser:page
    name="export_content"
    for="zope.interface.Interface"
    class=".export_content.CustomExportContent"
    layer="contentexport.interfaces.IContentexportLayer"
    permission="cmf.ManagePortal"
    />
```

The same approach is used for `content_import` and for all other exports and import that you want to customize.

### Add your own extension packages

To make that easier there are pre-prepared packages to override the export and import that can be used and added to your own projects:

* https://github.com/starzel/contentexport
* https://github.com/starzel/contentimport

#### Extend the export with `contentexport`

```console
cd src
git clone https://github.com/starzel/contentexport.git
cd contentexport
```

Update your `export.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport
    contentexport

auto-checkout +=
    contentexport

[sources]
contentexport = fs contentexport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the latest 7.x version for py2 and at support
plone.restapi = 7.8.0
pyrsistent = 0.15.7
hurry.filesize = 0.9
ijson = 3.1.4
```

After running buildout the customized export in `src/contentexport/contentexport/export_content.py` will be used.

#### Extend the import with `contentimport`

Go to the buildout of the Plone 6 site and checkout the package in `src`:

```console
cd src
git clone https://github.com/starzel/contentimport.git
cd contentimport
```

Update your `import.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport
    contentimport

auto-checkout +=
    contentimport

[sources]
contentimport = fs contentimport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the version that is shipped with your Plone version
# plone.restapi = 8.22.0
pyrsistent = 0.18.1
hurry.filesize = 0.9
ijson = 3.1.4
```

After running buildout the customized import in `src/contentimport/contentimport/import_content.py` will be used.

```{note}
You should obviously remove the `.git` directory from these repositories and commit it code to your own project.
```

## Step 5: Run all exports and import at once

Now that we have that we can use the views `@@export_all` and `@@import_all` to run all exports and imports at once.

First try the exports using `@@export_all`.
If all goes well this will add a bunch of json-files in `var/instance` of the old site's buildout:

* `Plone.json` (the name depends on the name of the Plone site)
* `export_defaultpages.json`
* `export_discussion.json`
* `export_localroles.json`
* `export_members.json`
* `export_ordering.json`
* `export_portlets.json`
* `export_redirects.json`
* `export_relations.json`
* `export_translations.json`

Move or copy all of these to the folder `var/instance/import/` of the Plone 6 site.

Now run `@@import_all`.
If the id of the site is different from `Plone` you need to change the name of the file in the import in the view (see https://github.com/starzel/contentimport/blob/main/contentexport/views.py#L47).

This should run all imports and the new site should be good to go and contain all content and configuration of the old site.

## Step 6: Add fixes, changes and extensions

The output from the export- and import-logs should tell you if you need to deal with any data that does not migrate smoothly.

`collective.exportimport` has a couple of hooks that you can use in your own packages `contentexport` and `contentimport`.

This training continues by inspecting, discussing and using the [examples from the documentation of exportimport](https://github.com/collective/collective.exportimport/#faq-tips-and-tricks)

Here are some of the discussed examples:

* Using global_obj_hook during export
* Using dict-hooks during export
* Export/Import placeful workflow policy
* Using dict-hooks during import
* Change workflow
* Export/Import Annotations
* Export/Import Marker Interfaces
* Skip versioning during import
* Dealing with validation errors by using a simple setter
* Dealing with validation errors by deferring import
* Handle LinguaPlone content
* Alternative ways to handle items without parent
* Export/Import registry settings
* Export/Import Zope Users
* Migrate PloneFormGen to Easyform
* Export and import collective.cover content
* Fixing invalid collection queries


## Further reading

```{seealso}

[Documentation of collective.exportimport](https://github.com/collective/collective.exportimport/#readme)

Talks:

* [A new hope for migrations and upgrades](https://www.youtube.com/watch?v=6xoXXyGnk4U) - Talk at Ploneconf 2021 (online).
* [collective.exportimport: Tips, tricks and deploying staging content](https://www.youtube.com/watch?v=SfHPKgeA0I0) - Talk at Ploneconf 2021 (online).
* [Make Plone Migrations fun again with collective.exportimport](https://www.youtube.com/watch?v=HEBF5VqlUc8) - Talk at World Plone Day 2021


Transmogrifier-Training:
{ref}`transmogrifier-label`

```