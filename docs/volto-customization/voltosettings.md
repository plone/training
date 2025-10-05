---
myst:
  html_meta:
    "description": "How can you configure Volto"
    "property=og:description": "How can you configure Volto"
    "property=og:title": "Most useful volto settings"
    "keywords": "Volto, configuration"
---

# Most useful Volto settings

You can configure Volto by modifying settings in your add-on.

## New approach: using the `config/folder`

Now, add-ons use a modular configuration structure.
Settings and blocks are defined in separate TypeScript files inside the {file}`config/folder` and imported into {file}`index.ts`.

In our add-on, we can modify the file {file}`config/settings.ts`

The following settings have been customized in this add-on:

```ts
import type { ConfigType } from "@plone/registry";

export default function install(config: ConfigType) {
  // Language settings configured with default values
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ["en"];
  config.settings.defaultLanguage = "en";

  // Other settings we have enabled
  config.settings.navDepth = 3;
  config.settings.openExternalLinkInNewTab = true;
  config.settings.hasWorkingCopySupport = true;

  return config;
}
```
This settings file is imported in {file}`index.ts` by default.
You can follow the same approach to add blocks, slots, summary, and other configurations.

For a practical example, see the [Volto Light Theme configuration](https://github.com/kitconcept/volto-light-theme/blob/main/frontend/packages/volto-light-theme/src/index.ts#L79).

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

- `contentIcons` - configure Content Types icons. See [documentation](https://github.com/plone/volto/blob/c72f17d3cb5002548d2c6d74b4498618b937e38a/packages/volto/src/config/index.js#L61).
- `navDepth` - Navigation levels depth used in the navigation endpoint calls. Increasing this is useful for implementing fat navigation menus.
- `workflowMapping` - Configure colors for workflow states/transitions - if you have a custom workflow or want to change the default colors.
- `openExternalLinkInNewTab` - Kind of self-explaining, isn't it?
- `hasWorkingCopySupport` - Enable if `plone.app.iterate` (Working Copy Support) is installed.
- `maxFileUploadSize` - Limit the size of uploads
- `nonContentRoutes` - A list of path strings which are considered to be outside of plone-restapi's content serialization. For example: `/controlpanel, /login,/sitemap,/personal-information` are all nonContentRoutes.

You can find all existing options in the file [`config/index.js`](https://github.com/plone/volto/blob/main/packages/volto/src/config/index.js#L73) of Volto itself which is available in your projects in `frontend/core/packages/volto/src/config/index.js`.

```{seealso}
Many options are explained in the {doc}`plone6docs:volto/configuration/settings-reference`
```

You can not only change but also extend Volto here by extending existing configuration options or adding new ones.

For example here you add new blocks, customize existing blocks or configure what view/template is used when displaying a certain content-type.
