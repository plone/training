---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Create a theme based on Diazo

We're goiging to create a theme package for Plone 6 Classic UI, that is based on the Business Casual theme from [startbootstrap.com](https://startbootstrap.com/previews/business-casual).

Integrating a custom layout (static mockup) with Plone classic UI,

**Use Case**
- You have an existing static layout comming from a website or a designer.
- You want to integrate this layout without changing too much.
- You want to use the Plone default layout for all edit-/backend-view's.

**What you will learn**
- How to prepare your development setup
- How to create your theme package with `plonecli`
- How to create the content structure for your theme
- How to integrate your static layout into the theme
- How to add and compile your styles
- How to create HTML snippets as TinyMCE templates
- How to create content type's and views

## Creating a theme package

To create a filesystem based theme, we first create a new addon package for Plone:

```{code-block} shell
$ plonecli create addon plonetheme.businesscasual21
```

Answer some questions about the package:

```
--> Author's name [Your Name]:

--> Author's email [yourname@example.com]:

--> Author's GitHub username: your_github_name_

--> Package description [An add-on for Plone]:

--> Do you want me to initialize a GIT repository in your new package?

--> Plone version [6.0]:

--> Python version for virtualenv [python3]:

--> Do you want me to activate VS Code support? (y/n) [y]:

Generated file structure at ... ./plonetheme.businesscasual21
```

Change into the generated package folder:

```{code-block} shell
$ cd plonetheme.businesscasual21
```

now we want to add a theme, to the addon:

```{code-block} shell
$ plonecli add theme
```

## Integrate the static layout

