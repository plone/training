---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Theme Package II: Build Your Diazo-Based Theme

In the previous section we {doc}`prepared our setup for our custom theme package <theme-package>`.
Now we will adjust the skeleton we got using `bobtemplates.plone` and build our Diazo theme.

You can start with the example files in the theme folder.
Change the {file}`index.html` and {file}`custom.less` files to customize the default theme to your needs.

As stated above it's the Plone 5 default {term}`Barceloneta` theme plus some custom files you can use to to override or write CSS/Less.

## Use Your Own Static Mockup

If you got a static mockup from your designer or from a website like <https://startbootstrap.com> (where the example template came from),
you can use this without customization and just apply the Diazo rules to it.

Another way is to change the static mockup a little bit to use mostly the same CSS id's and classes like Plone does.
This way it is easier to reuse CSS/Less from Barceloneta and Plone add-ons if needed.

## Download And Prepare A Static Theme

Let's start with an untouched static template, such as this Twitter Bootstrap based one: https://startbootstrap.com/theme/business-casual.
The latest version of that template uses a beta version of Twitter Bootstrap 4.

We are going to use the latest release which uses Twitter Bootstrap 3.
Download it from https://github.com/StartBootstrap/startbootstrap-business-casual/releases/tag/v3.3.7 and extract it into the theme folder.

Replace the {file}`index.html` with the one from the downloaded template.

The content of your theme folder should now look like this:

```console
tree -L 2 src/ploneconf/theme/theme/
src/ploneconf/theme/theme/
├── HOWTO_DEVELOP.rst
├── LICENSE
├── README.md
├── about.html
├── backend.xml
├── barceloneta
│   └── less
├── barceloneta-apple-touch-icon-114x114-precomposed.png
├── barceloneta-apple-touch-icon-144x144-precomposed.png
├── barceloneta-apple-touch-icon-57x57-precomposed.png
├── barceloneta-apple-touch-icon-72x72-precomposed.png
├── barceloneta-apple-touch-icon-precomposed.png
├── barceloneta-apple-touch-icon.png
├── barceloneta-favicon.ico
├── blog.html
├── contact.html
├── css
│   ├── bootstrap.css
│   ├── bootstrap.min.css
│   └── business-casual.css
├── fonts
│   ├── glyphicons-halflings-regular.eot
│   ├── glyphicons-halflings-regular.svg
│   ├── glyphicons-halflings-regular.ttf
│   ├── glyphicons-halflings-regular.woff
│   └── glyphicons-halflings-regular.woff2
├── form-handler-nodb.php
├── form-handler.php
├── img
│   ├── bg.jpg
│   ├── intro-pic.jpg
│   ├── slide-1.jpg
│   ├── slide-2.jpg
│   └── slide-3.jpg
├── index.html
├── js
│   ├── bootstrap.js
│   ├── bootstrap.min.js
│   └── jquery.js
├── less
│   ├── custom.less
│   ├── plone.toolbar.vars.less
│   ├── roboto
│   ├── theme-compiled.css
│   ├── theme.less
│   └── theme.local.less
├── manifest.cfg
├── node_modules
│   └── bootstrap
├── package-lock.json
├── package.json
├── preview.png
├── rules.xml
├── template-overrides
├── tinymce-templates
│   └── image-grid-2x2.html
└── views
    └── slider-images.pt.example

13 directories, 45 files
```

### Preparing The Template

To make the given template {file}`index.html` more useful, we customize it a little bit.

Right before the second box which contains:

```html
<div class="row">
    <div class="box">
        <div class="col-lg-12">
            <hr>
            <h2 class="intro-text text-center">Build a website
                <strong>worth visiting</strong>
            </h2>
```

Add this:

```html
<div class="row">
  <div id="content-container">
    <!-- main content (box2 and box3) comes here -->
  </div>
  <div id="column1-container"></div>
  <div id="column2-container"></div>
</div>
```

And then move the main content (the box 2 and box 3 including the parent `div` with the class `row`) into the `content-container`.

It should now look like this:

