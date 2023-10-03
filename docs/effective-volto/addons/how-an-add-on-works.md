---
myst:
  html_meta:
    "description": "How does a Volto add-on work?"
    "property=og:description": "How does a Volto add-on works?"
    "property=og:title": "How does a Volto add-on works?"
    "keywords": "Volto, Plone, Volto add-ons, JavaScript, JavaScript dependencies"
---

# How does a Volto add-on work?

Volto add-on packages are just CommonJS packages. The only requirement is that
they point the `main` key of their `package.json` to a module that exports, as
a default function that acts as a Volto configuration loader.

Similarly to how you develop a Plone backend Python add-on, you can control all aspects of Volto from a Volto add-on.

This gives you the ability to move all your project configuration, components, customizations and even theme files to an add-on. This has the advantage to render the project configuration empty, so you could at any point not only reuse the add-on(s) outside the current project, but also have the project as simply boilerplate that could be replaced at any point (for example, a Volto update).

An add-on can be published in an npm registry, just as any other package. However, Volto add-ons should not be transpiled. They should be released as "source" packages.

See [@kitconcept/volto-blocks-grid](https://github.com/kitconcept/volto-blocks-grid) as an example.

## Loading a Volto Add-on in a project

You should declare in your project that you are using an add-on.
This is done in the project `package.json`, `addons` key:

```json
{
  "name": "my-nice-volto-project",
  "addons": [
    "acme-volto-foo-addon",
    "@plone/some-addon",
    "collective-another-volto-addon"
  ]
}
```

```{warning}
Adding the add-on package to the `addons` key is obligatory! It allows Volto
to treat that package properly and provide it with BabelJS language
features. In Plone terminology, it is like including a Python egg to the
`zcml` section of `zc.buildout`.
```

By including the add-on name in the `addons` key, the add-on's main default export
function is executed, being passed the Volto configuration registry. In that
function, the add-on can customize the registry. The function needs to return
the `config` (Volto configuration registry) object, so that it's passed further
along to the other add-ons.


### Loading a Volto Add-on optional configuration

Some add-ons might choose to allow the Volto project to selectively load some of
their configuration, so they may offer additional optional configuration functions,
which you can load by overloading the add-on name in the `addons`
key in `package.json`, like so:

```{code-block} json
:emphasize-lines: 4

{
  "name": "my-nice-volto-project",
  "addons": [
    "acme-volto-foo-addon:loadOptionalBlocks,overrideSomeDefaultBlock",
    "volto-ga"
  ],
}
```

```{note}
If coming from the Plone backend development, you could map the main add-on configuration to the `default` GenericSetup profile, as it's loaded always. These optional configurations could be mapped to optional GenericSetup profiles that could be applied at any time on demand.
```

### Providing add-on configuration

The default export of your add-on main `index.js` file should be a function with
the signature `config => config`.
That is, it should take the `global` configuration object and return it,
possibly mutated or changed. So your main `index.js` will look like:

```js
export default function applyConfig(config) {
  config.blocks.blocksConfig.faq_viewer = {
    id: 'faq_viewer',
    title: 'FAQ Viewer',
    edit: FAQBlockEdit,
    view: FAQBlockView,
    icon: chartIcon,
    group: 'common',
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    security: {
      addPermission: [],
      view: [],
    },
  };
  return config;
}
```

And the `package.json` file of your add-on:

```json
{
  "main": "src/index.js",
}
```

In effect, Volto does the equivalent of:

```
import installMyVoltoAddon from 'my-volto-addon'

// ... in the configuration registry setup step:
const configRegistry = installMyVoltoAddon(defaultRegistry);
```

So the Volto add-on needs to export a default function
that receives the Volto configuration registry, is free to change the registry
as it sees fit, then it needs to return that registry.

Volto will chain-execute all the add-on configuration functions to compute the
final configuration registry.

```{warning}
An add-on's default configuration method will always be loaded.
```

### Providing optional add-on configurations

You can export additional configuration functions from your add-on's main
`index.js`.

```js
import applyConfig, {loadOptionalBlocks,overrideSomeDefaultBlock} from './config';

export { loadOptionalBlocks, overrideSomeDefaultBlock };
export default applyConfig;
```

## Add-on dependencies

Add-ons can depend on any other JavaScript package, but they can also depend on
other Volto add-ons. To do this, specify the name of your Volto add-on dependency
in your `dependencies` key of `package.json` and create a new `addons` key in
the `package.json` of your add-on, where you specify the extra Volto add-on
dependency.

By doing this, the add-ons can "chain-load" one another, so you don't have to
keep track of intermediary dependencies.
