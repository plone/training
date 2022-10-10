---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Create a theme based on Barceloneta

We’re going to create a theme for Plone 6 Classic UI that is based on the default theme plonetheme.barceloneta.

This package will allow you to change and extend the look of Plone to your needs. You will develop on the filesystem. You can add your package to any code repository e.g. GitHub and re-use it on different Plone sites.

**Use Case**
- Your own theme package based on Plone Classic Theming
- You want to have control over all styles
- You want to build on existing Plone Core or Addon Templates and Markup

**What you will learn**
- How to prepare your development setup
- How to create your theme package
- What are the important parts of your theme
- How to add and compile your styles


## Creating a theme package

To create a filesystem based theme, we first create a new addon package for Plone type:

```{code-block} shell
$ plonecli create addon myaddon.name
```

Answer some questions about the package:

```
--> Author's name [Your Name]:

--> Author's email [yourname@example.com]:

--> Author's GitHub username: your_name_gitbhub

--> Package description [An add-on for Plone]:

--> Do you want me to initialize a GIT repository in your new package?

--> Plone version [6.0]:

--> Python version for virtualenv [python3]:

--> Do you want me to activate VS Code support? (y/n) [y]:

Generated file structure at ... ./myaddon.name
```

Change into your package:

```{code-block} shell
$ cd myaddon.name
```

To create a theme based on Plones default theme Barceloneta, add `theme_barceloneta` from the list of templates.

```{code-block} shell
$ plonecli add theme_barceloneta
```

You will be asked for to name your theme (This will be the name that is displayed in the theming control panel and can but does not have to be the package name):

```{code-block} shell
--> Theme name [My Theme]:

Generated file structure at ... ./myaddon.name
```

All theme related files have now been added to `./myaddon.name/src/myaddon/name/theme/`

```shell
./myaddon.name/src/myaddon/name/theme/
├── barceloneta-apple-touch-icon-114x114-precomposed.png
├── barceloneta-apple-touch-icon-144x144-precomposed.png
├── barceloneta-apple-touch-icon-57x57-precomposed.png
├── barceloneta-apple-touch-icon-72x72-precomposed.png
├── barceloneta-apple-touch-icon-precomposed.png
├── barceloneta-apple-touch-icon.png
├── barceloneta-favicon.ico
├── index.html
├── manifest.cfg
├── package.json
├── preview.png
├── rules.xml
├── styles
│   ├── theme.css
│   ├── theme.min.css
│   └── theme.scss
└── tinymce-templates
    ├── README.rst
    ├── card-group.html
    └── list.html
```

## Run your theme package

Within the base directory of your package `./myaddon.name` run `plonecli build`to get all necessary packages to run Plone.


```{code-block} shell
$ plonecli build
```

After that you can start your Plone site with:

```{code-block} shell
$ plonecli serve

[...]

Serving on http://0.0.0.0:8080
```

Open <http://localhost:8080> in a Browser and see that Plone is running.

```{image} _static/barceloneta/plone_running.png
:alt: A running Plone instance.
```

Click {guilabel}`Create Classic Plone site` and enter `admin` for `Username` and also for `Password`

```{image} _static/barceloneta/create_plone_site.png
:alt: A running Plone instance.
```

Click {guilabel}`Create Plone Site` to complete the setup of your Plone instance.

```{image} _static/barceloneta/fresh_plone.png
:alt: New Plone instance.
```

To enable your theme

1. Go to the Plone Control Panel: {menuselection}`toolbar --> admin --> Site Setup`

2. Go to the "Add-ons" control panel.

3. You will see this form:

    ```{image} _static/barceloneta/install_myaddon.png
    :alt: Add-ons control panel
    ```

4. Click {guilabel}`Install` to enable your addon package and theme

    ```{image} _static/barceloneta/myaddon_installed.png
    :alt: Plone site with installed addon
    ```

## Compiling Styles

Open a **new** terminal and change into the theme folder of your package:

```{code-block} shell
$ cd myaddon.name/src/myaddon/name/theme/
```

The `package.json` file defines dependencies for the theme and includes `scripts` to compile the `theme.scss` to `theme.css` and a production optimized `theme.min.css`.

