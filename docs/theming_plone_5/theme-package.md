---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Theme Package I: Preparations

Creating a theme product with the Diazo inline editor is an easy way to start and to test,
but it is not a solid long term solution and you are also limited in what you can do that way.

Even if {py:mod}`plone.app.theming` allows importing and exporting of a Diazo theme as a ZIP archive,
it might be preferable to manage your theme as an actual Plone product.

One of the most obvious reasons is that it will allow you to override Plone elements that are not accessible via pure Diazo features
(such as overloading content view templates, viewlets, configuration settings, etc.).

## Preparing Your Setup

### Install npm

If you don't have {term}`npm` already installed on your system please do it.
{program}`npm` comes with {program}`nodejs`, we just need to install {program}`npm`.

On Debian/Ubuntu for example you can do this with apt:

```console
sudo apt install -y npm
```

On a Mac you can install {program}`npm` using {program}`Homebrew`:

```console
brew install node
```

If you need a newer version of {program}`npm` just update your version with {command}`npm` itself:

```console
npm install npm@latest -g
```

### Install Grunt

We also need to install {program}`grunt-cli` globally.

If you already have it, you can skip this step.

```console
npm install -g grunt-cli
```

````{dropdown}
:animate: fade-in-slide-down
:icon: question

If you get an error with {program}`node` on Debian/Ubuntu, please check if you already have `/usr/bin/node`,
if not create a symlink like:

```console
ln -s /usr/bin/nodejs /usr/bin/node
```
````

### Setup A Python Virtual Environment

First, let's create a Python {program}`virtualenv`:

```console
virtualenv mrbobvenv
```

Then we enable the virtualenv:

```console
source mrbobvenv/bin/activate
(mrbobvenv):$
```

## Create A Product To Handle Your Diazo Theme

To create a Plone 5 theme skeleton, you will use {program}`mr.bob`'s templates for Plone.

### Install mr.bob And bobtemplates.plone

To install {py:mod}`mr.bob`, you can use {command}`pip`:

```console
(mrbobvenv): pip install mr.bob
```

and to install the required bobtemplates for Plone, do:

```console
(mrbobvenv): pip install bobtemplates.plone==2.0
```

Create a Plone 5 theme product skeleton with {command}`mrbob`.
It will ask you some questions about the new theme package:

```console
(mrbobvenv): mrbob -O ploneconf.theme bobtemplates:plone_theme_package

Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

Answer with a question mark to display help.
Values in square brackets at the end of the questions show the default value if there is no answer.


--> Theme name [Theme]: Ploneconf Theme

--> Author name [Your Name]:

--> Author email [your.email@example.com]:

--> Author github username:

--> Package description [An add-on for Plone]: Plone Conference Training Theme

--> Plone version [5.0.8]:
```

Now you have a new Python package in your current folder:

```console
(mrbobvenv): ls ploneconf.theme
CHANGES.rst            LICENSE.GPL            bootstrap-buildout.py  package.json           src
CONTRIBUTORS.rst       LICENSE.rst            bootstrap-buildout.pyc requirements.txt
Gruntfile.js           MANIFEST.in            buildout.cfg           setup.cfg
HOWTO_DEVELOP.rst      README.rst             docs                   setup.py
```

It is now safe to deactivate the `mrbob` virtualenv:

```console
(mrbobvenv): deactivate
```

````{dropdown}
:animate: fade-in-slide-down
:icon: question

This would be the perfect time to initialize your package with Git and put your files under version control:

```console
cd ploneconf.theme
git init .
git add .
git commit -m "Initial commit."
cd ..
```
````

### Install zc.buildout And Bootstrap Your Development Environment

You can install Buildout globally or on a virtualenv.

We will install `zc.buildout` in a new virtual environment using the provided {file}`requirements.txt`.

```console
virtualenv buildoutvenv
source buildoutvenv/bin/activate
(buildoutvenv):$ cd ploneconf.theme
(buildoutvenv):$ pip install -r requirements.txt
(buildoutvenv):$ buildout bootstrap
```

