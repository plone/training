===================================
Create a Plone theme python package
===================================

Creating a theme product with the Diazo inline editor is an easy way to start
and to test, but it is not a solid long term solution.

Even if ``plone.app.theming`` allows importing and exporting of a Diazo theme
as a ZIP archive, it might be preferable to manage your theme as an actual
Plone product.

One of the most obvious reasons is that it will allow you to override Plone
elements that are not accessible via pure Diazo features (such as overloading
content view templates, viewlets, configuration settings, etc.).


Preparing your setup
====================

First we want create a Python virtualenv:

.. code-block:: bash

   $ virtualenv mrbobvenv

Then we enable the virtualenv:

.. code-block:: bash

   vagrant@precise32:~$ source mrbobvenv/bin/activate
   (mrbobvenv)vagrant@precise32:~$


Create a product to handle your Diazo theme
===========================================

To create a Plone 5 theme skeleton, you will use mr.bob's templates for Plone.


Install mr.bob and bobtemplates.plone
-------------------------------------

To install ``mr.bob``, you can use ``pip``:

.. code-block:: bash

   $ pip install mr.bob

and to install the required bobtemplates for Plone, do:

.. code-block:: bash

   $ pip install bobtemplates.plone

Create a Plone 5 theme product skeleton with mrbob:

.. code-block:: bash

   $ mrbob -O plonetheme.tango bobtemplates:plone_addon

It will ask you some question::

   --> What kind of package would you like to create? Choose between 'Basic', 'Dexterity', and 'Theme'. [Basic]: Theme

Here, choose "Theme" and fill out the rest of the questions however you like::

   --> Author's name [MrTango]:

   --> Author's email [md@derico.de]:

   --> Author's github username: MrTango

   --> Package description [An add-on for Plone]: Plone theme tango

   --> Plone version [4.3.6]: 5.0

   Generated file structure at /home/maik/develop/plone/plonetheme.tango

Now you have a new Python package in your current folder:

.. code-block:: bash

   (mrbobvenv)maik@planetmobile:~/develop/plone/plonetheme.tango
   $ ls
   bootstrap-buildout.py   buildout.cfg  CONTRIBUTORS.rst  MANIFEST.in  setup.py  travis.cfg
   bootstrap-buildout.pyc  CHANGES.rst   docs              README.rst   src

Deactivate mrbob virtualenv:

.. code-block:: bash

   (mrbobvenv)maik@planetmobile:~/develop/plone/plonetheme.tango$ deactivate


Bootstrap & buildout your development environment
-------------------------------------------------

You can run:

.. code-block:: bash

   $ python bootstrap-buildout.py
   Creating directory '/home/maik/develop/plone/plonetheme.tango/bin'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/parts'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/develop-eggs'.
   Generated script '/home/maik/develop/plone/plonetheme.tango/bin/buildout'.

Then you can run:

.. code-block:: bash

   $ ./bin/buildout

This will create the whole development environment for your package:

.. code-block:: bash

   $ ls bin/
   buildout                          code-analysis-hasattr
   code-analysis                     code-analysis-imports
   code-analysis-clean-lines         code-analysis-jscs
   code-analysis-csslint             code-analysis-jshint
   code-analysis-debug-statements    code-analysis-pep3101
   code-analysis-deprecated-aliases  code-analysis-prefer-single-quotes
   code-analysis-find-untranslated   code-analysis-utf8-header
   code-analysis-flake8              code-analysis-zptlint
   develop                           pildriver.py
   flake8                            pilfile.py
   fullrelease                       pilfont.py
   instance                          pilprint.py
   lasttagdiff                       postrelease
   lasttaglog                        prerelease
   longtest                          release
   pilconvert.py                     test


Start your Plone instance and play with your theme product
----------------------------------------------------------

To start the Plone instance, run:

.. code-block:: bash

   $ ./bin/instance fg

The Plone instance will then run on http://localhost:8080.
Add a Plone site ``Plone``.
Then activate/install your theme product on http://localhost:8080/Plone/prefs_install_products_form.
The theme will be automatically enabled.
If something is wrong with the theme,
you can always go to http://localhost:8080/Plone/@@theming-controlpanel and disable it.
This control panel will never be themed, so it works even if the theme might be broken.

Inspect your package source
---------------------------

Your package source code is in the ``src`` folder:

