---
myst:
  html_meta:
    "description": "In-place migrations"
    "property=og:description": "In-place migrations"
    "property=og:title": "In-place migrations"
    "keywords": "In-place, migrating, upgrade"
---

(inplace-label)=

# In-place migrations

An in-place migration means the content and settings of a Plone installation are updated while Plone is running.
These upgrades use a built-in tool, and basically run upgrade steps that are collected in [plone.app.upgrade](https://github.com/plone/plone.app.upgrade/).

This approach is recommended for all minor version upgrades, and can work fine for most major upgrades.
When dealing with major changes in Plone, or with very large or complex installations, an export-import based migration (see below) is often the better solution.

During in-place migrations, it is advisable to **not make large leaps** between version numbers.
A single upgrade should not try to bridge multiple major version numbers.

In-place migration can get very complex if you need to deal with multiple important changes.
This is a realistic example of a migration from Plone 4 with Archetypes and `LinguaPlone` to Plone 6:

```{image} _static/inplace-migration.png
:alt: The different steps of a complex in-place-migration.
```


## When to use them and when not

Plone has in-place migrations for all versions.
You could migrate a Plone 2.1 site to 6.0 only using in-place migrations.
That does not mean that it is the best option.

When you have only few changes, a small amount of custom code, add-ons, and content types, an in-place migration can be easier and faster.

This is especially true when you **do not** have to navigate any of the {ref}`major changes in Plone <migrations-major-changes-label>`.
For example when you want to upgrade from Plone 5.2 on Python 3 to Plone 6 Classic, an in-place migration is likely the best approach.

The following advice is valid for all in-place migrations, but especially meant for complex migrations.


## A very simple in-place upgrade

For simple cases, it may be enough to update your buildout and press the button {guilabel}`Upgrade` in the form ``@@plone-upgrade``.

In that case when you start your site, and the site root shows the message *"This site configuration is outdated and needs to be upgraded"* below *"Plone is up and running"*:

```{image} _static/upgrade-required.png
:alt: The zope root with the message "This site configuration is outdated and needs to be upgraded"
```

When you click on the button {guilabel}`Upgrade`, you will be forwarded to the view `/Plone/@@plone-upgrade`.
This view lists all the upgrade steps that Plone will run to get from the *Current active configuration* (the Plone version of your database) to the *Latest available configuration* (the Plone version of your code).

In this example, it lists all upgrade steps from Plone 5.2.9 to 6.0.0b2:

```{image} _static/plone-upgrade.png
:alt: The view @@plone-upgrade with all upgrade steps from Plone 5.2.9 to 6.0.0b2
```

After clicking {guilabel}`Upgrade`, the upgrade steps are run.
A report is displayed listing all the things that were done during the upgrade.
It should end with *Your Plone instance is now up-to-date.*:

```{image} _static/plone-upgrade-report.png
:alt: A abbreviated upgrade report
```

A lot of things changed between Plone 5.2 and Plone 6.
Inspect the log to identify some of the major changes for Plone 6:

* The Plone site root object is changed to a Dexterity object.
* The resource registry was rewritten.
* The add-on `collective.dexteritytextindexer` was integrated into Plone.
* ...


````{dropdown} The full log output
:animate: fade-in-slide-down
:icon: question

```console
2022-10-02 10:44:51,093 INFO    [plone.app.upgrade:293][waitress-3] Starting the migration from version: 5217
2022-10-02 10:44:51,094 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to_dx_site_root with dependency strategy upgrade.
2022-10-02 10:44:51,095 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to_dx_site_root
2022-10-02 10:44:51,100 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,120 INFO    [GenericSetup.types:100][waitress-3] Types tool imported.
2022-10-02 10:44:51,130 INFO    [GenericSetup.types:100][waitress-3] 'Plone Site' type info imported.
2022-10-02 10:44:51,134 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Be sure that the Plone Site FTI is a dexterity one
2022-10-02 10:44:51,134 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_setup'
2022-10-02 10:44:51,136 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'MailHost'
2022-10-02 10:44:51,158 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'caching_policy_manager'
2022-10-02 10:44:51,158 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'content_type_registry'
2022-10-02 10:44:51,161 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'error_log'
2022-10-02 10:44:51,161 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'plone_utils'
2022-10-02 10:44:51,162 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_actions'
2022-10-02 10:44:51,162 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_catalog'
2022-10-02 10:44:51,162 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_controlpanel'
2022-10-02 10:44:51,162 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_diff'
2022-10-02 10:44:51,162 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_groupdata'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_groups'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_memberdata'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_membership'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_migration'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_password_reset'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_properties'
2022-10-02 10:44:51,163 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_quickinstaller'
2022-10-02 10:44:51,164 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_registration'
2022-10-02 10:44:51,164 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_skins'
2022-10-02 10:44:51,164 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_types'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_uidannotation'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_uidgenerator'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_uidhandler'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_url'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_view_customizations'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_workflow'
2022-10-02 10:44:51,165 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'translation_service'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_form_controller'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'mimetypes_registry'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_transforms'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_archivist'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_historiesstorage'
2022-10-02 10:44:51,166 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_historyidhandler'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_modifier'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_purgepolicy'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_referencefactories'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_repository'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'acl_users'
2022-10-02 10:44:51,167 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_resources'
2022-10-02 10:44:51,168 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_registry'
2022-10-02 10:44:51,168 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'HTTPCache'
2022-10-02 10:44:51,168 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'RAMCache'
2022-10-02 10:44:51,168 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'ResourceRegistryCache'
2022-10-02 10:44:51,168 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'front-page'
2022-10-02 10:44:51,169 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'news'
2022-10-02 10:44:51,169 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'events'
2022-10-02 10:44:51,170 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'a-easyform'
2022-10-02 10:44:51,170 INFO    [plone.app.upgrade:92][waitress-3] Migrating object 'portal_placeful_workflow'
2022-10-02 10:44:51,170 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Make the Plone Site a dexterity container
2022-10-02 10:44:51,170 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to6000 with dependency strategy ignore.
2022-10-02 10:44:51,170 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to6000
2022-10-02 10:44:51,172 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,174 INFO    [GenericSetup.toolset:100][waitress-3] Toolset imported.
2022-10-02 10:44:51,178 INFO    [GenericSetup.actions:100][waitress-3] Actions tool imported.
2022-10-02 10:44:51,182 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,189 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Run to6000 upgrade profile.
2022-10-02 10:44:51,189 INFO    [plone.app.upgrade:34][waitress-3] Removed broken temp_folder from Zope root.
2022-10-02 10:44:51,190 INFO    [plone.app.upgrade:44][waitress-3] Removed temp_folder from Zope root _mount_points.
2022-10-02 10:44:51,190 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Remove broken temp_folder / tempstorage / Products.TemporaryStorage
2022-10-02 10:44:51,190 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Fix UUID for DX Site Root
2022-10-02 10:44:51,190 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Index the Site Root
2022-10-02 10:44:51,192 INFO    [ZPublisher:220][waitress-3] Changed property use_folder_tabs at /portal_properties/site_properties so value fits the type lines: ('EasyForm',)
2022-10-02 10:44:51,192 INFO    [ZPublisher:220][waitress-3] Changed property typesLinkToFolderContentsInFC at /portal_properties/site_properties so value fits the type lines: ('EasyForm',)
2022-10-02 10:44:51,192 INFO    [ZPublisher:220][waitress-3] Changed property default_page_types at /portal_properties/site_properties so value fits the type lines: ('EasyForm',)
2022-10-02 10:44:51,201 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Fix unicode properties
2022-10-02 10:44:51,201 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to6003 with dependency strategy ignore.
2022-10-02 10:44:51,201 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to6003
2022-10-02 10:44:51,202 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,205 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,210 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Run to6003 upgrade profile.
2022-10-02 10:44:51,210 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to6004 with dependency strategy ignore.
2022-10-02 10:44:51,210 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to6004
2022-10-02 10:44:51,211 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,211 INFO    [GenericSetup.plone.app.viewletmanager:100][waitress-3] Imported.
2022-10-02 10:44:51,212 INFO    [GenericSetup.skins:100][waitress-3] Skins tool imported.
2022-10-02 10:44:51,215 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,216 INFO    [GenericSetup.types:100][waitress-3] 'Event' type info imported.
2022-10-02 10:44:51,224 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Run to6004 upgrade profile.
2022-10-02 10:44:51,225 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:201 with dependency strategy ignore.
2022-10-02 10:44:51,225 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:201
2022-10-02 10:44:51,226 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.jscompilation.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.csscompilation.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.expression.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.enabled.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.depends.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.load_async.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.load_defer.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.compile.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.resources.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.last_compilation.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.develop_javascript.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.develop_css.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.stub_js_modules.
2022-10-02 10:44:51,230 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/resourceregistryt.merge_with.
2022-10-02 10:44:51,231 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:202 with dependency strategy ignore.
2022-10-02 10:44:51,231 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:202
2022-10-02 10:44:51,232 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,243 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:203 with dependency strategy ignore.
2022-10-02 10:44:51,243 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:203
2022-10-02 10:44:51,244 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,254 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:204 with dependency strategy ignore.
2022-10-02 10:44:51,254 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:204
2022-10-02 10:44:51,255 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,270 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:205 with dependency strategy ignore.
2022-10-02 10:44:51,270 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:205
2022-10-02 10:44:51,271 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,275 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:206 with dependency strategy ignore.
2022-10-02 10:44:51,276 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:206
2022-10-02 10:44:51,276 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,366 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:207 with dependency strategy ignore.
2022-10-02 10:44:51,366 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:207
2022-10-02 10:44:51,367 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,371 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:208 with dependency strategy ignore.
2022-10-02 10:44:51,371 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:208
2022-10-02 10:44:51,372 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,379 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.staticresources:default upgraded to version '208'.
2022-10-02 10:44:51,423 INFO    [plone.app.upgrade:187][waitress-3] Removed 1184 records from registry
2022-10-02 10:44:51,424 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle filemanager
2022-10-02 10:44:51,424 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-base
2022-10-02 10:44:51,425 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-datatables
2022-10-02 10:44:51,425 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-editor-tools
2022-10-02 10:44:51,425 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-fontello
2022-10-02 10:44:51,426 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-glyphicons
2022-10-02 10:44:51,426 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-moment
2022-10-02 10:44:51,426 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-tinymce
2022-10-02 10:44:51,427 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle resourceregistry
2022-10-02 10:44:51,427 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle thememapper
2022-10-02 10:44:51,427 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-legacy
2022-10-02 10:44:51,428 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-logged-in
2022-10-02 10:44:51,428 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-session-pseudo-css
2022-10-02 10:44:51,429 INFO    [plone.app.upgrade:225][waitress-3] Removed bundle plone-session-js
2022-10-02 10:44:51,431 INFO    [plone.app.upgrade:246][waitress-3] Removed 52 deprecated bundle attributes from registry
2022-10-02 10:44:51,445 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,447 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,449 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,450 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,451 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,451 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Cleanup resources and bundles
2022-10-02 10:44:51,452 INFO    [plone.app.upgrade:306][waitress-3] Added image scale: huge 1600:65536
2022-10-02 10:44:51,452 INFO    [plone.app.upgrade:306][waitress-3] Added image scale: great 1200:65536
2022-10-02 10:44:51,452 INFO    [plone.app.upgrade:306][waitress-3] Added image scale: larger 1000:65536
2022-10-02 10:44:51,452 INFO    [plone.app.upgrade:306][waitress-3] Added image scale: teaser 600:65536
2022-10-02 10:44:51,452 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Add new image scales.
2022-10-02 10:44:51,452 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to6005 with dependency strategy ignore.
2022-10-02 10:44:51,452 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to6005
2022-10-02 10:44:51,453 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,453 INFO    [GenericSetup.skins:100][waitress-3] Skins tool imported.
2022-10-02 10:44:51,460 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Run to6005 upgrade profile.
2022-10-02 10:44:51,461 INFO    [ProgressHandler:74][waitress-3] Process started (6 objects to go)
2022-10-02 10:44:51,461 INFO    [ProgressHandler:74][waitress-3] Process terminated. Duration: 0.00 seconds
2022-10-02 10:44:51,461 INFO    [plone.app.upgrade:348][waitress-3] Added image_scales column to catalog metadata schema.
2022-10-02 10:44:51,461 INFO    [plone.app.upgrade:360][waitress-3] Updating metadata.
2022-10-02 10:44:51,461 INFO    [ProgressHandler:74][waitress-3] Process started (6 objects to go)
2022-10-02 10:44:51,473 INFO    [ProgressHandler:74][waitress-3] Process terminated. Duration: 0.01 seconds
2022-10-02 10:44:51,473 INFO    [plone.app.upgrade:420][waitress-3] Updated metadata of all brains.
2022-10-02 10:44:51,473 INFO    [plone.app.upgrade:353][waitress-3] Time taken to update catalog for image scales: 0.0 minutes.
2022-10-02 10:44:51,473 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Update catalog brains to add image_scales.
2022-10-02 10:44:51,474 INFO    [Products.CMFEditions.setuphandlers:57][waitress-3] Removed broken RetainATRefs from portal_modifier.
2022-10-02 10:44:51,474 INFO    [Products.CMFEditions.setuphandlers:57][waitress-3] Removed broken NotRetainATRefs from portal_modifier.
2022-10-02 10:44:51,474 INFO    [Products.CMFEditions.setuphandlers:57][waitress-3] Removed broken SkipBlobs from portal_modifier.
2022-10-02 10:44:51,474 INFO    [Products.CMFEditions.setuphandlers:57][waitress-3] Removed broken CloneBlobs from portal_modifier.
2022-10-02 10:44:51,474 INFO    [Products.CMFEditions.setuphandlers:67][waitress-3] Removed CMFEditions from skin layers.
2022-10-02 10:44:51,475 INFO    [Products.CMFEditions.setuphandlers:75][waitress-3] Removed CMFEditions from skin selection Plone Default.
2022-10-02 10:44:51,475 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile Products.CMFEditions:CMFEditions upgraded to version '11'.
2022-10-02 10:44:51,476 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,477 INFO    [GenericSetup.skins:100][waitress-3] Skins tool imported.
2022-10-02 10:44:51,478 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,478 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow upgraded to version '1001'.
2022-10-02 10:44:51,478 INFO    [Products.PlonePAS.upgrades:42][waitress-3] Deleting broken 'Extended Cookie Auth Helper' plugin: '/acl_users/credentials_cookie_auth'
2022-10-02 10:44:51,479 INFO    [Products.PlonePAS.upgrades:49][waitress-3] Adding working 'Cookie Auth Helper' plugin: '/acl_users/credentials_cookie_auth'
2022-10-02 10:44:51,489 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile Products.PlonePAS:PlonePAS upgraded to version '5'.
2022-10-02 10:44:51,489 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.caching:v2 with dependency strategy ignore.
2022-10-02 10:44:51,489 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.caching:v2
2022-10-02 10:44:51,490 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,493 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,502 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,502 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.app.caching:default upgraded to version '3'.
2022-10-02 10:44:51,502 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Collection to string:contenttype/collection
2022-10-02 10:44:51,502 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Collection.
2022-10-02 10:44:51,502 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Document to string:contenttype/document
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Document.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Event to string:contenttype/event
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Event.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI File to string:contenttype/file
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI File.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Folder to string:contenttype/folder
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Folder.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Image to string:contenttype/image
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Image.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Link to string:contenttype/link
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI Link.
2022-10-02 10:44:51,503 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI News Item to string:contenttype/news-item
2022-10-02 10:44:51,504 INFO    [plone.app.contenttypes upgrade:109][waitress-3] Changed icon expression for view/edit action from FTI News Item.
2022-10-02 10:44:51,504 INFO    [plone.app.contenttypes upgrade:53][waitress-3] Set icon_expr property on FTI Plone Site to string:contenttype/plone
2022-10-02 10:44:51,504 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.app.contenttypes:default upgraded to version '3000'.
2022-10-02 10:44:51,506 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,507 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,507 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.app.dexterity:default upgraded to version '2007'.
2022-10-02 10:44:51,508 INFO    [GenericSetup.controlpanel:100][waitress-3] Control panel imported.
2022-10-02 10:44:51,510 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,511 INFO    [GenericSetup.workflow:100][waitress-3] Workflow tool imported.
2022-10-02 10:44:51,525 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.app.discussion:default upgraded to version '2000'.
2022-10-02 10:44:51,525 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.multilingual:to_1000 with dependency strategy ignore.
2022-10-02 10:44:51,525 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.multilingual:to_1000
2022-10-02 10:44:51,526 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,529 INFO    [GenericSetup.types:100][waitress-3] 'LRF' type info imported.
2022-10-02 10:44:51,529 INFO    [GenericSetup.types:100][waitress-3] 'LIF' type info imported.
2022-10-02 10:44:51,530 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.app.multilingual:default upgraded to version '1000'.
2022-10-02 10:44:51,532 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.session:default upgraded to version '1003'.
2022-10-02 10:44:51,533 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:209 with dependency strategy ignore.
2022-10-02 10:44:51,533 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:209
2022-10-02 10:44:51,533 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,684 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:210 with dependency strategy ignore.
2022-10-02 10:44:51,684 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:210
2022-10-02 10:44:51,685 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,690 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:211 with dependency strategy ignore.
2022-10-02 10:44:51,690 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:211
2022-10-02 10:44:51,690 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,694 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:212 with dependency strategy ignore.
2022-10-02 10:44:51,694 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:212
2022-10-02 10:44:51,695 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.jscompilation.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.csscompilation.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.expression.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.enabled.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.depends.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.load_async.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.load_defer.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.compile.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.resources.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.last_compilation.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.develop_javascript.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.develop_css.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.stub_js_modules.
2022-10-02 10:44:51,698 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/jquery.merge_with.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.jscompilation.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.csscompilation.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.expression.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.enabled.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.depends.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.load_async.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.load_defer.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.compile.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.resources.
2022-10-02 10:44:51,699 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.last_compilation.
2022-10-02 10:44:51,700 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.develop_javascript.
2022-10-02 10:44:51,700 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.develop_css.
2022-10-02 10:44:51,700 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.stub_js_modules.
2022-10-02 10:44:51,700 INFO    [GenericSetup.plone.app.registry:100][waitress-3] Removed record plone.bundles/bootstrap-js.merge_with.
2022-10-02 10:44:51,700 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.staticresources.upgrades:213 with dependency strategy ignore.
2022-10-02 10:44:51,700 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.staticresources.upgrades:213
2022-10-02 10:44:51,701 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,860 INFO    [Products.GenericSetup.tool:1207][waitress-3] Profile plone.staticresources:default upgraded to version '213'.
2022-10-02 10:44:51,860 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Upgrade profiles of core Plone modules to specific versions.
2022-10-02 10:44:51,860 INFO    [Products.GenericSetup.tool:1428][waitress-3] Importing profile profile-plone.app.upgrade.v60:to6007 with dependency strategy ignore.
2022-10-02 10:44:51,860 INFO    [Products.GenericSetup.tool:1469][waitress-3] Applying main profile profile-plone.app.upgrade.v60:to6007
2022-10-02 10:44:51,861 INFO    [GenericSetup.rolemap:100][waitress-3] Role / permission map imported.
2022-10-02 10:44:51,865 INFO    [GenericSetup.actions:100][waitress-3] Actions tool imported.
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Run to6007 upgrade profile.
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Add a timezone property to portal memberdata if it is missing.
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Fix the portal action icons.
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:300][waitress-3] Ran upgrade step: Rename the behavior collective.dexteritytextindexer to plone.textindexer
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:313][waitress-3] End of upgrade path, main migration has finished.
2022-10-02 10:44:51,867 INFO    [plone.app.upgrade:319][waitress-3] Starting upgrade of core addons.
2022-10-02 10:44:51,869 INFO    [plone.app.upgrade:321][waitress-3] Done upgrading core addons.
2022-10-02 10:44:51,869 INFO    [plone.app.upgrade:357][waitress-3] Your Plone instance is now up-to-date.
```
````

After that step you should check if you have add-ons that need to be upgraded in the add-ons control panel `/@@prefs_install_products_form`.
Migration steps for add-ons are not in `plone.app.upgrade`, but are contained in an add-on and are maintained by its developers.

In this example `collective.easyform` can be upgraded (from version 3.2.0 to 4.1.0):

```{image} _static/prefs_install_products_form.png
:alt: The view /@@prefs_install_products_form showing that easyform needs to be upgraded
```

After clicking on {guilabel}`Upgrade collective.easyform`, the add-on is up-to-date.
The log of your Plone instance will show what was done during that upgrade:

```console
2022-10-02 10:58:12,920 INFO    [collective.easyform.upgrades:92][waitress-1] Removed easyform.migrate_all_forms registry record
2022-10-02 10:58:12,921 INFO    [Products.GenericSetup.tool:1207][waitress-1] Profile collective.easyform:default upgraded to version '1013'.
```

Now your site should work fine again, and you have upgraded successfully from Plone 5.2 to Plone 6.0.0b2. 🎉🍾


## Complex in-place migrations

More complex migrations need to be separated into several steps that need to be developed, documented, and tested individually.

In the following example, we assume to migrate a Plone 4.3 with multilingual Archetypes content to Plone 6.0 (Classic UI).

```{note}
Most of this information is also contained in the talk [Migrations! Migrations! Migrations!](https://www.youtube-nocookie.com/embed/ZIN1qmhMHJ4?privacy_mode=1) that deals with in-place migrations and the helper package https://github.com/collective/collective.migrationhelpers.
```

The plan is to write upgrade steps for each step, once you know what needs to be done.
See the chapter {ref}`upgrade-steps-label` from the Mastering Plone Training for more information on upgrade steps.


## Step 1: Gather information

Before a migration, you need to know what the database contains:

* What add-ons are installed and what do they do?
* How much content of what type is there?

The code in https://github.com/collective/collective.migrationhelpers/blob/master/src/collective/migrationhelpers/statistics.py has code examples to help answer these questions.


(inplace-prepare-database-label)=

## Step 2: Prepare the database

While still running Plone 4.3, you should prepare your database for a smooth upgrade to Plone 5.2.
This mostly means you remove data you no longer need or that may cause problems.

Make a list of things you need to do.
Often it will contain the following items:

* Disable `solr`
* Disable `ldap-plugin`
* Reindex `portal_catalog`
* Remove any `portal_skin` and `portal_view_customization` overrides
* Release all WebDAV Locks
* Delete obsolete content
* Remove all revisions by clearing out `portal_historiesstorage`
* Disable a custom Diazo theme and switch to the default theme
* Remove obsolete add-ons
* Pack the database

https://github.com/collective/collective.migrationhelpers has upgrade steps for all the above that you can copy and paste.

You will know what to do when you test the migration, and it fails, likely because of one of the above issues.
Migrations are an iterative process, so add new tasks when you run into problems later on.


## Step 2: Migrate from LinguaPlone to plone.app.multilingual

Since `LinguaPlone` does not support Plone 5 (at all), you need to migrate to `plone.app.multilingual` (which has support for Archetypes and Dexterity) while still in Plone 4.3.

There is a builtin migration in `plone.app.multilingual`, but often you need to clean up translations first.
The code in https://github.com/collective/collective.migrationhelpers/blob/master/src/collective/migrationhelpers/linguaplone.py can serve as an example of how to do that, and run the steps provided by `plone.app.multilingual`.


## Step 3: Update installation

Update your buildout to run in Plone 5.2 in Python 2.7.
It is best to do that in another directory since you will have to switch back and forth sometimes until you get the upgrade steps in Plone 4 right.


## Step 4: Run upgrade steps of Plone

In Plone 5.2 you first run the Plone upgrade in `/@@plone-upgrade` as described above.


## Step 5: Migrate to Dexterity

You need to migrate all default and custom content from Archetypes to Dexterity.

```{seealso}
Please read the [migration documentation of `plone.app.contenttypes`](https://github.com/plone/plone.app.contenttypes/tree/2.2.x#migration).
```

There are forms that allow you to do both (migrate default and custom types) through-the-web, but again, you should use upgrade steps instead.

* See https://github.com/collective/collective.migrationhelpers/blob/master/src/collective/migrationhelpers/dexterity.py for upgrade steps that migrate default content as an upgrade step.

* See https://github.com/collective/collective.migrationhelpers/blob/master/src/collective/migrationhelpers/custom_dx_migration.py for upgrade steps that migrate custom content as an upgrade step.
  The target content types need to exist in Dexterity though!

* Safely remove Archetypes: https://github.com/collective/collective.migrationhelpers/blob/master/src/collective/migrationhelpers/archetypes.py


## Step 6: Migrate database to Python 3

Now you need to migrate your existing database.
ZODB itself is compatible with Python 3, but a database created in Python 2.7 cannot be used in Python 3 without modifying it.

Basically you only need to run one command:

```shell
./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding utf8 --encoding-fallback latin1
```

See the chapter {doc}`plone6docs:backend/upgrading/version-specific-migration/upgrade-zodb-to-python3` from the Plone Upgrade Guide for details.

Do not forget to pack the database after you are done!


## Step 7: Find and fix issues in the database

That would be a whole training by itself.
In a nutshell you should do the following:

* Add [zodbverify](https://github.com/plone/zodbverify) (>=1.2.0) to your buildout.
* Run it to collect all issues with objects that cannot be loaded.
* Inspect and fix each type of issue that was reported.

The details are discussed in https://www.starzel.de/blog/zodb-debugging


## Step 8: Upgrade to Plone 6

After packing the database you can:

* Update your buildout to install Plone 6.
* Run the upgrade steps of Plone in `/@@plone-upgrade`.


## Frequent Problems

* The migration can take a long time, especially the migration from Archetypes to Dexterity can take up to 12 hours.
  Consider using an export/import migration instead since that is much faster.
* Your site raises errors due to invalid data. See [Growing pains: PosKeyErrors and other malaises](https://www.youtube-nocookie.com/embed/SwxN3BBxAM8?privacy_mode=1) and https://www.starzel.de/blog/zodb-debugging
* Migrations are hungry for resources.
  You might run out of disk space or memory.


## Further reading

```{seealso}
Documentation:

* {doc}`plone6docs:backend/upgrading/index`

Helper Packages:

* [`collective.migrationhelpers`](https://github.com/collective/collective.migrationhelpers) - Helpers and examples to use during migrations. Useful to copy & paste the code from here to your own packages.
* [`plone.app.upgrade`](https://github.com/plone/plone.app.upgrade/) - Upgrade steps of the Plone core and some useful helpers.
* [`ftw.upgrade`](https://github.com/4teamwork/ftw.upgrade) - An upgrade control panel and upgrade helpers for plone upgrades.

Talks:

* [Migrations! Migrations! Migrations!](https://www.youtube-nocookie.com/embed/ZIN1qmhMHJ4?privacy_mode=1) - Talk at Ploneconf 2019 in Ferrara.
* [How to upgrade sites to Plone 5](https://www.youtube-nocookie.com/embed/bQ-IpO-7F00?privacy_mode=1) - Talk at Ploneconf 2015 in Bucharest.
* [Archetypes to Dexterity Migration](https://vimeo.com/110992921) - Talk at Ploneconf 2014 in Bristol.
* [Migrations, Upgrades and Relaunches](https://www.youtube-nocookie.com/embed/1Qx0JALp3lQ?privacy_mode=1) - Talk at Ploneconf 2013 in Brazilia.
```