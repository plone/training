---
myst:
  html_meta:
    "description": "Migrating Plone sites with collective.exportimport"
    "property=og:description": "Migrating Plone sites with collective.exportimport"
    "property=og:title": "Migrating with collective.exportimport"
    "keywords": "export, import"
---

(exportimport-label)=

# Migrating with `collective.exportimport`

This chapter describes how to export all content and settings that you want to keep from an old site and import it into a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3, and from Archetypes to Dexterity in one migration step
It is recommended for large and complex migrations.

The recommended tool for this is [`collective.exportimport`](https://github.com/collective/collective.exportimport).

With export-import migrations, you can shortcut most of the individual steps required for complex in-place migrations:

```{image} _static/exportimport-migration.png
:alt: The shortcut of a exportimport migration.
```

## collective.exportimport vs plone.exportimport

[`plone.exportimport`](https://github.com/plone/plone.exportimport) is shipped with Plone 6.1 and a great package to export and import data from the same version. It only exports data from Plone 6.x, while `collective.exportimport` works with Plone 4, 5 and 6.
One main use of is to export and import data for a Plone distribution (see [`plone.distribution`](https://github.com/plone/plone.distribution)).

While both use `plone.restapi` to serialize and deserialize data the data-format is slightly different, since they are intended to serve different use-cases.

With [`collective.transmute`](https://github.com/collective/collective.transmute) there is also a tool that - among other things - transforms the data exported with `collective.exportimport` to the format of `plone.exportimport`, so you can export with `collective.exportimport` from an old version of Plone and import with `plone.exportimport` to the newest version. See {ref}`Prepare data with collective.transmute for import with plone.exportimport <transmute-label>`


## When to use it

You can use it for all migrations, but it is especially useful when you encounter complex migrations.

## How does it work?

`collective.exportimport` serializes content and configuration to JSON files.
It uses and extends `plone.restapi` for serializing and deserializing.

Basically, the export of content is a wrapper for this:

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
* Portlets
* Versions
* Redirects

It also does the following:

* Update data to migrate Archetypes to Dexterity
* Update links and images in html to work with Plone 5.2 and 6

It can be used in:

* Plone 4 - 6 (and beyond)

Most of the additional exports and imports are separate from the content because they may require two or more content items.
During import, you cannot be certain that both items already exist when one is imported.
Example: Imagine a relation from A to B. When you try to create the relation while importing A the item B may not have been imported yet.
It also makes it easier to adapt and/or skip these exports and imports to your needs.


## Step 1: Cleanup

Just as for in-place migrations, it is a good idea to {ref}`cleanup your database <inplace-prepare-database-label>` first.

It is not required, but a smaller database without revisions and obsolete content is smaller and easier to handle.
There is no need to uninstall outdated add-ons or migrate to Dexterity, which is usually the hardest step.

The following steps are usually useful:

* Disable `solr`
* Disable `ldap-plugin`
* Reindex `portal_catalog`
* Delete obsolete content
* Remove all revisions by clearing out `portal_historiesstorage`
* Pack the database


## Step 2: Installation

You need to prepare the old site and the new site.

Both the old site (the one with the 4.3 database) and the new site (without a database) need to be extended to have `collective.exportimport` and its dependencies made available.


### Installation in Plone 4.3

Since `plone.restapi` is not shipped with Plone 4.3, you need to add it to the buildout and pin the latest version that supports Python 2 and Archetypes.

I recommend using custom configuration files for that.
Here is an example `export.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# always use the newest version!
collective.exportimport = 1.15
# Use the latest 7.x version for py2 and at support
plone.restapi = 7.8.3
pyrsistent = 0.15.7
hurry.filesize = 0.9
ijson = 3.2.3
```


### Installation in Plone 6.x

For Plone 6, you should use the version of `plone.restapi` that is shipped with Plone.
You only need to add `collective.exportimport` and pin its dependencies:

Here is an example `import.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# always use the newest version!
collective.exportimport = 1.15
# Use the version that is shipped with your Plone version
# plone.restapi = 9.0.0
pyrsistent = 0.19.3
hurry.filesize = 0.9
ijson = 3.2.3
```


## Basic use and options

There is no need to install `collective.exportimport` in the extensions control panel.
You can open the export form `/@@export_content` straight away and configure what you want to export.

Each form has links to all exports and imports.

### Export

In the export form (and in code), you can specify a couple of options:

Content Types to export (`portal_type=None`)
: The content types you want to have exported.
  Ignore those you don't need in the new site anymore.

Path (`path=<current context>`)
: The path in the portal you want exported.
  This allows you to only export parts of the site.

Depth (`depth=-1`)
: Unlimited (`-1`): this item and all children, `0`: this object only, `1`: only direct children of this object, `2`-`10`: children of this object up to the specified level.

Include blobs (`include_blobs=1`)
: Choose between download URLs (`0`), base-64 encoded strings (`1`), and blob paths (`2`).
  The best option is blob paths.

Modify exported data for migrations (`migration=True`)
: Use this if you want to import the data in a newer version of Plone or migrate from Archetypes to Dexterity.
  It does a multitude of changes, including renaming some default values such as `excludeFromNav` (Archetypes) to `exclude_from_nav` (Dexterity).

Include revisions (`include_revisions=False`)
: This exports the content history (versioning) of each exported item.
  Warning: This can significantly slow down the export!

Download (`download_to_server=False`)
: Export as one json-file through the browser (`False`), save as one file on the server (`1`) or save each item as a separate file on the server (`2`).

```{image} _static/export_form.png
:alt: The export form
```


### Import

The import also has some options:

Upload file (`jsonfile=None`)
: Optionally upload a file.

File on server to import (`server_file=None`):
: Or choose a file that is in `/parts/instance/import/` or `/var/instance/import/`.

Handle existing content (`handle_existing_content=0`)
: How should content be handled that exists with the same id/path?
  Options are:
  -   Skip: Don't import at all (`0`),
  -   Replace: Delete item and create new (`1`),
  -   Update: Reuse and only overwrite imported data (`2`),
  -   Ignore: Create with a new id (`3`)

Commit (`commit=None`)
: Do a commit after each specified number of items.

Import all items into the current folder (`import_to_current_folder=False`)
: By default, the old folder structure is recreated.
  This allows you to import every item as flat content in a container.

Import all old revisions (`import_old_revisions=False`)
: This will import the content history (versioning) for each item that has revisions.
  Warning: This can significantly slow down the import!

```{image} _static/import_form.png
:alt: The import form
```


## Step 3: Test export and import out-of-the-box

### Test the export

We will start with exporting all the content in a site.
For a first test, you should open `/@@export_content` and:

* Select all types (except those you want to drop).
* Select option {guilabel}`as blob paths` for {guilabel}`Include blobs`.

Then click {guilabel}`Export`.

You will end up with a large JSON file that you can inspect to see if whether the content was exported correctly.
Take some time to inspect custom content types.

Later when customizing the export, and you have issues with specific types, you only export these types, or only export one of these (for example, by using `/Plone/my-folder/a-special-type/@@export_content`), until you adapt the export to get it just right.

You should also inspect the console output to see if were any issues.

Don't worry about the other exports and imports for now.


### Test the import

Now startup the Plone 6 instance and open the import form `/@@import_content`.

Upload the JSON file created by the export and click `Import`.

Again you should also inspect the console output to see if there were any issues.


## Step 4: Extend default export and import

The exports and imports of `collective.exportimport` are relatively easy to extend.
The preferred way to do that is subclassing and using the many hooks it offers to plug into the export and import process.

Here is a very simple example:

```python
from collective.exportimport.export_content import ExportContent

class CustomExportContent(ExportContent):

    def global_obj_hook(self, obj):
        """Inspect the content item before serialization data.
        Bad: Changing the content item is a horrible idea.
        Good: Return None if you want to skip this particular object.
        """
        return obj

    def global_dict_hook(self, item, obj):
        """Use this to modify or skip the serialized data.
        Return None if you want to skip this particular object.
        """
        return item
```

You need to register this override in ZCML.
To make the override effective, it is registered for a custom browser layer.
This way when you use the view `/@@export_content`, your custom code will be used.

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

To make that easier, there are prepared packages to override the export and import that can be used and added to your own projects:

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
# always use the newest version!
collective.exportimport = 1.9
# Use the latest 7.x version for py2 and at support
plone.restapi = 7.8.0
pyrsistent = 0.15.7
hurry.filesize = 0.9
ijson = 3.1.4
```

After running buildout, the customized export in `src/contentexport/contentexport/export_content.py` will be used.


#### Extend the import with `contentimport`

Go to the buildout of the Plone 6 site, and checkout the package in `src`:

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
# always use the newest version!
collective.exportimport = 1.15
# Use the version that is shipped with your Plone version
# plone.restapi = 8.22.0
pyrsistent = 0.18.1
hurry.filesize = 0.9
ijson = 3.1.4
```

After running the installation, the customized import in `src/contentimport/contentimport/import_content.py` will be used.

```{note}
You should obviously remove the `.git` directory from these repositories and commit its code to your own project.
```


## Step 5: Run all exports and import at once

Now that we have all that done, we can use the views `@@export_all` and `@@import_all` to run all exports and imports at once.

First try the exports using `@@export_all`.
If all goes well, this will add a bunch of JSON files in `var/instance` of the old site's buildout:

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
If the ID of the site is different from `Plone`, then you need to change the name of the file in the import in the view.

This should run all imports, and the new site should be good to go, containing all content and configuration of the old site.


## FAQ

* Exporting the blob-path (`include_blobs=2`) and loading it from the original location uing `export COLLECTIVE_EXPORTIMPORT_BLOB_HOME=/Users/pbauer/workspace/dokpool/Plone/var/blobstorage_prod/` is the best option.
* You can export the blob-path without access to the actual blobs. WIP!
* Images of Archetypes NewsItems will still be base64-encoded because they don't use a blob. These can cause your json-file to get really large.
* Always check "Modify exported data for migrations" (`migration=True`)
* ...


## Step 6: Add fixes, changes, and extensions

The output from the export and import logs should tell you if you need to deal with any data that does not migrate smoothly.

`collective.exportimport` has a couple of hooks that you can use in your own packages `contentexport` and `contentimport`.

This training continues by inspecting, discussing and using the [examples from the documentation of exportimport](https://github.com/collective/collective.exportimport#faq-tips-and-tricks)

Here are some of the discussed examples:

* Using `global_obj_hook` during export
* Using `dict-hooks` during export
* Export/Import placeful workflow policy
* Using `dict-hooks` during import
* Change workflow
* Export/Import Annotations
* Export/Import Marker Interfaces
* Skip versioning during import
* Dealing with validation errors by using a simple setter
* Dealing with validation errors by deferring import
* Handle `LinguaPlone` content
* Alternative ways to handle items without parent
* Export/Import registry settings
* Export/Import Zope Users
* Export/Import properties, registry-settings and installed addons
* Migrate `PloneFormGen` to `Easyform`
* Export and import `collective.cover` content
* Fixing invalid collection queries
* Migrate very old Plone Versions with data created by collective.jsonify

## Fix html

The html generated by Plone 6 Classic differs from Plone 4 and 5 version in various ways. Here are some examples:

* Image-scales in Archetypes were created using urls like `.../myimage/image_large`. In Dexterity we use `.../myimage/@@images/[fieldname]/large` instead.
* The image-tag generated by TinyMCE now requires a data-attributes `data-scale`
* Link- and Image-tags require the uuid of the target as `data-val` to be able to find it during editing.
* Image-Tags now support picture-variants and srcsets.

Exportimport deals with these changes by modifying the html of all richtext-fields and static portlets.
It uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse and update the html and does a pretty good job.

But sometimes you may need additional changes in the html.
For this exportimport allows you to pass additional fixers (methods that modify the html).

Here are examples for some additional fixers and how to use them:

```python
from collective.exportimport.fix_html import fix_html_in_content_fields

class ImportAll(BrowserView):
    def __call__(self):
        # ...
        fixers = [anchor_fixer, table_class_fixer, scale_unscaled_images, remove_spans]
        results = fix_html_in_content_fields(fixers=fixers)
        # ...


def anchor_fixer(text, obj=None):
    """Remove anchors and links without text.
    Volto does not support anchors (yet).
    """
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all("a"):
        if not link.get("href") and not link.text:
            # drop empty links (e.g. anchors)
            link.decompose()
        elif not link.get("href") and link.text:
            # drop links without a href but keep the text
            link.unwrap()
    return soup.decode()


def table_class_fixer(text, obj=None):
    """Cleanup some table-classes"""
    if "table" not in text:
        return text
    dropped_classes = [
        "MsoNormalTable",
        "MsoTableGrid",
    ]
    replaced_classes = {
        "invisible": "invisible-grid",
    }
    soup = BeautifulSoup(text, "html.parser")
    for table in soup.find_all("table"):
        table_classes = table.get("class", [])
        for dropped in dropped_classes:
            if dropped in table_classes:
                table_classes.remove(dropped)
        for old, new in replaced_classes.items():
            if old in table_classes:
                table_classes.remove(old)
                table_classes.append(new)
        # all tables get the default bootstrap table class
        if "table" not in table_classes:
            table_classes.insert(0, "table")

    return soup.decode()


def scale_unscaled_images(text, obj=None):
    """Scale unscaled image"""
    if not text:
        return text
    fallback_scale = "huge"
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup.find_all("img"):
        if "data-val" not in tag.attrs:
            # maybe external image
            continue
        scale = tag["data-scale"]
        # Prevent unscaled images!
        if not scale:
            scale = fallback_scale
            tag["data-scale"] = fallback_scale
        if not tag["src"].endswith(scale):
            tag["src"] = tag["src"] + "/" + scale
    return soup.decode()


def remove_spans(text, obj=None):
    """Remove obsolete spans and smoothify html"""
    if not text:
        return text
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup.find_all("span"):
        style = tag.get("style", "")
        if "font-style:italic" in style or "font-weight:bold" in style:
            continue
        logger.info("Removing %s: %s", tag.name, tag.attrs)
        tag.unwrap()
    soup.smooth()
    return soup.decode()
```

## Migrate to Volto using exportimport

You can reuse the migration-code provided by the form `@@migrate_to_volto` (it is in `plone.volto`) in a migration.

You need to have the Blocks Conversion Tool (https://github.com/plone/blocks-conversion-tool) running that takes care of migrating richtext-values to Volto-blocks.


```python
class ImportAll(BrowserView):
    def __call__(self):
        # ...
        logger.info("Start migrating richtext to blocks...")
        migrate_richtext_to_blocks()
        transaction.commit()
        logger.info("Finished migrating richtext to blocks!")

        view = api.content.get_view("migrate_to_volto", portal, request)
        view.migrate_default_pages = True
        view.slate = True
        view.service_url = "http://localhost:5000/html"
        logger.info("Start migrating Folders to Documents...")
        view.do_migrate_folders()
        transaction.commit()
        logger.info("Finished migrating Folders to Documents!")
        logger.info("Start migrating Collections to Documents...")
        view.migrate_collections()
        transaction.commit()
        logger.info("Finished migrating Collections to Documents!")

```

## Final steps

After everyting else was done you can reset the modification- and creation-dates of all migrated content.

```python
class ImportAll(BrowserView):
    def __call__(self):
        # ...
        reset_dates = api.content.get_view("reset_dates", portal, request)
        reset_dates()
```

Keep in mind though that in a very strict sense you are lying to the users since the migrated content was actually created and modified by the migration...


## Further reading

```{seealso}
[Documentation of collective.exportimport](https://github.com/collective/collective.exportimport/#readme)

Talks:

* [A new hope for migrations and upgrades](https://www.youtube-nocookie.com/embed/6xoXXyGnk4U?privacy_mode=1) - Talk at Ploneconf 2021 (online).
* [collective.exportimport: Tips, tricks and deploying staging content](https://www.youtube-nocookie.com/embed/SfHPKgeA0I0?privacy_mode=1) - Talk at Ploneconf 2021 (online).
* [Make Plone Migrations fun again with collective.exportimport](https://www.youtube-nocookie.com/embed/HEBF5VqlUc8?privacy_mode=1) - Talk at World Plone Day 2021

[Migrating Content with Transmogrifier](https://2022.training.plone.org/transmogrifier/index.html)
```
