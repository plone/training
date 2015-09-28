===================================
Create a Plone theme python package
===================================

Creating a theme product with the Diazo inline editor is an easy way to start
and to test, but it is not a solid long term solution.

Even if ``plone.app.theming`` allows to import and export a Diazo theme as a ZIP
archive, it might be prefereable to manage your theme into an actual Plone
product.

One of the most obvious reason is it will allow you to override Plone elements
that are not accessible from the pure Diazo features (like overloading content
views templates, viewlets, configuration settings, etc.).

Create a product to handle your Diazo theme
===========================================

To create a Plone 5 theme skeleton, you will use mrbob's templates for Plone.

Install mr.bob and bobtemplates.plone
-------------------------------------

To install mr.bob you can do::

   $ pip install mr.bob

and to install the needed bobtemplates for Plone, do::

   $ pip install bobtemplates.plone

Create a Plone 5 theme product skeleton with mrbob::

   $ mrbob -O plonetheme.tango bobtemplates:plone_addon

It will ask you some question::

   --> What kind of package would you like to create? Choose between 'Basic', 'Dexterity', and 'Theme'. [Basic]: Theme

here choose Theme and fill out the rest of the questions as you like::

   --> Author's name [MrTango]:

   --> Author's email [md@derico.de]:

   --> Author's github username: MrTango

   --> Package description [An add-on for Plone]: Plone theme tango

   --> Plone version [4.3.6]: 5.0b3

   Generated file structure at /home/maik/develop/plone/plonetheme.tango

Now you have a new python package in your current folder::

   (mrbob)maik@planetmobile:~/develop/plone/plonetheme.tango
   $ ls
   bootstrap-buildout.py   buildout.cfg  CONTRIBUTORS.rst  MANIFEST.in  setup.py  travis.cfg
   bootstrap-buildout.pyc  CHANGES.rst   docs              README.rst   src

Deactivate mrbob virtualenv::

   (mrbob)maik@planetmobile:~/develop/plone/plonetheme.tango$ deactivate


Bootstrap & buildout your development environment
-------------------------------------------------

You can run::

   $ python bootstrap-buildout.py
   Creating directory '/home/maik/develop/plone/plonetheme.tango/bin'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/parts'.
   Creating directory '/home/maik/develop/plone/plonetheme.tango/develop-eggs'.
   Generated script '/home/maik/develop/plone/plonetheme.tango/bin/buildout'.

Then you can run::

   $ ./bin/buildout

This will create the whole develoment environment for your package::

   $ ls bin/
   buildout                          code-analysis-hasattr               develop        pildriver.py
   code-analysis                     code-analysis-imports               flake8         pilfile.py
   code-analysis-clean-lines         code-analysis-jscs                  fullrelease    pilfont.py
   code-analysis-csslint             code-analysis-jshint                instance       pilprint.py
   code-analysis-debug-statements    code-analysis-pep3101               lasttagdiff    postrelease
   code-analysis-deprecated-aliases  code-analysis-prefer-single-quotes  lasttaglog     prerelease
   code-analysis-find-untranslated   code-analysis-utf8-header           longtest       release
   code-analysis-flake8              code-analysis-zptlint               pilconvert.py  test


Start your Plone instance and play with your theme product
----------------------------------------------------------

To start the plone instanc, run::

   $ ./bin/instance fg

The Plone instance will then run on http://localhost:8080.
Add a Plone site ``Plone``.
Then activate/install your theme product on http://localhost:8080/Plone/prefs_install_products_form.
The theme will be automatically enabled. If some think is wrong with the theme, you can always go to http://localhost:8080/Plone/@@theming-controlpanel and disable it. This control panel will never be themed, so it works regardless the theme might be broken.


Inspect your package source
---------------------------

Your package source code is in the src folder::

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