.. code-block:: bash

   $ tree src/plonetheme/tango/
   src/plonetheme/tango/
   ├── browser
   │   ├── configure.zcml
   │   ├── __init__.py
   │   ├── __init__.pyc
   │   ├── overrides
   │   └── static
   ├── configure.zcml
   ├── __init__.py
   ├── interfaces.py
   ├── locales
   │   ├── plonetheme.tango.pot
   │   └── update.sh
   ├── profiles
   │   ├── default
   │   │   ├── browserlayer.xml
   │   │   ├── metadata.xml
   │   │   ├── plonethemetango_default.txt
   │   │   └── theme.xml
   │   └── uninstall
   │       ├── browserlayer.xml
   │       ├── plonethemetango_uninstall.txt
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
       ├── index.html
       ├── manifest.cfg
       ├── rules.xml
       └── template-overrides

   11 directories, 25 files

As you see, the package already contains a Diazo theme:

.. code-block:: bash

   $ tree src/plonetheme/tango/theme/
   src/plonetheme/tango/theme/
   ├── index.html
   ├── manifest.cfg
   ├── rules.xml
   └── template-overrides

Here you can build your Diazo theme.


Build your Diazo-based theme
============================

You can start with the example files in the theme folder,
or with your own static HTML mockup,
or you can use the Plone 5 default ``Barceloneta`` theme as a starting point.

Use your own static mockup
--------------------------

If you got a static mockup from your designer or from a website like
http://startbootstrap.com (where the example theme came from), you can use this
without customization and just apply the Diazo rules to it.
Another way is to change the static mockup a little bit to use mostly the same
CSS ids and classes. This way it is easier to reuse CSS/LESS from Barceloneta
theme if you want.


Download and prepare a static theme
+++++++++++++++++++++++++++++++++++

Let's start with an untouched static theme, such as this bootstrap theme:
http://startbootstrap.com/template-overviews/business-casual/.
Just download it and extract it into the theme folder:

.. code-block:: bash

   $ tree .
   .
   ├── about.html
   ├── blog.html
   ├── contact.html
   ├── css
   │   ├── bootstrap.css
   │   ├── bootstrap.min.css
   │   ├── bundle.less
   │   ├── business-casual.css
   │   └── main.less
   ├── fonts
   │   ├── glyphicons-halflings-regular.eot
   │   ├── glyphicons-halflings-regular.svg
   │   ├── glyphicons-halflings-regular.ttf
   │   ├── glyphicons-halflings-regular.woff
   │   └── glyphicons-halflings-regular.woff2
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
   │   ├── bundle.js
   │   └── jquery.js
   ├── LICENSE
   ├── manifest.cfg
   ├── README.md
   ├── rules.xml
   └── template-overrides


Preparing the template
**********************

To make the given template more useful, we customize it a little bit.
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

And then move the main content (the box 2 and box 3 including the parent row
``div``) into the ``content-container``.

It should look like this:

.. code-block:: html

   <div class="row">
     <div id="column1-container"></div>

     <div id="content-container">
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
   </div>

   <div id="column2-container"></div>


Using Diazo rules to map the theme with Plone content
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Now that we have the static theme,
we need to apply the Diazo rules in ``rules.xml`` to map the Plone content
elements to the theme.

First let me explain what we mean when we talk about *content* and *theme*.
*Content* is usually the dynamic generated content on the Plone site, and the
*theme* is the static template site.

For example:

.. code-block:: xml

   <replace css:theme="#headline" css:content="#firstHeading" />

This means that the element ``#headline`` in the theme should be replaced by
the ``#firstHeading`` element from the generated Plone content.

For more details how to use Diazo rules, look at
http://docs.diazo.org/en/latest/ and
http://docs.plone.org/external/plone.app.theming/docs/index.html.