```{code-block} html
:emphasize-lines: 1-3,35-38

<div class="row">
  <div id="content-container">
    <!-- main content (box2 and box3) comes here -->

    <div class="row">
      <div class="box">
        <div class="col-lg-12">
          <hr>
          <h2 class="intro-text text-center">Build a website
            <strong>worth visiting</strong>
          </h2>
          <hr>
          <img class="img-responsive img-border img-left" src="img/intro-pic.jpg" alt="">
          <hr class="visible-xs">
          <p>The boxes used in this template are nested inbetween a normal Bootstrap row and the start of your column layout. The boxes will be full-width boxes, so if you want to make them smaller then you will need to customize.</p>
          <p>A huge thanks to <a href="http://join.deathtothestockphoto.com/" target="_blank">Death to the Stock Photo</a> for allowing us to use the beautiful photos that make this template really come to life. When using this template, make sure your photos are decent. Also make sure that the file size on your photos is kept to a minumum to keep load times to a minimum.</p>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc placerat diam quis nisl vestibulum dignissim. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.</p>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="box">
        <div class="col-lg-12">
          <hr>
          <h2 class="intro-text text-center">Beautiful boxes
            <strong>to showcase your content</strong>
          </h2>
          <hr>
          <p>Use as many boxes as you like, and put anything you want in them! They are great for just about anything, the sky's the limit!</p>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc placerat diam quis nisl vestibulum dignissim. In hac habitasse platea dictumst. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.</p>
        </div>
      </div>
    </div>
  </div>
  <div id="column1-container"></div>
  <div id="column2-container"></div>
</div>
```

```{note}
We added the portlet columns *after* the main content.

Using the correct Twitter Bootstrap grid classes we can later *push* the 1st portlet column visually before the main content.
```

### Include Theme CSS

Next we need to include the CSS from the template into our {file}`theme.less` file.
We will add the include of the CSS the template provides in {file}`theme/css/business-casual.css` after the `END OF UTILS` marker,
but before the `custom.less` include:

```{code-block} less
:emphasize-lines: 89

// theme.less file that will be compiled

/* ### PLONE IMPORTS ### */

@barceloneta_path: "barceloneta/less";

// Core variables and mixins
@import "@{barceloneta_path}/fonts.plone.less";
@import "@{barceloneta_path}/variables.plone.less";
@import "@{barceloneta_path}/mixin.prefixes.plone.less";
@import "@{barceloneta_path}/mixin.tabfocus.plone.less";
@import "@{barceloneta_path}/mixin.images.plone.less";
@import "@{barceloneta_path}/mixin.forms.plone.less";
@import "@{barceloneta_path}/mixin.borderradius.plone.less";
@import "@{barceloneta_path}/mixin.buttons.plone.less";
@import "@{barceloneta_path}/mixin.clearfix.plone.less";
// @import "@{barceloneta_path}/mixin.gridframework.plone.less"; //grid Bootstrap
@import "@{barceloneta_path}/mixin.grid.plone.less"; //grid Bootstrap

@import "@{barceloneta_path}/normalize.plone.less";
@import "@{barceloneta_path}/print.plone.less";
@import "@{barceloneta_path}/code.plone.less";

// Core CSS
@import "@{barceloneta_path}/grid.plone.less";
@import "@{barceloneta_path}/scaffolding.plone.less";
@import "@{barceloneta_path}/type.plone.less";
@import "@{barceloneta_path}/tables.plone.less";
@import "@{barceloneta_path}/forms.plone.less";
@import "@{barceloneta_path}/buttons.plone.less";
@import "@{barceloneta_path}/states.plone.less";

// Components
@import "@{barceloneta_path}/breadcrumbs.plone.less";
@import "@{barceloneta_path}/pagination.plone.less";
@import "@{barceloneta_path}/formtabbing.plone.less"; //pattern
@import "@{barceloneta_path}/views.plone.less";
@import "@{barceloneta_path}/thumbs.plone.less";
@import "@{barceloneta_path}/alerts.plone.less";
@import "@{barceloneta_path}/portlets.plone.less";
@import "@{barceloneta_path}/controlpanels.plone.less";
@import "@{barceloneta_path}/tags.plone.less";
@import "@{barceloneta_path}/contents.plone.less";

// Patterns
@import "@{barceloneta_path}/accessibility.plone.less";
@import "@{barceloneta_path}/toc.plone.less";
@import "@{barceloneta_path}/dropzone.plone.less";
@import "@{barceloneta_path}/modal.plone.less";
@import "@{barceloneta_path}/pickadate.plone.less";
@import "@{barceloneta_path}/sortable.plone.less";
@import "@{barceloneta_path}/tablesorter.plone.less";
@import "@{barceloneta_path}/tooltip.plone.less";
@import "@{barceloneta_path}/tree.plone.less";

// Structure
@import "@{barceloneta_path}/header.plone.less";
@import "@{barceloneta_path}/sitenav.plone.less";
@import "@{barceloneta_path}/main.plone.less";
@import "@{barceloneta_path}/footer.plone.less";
@import "@{barceloneta_path}/loginform.plone.less";
@import "@{barceloneta_path}/sitemap.plone.less";

// Products
@import "@{barceloneta_path}/event.plone.less";
@import "@{barceloneta_path}/image.plone.less";
@import "@{barceloneta_path}/behaviors.plone.less";
@import "@{barceloneta_path}/discussion.plone.less";
@import "@{barceloneta_path}/search.plone.less";

/* ### END OF PLONE IMPORTS ### */

/* ### UTILS ### */

// import bootstrap files:
@bootstrap_path: "node_modules/bootstrap/less";

@import "@{bootstrap_path}/variables.less";
@import "@{bootstrap_path}/mixins.less";
@import "@{bootstrap_path}/utilities.less";
@import "@{bootstrap_path}/grid.less";
@import "@{bootstrap_path}/type.less";
@import "@{bootstrap_path}/forms.less";
@import "@{bootstrap_path}/navs.less";
@import "@{bootstrap_path}/navbar.less";
@import "@{bootstrap_path}/carousel.less";

/* ### END OF UTILS ### */
@import (less) "../css/business-casual.css";

// include our custom css/less
@import "custom.less";
```

