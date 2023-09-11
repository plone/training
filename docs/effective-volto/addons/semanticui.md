---
myst:
  html_meta:
    "description": "Extending Semantic UI"
    "property=og:description": "Extending Semantic UI"
    "property=og:title": "Extending SemanticUI"
    "keywords": "Volto, Plone, Semantic UI, CSS, Volto theme"
---

# Extending Semantic UI

Volto uses [Semantic UI](https://semantic-ui.com/) and
[React Semantic UI](https://react.semantic-ui.com)
(via [semantic-ui-less](https://github.com/Semantic-Org/Semantic-UI-LESS))
as development framework. It helps you to create websites with responsive
layouts using human-friendly HTML. Semantic UI treats words and classes as
exchangeable concepts. Classes use syntax from natural languages like
noun/modifier relationships, word order, and plurality to link concepts
intuitively.

Volto uses Semantic-UI for both the public and the "private" administration
interface. See the [Theme](./theme) chapter for details on how to use a different CSS framework for the public part of your theme.

Semantic-UI-LESS has a built-in theming engine based on the following concepts:

- LESS [definitions](https://github.com/Semantic-Org/Semantic-UI-LESS/tree/master/definitions) files (split in globals, collections, elements, etc) to define the basic styles (ex: `definitions/modules/tab.less`)
- A [semantic.less](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/semantic.less) file which imports all the available definition files
- Each definition file
  (ex [tab.less](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/definitions/modules/tab.less)
  is integrated with the theming engine by importing the [magic theme.config](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/theme.config.example)
- which defines the theme name for each component, so that the
  [theme variable overrides](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/definitions/modules/tab.less#L94)
  get loaded for that component
- a Semantic-UI theme is based on a folder structure that mirrors the
  definition files structure, with 2 types of files for each definition file:
  `<name>.variables` and `name.overrides`. The theme.config (which all
  definition files import), via its [theme.less import](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/theme.less)
  tries to import these variable and overrides files from the **default**
  theme, then the **theme** folder, then the **site** folder (which acts as an
  override for the theme). The `theme.less` is Semantic-UIs theming engine.

Volto comes with its own [implementation of
theme.config](https://github.com/plone/volto/blob/7044eca789d836786e9e789036669085cc22bee7/theme/theme.config)
(by shadowing, via webpack resolve aliases, the `../../theme.config` import
path).

Volto's theme is called Pastanaga. It's a typical Semantic-UI theme. For
the new elements and components that don't exist in Semantic-UI, the Pastanaga
theme uses the [extras](https://github.com/plone/volto/tree/master/theme/themes/pastanaga/extras) folder. The downside is that they aren't fully using the Semantic-UI theming engine.

The key to success in Volto theming is to understand how Semantic-UI's theming
engine works and how to manipulate it. Reading the `theme.less` and
understanding it is a must.

Each Volto project brings its own `src/theme.js`, which is the entry point for
Volto's CSS.

```js
import 'semantic-ui-less/semantic.less';
import '@plone/volto/../theme/themes/pastanaga/extras/extras.less';
```

By simply providing your own copy of semantic.less (and changing the above
import), you can tweak which basic semantic-ui definitions are loaded, or even
create new elements. See an example in the [EEA website
frontend](https://github.com/eea/eea-website-frontend/blob/160ecd7924d113966e1ebd6cbe957dca3f228c6b/src/theme.js)

```
& {
  @import '@eeacms/volto-eea-design-system/../theme/themes/eea/extras/hero';
}
```