```{code-block} json

{
  "//": "Put here only theme dependencies, devDependencies should stay outside of the theme folder in the package root.",
  "name": "my-theme",
  "version": "1.0.0",
  "license": "MIT",
  "devDependencies": {
    "autoprefixer": "^10.2.5",
    "bootstrap": "^5.1.1",
    "clean-css-cli": "^5.3.0",
    "nodemon": "^2.0.7",
    "npm-run-all": "^4.1.5",
    "postcss": "^8.2.15",
    "postcss-cli": "^8.3.1",
    "sass": "^1.32.13",
    "stylelint-config-twbs-bootstrap": "^2.2.0"
  },
  "scripts": {
    "watch": "nodemon --watch styles/ --ext scss --exec \"npm run css-main\"",
    "build": "npm-run-all css-compile-main css-prefix-main css-minify-main",
    "css-main": "npm-run-all css-compile-main css-prefix-main css-minify-main",
    "css-compile-main": "sass --load-path=node_modules --style expanded --source-map --embed-sources --no-error-css styles/theme.scss:styles/theme.css",
    "css-prefix-main": "postcss --config postcss.config.js --replace \"styles/*.css\" \"!styles/*.min.css\"",
    "css-minify-main": "cleancss -O1 --format breakWith=lf --with-rebase --source-map --source-map-inline-sources --output styles/theme.min.css styles/theme.css",
    "css-lint": "stylelint \"styles/**/*.scss\" --cache --cache-location .cache/.stylelintcache"
  },
  "dependencies": {
    "@plone/plonetheme-barceloneta-base": "^3.0.0-alpha5"
  }
}

```

Install theme dependencies

```{code-block} shell
$ npm install
```

To compile your styles and watch for changes while developing run

```{code-block} shell
$ npm run watch
```

If you visit your browser again, the green placeholder should be gone and you're ready to add your own styles.

## Working with Bootstrap variables

In this example we will be recreating `plonetheme.gruuezibuesi` you can find it https://github.com/collective/plonetheme.grueezibuesi for reference.

An awesome looking theme often is based on the colors that the site logo offers. So go ahead and add a logo as explained in {doc}`./ttw_customizations`.


```{image} _static/barceloneta/buesi1.png
:alt: Site with new logo
```


Now you have some colors that you will use throughout your theme. And to use them throughout every aspect of the theme, we're doing this using variables.

Bootstrap offers **[tons of variables](https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss)** that allow you to change every aspect of the theme without writing any extra styles yourself.

We have overall properties like shadows, gradients, rounded corners or generic variables for things like colors, sizes, fonts and variables for very detailed aspects like the inner padding of your buttons or fields.

Within the `styles` folder of your theme you find `theme.scss`. This is the base file for the compilation of your styles.

```{code-block} scss
:linenos: true

// Theme import structure is based on Bootstrap documentation
// https://getbootstrap.com/docs/5.2/customize/sass/#importing

// Barceloneta and Bootstrap import are using --load-path=node_modules

// Roboto is not included in this template and therefore we disable the setup here.
$enable-roboto-webfont: false !default;

// 1. Include functions first (so you can manipulate colors, SVGs, calc, etc)
@import "bootstrap/scss/functions";

// 2. Include any default variable overrides here

$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;


// 3. Include remainder of required Barceloneta and Bootstrap stylesheets
@import "@plone/plonetheme-barceloneta-base/scss/variables.colors.plone";
@import "@plone/plonetheme-barceloneta-base/scss/variables.properties";
@import "@plone/plonetheme-barceloneta-base/scss/variables.barceloneta";
@import "bootstrap/scss/variables";

// 4. Include any default map overrides here

// 5. Include remainder of required parts
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";
@import "@plone/plonetheme-barceloneta-base/scss/mixins/mixin.portlets.plone";
@import "@plone/plonetheme-barceloneta-base/scss/mixins/mixin.font.plone";
@import "@plone/plonetheme-barceloneta-base/scss/root_variables";

// 6. Bootstrap base parts as needed
@import "bootstrap/scss/utilities";
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/type";
@import "bootstrap/scss/images";
@import "bootstrap/scss/containers";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/helpers";

// 7. Bootstrap components
@import "bootstrap/scss/tables";
@import "bootstrap/scss/forms";
@import "bootstrap/scss/buttons";
@import "bootstrap/scss/transitions";
@import "bootstrap/scss/dropdown";
@import "bootstrap/scss/button-group";
@import "bootstrap/scss/nav";
@import "bootstrap/scss/navbar";
@import "bootstrap/scss/card";
@import "bootstrap/scss/accordion";
@import "bootstrap/scss/breadcrumb";
@import "bootstrap/scss/pagination";
@import "bootstrap/scss/badge";
@import "bootstrap/scss/alert";
@import "bootstrap/scss/progress";
@import "bootstrap/scss/list-group";
@import "bootstrap/scss/close";
@import "bootstrap/scss/toasts";
@import "bootstrap/scss/modal";
@import "bootstrap/scss/tooltip";
@import "bootstrap/scss/popover";
@import "bootstrap/scss/carousel";
@import "bootstrap/scss/spinners";
@import "bootstrap/scss/offcanvas";
@import "bootstrap/scss/placeholders";

// 8. Optionally include utilities API last to generate classes based on the Sass map in `_utilities.scss`
@import "bootstrap/scss/utilities/api";

// 9. Barceloneta base
@import "@plone/plonetheme-barceloneta-base/scss/alerts";
@import "@plone/plonetheme-barceloneta-base/scss/forms";
@import "@plone/plonetheme-barceloneta-base/scss/controlpanels";
@import "@plone/plonetheme-barceloneta-base/scss/login";
@import "@plone/plonetheme-barceloneta-base/scss/toolbar";
@import "@plone/plonetheme-barceloneta-base/scss/grid";
@import "@plone/plonetheme-barceloneta-base/scss/content_base";
@import "@plone/plonetheme-barceloneta-base/scss/content_tables";

// Barceloneta full
@import "@plone/plonetheme-barceloneta-base/scss/cards";
@import "@plone/plonetheme-barceloneta-base/scss/scaffolding";
@import "@plone/plonetheme-barceloneta-base/scss/icons";
@import "@plone/plonetheme-barceloneta-base/scss/header";
@import "@plone/plonetheme-barceloneta-base/scss/sitenav";
@import "@plone/plonetheme-barceloneta-base/scss/breadcrumbs";
@import "@plone/plonetheme-barceloneta-base/scss/content";
@import "@plone/plonetheme-barceloneta-base/scss/comments";
@import "@plone/plonetheme-barceloneta-base/scss/portlets";
@import "@plone/plonetheme-barceloneta-base/scss/footer";

@import "@plone/plonetheme-barceloneta-base/scss/print";

// @import "@plone/plonetheme-barceloneta-base/scss/roboto-webfont";


// 9. Add additional custom code here

```

