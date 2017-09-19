===================================
Create a Plone Theme python package
===================================

Creating a theme product with the Diazo inline editor is an easy way to start and to test, but it is not a solid long term solution and you are also limited in what you can do that way.

Even if :py:mod:`plone.app.theming` allows importing and exporting of a Diazo theme as a ZIP archive, it might be preferable to manage your theme as an actual Plone product.

One of the most obvious reasons is that it will allow you to override Plone elements that are not accessible via pure Diazo features (such as overloading content view templates, viewlets, configuration settings, etc.).


Preparing your setup
====================

Install npm
-----------

If you don't have :term:`npm` already installed on your system please do it.
:program:`npm` comes with :program:`nodejs`, we just need to install :program:`npm`.
On Debian/Ubuntu for example you can do this with apt:

.. code-block:: bash

   $ sudo apt install -y npm

On a Mac you can install :program:`npm` using :program:`Homebrew`:

.. code-block:: bash

   $ brew install node

If you need a newer version of :program:`npm` just update your version with :command:`npm` itself:

.. code-block:: bash

   $ npm install npm@latest -g


Installing Grunt
----------------

We also need to install :program:`grunt-cli` globally.
If you already have it, you can skip this step.

.. code-block:: bash

   $ npm install -g grunt-cli

.. note::
   :class: toggle

   If you get an error with :program:`node` on Debian/Ubuntu, please check if you already have ``/usr/bin/node``, if not create a symlink like:

   .. code-block:: bash

      ln -s /usr/bin/nodejs /usr/bin/node


virtualenv and mr.bob
---------------------

First, let's create a Python :program:`virtualenv`:

.. code-block:: bash

   $ virtualenv mrbobvenv

Then we enable the virtualenv:

.. code-block:: bash

   $ source mrbobvenv/bin/activate
   (mrbobvenv):$


Create a product to handle your Diazo theme
===========================================

To create a Plone 5 theme skeleton, you will use :program:`mr.bob`'s templates for Plone.


Install mr.bob and bobtemplates.plone
-------------------------------------

To install :py:mod:`mr.bob`, you can use :command:`pip`:

.. code-block:: bash

   (mrbobvenv):$ pip install bobtemplates.plone==2.0

Create a Plone 5 theme product skeleton with :command:`mrbob`.
It will ask you some questions about the new theme package:

.. code-block:: bash

   (mrbobvenv):$ mrbob -O ploneconf.theme bobtemplates:plone_theme_package

   Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

   Answer with a question mark to display help.
   Values in square brackets at the end of the questions show the default value if there is no answer.


   --> Theme name [Theme]: Ploneconf Theme

   --> Author name [Your Name]:

   --> Author email [your.email@example.com]:

   --> Author github username:

   --> Package description [An add-on for Plone]: Plone Conference Training Theme

   --> Plone version [5.0.8]:

Now you have a new Python package in your current folder:

.. code-block:: bash

   (mrbobvenv):$ ls ploneconf.theme
   CHANGES.rst            LICENSE.GPL            bootstrap-buildout.py  package.json           src
   CONTRIBUTORS.rst       LICENSE.rst            bootstrap-buildout.pyc requirements.txt
   Gruntfile.js           MANIFEST.in            buildout.cfg           setup.cfg
   HOWTO_DEVELOP.rst      README.rst             docs                   setup.py

It is now safe to deactivate the ``mrbob`` virtualenv:

.. code-block:: bash

   (mrbobvenv):$ deactivate

.. hint::
   :class: toggle

   This would be the perfect time to initialize your package with Git and put your files under version control:

   .. code-block:: bash

      $ cd ploneconf.theme
      $ git init .
      $ git add .
      $ git commit -m "Initial commit."
      $ cd ..


Install Buildout and boostrap your development environment
----------------------------------------------------------

You can install Buildout globally or on a virtualenv.
We will install ``zc.buildout`` in a new virtual environment using the provided :file:`requirements.txt`.

.. code-block:: bash

   $ virtualenv buildoutvenv
   $ source buildoutvenv/bin/activate
   (buildoutvenv):$ cd ploneconf.theme
   (buildoutvenv):$ pip install -r requirements.txt
   (buildoutvenv):$ buildout bootstrap

Now you have everything in place and you can run :command:`buildout`.
Depending on your internet connection and your local buildout cache this can take several minutes to complete.

.. code-block:: bash

   (buildoutvenv):$ ./bin/buildout

After buildout finished successfully it is now safe to deactivate the ``buildoutvenv`` virtualenv:

.. code-block:: bash

   (buildoutvenv):$ deactivate

This will create the whole development environment for your package:

.. code-block:: bash

   $ ls bin
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