As a starting point we use this rules set:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <rules xmlns="http://namespaces.plone.org/diazo"
          xmlns:css="http://namespaces.plone.org/diazo/css"
          xmlns:xhtml="http://www.w3.org/1999/xhtml"
          xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
          xmlns:xi="http://www.w3.org/2001/XInclude">

     <theme href="index.html"/>
     <notheme css:if-not-content="#visual-portal-wrapper" />

     <rules css:if-content="#portal-top">
       <!-- Attributes -->
       <copy attributes="*" css:theme="html" css:content="html" />
       <!-- Base tag -->
       <before css:theme="head title" css:content="head base" />
       <!-- Title -->
       <replace css:theme="head title" css:content="head title" />
       <!-- Pull in Plone Meta -->
       <after css:theme-children="head" css:content="head meta" />
       <!-- dont use Plone icons, use the theme's -->
       <drop css:content="head link[rel='apple-touch-icon'], head link[rel='shortcut icon']" />
       <!-- CSS -->
       <after css:theme-children="head" css:content="head link" />
       <!-- Script -->
       <after css:theme-children="head" css:content="head script" />
     </rules>

     <!-- Copy over the id/class attributes on the body tag.
          This is important for per-section styling -->
     <copy attributes="*" css:content="body" css:theme="body" />

     <!-- toolbar -->
     <before
       css:theme-children="body"
       css:content-children="#edit-bar"
       css:if-not-content=".ajax_load"
       css:if-content=".userrole-authenticated"
       />

     <!-- login link -->
     <after
       css:theme-children="body"
       css:content="#portal-anontools"
       css:if-not-content=".ajax_load"
       css:if-content=".userrole-anonymous"
       />

     <!-- replace theme navbar-nav with Plone plone-navbar-nav -->
     <replace
       css:theme-children=".plone-navbar-nav"
       css:content-children=".plone-navbar-nav" />

     <!-- full-width breadcrumb -->
     <replace
       css:theme-children="#above-content"
       css:content-children="#viewlet-above-content"
       />
      <drop css:content="#portal-breadcrumbs" />

     <!-- Alert message -->
     <replace
       css:theme-children="#global_statusmessage"
       css:content-children="#global_statusmessage"
       />

     <!-- Central column -->
     <replace css:theme="#content-container" method="raw">

         <xsl:variable name="central">
           <xsl:if test="//aside[@id='portal-column-one'] and //aside[@id='portal-column-two']">col-xs-12 col-sm-6</xsl:if>
           <xsl:if test="//aside[@id='portal-column-two'] and not(//aside[@id='portal-column-one'])">col-xs-12 col-sm-9</xsl:if>
           <xsl:if test="//aside[@id='portal-column-one'] and not(//aside[@id='portal-column-two'])">col-xs-12 col-sm-9</xsl:if>
           <xsl:if test="not(//aside[@id='portal-column-one']) and not(//aside[@id='portal-column-two'])">col-xs-12 col-sm-12</xsl:if>
         </xsl:variable>

         <div class="{$central}">
           <div class="row">
             <div class="box">
               <div class="col-xs-12 col-sm-12">
                 <xsl:apply-templates css:select="#content" />
               </div>
               <div class="clearFix"></div>
             </div>
           </div>
           <section id="viewlet-below-content-body" class="row">
             <div class="box">
               <div class="col-xs-12 col-sm-12">
                <xsl:copy-of css:select="#viewlet-below-content" />
               </div>
               <div class="clearFix"></div>
             </div>
           </section>
         </div><!--/row-->
     </replace>

     <!-- Left column -->
     <rules css:if-content="#portal-column-one">
       <replace css:theme="#column1-container">
           <div class="col-xs-6 col-sm-3 sidebar-offcanvas">
             <aside id="portal-column-one">
                <xsl:copy-of css:select="#portal-column-one > *" />
             </aside>
           </div>
       </replace>
     </rules>

     <!-- Right column -->
     <rules css:if-content="#portal-column-two">
       <replace css:theme="#column2-container">
           <div class="col-xs-6 col-sm-3 sidebar-offcanvas" role="complementary">
             <aside id="portal-column-two">
                <xsl:copy-of css:select="#portal-column-two > *"/>
             </aside>
           </div>
       </replace>
     </rules>

     <replace css:theme-children="#portal-footer" css:content-children="#portal-footer-wrapper" />
   </rules>


Login link & co
***************

Add the login link:

.. code-block:: xml

   <!-- login link -->
   <after
     css:theme-children="body"
     css:content="#portal-anontools"
     css:if-not-content=".ajax_load"
     css:if-content=".userrole-anonymous"
     />

This will place the ``portal-anontools`` (for example the login link) on the
bottom of the page. You can change that to place it where you want.


Top-navigation
**************

Replace the placeholder with the real Plone top-navigation links:

.. code-block:: xml

   <!-- replace theme navbar-nav with Plone plone-navbar-nav -->
   <replace
     css:theme-children=".navbar-nav"
     css:content-children=".plone-navbar-nav" />

Here we take the list of links from Plone and replace the placeholder links in
the theme with it.


Breadcrumb & co
***************