To make your colors and other variables work, it is important to define them **before** `@import`.
We add some colors and map those colors to `$primary` and `$secondary` variables that Bootstap uses.


```{code-block} scss
:linenos: true

// 2. Include any default variable overrides here

$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;


```


```{image} _static/barceloneta/buesi2.png
:alt: Site with new pinkish primary and secondary color
```

One of the overall properties for the theme is `$enable-rounded`,  add it and change the `$border-radius` too.


```{code-block} scss
:linenos: true

//// VARIABLES
// ... add your variables here
$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;

$enable-rounded: true;
$border-radius: 1rem;

//// IMPORTS
// Import barceloneta files from node_modules --load-path=node_modules
@import "@plone/plonetheme-barceloneta-base/scss/barceloneta.scss";

//// STYLES
// ... add your styles here


```


```{image} _static/barceloneta/buesi3.png
:alt: Site with new pinkish primary and secondary color
```

Let's change some more variables and set `$body-bg` and `$breadcrumb-bg`



```{code-block} scss
:linenos: true

//// VARIABLES
// ... add your variables here
$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;

$enable-rounded: true;
$border-radius: 1rem;

$body-bg: $lightest-pink;
$breadcrumb-bg: $lighter-pink;

//// IMPORTS
// Import barceloneta files from node_modules --load-path=node_modules
@import "@plone/plonetheme-barceloneta-base/scss/barceloneta.scss";

//// STYLES
// ... add your styles here


```

## Modifying the theme html

Not everything has to be done in `css`. Sometimes it's easier to change the underlying `index.html`.
Let's add `class="container"` from [Bootstraps Grid System](https://getbootstrap.com/docs/5.1/layout/grid/) to `id="mainnavigation-wrapper"` and `id="above-content-wrapper"`. This will align the width of the main navigation and breadcrumbs to the width of our content.

Just be careful to keep ids used in `rules.xml` that Diazo can still replace areas in the static html with actual contents.

```{code-block} scss
:linenos: true
:lineno-start: 32
:emphasize-lines: 1, 11

  <div id="mainnavigation-wrapper" class="container">
    <div id="mainnavigation">
    </div>
  </div>
  <div id="hero" class="principal">
    <div class="container">
      <div class="gigantic">
      </div>
    </div>
  </div>
  <div id="above-content-wrapper" class="container">
      <div id="above-content">
      </div>
  </div>

```


```{image} _static/barceloneta/buesi4.png
:alt: Site with main navigation and breadcrumbs aligned with content
```


## Fonts

Fonts are an important visual factor in a theme. To use web fonts we can either `link` them in the html or `@import` them within the css.

**link**
```{code-block} html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Itim&family=Vibur&display=swap" rel="stylesheet">
```

**@import**
```{code-block} scss
@import url('https://fonts.googleapis.com/css2?family=Itim&family=Vibur&display=swap');
```