Inspect your package source
---------------------------

Your package source code is in the ``src`` folder:

.. code-block:: bash

   $ tree src/ploneconf/theme/
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


As you can see, the package already contains a :term:`Diazo` theme including the :term:`Barceloneta` resources:

.. code-block:: bash

   $ tree -L 2 src/ploneconf/theme/theme/
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

This theme basically provides you with a copy of the Plone 5 default theme (Barceloneta), and you can change everything you need to create your own theme.
The Barceloneta resources are in the folder ``barceloneta``.
This is basically a copy of the theme folder of :py:mod:`plonetheme.barceloneta`.
We removed some unneeded files there, because we only need the :term:`Less` part for partially including it in our file :file:`theme.less`.
We also have the icons and the file :file:`backend.xml` from Barceloneta in our theme folder.

In the folder ``theme/less`` we have our :term:`CSS`/:term:`Less` files.
Our own CSS goes into the file :file:`custom.less`.
You can also add more :term:`Less` files and include them in :file:`theme.less`, if you have a lot of custom CSS and you like to split it into multiple files.

The file :file:`theme.less` is our main :term:`Less` file.
Here we include all other files we need.
It already has some includes of :term:`Barceloneta`, Twitter Bootstrap and our cusomizations from the file :file:`custom.less` at the bottom.

We also have a file :file:`package.json`, which we can use to define external dependencies like Twitter Bootstrap or other CSS/JS packages we want to use in our theme.
For more information on how to do this, see :ref:`install-ext-packages-with-npm`.


Start Plone and install your theme product
------------------------------------------

To start the Plone instance, run:

.. code-block:: bash

   $ ./bin/instance fg

The Plone instance will then be available at http://localhost:8080.
The default username is ``admin`` and password is ``admin``.

#. Go to http://localhost:8080 and click the button :guilabel:`Create a new Plone site` to add a new Plone site.
#. Name the site ``Plone`` (which should be the default) and click on :guilabel:`Create Plone Site`.
#. Go to the Plone Control Panel: :menuselection:`toolbar --> admin --> Site Setup`
#. Go to the :guilabel:`Add-ons` control panel.
#. Click on the :guilabel:`Install` next to ``Plone Theme: Ploneconf Theme`` to install your add-on.
#. The theme will be automatically enabled.

If something is wrong with the theme, you can always go to http://localhost:8080/Plone/@@theming-controlpanel and disable it.
This control panel will never be themed, so it works even if the theme might be broken.

.. hint::
   :class: toggle

   Don't forget to commit any changes on your package to version control.
   After the first buildout run, there are some new files and folders.
   Some of them (:file:`node_modules` and :file:`package-lock.json`) can be ignored, while others (:file:`theme-compiled.css`) need to be added to the repository.

   Edit the :file:`.gitignore` file and add the following entries:

   .. code-block:: bash

      node_modules/
      package-lock.json

   Then run the following commands:

   .. code-block:: bash

      $ git add .
      $ git commit -m "Add compiled CSS file."


Build your Diazo-based theme
============================

You can start with the example files in the theme folder and just change the :file:`index.html` and :file:`custom.less` files to customize the default theme to your needs.
As stated above it's the Plone 5 default :term:`Barceloneta` theme plus some custom files you can use to to override or write CSS/Less.

Use your own static mockup
--------------------------

If you got a static mockup from your designer or from a website like http://startbootstrap.com (where the example template came from), you can use this without customization and just apply the Diazo rules to it.

Another way is to change the static mockup a little bit to use mostly the same CSS id's and classes like Plone does.
This way it is easier to reuse CSS/Less from Barceloneta and Plone add-ons if needed.


Download and prepare a static theme
-----------------------------------

Let's start with an untouched static template, such as this Twitter Bootstrap based one: http://startbootstrap.com/template-overviews/business-casual/.
The latest version of that template uses a beta version of Twitter Bootstrap 4.
We are going to use the latest release which uses Twitter Bootstrap 3.
Download it from https://github.com/BlackrockDigital/startbootstrap-business-casual/releases/tag/v3.3.7 and extract it into the theme folder.
Replace the :file:`index.html` with the one from the downloaded template.
The content of your theme folder should now look like this:

.. code-block:: bash

   $ tree -L 2 src/ploneconf/theme/theme/
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


Preparing the template
++++++++++++++++++++++

To make the given template :file:`index.html` more useful, we customize it a little bit.
Right before the second box which contains:

.. code-block:: html

   <div class="row">
       <div class="box">
           <div class="col-lg-12">
               <hr>
               <h2 class="intro-text text-center">Build a website
                   <strong>worth visiting</strong>
               </h2>