As you see, the package contains already a Diazo theme::

   $ tree src/plonetheme/tango/theme/
   src/plonetheme/tango/theme/
   ├── index.html
   ├── manifest.cfg
   ├── rules.xml
   └── template-overrides

Here you can build your Diazo theme.


Build your Diazo based theme
============================

You can start with the example files in the theme folder, your own static html mockup or you use the Plone 5 default theme ``Barceloneta`` as a starting point.

Use your own static mockup
--------------------------

If you got a static mockup from your designer or from a website like http://startbootstrap.com where the example theme came from, you can use this without customization and just apply the Diazo rules on it. Another way is, to change the static mockup a little bit to use mostly the same css id's and classes. This way it is easier to reuse css/less from Barceloneta theme if you want.


Download and prepare a static theme
+++++++++++++++++++++++++++++++++++

Lets start with an untouched static theme like this bootstrap theme http://startbootstrap.com/template-overviews/business-casual/. Just download it and extract it into the theme folder::

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
Right before the second box which contains::

   <div class="row">
       <div class="box">
           <div class="col-lg-12">
               <hr>
               <h2 class="intro-text text-center">Build a website
                   <strong>worth visiting</strong>
               </h2>

Add this::

   <div id="column1-container"></div>
   <div id="content-container">
     <!-- main content (box2 and box3) comes here -->
   </div>
   <div id="column2-container"></div>

And then move the main content (the box 2 and box 3 including the parent row div) into the content-container.

It should look like::

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

   <div id="column2-container"></div>


Using Diazo rules to map the theme with Plone content
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Now that we have the static theme inside, we need to apply the Diazo rules in rules.xml to map the theme with the Plone content elements.

First let me explane what we mean, when we talk about content and theme.
Content is normaly the dynamic generated content on the Plone site and theme
is the static template site.

For exaple::

   <replace css:theme="#headline" css:content="#firstHeading" />

This means replace the element "#headline" in the theme with the element "#firstHeading" from the gerated Plone content.

For more details how to use Diazo rules, look at http://diazo.org and http://docs.plone.org/external/plone.app.theming/docs/index.html.


As a starting point we use this rules set::

   <?xml version="1.0" encoding="utf-8"?>
   <rules xmlns="http://namespaces.plone.org/diazo"
          xmlns:css="http://namespaces.plone.org/diazo/css"
          xmlns:xhtml="http://www.w3.org/1999/xhtml"
          xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
          xmlns:xi="http://www.w3.org/2001/XInclude">

     <theme href="index.html"/>
     <notheme css:if-not-content="#visual-portal-wrapper" />

     <rules if-content="//*[@id='portal-top']">
       <!-- Attributes -->
       <copy attributes="*" theme="/html" content="/html"/>
       <!-- Base tag -->
       <before theme="/html/head/title" content="/html/head/base"/>
       <!-- Title -->
       <replace theme="/html/head/title" content="/html/head/title" />
       <!-- Pull in Plone Meta -->
       <after theme-children="/html/head" content="/html/head/meta" />
       <!-- dont use Plone icons, use the theme -->
       <drop css:content="head link[rel='apple-touch-icon']" />
       <drop css:content="head link[rel='shortcut icon']" />
       <!-- CSS -->
       <after theme-children="/html/head" content="/html/head/link" />
       <!-- Script -->
       <after theme-children="/html/head" content="/html/head/script" />
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
      <drop
       css:content="#portal-breadcrumbs"
       />

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
                 <xsl:apply-templates css:select="#content"/>
               </div>
               <div class="clearFix"></div>
             </div>
           </div>
           <section class="row" id="viewlet-below-content-body">
             <div class="box">
               <div class="col-xs-12 col-sm-12">
                <xsl:copy-of select="//div[@id='viewlet-below-content']"/>
               </div>
               <div class="clearFix"></div>
             </div>
           </section>
         </div><!--/row-->
     </replace>

     <!-- Left column -->
     <rules if-content="//*[@id='portal-column-one']">
       <replace css:theme="#column1-container">
           <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar">
             <aside id="portal-column-one">
                <xsl:copy-of select="//*[@id='portal-column-one']/*"/>
             </aside>
           </div>
       </replace>
     </rules>

     <!-- Right column -->
     <rules if-content="//*[@id='portal-column-two']">
       <replace css:theme="#column2-container">
           <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar" role="complementary">
             <aside id="portal-column-two">
                <xsl:copy-of select="//*[@id='portal-column-two']/*"/>
             </aside>
           </div>
       </replace>
     </rules>

     <replace css:theme-children="#portal-footer" css:content-children="#portal-footer-wrapper" />
   </rules>

