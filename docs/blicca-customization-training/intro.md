---
myst:
    html_meta:
        "description": "How the Blicca JavaScript stack works: Mockup, the Patternslib registry, module federation, and Svelte components."
        "property=og:description": "How the Blicca JavaScript stack works: Mockup, the Patternslib registry, module federation, and Svelte components."
        "property=og:title": "The Blicca JS stack in a nutshell"
        "keywords": "Plone, Blicca, Mockup, Patternslib, module federation, Svelte, registry"
---

(blicca-intro-label)=

# The Blicca JS stack in a nutshell

Before we override anything, let's look at the moving parts.
This chapter is a guided tour with the browser's developer tools, not a slide deck.

## Mockup and the Plone bundle

[Mockup](https://github.com/plone/mockup) is the JavaScript package behind the Plone bundle.
The bundle is shipped by `plone.staticresources` as `++plone++static/bundle-plone/bundle.min.js`, and registered in the resource registry under the name `plone`.

## Patterns and the registry

Patterns are registered in the Patternslib registry.
During the DOM scan, each pattern initializes on the elements that match its trigger, which is a plain CSS selector such as `.pat-tinymce`.

The registry follows one important rule.
**First registration wins.**
A pattern name can only be registered once, and later attempts are ignored.
Remember this rule for {ref}`blicca-replace-pattern-label`.

## Module federation

The Plone bundle is a module federation host.
Add-on bundles are remotes.
The host initializes each remote automatically on document-ready and shares core modules with it, including the Patternslib registry, `@plone/registry`, jQuery, and Bootstrap.
This way, the add-on and the core talk to the same registry instances.

## Svelte components

Newer patterns, such as `pat-contentbrowser`, are Svelte apps.
They pull some of their sub-components from the `@plone/registry` component registry.
That is exactly where add-ons can hook in their own components, as we do in {ref}`blicca-svelte-override-label`.

Why Svelte, and not React?
Svelte compiles components to small, plain JavaScript without a virtual DOM, so the runtime footprint stays small.
That is a good fit for a server-rendered UI that is progressively enhanced with JavaScript.
Components read like HTML, CSS, and JavaScript, which keeps the learning curve flat for integrators.
And Blicca deliberately stays free of React dependencies: it does not need Volto's stack to render a widget.

## See it live

Open your browser's developer tools on any Plone page, and observe the stack at work:

- The `<body>` element carries `data-pat-*` attributes with global pattern options.
- The network tab shows the bundle and its lazily loaded chunks.
- The console logs a message for every initialized module federation bundle:

```console
Patternslib Module Federation: Loaded and initialized bundle "__patternslib_mf__bliccastaticresourceoverride".
```