Add this:

.. code-block:: html

   <div class="row">
     <div id="column1-container"></div>
     <div id="content-container">
       <!-- main content (box2 and box3) comes here -->
     </div>
     <div id="column2-container"></div>
   </div>

And then move the main content (the box 2 and box 3 including the parent ``div`` with the class ``row``) into the ``content-container``.

It should now look like this:

.. code-block:: html

   <div class="row">
     <div id="column1-container"></div>
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
     <div id="column2-container"></div>
   </div>

Include theme CSS
+++++++++++++++++

Next we need to include the CSS from the template into our :file:`theme.less` file:

.. code-block:: less

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

   // include our custom css/less
   @import "custom.less";

We will add the include of the CSS the template provides in :file:`theme/css/business-casual.css` after the ``END OF UTILS`` marker, but before the ``custom.less`` include:

.. code-block:: less

   /* ### END OF UTILS ### */
   @import "../css/business-casual.css";

We include the CSS file here as a :term:`Less` file.
This way we can extend parts of the CSS in our theme (we will do this with the ``.box`` class in the next section).

.. note::

   Don't forget to run :command:`grunt compile` in your package root after you changed the :term:`Less` files.
   You can also use :command:`grunt watch` to automatically compile your :term:`Less` files to CSS whenver they are changed.

Using Diazo rules to map the theme with Plone content
-----------------------------------------------------

Now that we have the static theme,
we need to apply the Diazo rules in :file:`rules.xml` to map the Plone content
elements to the theme.

First let me explain what we mean when we talk about *content* and *theme*.
*Content* is usually the dynamic generated content on the Plone site, and the
*theme* is the static template site.

For example:

.. code-block:: xml

   <replace css:theme="#headline" css:content="#firstHeading" />

This means that the element ``#headline`` in the theme should be replaced by
the ``#firstHeading`` element from the generated Plone content.

To inspect the content side, you can open another Browser tab, but instead of http://localhost:8080/Plone, use http://127.0.0.1:8080/Plone.
In this tab Diazo is disabled, allowing you to use your browser's Inspector or Developer tools to view the DOM structure of default Plone.
This 'unthemed host name' is managed in the Theming control panel > Advanced Settings, where more domains can be added.

For more details on how to use Diazo rules, look at
http://docs.diazo.org/en/latest/ and
https://docs.plone.org/external/plone.app.theming/docs/index.html.


We already have a fully functional rule set based on the Plone 5 default Theme:

.. code-block:: xml

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
       <!-- drop the theme stylesheets -->
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

As you probably noticed, the theme does not look like it should and is missing some important parts like the toolbar. That is because we are using an HTML template, which has different HTML structure, than the one Plone's default theme is using.

We can either change our theme's template to use the same structure and naming for classes and ids, or we can change our rule set to work with the theme template like it is. We will mainly go the second way and customize our rule set to work with the provided theme template. In fact if you use a better theme template then this, where more useful CSS classes and ids used and the grid is defined in CSS/LESS and not in the HTML markup it self, it is a lot easier to work with touching the theme. But we use this popular example theme and therefor need also to make changes to the template it self a bit.

Customize the rule set
----------------------

The most important part of Plone is the toolbar. So let's first make sure we have it in our theme template.

Plone Toolbar
+++++++++++++

We already have the needed Diazo rules in our rules.xml:

.. code-block:: xml

   <!-- toolbar -->
   <replace css:theme="#portal-toolbar" css:content-children="#edit-bar" css:if-not-content=".ajax_load" css:if-content=".userrole-authenticated" />

The only thing we need is a placeholder in our theme template:

.. code-block:: html

   <section id="portal-toolbar">
   </section>

You can put it right after the opening body tag in your index.html



Login link & co
+++++++++++++++

If you want to have a login link for your users, you can put this placeholder in your theme template where you want the link to display.
You can always log in by adding ``/login`` to the Plone url, so it's optional.

.. code-block:: html

   <div id="anonymous-actions">
   </div>

The necessary rule to fill this with the Plone login link is already in our rules.xml:

.. code-block:: xml

   <replace css:theme="#anonymous-actions" css:content-children="#portal-personaltools-wrapper" css:if-not-content=".ajax_load" css:if-content=".userrole-anonymous" />

This will replace your placeholder with ``#portal-personaltools-wrapper`` from Plone (for example the login link). The link will only be inserted if the user is not already logged in.


Top-navigation
++++++++++++++

Replace the placeholder with the real Plone top-navigation links.
To do this we replace this rule from Barceloneta:

.. code-block:: xml

   <!-- move global nav -->
   <replace css:theme-children="#mainnavigation" css:content-children="#portal-mainnavigation" method="raw" />

