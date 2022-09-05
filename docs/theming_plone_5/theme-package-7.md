---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Theme Package VII: Advanced Resource Registries Usage

```{note}
For theming in general you don't need to use the **Resource Registries**.
The following infos are here as an example usage of the Plone **Resource Registries**.
```

In **Resource Registries** we can register our static resources, like CSS and LESS files and also JavaScript resources.

In fact even our resources we defined in the {file}`manifest.xml` are registered here automatically, but hidden.

In this chapter we will cover CSS and LESS, but you can also do nice things with your JavaScript resources
(for example using `requirejs` to do the import correctly without worrying about import order).

For details about this, take a look into the documentation of the **Plone Resource Registries** and
in the {doc}`JavaScript part of the training <../javascript/index>`.

## Register CSS And Less Resources In The Registry

Because of the flexibility of Less over CSS we will only use Less files here, but static CSS files can be registered in the same way.
Less files have the advantage that we can use imports, and with `reference-imports` we can even import only the parts of the files which we are really using.

We will now add a new resource to the **Resource Registries**.
To do that, we add an `IResourceRegistry` entry into the {file}`registry.xml` file in our {file}`profiles/default` folder:

```{code-block} xml
:emphasize-lines: 3-8

<?xml version="1.0"?>
<registry>
  <records prefix="plone.resources/conf-main"
           interface='Products.CMFPlone.interfaces.IResourceRegistry'>
    <value key="css">
      <element>++theme++ploneconf-theme/less/custom.less</element>
    </value>
  </records>
</registry>
```

This registers a file named {file}`custom.less` (from our theme package named `ploneconf.theme`) as a *resource* named `conf-main`.
We can now add this resource to a *resource bundle* like the existing `plone` bundle:

```{code-block} xml
:emphasize-lines: 10-16

<?xml version="1.0"?>
<registry>
  <records prefix="plone.resources/conf-main"
           interface='Products.CMFPlone.interfaces.IResourceRegistry'>
    <value key="css">
      <element>++theme++ploneconf-theme/less/custom.less</element>
    </value>
  </records>

  <!-- Bundle definition -->
  <records prefix="plone.bundles/plone"
           interface='Products.CMFPlone.interfaces.IBundleRegistry'>
    <value key="resources" purge="false">
      <element>conf-main</element>
    </value>
  </records>
</registry>
```

This has the advantage of reducing the number of bundles, which also means reducing the amount of files which are loaded for the site,
because every bundle will result in *one* compiled CSS file and *one* compiled JavaScript file.

If we have multiple LESS resources in the same bundle, they will be merged into one compiled CSS file.

We can also create our own custom bundle which contains our resource:

```{code-block} xml
:emphasize-lines: 10-20

<?xml version="1.0"?>
<registry>
  <records prefix="plone.resources/conf-main"
           interface='Products.CMFPlone.interfaces.IResourceRegistry'>
    <value key="css">
      <element>++theme++ploneconf-theme/less/custom.less</element>
    </value>
  </records>

  <!-- Bundle definition -->
  <records prefix="plone.bundles/mycustomtheme"
           interface='Products.CMFPlone.interfaces.IBundleRegistry'>
    <value key="resources" purge="false">
      <element>conf-main</element>
    </value>
    <value key="enabled">True</value>
    <value key="compile">True</value>
    <value key="csscompilation">++theme++ploneconf-theme/less/custom.css</value>
    <value key="last_compilation"></value>
  </records>
</registry>
```

This can make sense if we only want to load that bundle under certain conditions, like only in a specific context.
This could lead to a smaller size of loaded static resources, when they are not all needed.

After making changes to the registry, like adding resources to a bundle, you have to reload the registry configuration via an upgrade step,
or via a uninstall/install of the package.

If you change a bundle, it has to be built or rebuilt.
You can do this in the `@@resourceregistry-controlpanel` by clicking on *Build* for the bundle involved.

````{note}
Before you can compile the bundles TTW (Through-The-Web) you have to adjust the `@barceloneta_path` and `@bootstrap_path`

: variables in the file {file}`theme.less`.

Otherwise Plone can't find the resources and will give you an error during compilation.

```{code-block} less
:emphasize-lines: 1,4

@barceloneta_path: "../barceloneta/less";
...
// import bootstrap files:
@bootstrap_path: "../node_modules/bootstrap/less";
```
````