Plone provides some viewlets like the breadcrumbs (the current path) above the content area.
To get this into the theme layout, we add a placeholder with the CSS id ``#above-content`` to the theme.
This is the place where we want to insert Plones "above-content" stuff.
For example at the top of the ``div.container`` after:

.. code-block:: html

    <!-- Navigation -->
    <nav class="navbar navbar-default" role="navigation">
        ...
    </nav>

    <div class="container">

        <!-- insert here -->

goes this before the row/box.

.. code-block:: html

       <div class="row">
           <div id="above-content" class="box"></div>
       </div>

This rule then inserts the Plone breadcrumbs etc.:

.. code-block:: xml

   <!-- full-width breadcrumb -->
   <replace
     css:theme-children="#above-content"
     css:content-children="#viewlet-above-content"
     />

This will bring over everything from the ``viewlet-above-content`` block from
Plone. Our current theme does not provide a breadcrumb bar, so we can just
drop them from Plone content, like this:

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
*************************

We want the slider in the template only on the front page, and we don't want it
when we are editing the front page. To make this easier, we wrap the slider
area with a ``#front-page-slider`` ``div``-tag like this:

.. code-block:: html

   <div id="front-page-slider">
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

Now we can drop it if we are not on the front page and also in some other situations:

.. code-block:: xml

   <!-- front-page slider -->
   <drop
     css:theme="#front-page-slider"
     css:if-not-content=".section-front-page" />
   <drop
     css:theme="#front-page-slider"
     css:if-content=".template-edit" />
   <drop
     css:theme="#front-page-slider"
     css:if-content=".template-topbar-manage-portlets" />

At the moment the slider is still static, but we will change that later.


Status messages
***************

Plone will render status messages in the ``#global_statusmessage`` element.
We want to bring these messages across to the theme.
For this, we add another placeholder into our theme template:

.. code-block:: html

   <div class="row">
       <div id="global_statusmessage"></div>
       <div id="above-content"></div>
   </div>

and use this rule to bring the messages across:

.. code-block:: xml

  <!-- Alert message -->
  <replace
    css:theme-children="#global_statusmessage"
    css:content-children="#global_statusmessage"
    />

To test that, just edit the front page. You should see a confirmation-message from Plone.

Main content area
*****************

To get the Plone content area in a flexible way which also provides the right
bootstrap grid classes, we use an inline XSL snippet like this:

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
         <div class="row">
           <div class="box">
             <div class="col-xs-12 col-sm-12">
               <xsl:apply-templates css:select="#content" />
             </div>
             <div class="clearFix"></div>
           </div>
         </div>
         <section id="viewlet-below-content-body" class="row">
           <div class="box">
             <div class="col-xs-12 col-sm-12">
              <xsl:copy-of css:select="#viewlet-below-content" />
             </div>
             <div class="clearFix"></div>
           </div>
         </section>
       </div><!--/row-->
   </replace>

This will add the right grid-classes to the content columns depending on one-column-, two-column- or tree-column-layout.


Left and right columns
**********************

We have already added the ``column1-container`` and ``column2-container`` ids  to our template.
The following rules will incorporate the left and the right columns from Plone
into the theme, and also change their markup to be an ``aside`` instead of a
normal ``div``. That is the reason to use inline XSL here:

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


Footer
******

Bring across the footer from Plone:

.. code-block:: xml

   <!-- footer -->
   <replace
     css:theme-children="footer .container"
     css:content-children="#portal-footer-wrapper" />


CSS and JS resources
++++++++++++++++++++

First let's make sure that we have loaded the ``registerless`` profile of
Barceloneta.
To do that, we change our ``metadata.xml`` as follows:

.. code:: xml

   <?xml version="1.0"?>
   <metadata>
     <version>1000</version>
     <dependencies>
       <dependency>profile-plone.app.theming:default</dependency>
       <dependency>profile-plonetheme.barceloneta:registerless</dependency>
     </dependencies>
   </metadata>

This will register all LESS files of the Barceloneta theme in Plone's resource
registry, so that we can use them in our custom LESS files.

Now let's add the two LESS files ``main.less`` and ``custom.less`` to our CSS
folder:

.. code-block:: bash

   $ tree ./css/
   ./css/
   ├── bootstrap.css
   ├── bootstrap.min.css
   ├── business-casual.css
   ├── custom.less
   └── main.less

The ``main.less`` file can look like this:

