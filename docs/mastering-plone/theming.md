---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(theming-mastering-label)=

# Theming

````{sidebar} Plone Classic UI Chapter
```{figure} _static/plone-training-logo-for-classicui.svg
:alt: Plone Classic UI
:class: logo
```

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout user_generated_content
```

Code for the end of this chapter:

```shell
git checkout resources
```
````

We don't do any real theming during the training. Instead we'll only add some style to extend and modify the default theme.

If you want to learn about theming see [the documentation](https://5.docs.plone.org/adapt-and-extend/theming/index.html) and the Training {doc}`../theming/index`

## Add you own css and javascript

You can declare and access static resources like css, javascript or images with special URLs.
The `configure.zcml` of our package already has a declaration for a resource-folder {file}`static`.

```xml
<plone:static
    name="ploneconf.site"
    type="plone"
    directory="static"
    />
```

All files we put in the {file}`static` folder can be accessed via the url <http://localhost:8080/Plone/++plone++ploneconf.site/the_real_filename.css>

Another feature of this folder is that the resources you put in there are editable and overrideable in the browser
using the overrides-tab of the resource registry.

Let's create a file {file}`ploneconf.css` in the {file}`static` folder with some CSS:

```{code-block} CSS
:linenos:

 header #portal-header #portal-searchbox .searchSection {
     display: none;
 }

 body.userrole-contributor #formfield-form-widgets-IEventBasic-start,
 body.userrole-contributor #formfield-form-widgets-IEventBasic-end > *,
 body.userrole-contributor #formfield-form-widgets-IEventBasic-whole_day,
 body.userrole-contributor #formfield-form-widgets-IEventBasic-open_end {
     display: none;
 }

 body.userrole-reviewer #formfield-form-widgets-IEventBasic-start,
 body.userrole-reviewer #formfield-form-widgets-IEventBasic-end > *,
 body.userrole-reviewer #formfield-form-widgets-IEventBasic-whole_day,
 body.userrole-reviewer #formfield-form-widgets-IEventBasic-open_end {
     display: block;
 }
```

The CSS is not very exciting.
It hides the {guilabel}`only in current section` below the search-box (we could also overwrite the viewlet, but ...).

It also hides the event-fields we added in {ref}`events-label` from people submitting their talks.

For exciting CSS, you should take the {ref}`theming-label` training class.

If we now access <http://localhost:8080/Plone/++plone++ploneconf.site/ploneconf.css> we see our CSS file.

Also add a {file}`ploneconf.js` in the same folder but leave it empty for now. You could add some JavaScript to that file later.

## Including custom css and javascript in every page

How do our JavaScript and CSS files get used when visiting the page?
For now the new files are accessible in the browser but we want Plone to use them every time we access the page.

Adding them directly into the HTML is not a good solution, because having many CSS and JS files slows down the page loading.

Instead, we need to register a _bundle_ that contains these files.
Plone will then make sure that all files that are part of this bundle are also deployed.

We need to register our resources with GenericSetup.

Open the file {file}`profiles/default/registry.xml` and add the following:

```{code-block} xml
:linenos:

 <!-- the plonconf bundle -->
 <records prefix="plone.bundles/ploneconf-bundle"
          interface='Products.CMFPlone.interfaces.IBundleRegistry'>
   <value key="resources">
     <element>ploneconf-main</element>
   </value>
   <value key="enabled">True</value>
   <value key="compile">True</value>
   <value key="csscompilation">++plone++ploneconf.site/ploneconf.css</value>
   <value key="jscompilation">++plone++ploneconf.site/ploneconf.js</value>
   <value key="last_compilation"></value>
 </records>
```

The resources that are part of the registered bundle will now be deployed with every request.

% This chapter will be removed. No need to update the url to /theming_plone_5
For more information on working with CSS and JavaScript resources, please see the [resource registry documentation](https://5.docs.plone.org/adapt-and-extend/theming/resourceregistry.html)
or the [Advanced Diazo training class](https://2022.training.plone.org/theming_plone_5/adv-diazo.html).