We include the CSS file here as a {term}`Less` file.
This way we can extend parts of the CSS in our theme (we will do this with the `.box` class in the next section).

```{note}
Don't forget to run {command}`grunt compile` in your package root after you changed the {term}`Less` files.

You can use {command}`grunt watch` to automatically compile your {term}`Less` files to CSS whenver they are changed.
```

## Using Diazo Rules To Map The Theme With Plone Content

Now that we have the static theme, we need to apply the Diazo rules in {file}`rules.xml` to map the Plone content elements to the theme.

First let me explain what we mean when we talk about *content* and *theme*.

*Content* is usually the dynamic generated content on the Plone site, and the *theme* is the static template site.

For example:

```xml
<replace css:theme="#headline" css:content="#firstHeading" />
```

This rule will replace the element with the CSS id `#headline` in the theme with the element with CSS id `#firstHeading` from the generated Plone content.

To inspect the content side, you can open another Browser tab, but instead of <http://localhost:8080/Plone>, use <http://127.0.0.1:8080/Plone>.
In this tab Diazo is disabled, allowing you to use your browser's Inspector or Developer tools to view the DOM structure of the default, unthemed Plone content.

This *unthemed host name* is managed in the {guilabel}`Theming Control Panel` under {guilabel}`Advanced Settings`, where more domains can be added.

For more details on how to use Diazo rules, take a look at <http://docs.diazo.org/en/latest/> and <https://5.docs.plone.org/external/plone.app.theming/docs/index.html>.