.. code-block:: sass

   /* bundle less file that will be compiled into tango-compiled.css */

   // ### PLONE IMPORTS ###

   //*// Font families
   //@import "@{barceloneta-fonts}";

   //*// Core variables and mixins
   @import "@{barceloneta-variables}";
       @import "@{barceloneta-mixin-prefixes}";
       @import "@{barceloneta-mixin-tabfocus}";
       @import "@{barceloneta-mixin-images}";
       @import "@{barceloneta-mixin-forms}";
       @import "@{barceloneta-mixin-borderradius}";
       @import "@{barceloneta-mixin-buttons}";
       @import "@{barceloneta-mixin-clearfix}";
   //  @import "@{barceloneta-mixin-gridframework}";
   //  @import "@{barceloneta-mixin-grid}";


   //*// Reset and dependencies
   @import "@{barceloneta-normalize}";
   @import "@{barceloneta-print}";

   //*// Core CSS
   @import "@{barceloneta-scaffolding}";
   @import "@{barceloneta-type}";
   @import "@{barceloneta-code}";
   //@import "@{barceloneta-deco}"; //uncomment for deco variant
   //@import "@{barceloneta-grid}";
   @import "@{barceloneta-tables}";
   @import "@{barceloneta-forms}";
   @import "@{barceloneta-buttons}";
   @import "@{barceloneta-states}";

   //*// Components
   @import "@{barceloneta-breadcrumbs}";
   @import "@{barceloneta-pagination}";
   @import "@{barceloneta-formtabbing}";
   @import "@{barceloneta-views}";
   @import "@{barceloneta-thumbs}";
   @import "@{barceloneta-alerts}";
   @import "@{barceloneta-portlets}";
   @import "@{barceloneta-controlpanels}";
   @import "@{barceloneta-tags}";
   @import "@{barceloneta-contents}";

   //*// Patterns
   @import "@{barceloneta-accessibility}";
   @import "@{barceloneta-toc}";
   @import "@{barceloneta-dropzone}";
   @import "@{barceloneta-modal}";
   @import "@{barceloneta-pickadate}";
   @import "@{barceloneta-sortable}";
   @import "@{barceloneta-tablesorter}";
   @import "@{barceloneta-tooltip}";
   @import "@{barceloneta-tree}";

   //*// Structure
   @import "@{barceloneta-header}";
   @import "@{barceloneta-sitenav}";
   @import "@{barceloneta-main}";
   //@import "@{barceloneta-footer}";
   @import "@{barceloneta-loginform}";
   @import "@{barceloneta-sitemap}";

   //*// Products
   @import "@{barceloneta-event}";
   @import "@{barceloneta-image}";
   @import "@{barceloneta-behaviors}";
   @import "@{barceloneta-discussion}";
   @import "@{barceloneta-search}";

   //*// Products
   @import "@{barceloneta-event}";
   @import "@{barceloneta-image}";
   @import "@{barceloneta-behaviors}";
   @import "@{barceloneta-discussion}";
   @import "@{barceloneta-search}";

   // ### END OF PLONE IMPORTS ###

   // include theme css as less
   @import (less) "business-casual.css";

   // include our custom less
   @import "custom.less";

Here we import a number of specific parts from the default Plone 5 Barceloneta theme.
Feel free to comment out stuff that you don't need.

At the bottom you can see that we import the ``business-casual.css`` as a LESS
file, as well as our new ``custom.less`` file.
The ``business-casual.css`` comes from the downloaded static theme and is
included to reduce the amount of CSS files.

The ``custom.less`` will contain our custom styles and can look like this:

.. code-block:: css

   h1 {
     color: green;
   }

Before we register our bundle, let's also add a JavaScript file with the
following content as ``js/bundle.js``:

.. code-block:: js

   /* This is a bundle that uses RequireJS to pull in dependencies.
      These dependencies are defined in the registry.xml file */


   /* do not include jquery multiple times */
   if (window.jQuery) {
     define('jquery', [], function() {
       return window.jQuery;
     });
   }

   require([
     'jquery',
   ], function($, dep1, logger){
     'use strict';

     // initialize only if we are in top frame
     if (window.parent === window) {
       $(document).ready(function() {
         $('body').addClass('tango-main');
       });
     }

   });


We now have to register our resources in a bundle. We could use the new
resource registry directly, but to make this training much simpler and
easier to understand, we'll prefer to use the new options in ``manifest.cfg``.
Those allow us to register our CSS and JS in a pre-built implicit ``diazo``
bundle that is only delivered when Diazo transformations are enabled (which
is default) in ``@@theming-controlpanel``.