with our new rule:

.. code-block:: xml

   <!-- replace theme navbar-nav with Plone plone-navbar-nav -->
   <replace
     css:theme-children=".navbar-nav"
     css:content-children=".plone-navbar-nav" />

Here we take the list of links from Plone and replace the placeholder links in
the theme with it. The Barceloneta rule copies the whole navigation container into the theme, but only need to copy the links over.


Breadcrumb & co
+++++++++++++++

Plone provides some viewlets like the breadcrumbs (the current path) above the content area.

We already have the needed rule to insert the Plone above-content stuff into the theme:

.. code-block:: xml

   <!-- full-width breadcrumb -->
   <replace css:content="#viewlet-above-content" css:theme="#above-content" />

To get this into the theme layout, we add a placeholder with the CSS id ``#above-content`` to the theme's ``index.html``.
This is the place where we want to insert Plone's "above-content" stuff.

For example, at the top of the ``div.container`` after:

.. code-block:: html

    <!-- Navigation -->
    <nav class="navbar navbar-default" role="navigation">
        ...
    </nav>

    <div class="container">

        <!-- insert here -->

goes this before the row/box:

.. code-block:: html

       <div class="row">
           <div id="above-content" class="box"></div>
       </div>


This will bring over everything from the ``viewlet-above-content`` block from
Plone.

This also includes the Breadcrumb bar. Because our current theme does not provide a breadcrumb bar, we can just drop it from the Plone content, like this:

.. code-block:: xml

   <drop css:content="#portal-breadcrumbs" />

If you only want to drop this for non-administrators, you can do it like this:

.. code-block:: xml

   <drop
    css:content="#portal-breadcrumbs"
    css:if-not-content=".userrole-manager"
    />

Or for anonymous users only:

.. code-block:: xml

   <drop
    css:content="#portal-breadcrumbs"
    css:if-content=".userrole-anonymous"
    />

.. note::

   The classes like *userrole-anonymous* are provided by Plone in the ``body`` tag.


Slider only on Front-page
+++++++++++++++++++++++++

We want the slider in the template only on the front page, and we don't want it
when we are editing the front page. To make this easier, we add ``#front-page-slider`` to the outer row ``div``-tag which contains the slider:

.. code-block:: html

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


Now we can drop it if we are not on the front page and also in some other situations:

.. code-block:: xml

   <drop
     css:theme="#front-page-slider"
     css:if-not-content=".section-front-page.template-document_view" />

Currently the slider is still static, but we will change that later in :ref:`create-dynamic-slider-content-in-plone`.

Title and Description
+++++++++++++++++++++

Let's delete the tag with the id ``brand-before`` from the theme template.

.. code-block:: xml

   <drop
     css:theme=".brand-before"
     css:if-content=".section-front-page" />

Now let's put the necessary rules for the Title and Description in our rules.xml:

.. code-block:: xml

   <replace
     css:theme-children=".brand-name"
     css:content-children=".documentFirstHeading"
     method="raw" />
   <drop
     css:content=".documentFirstHeading"
     css:if-content=".section-front-page" />

   <replace
     css:theme="#front-page-slider h2"
     css:content=".documentDescription"
     method="raw" />
   <drop
     css:content=".documentDescription"
     css:if-content=".section-front-page" />


If we have the slider on the front page, the Plone title will be placed inside the tag with the class ``brand-name``. If we don't have the slider, we see the title inside the tag with the class ``documentFirstHeading``.


Status messages
+++++++++++++++

Plone will render status messages in the ``#global_statusmessage`` element.
We want to bring these messages across to the theme.
For this, we add another placeholder into our theme template:

.. code-block:: html

   <div class="row">
       <div id="global_statusmessage"></div>
       <div id="above-content"></div>
   </div>

and we already have this rule to bring the messages across:

.. code-block:: xml

   <!-- Alert message -->
   <replace css:theme-children="#global_statusmessage" css:content-children="#global_statusmessage" />

To test that, just edit the front page. You should see a confirmation message from Plone.

Main content area 1
+++++++++++++++++++

To make the Plone content area flexible and containing the correct
bootstrap grid classes, we use an inline XSL snippet.
This is already in our rules.xml, but needs some customization for our theme:

.. code-block:: xml

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
         <div class="box">
           <div class="col-xs-12 col-sm-12">
             <xsl:apply-templates css:select="#content" />
           </div>
         </div>
       </div>
       <footer class="row">
         <div class="box">
           <div class="col-xs-12 col-sm-12">
             <xsl:copy-of css:select="#viewlet-below-content" />
           </div>
         </div>
       </footer>
     </div>
   </replace>

