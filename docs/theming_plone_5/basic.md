---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Basic: Customize The Logo And CSS From The Default Theme

In this section you will:

- Use the Site control panel to add a custom logo
- Customize the look of a Plone site by adjusting Less Variables
- Add a custom toolbar logo

Topics covered:

- The "Site" control panel
- The "Resource Registries" Control Panel
- Resource Registries > Development Mode

## Customize Logo

1. Go to the Plone Control Panel: {menuselection}`toolbar --> admin --> Site Setup`

2. Go to the "Site" control panel.

3. You will see this form:

   ```{image} ../theming/_static/change-logo-in-site-control-panel.png
   ```

4. You can now add/edit/remove your custom logo.

For more information, take a look at the [official docs](https://5.docs.plone.org/adapt-and-extend/change-the-logo.html).

## Customize CSS/Less Variables

1. Go back to the Control Panel.
2. Go to the {guilabel}`Resource Registries` control panel.
3. On the first tab: enable {guilabel}`Development Mode`.
4. In the "plone" bundle below, click on "develop CSS".

Your panel should now look like this:

```{image} ./_static/theming-dev_mode_on.png
:align: center
```

Now we can play with some Less variables:

1. Go to the {guilabel}`Less Variables` tab.

2. Find the variable `plone-left-toolbar-expanded` and set it to 400px.

   ```{image} ./_static/theming-less_var_hack.png
   :align: center
   ```

3. Hit the {guilabel}`Save` button in the upper right and reload the page.

4. Click on the toolbar logo to expand the toolbar: voilá!

You can play around with some other variables, if you want.

```{Warning}
"Development Mode" is expensive for the browser.
Depending on the browser and on the system, you might encounter extreme slowness while rendering the page.
You could see an unthemed page for a while.

Remember to switch it off as soon as you finished tweaking.
```

However, when you now turn off development mode after changing some lesss variables, you will see that the
changes you have just made in the {guilabel}`Less Variables` tab are no longer active in the theme.
Development mode recompiles the theme resources on the fly for every request, but in production mode the
theme will be compiled once or manually from the "Resource Registries" Control Panel. When you install
Plone, the included and active Barceloneta theme is served from the filesystem. These compiled theme
resources on the filesystem cannot be changed from within Plone.

In the next chapter we will make a custom copy of the Barceloneta Theme which will not be stored on the filesystem,
but as a copy in the site database. When you activate this editable copy, your less variables will be included in the
compiled resources of that theme.
