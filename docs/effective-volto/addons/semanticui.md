# Extending SemanticUI

Volto uses [Semantic UI](https://semantic-ui.com/) and
[React Semantic UI](https://react.semantic-ui.com)
(via [semantic-ui-less](https://github.com/Semantic-Org/Semantic-UI-LESS))
as development framework. It helps you to create websites with responsive
layouts using human-friendly HTML. Semantic UI treats words and classes as
exchangeable concepts. Classes use syntax from natural languages like
noun/modifier relationships, word order, and plurality to link concepts
intuitively.

Semantic-UI-LESS has a builtin theming engine based on the following concepts:

- LESS [definitions](https://github.com/Semantic-Org/Semantic-UI-LESS/tree/master/definitions) files (split in globals, collections, elements, etc) to define the basic styles (ex: `definitions/modules/tab.less`)
- A [semantic.less](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/semantic.less) file which imports all the available definition files
- Each definition file
  (ex [tab.less](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/definitions/modules/tab.less)
  is integrated with the theming engine by importing the [magic theme.config](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/theme.config.example)
- which defines the theme name for each component, so that the
  [theme variable overrides](https://github.com/Semantic-Org/Semantic-UI-LESS/blob/e4395217c1b8b3227c7387284d12f2d9774d33c6/definitions/modules/tab.less#L94)
  get loaded for that component

Volto comes with its own [implementation of
theme.config](https://github.com/plone/volto/blob/7044eca789d836786e9e789036669085cc22bee7/theme/theme.config)
(by shadowing, via webpack resolve aliases, the `../../theme.config` import
path).

Volto's theme is called Pastanaga, which is a typical Semantic-UI theme. For
the new elements and components that don't exist in Semantic-UI, the Pastanaga
theme uses the [extras](https://github.com/plone/volto/tree/master/theme/themes/pastanaga/extras) folder, which isn't fully using the Semantic-UI theming engine.

The key to success in Volto theming is to understand how Semantic-UI's theming
engine works and how to manipulate it.

For example, each Volto project brings has its own `src/theme.js`, from which
the CSS is loaded.

```js
import 'semantic-ui-less/semantic.less';
import '@plone/volto/../theme/themes/pastanaga/extras/extras.less';
```

By simply providing your own copy of semantic.less, you can tweak which basic
semantic-ui definitions are loaded, or even create new elements.

```
& {
  @import '@eeacms/volto-eea-design-system/../theme/themes/eea/extras/hero';
}
```