This will add the right grid classes to the content columns depending on one-column-, two-column- or three-column-layout.
We need to wrap these elements in a div with the class ``box``.


Left and right columns
++++++++++++++++++++++

We have already added the ``column1-container`` and ``column2-container`` ids to our template.
The following rules will incorporate the left and the right columns from Plone
into the theme, and also change their markup to be an ``aside`` instead of a
normal ``div``. That is the reason to use inline XSL here, but we already have it in our rules:

.. code-block:: xml

   <!-- Left column -->
   <rules css:if-content="#portal-column-one">
     <replace css:theme="#column1-container">
         <div id="left-sidebar" class="col-xs-6 col-sm-3 sidebar-offcanvas">
           <aside id="portal-column-one">
              <xsl:copy-of css:select="#portal-column-one > *" />
           </aside>
         </div>
     </replace>
   </rules>

   <!-- Right column -->
   <rules css:if-content="#portal-column-two">
     <replace css:theme="#column2-container">
         <div id="right-sidebar" class="col-xs-6 col-sm-3 sidebar-offcanvas" role="complementary">
           <aside id="portal-column-two">
              <xsl:copy-of css:select="#portal-column-two > *" />
           </aside>
         </div>
     </replace>
   </rules>

So nothing more to do here.

Footer
++++++

Bring across the footer from Plone:

.. code-block:: xml

   <!-- footer -->
   <replace
     css:theme-children="footer > .container"
     css:content-children="#portal-footer-wrapper" />

That was basically all to bring the theme together with the dynamic elements from Plone.
The rest is more or less CSS. Later we will :ref:`create-dynamic-slider-content-in-plone` to make the slider dynamic and let users change the pictures for the slider.

Understanding and using the Grunt build system
++++++++++++++++++++++++++++++++++++++++++++++

We already have a ``Gruntfile.js`` in the top level directory of our theme package:

.. code-block:: js

   module.exports = function (grunt) {
       'use strict';
       grunt.initConfig({
           pkg: grunt.file.readJSON('package.json'),
           // we could just concatenate everything, really
           // but we like to have it the complex way.
           // also, in this way we do not have to worry
           // about putting files in the correct order
           // (the dependency tree is walked by r.js)
           less: {
               dist: {
                   options: {
                       paths: [],
                       strictMath: false,
                       sourceMap: true,
                       outputSourceFiles: true,
                       sourceMapURL: '++theme++tango/less/theme-compiled.css.map',
                       sourceMapFilename: 'less/theme-compiled.css.map',
                       modifyVars: {
                           "isPlone": "false"
                       }
                   },
                   files: {
                       'less/theme-compiled.css': 'less/theme.local.less',
                   }
               }
           },
           postcss: {
               options: {
                   map: true,
                   processors: [
                       require('autoprefixer')({
                           browsers: ['last 2 versions']
                       })
                   ]
               },
               dist: {
                   src: 'less/*.css'
               }
           },
           watch: {
               scripts: {
                   files: [
                       'less/*.less',
                       'barceloneta/less/*.less'
                   ],
                   tasks: ['less', 'postcss']
               }
           },
           browserSync: {
               html: {
                   bsFiles: {
                       src : [
                         'less/*.less',
                         'barceloneta/less/*.less'
                       ]
                   },
                   options: {
                       watchTask: true,
                       debugInfo: true,
                       online: true,
                       server: {
                           baseDir: "."
                       },
                   }
               },
               plone: {
                   bsFiles: {
                       src : [
                         'less/*.less',
                         'barceloneta/less/*.less'
                       ]
                   },
                   options: {
                       watchTask: true,
                       debugInfo: true,
                       proxy: "localhost:8080",
                       reloadDelay: 3000,
                       // reloadDebounce: 2000,
                       online: true
                   }
               }
           }
       });

       // grunt.loadTasks('tasks');
       grunt.loadNpmTasks('grunt-browser-sync');
       grunt.loadNpmTasks('grunt-contrib-watch');
       grunt.loadNpmTasks('grunt-contrib-less');
       grunt.loadNpmTasks('grunt-postcss');

       // CWD to theme folder
       grunt.file.setBase('./src/plonetheme/tango/theme');

       grunt.registerTask('compile', ['less', 'postcss']);
       grunt.registerTask('default', ['compile']);
       grunt.registerTask('bsync', ["browserSync:html", "watch"]);
       grunt.registerTask('plone-bsync', ["browserSync:plone", "watch"]);
   };


At the end, we can see some registered ``Grunt`` tasks.
We can use these tasks to control what happens when we run ``Grunt``.

By default ``Grunt`` will just run the ``compile task``, which means the less files are getting compiled and the postcss task is run:

