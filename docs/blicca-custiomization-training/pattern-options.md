---
myst:
    html_meta:
        "description": "Configure Blicca patterns site-wide with the plone.patternoptions registry record, without writing any JavaScript."
        "property=og:description": "Configure Blicca patterns site-wide with the plone.patternoptions registry record, without writing any JavaScript."
        "property=og:title": "Overrides without JavaScript"
        "keywords": "Plone, Blicca, patternoptions, registry, pattern options, markspeciallinks"
---

(blicca-pattern-options-label)=

# Overrides without JavaScript

Many customizations don't need a single line of JavaScript.
In this chapter, we make external links open in a new window, site-wide, with pure XML.

## How pattern options travel

The registry record `plone.patternoptions` is a dictionary that maps a pattern name to a JSON string of options.
Plone renders each entry as a `data-pat-<name>` attribute on the `<body>` element.
The pattern's options parser walks up the DOM tree, so every pattern element inherits these options.

Plone itself uses this mechanism, and configures `pickadate` and `plone-modal` this way.

## Exercise: change options through the web

Open {menuselection}`Site Setup --> Management --> Configuration Registry` and search for `plone.patternoptions`.
Add an entry with the key `markspeciallinks` and the value:

```json
{ "external_links_open_new_window": "true" }
```

Reload the page, and inspect the `<body>` element in the developer tools.
Notice the new `data-pat-markspeciallinks` attribute.
External links in the content area now open in a new window.

## Persist it in a GenericSetup profile

A through-the-web change lives in the database only.
We persist it in the add-on's profile instead, in {file}`profiles/default/registry/patternoptions.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<registry>
  <record name="plone.patternoptions">
    <value purge="false">
      <element key="markspeciallinks">{"external_links_open_new_window": "true"}</element>
    </value>
  </record>
</registry>
```

```{important}
Keep `purge="false"`.
Without it, the import wipes the entries of the Plone core and of other add-ons.
```

## The trigger class catch

Options alone don't run a pattern.
The trigger class must be present in the DOM.

The `pat-markspeciallinks` class on the `<body>` is only rendered when one of Plone's link settings is enabled.
That's why the profile also enables `plone.mark_special_links` in {file}`profiles/default/registry/linksettings.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<registry>
  <record name="plone.mark_special_links">
    <value>True</value>
  </record>
</registry>
```

When a pattern "does nothing", first check the trigger, then the options.

## Precedence

An entry in `plone.patternoptions` overrides the `<body>` attribute that Plone's `IPatternsSettings` adapters render for the same pattern.
This includes the link settings from the control panel.
This is powerful, so be deliberate.

## Checkpoint

External links open in a new tab, and you did not run any build.