Now you have everything in place and you can run {command}`buildout`.

Depending on your internet connection and your local buildout cache this can take several minutes to complete.

```console
(buildoutvenv): ./bin/buildout
```

After buildout finished successfully it is now safe to deactivate the `buildoutvenv` virtualenv:

```console
(buildoutvenv): deactivate
```

This will create the whole development environment for your package:

```console
ls bin
addchangelogentry               code-analysis-zptlint           lasttagdiff                     prerelease
buildout                        coverage                        lasttaglog                      pybabel
bumpversion                     createcoverage                  libdoc                          pybot
check-manifest                  createfontdatachunk.py          longtest                        release
code-analysis                   develop                         painter.py                      ride
code-analysis-check-manifest    enhancer.py                     pilconvert.py                   robot
code-analysis-clean-lines       explode.py                      pildriver.py                    robot-debug
code-analysis-csslint           flake8                          pilfile.py                      robot-server
code-analysis-find-untranslated fullrelease                     pilfont.py                      test
code-analysis-flake8            gifmaker.py                     pilprint.py                     thresholder.py
code-analysis-jscs              i18ndude                        player.py                       viewer.py
code-analysis-jshint            instance                        postrelease
```

### Inspect Your Package Source

Your package source code is in the `src` folder:

```console
tree src/ploneconf/theme/
src/ploneconf/theme
├── __init__.py
├── browser
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── configure.zcml
│   ├── overrides
│   └── static
├── configure.zcml
├── interfaces.py
├── locales
│   ├── ploneconf.theme.pot
│   └── update.sh
├── profiles
│   ├── default
│   │   ├── browserlayer.xml
│   │   ├── metadata.xml
│   │   ├── registry.xml
│   │   └── theme.xml
│   └── uninstall
│       ├── browserlayer.xml
│       └── theme.xml
├── setuphandlers.py
├── testing.py
├── tests
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── robot
│   │   └── test_example.robot
│   ├── test_robot.py
│   └── test_setup.py
└── theme
    ├── HOWTO_DEVELOP.rst
    ├── backend.xml
    ├── barceloneta
    │   └── less
    │       ├── accessibility.plone.less
    │       ├── alerts.plone.less
    │       ├── barceloneta-compiled.css
    │       ├── barceloneta-compiled.css.map
    │       ├── barceloneta.css
    │       ├── barceloneta.plone.export.less
    │       ├── barceloneta.plone.less
    │       ├── barceloneta.plone.local.less
    │       ├── behaviors.plone.less
    │       ├── breadcrumbs.plone.less
    │       ├── buttons.plone.less
    │       ├── code.plone.less
    │       ├── contents.plone.less
    │       ├── controlpanels.plone.less
    │       ├── deco.plone.less
    │       ├── discussion.plone.less
    │       ├── dropzone.plone.less
    │       ├── event.plone.less
    │       ├── fonts.plone.less
    │       ├── footer.plone.less
    │       ├── forms.plone.less
    │       ├── formtabbing.plone.less
    │       ├── grid.plone.less
    │       ├── header.plone.less
    │       ├── image.plone.less
    │       ├── loginform.plone.less
    │       ├── main.plone.less
    │       ├── mixin.borderradius.plone.less
    │       ├── mixin.buttons.plone.less
    │       ├── mixin.clearfix.plone.less
    │       ├── mixin.forms.plone.less
    │       ├── mixin.grid.plone.less
    │       ├── mixin.gridframework.plone.less
    │       ├── mixin.images.plone.less
    │       ├── mixin.prefixes.plone.less
    │       ├── mixin.tabfocus.plone.less
    │       ├── modal.plone.less
    │       ├── normalize.plone.less
    │       ├── pagination.plone.less
    │       ├── pickadate.plone.less
    │       ├── plone-toolbarlogo.svg
    │       ├── portlets.plone.less
    │       ├── print.plone.less
    │       ├── scaffolding.plone.less
    │       ├── search.plone.less
    │       ├── sitemap.plone.less
    │       ├── sitenav.plone.less
    │       ├── sortable.plone.less
    │       ├── states.plone.less
    │       ├── tables.plone.less
    │       ├── tablesorter.plone.less
    │       ├── tags.plone.less
    │       ├── thumbs.plone.less
    │       ├── toc.plone.less
    │       ├── tooltip.plone.less
    │       ├── tree.plone.less
    │       ├── type.plone.less
    │       ├── variables.plone.less
    │       └── views.plone.less
    ├── barceloneta-apple-touch-icon-114x114-precomposed.png
    ├── barceloneta-apple-touch-icon-144x144-precomposed.png
    ├── barceloneta-apple-touch-icon-57x57-precomposed.png
    ├── barceloneta-apple-touch-icon-72x72-precomposed.png
    ├── barceloneta-apple-touch-icon-precomposed.png
    ├── barceloneta-apple-touch-icon.png
    ├── barceloneta-favicon.ico
    ├── index.html
    ├── less
    │   ├── custom.less
    │   ├── plone.toolbar.vars.less
    │   ├── roboto
    │   │   ├── LICENSE.txt
    │   │   ├── Roboto-Light.eot
    │   │   ├── Roboto-Light.svg
    │   │   ├── Roboto-Light.ttf
    │   │   ├── Roboto-Light.woff
    │   │   ├── Roboto-LightItalic.eot
    │   │   ├── Roboto-LightItalic.svg
    │   │   ├── Roboto-LightItalic.ttf
    │   │   ├── Roboto-LightItalic.woff
    │   │   ├── Roboto-Medium.eot
    │   │   ├── Roboto-Medium.svg
    │   │   ├── Roboto-Medium.ttf
    │   │   ├── Roboto-Medium.woff
    │   │   ├── Roboto-MediumItalic.eot
    │   │   ├── Roboto-MediumItalic.svg
    │   │   ├── Roboto-MediumItalic.ttf
    │   │   ├── Roboto-MediumItalic.woff
    │   │   ├── Roboto-Regular.eot
    │   │   ├── Roboto-Regular.svg
    │   │   ├── Roboto-Regular.ttf
    │   │   ├── Roboto-Regular.woff
    │   │   ├── Roboto-Thin.eot
    │   │   ├── Roboto-Thin.svg
    │   │   ├── Roboto-Thin.ttf
    │   │   ├── Roboto-Thin.woff
    │   │   ├── Roboto-ThinItalic.eot
    │   │   ├── Roboto-ThinItalic.svg
    │   │   ├── Roboto-ThinItalic.ttf
    │   │   ├── Roboto-ThinItalic.woff
    │   │   ├── RobotoCondensed-Light.eot
    │   │   ├── RobotoCondensed-Light.svg
    │   │   ├── RobotoCondensed-Light.ttf
    │   │   ├── RobotoCondensed-Light.woff
    │   │   ├── RobotoCondensed-LightItalic.eot
    │   │   ├── RobotoCondensed-LightItalic.svg
    │   │   ├── RobotoCondensed-LightItalic.ttf
    │   │   └── RobotoCondensed-LightItalic.woff
    │   ├── theme-compiled.css
    │   ├── theme.less
    │   └── theme.local.less
    ├── manifest.cfg
    ├── node_modules
    │   └── bootstrap
    │       ├── CHANGELOG.md
    │       ├── Gruntfile.js
    │       ├── LICENSE
    │       ├── README.md
    │       ├── dist
    │       │   ├── css
    │       │   │   ├── bootstrap-theme.css
    │       │   │   ├── bootstrap-theme.css.map
    │       │   │   ├── bootstrap-theme.min.css
    │       │   │   ├── bootstrap-theme.min.css.map
    │       │   │   ├── bootstrap.css
    │       │   │   ├── bootstrap.css.map
    │       │   │   ├── bootstrap.min.css
    │       │   │   └── bootstrap.min.css.map
    │       │   ├── fonts
    │       │   │   ├── glyphicons-halflings-regular.eot
    │       │   │   ├── glyphicons-halflings-regular.svg
    │       │   │   ├── glyphicons-halflings-regular.ttf
    │       │   │   ├── glyphicons-halflings-regular.woff
    │       │   │   └── glyphicons-halflings-regular.woff2
    │       │   └── js
    │       │       ├── bootstrap.js
    │       │       ├── bootstrap.min.js
    │       │       └── npm.js
    │       ├── fonts
    │       │   ├── glyphicons-halflings-regular.eot
    │       │   ├── glyphicons-halflings-regular.svg
    │       │   ├── glyphicons-halflings-regular.ttf
    │       │   ├── glyphicons-halflings-regular.woff
    │       │   └── glyphicons-halflings-regular.woff2
    │       ├── grunt
    │       │   ├── bs-commonjs-generator.js
    │       │   ├── bs-glyphicons-data-generator.js
    │       │   ├── bs-lessdoc-parser.js
    │       │   ├── bs-raw-files-generator.js
    │       │   ├── change-version.js
    │       │   ├── configBridge.json
    │       │   ├── npm-shrinkwrap.json
    │       │   └── sauce_browsers.yml
    │       ├── js
    │       │   ├── affix.js
    │       │   ├── alert.js
    │       │   ├── button.js
    │       │   ├── carousel.js
    │       │   ├── collapse.js
    │       │   ├── dropdown.js
    │       │   ├── modal.js
    │       │   ├── popover.js
    │       │   ├── scrollspy.js
    │       │   ├── tab.js
    │       │   ├── tooltip.js
    │       │   └── transition.js
    │       ├── less
    │       │   ├── alerts.less
    │       │   ├── badges.less
    │       │   ├── bootstrap.less
    │       │   ├── breadcrumbs.less
    │       │   ├── button-groups.less
    │       │   ├── buttons.less
    │       │   ├── carousel.less
    │       │   ├── close.less
    │       │   ├── code.less
    │       │   ├── component-animations.less
    │       │   ├── dropdowns.less
    │       │   ├── forms.less
    │       │   ├── glyphicons.less
    │       │   ├── grid.less
    │       │   ├── input-groups.less
    │       │   ├── jumbotron.less
    │       │   ├── labels.less
    │       │   ├── list-group.less
    │       │   ├── media.less
    │       │   ├── mixins
    │       │   │   ├── alerts.less
    │       │   │   ├── background-variant.less
    │       │   │   ├── border-radius.less
    │       │   │   ├── buttons.less
    │       │   │   ├── center-block.less
    │       │   │   ├── clearfix.less
    │       │   │   ├── forms.less
    │       │   │   ├── gradients.less
    │       │   │   ├── grid-framework.less
    │       │   │   ├── grid.less
    │       │   │   ├── hide-text.less
    │       │   │   ├── image.less
    │       │   │   ├── labels.less
    │       │   │   ├── list-group.less
    │       │   │   ├── nav-divider.less
    │       │   │   ├── nav-vertical-align.less
    │       │   │   ├── opacity.less
    │       │   │   ├── pagination.less
    │       │   │   ├── panels.less
    │       │   │   ├── progress-bar.less
    │       │   │   ├── reset-filter.less
    │       │   │   ├── reset-text.less
    │       │   │   ├── resize.less
    │       │   │   ├── responsive-visibility.less
    │       │   │   ├── size.less
    │       │   │   ├── tab-focus.less
    │       │   │   ├── table-row.less
    │       │   │   ├── text-emphasis.less
    │       │   │   ├── text-overflow.less
    │       │   │   └── vendor-prefixes.less
    │       │   ├── mixins.less
    │       │   ├── modals.less
    │       │   ├── navbar.less
    │       │   ├── navs.less
    │       │   ├── normalize.less
    │       │   ├── pager.less
    │       │   ├── pagination.less
    │       │   ├── panels.less
    │       │   ├── popovers.less
    │       │   ├── print.less
    │       │   ├── progress-bars.less
    │       │   ├── responsive-embed.less
    │       │   ├── responsive-utilities.less
    │       │   ├── scaffolding.less
    │       │   ├── tables.less
    │       │   ├── theme.less
    │       │   ├── thumbnails.less
    │       │   ├── tooltip.less
    │       │   ├── type.less
    │       │   ├── utilities.less
    │       │   ├── variables.less
    │       │   └── wells.less
    │       └── package.json
    ├── package-lock.json
    ├── package.json
    ├── preview.png
    ├── rules.xml
    ├── template-overrides
    ├── tinymce-templates
    │   └── image-grid-2x2.html
    └── views
        └── slider-images.pt.example

28 directories, 256 files
```