With our theme generated from {py:mod}`bobtemplates.plone` we already got a fully functional rule set based on the Plone 5 default Theme:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rules xmlns="http://namespaces.plone.org/diazo"
       xmlns:css="http://namespaces.plone.org/diazo/css"
       xmlns:xhtml="http://www.w3.org/1999/xhtml"
       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
       xmlns:xi="http://www.w3.org/2001/XInclude">

  <theme href="index.html" />
  <notheme css:if-not-content="#visual-portal-wrapper" />

  <rules css:if-content="#portal-top">
    <!-- Attributes -->
    <copy attributes="*" css:theme="html" css:content="html" />
    <!-- Base tag -->
    <before css:theme="title" css:content="base" />
    <!-- Title -->
    <replace css:theme="title" css:content="title" />
    <!-- Pull in Plone Meta -->
    <after css:theme-children="head" css:content="head meta" />
    <!-- Don't use Plone icons, use the theme's -->
    <drop css:content="head link[rel='apple-touch-icon']" />
    <drop css:content="head link[rel='shortcut icon']" />
    <!-- drop the theme style sheets-->
    <drop theme="/html/head/link[rel='stylesheet']" />
    <!-- CSS -->
    <after css:theme-children="head" css:content="head link" />
    <!-- Script -->
    <after css:theme-children="head" css:content="head script" />
  </rules>

  <!-- Copy over the id/class attributes on the body tag. This is important for per-section styling -->
  <copy attributes="*" css:content="body" css:theme="body" />

  <!-- move global nav -->
  <replace css:theme-children="#mainnavigation" css:content-children="#portal-mainnavigation" method="raw" />

  <!-- full-width breadcrumb -->
  <replace css:content="#viewlet-above-content" css:theme="#above-content" />

  <!-- Central column -->
  <replace css:theme="#content-container" method="raw">

    <xsl:variable name="central">
      <xsl:if test="//aside[@id='portal-column-one'] and //aside[@id='portal-column-two']">col-xs-12 col-sm-6</xsl:if>
      <xsl:if test="//aside[@id='portal-column-two'] and not(//aside[@id='portal-column-one'])">col-xs-12 col-sm-9</xsl:if>
      <xsl:if test="//aside[@id='portal-column-one'] and not(//aside[@id='portal-column-two'])">col-xs-12 col-sm-9</xsl:if>
      <xsl:if test="not(//aside[@id='portal-column-one']) and not(//aside[@id='portal-column-two'])">col-xs-12 col-sm-12</xsl:if>
    </xsl:variable>

    <div class="{$central}">
      <!-- <p class="pull-right visible-xs">
        <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
      </p> -->
      <div class="row">
        <div class="col-xs-12 col-sm-12">
          <xsl:apply-templates css:select="#content" />
        </div>
      </div>
      <footer class="row">
        <div class="col-xs-12 col-sm-12">
          <xsl:copy-of css:select="#viewlet-below-content" />
        </div>
      </footer>
    </div>
  </replace>

  <!-- Alert message -->
  <replace css:theme-children="#global_statusmessage" css:content-children="#global_statusmessage" />

  <!-- Left column -->
  <rules css:if-content="#portal-column-one">
    <replace css:theme="#column1-container">
        <div id="sidebar" class="col-xs-6 col-sm-3 sidebar-offcanvas">
          <aside id="portal-column-one">
              <xsl:copy-of css:select="#portal-column-one > *" />
          </aside>
        </div>
    </replace>
  </rules>

  <!-- Right column -->
  <rules css:if-content="#portal-column-two">
    <replace css:theme="#column2-container">
        <div id="sidebar" class="col-xs-6 col-sm-3 sidebar-offcanvas" role="complementary">
          <aside id="portal-column-two">
              <xsl:copy-of css:select="#portal-column-two > *" />
          </aside>
        </div>
    </replace>
  </rules>

  <!-- Content header -->
  <replace css:theme="#portal-top" css:content-children="#portal-top" />

  <!-- Footer -->
  <replace css:theme-children="#portal-footer" css:content-children="#portal-footer-wrapper" />

  <!-- toolbar -->
  <replace css:theme="#portal-toolbar" css:content-children="#edit-bar" css:if-not-content=".ajax_load" css:if-content=".userrole-authenticated" />
  <replace css:theme="#anonymous-actions" css:content-children="#portal-personaltools-wrapper" css:if-not-content=".ajax_load" css:if-content=".userrole-anonymous" />

</rules>
```

As you probably noticed, the theme does not look like it should right now and is missing some important parts like the toolbar.
That is because we are using an HTML template which has a different HTML structure than the one Plone's default theme is using.

We can either change our theme's template to use the same structure and naming for classes and id's, or we can change our rule set to work with the theme template like it is.
We will use the second approach and customize our rule set to work with the provided theme template.

In fact, if you use a better theme template then this one - where more useful CSS classes and id's are used and the grid is defined in CSS/Less and not in the HTML markup itself - it is a lot easier to work with without touching the template.
But we decided to use this popular template as an example and therefor we have to make changes to the template itself.

## Customizing The Ruleset

In this section we will adjust the Diazo rules to place the Plone content into the predefined template sections.

### Plone Toolbar

We start with the toolbar since it is the most important part of the Plone site (for logged in users).
So let's first make sure we have it in our theme template.
We already have the required Diazo rule in our {file}`rules.xml`:

```xml
<!-- toolbar -->
<replace css:theme="#portal-toolbar" css:content-children="#edit-bar" css:if-not-content=".ajax_load" css:if-content=".userrole-authenticated" />
```

The only thing we need is the corresponding HTML part in our theme template:

```{code-block} html
:emphasize-lines: 2