So we extend our theme's ``manifest.cfg`` to declare ``development-css``,
``production-css`` and optionally ``tinymce-content-css``, like this:


.. code-block:: xml

   [theme]
   title = plonetheme.tango
   description = An example diazo theme
   rules = /++theme++plonetheme.tango/rules.xml
   prefix = /++theme++plonetheme.tango
   doctype = <!DOCTYPE html>
   enabled-bundles =
   disabled-bundles =

   development-css = /++theme++plonetheme.tango/css/main.less
   production-css = /++theme++plonetheme.tango/css/tango-compiled.css
   tinymce-content-css = /++theme++plonetheme.tango/css/business-casual.css

   [theme:overrides]
   directory = template-overrides

   [theme:parameters]
   ajax_load = python: request.form.get('ajax_load')
   portal_url = python: portal.absolute_url()


The last of these tells Plone to load that particular CSS file wherever a
TinyMCE rich text field is displayed. Good for specific overrides and stylings.

After adding the manifest changes, we need to deactivate/activate the theme
for them to take effect. Just go to ``/@@theming-controlpanel`` and do it.


Extend your buildout configuration
++++++++++++++++++++++++++++++++++

Add the following buildout parts, if they don't already exist:

.. code-block:: ini

   [zopepy]
   recipe = zc.recipe.egg
   eggs =
       ${instance:eggs}
       ${test:eggs}
   interpreter = zopepy
   scripts =
       zopepy
       plone-generate-gruntfile
       plone-compile-resources

   [omelette]
   recipe = collective.recipe.omelette
   eggs = ${instance:eggs}


And add these parts to the list of parts:

.. code-block:: ini

   parts=
       ...
       zopepy
       omelette

Also add ``Products.CMFPlone`` to the eggs list in the ``instance`` part:

.. code-block:: ini

   [instance]
   recipe = plone.recipe.zope2instance
   user = admin:admin
   http-address = 8080
   eggs =
       Plone
       Pillow
       Products.CMFPlone
       plonetheme.tango [test]

Now rerun buildout:

.. code-block:: bash

   $ ./bin/buildout

This will generate some new scripts including ``plone-compile-resources`` and
``plone-generate-gruntfile`` in the ``bin`` folder:

.. code-block:: bash

   $ ls bin/
   buildout                            flake8
   check-manifest                      fullrelease
   code-analysis                       instance
   code-analysis-check-manifest        lasttagdiff
   code-analysis-clean-lines           lasttaglog
   code-analysis-csslint               longtest
   code-analysis-debug-statements      pilconvert.py
   code-analysis-deprecated-aliases    pildriver.py
   code-analysis-find-untranslated     pilfile.py
   code-analysis-flake8                pilfont.py
   code-analysis-hasattr               pilprint.py
   code-analysis-imports               plone-compile-resources
   code-analysis-jscs                  plone-generate-gruntfile
   code-analysis-jshint                postrelease
   code-analysis-pep3101               prerelease
   code-analysis-prefer-single-quotes  release
   code-analysis-utf8-header           test
   code-analysis-zptlint               zopepy
   develop

You can use ``./bin/plone-compile-resources`` to build your resource bundle as
detailed below, but you first have to start the instance and add a Plone site
named ``Plone``, because the compilation process depends on the resource
registries of the live site.

We also need ``grunt`` installed on our system.

.. code-block:: bash

   sudo npm install -g grunt-cli
   sudo npm install -g grunt

If you get errors like this:

.. code-block:: bash

   ERR! Error: failed to fetch from registry: grunt

then use this as a workaround and try again:

.. code-block:: bash

   npm config set registry http://registry.npmjs.org/

.. note:: You have to rebuild the bundle whenever you make changes to your LESS/CSS files.

To test changes in LESS files you can build/rebuild your bundle TTW in Plone's
``resource registry`` control panel.
Just go to ``@@resourceregistry-controlpanel`` and press *Build* for the tango-bundle.

.. TODO:: show some screenshots here.

Alternatively, you can use the ``plone-compile-resources`` script to rebuild the bundle.
If you are running a ZEO cluster with multiple clients, you can run this script at any time.
If not, you have to stop your instance first, because the script needs to write to the ZODB.

.. code-block:: bash

   $ ./bin/plone-compile-resources --bundle=tango-bundle