Slider only on Front-page
*************************

We want the slider in the template only on front-page and also not when we are editing the front-page.
So we drop it in these cases::

   <!-- front-page slider -->
   <drop
     css:theme="#front-page-slider"
     css:if-not-content=".section-front-page" />
   <drop
     css:theme="#front-page-slider"
     css:if-content=".template-edit" />

By now the slide is still static, but we will change that later.

Login link & co
***************

Add the login link::

   <!-- login link -->
   <after
     css:theme-children="body"
     css:content="#portal-anontools"
     css:if-not-content=".ajax_load"
     css:if-content=".userrole-anonymous"
     />

This will place the portal-anontools for example the login link on bottom of the page.
You can change that to place it where you want.

Top-navigation
**************

Replace the place holder with the real Plone top-navigation links::

   <!-- replace theme navbar-nav with Plone plone-navbar-nav -->
   <replace
     css:theme-children=".navbar-nav"
     css:content-children=".plone-navbar-nav" />

Here we take the list of links from Plone and replace the placeholder links in the theme with it.

Breadcrumb & co
***************

Plone provides some viewlets like the breadcrumb above the content area.
To get this, we add a place holder with the CSS id "#above-content" into the theme, where we want to have this above -content stuff, for example right before the first row/box in the container::

   <div class="row">
       <div id="above-content" class="box"></div>
   </div>

This rule then takes the Plone breadcrumb & co over::

   <!-- full-width breadcrumb -->
   <replace
     css:theme-children="#above-content"
     css:content-children="#viewlet-above-content"
     />

This will take over everthing in viewlet-above from Plone.
Our current theme does not provide a breadcrumb bar, so we can just drop them from Plone content, like this::

   <drop css:content="#portal-breadcrumbs" />

If you only want to drop this for non administrators, you can do it like this::

   <drop
    css:content="#portal-breadcrumbs"
    css:if-not-content=".userrole-manager"
    />

or only for not logged-in users::

   <drop
    css:content="#portal-breadcrumbs"
    css:if-content=".userrole-anonymous"
    />

.. note::

   The classes like userrole-anonymous, are provided by Plone in the BODY-Tag.

Status messages
***************

Plone will give status messages in the #global_statusmessage element. We want to take over these messages.
For this, we add another placeholder into our theme template::

   <div class="row">
       <div id="global_statusmessage"></div>
       <div id="above-content"></div>
   </div>

and use this rule to take over the messages::

  <!-- Alert message -->
  <replace
    css:theme-children="#global_statusmessage"
    css:content-children="#global_statusmessage"
    />

To test that, just edit the front-page.
You should see a message from Plone.

Main content area
*****************

To get the Plone content area in a flexible way which also provides the right bootstrap grid classes, we use a inline XSL snippet like this::

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
               <xsl:apply-templates css:select="#content"/>
             </div>
             <div class="clearFix"></div>
           </div>
         </div>
         <section class="row" id="viewlet-below-content-body">
           <div class="box">
             <div class="col-xs-12 col-sm-12">
              <xsl:copy-of select="//div[@id='viewlet-below-content']"/>
             </div>
             <div class="clearFix"></div>
           </div>
         </section>
       </div><!--/row-->
   </replace>