<body>
  <section id="portal-toolbar"></section>
```

You can add it right after the opening body tag in your {file}`index.html`.

### Unthemed Backend

If the only thing you want to do is theme your frontend, and use the default Barceloneta theme for your backend (edit, folder contents, settings),
you can include Barceloneta's {file}`backend.xml`.

To only have your frontend theme rules active when you visit the frontend part of your site, you can wrap the existing rules into another `rules` block:

```{code-block} xml
:emphasize-lines: 1-4,6-7,14

<!-- Include barceloneta's backend.xml for backend theming. -->
<rules css:if-not-content="body.viewpermission-view, body.viewpermission-none">
  <xi:include href="++theme++barceloneta/backend.xml" />
</rules>

<!-- Include theme for frontend theming. -->
<rules css:if-content="body.viewpermission-view, body.viewpermission-none">
  <theme href="index.html" />
  <notheme css:if-not-content="#visual-portal-wrapper" />

  <rules css:if-content="#portal-top">
    <!-- Attributes -->
    ...
  </rules>
</rules>
```

Note that we include the file from the theme directly, and don't use the one we got from {py:mod}`bobtemplates.plone`.

### Login Link & Co

If you want to have a login link for your users, you can put this placeholder in your theme template where you want the link to display.
You can always login into the Plone site by adding `/login` to the Plone url, so it's optional.

You can add it right before the tag `<div class="brand">Business Casual</div>` in your {file}`index.html`.

```{code-block} html
:emphasize-lines: 3

<body>
  <section id="portal-toolbar"></section>
  <div id="anonymous-actions"></div>

  <div class="brand">Business Casual</div>
```

The necessary rule to fill this with the Plone login link is already in our rules.xml.
But because the id for the anonymous tools in Plone changed in one of the recent versions,
we have to update it (change `#portal-personaltools-wrapper` to `#portal-anontools`):

```xml
<replace css:theme="#anonymous-actions" css:content-children="#portal-anontools" css:if-not-content=".ajax_load" css:if-content=".userrole-anonymous" />
```

This will replace your placeholder with `#portal-anontools` from Plone (for example the login link).
The link will only be inserted if the user is not already logged in.

### Top Navigation

In the next step we will replace the menu placeholder with the real Plone top-navigation links.
To do this we adjust this rule from Barceloneta:

```xml
<!-- move global nav -->
<replace css:theme-children="#mainnavigation" css:content-children="#portal-mainnavigation" method="raw" />
```

Change the rule to the following:

```xml
<!-- move global nav -->
<replace css:theme-children=".navbar-nav" css:content-children="#portal-globalnav" />
```

Here we take the list of links from Plone and replace the placeholder links in the theme.
The Barceloneta rule copies the whole navigation container into the theme, but we only need to copy the links over.

### Breadcrumbs & Co

Plone provides some viewlets like the breadcrumbs (showing the current path) which are rendered in the *above the content* area.

We already have the required rule to insert the Plone above-content viewlets into the theme:

```xml
<!-- full-width breadcrumb -->
<replace css:content="#viewlet-above-content" css:theme="#above-content" />
```

All we have to do to get this into the theme layout is to add a placeholder with the CSS id `#above-content` to the theme's {file}`index.html`.

We can add this for example as a first element in the main container with the CSS class `.container`, after the main navigation:

```{code-block} html
:emphasize-lines: 8-10

<!-- Navigation -->
<nav class="navbar navbar-default" role="navigation">
  ...
</nav>

<div class="container">

  <div class="row">
    <div id="above-content" class="box"></div>
  </div>

  <div class="row">
    <div class="box">
      <div class="col-lg-12 text-center">
        ...
```

This will bring over everything from the `viewlet-above-content` block from Plone.
It also includes the breadcrumbs bar.

Because our current theme does not provide a breadcrumbs bar, we can drop it from the Plone content, like this:

```xml
<drop css:content="#portal-breadcrumbs" />
```

If you only want to drop this for non-administrators, you can do it like this:

```{code-block} xml
:emphasize-lines: 2

<drop css:content="#portal-breadcrumbs"
    css:if-not-content=".userrole-manager"
    />
```

Or for anonymous users only:

```{code-block} xml
:emphasize-lines: 2

<drop css:content="#portal-breadcrumbs"
    css:if-content=".userrole-anonymous"
    />
```

