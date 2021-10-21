---
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

All theme related files have now been added to `./myaddon.name/src/myddon/name/theme/`

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

    ```{figure} _static/barceloneta/plone_running.png
    :alt: A running Plone instance.
    :scale: 50 %
    ```

Click {guilabel}`Create a new Plone site` and enter `admin` for `Username` and also for `Password`

    ```{figure} _static/barceloneta/create_plone_site.png
    :alt: A running Plone instance.
    :scale: 50 %
    ````

Click {guilabel}`Create Plone Site` to complete the setup of your Plone instance.

    ```{figure} _static/barceloneta/fresh_plone.png
    :alt: New Plone instance.
    :scale: 50 %
    ````

To enable your theme

1. Go to the Plone Control Panel: {menuselection}`toolbar --> admin --> Site Setup`

2. Go to the "Add-ons" control panel.

3. You will see this form:

    ```{figure} _static/barceloneta/install_myaddon.png
    :alt: Add-ons control panel
    :scale: 50 %
    ````

4. Click {guilabel}`Install` to enable your addon package and theme

    ```{figure} _static/barceloneta/myaddon_installed.png
    :alt: Plone site with installed addon
    :scale: 50 %
    ````

## Compiling Styles

Open a **new** terminal and change into the theme folder your package:

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


## Adding styles and compile
- Package.json explain dependencies and scripts
- npm run watch
- As a start add your logo through control panel
- Now you have some colors that you will use throughout your theme
- Explain Styles/Variables/..
- Bootstrap has a lot of variables to change almost everything that defines your theme - look at https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss
- To make variables work they have to be defined before barceloneta/bootstap is imported
- Color variables
- Map variables for primary secondary…
- Properties “rounded”
- Add more rounding 1rem

## Fonts
Add fonts (link vs import)
Show index.html (preconnect)
Set font-family
Set font-sizes
Styles
Fix Search Button Styling
Navbar / Breadcrumbs
Add container to index.html
Add more styles
Custom CSS