This will give the the right grid-classes for the content-column depending on one-column-, two-column- or tree-column-layout.

Left and right columns
**********************

We already add the column1-container and column2-container in our template.
The following rules will take over the left and the right columns and also change the markup of it to be a aside instead of a normal div. That is the reason to use inline XSL here.

   <!-- Left column -->
   <rules if-content="//*[@id='portal-column-one']">
     <replace css:theme="#column1-container">
         <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar">
           <aside id="portal-column-one">
              <xsl:copy-of select="//*[@id='portal-column-one']/*"/>
           </aside>
         </div>
     </replace>
   </rules>

   <!-- Right column -->
   <rules if-content="//*[@id='portal-column-two']">
     <replace css:theme="#column2-container">
         <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar" role="complementary">
           <aside id="portal-column-two">
              <xsl:copy-of select="//*[@id='portal-column-two']/*"/>
           </aside>
         </div>
     </replace>
   </rules>

Footer
******

Take over the footer from Plone::

   <!-- footer -->
   <replace
     css:theme-children="footer .container"
     css:content-children="#portal-footer-wrapper" />


Initial css and js resources
++++++++++++++++++++++++++++

Now create folders for your css and javascript resources and add the first files::

   $ tree .
   .
   ├── css
   │   ├── bundle.less
   │   └── main.less
   ├── index.html
   ├── js
   │   └── bundle.js
   ├── manifest.cfg
   ├── rules.xml
   └── template-overrides

The bundle.less file can look like this::

   /* bundle less file that will be compiled */

   // ### PLONE IMPORTS ###

   // //*// Font families
   @import "@{barcelonetaLessPath}fonts.plone.less";

   // //*// Core variables and mixins
   @import "@{barcelonetaLessPath}variables.plone.less";
   @import "@{barcelonetaLessPath}mixin.prefixes.plone.less";
   @import "@{barcelonetaLessPath}mixin.tabfocus.plone.less";
   @import "@{barcelonetaLessPath}mixin.images.plone.less";
   @import "@{barcelonetaLessPath}mixin.forms.plone.less";
   @import "@{barcelonetaLessPath}mixin.borderradius.plone.less";
   @import "@{barcelonetaLessPath}mixin.buttons.plone.less";
   @import "@{barcelonetaLessPath}mixin.clearfix.plone.less";
   @import "@{barcelonetaLessPath}mixin.gridframework.plone.less"; //grid Bootstrap
   @import "@{barcelonetaLessPath}mixin.grid.plone.less"; //grid Bootstrap


   // //*// Reset and dependencies
   @import "@{barcelonetaLessPath}normalize.plone.less";
   @import "@{barcelonetaLessPath}print.plone.less";

   // //*// Core CSS
   @import "@{barcelonetaLessPath}scaffolding.plone.less";
   @import "@{barcelonetaLessPath}type.plone.less";
   @import "@{barcelonetaLessPath}code.plone.less";
   //@import "deco.plone.less"; //uncomment for deco variant
   @import "@{barcelonetaLessPath}grid.plone.less"; //grid Bootstrap
   @import "@{barcelonetaLessPath}tables.plone.less";
   @import "@{barcelonetaLessPath}forms.plone.less";
   @import "@{barcelonetaLessPath}buttons.plone.less";
   @import "@{barcelonetaLessPath}states.plone.less";

   //*// Components
   @import "@{barcelonetaLessPath}breadcrumbs.plone.less";
   @import "@{barcelonetaLessPath}pagination.plone.less";
   @import "@{barcelonetaLessPath}formtabbing.plone.less"; //pattern
   @import "@{barcelonetaLessPath}views.plone.less";
   @import "@{barcelonetaLessPath}thumbs.plone.less";
   @import "@{barcelonetaLessPath}alerts.plone.less";
   @import "@{barcelonetaLessPath}portlets.plone.less";
   @import "@{barcelonetaLessPath}controlpanels.plone.less";
   @import "@{barcelonetaLessPath}tags.plone.less";
   @import "@{barcelonetaLessPath}contents.plone.less";

   //*// Patterns
   @import "@{barcelonetaLessPath}accessibility.plone.less";
   @import "@{barcelonetaLessPath}toc.plone.less";
   //@import "@{barcelonetaLessPath}backdrop.plone.less"; Still no implemented on Plone
   @import "@{barcelonetaLessPath}dropzone.plone.less";
   //@import "@{barcelonetaLessPath}formautofocus.plone.less"; Still no implemented on Plone
   @import "@{barcelonetaLessPath}modal.plone.less";
   @import "@{barcelonetaLessPath}pickadate.plone.less";
   @import "@{barcelonetaLessPath}sortable.plone.less";
   @import "@{barcelonetaLessPath}tablesorter.plone.less";
   @import "@{barcelonetaLessPath}tooltip.plone.less";
   @import "@{barcelonetaLessPath}tree.plone.less";

   //*// Structure
   @import "@{barcelonetaLessPath}header.plone.less";
   @import "@{barcelonetaLessPath}sitenav.plone.less";
   @import "@{barcelonetaLessPath}main.plone.less";
   @import "@{barcelonetaLessPath}footer.plone.less";
   @import "@{barcelonetaLessPath}loginform.plone.less";
   @import "@{barcelonetaLessPath}sitemap.plone.less";

   //*// Products
   @import "@{barcelonetaLessPath}event.plone.less";
   @import "@{barcelonetaLessPath}image.plone.less";
   @import "@{barcelonetaLessPath}news.plone.less";
   @import "@{barcelonetaLessPath}discussion.plone.less";
   @import "@{barcelonetaLessPath}search.plone.less";

   //@import "@{barcelonetaLessPath}barceloneta.plone.less";

   // ### END OF PLONE IMPORTS ###

   @import "main.less";