This will start the Plone instance, read variables from the registry, and
compile your bundle.

If your Plone site is not named ``Plone``, you can provide the id using the
``--site-id`` parameter.

After you compiled your bundle with the ``plone-compile-resources`` once,
you can use the generated ``Gruntfile.js`` and recompile your bundle as follows:

.. code-block:: bash

   $ grunt compile-tango-bundle

The name of our bundle is ``tango-bundle``. You can find the name of the
generated *Grunt task* to compile your bundle at the bottom of the
``Gruntfile.js``.

.. note::

    This Grunt-only method is much faster than using the
    ``plone-compile-resources`` script, but it cannot be used in all
    circumstances.

   Specifically, you can use this direct method until you change something in
   the resources and bundle registration.  Then you have to use the
   ``plone-compile-resources`` once again, before you can use the pure Grunt
   method.


.. Using parts of Bootstrap
.. +++++++++++++++++++++++

.. Since Plone already uses Bootstrap internally, we only need to load some parts of Bootstrap which does not come with Plone.
.. To find out what parts of Bootstrap Plone uses already, you can look into ``Products/CMFPlone/profiles/dependencies/registry.xml`` or in the Resource Registry TTW.
.. But I would recommend the ``registry.xml`` file because, it is easier to search in.
.. So if you search for bootstrap in the ``registry.xml`` you will find out that Plone uses at least the follwing parts of Bootstrap already:

.. LESS files
.. **********

.. * less/variables.less
.. * less/mixins.less
.. * less/utilities.less
.. * less/forms.less
.. * less/navs.less
.. * less/navbar.less
.. * less/progress-bars.less
.. * less/modals.less
.. * less/button-groups.less
.. * less/buttons.less
.. * less/close.less
.. * less/dropdowns.less
.. * less/glyphicons.less
.. * less/badges.less

.. Javascript files
.. ****************

.. * js/alert.js
.. * js/dropdown.js
.. * js/collapse.js
.. * js/tooltip.js
.. * js/transition.js


Load LESS parts of Bootstrap
****************************

To load for example the carousel we first install the LESS version of Bootstrap
into our theme.
To do that, we use ``bower``, which you should have globally installed on your
system.
First we initialize our theme package. To do that, we run the following command
inside our theme folder:

.. code-block:: bash

   $ bower init

This command will ask you some questions, which are all irrelevant for our purposes.  So we can accept all the default answers, except perhaps marking the package as private, as a precaution.  After this we have a bower config file called
``bower.json``.
All the packages that we need for our theme should be mentioned in this
``bower.json`` file.

Now we install bootstrap, using bower:

.. code-block:: bash

   $ bower install bootstrap --save

The ``--save`` option will add the package to ``bower.json`` for us.
Now, we can install all dependencies on any other system by running the
following command from inside of our theme folder:

.. code-block:: bash

   $ bower install

Now that we have installed bootstrap using bower, we have all bootstrap
components available in the subfolder called ``bower_components``:

.. code-block:: bash

   $ tree bower_components/bootstrap/
   bower_components/bootstrap/
   ├── bower.json
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
   ├── package.js
   ├── package.json
   └── README.md

To include the needed "carousel" part and some other bootstrap components which
our downloaded theme uses, we change the end of our ``main.less`` like this:

.. code-block:: css

   // ### UTILS ###

   // import bootstrap variables from Plone -->
   @import "@{bootstrap-variables}";

   // import needed bootstrap less files from bower_components
   @import "../bower_components/bootstrap/less/mixins.less";
   @import "../bower_components/bootstrap/less/utilities.less";

   @import "../bower_components/bootstrap/less/forms.less";
   @import "../bower_components/bootstrap/less/navs.less";
   @import "../bower_components/bootstrap/less/navbar.less";
   @import "../bower_components/bootstrap/less/carousel.less";

   // ### END OF UTILS ###


   // include theme css as less
   @import (less) "business-casual.css";

   // include our custom less
   @import "custom.less";


Final CSS customization
+++++++++++++++++++++++

To make our theme look nicer, we add some CSS as follows to our ``custom.less``
file:

.. code:: css

   /* Custom LESS file that is included from the main.less file */

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


More Diazo and plone.app.theming details
****************************************

For more details how to build a Diazo based theme, look at http://docs.diazo.org/en/latest/ and http://docs.plone.org/external/plone.app.theming/docs/index.html.
