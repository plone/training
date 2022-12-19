---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# TTW Customizations

You will learn how to customize the look of your Plone site through the web. Plone allows to change the site logo, favicon, and basic styling through the site control panel.


**Use Case**

- If you want to make quick changes to the look of your Plone site, without touching the code base on the filesystem.

**What you will learn**

- Change the appearance of your Plone site through the web
- Change the site logo
- Change the look of a Plone site by changing CSS custom properties (variables)
- Add extra styles to a Plone site

## Customize Logo

1. Go to the Plone Control Panel: {menuselection}`toolbar --> admin --> Site Setup`

2. Go to the "Site" control panel.

3. You will see this form:

   ```{image} ../theming/_static/change-logo-in-site-control-panel.png
   ```

4. You can now add/edit/remove your custom logo.

For more information, take a look at the [official docs](https://5.docs.plone.org/adapt-and-extend/change-the-logo.html).

## Customize CSS (variables)

1. Go back to the Control Panel.
2. Go to the {guilabel}`Theming` control panel.
3. Go to tab {guilabel}`Advanded settings`.
3. Go to tab: {guilabel}`Custom Styles` underneath.

Your panel should now look like this:

```{image} ../theming/_static/custom_styles.png
:alt: Custom Styles Field
```

The contents of this text field are added after all other style sheets and is similar to the `custom.css` that you maybe know from Plone 4.


```{code-block} scss

header h1 {
  color: red;
}

```

The Plone 6 default theme Barceloneta is based on Bootstrap 5. Bootstrap 5 added support for [CSS custom properties (variables)](https://getbootstrap.com/docs/5.1/customize/css-variables/). This will give quite a range of possibilities to change the look of your Plone site without changing the theme itself or the need to recompile.

Within `:root` you can override, remap or add your own variables.

```{code-block} scss

header h1 {
   color: var(--my-green);
}

:root {

   --my-green: yellowgreen;
   --my-orange: orangered;

   --bs-body-bg: var(--bs-gray-200);
   --bs-body-color: var(--my-orange);

}
```


```{image} ../theming/_static/custom_variables.png
:alt: Custom Variables
```


The availability of those variables will evolve with the development of Bootstrap.