```{note}
The classes like *userrole-anonymous* are provided by Plone in the `body` tag.
```

### Slider Only On Front Page

We want the slider in the template to be only visible on the front page.
To make this easier, we add the CSS-ID `#front-page-slider` to the outer row `div`-tag which contains the slider:

```{code-block} html
:emphasize-lines: 1

<div class="row" id="front-page-slider">
  <div class="box">
    <div class="col-lg-12 text-center">
      <div id="carousel-example-generic" class="carousel slide">
        <!-- Indicators -->
        <ol class="carousel-indicators hidden-xs">
          <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
          <li data-target="#carousel-example-generic" data-slide-to="1"></li>
          <li data-target="#carousel-example-generic" data-slide-to="2"></li>
        </ol>

        <!-- Wrapper for slides -->
        <div class="carousel-inner">
          <div class="item active">
            <img class="img-responsive img-full" src="img/slide-1.jpg" alt="">
          </div>
          <div class="item">
            <img class="img-responsive img-full" src="img/slide-2.jpg" alt="">
          </div>
          <div class="item">
            <img class="img-responsive img-full" src="img/slide-3.jpg" alt="">
          </div>
        </div>

        <!-- Controls -->
        <a class="left carousel-control" href="#carousel-example-generic" data-slide="prev">
          <span class="icon-prev"></span>
        </a>
        <a class="right carousel-control" href="#carousel-example-generic" data-slide="next">
          <span class="icon-next"></span>
        </a>
      </div>
      <h2 class="brand-before">
        <small>Welcome to</small>
      </h2>
      <h1 class="brand-name">Business Casual</h1>
      <hr class="tagline-divider">
      <h2>
        <small>By
          <strong>Start Bootstrap</strong>
        </small>
      </h2>
    </div>
  </div>
</div>
```

Now we can drop it if we are not on the front page and also in some other situations:

```xml
<drop
    css:theme="#front-page-slider"
    css:if-not-content=".section-front-page"
    />
```

Currently the slider is still static, but we will change that later in {ref}`create-dynamic-slider-content-in-plone`.

### Title And Description

The front page with the slider gives us a nice structure we can use for our title and description.
We will use the `<h1>` tag with the class `brand-name` for the title and the following `<h2>` tag for the description.
There is also an `<h2>` tag with the class `brand-before` which we don't need, so we will remove it.

The resulting block of rules can be wrapped into a separate `rules` tag with the `css:if-content` condition, so we only have to write this once:

```xml
<!-- Title & Description on front page -->
<rules css:if-content=".section-front-page">
  <drop css:theme=".brand-before" />

  <replace
      css:theme-children=".brand-name"
      css:content-children=".documentFirstHeading"
      method="raw"
      />
  <drop css:content=".documentFirstHeading" />

  <replace
    css:theme="#front-page-slider h2"
    css:content=".documentDescription"
    method="raw"
    />
  <drop css:content=".documentDescription" />
</rules>
```

If we are on the front page, the Plone title will be placed inside the tag with the class `brand-name`.
For all other pages, the title and description stay at their place in the content area.

### Status Messages

Plone will render status messages in an element with the CSS-ID `#global_statusmessage`.
To show the messages in our theme, we have to add another placeholder into our theme template (e.g. next to the `above-content` viewlets):

```{code-block} html
:emphasize-lines: 2

<div class="row">
  <div id="global_statusmessage"></div>
  <div id="above-content"></div>
</div>
```

The necessary rule is already available:

```xml
<!-- Alert message -->
<replace css:theme-children="#global_statusmessage" css:content-children="#global_statusmessage" />
```

To test that the status messages are working, you can for example edit the front page and then click on cancel or save,
which will give you a confirmation message from Plone.

### Main Content Area

To make the Plone content area flexible and containing the correct Twitter Bootstrap grid classes, we use an inline {term}`XSLT` snippet.
This is already available in our {file}`rules.xml` file, but it needs some customization for our theme:

1. We need to wrap the grid columns into an element with the class `box` and `clearfix`.
2. We have to adjust the CSS class depending on the available portlets.

