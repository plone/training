---
myst:
  html_meta:
    "description": "How can you configure Volto"
    "property=og:description": "How can you configure Volto"
    "property=og:title": "Most useful volto settings"
    "keywords": "Volto, configuration"
---

# Most useful volto settings

You can configure Volto by modifying settings in a js-file.

This is the original `config.js` of a project where the registry is imported and returned unchanged.

```{code-block} js
import "@plone/volto/config";

export default function applyConfig(config) {
  // Add here your project's configuration here by modifying `config` accordingly
  return config;
}
```

Here three settings are changed:

```{code-block} js
import "@plone/volto/config";

export default function applyConfig(config) {
  config.settings = {
    ...config.settings,
    navDepth: 3,
    openExternalLinkInNewTab: true,
    hasWorkingCopySupport: true,
  };
  return config;
}
```

```{note}
The `...` is a use of the [spread-syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) that "expands" the configuration into its elements and allows to change existing values and add new ones.
```

Some of the settings are duplicates of setting existing in the Plone backend.
For example the setting `supportedLanguages` must match the one set in the Plone registry as `plone.available_languages` and in `plone.default_language`.

To use Volto in a multilingual project you do this:

```{code-block} js
import "@plone/volto/config";

export default function applyConfig(config) {
  config.settings = {
    ...config.settings,
    defaultLanguage: "de",
    isMultilingual: true,
    supportedLanguages: ["en", "de", "fr"],
  };
  return config;
}
```

```{seealso}
{doc}`plone6docs:volto/configuration/multilingual`
```

Here are some more setting you might use in your projects:

- `contentIcons` - configure Content Types icons. See https://6.docs.plone.org/volto/configuration/settings-reference.html#term-contentIcons
- `navDepth` - Navigation levels depth used in the navigation endpoint calls. Increasing this is useful for implementing fat navigation menus.
- `workflowMapping` - colors for workflow states/transitions.
- `openExternalLinkInNewTab`
- `hasWorkingCopySupport`
- `maxFileUploadSize`
- `nonContentRoutes` - A list of path strings which are considered to be outside of plone-restapi's content serialization. For example: `/controlpanel, /login,/sitemap,/personal-information` are all nonContentRoutes.

You can find all existing options in the file [config/index.js](https://github.com/plone/volto/blob/master/src/config/index.js#L73) of Volto itself which is available in your projects in `frontend/omelette/src/config/index.js`.

```{seealso}
Many options are explained in the {doc}`plone6docs:volto/configuration/settings-reference`
```

You can not only change but also extend Volto here by extending existing configuration options or adding new ones.

For example here you add new blocks, cusomize existing blocks or configure what view/template is used for viewing a certain content-type.
Here are the most useful volto settings which we have for a typical volto project.