.. code-block:: bash

   $ grunt
   Running "less:dist" (less) task
   >> 1 stylesheet created.
   >> 1 sourcemap created.

   Running "postcss:dist" (postcss) task
   >> 1 processed stylesheet created.

   Done, without errors.

If we want ``grunt`` to watch for changes in our less files and let them compile it automatically after every change, we can run ``grunt watch``, and it will run the ``compile`` task after every change of a LESS file:

.. code-block:: bash

   $ grunt watch
   Running "watch" task
   Waiting...

If some LESS file has changed, you will see something like this:

.. code-block:: bash

   $ grunt watch
   Running "watch" task
   Waiting...
   >> File "less/custom.less" changed.
   Running "less:dist" (less) task
   >> 1 stylesheet created.
   >> 1 sourcemap created.

   Running "postcss:dist" (postcss) task
   >> 1 processed stylesheet created.

   Done, without errors.
   Completed in 2.300s at Mon Oct 10 2016 20:05:27 GMT+0200 (CEST) - Waiting...

   Done, without errors.

They are also other useful tasks like ``plone-bsync``, which we can use to also update the Browser after changes.

.. code-block:: bash

   $ grunt plone-bsync
   Running "browserSync:plone" (browserSync) task
   [BS] Proxying: http://localhost:8081
   [BS] Access URLs:
    --------------------------------------
          Local: http://localhost:3000
       External: http://192.168.2.149:3000
    --------------------------------------
             UI: http://localhost:3001
    UI External: http://192.168.2.149:3001
    --------------------------------------
   [BS] Watching files...

   Running "watch" task
   Waiting...

You will now see an open browser window, which is automatically reloaded any time a LESS file has changed and the CSS was recompiled.

.. note::

   If you use other ports or IP's for your Plone backend, you have to set up the proxy in the Gruntfile.js to the Plone backend address:port.


Theme manifest.xml
******************

Now let's have a look at our theme's ``manifest.cfg`` which declares ``development-css``, ``production-css`` and optionally ``tinymce-content-css``, like this:

.. code-block:: cfg

   [theme]
   title = Plone Theme: Tango
   description = A Diazo based Plone theme
   doctype = <!DOCTYPE html>
   rules = /++theme++tango/rules.xml
   prefix = /++theme++tango
   enabled-bundles =
   disabled-bundles =

   development-css = /++theme++tango/less/theme.less
   production-css = /++theme++tango/less/theme-compiled.css
   tinymce-content-css = /++theme++tango/less/theme-compiled.css

   # development-js = /++theme++tango/js/theme.js
   # production-js = /++theme++tango/js/theme-compiled.js

   [theme:overrides]
   directory = template-overrides

   [theme:parameters]
   # portal_url = python: portal.absolute_url()

The ``development-css`` file is used when Plone is running in development mode, otherwise the file under ``production-css`` will be used.

The last one ``tinymce-content-css`` tells Plone to load that particular CSS file inside TinyMCE, wherever a TinyMCE rich text field is displayed.

.. note::

  After making manifest changes, we need to deactivate/activate the theme
  for them to take effect. Just go to ``/@@theming-controlpanel`` and do it.


Final CSS customization
+++++++++++++++++++++++

To make our theme look nicer, we add some CSS as follows to our ``custom.less``
file:

.. code:: css

   /* Custom LESS file that is included from the theme.less file */

   .brand-name{
       margin-top: 0.5em;
   }

   .documentDescription{
       margin-top: 1em;
   }

   .clearFix{
       clear: both;
   }

   #left-sidebar {
       padding-left: 0;
   }

   #right-sidebar {
       padding-right: 0;
   }

   #content {
       label, .label {
           color: #333;
           font-size: 100%;
       }
   }

   .pat-autotoc.autotabs, .autotabs {
       border-width: 0;
   }

   .portal-column-one .portlet,
   .portal-column-two .portlet {
       .box;
   }

   footer .portletActions{
   }

   footer {
       .portlet {
           padding: 1em 0;
           margin-bottom: 0;
           border: 0;
           background: transparent;
           .portletContent{
               border: 0;
               background: transparent;
               ul {
                   padding-left: 0;
                   list-style-type: none;
                   .portletItem {
                       display: inline-block;
                       &:not(:last-child){
                           padding-right: 0.5em;
                           margin-right: 0.5em;
                           border-right: 1px solid;
                       }
                       &:hover{
                           background-color: transparent;
                       }
                       a{
                           color: #000;
                           padding: 0;
                           text-decoration: none;
                           &:hover{
                               background-color: transparent;
                           }
                           &::before{
                               content: none;
                           }
                       }
                   }
               }
           }
       }
   }