```{code-block} xml
:emphasize-lines: 5-13,24,28,31,35

<!-- Central column -->
<replace css:theme="#content-container" method="raw">

  <xsl:variable name="central">
    <xsl:if test="//aside[@id='portal-column-one'] and //aside[@id='portal-column-two']">
      col-xs-12 col-sm-12 col-md-6 col-md-push-3
    </xsl:if>
    <xsl:if test="//aside[@id='portal-column-two'] and not(//aside[@id='portal-column-one'])">
      col-xs-12 col-sm-12 col-md-9
    </xsl:if>
    <xsl:if test="//aside[@id='portal-column-one'] and not(//aside[@id='portal-column-two'])">
      col-xs-12 col-sm-12 col-md-9 col-md-push-3
    </xsl:if>
    <xsl:if test="not(//aside[@id='portal-column-one']) and not(//aside[@id='portal-column-two'])">
      col-xs-12 col-sm-12
    </xsl:if>
  </xsl:variable>

  <div class="{$central}">
    <!-- <p class="pull-right visible-xs">
      <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
    </p> -->
    <div class="row">
      <div class="box clearfix">
        <div class="col-xs-12 col-sm-12">
          <xsl:apply-templates css:select="#content" />
        </div>
      </div>
    </div>
    <footer class="row">
      <div class="box clearfix">
        <div class="col-xs-12 col-sm-12">
          <xsl:copy-of css:select="#viewlet-below-content" />
        </div>
      </div>
    </footer>
  </div>
</replace>
```

This code will add the correct Twitter Bootstrap grid classes to the content columns, depending on a one-, two- or three-column-layout.
We had to adjust the column classes (we added `col-md-push-3`) to push the main content (visually) after the 1st portlet column, if this one is available.

For our template we also need to wrap the content and the viewlets showing below the content in a `<div>` tag with the CSS class `box`.
This will add the shiny white transparent background.

```{hint}
We also changed the column classes to use the `col-sm-*` size for small screens to use the full width and the `col-md-*` size for mid-size screens to use a column layout.
This fits better on smaller screen sizes.
```

### Left And Right Columns

We already added the necessary placeholders `column1-container` and `column2-container` for the two portlet columns to our template.
The next set of rules will add the left and right portlet columns from Plone into the theme, and also change their markup to be an `<aside>` element instead of a normal `<div>` tag.

Because the main content column is coming before the two portlet columns, but we want to have the 1st column appear on the left side, we need to *pull* the column before the main content.
This is done with the CSS classes `col-md-pull-6` (if both portlet columns are available) and `col-md-pull-9` (if only the left column is available).

```{code-block} xml
:emphasize-lines: 4-12,23-31

<!-- Left column -->
<rules css:if-content="#portal-column-one">
  <replace css:theme="#column1-container">
    <xsl:variable name="columnone">
      <xsl:if test="//aside[@id='portal-column-two']">
        col-xs-12 col-sm-6 col-md-3 col-md-pull-6
      </xsl:if>
      <xsl:if test="//aside[@id='portal-column-one'] and not(//aside[@id='portal-column-two'])">
        col-xs-12 col-sm-12 col-md-3 col-md-pull-9
      </xsl:if>
    </xsl:variable>
    <div id="left-sidebar" class="{$columnone} sidebar-offcanvas">
      <aside id="portal-column-one">
        <xsl:copy-of css:select="#portal-column-one > *" />
      </aside>
    </div>
  </replace>
</rules>

<!-- Right column -->
<rules css:if-content="#portal-column-two">
  <replace css:theme="#column2-container">
    <xsl:variable name="columntwo">
      <xsl:if test="//aside[@id='portal-column-one']">
        col-xs-12 col-sm-6 col-md-3
      </xsl:if>
      <xsl:if test="//aside[@id='portal-column-two'] and not(//aside[@id='portal-column-one'])">
        col-xs-12 col-sm-12 col-md-3
      </xsl:if>
    </xsl:variable>
    <div id="right-sidebar" class="{$columntwo} sidebar-offcanvas" role="complementary">
      <aside id="portal-column-two">
        <xsl:copy-of css:select="#portal-column-two > *" />
      </aside>
    </div>
  </replace>
</rules>
```

Another thing we have to change are the CSS-IDs for the columns.
The ruleset we got from `bobtemplates.plone` assigned the ID `sidebar` twice, which is not valid HTML.

### Footer Area

Last but not least we have to integrate the footer area from Plone.
The rule to move all footer portlets at once is already available, the only thing we have to adjust is the selector for the theme:

```{code-block} xml
:emphasize-lines: 3

<!-- Footer -->
<replace
    css:theme-children="footer > .container"
    css:content-children="#portal-footer-wrapper"
    />
```

