(plone5-label)=

# What's New in Plone?

This is a list of mayor changes in the last mayor Plone versions.

Plone 5.0 was released in September 2015. Plone 5 was a mayor release, that changed the content type framework, the user interface and the default design.

Plone 5.1 was released in October 2017 and holds a couple of smaller improvements.

Plone 5.2 was released in March 2019. Plone 5.2 is the first version that supports Python 3. It also has some improvements like a new drop-down navigation and built-in url-management.

Plone 6 is not yet released. Plone 6 will only run on Python 3 and will ship with Volto, a new ReactJS-based frontend. The "classic" frontend will stay in place.

## Plone 5.0

(plone5-content-types-label)=

### Content Types

While Plone 4 used Archetypes all default types since Plone 5.0 are based on Dexterity. This means you can use behaviors to change their features and edit them through the web. Existing old content can be migrated to the new types.

### Default Theme

The default theme of Plone 5.x is called [Barceloneta](https://github.com/plone/plonetheme.barceloneta/).

It is a Diazo theme, meaning it uses {py:mod}`plone.app.theming` to insert the output of Plone into static html/css.

It uses html5, so it uses `<header>`, `<nav>`, `<aside>`, `<section>`, `<article>` and `<footer>` for semantic html.

(plone5-ui-widgets-label)=

### New UI and widgets

While Plone 4 had a green edit-bar above the content Plone 5 introduced a toolbar that is located on the left.

The widgets where you input data were also completely rewritten.

(plone5-foldercontents-label)=

### Folder Contents

The view to manage the content of a folder was rewritten and allows a multitude of features.

(plone5-resource-registry-label)=

### Resource Registry

The resource registry was instroduced to configure and edit the static resources (js, css) of Plone. It replaced the old javascript and css registries of Plone 4.

(plone5-chameleon-label)=

### Chameleon template engine

[Chameleon](https://chameleon.readthedocs.io/en/latest/) is the new and much faster rendering engine of Plone 5.

(plone5-control-panel-label)=

### Control panel

- You can finally upload a logo in `@@site-controlpanel`.
- All control panels were moved to z3c.form
- Many small improvements

(plone5-dateformatting-label)=

### Date formatting on the client side

Using the js library moment.js the formatting of dates was moved to the client.

```html
<ul class="pat-moment"
    data-pat-moment="selector:li;format:calendar;">
    <li>${python:context.created().ISO()}</li>
    <li>2015-10-22T12:10:00-05:00</li>
</ul>
```

returns

> - Today at 3:24 PM
> - 10/22/2015

(plone5-multilingual-label)=

### plone.app.multilingual

Plone 5 ships with [plone.app.multilingual](https://github.com/plone/plone.app.multilingual) that is the new default add-on for sites in more than one language.

(plone5-portletmanager-label)=

### New portlet manager

`plone.footerportlets` is a new place to put portlets. The footer (holding the footer, site_actions, colophon) is now built from portlets. This means you can edit the footer TTW.

There is also a useful new portlet type {guilabel}`Actions` used for displaying the site_actions.

## Plone 5.1

Plone 5.1 comes with many incremental improvements. None of these changes the way you develop for Plone. Here are three noteworthy changes:

- The operations for indexing, reindexing and unindexing are queued, optimized and only processed at the end of the transaction. This change can have big performance benefits.
- Actions now have a user-interface in the Plone control panel. You no longer need to use the ZMI to manage them by hand.
- "Retina" Image scales: Plone now has scales for high pixel density images.

For a complete list of changes see <https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_to_51.html#changes-between-plone-5-0-and-5-1>

## Plone 5.2

Plone 5.2 supports Python 2.7, 3.6 and 3.7. It is based on Zope 4.x and runs WSGI. These three are major changes under the hood but have only limited effect on end-users and development of add-ons.

Plone 5.2 comes with many bug fixes and a couple of nice improvements. Here are some noteworthy changes:

- New navigation with dropdown. Site-Administrators can use the navigation control panel `/@@navigation-controlpanel` to configure the dropdown-navigation.
- Plone 5.2 ships with [plone.restapi](https://plonerestapi.readthedocs.io/en/latest/)
- New Login. The old skin-templates and skin-scripts were replaced by browser-views that are much easier to customize.
- Merge Products.RedirectionTool into core. Site-Administrators can use the {guilabel}`URL Management` control panel (`/@@redirection-controlpanel`) to manage and add alternative URLs including bulk upload of alternative urls. As an Editor, you can see the {guilabel}`URL Management` link in the {guilabel}`actions` menu of a content item, and add or remove alternative URLs for this specific content item.

```{seealso}
- [Complete list of changes for Plone 5.2](https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_to_52.html)
- [Upgrade add-ons to Python 3](https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_to_python3.html)
- [Migrate a ZODB from Python 2.7 to Python 3](https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_zodb_to_python3.html)
```

## Plone 6

Plone 6 uses Volto, a new ReactJS-based frontend for Plone implemented on top of the plone.restapi. This combines the stability, maturity, and security of the Plone backend with a modern, mature, user-friendly and well maintained frontend.

Plone 6 continues to allow the current server-side rendering and Diazo theming without Volto. This will be referred to as "Plone Classic". The classic Barceloneta-based frontend in Plone 6 is modernized to use Bootstrap 5. This fontend will stay in place to give developers and users time to adapt to Volto and to provide an easy upgrade-path for existing projects.

Plone 6 will be a long-term support (LTS) release - we anticipate it will be around for several years.

Plone 6 runs on Python 3 only and runs on top of Zope 5.x.