.. _install-ext-packages-with-npm:

Install external CSS and JavaScript with npm and use them in your theme
***********************************************************************

As our theme is based on ``Bootstrap``, we want to install ``Bootstrap`` with ``npm`` to have more flexibility, for example to use the LESS file of Bootstrap.
To do that, we use ``npm``, which you should already have globally installed on your
system.

.. note:: The following steps are already included in bobtemplates.plone template, they are here only for documentation reasons, to show how to install and use external packages like ``Bootstrap``.

To install ``Bootstrap`` with ``npm`` run the following command inside the theme folder:

.. code-block:: bash

   $ npm install bootstrap --save

The ``--save`` option will add the package to ``package.json`` in the theme folder for us.
Now, we can install all dependencies on any other system by running the
following command from inside of our theme folder:

.. code-block:: bash

   $ npm install

Now that we have installed bootstrap using npm, we have all bootstrap
components available in the subfolder called ``node_modules``:

.. code-block:: bash

   $ tree node_modules/bootstrap/
   node_modules/bootstrap/
   ├── CHANGELOG.md
   ├── dist
   │   ├── css
   │   │   ├── bootstrap.css
   │   │   ├── bootstrap.css.map
   │   │   ├── bootstrap.min.css
   │   │   ├── bootstrap-theme.css
   │   │   ├── bootstrap-theme.css.map
   │   │   └── bootstrap-theme.min.css
   │   ├── fonts
   │   │   ├── glyphicons-halflings-regular.eot
   │   │   ├── glyphicons-halflings-regular.svg
   │   │   ├── glyphicons-halflings-regular.ttf
   │   │   ├── glyphicons-halflings-regular.woff
   │   │   └── glyphicons-halflings-regular.woff2
   │   └── js
   │       ├── bootstrap.js
   │       ├── bootstrap.min.js
   │       └── npm.js
   ├── fonts
   │   ├── glyphicons-halflings-regular.eot
   │   ├── glyphicons-halflings-regular.svg
   │   ├── glyphicons-halflings-regular.ttf
   │   ├── glyphicons-halflings-regular.woff
   │   └── glyphicons-halflings-regular.woff2
   ├── grunt
   │   ├── bs-commonjs-generator.js
   │   ├── bs-glyphicons-data-generator.js
   │   ├── bs-lessdoc-parser.js
   │   ├── bs-raw-files-generator.js
   │   ├── configBridge.json
   │   └── sauce_browsers.yml
   ├── Gruntfile.js
   ├── js
   │   ├── affix.js
   │   ├── alert.js
   │   ├── button.js
   │   ├── carousel.js
   │   ├── collapse.js
   │   ├── dropdown.js
   │   ├── modal.js
   │   ├── popover.js
   │   ├── scrollspy.js
   │   ├── tab.js
   │   ├── tooltip.js
   │   └── transition.js
   ├── less
   │   ├── alerts.less
   │   ├── badges.less
   │   ├── bootstrap.less
   │   ├── breadcrumbs.less
   │   ├── button-groups.less
   │   ├── buttons.less
   │   ├── carousel.less
   │   ├── close.less
   │   ├── code.less
   │   ├── component-animations.less
   │   ├── dropdowns.less
   │   ├── forms.less
   │   ├── glyphicons.less
   │   ├── grid.less
   │   ├── input-groups.less
   │   ├── jumbotron.less
   │   ├── labels.less
   │   ├── list-group.less
   │   ├── media.less
   │   ├── mixins
   │   │   ├── alerts.less
   │   │   ├── background-variant.less
   │   │   ├── border-radius.less
   │   │   ├── buttons.less
   │   │   ├── center-block.less
   │   │   ├── clearfix.less
   │   │   ├── forms.less
   │   │   ├── gradients.less
   │   │   ├── grid-framework.less
   │   │   ├── grid.less
   │   │   ├── hide-text.less
   │   │   ├── image.less
   │   │   ├── labels.less
   │   │   ├── list-group.less
   │   │   ├── nav-divider.less
   │   │   ├── nav-vertical-align.less
   │   │   ├── opacity.less
   │   │   ├── pagination.less
   │   │   ├── panels.less
   │   │   ├── progress-bar.less
   │   │   ├── reset-filter.less
   │   │   ├── reset-text.less
   │   │   ├── resize.less
   │   │   ├── responsive-visibility.less
   │   │   ├── size.less
   │   │   ├── tab-focus.less
   │   │   ├── table-row.less
   │   │   ├── text-emphasis.less
   │   │   ├── text-overflow.less
   │   │   └── vendor-prefixes.less
   │   ├── mixins.less
   │   ├── modals.less
   │   ├── navbar.less
   │   ├── navs.less
   │   ├── normalize.less
   │   ├── pager.less
   │   ├── pagination.less
   │   ├── panels.less
   │   ├── popovers.less
   │   ├── print.less
   │   ├── progress-bars.less
   │   ├── responsive-embed.less
   │   ├── responsive-utilities.less
   │   ├── scaffolding.less
   │   ├── tables.less
   │   ├── theme.less
   │   ├── thumbnails.less
   │   ├── tooltip.less
   │   ├── type.less
   │   ├── utilities.less
   │   ├── variables.less
   │   └── wells.less
   ├── LICENSE
   ├── package.json
   └── README.md