If we want to go advanced, we can create a doormat like footer.
Therefore, we first have to select the *footer*, *site actions* and *colophon* (which are the default portlets available in the footer) and move them into place:

```xml
<!-- Footer -->
<!-- <replace css:theme-children="footer > .container" css:content-children="#portal-footer-wrapper" /> -->
<replace css:theme-children="footer > .container">
  <xsl:if css:test="#portal-footer-signature">
    <div class="row">
      <div class="col-xs-12 text-center">
        <div><xsl:copy-of select="//section[@id='portal-footer-signature']/attribute::*" />
          <p><xsl:apply-templates select="//section[@id='portal-footer-signature']/div/node()" /></p>
        </div>
      </div>
    </div>
  </xsl:if>
  <xsl:if css:test="#portal-footer-wrapper .portletActions">
    <div class="row">
      <div class="col-xs-12 text-center">
        <div><xsl:copy-of select="//footer[@id='portal-footer-wrapper']//section[contains(@class,'portletActions')]/attribute::*" />
          <xsl:apply-templates select="//footer[@id='portal-footer-wrapper']//section[contains(@class,'portletActions')]/node()" />
        </div>
      </div>
    </div>
  </xsl:if>
  <xsl:if css:test="#portal-colophon">
    <div class="row">
      <div class="col-xs-12 text-center">
        <div><xsl:copy-of select="//section[@id='portal-colophon']/attribute::*" />
          <p><xsl:apply-templates select="//section[@id='portal-colophon']/div/node()" /></p>
        </div>
      </div>
    </div>
  </xsl:if>
</replace>
```

Next we have to select all other available footer portlets, if any, and add them before the *footer*, *site actions* and *colophon* portlets in the footer area.

We will count the amount of portlets, and based on the number we get we set the column classes.

```xml
<!-- Move all other footer portlets into footer area. -->
<before css:theme-children="footer > .container">
  <xsl:variable name="portlets" select="count(//footer[@id='portal-footer-wrapper']//div[@class='portletWrapper']/*[not(contains(@id,'portal-colophon')) and not(contains(@id,'portal-footer-signature')) and not(contains(@class,'portletActions'))])"></xsl:variable>
  <xsl:variable name="columns">
    <xsl:if test="$portlets=1">col-md-12</xsl:if>
    <xsl:if test="$portlets=2">col-md-6</xsl:if>
    <xsl:if test="$portlets=3">col-md-4</xsl:if>
    <xsl:if test="$portlets=4">col-md-3</xsl:if>
    <xsl:if test="$portlets>4">col-md-4</xsl:if>
  </xsl:variable>
  <div class="row">
    <xsl:for-each select="//footer[@id='portal-footer-wrapper']//div[@class='portletWrapper']/*[not(contains(@id,'portal-colophon')) and not(contains(@id,'portal-footer-signature')) and not(contains(@class,'portletActions'))]">
      <div class="col-xs-12 {$columns}">
        <xsl:for-each select=".">
          <xsl:choose>
            <xsl:when css:test=".portlet">
              <xsl:choose>
                <xsl:when css:test=".portletHeader:not(.titleless)">
                  <div class="headline"><h2><xsl:value-of css:select=".portletHeader" /></h2></div>
                </xsl:when>
              </xsl:choose>
              <xsl:choose>
                <xsl:when css:test=".portletCollection">
                  <ul>
                    <xsl:for-each css:select=".portletItem">
                      <li>
                        <a><xsl:copy-of select="a/attribute::*" /><xsl:copy-of select="./a/text()" /></a>
                        <small><xsl:value-of css:select=".portletItemDetails" /></small>
                      </li>
                    </xsl:for-each>
                  </ul>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:copy-of css:select=".portletContent" />
                </xsl:otherwise>
              </xsl:choose>
              <xsl:if css:test=".portletFooter">
                <p><xsl:copy-of select="./node()[@class='portletFooter']/node()" /></p>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <xsl:copy-of select="./node()" />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </div>
    </xsl:for-each>
  </div>
</before>
```

That was basically all to bring the theme together with the dynamic elements from Plone.
The next part will {doc}`cover necessary CSS customizations <theme-package-3>` for our theme.
Later we will {ref}`make the slider dynamic and let users change the pictures for the slider <create-dynamic-slider-content-in-plone>`.