As you can see, the package already contains a {term}`Diazo` theme including the {term}`Barceloneta` resources:

```console
tree -L 2 src/ploneconf/theme/theme/
src/ploneconf/theme/theme/
├── HOWTO_DEVELOP.rst
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
├── index.html
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

9 directories, 22 files
```

This theme basically provides you with a copy of the Plone 5 default theme (Barceloneta), and you can change everything you need to create your own theme.
The Barceloneta resources are in the folder `barceloneta`.

This is basically a copy of the theme folder of {py:mod}`plonetheme.barceloneta`.
We removed some unneeded files there, because we only need the {term}`Less` part for partially including it in our file {file}`theme.less`.

We also have the icons and the file {file}`backend.xml` from Barceloneta in our theme folder.

In the folder `theme/less` we have our {term}`CSS`/{term}`Less` files.
Our own CSS goes into the file {file}`custom.less`.

You can also add more {term}`Less` files and include them in {file}`theme.less`, if you have a lot of custom CSS and you like to split it into multiple files.

The file {file}`theme.less` is our main {term}`Less` file.
Here we include all other files we need.

It already has some includes of {term}`Barceloneta`, Twitter Bootstrap and our cusomizations from the file {file}`custom.less` at the bottom.

We also have a file {file}`package.json`, which we can use to define external dependencies like Twitter Bootstrap or other CSS/JS packages we want to use in our theme.
For more information on how to do this, see {ref}`install-ext-packages-with-npm`.