<em>If you want to see the fonts within TinyMCE as well, you should go with `@import`. To optimize loading and reduce unwanted effects like web font flashing or flickering it's a good idea to add the `rel="preconnect"` tags even if you import the fonts in your css.</em>

Let's add those fonts to our css and change the variables to use them.

```{code-block} scss
:linenos: true

//// VARIABLES
// ... add your variables here
$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;

$enable-rounded:              true;
$border-radius:               1rem;

$body-bg: $lightest-pink;
$breadcrumb-bg: $lighter-pink;


// Fonts
@import url('https://fonts.googleapis.com/css2?family=Itim&family=Vibur&display=swap');
// Fonts - use Import if you want the fonts displayed in TinyMCE as well
$font-family-sans-serif: Itim, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
$headings-font-family: Vibur;


//// IMPORTS
// Import barceloneta files from node_modules --load-path=node_modules
@import "@plone/plonetheme-barceloneta-base/scss/barceloneta.scss";


//// STYLES
// ... add your styles here


```


```{image} _static/barceloneta/buesi5.png
:alt: Site with web fonts
```

In addition, let's adjust the color and size


```{code-block} scss
:linenos: true

//// VARIABLES
// ... add your variables here
$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;

$enable-rounded:              true;
$border-radius:               1rem;

$body-bg: $lightest-pink;
$breadcrumb-bg: $lighter-pink;

// Fonts
@import url('https://fonts.googleapis.com/css2?family=Itim&family=Vibur&display=swap');
// Fonts - use Import if you want the fonts displayed in TinyMCE as well
$font-family-sans-serif: Itim, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
$headings-font-family: Vibur;

// Font colors
$headings-color: $primary;
$body-color: $medium-grey;

// Font sizes
$font-size-base:              1rem;
$h1-font-size:                $font-size-base * 3;
$h2-font-size:                $font-size-base * 2.5;


//// IMPORTS
// Import barceloneta files from node_modules --load-path=node_modules
@import "@plone/plonetheme-barceloneta-base/scss/barceloneta.scss";


//// STYLES
// ... add your styles here

```

```{image} _static/barceloneta/buesi6.png
:alt: Site with web fonts
```

## Styles

Although we managed to change quite a lot with based on variabless, we still need to write some css to make our theme really pretty. We'll fix the corners of the search, make the main navigation rounded and change the alignment of items within the portal-header.

For these styles it's a good idea to use variables from Bootstrap again to make the consistency of your styles easier. We'll include those styles after the import of Barbeloneta/Bootstrap styles and are able to make use of Bootstraps own mixins and utilities too.

```{code-block} scss
:linenos: true

//// VARIABLES
// ... add your variables here
$pink: #EE4793;
$light-pink: #F3A4CB;
$lighter-pink: #f7d4e5;
$lightest-pink: #fff2f8;
$medium-grey: #555;

$primary: $pink;
$secondary: $light-pink;

$enable-rounded:              true;
$border-radius:               1rem;

$body-bg: $lightest-pink;
$breadcrumb-bg: $lighter-pink;

// Fonts
@import url('https://fonts.googleapis.com/css2?family=Itim&family=Vibur&display=swap');
// Fonts - use Import if you want the fonts displayed in TinyMCE as well
$font-family-sans-serif: Itim, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
$headings-font-family: Vibur;

// Font colors
$headings-color: $primary;
$body-color: $medium-grey;

// Font sizes
$font-size-base:              1rem;
$h1-font-size:                $font-size-base * 3;
$h2-font-size:                $font-size-base * 2.5;


//// IMPORTS
// Import barceloneta files from node_modules --load-path=node_modules
@import "@plone/plonetheme-barceloneta-base/scss/barceloneta.scss";


//// STYLES
// ... add your styles here

// Search Button
.searchButton.btn.btn-secondary {
    border-radius: 0 $border-radius $border-radius 0;
}

// Navbar & Breadcrumbs
.navbar {
    border-radius: $border-radius $border-radius 0 0;
}

#portal-breadcrumbs {
    @include border-bottom-radius($border-radius);
}
#portal-header {
    align-items: end;
}

```



```{image} _static/barceloneta/buesi7.png
:alt: Site with additional styles
```

## CSS variables

Bootstrap 5 added support for [CSS custom properties (variables)](https://getbootstrap.com/docs/5.1/customize/css-variables/). If you want to change any of the `:root` variables of Bootstrap directly, best thing is to add them at the bottom of your style sheet, since browsers interpret them native, like any other CSS.


```{code-block} scss
:linenos: true

:root {
--foo: red;
}
```

You can also change colors of specific components like this:


```{code-block} scss
:linenos: true

.navbar-barceloneta{
    --bs-navbar-background: green;
}
```

This works event in Theming > "Custom Styles", as it is plain CSS.