Download the Bootstrap theme [Business Casual](https://startbootstrap.com/previews/business-casual) and extract the content into the theme folder under `src/plonetheme/businesscasual21/theme/`.
Your folder structure should now look like this:

```{code-block} shell
├── about.html
├── assets
│   ├── favicon.ico
│   └── img
│       ├── about.jpg
│       ├── bg.jpg
│       ├── intro.jpg
│       ├── products-01.jpg
│       ├── products-02.jpg
│       └── products-03.jpg
├── css
│   └── styles.css
├── index.html
├── js
│   └── scripts.js
├── manifest.cfg
├── package.json
├── products.html
├── README.rst
├── rules.xml
├── store.html
└── tinymce-templates
    ├── bs-dark-hero.html
    ├── bs-hero-left.html
    └── bs-pricing.html
```

## Showtime, build your setup and test your theme

Run `plonecli build` to get build a development setup with Plone.


```{code-block} shell
$ plonecli build
```

After that you can start your Plone site with:

```{code-block}
$ plonecli serve

[...]

Serving on http://0.0.0.0:8080
```

Open <http://localhost:8080> in a Browser and see that Plone is running.

```{image} _static/barceloneta/plone_running.png
:alt: A running Plone instance.
```

Click {guilabel}`Create a new Plone site` and enter `admin` for `Username` and also for `Password`

```{image} _static/barceloneta/create_plone_site.png
:alt: A running Plone instance.
```

Click {guilabel}`Create Plone Site` to complete the setup of your Plone instance.

```{image} _static/barceloneta/fresh_plone.png
:alt: New Plone instance.
```


To enable your theme:

1. Go to the Plone Control Panel: {menuselection} `toolbar --> admin --> Site Setup`

2. Go to the "Add-ons" control panel.

3. You will see this form:

```{image} _static/diazo/activate_theme_addon.png
:alt: Add-ons control panel
```

4. Click {guilabel}`Install` to enable your addon package. To see the theme layout, go to the start page.

```{image} _static/diazo/first-start-after-copying-static-layout.png
:alt: Plone site with installed addon
```

Since the theme for now is rather static, we will deactivate it for now. For that go to the Plone Control Panel: {menuselection} `toolbar --> admin --> Site Setup` and then to `Theming` and click on activate on the Barceloneta theme. We now have again the default theme active.

## Creating content for our theme to shine

On the root level, we add the following folders:

- About
- Products
- Store

In the folders `About` and `Store` we add a Page and make it the default page.

For the folder Products we are going to use a Collection instead and making it the default page. The criteria for the Collection we will define later.

Let's cleanup some of the default content. In the toolbar click on `Contents`, mark news, events and users folders and press the delete button.

```{image} _static/diazo/folder-contents-delete-news-events.png
:alt: Delete news and events folder in folder contents view
```

## Adding HTML snippets as TinyMCE templates

Since our layout requires a specific content layout, which would be hard to create manually, we will create these HTML structures as TinyMCE templates.
To do so, we copy the desired HTML snippets from the layout and add them to the tinymce-templates folder in our theme.

Let's start with the About section. With the inspector from of the Browser we simple copy the HTML and insert it in the section-about.HTML file. We also wrap it in the `<div class="mceTmpl">` tag.

section-about.html:

```html
<div class="mceTmpl">
  <section class="page-section about-heading">
    <div class="container">
      <img class="img-fluid rounded about-heading-img mb-3 mb-lg-0" src="assets/img/about.jpg" alt="...">
      <div class="about-heading-content">
        <div class="row">
          <div class="col-xl-9 col-lg-10 mx-auto">
            <div class="bg-faded rounded p-5">
              <h2 class="section-heading mb-4">
                <span class="section-heading-upper">Strong Coffee, Strong Roots</span>
                <span class="section-heading-lower">About Our Cafe</span>
              </h2>
              <p>Founded in 1987 by the Hernandez brothers, our establishment has been serving up rich coffee sourced from
                artisan farmers in various regions of South and Central America. We are dedicated to travelling the world,
                finding the best coffee, and bringing back to you here in our cafe.</p>
              <p class="mb-0">
                We guarantee that you will fall in
                <em>lust</em>
                with our decadent blends the moment you walk inside until you finish your last sip. Join us for your daily
                routine, an outing with friends, or simply just to enjoy some alone time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
```

section-intro.html:

```html
<div class="mceTmpl">
  <section class="page-section clearfix">
    <div class="container">
      <div class="intro">
        <img class="intro-img img-fluid mb-3 mb-lg-0 rounded" src="assets/img/intro.jpg" alt="...">
        <div class="intro-text left-0 text-center bg-faded p-5 rounded">
          <h2 class="section-heading mb-4">
            <span class="section-heading-upper">Fresh Coffee</span>
            <span class="section-heading-lower">Worth Drinking</span>
          </h2>
          <p class="mb-3">Every cup of our quality artisan coffee starts with locally sourced, hand picked ingredients.
            Once you try it, our coffee will be a blissful addition to your everyday morning routine - we guarantee it!
          </p>
          <div class="intro-button mx-auto"><a class="btn btn-primary btn-xl" href="#!">Visit Us Today!</a></div>
        </div>
      </div>
    </div>
  </section>
</div>
```

section-promise.html:

```html
<div class="mceTmpl">
  <section class="page-section cta">
    <div class="container">
      <div class="row">
        <div class="col-xl-9 mx-auto">
          <div class="cta-inner bg-faded text-center rounded">
            <h2 class="section-heading mb-4">
              <span class="section-heading-upper">Our Promise</span>
              <span class="section-heading-lower">To You</span>
            </h2>
            <p class="mb-0">When you walk into our shop to start your day, we are dedicated to providing you with
              friendly service, a welcoming atmosphere, and above all else, excellent products made with the highest
              quality ingredients. If you are not satisfied, please let us know and we will do whatever we can to make
              things right!</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
```

section-opening-hours.html:

```html
<div class="mceTmpl">
  <section class="page-section cta">
    <div class="container">
      <div class="row">
        <div class="col-xl-9 mx-auto">
          <div class="cta-inner bg-faded text-center rounded">
            <h2 class="section-heading mb-5">
              <span class="section-heading-upper">Come On In</span>
              <span class="section-heading-lower">We're Open</span>
            </h2>
            <ul class="list-unstyled list-hours mb-5 text-left mx-auto">
              <li class="list-unstyled-item list-hours-item d-flex">
                Sunday
                <span class="ms-auto">Closed</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex">
                Monday
                <span class="ms-auto">7:00 AM to 8:00 PM</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex">
                Tuesday
                <span class="ms-auto">7:00 AM to 8:00 PM</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex">
                Wednesday
                <span class="ms-auto">7:00 AM to 8:00 PM</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex today">
                Thursday
                <span class="ms-auto">7:00 AM to 8:00 PM</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex">
                Friday
                <span class="ms-auto">7:00 AM to 8:00 PM</span>
              </li>
              <li class="list-unstyled-item list-hours-item d-flex">
                Saturday
                <span class="ms-auto">9:00 AM to 5:00 PM</span>
              </li>
            </ul>
            <p class="address mb-5">
              <em>
                <strong>1116 Orchard Street</strong>
                <br>
                Golden Valley, Minnesota
              </em>
            </p>
            <p class="mb-0">
              <small><em>Call Anytime</em></small>
              <br>
              (317) 585-8468
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
```

when you are done with it, the tinymce-templates folder should look like this:

```shell
tinymce-templates/
├── bs-dark-hero.html
├── bs-hero-left.html
├── bs-pricing.html
├── section-about.html
├── section-intro.html
├── section-opening-hours.html
└── section-promise.html
```

Now we need to register the templates for the TinyMCE editor. You could do this manually in the TinyMCE control panel, but we will do the registration with the package in `profiles/default/registry/tinymce.xml`.

Right now it should look like this:

```xml
<?xml version="1.0"?>
<registry>

  <record name="plone.templates" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="templates">
    <field type="plone.registry.field.Text">
      <default></default>
      <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="help_tinymce_templates">Enter the list of templates in json format http://www.tinymce.com/wiki.php/Plugin:template</description>
      <required>False</required>
      <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="label_tinymce_templates">Templates</title>
    </field>
    <value>[
      {"title": "BS Pricing", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-pricing.html"},
      {"title": "BS Hero: Dark", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-dark-hero.html"},
      {"title": "BS Hero: left-aligned with image", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-hero-left.html"}
      ]
    </value>
  </record>

  <record name="plone.custom_plugins" interface="Products.CMFPlone.interfaces.controlpanel.ITinyMCESchema" field="custom_plugins">
    <field type="plone.registry.field.List">
      <default/>
      <description xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="">Enter a list of custom plugins which will be loaded in the editor. Format is pluginname|location, one per line.</description>
      <required>False</required>
      <title xmlns:ns0="http://xml.zope.org/namespaces/i18n" ns0:domain="plone" ns0:translate="">Custom plugins</title>
      <value_type type="plone.registry.field.TextLine"/>
    </field>
    <value>
      <element>template|++plone++static/components/tinymce-builded/js/tinymce/plugins/template</element>
    </value>
  </record>

 <!-- <records interface="Products.CMFPlone.interfaces.controlpanel.IFilterSchema" prefix="plone">
    <value key="custom_attributes" purge="false">
      <element></element>
    </value>
  </records> -->

  <records interface="Products.CMFPlone.interfaces.controlpanel.IFilterSchema" prefix="plone">
    <value key="valid_tags" purge="false">
      <element>button</element>
    </value>
  </records>

</registry>
```

In the first record, we add our new template files as follow:

```xml
    <value>[
      {"title": "BS Pricing", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-pricing.html"},
      {"title": "BS Hero: Dark", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-dark-hero.html"},
      {"title": "BS Hero: left-aligned with image", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/bs-hero-left.html"},
      {"title": "Section: Intro", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/section-intro.html"},
      {"title": "Section: About", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/section-about.html"},
      {"title": "Section: Promise", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/section-promise.html"},
      {"title": "Section: Opening Hours", "url": "++theme++{{{ theme.normalized_name }}}/tinymce-templates/section-opening-hours.html"}
      ]
    </value>
```

That's all, after uninstalling/installing the addon we will have the new templates in the TinyMCE.

## Inspect and optimize our layout file

The `index.html` file of the Bootstrap theme we got, looks as follow:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Business Casual - Start Bootstrap Theme</title>
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Raleway:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css?family=Lora:400,400i,700,700i" rel="stylesheet" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
    </head>
    <body>
        <header>
            <h1 class="site-heading text-center text-faded d-none d-lg-block">
                <span class="site-heading-upper text-primary mb-3">A Free Bootstrap Business Theme</span>
                <span class="site-heading-lower">Business Casual</span>
            </h1>
        </header>
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-dark py-lg-4" id="mainNav">
            <div class="container">
                <a class="navbar-brand text-uppercase fw-bold d-lg-none" href="index.html">Start Bootstrap</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mx-auto">
                        <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="index.html">Home</a></li>
                        <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="about.html">About</a></li>
                        <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="products.html">Products</a></li>
                        <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="store.html">Store</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <section class="page-section clearfix">
            <div class="container">
                <div class="intro">
                    <img class="intro-img img-fluid mb-3 mb-lg-0 rounded" src="assets/img/intro.jpg" alt="..." />
                    <div class="intro-text left-0 text-center bg-faded p-5 rounded">
                        <h2 class="section-heading mb-4">
                            <span class="section-heading-upper">Fresh Coffee</span>
                            <span class="section-heading-lower">Worth Drinking</span>
                        </h2>
                        <p class="mb-3">Every cup of our quality artisan coffee starts with locally sourced, hand picked ingredients. Once you try it, our coffee will be a blissful addition to your everyday morning routine - we guarantee it!</p>
                        <div class="intro-button mx-auto"><a class="btn btn-primary btn-xl" href="#!">Visit Us Today!</a></div>
                    </div>
                </div>
            </div>
        </section>
        <section class="page-section cta">
            <div class="container">
                <div class="row">
                    <div class="col-xl-9 mx-auto">
                        <div class="cta-inner bg-faded text-center rounded">
                            <h2 class="section-heading mb-4">
                                <span class="section-heading-upper">Our Promise</span>
                                <span class="section-heading-lower">To You</span>
                            </h2>
                            <p class="mb-0">When you walk into our shop to start your day, we are dedicated to providing you with friendly service, a welcoming atmosphere, and above all else, excellent products made with the highest quality ingredients. If you are not satisfied, please let us know and we will do whatever we can to make things right!</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <footer class="footer text-faded text-center py-5">
            <div class="container"><p class="m-0 small">Copyright &copy; Your Website 2021</p></div>
        </footer>
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
    </body>
</html>
```

Let's focus on the styles in the header for now. You will find here a line like this:

```html
<link href="css/styles.css" rel="stylesheet" />
```

Since we will include the css later via our manifest file, we will delete this line here.

Now to the JavaScript in the footer of the body.

```html
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
```

the first line which includes the Bootstrap JavaScript, we will delete, since Plone come with it by default. The second line we will keep.

Now let's make two more little changes to the markup.

Let's add a tag where we will show portal messages from Plone later. Add this right under the `<nav>` tag.

```html
<div id="global_statusmessage" class="container"></div>
```

The second change is, to wrap the sections in a `<main></main>` tag.

Now the file should look like this:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <meta name="description" content="" />
  <meta name="author" content="" />
  <title>Business Casual - Start Bootstrap Theme</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
  <!-- Font Awesome icons (free version)-->
  <script src="https://use.fontawesome.com/releases/v5.15.4/js/all.js" crossorigin="anonymous"></script>
  <!-- Google fonts-->
  <link
    href="https://fonts.googleapis.com/css?family=Raleway:100,100i,200,200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i"
    rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css?family=Lora:400,400i,700,700i" rel="stylesheet" />
</head>

<body>
  <header>
    <h1 class="site-heading text-center text-faded d-none d-lg-block">
      <span class="site-heading-upper text-primary mb-3">A Free Bootstrap Business Theme</span>
      <span class="site-heading-lower">Business Casual</span>
    </h1>
  </header>
  <!-- Navigation-->
  <nav class="navbar navbar-expand-lg navbar-dark py-lg-4" id="mainNav">
    <div class="container">
      <a class="navbar-brand text-uppercase fw-bold d-lg-none" href="index.html">Start Bootstrap</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span
          class="navbar-toggler-icon"></span></button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="index.html">Home</a></li>
          <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="about.html">About</a></li>
          <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="products.html">Products</a></li>
          <li class="nav-item px-lg-4"><a class="nav-link text-uppercase" href="store.html">Store</a></li>
        </ul>
      </div>
    </div>
  </nav>
  <div id="global_statusmessage" class="container"></div>
  <main>
    <section class="page-section clearfix">
      <div class="container">
        <div class="intro">
          <img class="intro-img img-fluid mb-3 mb-lg-0 rounded" src="assets/img/intro.jpg" alt="..." />
          <div class="intro-text left-0 text-center bg-faded p-5 rounded">
            <h2 class="section-heading mb-4">
              <span class="section-heading-upper">Fresh Coffee</span>
              <span class="section-heading-lower">Worth Drinking</span>
            </h2>
            <p class="mb-3">Every cup of our quality artisan coffee starts with locally sourced, hand picked
              ingredients. Once you try it, our coffee will be a blissful addition to your everyday morning routine - we
              guarantee it!</p>
            <div class="intro-button mx-auto"><a class="btn btn-primary btn-xl" href="#!">Visit Us Today!</a></div>
          </div>
        </div>
      </div>
    </section>
    <section class="page-section cta">
      <div class="container">
        <div class="row">
          <div class="col-xl-9 mx-auto">
            <div class="cta-inner bg-faded text-center rounded">
              <h2 class="section-heading mb-4">
                <span class="section-heading-upper">Our Promise</span>
                <span class="section-heading-lower">To You</span>
              </h2>
              <p class="mb-0">When you walk into our shop to start your day, we are dedicated to providing you with
                friendly service, a welcoming atmosphere, and above all else, excellent products made with the highest
                quality ingredients. If you are not satisfied, please let us know and we will do whatever we can to make
                things right!</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer text-faded text-center py-5">
    <div class="container">
      <p class="m-0 small">Copyright &copy; Your Website 2021</p>
    </div>
  </footer>
  <!-- Core theme JS-->
  <script src="js/scripts.js"></script>
</body>

</html>
```

To include the CSS, we will create a SCSS file `theme.scss` in the `css` folder and import the `styles.css` provided by the Bootstrap theme in there.

```scss
@import "styles";
```

## Adjust and use the `package.json`

The theme provides some useful scripts to compile and optimize SCSS into CSS. These commands are defined in the script area of the `package.json`.

```json
  "scripts": {
    "dev": "npm-run-all --parallel reload-browser watch",
    "watch": "nodemon --watch css/ --ext scss --exec \"npm run css-main\"",
    "build": "npm-run-all fetch-vendor-files css-compile-main css-prefix-main css-minify-main",
    "css-main": "npm-run-all css-compile-main css-prefix-main css-minify-main",
    "css-compile-main": "sass --load-path=node_modules --style expanded --source-map --embed-sources --no-error-css styles/theme.scss:styles/theme.css",
    "css-prefix-main": "postcss --config postcss.config.js --replace \"styles/*.css\" \"!styles/*.min.css\"",
    "css-minify-main": "cleancss -O1 --format breakWith=lf --with-rebase --source-map --source-map-inline-sources --output styles/theme.min.css styles/theme.css",
    "css-lint": "stylelint \"styles/**/*.scss\" --cache --cache-location .cache/.stylelintcache",
    "fetch-vendor-files": "./node_modules/.bin/copy-node-modules ./ ./vendor --verbose",
    "reload-browser": "reload -b --exts html,js,css"
  },
```

Here we can see, that the scripts are searching for SCSS files inside a folder called styles. Our theme has a slightly different structure. One way to fix this, that we adjust the script definitions here to our needs.
Let's change the path from `styles/` to `css/`.

the script area should now look like this:

```json
  "scripts": {
    "dev": "npm-run-all --parallel reload-browser watch",
    "watch": "nodemon --watch css/ --ext scss --exec \"npm run css-main\"",
    "build": "npm-run-all fetch-vendor-files css-compile-main css-prefix-main css-minify-main",
    "css-main": "npm-run-all css-compile-main css-prefix-main css-minify-main",
    "css-compile-main": "sass --load-path=node_modules --style expanded --source-map --embed-sources --no-error-css css/theme.scss:css/theme.css",
    "css-prefix-main": "postcss --config postcss.config.js --replace \"css/*.css\" \"!css/*.min.css\"",
    "css-minify-main": "cleancss -O1 --format breakWith=lf --with-rebase --source-map --source-map-inline-sources --output css/theme.min.css css/theme.css",
    "css-lint": "stylelint \"css/**/*.scss\" --cache --cache-location .cache/.stylelintcache",
    "fetch-vendor-files": "./node_modules/.bin/copy-node-modules ./ ./vendor --verbose",
    "reload-browser": "reload -b --exts html,js,css"
  },
```

now that we fixed the `package.json`, let's use it and run the following commands.

Let's


```shell
npm install
```

We now have a new folder called `node_modules` in our theme folder, where all build tools and CSS/JavaScript resources are installed.

The following command will build our resource files to a bundle.

```shell
npm run build
```

You will now find new folder `vendor`:

```shell
vendor/
└── node_modules
```

Inside the `vendor/node_modules` you will find all dependencies declared in the `package.json`.

For example if you install a JQuery library you will find all JavaScript and CSS files in that place and can include them from there. The main `node_modules` in the `theme` folder contains much more, because there we also have all the `devDependencies` needed to build the bundles an so on. But we don't want them shipped with our theme, that why we separate what we need into the `vendor` folder.


## Adjust the layout and manifest files

We need to adjust a bit the `manifest.ini`, to reflect the layout structure of the Bootstrap theme we got.

By default the `manifest.ini` will look like this:

```ini
[theme]
title = Plone Theme: Business casual (2021)
description = A Diazo based Plone theme
doctype = <!DOCTYPE html>
rules = /++theme++business-casual-2021/rules.xml
prefix = /++theme++business-casual-2021

production-css = ++theme++business-casual-2021/styles/theme.min.css
tinymce-content-css = ++theme++business-casual-2021/styles/theme.min.css

# production-js = ++theme++business-casual-2021/js/theme.min.js

[theme:parameters]
# portal_url = python: portal.absolute_url()
```

Since our styles are located inside the `css` folder and not in `styles`, we will change the paths:

```ini
production-css = ++theme++business-casual-2021/css/theme.min.css
tinymce-content-css = ++theme++business-casual-2021/css/theme.min.css
```


