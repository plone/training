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

In our addon we can modify the `index.js`

```js
const applyConfig = (config) => {
  return config;
};

export default applyConfig;
```

Here three settings are changed:

```js
const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    navDepth: 3,
    openExternalLinkInNewTab: true,
    hasWorkingCopySupport: true,
  };
  return config;
};

export default applyConfig;
```

```{note}
The `...` is a use of the <a target="_blank" href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax">spread-syntax</a> that "expands" the configuration into its elements and allows to change existing values and add new ones.
```

```{note}
If you instead make your changes in the project (i.e. not using a addon) you make the same changes in the file `config.js` of the project.
```

Some of the settings are duplicates of settings that exist in the Plone backend.
For example the setting `supportedLanguages` must match the one set in the Plone registry as `plone.available_languages` and in `plone.default_language`.

To configure Volto as a multilingual project you do this:

```js
const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    defaultLanguage: "de",
    isMultilingual: true,
    supportedLanguages: ["en", "de", "fr"],
  };
  return config;
};

export default applyConfig;
```

```{seealso}
{doc}`plone6docs:volto/configuration/multilingual`
```

Here are some more setting you might use in your projects:

- `contentIcons` - configure Content Types icons. See <a target="_blank" href="https://6.docs.plone.org/volto/configuration/settings-reference.html#term-contentIcons">documentation</a>.
- `navDepth` - Navigation levels depth used in the navigation endpoint calls. Increasing this is useful for implementing fat navigation menus.
- `workflowMapping` - Configure colors for workflow states/transitions - if you have a custom workflow or want to change the default colors.
- `openExternalLinkInNewTab` - Kind of self-explaining, isn't it?
- `hasWorkingCopySupport` - Enable if `plone.app.iterate` (Working Copy Support) is installed.
- `maxFileUploadSize` - Limit the size of uploads
- `nonContentRoutes` - A list of path strings which are considered to be outside of plone-restapi's content serialization. For example: `/controlpanel, /login,/sitemap,/personal-information` are all nonContentRoutes.

You can find all existing options in the file <a target="_blank" href="https://github.com/plone/volto/blob/main/src/config/index.js#L73">config/index.js</a> of Volto itself which is available in your projects in `frontend/omelette/src/config/index.js`.

```{seealso}
Many options are explained in the {doc}`plone6docs:volto/configuration/settings-reference`
```

You can not only change but also extend Volto here by extending existing configuration options or adding new ones.

For example here you add new blocks, customize existing blocks or configure what view/template is used when displaying a certain content-type.