### Start Plone And Install Your Theme Product

To start the Plone instance, run:

```console
./bin/instance fg
```

The Plone instance will then be available at <http://localhost:8080>.
The default username is `admin` and password is `admin`.

1. Go to <http://localhost:8080> and click the button {guilabel}`Create a new Plone site` to add a new Plone site.
2. Name the site `Plone` (which should be the default) and click on {guilabel}`Create Plone Site`.
3. Go to the Plone Control Panel: {menuselection}`toolbar --> admin --> Site Setup`
4. Go to the {guilabel}`Add-ons` control panel.
5. Click on the {guilabel}`Install` next to `Plone Theme: Ploneconf Theme` to install your add-on.
6. The theme will be automatically enabled.

If something is wrong with the theme, you can always go to <http://localhost:8080/Plone/@@theming-controlpanel> and disable it.

This control panel will never be themed, so it works even if the theme might be broken.

````{dropdown}
:animate: fade-in-slide-down
:icon: question

Don't forget to commit any changes on your package to version control.
After the first buildout run, there are some new files and folders.
Some of them ({file}`node_modules` and {file}`package-lock.json`) can be ignored,
while others ({file}`theme-compiled.css`) need to be added to the repository.

Edit the {file}`.gitignore` file and add the following entries:

```console
node_modules/
package-lock.json
```

Then run the following commands:

```shell
git add .
git commit -m "Add compiled CSS file."
```
````

{doc}`In the next section <theme-package-2>` we will adjust the skeleton we got from `bobtemplates.plone` and fill it with our custom theme.
