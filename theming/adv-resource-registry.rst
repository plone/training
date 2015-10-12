=================================
Advanced resources registry usage
=================================

In the Plone ``resource registry`` we can register our static resources, like CSS and LESS files and also JavaScript resources. We will cover here only the CSS and LESS part but you can do also nice things with your JavaScript resources, for example using requireJS to do the import the right way without hassle with the right order of all the JavaScript files which are registered like before. But for details look into the documentation of the ``resource registry`` and in the JavaScript part of the training.

Registering CSS/LESS resources in the registry
==============================================

Because of the flexibility of LESS over CSS we will only use LESS files here, but you can also register static CSS files the same way. LESS files have the advantage that we can use imports inside the less files and with the reference-imports we can even only import parts of the files which we are really using.

Let's see how we can register a resource in the ``resource registry``. For that we add a IResourceRegistry entry into the registry.xml in our profiles/default folder:

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>
   </registry>

This registers a file named main.less from our theme package as a ``resource`` named tango-main.
We can now add this resource to a ``resource bundle`` like the existing ``plone`` bundle.

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>

       <records prefix="plone.bundles/plone"
                 interface='Products.CMFPlone.interfaces.IBundleRegistry'>
         <value key="resources" purge="false">
           <element>tango-main</element>
         </value>
       </records>
   </registry>

This has the advantage of reducing the amount of bundles, which also means reducing the amount of files which are loaded for the site. Because every bundle will result in one compiled CSS files and one compiled JavavScript file.
So if we have multiple LESS resources in the same bundle, it will be merged into on compiled CSS file.

But we can also create our own bundle which contains our resource:

.. code-block:: xml

   <?xml version="1.0"?>
   <registry>
       <records prefix="plone.resources/tango-main"
                 interface='Products.CMFPlone.interfaces.IResourceRegistry'>
          <value key="css">
             <element>++theme++plonetheme.tango/css/main.less</element>
          </value>
       </records>

       <!-- bundle definition -->
       <records prefix="plone.bundles/tango-bundle"
                 interface='Products.CMFPlone.interfaces.IBundleRegistry'>
         <value key="resources">
           <element>tango-main</element>
         </value>
         <value key="enabled">True</value>
         <value key="compile">True</value>
         <value key="csscompilation">++theme++plonetheme.tango/css/tango-compiled.css</value>
         <value key="last_compilation"></value>
       </records>
   </registry>

This can make sense if we only want to load that bundle under certain conditions, like in a specific context.
This could lead to a smaller size of loaded static resources, when the are not all needed.

After making changes to the registry, like adding resources to a bundle, you have to reload the registry configuration thru an upgrade step or thru a reinstall of the package.

The concerning bundle has to build/rebuild then. You can do this in the ``@@resourceregistry-controlpanel`` by clicking on build for the concerning bundle or by running the ``plone-compile-resources`` script like follow:

.. code-block:: bash

   $ ./bin/plone-compile-resources --bundle=plone

.. note:: Unfortunately the ``plone-compile-resources`` does not work currently with multiple resources in a bundle. But i hope that this will fixed soon.

If you have created your own bundle, do the same for this bundle:

.. code-block:: bash

   $ ./bin/plone-compile-resources --bundle=tango-bundle

Using resources in LESS-files
=============================

Let's have a look at our ``main.less`` file:

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

Here we use different functionality of LESS and the ``resource registry``.

At he bottom for example, we use LESS-imports to import a second less file which contains our custom LESS statements.
And we also import a CSS-file of the downloaded theme as a LESS-file. So we could change parts of it using LESS-syntax.

Above these two imports, we import stuff from Barceloneta. Here we can see, that we use the names of the registered ``resource registry`` resources of the Barceloneta theme to import them. So if for example one wants to import our registered resource ``tango-main`` she could import it like below in her LESS-file:

.. code-block:: css

   @import "@{tango-main}";

or even with the reference option:

.. code-block:: css

   @import (reference) "@{tango-main}";

If you use the ``reference`` option on LESS-import only parts of this file which are used are included in the compiled version (CSS).

So for example you have to trigger it like:

.. code-block:: css

   .greenBox{
       &:extend(.box);
       background: green;
   }

or with the all option, see http://lesscss.org/features/#extend-feature:

.. code-block:: css

   .greenBox{
       &:extend(.box all);
       background: green;
   }

or just use it as a mixin like this:

.. code-block:: css

   .documentDescription{
     .intro-text;
   }

