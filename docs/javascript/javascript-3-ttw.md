---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Through-The-Web Development

It is possible to include JavaScript functionality without the need to know about any of the tools involved.

```{note}
This is not reccommended for when you need to do a complex and modular implementation.
```

## portal_javascript & portal_css

These two portal tools are no longer used in Plone 5.
They are still present, but nothing should be included in them.

## Resource Registries

This is the new tool included in Plone 5.
From here we will manage everything related to JavaScript and CSS resources.

It can be found right at the bottom of Plone's Control Panel, in the {guilabel}`Advanced` section.

```{figure} _static/resource_registry.png
:align: center
```

## Add Files

We are going to include 2 new resources, a JavaScript file, and a LESS file.

The JavaScript will look like this:

```js
$( document ).ready(function() {
    var links = $('a');
    links.addClass('custom-background');
});
```

The LESS will look like this:

```css
a.custom-background{
    background-color: #F7E1CF;
    color: black;
}
```

- Go to the {guilabel}`Overrides` tab
- Click the {guilabel}`Add file` button
- Name the new file {file}`++plone++static/custom-links.js`
- Paste the contents of the JavaScript section into the textarea
- Click {guilabel}`Save`
- Click the {guilabel}`Add file` button again
- Name the new file {file}`++plone++static/custom-links.less`
- Paste the contents of the CSS section into the textarea
- Click {guilabel}`Save`

## Create The Resource

- Go to the {guilabel}`Registry` tab
- Click the {guilabel}`Add resource` button
- Name it `training-custom-links`
- Under `JS` enter `++plone++static/custom-links.js`
- For the {guilabel}`CSS/LESS` section, click {guilabel}`Add`
- Enter {file}`++plone++static/custom-links.less`

It should look something like this:

```{figure} _static/add_resource.png
:align: center
```

- Click {guilabel}`Save`

## Create The Bundle And Wire Everything Up

- Go to the {guilabel}`Registry` tab
- Click the {guilabel}`Add bundle` button
- Name it `training-custom-bundle`
- Under {guilabel}`Resources` enter `training-custom-links`
- For the {guilabel}`Depends` section, we'll use `plone`
- Make sure {guilabel}`Enabled` is checked

It should look something like this:

```{figure} _static/add_bundle.png
:align: center
```

- Click {guilabel}`Save`

## Build The Bundle

To include changes, you need to build your bundle.
For doing this, you need to click the {guilabel}`Build` under the bundle you want to build.
