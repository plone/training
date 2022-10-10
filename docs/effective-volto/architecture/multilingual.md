---
myst:
  html_meta:
    "description": "Multilingual"
    "property=og:description": "Multilingual"
    "property=og:title": "Multilingual"
    "keywords": "Volto, Plone, i18n, Multilingual"
---

# Multilingual

This feature has to be enabled and configured both in the backend and in the frontend.

## How to enable

### Backend

Volto provide support for Plone's Multilingual feature.
You need to install Multiligual support in Plone (plone.app.multilingual add-on), that comes available by default since Plone 5 and can be installed in Plone's Add-ons control panel.
This will setup the backend and it will create the Language Root Folders (LRFs) (/de, /en, etc.)

From your Python policy add-on in `profiles/default/registry.xml`:

```xml
<!-- Set default language to de -->
<record name="plone.default_language">
  <value>de</value>
</record>
<!-- Set language to de/en -->
<record name="plone.available_languages">
  <value>
    <element>de</element>
    <element>en</element>
  </value>
</record>
```

```{warning}
The default language and the supported languages must match the one set in the Plone
side, and those should be set using GenericSetup using your policy package, or
manually via the Languages control panel, i.e. en for English, or pt-br for Portuguese (Brazil)
```

### Frontend

You should configure Volto also to declare that the site is multilingual.
You should modify the configuration object (in a project from your `src/config.js` or from your add-on `src/index.js` like:

```js
config.settings.isMultilingual = true;
config.settings.supportedLanguages = ['de', 'en'];
config.settings.defaultLanguage = 'de';
```

## Make code i18n aware

See {ref}`internationalization`.