Here we import the specific parts of the default Plone 5 Barceloneta theme.
Feel free to comment out staff that you don't needed.

At the bottom you can see, that we import the main.less file.
The main.less will contain your custom styles and can look like this::

   h1 {
     color: green;
   }


More Diazo and plone.app.theming details
****************************************

For more details how to build a Diazo based theme, look at http://diazo.org and http://docs.plone.org/external/plone.app.theming/docs/index.html.


Override Plone BrowserViews with jbot
=====================================

A large part of the Plone UI are provided by BrowserView or Viewlet templates.

That is the case for viewlets (all the blocks you can see when you call the url
``./@@manage-viewlets``).

.. note:: to override them from the ZMI, you can go to ``./portal_view_customizations``.

To overrides them from your theme product, the easiest way is to use
``z3c.jbot`` (Just a Bunch of Templates).

Since jbot is already included in the skeleton, you can just start using it, by putting in ``src/plonetheme/tango/browser/overrides/`` all the templates you want to override.
But you will need to name them by prefixing the template
name by its complete path to its original version.

For instance, to override ``colophon.pt`` from plone.app.layout, knowing this
template in a subfolder named ``viewlets``, you need to name it
``plone.app.layout.viewlets.colophon.pt``.

.. note:: ZMI > portal_view_customizations is an handy way to find the template path.

You can now restart Zope and re-install your product from the Plone control
panel (Site Setup > Add-ons).


Dynamic slider
==============

Create dynamic slider content in Plone
--------------------------------------

We need a custom view to render ower dynamic content for the slider in Plone.
There different ways to create views, for now we use a very simple template-only-view thru jbot and theming-plugins.

TODO: show views folder and custom slider-images view


Take over the dynamic slider content from Plone
-----------------------------------------------
::

   <replace
     css:theme="#carousel-example-generic"
     css:content="#carousel-example-generic"
     href="/slider-images/@@slider-images" />