To include the needed "carousel" part and some other bootstrap components which
our downloaded theme uses, we change our ``theme.less`` to look like this:

.. code-block:: css

   /* theme.less file that will be compiled */

   /* ### PLONE IMPORTS ### */

   @barceloneta_path: "barceloneta/less";

   /* Core variables and mixins */
   @import "@{barceloneta_path}/fonts.plone.less";
   @import "@{barceloneta_path}/variables.plone.less";
       @import "@{barceloneta_path}/mixin.prefixes.plone.less";
       @import "@{barceloneta_path}/mixin.tabfocus.plone.less";
       @import "@{barceloneta_path}/mixin.images.plone.less";
       @import "@{barceloneta_path}/mixin.forms.plone.less";
       @import "@{barceloneta_path}/mixin.borderradius.plone.less";
       @import "@{barceloneta_path}/mixin.buttons.plone.less";
       @import "@{barceloneta_path}/mixin.clearfix.plone.less";
   //    @import "@{barceloneta_path}/mixin.gridframework.plone.less"; //grid Bootstrap
       @import "@{barceloneta_path}/mixin.grid.plone.less"; //grid Bootstrap

   @import "@{barceloneta_path}/normalize.plone.less";
   @import "@{barceloneta_path}/print.plone.less";
   @import "@{barceloneta_path}/code.plone.less";

   /* Core CSS */
   @import "@{barceloneta_path}/grid.plone.less";
   @import "@{barceloneta_path}/scaffolding.plone.less";
   @import "@{barceloneta_path}/type.plone.less";
   @import "@{barceloneta_path}/tables.plone.less";
   @import "@{barceloneta_path}/forms.plone.less";
   @import "@{barceloneta_path}/buttons.plone.less";
   @import "@{barceloneta_path}/states.plone.less";

   /* Components */
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

   /* Patterns */
   @import "@{barceloneta_path}/accessibility.plone.less";
   @import "@{barceloneta_path}/toc.plone.less";
   @import "@{barceloneta_path}/dropzone.plone.less";
   @import "@{barceloneta_path}/modal.plone.less";
   @import "@{barceloneta_path}/pickadate.plone.less";
   @import "@{barceloneta_path}/sortable.plone.less";
   @import "@{barceloneta_path}/tablesorter.plone.less";
   @import "@{barceloneta_path}/tooltip.plone.less";
   @import "@{barceloneta_path}/tree.plone.less";

   /* Structure */
   @import "@{barceloneta_path}/header.plone.less";
   @import "@{barceloneta_path}/sitenav.plone.less";
   @import "@{barceloneta_path}/main.plone.less";
   @import "@{barceloneta_path}/footer.plone.less";
   @import "@{barceloneta_path}/loginform.plone.less";
   @import "@{barceloneta_path}/sitemap.plone.less";

   /* Products */
   @import "@{barceloneta_path}/event.plone.less";
   @import "@{barceloneta_path}/image.plone.less";
   @import "@{barceloneta_path}/behaviors.plone.less";
   @import "@{barceloneta_path}/discussion.plone.less";
   @import "@{barceloneta_path}/search.plone.less";

   // ### END OF PLONE IMPORTS ###

   // ### UTILS ###

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

   // END OF UTILS

   // include theme css as less
   @import (less) "../css/business-casual.css";

   // include our custom css/less
   @import "custom.less";

Here you can see how we include the resources like ``@import "@{bootstrap_path}/carousel.less";`` in our LESS file.

Also take notice of the definition:

.. code-block:: css

   @bootstrap_path: "node_modules/bootstrap/less";

here we define the bootstrap path, so that we can use it in all bootstrap includes.

.. note:: Don't forget to run ``grunt compile`` after you changed the LESS files or use ``grunt watch`` to do this automatically after every change!


More Diazo and plone.app.theming details
****************************************

For more details how to build a Diazo based theme, look at http://docs.diazo.org/en/latest/ and https://docs.plone.org/external/plone.app.theming/docs/index.html.
