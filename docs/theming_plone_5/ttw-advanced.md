---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# TTW Theming I: Introduction To Diazo Theming

In this section you will:

- Use the "Theming" control panel to make a copy of Plone's default theme ({term}`Barceloneta`)
- Customize a theme using {term}`Diazo` rules
- Customize a theme by editing and compiling {term}`Less` files

Topics covered:

- {term}`Diazo` and plone.app.theming
- The Default Plone Theme ({term}`Barceloneta`)
- The "Theming Tool"
- Building CSS in the "Theming Tool"
- CSS classes of the `<body>` element
- Conditionally activating {term}`Diazo` rules

## Installation

We will use a [Plone pre-configured Heroku instance](https://github.com/collective/training-sandbox).

Once deployed, create a Plone site.

## Two Approaches To Theming

There are two main approaches to creating a custom theme:

1. Copying the default Barceloneta theme
2. Inheriting from the default Barceloneta theme.

In this section we will work with the first approach

The second one will be covered in detail in {doc}`ttw-advanced-2`.

## What Is Diazo?

{program}`Diazo` is a theming engine used by Plone to make theming a site easier.
At it's core, a {term}`Diazo` theme consists of an HTML page and {file}`rules.xml` file containing directives.

```{note}
You can find extended information about Diazo and its integration package {py:mod}`plone.app.theming`
in the official docs for [Diazo](http://docs.diazo.org/en/latest/) and
[plone.app.theming](https://5.docs.plone.org/external/plone.app.theming/docs/index.html#what-is-a-diazo-theme).
```

## Principles

For this part of the training you just need to know the basic principles of a Diazo theme:

- Plone renders the content of the page.
- Diazo rules inject the content into any static theme.

## Copy Barceloneta Theme

To create our playground we will copy the existing Barceloneta theme.

1. Go to the {guilabel}`Theming` control panel.

2. You will see a list of the available themes.
   In a bare new Plone site, you will see something like this:

   ```{image} ./_static/theming-bare_plone_themes_list.png
   :align: center
   ```

3. Look for the *Barceloneta Theme* and click the {guilabel}`Copy` button next to it.

4. Insert "My theme" as the name and click the checkbox to immediately enable the theme:

   ```{image} ./_static/theming-copy_theme_form.png
   :align: center
   ```

5. Click on {guilabel}`Create` and you get redirected to your new theme's inspector:

   ```{image} ./_static/theming-just_copied_theme_inspector.png
   :align: center
   ```

## Anatomy Of A Diazo Theme

The most important files:

- {file}`manifest.cfg`: contains metadata about the theme ([manifest reference](https://5.docs.plone.org/external/plone.app.theming/docs/index.html#the-manifest-file));
- {file}`rules.xml`: contains the theme rules ([rules reference](https://5.docs.plone.org/external/plone.app.theming/docs/index.html#rules-syntax));
- {file}`index.html`: the static HTML of the theme.

### Exercise 1 - Inspecting The {file}`manifest.cfg`

To better understand how your theme is arranged start by reading the {file}`manifest.cfg` file.

In the theming tool, open the {file}`manifest.cfg` spend a minute or two looking through it, then see if you can answer the questions below.

1. Where are the main rules located for your theme?
2. What property in the {file}`manifest.cfg` file defines the source CSS/Less file used by the theme?
3. What do you think is the purpose of the `prefix` property?

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

1. The main rules are defined by the `rules` property (you could point this anywhere, however the accepted convention is to use a file named {file}`rules.xml`.
2. The `development-css` property points at the main Less file, when compiled to CSS it is placed in the location defined by the `production-css` property.
3. The `prefix` property defines the default location to look for non prefixed files, for example if your prefix is set to `/++theme++mytheme` then a file like index.html will be expected at `/++theme++mytheme/index.html`
```

## CSS Classes For The `<body>` Element

As you browse a Plone site, Plone adds rich information about your current context.
This information is represented as special classes in the `<body>` element.
Information represented by the `<body>` classes includes:

- the current user role  and permissions,
- the current content-type and its template,
- the site section and sub section,
- the current subsite (if any),
- whether this is a frontend view,
- whether icons are enabled.

### `<body>` Classes For An Anonymous Visitor

Below you can see an example of the body classes for a page named "front-page", located in the root of a typical Plone site called "acme":

```html
<body class="template-document_view
             portaltype-document
             site-acme
             section-front-page
             icons-on
             thumbs-on
             frontend
             viewpermission-view
             userrole-anonymous">
```

### `<body>` Classes For A Manager

And here is what the classes for the same page look like when viewed by a manager who has logged in:

```html
<body class="template-document_view
             portaltype-document
             site-acme
             section-front-page
             icons-on
             thumbs-on
             frontend
             viewpermission-view
             userrole-member
             userrole-manager
             userrole-authenticated
             plone-toolbar-left
             plone-toolbar-expanded
             plone-toolbar-left-expanded">
```

Notice the addition of `userrole-manager`.

### Exercise 2 - Discussion About The `<body>` Classes

Look back at the `<body>` classes for a manager. Can you answer the following questions?

1. What other roles does the manager have?
2. Can you see other differences?
3. What do you think the `plone-toolbar-expanded` class does?

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

1. The manager also has the role "member" and "authenticated"
2. There are `plone-toolbar` classes added to the `<body>` element, these control the display of the toolbar
3. The `plone-toolbar-expanded` class is used to control styles used by the expanded version of the toolbar.
```

## Custom Rules

Let's open the default rules file {file}`rules.xml`.
You will see all the rules that are used in the Barceloneta theme right now.
For the time being let's concentrate on how to hack these rules.

### Conditionally Showing Content

```{image} ./_static/theming-viewlet-above-content-in-plone-site.png
:align: center
```

Suppose that we want to make the "above content" block (the one that contains breadcrumbs) conditional, and show it only for authenticated users.

In the {file}`rules.xml` find this line:

```xml
<replace css:content="#viewlet-above-content" css:theme="#above-content" />
```

This rule states that the element that comes from the content (Plone) with the id `#viewlet-above-content` must replace the element with the id `#above-content` in the static theme.

We want to hide it for anonymous users  (hint: we'll use the `<body>` classses we discussed above).

The class we are looking for is `userrole-authenticated`.
Add another attribute to the rule so that we produce this code:

```xml
<replace
    css:if-content="body.userrole-authenticated"
    css:content="#viewlet-above-content"
    css:theme="#above-content" />
```

The attribute `css:if-content` allows us to put a condition on the rule based on a CSS selector that acts on the content.
In this way the rule will be applied only if the body element has the class `.userrole-authenticated`.

We will learn more about Diazo rules in {doc}`ttw-advanced-2`.

## Customize CSS

1. In the theme editor open the file {file}`less/barceloneta.plone.less`.
   This file is the main Less file as specified in the {file}`manifest.cfg`.

2. Add your own customization at the bottom of the file, like:

   ```css
   body {
       background-color: red;
       font-size: 18px;
   }
   ```

   ```{Note}
   Normally you would place this in a separate file to keep the main one clean but for this example it is enough.
   ```

3. Click the buttons {guilabel}`Save` and {guilabel}`Build CSS`.

   ```{image} ./_static/theming-editor_compile_css.png
   :align: center
   ```

4. Go back to the Plone site and reload the page: voilá!

```{Warning}
At the moment you need to "Build CSS" from the main file, the one declared in the manifest (in this case {file}`less/barceloneta.plone.less`).
So, whatever Less file you edit, go back to the main one to compile.
This behavior will be improved in the future, but for now remember this simple rule.
```
